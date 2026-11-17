#!/usr/bin/env python3
"""Does a skill, or the whole pack, help? Reads committed run rows; makes no model calls.

    python scripts/skill_effectiveness.py activation ROWS...
    python scripts/skill_effectiveness.py compare --baseline baseline --arm bossku ROWS...
    python scripts/skill_effectiveness.py classify --baseline baseline --arm bossku ROWS...
    python scripts/skill_effectiveness.py record --date 2026-11-17 --skill pack:bossku --baseline baseline --arm bossku ROWS...
    python scripts/skill_effectiveness.py record --date 2026-11-17 --skill minimal-fix

Every command prints JSON; add --table for a plain table. A value that was not measured is null.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from scripts.benchmark_agent import bootstrap_ci, excluded, total_input, wilson  # noqa: E402

MIN_PAIRED_TASKS = 10   # fewer paired tasks than this can never earn a "demonstrated" label
LABELS = ('demonstrated_improvement', 'demonstrated_regression', 'promising_insufficient_evidence',
          'neutral_or_inconclusive', 'not_tested')
STATUSES = LABELS + ('required_safety_control',)
RECORD_FIELDS = ('skill_id', 'skill_version', 'model', 'host', 'task_category', 'suite', 'baseline_arm', 'arm',
                 'sample_size', 'baseline_pass_rate', 'skill_pass_rate', 'paired_difference', 'confidence_interval',
                 'token_overhead', 'cost_per_success', 'evaluation_status', 'last_evaluated', 'source_rows')
SKILL_ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]*$')


def load_rows(paths, kinds=('task', 'routing')) -> list[dict]:
    """Rows that count (not a harness or infrastructure failure), tagged with their file and suite."""
    rows = []
    for path in map(Path, paths):
        for line in path.read_text(encoding='utf-8').splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get('kind') in kinds and not excluded(row):
                row['_file'] = _rel(path)
                row['_suite'] = suite_name(path, row)
                rows.append(row)
    return rows


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO).as_posix()
    except ValueError:
        return path.as_posix()


def suite_name(path: Path, row: dict) -> str:
    """`coding` from `coding-<model>.jsonl`; a set folder (not `raw`) is kept in front: `2026-10-29-packs/coding`."""
    stem = path.stem
    slug = str(row.get('model', '')).replace(':', '-')
    if slug and stem.endswith('-' + slug):
        stem = stem[:-len(slug) - 1]
    return stem if path.parent.name == 'raw' else f'{path.parent.name}/{stem}'


def opened(row: dict) -> set[str]:
    return set(row.get('skills_loaded') or []) | set(row.get('skills_invoked') or [])


def acceptable(row: dict) -> set[str] | None:
    concerns = row.get('concerns')
    return set().union(*map(set, concerns)) if concerns else None


def activation(rows: list[dict]) -> list[dict]:
    """Per model, arm and kind: how many runs showed a hint, opened a skill, opened an acceptable one."""
    out = []
    for key in sorted({(r['model'], r['arm'], r['kind']) for r in rows}):
        group = [r for r in rows if (r['model'], r['arm'], r['kind']) == key]
        graded = [r for r in group if acceptable(r) is not None]
        hinted = [r for r in group if r.get('hint_shown') is not None]
        out.append({
            'model': key[0], 'arm': key[1], 'kind': key[2], 'runs': len(group),
            'hint_shown': sum(bool(r['hint_shown']) for r in hinted) if hinted else None,
            'opened_any': sum(bool(opened(r)) for r in group),
            'acceptable_opened': sum(bool(opened(r) & acceptable(r)) for r in graded) if graded else None,
            'only_outside_acceptable': (sum(bool(opened(r)) and not opened(r) & acceptable(r) for r in graded)
                                        if graded else None),
            'passed': sum(bool(r.get('passed')) for r in group) if any('passed' in r for r in group) else None,
        })
    return out


def sign_test_p(better: int, worse: int) -> float | None:
    """Exact two-sided sign test over the tasks that differ."""
    n = better + worse
    if n == 0:
        return None
    tail = sum(math.comb(n, k) for k in range(min(better, worse) + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def arm_summary(rows: list[dict]) -> dict:
    passed = sum(bool(r.get('passed')) for r in rows)
    lo, hi = wilson(passed, len(rows))
    costs = [r['cost_usd'] for r in rows]
    known = all(c is not None for c in costs)
    return {
        'runs': len(rows), 'days': sorted({str(r.get('timestamp'))[:10] for r in rows if r.get('timestamp')}),
        'passed': passed, 'pass_rate': passed / len(rows), 'pass_ci': [lo, hi],
        'tokens_mean': statistics.mean(total_input(r['tokens']) + r['tokens']['output'] for r in rows),
        'cost_mean': statistics.mean(costs) if known else None,
        'cost_per_passed': sum(costs) / passed if known and passed else None,
    }


def per_task(rows: list[dict]) -> dict[str, float]:
    by: dict[str, list[float]] = {}
    for r in rows:
        by.setdefault(r['task'], []).append(1.0 if r.get('passed') else 0.0)
    return {t: statistics.mean(v) for t, v in by.items()}


def compare(rows: list[dict], baseline: str, arm: str, allow_unpaired: bool = False) -> list[dict]:
    """One cell per model and suite that has rows for both arms, paired by task."""
    cells = []
    for model, suite in sorted({(r['model'], r.get('_suite', 'all')) for r in rows}):
        group = [r for r in rows if r['model'] == model and r.get('_suite', 'all') == suite]
        base = [r for r in group if r['arm'] == baseline]
        test = [r for r in group if r['arm'] == arm]
        if not base or not test:
            continue
        b, a = per_task(base), per_task(test)
        only_b, only_a = sorted(set(b) - set(a)), sorted(set(a) - set(b))
        if (only_b or only_a) and not allow_unpaired:
            raise ValueError(f'{model} {suite}: the arms ran different tasks (only in {baseline}: {only_b}; '
                             f'only in {arm}: {only_a}); pass --allow-unpaired to compare the shared tasks')
        shared = sorted(set(b) & set(a))
        diffs = [a[t] - b[t] for t in shared]
        lo, hi = bootstrap_ci(diffs) if diffs else (float('nan'), float('nan'))
        interval = None if math.isnan(lo) else [lo, hi]
        bs, as_ = arm_summary(base), arm_summary(test)
        cells.append({
            'model': model, 'suite': suite, 'baseline_arm': baseline, 'arm_name': arm,
            'host': 'claude-code' if any(r.get('claude_code_version') for r in group) else None,
            'categories': sorted({r['category'] for r in group if r.get('category')}),
            'unpaired': bool(only_b or only_a), 'tasks_only_in_baseline': only_b, 'tasks_only_in_arm': only_a,
            'paired_tasks': len(shared),
            'baseline': bs, 'arm': as_,
            'paired_difference': statistics.mean(diffs) if diffs else None,
            'confidence_interval': interval,
            'sign_test_p': sign_test_p(sum(d > 0 for d in diffs), sum(d < 0 for d in diffs)),
            'token_overhead': as_['tokens_mean'] / bs['tokens_mean'] - 1 if bs['tokens_mean'] else None,
            'source_rows': sorted({r['_file'] for r in group if '_file' in r}),
        })
    return cells


def classify(cell: dict | None) -> str:
    """The interval, not the point estimate, decides. An interval across zero is never "no difference"."""
    if not cell or not cell.get('paired_tasks') or cell.get('confidence_interval') is None:
        return 'not_tested'
    lo, hi = cell['confidence_interval']
    p = cell.get('sign_test_p')   # a few tasks that differ can clear the interval by luck: the exact test must agree
    enough = cell['paired_tasks'] >= MIN_PAIRED_TASKS and p is not None and p <= 0.05
    if lo > 0:
        return 'demonstrated_improvement' if enough else 'promising_insufficient_evidence'
    if hi < 0 and enough:
        return 'demonstrated_regression'
    return 'promising_insufficient_evidence' if cell['paired_difference'] > 0 else 'neutral_or_inconclusive'


def skill_blob_hash(skill_id: str) -> str:
    """Version of a skill: the git blob hash of its SKILL.md."""
    path = REPO / 'skills' / skill_id / 'SKILL.md'
    if not SKILL_ID.match(skill_id) or not path.is_file():
        raise ValueError(f'no skill {skill_id!r}')
    done = subprocess.run(['git', 'hash-object', str(path)], capture_output=True, text=True, cwd=REPO, check=True)
    return done.stdout.strip()


def make_record(cell: dict, *, skill_id: str, skill_version: str | None, baseline_arm: str, arm: str, date: str,
                source_rows: list[str], required: bool) -> dict:
    categories = cell.get('categories') or []
    return {
        'skill_id': skill_id, 'skill_version': skill_version, 'model': cell['model'], 'host': cell.get('host'),
        'task_category': categories[0] if len(categories) == 1 else None, 'suite': cell['suite'],
        'baseline_arm': baseline_arm, 'arm': arm, 'sample_size': cell['paired_tasks'],
        'baseline_pass_rate': cell['baseline']['pass_rate'], 'skill_pass_rate': cell['arm']['pass_rate'],
        'paired_difference': cell['paired_difference'], 'confidence_interval': cell['confidence_interval'],
        'token_overhead': cell['token_overhead'], 'cost_per_success': cell['arm']['cost_per_passed'],
        'evaluation_status': 'required_safety_control' if required else classify(cell),
        'last_evaluated': date, 'source_rows': list(source_rows),
    }


def not_tested_record(skill_id: str, skill_version: str | None, date: str) -> dict:
    rec = dict.fromkeys(RECORD_FIELDS)
    rec.update(skill_id=skill_id, skill_version=skill_version, evaluation_status='not_tested', last_evaluated=date,
               source_rows=[])
    return rec


def validate_record(rec: dict) -> None:
    missing = [k for k in RECORD_FIELDS if k not in rec]
    extra = sorted(set(rec) - set(RECORD_FIELDS))
    if missing or extra:
        raise ValueError(f'record fields differ from the schema: missing {missing}, extra {extra}')
    if rec['evaluation_status'] not in STATUSES:
        raise ValueError(f'bad evaluation_status {rec["evaluation_status"]!r}')
    if not isinstance(rec['skill_id'], str) or not rec['skill_id']:
        raise ValueError('skill_id must be a string')
    if not isinstance(rec['last_evaluated'], str) or not rec['last_evaluated']:
        raise ValueError('last_evaluated must be a date string')
    if not isinstance(rec['source_rows'], list):
        raise ValueError('source_rows must be a list')
    if rec['skill_id'].startswith('pack:') and rec['skill_version'] is not None:
        raise ValueError('a pack has no skill_version')
    if rec['evaluation_status'] == 'not_tested' and any(rec[k] is not None for k in RECORD_FIELDS[2:15]):
        raise ValueError('a not_tested record carries no measurement')
    ci = rec['confidence_interval']
    if ci is not None and not (isinstance(ci, list) and len(ci) == 2):
        raise ValueError('confidence_interval must be [low, high] or null')


# --------------------------------------------------------------------------- command line

def fmt(value, pct=False) -> str:
    if value is None:
        return '-'
    return f'{round(100 * value)}%' if pct else f'{value:.3g}'


def table(headers: list[str], body: list[list]) -> str:
    cells = [headers] + [[str(c) for c in r] for r in body]
    widths = [max(len(r[i]) for r in cells) for i in range(len(headers))]
    return '\n'.join('  '.join(c.ljust(w) for c, w in zip(r, widths)).rstrip() for r in cells)


def activation_table(items: list[dict]) -> str:
    keys = ('runs', 'hint_shown', 'opened_any', 'acceptable_opened', 'only_outside_acceptable', 'passed')
    return table(['model', 'arm', 'kind', *keys],
                 [[i['model'], i['arm'], i['kind'], *('-' if i[k] is None else i[k] for k in keys)] for i in items])


def interval_text(c: dict) -> str:
    ci = c['confidence_interval']
    return '-' if ci is None else f'{ci[0]:+.2f}..{ci[1]:+.2f}'


def compare_table(cells: list[dict]) -> str:
    body = []
    for c in cells:
        diff = '-' if c['paired_difference'] is None else f'{c["paired_difference"]:+.2f}'
        body.append([c['model'], c['suite'], c['arm_name'], c['paired_tasks'],
                     f'{fmt(c["baseline"]["pass_rate"], True)} ({c["baseline"]["runs"]})',
                     f'{fmt(c["arm"]["pass_rate"], True)} ({c["arm"]["runs"]})', diff, interval_text(c),
                     fmt(c['sign_test_p']), fmt(c['token_overhead'], True), fmt(c['arm']['cost_per_passed']),
                     classify(c) + (' (unpaired)' if c['unpaired'] else '')])
    return table(['model', 'suite', 'arm', 'tasks', 'base pass (runs)', 'arm pass (runs)', 'diff', '95% interval',
                  'sign p', 'token overhead', '$/passed', 'label'], body)


def record_path(rec: dict, out: Path) -> Path:
    parts = [rec['skill_id']]
    if rec['model']:
        parts += [rec['model'], rec['suite'], rec['arm']]
    parts = [re.sub(r'[^A-Za-z0-9._-]', '-', part) for part in parts]
    return out / ('--'.join(parts) + '.json')


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('activation', 'compare', 'classify', 'record'):
        p = sub.add_parser(name)
        p.add_argument('rows', nargs='*')
        p.add_argument('--table', action='store_true', help='print a plain table instead of JSON')
        if name != 'activation':
            p.add_argument('--baseline')
            p.add_argument('--arm', action='append', default=[], help='an arm to compare (repeat for several)')
            if name != 'record':
                p.add_argument('--allow-unpaired', action='store_true')
        if name == 'record':
            p.add_argument('--skill', required=True, help='skill id, or pack:bossku')
            p.add_argument('--date', required=True, help='last_evaluated, YYYY-MM-DD')
            p.add_argument('--required', action='store_true')
            p.add_argument('--out', default=str(REPO / 'benchmarks' / 'skill-effectiveness' / 'records'))
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == 'activation':
            items = activation(load_rows(args.rows))
            print(activation_table(items) if args.table else json.dumps(items, indent=2))
            return 0
        pack = getattr(args, 'skill', '').startswith('pack:')
        if args.command == 'record' and not args.rows:
            version = None if pack else skill_blob_hash(args.skill)
            records = [not_tested_record(args.skill, version, args.date)]
            if args.required:
                records[0]['evaluation_status'] = 'required_safety_control'
        else:
            if not args.baseline or not args.arm:
                parser.error('--baseline and at least one --arm are required')
            rows = load_rows(args.rows, kinds=('task',))
            # a record has no field to say "unpaired": record skips those cells and says so
            allow = args.command == 'record' or getattr(args, 'allow_unpaired', False)
            cells = [c for arm in args.arm for c in compare(rows, args.baseline, arm, allow)]
            if args.command == 'record':
                for c in cells:
                    if c['unpaired']:
                        print(f'skill_effectiveness: skipped {c["model"]} {c["suite"]} {c["arm_name"]}: '
                              'the arms ran different tasks', file=sys.stderr)
                cells = [c for c in cells if not c['unpaired']]
            if args.command == 'compare':
                print(compare_table(cells) if args.table else json.dumps(cells, indent=2))
                return 0
            if args.command == 'classify':
                result = [{'model': c['model'], 'suite': c['suite'], 'arm': c['arm_name'], 'label': classify(c)}
                          for c in cells] or [{'label': 'not_tested'}]
                print(table(list(result[0]), [list(r.values()) for r in result]) if args.table
                      else json.dumps(result, indent=2))
                return 0
            version = None if pack else skill_blob_hash(args.skill)
            records = [make_record(c, skill_id=args.skill, skill_version=version, baseline_arm=c['baseline_arm'],
                                   arm=c['arm_name'], date=args.date, source_rows=c['source_rows'],
                                   required=args.required) for c in cells]
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        for rec in records:
            validate_record(rec)
            path = record_path(rec, out)
            path.write_text(json.dumps(rec, indent=2) + '\n', encoding='utf-8')
            print(_rel(path))
        return 0
    except (ValueError, OSError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print(f'skill_effectiveness: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
