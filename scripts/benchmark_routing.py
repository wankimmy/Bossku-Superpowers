"""Offline routing regression benchmark; no model calls or installed-index writes."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import platform
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
if __package__ in {None, ''}:
    sys.path.insert(0, str(ROOT))

from bossku.index import build_index, tokenize
from bossku.skills import NOT_INSTALLED, find_skill, rank_skills, select_skill_stack


CORPUS_NAMES = ('ROUTING_CASES', 'REVIEW_ROUTING_CASES')
INPUT_FILES = (
    'scripts/benchmark_routing.py',
    'bossku/index.py',
    'bossku/skills.py',
    'bossku/paths.py',
    'tests/test_routing.py',
    'skills/aliases.json',
    'skills/vendored.json',
)


def digest(value: object) -> str:
    data = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def load_corpus(path: Path) -> list[dict]:
    """Read static test cases with AST literal evaluation, without running tests."""
    groups = {}
    for node in ast.parse(path.read_text(encoding='utf-8')).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in CORPUS_NAMES:
                    groups[target.id] = ast.literal_eval(node.value)
    if set(groups) != set(CORPUS_NAMES):
        raise ValueError(f'Corpus must define {CORPUS_NAMES}')
    merged = {}
    for name in CORPUS_NAMES:
        for prompt, expected in groups[name]:
            row = merged.setdefault(prompt, {'prompt': prompt, 'expected': set(), 'sources': []})
            row['expected'].update(expected)
            if name not in row['sources']:
                row['sources'].append(name)
    return [
        {'case_id': f'routing-{i:03d}', **row, 'expected': sorted(row['expected'])}
        for i, row in enumerate(merged.values(), start=1)
    ]


def baseline_documents(entries: dict[str, dict]) -> tuple[dict[str, set[str]], dict[str, float]]:
    """ID/description token sets and their document-frequency weights only."""
    documents = {
        sid: set(tokenize(sid.removeprefix('bosskuai-').replace('-', ' ') + ' ' + entry['description']))
        for sid, entry in sorted(entries.items()) if sid not in NOT_INSTALLED
    }
    frequencies = {}
    for terms in documents.values():
        for term in terms:
            frequencies[term] = frequencies.get(term, 0) + 1
    count = len(documents)
    weights = {term: math.log(1 + count / (1 + frequency)) for term, frequency in frequencies.items()}
    return documents, weights


def baseline_rank(
    prompt: str, documents: dict[str, set[str]], weights: dict[str, float], limit: int = 3
) -> list[tuple[str, float]]:
    query = set(tokenize(prompt))
    default = max(weights.values(), default=1.0)
    mass = sum(weights.get(term, default) for term in sorted(query)) or 1.0
    ranked = [
        (sid, sum(weights.get(term, default) for term in sorted(query & terms)) / mass)
        for sid, terms in documents.items()
    ]
    return sorted(ranked, key=lambda row: (-row[1], row[0]))[:limit]


def outcome(top1: tuple[str, float], top3: list[tuple[str, float]], expected: list[str]) -> dict:
    def result(pair):
        return {'skill_id': pair[0], 'score': round(pair[1], 6)}
    return {
        'top1': result(top1),
        'top3': [result(pair) for pair in top3],
        'top1_hit': top1[0] in expected,
        'top3_hit': bool({sid for sid, _ in top3} & set(expected)),
    }


def summarize(rows: list[dict], method: str) -> dict:
    count = len(rows)
    top1 = sum(row[method]['top1_hit'] for row in rows)
    top3 = sum(row[method]['top3_hit'] for row in rows)
    return {
        'cases': count,
        'top1_hits': top1,
        'top3_hits': top3,
        'top1_percent': round(100 * top1 / count, 2) if count else 0.0,
        'top3_percent': round(100 * top3 / count, 2) if count else 0.0,
    }


def selection_outcome(selection: dict, expected: list[str], entries: dict[str, dict]) -> dict:
    model_expected = [sid for sid in expected if not entries[sid].get('user_invoked')]
    user_expected = [sid for sid in expected if entries[sid].get('user_invoked')]
    selected = [row['skill_id'] for row in selection['selected']]
    deferred = [{'skill_id': row['skill_id'], 'reason': row['reason']} for row in selection['deferred']]
    user_loaded = any(entries[sid].get('user_invoked') for sid in selected)
    if model_expected:
        mode = 'model_primary'
        hit = selection['primary'] in model_expected and not user_loaded
    else:
        mode = 'user_invocation_deferral'
        hit = not user_loaded and any(
            row['skill_id'] in user_expected and 'user invocation' in row['reason'] for row in deferred
        )
    return {
        'expected_mode': mode,
        'expected_model_ids': model_expected,
        'expected_user_only_ids': user_expected,
        'primary': selection['primary'],
        'selected': selected,
        'deferred': deferred,
        'hit': hit,
    }


def summarize_selection(rows: list[dict]) -> dict:
    def stats(group):
        hits = sum(row['automatic_selection']['hit'] for row in group)
        return {'cases': len(group), 'hits': hits, 'percent': round(100 * hits / len(group), 2) if group else 0.0}
    model = [row for row in rows if row['automatic_selection']['expected_mode'] == 'model_primary']
    user = [row for row in rows if row['automatic_selection']['expected_mode'] == 'user_invocation_deferral']
    return {
        'actionable_route': stats(rows),
        'model_primary': stats(model),
        'user_invocation_deferral': stats(user),
        'misses': [
            {'case_id': row['case_id'], 'prompt': row['prompt'], 'expected': row['expected'],
             **row['automatic_selection']}
            for row in rows if not row['automatic_selection']['hit']
        ],
    }


def source_snapshot(root: Path, index: dict) -> dict:
    files = {
        name: hashlib.sha256((root / name).read_text(encoding='utf-8').encode('utf-8')).hexdigest()
        for name in INPUT_FILES
    }
    index_hash = digest(index)
    try:
        revision = subprocess.run(
            ['git', '-C', str(root), 'rev-parse', 'HEAD'],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        status = subprocess.run(
            ['git', '-C', str(root), 'status', '--porcelain', '--', *INPUT_FILES, 'skills'],
            capture_output=True, text=True, check=True,
        ).stdout
        modified = bool(status.strip())
    except (OSError, subprocess.CalledProcessError):
        revision, modified = None, None
    return {
        'git_revision': revision,
        'working_tree_modified': modified,
        'routing_inputs_sha256': digest({'files': files, 'index': index_hash}),
        'input_files_sha256': files,
        'fresh_index_sha256': index_hash,
    }


def run_benchmark(root: Path = ROOT) -> dict:
    index = build_index(root)
    entries = index['skills']
    documents, weights = baseline_documents(entries)
    corpus = load_corpus(root / 'tests/test_routing.py')
    unknown = {sid for row in corpus for sid in row['expected']} - set(documents)
    if unknown:
        raise ValueError(f'Expected skills outside eligible inventory: {sorted(unknown)}')
    snapshot = source_snapshot(root, index)
    rows = []
    # Both public APIs read this freshly built index; no cache is written or trusted.
    with patch('bossku.index.load_index', return_value=index):
        for case in corpus:
            prompt, expected = case['prompt'], case['expected']
            baseline = baseline_rank(prompt, documents, weights)
            rows.append({
                **case,
                'bossku': outcome(find_skill(prompt, root), rank_skills(prompt, root, limit=3), expected),
                'description_only': outcome(baseline[0], baseline, expected),
                'automatic_selection': selection_outcome(
                    select_skill_stack(prompt, root, available=set(documents)), expected, entries
                ),
            })
    if source_snapshot(root, build_index(root))['routing_inputs_sha256'] != snapshot['routing_inputs_sha256']:
        raise RuntimeError('Routing inputs changed during the benchmark; rerun after edits finish')
    return {
        'schema_version': 1,
        'source': snapshot,
        'python_version': platform.python_version(),
        'corpus': {
            'kind': 'curated regression corpus, not held-out',
            'source': 'tests/test_routing.py',
            'groups': list(CORPUS_NAMES),
            'cases': len(corpus),
            'sha256': digest(corpus),
            'grading': 'top1 is a defensible ID; top3 contains at least one defensible ID',
            'duplicate_policy': 'one case per identical prompt, union defensible IDs and source groups',
        },
        'inventory': {
            'eligible_count': len(documents),
            'excluded': sorted(NOT_INSTALLED),
            'skill_ids': sorted(documents),
        },
        'methods': {
            'bossku': 'find_skill top1 and rank_skills top3, using a fresh in-memory build_index',
            'description_only': (
                'IDF-weighted query coverage over skill ID and description token sets. '
                'Shared tokenize normalization; ID prefix removed and hyphens spaced. '
                'w(t)=log(1+N/(1+df(t))); score=sum matched query weights/sum query weights. '
                'Unseen query terms use maximum IDF. No curated triggers, exclusions, aliases, '
                'body headings, phrase bonuses or query-side variants. Ties sort by skill ID.'
            ),
            'automatic_selection': (
                'select_skill_stack with the full eligible inventory. A model-invoked expected set '
                'requires an accepted primary ID. A user-only expected set requires an expected ID '
                'deferred for user invocation. Automatically loading any user-only skill fails the outcome.'
            ),
        },
        'results': {
            **{name: summarize(rows, name) for name in ('bossku', 'description_only')},
            'automatic_selection': summarize_selection(rows),
        },
        'cases': rows,
        'limitations': [
            'Routing has been tuned against this curated corpus; this is not generalization evidence.',
            'Measures candidate ranking and primary/defer policy outcomes, not full complement coverage, host loading or task quality.',
            'No model coding runs, token consumption, cost, latency or live optional runtime measurements.',
        ],
    }


def comparable(report: dict) -> dict:
    """Ignore provenance fields that can change on commit or another Python host."""
    return {
        key: value for key, value in report.items() if key not in {'source', 'python_version'}
    } | {'routing_inputs_sha256': report['source']['routing_inputs_sha256']}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'docs/benchmarks/routing.json')
    parser.add_argument('--check', action='store_true', help='Compare current inputs/results with an existing snapshot')
    args = parser.parse_args()
    report = run_benchmark()
    if args.check:
        previous = json.loads(args.output.read_text(encoding='utf-8'))
        matched = comparable(previous) == comparable(report)
        print(json.dumps({'snapshot_matches': matched, 'results': report['results']}, indent=2))
        return 0 if matched else 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps({'results': report['results'], 'corpus_sha256': report['corpus']['sha256']}, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
