#!/usr/bin/env python3
"""Offline skill-routing check on prompts the router was never tuned against.

    python scripts/benchmark_routing_heldout.py --arm v1=/path/to/snapshot --arm v2=. --out benchmarks/results/routing-heldout.json

The prompts and their acceptable skills were written by AI agents that saw only the skill catalog
(ids and descriptions), never the router code or its tests. Each prompt has 1-3 concerns; a concern
lists the skills a sensible expert would accept for that part of the request. Prompts are split in
two by a hash of their id: tune on `dev`, report on `test`.

The `description-only` keyword baseline reads the skill catalog of the first `--arm` (or `--baseline-arm`), so its score
depends on that arm. The output records the arm and a hash of the catalog (`baseline`) and each arm's git revision (`arms`).

Hint-policy arms (`--policy`) measure what the prompt hook would show, not what the router ranks. They run on the working
tree (or `--policy-root`) and take `--prompts` once per file, for example the fresh set that decides the smart-lean gate:

    python scripts/benchmark_routing_heldout.py --policy v1 v2 full_router listed_only v2_min_words_3
        --prompts benchmarks/routing-heldout/fresh.json --prompts benchmarks/routing-heldout/trivial.json
    (one command line)

    v1, v2          the hint as hint_mode v1 / v2 builds it (bossku.hint.pick_skills)
    full_router      no gate: the router's top 3 for every prompt, the ceiling
    listed_only      the same top 3 with only the skills `skills/lean.json` lists, i.e. what a host sees without any hint
    v2_min_words_3   v2 with MIN_WORDS 3 instead of 5 (read it on the `short` kind)

A prompt with no concerns needs no skill (follow-ups, chit-chat, trivial questions). Metrics, defined once:
  shown_rate               prompts with a hint / prompts
  precision                acceptable picks / picks shown (silence is not counted)
  concern_recall           gold concerns covered by the picks / gold concerns (silence covers none)
  all_concerns             prompts where every concern is covered / prompts with a gold concern
  primary_right_when_shown prompts whose first pick is acceptable / prompts with a gold concern and a hint
  no_skill_fire_rate       prompts that need no skill but got a hint / prompts that need no skill
  top1                     prompts whose first pick is acceptable (silence is a miss) / prompts with a gold concern
Splits: dev (tune) and test (report) from the hash of the id for prompts.json; fresh (decide) for the files whose rows
carry a `kind`. `multi_concern` is the subset with two or more concerns.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
import tempfile
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


POLICIES = ('v1', 'v2', 'full_router', 'listed_only', 'v2_min_words_3')

POLICY_SELECTOR = r'''
import json, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
prompts = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
policies = sys.argv[3].split(",")
sys.path.insert(0, str(root))
import bossku
assert Path(bossku.__file__).resolve().parent.parent == root, bossku.__file__
from bossku import hint, skills
data = skills._routing_index(root)
listed = set(skills.load_lean(root)["listed"])
out = {}
for row in prompts:
    answer = {}
    for name in policies:
        if name in ("full_router", "listed_only"):
            stack = skills.select_skill_stack(row["prompt"], root, limit=hint.MAX_HINTS, data=data,
                                              available=listed if name == "listed_only" else None)
            answer[name] = [item["skill_id"] for item in stack["selected"]]
        else:
            mode, words = ("v2", 3) if name == "v2_min_words_3" else (name, hint.MIN_WORDS)
            picks = hint.pick_skills(row["prompt"], root=root, mode=mode, min_words=words, data=data)
            answer[name] = [item["skill_id"] for item in picks]
    out[row["id"]] = answer
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


def description_only(prompts: list[dict], root: Path) -> tuple[dict, str]:
    """The same keyword baseline as scripts/benchmark_routing.py: skill ids and descriptions only.

    Also returns a hash of the catalog it read (skill ids and their description terms), so the saved file shows which
    catalog the baseline came from: the number moves with the skill list, not with the router.
    """
    sys.path.insert(0, str(root))
    from bossku.index import build_index
    from bossku.skills import NOT_INSTALLED  # noqa: F401  (keeps the import surface identical)
    from scripts.benchmark_routing import baseline_documents, baseline_rank
    documents, weights = baseline_documents(build_index(root)['skills'])
    catalog = sorted((sid, sorted(terms)) for sid, terms in documents.items())
    answers = {row['id']: {'top': [sid for sid, _ in baseline_rank(row['prompt'], documents, weights, limit=5)]}
               for row in prompts}
    return answers, hashlib.sha256(json.dumps(catalog).encode('utf-8')).hexdigest()


def arm_provenance(root: Path) -> dict:
    """Which code an arm ran: the git revision and whether skills or code were edited since (null outside a checkout)."""
    if not (root / '.git').exists():
        return {'git_revision': None, 'working_tree_modified': None}
    try:
        revision = subprocess.run(['git', '-C', str(root), 'rev-parse', '--short', 'HEAD'],
                                  capture_output=True, text=True, check=True).stdout.strip()
        status = subprocess.run(['git', '-C', str(root), 'status', '--porcelain', '--', 'bossku', 'skills'],
                                capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return {'git_revision': None, 'working_tree_modified': None}
    return {'git_revision': revision, 'working_tree_modified': bool(status.strip())}


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


def ratio(hits: int, n: int) -> dict:
    low, high = wilson(hits, n)
    return {'hits': hits, 'n': n, 'rate': hits / n if n else None, 'ci': [low, high]}


def hint_metrics(rows: list[dict], picks: dict) -> dict:
    """What the hint showed for these prompts (`picks`: prompt id -> skill ids shown, empty = silence), see the docstring."""
    gold = [row for row in rows if row['concerns']]
    quiet = [row for row in rows if not row['concerns']]
    shown_picks = acceptable = covered = concerns = all_covered = primary = gold_shown = 0
    for row in rows:
        chosen = picks[row['id']]
        union = set().union(*[set(c) for c in row['concerns']])
        shown_picks += len(chosen)
        acceptable += sum(sid in union for sid in chosen)
    for row in gold:
        chosen = picks[row['id']]
        union = set().union(*[set(c) for c in row['concerns']])
        hit = [bool(set(chosen) & set(c)) for c in row['concerns']]
        covered += sum(hit)
        concerns += len(hit)
        all_covered += all(hit)
        gold_shown += bool(chosen)
        primary += bool(chosen) and chosen[0] in union
    return {'prompts': len(rows), 'with_skill': len(gold), 'no_skill': len(quiet),
            'shown_rate': ratio(sum(bool(picks[row['id']]) for row in rows), len(rows)),
            'precision': ratio(acceptable, shown_picks),
            'concern_recall': ratio(covered, concerns),
            'all_concerns': ratio(all_covered, len(gold)),
            'primary_right_when_shown': ratio(primary, gold_shown),
            'no_skill_fire_rate': ratio(sum(bool(picks[row['id']]) for row in quiet), len(quiet)),
            'top1': ratio(primary, len(gold))}


def policy_splits(rows: list[dict], picks: dict, policies: list[str]) -> dict:
    """split -> subset -> policy -> hint_metrics. Subsets: all, multi_concern (2+ concerns), and each `kind` the rows carry."""
    out = {}
    for split in ('dev', 'test', 'fresh', 'all'):
        part = [row for row in rows if split == 'all' or row['split'] == split]
        if not part:
            continue
        groups = {'all': part, 'multi_concern': [row for row in part if len(row['concerns']) >= 2]}
        for kind in sorted({row['kind'] for row in part if 'kind' in row}):
            groups[kind] = [row for row in part if row.get('kind') == kind]
        out[split] = {name: {policy: hint_metrics(group, {row['id']: picks[row['id']][policy] for row in group})
                             for policy in policies}
                      for name, group in groups.items() if group}
    return out


def run_policies(root: Path, prompts_file: Path, policies: list[str]) -> dict:
    out = subprocess.run([sys.executable, '-c', POLICY_SELECTOR, str(root), str(prompts_file), ','.join(policies)],
                         capture_output=True, text=True, encoding='utf-8', timeout=900)
    if out.returncode:
        raise SystemExit(f'policy run failed for {root}: {out.stderr[-800:]}')
    return json.loads(out.stdout)


def load_rows(files: list[Path]) -> list[dict]:
    """Every prompt of the given files. A row with a `kind` belongs to the fresh split; the others split by id hash."""
    rows = [row for file in files for row in json.loads(file.read_text(encoding='utf-8'))]
    if len({row['id'] for row in rows}) != len(rows):
        raise SystemExit('prompt ids are not unique across the --prompts files')
    for row in rows:
        row['split'] = 'fresh' if 'kind' in row else split_of(row['id'])
    return rows


def print_policy(report: dict, split: str) -> None:
    def pct(metric: dict) -> str:
        return f'{100 * metric["rate"]:.0f}%' if metric['rate'] is not None else '-'

    for name, policies in report['splits'][split].items():
        first = next(iter(policies.values()))
        print(f'\n== hint policy, {split}, {name} ({first["prompts"]} prompts, {first["with_skill"]} with a gold concern)')
        print(f'{"policy":<16}{"shown":>7}{"precision":>11}{"recall":>8}{"all concerns":>14}{"primary right":>15}{"no-skill fires":>16}{"top-1":>7}')
        for policy, m in policies.items():
            print(f'{policy:<16}{pct(m["shown_rate"]):>7}{pct(m["precision"]):>11}{pct(m["concern_recall"]):>8}'
                  f'{pct(m["all_concerns"]):>14}{pct(m["primary_right_when_shown"]):>15}{pct(m["no_skill_fire_rate"]):>16}'
                  f'{pct(m["top1"]):>7}')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--arm', action='append', default=[], help='NAME=BOSSKU_ROOT (repeatable)')
    parser.add_argument('--baseline-arm', help='arm whose skill catalog the keyword baseline reads (default: the first --arm)')
    parser.add_argument('--prompts', type=Path, action='append', help='prompt file, repeatable (default: prompts.json)')
    parser.add_argument('--out', type=Path)
    parser.add_argument('--split', choices=['dev', 'test', 'fresh', 'all'], default='all')
    parser.add_argument('--policy', nargs='+', choices=POLICIES, default=[], help='hint-policy arms to measure')
    parser.add_argument('--policy-root', type=Path, default=REPO, help='checkout whose hint code the policy arms run')
    args = parser.parse_args(argv)
    files = args.prompts or [PROMPTS]
    rows = load_rows(files)
    arms = {}
    for spec in args.arm:
        name, _, root = spec.partition('=')
        arms[name] = Path(root).resolve()
    if not arms and not args.policy:
        parser.error('--arm NAME=ROOT or --policy NAME is required')
    baseline_arm = args.baseline_arm or next(iter(arms), None)
    if arms and baseline_arm not in arms:
        parser.error(f'--baseline-arm {baseline_arm!r} is not one of the --arm names')
    with tempfile.TemporaryDirectory() as tmp:
        prompts_file = files[0]
        if len(files) > 1:   # one file for the selector processes
            prompts_file = Path(tmp) / 'prompts.json'
            prompts_file.write_text(json.dumps(rows), encoding='utf-8')
        answers = {name: run_selector(root, prompts_file) for name, root in arms.items()}
        picks = run_policies(args.policy_root.resolve(), prompts_file, args.policy) if args.policy else {}
    report = {'prompts_file': ', '.join(str(f.relative_to(REPO)) if f.is_relative_to(REPO) else str(f) for f in files),
              # line endings differ between Windows and Linux checkouts; the hash must not
              'prompts_sha256': hashlib.sha256(b''.join(f.read_bytes().replace(b'\r\n', b'\n') for f in files)).hexdigest(),
              # arm labels only, never folder paths: the file is committed
              'arms': {name: arm_provenance(root) for name, root in arms.items()}}
    if arms:
        answers['description-only'], catalog_hash = description_only(rows, arms[baseline_arm])
        print(f'description-only uses the catalog of arm {baseline_arm} (catalog sha256 {catalog_hash[:12]})')
        report['baseline'] = {'arm': baseline_arm, 'catalog_sha256': catalog_hash}
    report['splits'] = {}
    for split in ('dev', 'test', 'fresh', 'all') if arms else ():
        # a prompt with no gold concern (a follow-up, chit-chat) has nothing to score the router on
        subset = [row for row in rows if row['concerns'] and (split == 'all' or row['split'] == split)]
        if not subset:
            continue
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
    if args.policy:
        report['hint_policy'] = {'root': arm_provenance(args.policy_root.resolve()), 'policies': list(args.policy),
                                 'splits': policy_splits(rows, picks, args.policy)}
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2), encoding='utf-8')
    shown = [args.split] if args.split != 'all' else ['dev', 'test', 'fresh', 'all']
    for split in shown:
        if arms and split in report['splits']:
            print(f'\n== {split} ({report["splits"][split][next(iter(answers))]["prompts"]} prompts)')
            print(f'{"method":<18}{"top-1":>8}{"top-3":>8}{"concerns covered":>18}{"all covered":>13}{"precision":>11}{"stack":>7}')
            for name in answers:
                s = report['splits'][split][name]
                cov = f'{100 * s["concern_coverage"]:.0f}%' if 'concern_coverage' in s else '-'
                allc = f'{100 * s["all_concerns_covered"]["rate"]:.0f}%' if 'all_concerns_covered' in s else '-'
                prec = f'{100 * s["stack_precision"]:.0f}%' if 'stack_precision' in s else '-'
                size = f'{s["stack_size"]:.1f}' if 'stack_size' in s else '-'
                print(f'{name:<18}{100 * s["top1"]["rate"]:>7.0f}%{100 * s["top3"]["rate"]:>7.0f}%{cov:>18}{allc:>13}{prec:>11}{size:>7}')
        if args.policy and split in report['hint_policy']['splits']:
            print_policy(report['hint_policy'], split)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
