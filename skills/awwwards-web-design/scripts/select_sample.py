#!/usr/bin/env python3
"""Pick a diverse, high-signal teardown sample from corpus.jsonl.

Buckets (award tier, technique, category) each take their best recent sites by
jury score; a site counts once. Prints the sample and writes sample.json.

  python3 select_sample.py --corpus data/corpus.jsonl --out data/sample.json --since 2024
"""
import argparse
import json
import re
from pathlib import Path

BUCKETS = [  # (label, quota, predicate on record)
    ("site-of-the-year", 8, lambda r: "Site of the Year" in (r.get("award_heading") or "") or "sites_of_the_year" in r["sources"]),
    ("site-of-the-month", 10, lambda r: "Site of the Month" in (r.get("award_heading") or "") or "sites_of_the_month" in r["sources"]),
    ("3d-webgl", 9, lambda r: bool({"3d", "webgl", "three-js", "react-three-fiber", "blender", "spline"} & set(r["sources"] + r.get("tag_slugs", [])))),
    ("typography", 4, lambda r: bool({"typography", "big-typography"} & set(r["sources"] + r.get("tag_slugs", [])))),
    ("e-commerce", 5, lambda r: bool({"e-commerce", "shopify", "fashion"} & set(r["sources"] + r.get("tag_slugs", [])))),
    ("portfolio-agency", 5, lambda r: bool({"portfolio", "design-agencies"} & set(r["sources"] + r.get("tag_slugs", [])))),
    ("motion-transitions", 4, lambda r: bool({"transitions", "page-transition", "animation", "gsap", "scrolling", "parallax", "microinteractions"} & set(r["sources"] + r.get("tag_slugs", [])))),
    ("category-mix", 5, lambda r: bool({"architecture", "minimal", "black", "colorful", "storytelling"} & set(r["sources"] + r.get("tag_slugs", [])))),
    ("recent-sotd", 4, lambda r: "sites_of_the_day" in r["sources"]),
]

MOTION_TAGS = {"animation", "scroll", "transition", "transitions", "3d", "webgl", "hover", "menu", "intro",
               "loader", "preloader", "loading", "gallery", "slider", "cursor", "navigation", "typography", "text"}


def year_of(rec):
    m = re.search(r"(20\d\d)", rec.get("award_heading") or "")
    if m:
        return int(m.group(1))
    for el in rec.get("elements", []):
        m = re.search(r"/(20\d\d)/", el.get("media") or "")
        if m:
            return int(m.group(1))
    m = re.search(r"/(20\d\d)/", rec.get("thumbnail") or "")
    return int(m.group(1)) if m else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--since", type=int, default=2024)
    a = ap.parse_args()
    recs = [json.loads(l) for l in a.corpus.read_text().splitlines() if l.strip()]
    recs = [r for r in recs if not r.get("error") and r.get("live_url")]
    for r in recs:
        r["year"] = year_of(r)
        r["_score"] = (r.get("scores") or {}).get("overall") or 0
    pool = [r for r in recs if r["year"] >= a.since]
    chosen, seen = [], set()
    for label, quota, pred in BUCKETS:
        cands = sorted((r for r in pool if pred(r) and r["slug"] not in seen),
                       key=lambda r: (r["_score"], r["year"]), reverse=True)
        for r in cands[:quota]:
            seen.add(r["slug"])
            els = sorted(r.get("elements", []), key=lambda e: -len(MOTION_TAGS & set(e.get("tags", []))))
            chosen.append({
                "slug": r["slug"], "title": r["title"], "bucket": label, "year": r["year"],
                "award": r.get("award_heading"), "score": r["_score"], "live_url": r["live_url"],
                "tags": r.get("tags", []), "palette": r.get("palette", []),
                "elements": [e for e in els if (e.get("media") or "").endswith((".mp4", ".webm"))][:4],
                "dev": (r.get("scores") or {}).get("dev"), "description": r.get("description"),
            })
    a.out.write_text(json.dumps(chosen, indent=1, ensure_ascii=False))
    for c in chosen:
        print(f"{c['bucket']:<20} {c['score']:<5} {c['year']} {c['slug']:<40} {c['live_url']}")
    print(f"{len(chosen)} sites -> {a.out}")


if __name__ == "__main__":
    main()
