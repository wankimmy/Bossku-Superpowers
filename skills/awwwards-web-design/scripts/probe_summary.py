#!/usr/bin/env python3
"""Aggregate site_probe.py outputs across many sites into one measured portrait.

  python3 probe_summary.py --probes evidence/probes --out data/probe_summary.json

Counts are per SITE (a site using an easing 40 times counts once) unless noted.
"""
import argparse
import json
import re
import statistics
from collections import Counter
from pathlib import Path


def px(v):
    try:
        return float(str(v).replace("px", ""))
    except ValueError:
        return None


def norm_ease(e: str) -> str:
    nums = re.findall(r"-?\d*\.?\d+", e)
    return "cubic-bezier(" + ",".join(f"{float(x):g}" for x in nums) + ")"


def norm_dur(x: str) -> str:
    ms = float(x[:-2]) if x.endswith("ms") else float(x[:-1]) * 1000
    return f"{ms:g}ms"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probes", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--sample", type=Path, default=None, help="only include slugs listed in this sample.json")
    a = ap.parse_args()
    keep = {s["slug"] for s in json.loads(a.sample.read_text())} if a.sample else None
    sites = []
    for f in sorted(a.probes.glob("*/probe.json")):
        if keep is not None and f.parent.name not in keep:
            continue
        d = json.loads(f.read_text())
        if re.search(r"not supported|error|just a moment", d.get("title") or "", re.I):
            continue
        sites.append(d)
    n = len(sites)
    libs, ctx, feats, eases, durs, fams, ext, blend = Counter(), Counter(), Counter(), Counter(), Counter(), Counter(), Counter(), Counter()
    display_px, body_px, display_ls, display_lh, mobile_display = [], [], [], [], []
    usage = Counter()
    reduced = 0
    three_d_sites, asset_kinds = 0, Counter()
    for d in sites:
        m = d.get("measure") or {}
        libs.update(set(d.get("libs_from_requests") or []))
        g = d.get("globals") or {}
        libs.update({f"global:{k}" for k in g if not k.endswith(("_version", "_revision"))})
        ctx.update({k for k, v in (d.get("contexts") or {}).items() if v})
        feats.update({k for k, _ in m.get("css_features") or []})
        eases.update({norm_ease(e) for e, _ in m.get("easings") or []})
        durs.update({norm_dur(x) for x, _ in m.get("durations") or []})
        loaded = {re.sub(r"\s+\d{3}.*$", "", f).strip() for f in m.get("fonts_loaded") or []}
        fams.update(loaded)
        ext.update(set((d.get("asset_extensions") or {}).keys()))
        if d.get("assets_3d"):
            three_d_sites += 1
            asset_kinds.update({re.search(r"\.([a-z0-9]+)$", u.lower()).group(1) for u in d["assets_3d"] if re.search(r"\.([a-z0-9]+)$", u.lower())})
        if (m.get("reduced_motion_rules") or 0) > 0:
            reduced += 1
        cu = m.get("css_usage") or {}
        for k in ["clip_path", "mix_blend_mode", "backdrop_filter", "sticky", "transform3d", "cursor_none", "box_shadows", "filters"]:
            if (cu.get(k) or 0) > 0:
                usage[k] += 1
        lt = m.get("largest_text") or []
        if lt:
            size = px(lt[0].get("size"))
            if size:
                display_px.append(size)
                ls = lt[0].get("ls")
                if ls and ls != "normal" and px(ls) is not None:
                    display_ls.append(round(px(ls) / size, 3))
                lh = lt[0].get("lh")
                if lh and lh != "normal" and px(lh) is not None:
                    display_lh.append(round(px(lh) / size, 2))
        b = px((m.get("body") or {}).get("size"))
        ps = [px(p.get("size")) for p in (m.get("type") or {}).get("p", []) if px(p.get("size"))]
        if ps:
            body_px.append(statistics.median(ps))
        elif b:
            body_px.append(b)
        mm = d.get("mobile_measure") or {}
        if mm.get("largest"):
            mobile_display.append(mm["largest"][0])

    def dist(xs):
        if not xs:
            return None
        xs = sorted(xs)
        q = lambda p: xs[min(len(xs) - 1, int(p * (len(xs) - 1)))]
        return {"n": len(xs), "min": xs[0], "p25": q(0.25), "median": q(0.5), "p75": q(0.75), "max": xs[-1]}

    out = {
        "sites": n,
        "libraries_by_sites": libs.most_common(),
        "canvas_contexts_by_sites": ctx.most_common(),
        "sites_loading_3d_assets": three_d_sites,
        "3d_asset_types_by_sites": asset_kinds.most_common(),
        "asset_extensions_by_sites": ext.most_common(),
        "css_features_by_sites": feats.most_common(),
        "css_usage_by_sites": usage.most_common(),
        "sites_with_reduced_motion_rules": reduced,
        "easings_by_sites": eases.most_common(40),
        "durations_by_sites": durs.most_common(30),
        "fonts_loaded_by_sites": fams.most_common(80),
        "display_type_px_desktop_1440": dist(display_px),
        "display_letter_spacing_em": dist(display_ls),
        "display_line_height_ratio": dist(display_lh),
        "body_type_px_desktop": dist(body_px),
        "display_type_px_mobile_390": dist(mobile_display),
        "note": "css easings/durations only cover same-origin stylesheets; JS-driven (GSAP) timing lives in bundles and teardowns.",
    }
    a.out.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(json.dumps({k: (v[:25] if isinstance(v, list) else v) for k, v in out.items()}, indent=1, ensure_ascii=False)[:9000])


if __name__ == "__main__":
    main()
