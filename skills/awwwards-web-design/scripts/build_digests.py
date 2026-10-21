#!/usr/bin/env python3
"""Validate teardown JSONs and build one digest per design dimension.

  python3 build_digests.py --teardowns data/teardowns --out evidence/digests

Each digest concatenates that dimension's section from every teardown (plus the
site signature, award and score) so a synthesis agent can read one dimension
across all sites without loading every full teardown.
"""
import argparse
import json
from pathlib import Path

DIMENSIONS = {
    "typography": ["typography", "first_screen", "content_voice"],
    "color": ["color"],
    "layout": ["layout", "first_screen"],
    "motion": ["motion", "navigation_interaction"],
    "imagery": ["imagery", "first_screen"],
    "three_d": ["three_d", "imagery"],
    "interaction": ["navigation_interaction", "motion"],
    "tech_perf_a11y": ["tech_stack", "performance_accessibility", "three_d"],
    "signatures": ["steal_this", "slop_risks", "first_screen"],
    "content": ["content_voice", "first_screen", "navigation_interaction"],
}
REQUIRED = ["slug", "signature", "typography", "color", "layout", "motion", "imagery", "three_d",
            "navigation_interaction", "tech_stack", "performance_accessibility", "steal_this", "slop_risks"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--teardowns", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    sites, problems = [], []
    for f in sorted(a.teardowns.glob("*.json")):
        if f.name.startswith("_"):
            continue
        try:
            d = json.loads(f.read_text())
        except json.JSONDecodeError as exc:
            problems.append(f"{f.name}: invalid JSON ({exc})")
            continue
        missing = [k for k in REQUIRED if k not in d]
        if missing:
            problems.append(f"{f.name}: missing {missing}")
        sites.append(d)
    for dim, keys in DIMENSIONS.items():
        lines = [f"# Digest: {dim} across {len(sites)} Awwwards winners", ""]
        for d in sites:
            head = f"## {d.get('title') or d.get('slug')} ({d.get('slug')}) | {d.get('award','')} | score {((d.get('scores') or {}).get('overall'))}"
            lines += [head, f"signature: {d.get('signature','')}", f"industry: {d.get('industry','')}"]
            for k in keys:
                lines.append(f"{k}: {json.dumps(d.get(k), ensure_ascii=False)}")
            lines.append("")
        (a.out / f"{dim}.md").write_text("\n".join(lines))
    (a.out / "_validation.txt").write_text("\n".join(problems) or "all teardowns valid")
    print(f"{len(sites)} teardowns, {len(problems)} problems -> {a.out}")
    for p in problems:
        print("  ", p)


if __name__ == "__main__":
    main()
