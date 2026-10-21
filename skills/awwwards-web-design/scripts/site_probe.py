#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright==1.63.0"]
# ///
"""Probe a live website: screenshots through the scroll + measured design signals.

Needs Python Playwright with Chromium (`pip install playwright && playwright install chromium`).

  python3 site_probe.py https://example.com --out probes/ --name example
  python3 site_probe.py URL --out probes/ --steps 8 --no-mobile

Writes <out>/<name>/:
  desktop_00.jpg ... desktop_NN.jpg   1440x900 viewport, one per wheel-scroll step
  mobile_00.jpg, mobile_01.jpg        390x844 (skipped with --no-mobile)
  probe.json                          libraries, WebGL, 3D assets, fonts, type scale,
                                      colors, easings, durations, CSS features, media mix

It never clicks, accepts banners or submits anything. Wheel events (not scrollTo)
drive the page so smooth-scroll and scroll-triggered timelines actually fire.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

LIB_PATTERNS = {
    "gsap": r"gsap(\.min)?\.js|/gsap@|/gsap/|greensock",
    "scrolltrigger": r"ScrollTrigger",
    "splittext": r"SplitText|split-type|splitting",
    "lenis": r"lenis",
    "locomotive-scroll": r"locomotive",
    "three.js": r"three(\.module)?(\.min)?\.js|/three@|/three/",
    "react-three-fiber": r"@react-three|react-three-fiber",
    "ogl": r"/ogl[@/]|ogl\.js",
    "pixi.js": r"pixi",
    "babylon.js": r"babylon",
    "spline": r"spline(tool)?\.|@splinetool|prod\.spline\.design",
    "unicorn-studio": r"unicorn",
    "rive": r"rive\.app|@rive-app|rive\.wasm",
    "lottie": r"lottie|bodymovin",
    "barba.js": r"barba",
    "swup": r"swup",
    "taxi.js": r"taxi",
    "highway": r"highway",
    "framer-motion": r"framer-motion|motion\.dev|/motion@",
    "theatre.js": r"theatre",
    "matter.js": r"matter(\.min)?\.js",
    "webflow": r"webflow",
    "framer": r"framerusercontent|framer\.com/m/|framerstatic",
    "next.js": r"/_next/",
    "nuxt": r"/_nuxt/",
    "astro": r"/_astro/",
    "sveltekit": r"/_app/immutable",
    "shopify": r"cdn\.shopify|shopify",
    "wordpress": r"wp-content|wp-includes",
    "vite": r"/assets/index-[A-Za-z0-9_-]+\.js",
}

GLOBALS_JS = """() => {
  const g = {};
  const probe = {gsap: 'gsap', ScrollTrigger: 'ScrollTrigger', THREE: 'THREE', Lenis: 'Lenis',
    lenis: 'lenis', PIXI: 'PIXI', barba: 'barba', swup: 'swup', lottie: 'lottie',
    bodymovin: 'bodymovin', Webflow: 'Webflow', __NEXT_DATA__: '__NEXT_DATA__', __NUXT__: '__NUXT__',
    Shopify: 'Shopify', rive: 'rive', LocomotiveScroll: 'LocomotiveScroll', Matter: 'Matter'};
  for (const [k, v] of Object.entries(probe)) { try { if (window[v] !== undefined) g[k] = true } catch (e) {} }
  try { if (window.gsap && window.gsap.version) g.gsap_version = window.gsap.version } catch (e) {}
  try { if (window.THREE && window.THREE.REVISION) g.three_revision = window.THREE.REVISION } catch (e) {}
  try { if (window.__THREE__) g.three_revision = window.__THREE__ } catch (e) {}
  return g;
}"""

MEASURE_JS = r"""() => {
  const out = {};
  const cs = (el) => getComputedStyle(el);
  const pick = (el) => { const s = cs(el); return {
      tag: el.tagName.toLowerCase(), text: (el.innerText || '').trim().slice(0, 90),
      family: s.fontFamily, size: s.fontSize, weight: s.fontWeight, lh: s.lineHeight,
      ls: s.letterSpacing, tt: s.textTransform, color: s.color, style: s.fontStyle }; };
  const vis = (el) => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  out.type = {};
  for (const sel of ['h1','h2','h3','p','a','button','nav a','li','small','figcaption','label']) {
    out.type[sel] = [...document.querySelectorAll(sel)].filter(vis).slice(0, 4).map(pick);
  }
  // Largest rendered text on the page = the real display type.
  const texts = [...document.querySelectorAll('body *')].filter(el => el.childElementCount === 0 && (el.innerText||'').trim().length > 1 && vis(el));
  texts.sort((a, b) => parseFloat(cs(b).fontSize) - parseFloat(cs(a).fontSize));
  out.largest_text = texts.slice(0, 8).map(pick);
  const fam = new Counter(); const sizes = new Counter(); const colors = new Counter(); const bgs = new Counter();
  function Counter() { const m = new Map(); return { add: k => m.set(k, (m.get(k) || 0) + 1), top: n => [...m.entries()].sort((a,b)=>b[1]-a[1]).slice(0, n) }; }
  const all = [...document.querySelectorAll('body *')].slice(0, 6000);
  let clip = 0, blend = 0, backdrop = 0, grid = 0, sticky = 0, fixed = 0, transform3d = 0, filters = 0, cursorNone = 0, radius = new Counter(), shadows = 0;
  for (const el of all) {
    const s = cs(el);
    if (el.childElementCount === 0 && (el.innerText || '').trim()) { fam.add(s.fontFamily.split(',')[0].replace(/["']/g, '').trim()); sizes.add(Math.round(parseFloat(s.fontSize))); colors.add(s.color); }
    if (s.backgroundColor && s.backgroundColor !== 'rgba(0, 0, 0, 0)') bgs.add(s.backgroundColor);
    if (s.clipPath && s.clipPath !== 'none') clip++;
    if (s.mixBlendMode && s.mixBlendMode !== 'normal') blend++;
    if (s.backdropFilter && s.backdropFilter !== 'none') backdrop++;
    if (s.display.includes('grid')) grid++;
    if (s.position === 'sticky') sticky++;
    if (s.position === 'fixed') fixed++;
    if (s.transform && s.transform.startsWith('matrix3d')) transform3d++;
    if (s.filter && s.filter !== 'none') filters++;
    if (s.cursor === 'none') cursorNone++;
    if (s.borderRadius && s.borderRadius !== '0px') radius.add(s.borderRadius);
    if (s.boxShadow && s.boxShadow !== 'none') shadows++;
  }
  out.font_families_rendered = fam.top(8);
  out.font_sizes_px = sizes.top(14);
  out.text_colors = colors.top(8);
  out.bg_colors = bgs.top(10);
  out.css_usage = {clip_path: clip, mix_blend_mode: blend, backdrop_filter: backdrop, grid_containers: grid,
    sticky, fixed, transform3d, filters, cursor_none: cursorNone, box_shadows: shadows, radius_top: radius.top(5)};
  const b = cs(document.body), h = cs(document.documentElement);
  out.body = {bg: b.backgroundColor, html_bg: h.backgroundColor, color: b.color, family: b.fontFamily, size: b.fontSize};
  out.html_classes = document.documentElement.className.toString().slice(0, 200);
  out.body_classes = document.body.className.toString().slice(0, 200);
  // Stylesheet mining (same-origin or CORS-open sheets only).
  const eases = new Counter(), durs = new Counter(), vars = {}, feats = new Counter(); let keyframes = 0, reduced = 0, sheetsRead = 0, sheetsBlocked = 0;
  const walk = (rules) => { for (const r of rules) {
      const t = r.cssText || '';
      if (r.type === 7) keyframes++;
      if (r.media && /prefers-reduced-motion/.test(r.media.mediaText)) reduced++;
      for (const m of t.matchAll(/cubic-bezier\([^)]*\)/g)) eases.add(m[0].replace(/\s+/g, ''));
      for (const m of t.matchAll(/(?:transition|animation)[^;]*?(\d*\.?\d+m?s)/g)) durs.add(m[1]);
      if (/animation-timeline|scroll-timeline|view-timeline/.test(t)) feats.add('scroll-driven-animations');
      if (/view-transition/.test(t)) feats.add('view-transitions');
      if (/@container|container-type/.test(t)) feats.add('container-queries');
      if (/:has\(/.test(t)) feats.add(':has()');
      if (/clamp\(/.test(t)) feats.add('clamp()');
      if (/\bsvh|\bdvh|\blvh/.test(t)) feats.add('dynamic-viewport-units');
      if (/text-wrap:\s*balance|text-wrap:\s*pretty/.test(t)) feats.add('text-wrap balance/pretty');
      if (/font-variation-settings/.test(t)) feats.add('variable-font-axes');
      if (/subgrid/.test(t)) feats.add('subgrid');
      if (/oklch|oklab|color-mix/.test(t)) feats.add('modern-color (oklch/color-mix)');
      if (r.selectorText === ':root' && r.style) { for (const p of r.style) if (p.startsWith('--') && Object.keys(vars).length < 160) vars[p] = r.style.getPropertyValue(p).trim().slice(0, 80); }
      if (r.cssRules) walk(r.cssRules);
  } };
  for (const sh of document.styleSheets) { try { walk(sh.cssRules); sheetsRead++; } catch (e) { sheetsBlocked++; } }
  out.easings = eases.top(12); out.durations = durs.top(12); out.root_vars = vars; out.css_features = feats.top(20);
  out.keyframes = keyframes; out.reduced_motion_rules = reduced; out.sheets = {read: sheetsRead, blocked: sheetsBlocked};
  out.fonts_loaded = [...document.fonts].filter(f => f.status === 'loaded').map(f => `${f.family.replace(/["']/g,'')} ${f.weight} ${f.style}`).filter((v, i, a) => a.indexOf(v) === i).slice(0, 30);
  const canv = [...document.querySelectorAll('canvas')];
  out.canvas = canv.map(c => { const r = c.getBoundingClientRect(); let ctx = 'unknown';
      try { ctx = c.getContext('webgl2') ? 'webgl2?' : 'n/a' } catch (e) { ctx = 'in-use' }
      return {w: Math.round(r.width), h: Math.round(r.height), fixed: cs(c).position, z: cs(c).zIndex}; }).slice(0, 6);
  out.media = {img: document.images.length, video: document.querySelectorAll('video').length, svg: document.querySelectorAll('svg').length,
    iframes: document.querySelectorAll('iframe').length, lottie: document.querySelectorAll('lottie-player,dotlottie-player,[data-animation-path]').length,
    picture: document.querySelectorAll('picture').length};
  out.videos = [...document.querySelectorAll('video')].slice(0, 6).map(v => ({src: (v.currentSrc || v.src || '').slice(0, 160), autoplay: v.autoplay, loop: v.loop, muted: v.muted}));
  out.headings = [...document.querySelectorAll('h1,h2,h3')].filter(vis).slice(0, 24).map(h => `${h.tagName}: ${(h.innerText||'').trim().replace(/\s+/g,' ').slice(0, 100)}`);
  out.nav = [...document.querySelectorAll('nav a, header a')].slice(0, 20).map(a => (a.innerText || a.getAttribute('aria-label') || '').trim().replace(/\s+/g,' ').slice(0, 40));
  out.sections = document.querySelectorAll('section').length;
  out.doc_height = document.documentElement.scrollHeight;
  out.lang = document.documentElement.lang;
  out.meta = {description: (document.querySelector('meta[name=description]')||{}).content || null,
    generator: (document.querySelector('meta[name=generator]')||{}).content || null,
    theme_color: (document.querySelector('meta[name=theme-color]')||{}).content || null};
  return out;
}"""

DESKTOP_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")
MOBILE_UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 "
             "(KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1")
ASSET_3D = re.compile(r"\.(glb|gltf|drc|ktx2|basis|hdr|exr|splat|ply|usdz|fbx|obj)(\?|$)", re.I)
ASSET_SHADER = re.compile(r"\.(glsl|frag|vert|wgsl)(\?|$)", re.I)


GPU_ARGS = {
    # Real GPU through ANGLE/Metal: sites that gate on GPU tier (detect-gpu etc.) reject SwiftShader.
    "metal": ["--use-angle=metal", "--enable-gpu", "--ignore-gpu-blocklist"],
    "swiftshader": ["--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--use-angle=swiftshader"],
}


def probe(url: str, out: Path, name: str, steps: int, mobile: bool, settle: float, gpu: str = "metal") -> dict:
    target = out / name
    target.mkdir(parents=True, exist_ok=True)
    requests, sizes = [], Counter()
    result: dict = {"url": url, "name": name, "gpu": gpu}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel="chromium", args=GPU_ARGS[gpu] + [
            "--autoplay-policy=no-user-gesture-required", "--mute-audio"])
        ctx = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1,
                                  locale="en-US", reduced_motion="no-preference", user_agent=DESKTOP_UA)
        page = ctx.new_page()
        webgl_calls = []
        page.add_init_script("""(() => { const o = HTMLCanvasElement.prototype.getContext;
          HTMLCanvasElement.prototype.getContext = function(t, ...a) { try { window.__ctx = (window.__ctx||[]); window.__ctx.push(t) } catch(e) {}; return o.call(this, t, ...a) } })()""")

        def on_response(resp):
            try:
                u = resp.url
                requests.append(u)
                ct = (resp.headers or {}).get("content-type", "")
                kind = ("3d" if ASSET_3D.search(u) else "shader" if ASSET_SHADER.search(u)
                        else ct.split("/")[-1].split(";")[0] if ct else "other")
                sizes[kind] += int((resp.headers or {}).get("content-length", 0) or 0)
            except Exception:
                pass
        page.on("response", on_response)
        t0 = time.time()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
        except Exception as exc:
            result["nav_error"] = str(exc)[:200]
        time.sleep(settle)  # let preloaders and intro timelines play out
        result["load_seconds_to_settle"] = round(time.time() - t0, 1)
        result["final_url"] = page.url
        try:
            result["title"] = page.title()
        except Exception:
            result["title"] = None
        crashed = {"flag": False}
        page.on("crash", lambda *_: crashed.update(flag=True))

        def measure(tag):
            try:
                result["globals"] = page.evaluate(GLOBALS_JS)
                result["contexts"] = page.evaluate("(() => { const c = {}; (window.__ctx || []).forEach(t => c[t] = (c[t] || 0) + 1); return c })()")
                result["measure"] = page.evaluate(MEASURE_JS)
                result["measured_at"] = tag
            except Exception as exc:
                result.setdefault("measure_errors", []).append(f"{tag}: {str(exc)[:160]}")

        try:
            page.screenshot(path=str(target / "desktop_00.jpg"), type="jpeg", quality=72)
        except Exception as exc:
            result["screenshot_error"] = str(exc)[:200]
        measure("after-load")
        try:
            height = page.evaluate("document.documentElement.scrollHeight")
        except Exception:
            height = 900 * steps
        per = max(450, int(min(height, 900 * 14) / max(steps, 1)))
        shots = 1
        try:
            page.mouse.move(720, 450)
            for i in range(1, steps + 1):
                for _ in range(max(1, per // 150)):
                    page.mouse.wheel(0, 150)
                    time.sleep(0.06)
                time.sleep(1.1)
                page.screenshot(path=str(target / f"desktop_{i:02d}.jpg"), type="jpeg", quality=72)
                shots += 1
        except Exception as exc:
            result["scroll_error"] = f"step {shots}: {str(exc)[:160]}"
        result["desktop_shots"] = shots
        result["renderer_crashed"] = crashed["flag"]
        if not crashed["flag"] and "scroll_error" not in result:
            measure("after-scroll")  # more fonts/lazy assets are live now
        try:
            ctx.close()
        except Exception:
            pass
        if mobile:
            mctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                                       is_mobile=True, has_touch=True, locale="en-US", user_agent=MOBILE_UA)
            mp = mctx.new_page()
            try:
                mp.goto(url, wait_until="domcontentloaded", timeout=60000)
                time.sleep(settle)
                mp.screenshot(path=str(target / "mobile_00.jpg"), type="jpeg", quality=70)
                mp.evaluate("window.scrollBy(0, 1400)")
                time.sleep(1.5)
                mp.screenshot(path=str(target / "mobile_01.jpg"), type="jpeg", quality=70)
                result["mobile_measure"] = mp.evaluate("""() => ({h1: [...document.querySelectorAll('h1')].slice(0,2).map(h => getComputedStyle(h).fontSize),
                   largest: [...document.querySelectorAll('body *')].filter(e => e.childElementCount===0 && (e.innerText||'').trim()).map(e => parseFloat(getComputedStyle(e).fontSize)).sort((a,b)=>b-a).slice(0,3),
                   overflow_x: document.documentElement.scrollWidth > window.innerWidth + 2})""")
            except Exception as exc:
                result["mobile_error"] = str(exc)[:200]
            mctx.close()
        browser.close()

    joined = "\n".join(requests)
    result["libs_from_requests"] = sorted(k for k, pat in LIB_PATTERNS.items() if re.search(pat, joined, re.I))
    result["assets_3d"] = sorted({u.split("?")[0] for u in requests if ASSET_3D.search(u)})[:25]
    result["assets_shader"] = sorted({u.split("?")[0] for u in requests if ASSET_SHADER.search(u)})[:15]
    hosts = Counter(urlparse(u).netloc for u in requests)
    result["top_hosts"] = hosts.most_common(12)
    result["request_count"] = len(requests)
    result["bytes_by_type_declared"] = dict(sizes.most_common(12))
    exts = Counter()
    for u in requests:
        m = re.search(r"\.(avif|webp|jpe?g|png|gif|svg|mp4|webm|m3u8|woff2?|ttf|otf|glb|gltf|ktx2|hdr|json|riv|lottie)(\?|$)", u, re.I)
        if m:
            exts[m.group(1).lower()] += 1
    result["asset_extensions"] = dict(exts.most_common())
    (target / "probe.json").write_text(json.dumps(result, indent=1, ensure_ascii=False))
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--out", type=Path, default=Path("probes"))
    ap.add_argument("--name", default=None)
    ap.add_argument("--steps", type=int, default=7)
    ap.add_argument("--settle", type=float, default=6.0, help="seconds to wait after load (preloaders)")
    ap.add_argument("--no-mobile", action="store_true")
    ap.add_argument("--gpu", choices=sorted(GPU_ARGS), default="metal",
                    help="metal = real GPU (macOS); swiftshader = software GL (Linux/CI)")
    args = ap.parse_args()
    name = args.name or re.sub(r"[^a-z0-9]+", "-", urlparse(args.url).netloc.lower()).strip("-")
    res = probe(args.url, args.out, name, args.steps, not args.no_mobile, args.settle, args.gpu)
    short = {k: res.get(k) for k in ["final_url", "title", "libs_from_requests", "globals", "contexts", "assets_3d", "request_count"]}
    print(json.dumps(short, indent=1))


if __name__ == "__main__":
    main()
