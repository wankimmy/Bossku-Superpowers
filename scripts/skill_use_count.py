#!/usr/bin/env python3
"""How often did an agent with Bossku Superpower open a skill during the task runs?

    python scripts/skill_use_count.py

Counts the completed task runs of the "after" setup in benchmarks/results/raw/ and the runs in which the agent
opened at least one skill (`skills_loaded` or `skills_invoked`).
"""

from __future__ import annotations

import glob
import json
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / 'benchmarks' / 'results' / 'raw'


def count() -> tuple[int, int, set[str]]:
    runs = used = 0
    skills: set[str] = set()
    for path in sorted(glob.glob(str(RAW / '*.jsonl'))):
        if any(word in Path(path).name for word in ('overhead', 'routing', 'timeouts')):
            continue
        for line in Path(path).read_text(encoding='utf-8').splitlines():
            row = json.loads(line)
            if row.get('kind') != 'task' or not str(row.get('arm', '')).startswith('after') or row.get('infrastructure_failure'):
                continue
            runs += 1
            opened = set(row.get('skills_loaded') or []) | set(row.get('skills_invoked') or [])
            if opened:
                used += 1
                skills |= opened
    return runs, used, skills


if __name__ == '__main__':
    runs, used, skills = count()
    print(f'{used} of {runs} completed task runs with Bossku Superpower opened a skill ({", ".join(sorted(skills)) or "none"})')
