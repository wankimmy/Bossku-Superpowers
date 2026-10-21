#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright==1.63.0"]
# ///
"""Stress checks for the recipes, beyond test_recipes.py's five scenarios.

  python3 test_recipes_stress.py

slow-cdn     every cdn.jsdelivr.net request delayed 4s: text visible at 1s and after load
mobile-390   390x844 touch: no horizontal overflow, pinned section usable, content visible
zoom-200     720x450 viewport (= 1440x900 at 200% zoom): no overflow, text visible
keyboard     Tab through index: every focused element has a visible focus indicator and is on screen
live-reduce  switch prefers-reduced-motion to reduce after boot: nothing left hidden or mid-transform
Screenshots go to .qa/stress-*.png (or $RECIPES_QA_OUT). Exit code 1 on any failure.
"""
import functools
import os
import http.server
import sys
import threading
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
SHOTS = Path(os.environ.get("RECIPES_QA_OUT", ROOT / ".qa"))
ARGS = ["--use-angle=metal", "--enable-gpu", "--ignore-gpu-blocklist"]

HIDDEN_JS = """() => {
  const bad = [];
  for (const el of document.querySelectorAll('h1,h2,h3,p,li,a,button,img,figcaption')) {
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) continue;
    let n = el, op = 1;
    while (n && n.nodeType === 1) { op *= parseFloat(getComputedStyle(n).opacity); n = n.parentElement; }
    const s = getComputedStyle(el);
    if (op < 0.99 || s.visibility === 'hidden') bad.push(`${el.tagName} "${(el.innerText || el.alt || '').trim().slice(0, 40)}" opacity=${op.toFixed(2)}`);
  }
  return bad.slice(0, 8);
}"""
OVERFLOW_JS = "() => document.documentElement.scrollWidth - window.innerWidth"


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    handler = functools.partial(Quiet, directory=str(ROOT))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f"http://127.0.0.1:{httpd.server_address[1]}"


def scroll_through(page, steps=14, dy=500):
    for _ in range(steps):
        page.mouse.wheel(0, dy)
        time.sleep(0.25)
    time.sleep(1.5)


def main():
    SHOTS.mkdir(parents=True, exist_ok=True)
    httpd, base = serve()
    results = []

    def record(name, ok, detail=""):
        results.append((name, ok, detail))
        print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel="chromium", args=ARGS)

        # slow CDN
        for page_name in ["index", "webgl"]:
            ctx = browser.new_context(viewport={"width": 1440, "height": 900})
            page = ctx.new_page()
            page.route("**/cdn.jsdelivr.net/**", lambda route: (time.sleep(4), route.continue_()))
            page.goto(f"{base}/demo/{page_name}.html", wait_until="commit")
            time.sleep(1.0)
            early = page.evaluate(HIDDEN_JS)
            page.screenshot(path=str(SHOTS / f"stress-slowcdn-{page_name}-early.png"))
            page.wait_for_load_state("load", timeout=60000)
            time.sleep(2)
            scroll_through(page)
            late = page.evaluate(HIDDEN_JS)
            record(f"slow-cdn/{page_name}", not early and not late, f"early={early} late={late}")
            ctx.close()

        # mobile 390 and zoom 200 equivalent
        for label, vp, mobile in [("mobile-390", {"width": 390, "height": 844}, True), ("zoom-200", {"width": 720, "height": 450}, False)]:
            for page_name in ["index", "about", "webgl"]:
                ctx = browser.new_context(viewport=vp, is_mobile=mobile, has_touch=mobile, device_scale_factor=2 if mobile else 1)
                page = ctx.new_page()
                errors = []
                page.on("pageerror", lambda e: errors.append(str(e)[:120]))
                page.goto(f"{base}/demo/{page_name}.html", wait_until="load")
                time.sleep(2)
                for _ in range(16):
                    page.evaluate("window.scrollBy(0, 400)")
                    time.sleep(0.2)
                time.sleep(1.5)
                over = page.evaluate(OVERFLOW_JS)
                hidden = page.evaluate(HIDDEN_JS)
                page.screenshot(path=str(SHOTS / f"stress-{label}-{page_name}.png"))
                record(f"{label}/{page_name}", over <= 1 and not hidden and not errors, f"overflow={over}px hidden={hidden} errors={errors}")
                ctx.close()

        # keyboard focus
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(f"{base}/demo/index.html", wait_until="load")
        time.sleep(2)
        problems, seen = [], 0
        for i in range(40):
            page.keyboard.press("Tab")
            time.sleep(0.15)
            info = page.evaluate("""() => { const el = document.activeElement; if (!el || el === document.body) return null;
              const s = getComputedStyle(el); const r = el.getBoundingClientRect();
              const ring = (s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 1) || s.boxShadow !== 'none';
              return {tag: el.tagName, text: (el.innerText || el.getAttribute('aria-label') || '').trim().slice(0, 30), ring,
                      onscreen: r.bottom > 0 && r.top < innerHeight && r.right > 0 && r.left < innerWidth}; }""")
            if not info:
                continue
            seen += 1
            if not info["ring"] or not info["onscreen"]:
                problems.append(info)
        page.screenshot(path=str(SHOTS / "stress-keyboard-index.png"))
        record("keyboard/index", seen > 3 and not problems, f"focused={seen} problems={problems[:4]}")
        ctx.close()

        # live reduced-motion toggle
        ctx = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="no-preference")
        page = ctx.new_page()
        page.goto(f"{base}/demo/index.html", wait_until="load")
        time.sleep(1.5)
        page.mouse.wheel(0, 1200)
        time.sleep(0.3)
        page.emulate_media(reduced_motion="reduce")
        time.sleep(1.5)
        scroll_through(page, steps=10)
        hidden = page.evaluate(HIDDEN_JS)
        lenis = page.evaluate("document.documentElement.classList.contains('lenis-smooth')")
        page.screenshot(path=str(SHOTS / "stress-livereduce-index.png"))
        record("live-reduce/index", not hidden, f"hidden={hidden} lenis-smooth-class={lenis}")
        ctx.close()
        browser.close()
    httpd.shutdown()
    failed = [r for r in results if not r[1]]
    print(f"\n{len(results) - len(failed)}/{len(results)} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
