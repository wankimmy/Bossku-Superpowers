#!/usr/bin/env python3
"""Score the stated-rule detector (bossku/rules.py) on messages written and labelled by other agents.

    python scripts/benchmark_rules.py prepare     # shuffle pos-*.json / neg-*.json into key.json (+ unlabeled audit files)
    python scripts/benchmark_rules.py score       # key.json + labels-*.json -> recall, false alarms

Writers saw neither the detector nor its tests. Two labellers then classified the shuffled messages without seeing the
writer's intent; a message counts only where the labeller and the writer agree, so ambiguous ones are dropped. The data
lives in benchmarks/rules-eval/. A set stops being a fair test the moment the detector is tuned on it.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from bossku.rules import states_rule  # noqa: E402

DIR = REPO / 'benchmarks' / 'rules-eval'
SOURCES = (('pos-a', 1), ('pos-b', 1), ('neg-a', 0), ('neg-b', 0))


def wilson(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def prepare(directory: Path, seed: int = 11) -> int:
    rows = []
    for name, label in SOURCES:
        messages = json.loads((directory / f'{name}.json').read_text(encoding='utf-8'))
        rows += [{'src': name, 'i': i, 'label': label, 'text': t} for i, t in enumerate(messages)
                 if isinstance(t, str) and t.strip()]
    random.Random(seed).shuffle(rows)
    (directory / 'key.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
    for k in (0, 1):
        part = [{'id': n, 'text': r['text']} for n, r in enumerate(rows) if n % 2 == k]
        (directory / f'audit-{k}.json').write_text(json.dumps(part, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'{len(rows)} messages; wrote key.json and audit-0.json / audit-1.json (the labellers get only the audit files)')
    return len(rows)


def kept_messages(directory: Path) -> tuple[list[dict], int]:
    key = json.loads((directory / 'key.json').read_text(encoding='utf-8'))
    labels: dict[int, object] = {}
    for k in (0, 1):
        path = directory / f'labels-{k}.json'
        if path.is_file():
            labels.update({int(i): v for i, v in json.loads(path.read_text(encoding='utf-8')).items()})
    agreed = [r for n, r in enumerate(key) if labels.get(n) == r['label']]
    return agreed, len(key)


def score(directory: Path, show: bool = False) -> dict:
    agreed, total = kept_messages(directory)
    pos = [r for r in agreed if r['label'] == 1]
    neg = [r for r in agreed if r['label'] == 0]
    caught = sum(states_rule(r['text']) for r in pos)
    flagged = sum(states_rule(r['text']) for r in neg)
    result = {'messages': total, 'kept': len(agreed), 'rules': len(pos), 'caught': caught,
              'recall_ci': wilson(caught, len(pos)), 'non_rules': len(neg), 'flagged': flagged,
              'false_alarm_ci': wilson(flagged, len(neg))}
    print(f"{total} messages, {len(agreed)} kept after the labellers agreed with the writers")
    for name, _ in SOURCES:
        sub = [r for r in agreed if r['src'] == name]
        print(f"  {name}: flagged {sum(states_rule(r['text']) for r in sub)}/{len(sub)}")
    lo, hi = result['recall_ci']
    print(f"stated rules caught: {caught}/{len(pos)} ({caught / max(1, len(pos)):.0%}, 95% interval {lo:.0%}-{hi:.0%})")
    lo, hi = result['false_alarm_ci']
    print(f"non-rules wrongly flagged: {flagged}/{len(neg)} ({flagged / max(1, len(neg)):.0%}, 95% interval {lo:.0%}-{hi:.0%})")
    if show:
        for r in pos:
            if not states_rule(r['text']):
                print('MISSED:', r['text'][:160].replace('\n', ' '))
        for r in neg:
            if states_rule(r['text']):
                print('FALSE ALARM:', r['text'][:160].replace('\n', ' '))
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('command', choices=('prepare', 'score'))
    parser.add_argument('--dir', type=Path, default=DIR)
    parser.add_argument('--show', action='store_true', help='print the missed rules and the false alarms')
    args = parser.parse_args(argv)
    if args.command == 'prepare':
        prepare(args.dir)
    else:
        score(args.dir, args.show)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
