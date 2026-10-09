#!/usr/bin/env python3
"""Check narrow literal invariants, not language authenticity. Python stdlib only."""
import argparse
import json
from pathlib import Path
import re

SKILL = Path(__file__).resolve().parents[1] / 'skills/malaysia-localisation'


def read_jsonl(path):
    rows = []
    for number, line in enumerate(Path(path).read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f'{path}:{number}: {exc}') from exc
        if not isinstance(row, dict):
            raise ValueError(f'{path}:{number}: expected an object')
        rows.append(row)
    return rows


def load_cases(skill=SKILL):
    cases = {}
    for path in sorted((Path(skill) / 'evals').glob('*.jsonl')):
        for row in read_jsonl(path):
            if row['id'] in cases:
                raise ValueError(f'Duplicate case ID: {row["id"]}')
            cases[row['id']] = row
    if not cases:
        raise ValueError('No evaluation cases found')
    return cases


def check(cases, responses):
    seen = set()
    failures = []
    checked = 0
    for row in responses:
        id_ = row.get('id')
        if not isinstance(id_, str) or id_ not in cases:
            raise ValueError(f'Unknown/missing case ID: {id_!r}')
        if id_ in seen:
            raise ValueError(f'Duplicate response ID: {id_}')
        seen.add(id_)
        output = row.get('output')
        if not isinstance(output, str) or not output.strip():
            raise ValueError(f'{id_}: output must be a non-empty string')
        checks = cases[id_]['checks']
        checked += bool(checks['contains'] or checks['forbidden_regex'])
        for literal in checks['contains']:
            if literal not in output:
                failures.append({'id': id_, 'failure': f'Missing exact literal: {literal}'})
        for pattern in checks['forbidden_regex']:
            if re.search(pattern, output, flags=re.IGNORECASE):
                failures.append({'id': id_, 'failure': f'Prohibited expression for this case: {pattern}'})
    missing = sorted(set(cases) - seen)
    return {
        'submitted': len(seen), 'total_cases': len(cases),
        'cases_with_automated_checks': checked,
        'missing': missing, 'failures': failures,
        'literal_checks_complete_and_clean': not failures and not missing,
        'language_quality_status': 'HUMAN REVIEW REQUIRED',
        'note': 'Passing these checks does not establish register fit, meaning fidelity or authenticity.'
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('responses', type=Path, help='JSONL with id and output')
    args = parser.parse_args()
    try:
        report = check(load_cases(), read_jsonl(args.responses))
    except (ValueError, KeyError, OSError) as exc:
        parser.exit(2, f'Invalid evaluation input: {exc}\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['literal_checks_complete_and_clean'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
