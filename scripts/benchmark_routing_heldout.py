#!/usr/bin/env python3
"""Offline skill-routing check on prompts the router was never tuned against.

    python scripts/benchmark_routing_heldout.py --arm v1=/path/to/snapshot --arm v2=. --out benchmarks/results/routing-heldout.json

The prompts and their acceptable skills were written by AI agents that saw only the skill catalog
(ids and descriptions), never the router code or its tests. Each prompt has 1-3 concerns; a concern
lists the skills a sensible expert would accept for that part of the request. Prompts are split in
two by a hash of their id: tune on `dev`, report on `test`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PROMPTS = REPO / 'benchmarks' / 'routing-heldout' / 'prompts.json'

SELECTOR = r'''
import json, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
prompts = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
sys.path.insert(0, str(root))
import bossku
assert Path(bossku.__file__).resolve().parent.parent == root, bossku.__file__
from bossku.skills import rank_skills, select_skill_stack
out = {}
for row in prompts:
    ranked = rank_skills(row["prompt"], root, limit=5)
    stack = select_skill_stack(row["prompt"], root, limit=5)
    out[row["id"]] = {
        "top": [sid for sid, _ in ranked],
        "primary": stack["primary"],
        "selected": [item["skill_id"] for item in stack["selected"]],
        "confident": stack["confident"],
    }
print(json.dumps(out))
'''


def split_of(prompt_id: str) -> str:
    return 'dev' if int(hashlib.sha1(prompt_id.encode()).hexdigest()[:8], 16) % 2 == 0 else 'test'


def wilson(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def run_selector(root: Path, prompts_file: Path) -> dict:
    out = subprocess.run([sys.executable, '-c', SELECTOR, str(root), str(prompts_file)],
                         capture_output=True, text=True, encoding='utf-8', timeout=900)
    if out.returncode:
        raise SystemExit(f'selector failed for {root}: {out.stderr[-800:]}')
    return json.loads(out.stdout)


def description_only(prompts: list[dict], root: Path) -> dict:
    """The same keyword baseline as scripts/benchmark_routing.py: skill ids and descriptions only."""
    sys.path.insert(0, str(root))
    from bossku.index import build_index
    from bossku.skills import NOT_INSTALLED  # noqa: F401  (keeps the import surface identical)
    from scripts.benchmark_routing import baseline_documents, baseline_rank
    documents, weights = baseline_documents(build_index(root)['skills'])
    return {row['id']: {'top': [sid for sid, _ in baseline_rank(row['prompt'], documents, weights, limit=5)]}
            for row in prompts}


def score(prompts: list[dict], answers: dict, with_stack: bool) -> dict:
    n = len(prompts)
    hits = {'top1': 0, 'top3': 0, 'first_concern': 0}
    coverage, covered_all, unsure, precision, sizes = [], 0, 0, [], []
    for row in prompts:
        concerns = [set(c) for c in row['concerns']]
        union = set().union(*concerns)
        answer = answers[row['id']]
        top = answer['top']
        primary = answer.get('primary') or (top[0] if top else None)
        hits['top1'] += primary in union
        hits['top3'] += bool(set(top[:3]) & union)
        if with_stack:
            chosen = set(answer['selected'])
            sizes.append(len(chosen))
            precision.append(len(chosen & union) / len(chosen) if chosen else 0.0)
            covered = sum(bool(chosen & c) for c in concerns) / len(concerns)
            coverage.append(covered)
            covered_all += covered == 1.0
            unsure += not answer['confident']
    result = {'prompts': n}
    for key, value in hits.items():
        if key == 'first_concern':
            continue
        low, high = wilson(value, n)
        result[key] = {'hits': value, 'rate': value / n if n else 0.0, 'ci': [low, high]}
    if with_stack:
        result['concern_coverage'] = sum(coverage) / n if n else 0.0
        result['all_concerns_covered'] = {'hits': covered_all, 'rate': covered_all / n if n else 0.0}
        result['not_confident'] = unsure
        result['stack_precision'] = sum(precision) / n if n else 0.0
        result['stack_size'] = sum(sizes) / n if n else 0.0
    return result


def paired(prompts: list[dict], first: dict, second: dict) -> dict:
    """Prompts one version got right and the other did not, with an exact two-sided sign-test p-value.

    Two intervals that overlap can still hide a real difference when both versions are scored on the same
    prompts; counting only the prompts where they disagree is the fair comparison.
    """
    def top1(answer: dict, row: dict) -> bool:
        union = set().union(*[set(c) for c in row['concerns']])
        got = answer[row['id']]
        return (got.get('primary') or (got['top'][0] if got['top'] else None)) in union

    def whole(answer: dict, row: dict) -> bool:
        chosen = set(answer[row['id']]['selected'])
        return all(chosen & set(c) for c in row['concerns'])

    result = {}
    for name, judge in (('top1', top1), ('whole_request', whole)):
        only_first = sum(judge(first, r) and not judge(second, r) for r in prompts)
        only_second = sum(judge(second, r) and not judge(first, r) for r in prompts)
        n = only_first + only_second
        tail = sum(math.comb(n, k) for k in range(min(only_first, only_second) + 1))
        result[name] = {'only_first': only_first, 'only_second': only_second,
                        'p_two_sided': min(1.0, 2 * tail / 2 ** n) if n else 1.0}
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--arm', action='append', default=[], help='NAME=BOSSKU_ROOT (repeatable)')
    parser.add_argument('--prompts', type=Path, default=PROMPTS)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--split', choices=['dev', 'test', 'all'], default='all')
    args = parser.parse_args()
    rows = json.loads(args.prompts.read_text(encoding='utf-8'))
    for row in rows:
        row['split'] = split_of(row['id'])
    arms = {}
    for spec in args.arm:
        name, _, root = spec.partition('=')
        arms[name] = Path(root).resolve()
    if not arms:
        parser.error('--arm NAME=ROOT is required')
    answers = {name: run_selector(root, args.prompts) for name, root in arms.items()}
    first_root = next(iter(arms.values()))
    answers['description-only'] = description_only(rows, first_root)
    report = {'prompts_file': str(args.prompts.relative_to(REPO)) if args.prompts.is_relative_to(REPO) else str(args.prompts),
              # line endings differ between Windows and Linux checkouts; the hash must not
              'prompts_sha256': hashlib.sha256(args.prompts.read_bytes().replace(b'\r\n', b'\n')).hexdigest(), 'splits': {}}
    for split in ('dev', 'test', 'all'):
        subset = [row for row in rows if split == 'all' or row['split'] == split]
        report['splits'][split] = {
            name: score(subset, answer, with_stack=name != 'description-only') for name, answer in answers.items()}
        if 'before' in answers and 'after' in answers:
            report['splits'][split]['_paired_after_vs_before'] = paired(subset, answers['after'], answers['before'])
        if split != 'all':
            report['splits'][split]['_domains'] = {}
            for domain in sorted({row['domain'] for row in subset}):
                part = [row for row in subset if row['domain'] == domain]
                report['splits'][split]['_domains'][domain] = {
                    name: score(part, answer, with_stack=name != 'description-only')['top1']['rate']
                    for name, answer in answers.items()}
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2), encoding='utf-8')
    shown = [args.split] if args.split != 'all' else ['dev', 'test', 'all']
    for split in shown:
        print(f'\n== {split} ({report["splits"][split][next(iter(answers))]["prompts"]} prompts)')
        print(f'{"method":<18}{"top-1":>8}{"top-3":>8}{"concerns covered":>18}{"all covered":>13}{"precision":>11}{"stack":>7}')
        for name in answers:
            s = report['splits'][split][name]
            cov = f'{100 * s["concern_coverage"]:.0f}%' if 'concern_coverage' in s else '-'
            allc = f'{100 * s["all_concerns_covered"]["rate"]:.0f}%' if 'all_concerns_covered' in s else '-'
            prec = f'{100 * s["stack_precision"]:.0f}%' if 'stack_precision' in s else '-'
            size = f'{s["stack_size"]:.1f}' if 'stack_size' in s else '-'
            print(f'{name:<18}{100 * s["top1"]["rate"]:>7.0f}%{100 * s["top3"]["rate"]:>7.0f}%{cov:>18}{allc:>13}{prec:>11}{size:>7}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
