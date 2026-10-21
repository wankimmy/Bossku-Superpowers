#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright==1.63.0"]
# ///
"""
test_recipes.py: end-to-end proof that the recipes keep content visible and work.

What it does
  Serves this recipes/ folder over http (http.server on a free port, in a background thread, stopped at
  exit), then drives headless Chromium through Playwright over demo/index.html, demo/about.html and
  demo/webgl.html?stack (the WebGL recipes plus motion-core.js) in five scenarios, each in a fresh browser:
    normal       no console errors or failed requests; wheel-scroll the whole page, then every
                 [data-reveal], heading, paragraph, list item, link, caption and image is at opacity 1,
                 unclipped, unmasked and on screen; Lenis active (html.lenis); intro owned; split text
                 reverted; split masks clear every glyph at rest (pixel diff against the unsplit heading);
                 pin travelled; marquee pause button pauses and resumes; three-hero drew a
                 non-blank frame and followed the scroll; image hover drew planes and gave the <img> back;
                 the page-transition link navigates (with a View Transition).
    nojs         java_script_enabled=False: all text and images visible, loaded, unclipped, not moved off
                 screen; JS-only controls stay hidden; plain navigation works.
    reduced      reduced_motion='reduce': no Lenis, no hidden state at ANY sampled frame from first paint,
                 pin falls back to a vertical stack, marquee static, three-hero one still frame (or poster),
                 image hover never boots, navigation without a transition.
    nowebgl      getContext('webgl'|'webgl2'|'experimental-webgl') returns null: poster and images stay,
                 no WebGL canvas, no uncaught errors, the rest of the motion layer still runs.
    cdn-blocked  every cdn.jsdelivr.net request aborted: all content visible after the CSS deadline, nothing
                 stuck hidden, JS-only controls stay hidden, no uncaught errors.
  In every JS scenario an init script samples each tracked element on every animation frame from first
  paint, so a hidden state that exists for a single frame is caught, together with whether the element
  was in the viewport at boot (only the deadline-guarded [data-intro] may hide such an element).
  Screenshots: <out>/<scenario>-<page>-<n>.png (viewport-sized, taken while wheel-scrolling, so reveals are
  captured mid-flight; then the page-transition frames). Results: <out>/test_recipes_results.json.
  Prints a PASS/FAIL table and exits 1 on any failure.

Options
  --scenarios normal,nojs,reduced,nowebgl,cdn-blocked   (default: all)
  --pages index,about,webgl                            (default: all)
  --out DIR          screenshots + JSON (default: <repo>/evidence/recipes-qa)
  --no-shots         skip screenshots
  --headed           show the browser
  -v                 print every check, not only failures

Fallback behaviour
  Launches Playwright's full Chromium build (channel "chromium", new headless) with
  --use-angle=metal --enable-gpu --ignore-gpu-blocklist so WebGL runs on the GPU; if that channel is
  missing it falls back to the default headless shell. A run whose browser disconnects is retried once and
  the retry is reported. Needs network access to cdn.jsdelivr.net for every scenario except cdn-blocked.

Tested against
  gsap 3.15.0, lenis 1.3.26, three 0.186.1 (jsDelivr +esm via the demo import maps), Playwright 1.58.0,
  Chromium 145 (chromium-1208), Python 3, macOS on Apple silicon (ANGLE Metal), 2026-09-25.
  Pillow is optional (used for the blank-canvas and mask-clearance pixel checks; skipped with a note when missing).
"""
from __future__ import annotations

import os
import argparse
import atexit
import functools
import http.server
import io
import json
import socketserver
import sys
import threading
import time
from pathlib import Path

from playwright.sync_api import Error as PWError
from playwright.sync_api import sync_playwright

try:
    from PIL import Image, ImageChops, ImageStat
except ImportError:  # pixel checks (blank canvas, mask clearance) are skipped without Pillow
    Image = ImageChops = ImageStat = None

HERE = Path(__file__).resolve().parent                      # .../recipes
DEFAULT_OUT = Path(os.environ.get('RECIPES_QA_OUT', HERE / '.qa'))   # screenshots
GPU_ARGS = ['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist']
VIEWPORT = {'width': 1440, 'height': 900}
# webgl.html runs its recipes in isolation by default; ?stack also boots motion-core.js (Lenis + ScrollTrigger),
# which is how a real build ships them, so that is the combination tested here.
PAGES = {'index': 'demo/index.html', 'about': 'demo/about.html', 'webgl': 'demo/webgl.html?stack'}
NAV_TARGET = {'index': 'about.html', 'about': 'index.html', 'webgl': 'index.html'}
SCENARIOS = ['normal', 'nojs', 'reduced', 'nowebgl', 'cdn-blocked']
INTRO_DEADLINE_MS = 2000       # --intro-deadline default in boot.html-snippet.html
DEADLINE_SLACK_MS = 900        # first style resolution happens after navigation start

# ---------------------------------------------------------------------------------------------
# In-page scripts
# ---------------------------------------------------------------------------------------------

# Tracked elements: everything that carries content.
TRACK_SEL = ('h1,h2,h3,h4,h5,h6,p,li,figcaption,a,button,pre,img,'
             '[data-reveal],[data-intro],[data-intro-item],[data-intro-media]')

# Shared helpers, injected into both the per-frame monitor and the rest check.
HELPERS = r"""
const __desc = (el) => {
  const t = (el.getAttribute('alt') || el.getAttribute('aria-label') || el.textContent || '').trim().replace(/\s+/g, ' ');
  return el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.dataset.reveal ? '[reveal=' + el.dataset.reveal + ']' : '') + ' "' + t.slice(0, 44) + '"';
};
const __memo = () => {
  const op = new Map(), clip = new Map();
  const effOp = (n) => {
    if (!n || n.nodeType !== 1) return 1;
    if (op.has(n)) return op.get(n);
    const v = parseFloat(getComputedStyle(n).opacity) * effOp(n.parentElement);
    op.set(n, v); return v;
  };
  const clipOf = (n) => {
    if (!n || n.nodeType !== 1) return null;
    if (clip.has(n)) return clip.get(n);
    const cp = getComputedStyle(n).clipPath;
    const v = cp && cp !== 'none' ? cp : clipOf(n.parentElement);
    clip.set(n, v); return v;
  };
  return { effOp, clipOf };
};
// Fraction of the least visible split line inside its mask (1 = fully visible).
const __maskedFrac = (el) => {
  let min = 1;
  for (const ln of el.querySelectorAll('.rv-line')) {
    const m = ln.parentElement, r = ln.getBoundingClientRect(), mr = m.getBoundingClientRect();
    if (r.height < 1) continue;
    const vis = Math.max(0, Math.min(r.bottom, mr.bottom) - Math.max(r.top, mr.top)) / r.height;
    min = Math.min(min, vis);
  }
  return min;
};
const __skip = (el) => !!el.closest('[hidden], [inert], .skip');
"""

# Per-frame monitor (init script, JS scenarios). Records every hidden state with timing.
MONITOR_JS = r"""
(() => {
  if (window.__qa) return;
  const SEL = %s;
  %s
  const qa = window.__qa = { frames: 0, events: {}, vt: null, pageswapVT: null, lcp: [] };
  const meta = new WeakMap();
  addEventListener('pagereveal', (e) => {
    qa.vt = { reveal: !!e.viewTransition, types: e.viewTransition && e.viewTransition.types ? [...e.viewTransition.types] : [] };
  });
  try {
    new PerformanceObserver((l) => { for (const e of l.getEntries()) qa.lcp.push([Math.round(e.startTime), e.element ? e.element.tagName : null]); })
      .observe({ type: 'largest-contentful-paint', buffered: true });
  } catch (e) {}
  const inView = (r) => r.bottom > 0 && r.top < innerHeight && r.right > 0 && r.left < innerWidth && r.width > 0 && r.height > 0;
  function sample() {
    const now = performance.now();
    qa.frames++;
    const { effOp, clipOf } = __memo();
    for (const el of document.querySelectorAll(SEL)) {
      if (__skip(el)) continue;
      const r = el.getBoundingClientRect();
      let info = meta.get(el);
      if (!info) {
        info = { id: __desc(el), boot: now < 1500 && scrollY < 1 && inView(r),
                 intro: !!el.closest('[data-intro]') };
        meta.set(el, info);
      }
      const cs = getComputedStyle(el);
      if (cs.display === 'none') continue;
      const reasons = [];
      const o = effOp(el);
      if (o < 0.99) reasons.push(el.matches('img[data-gl-hover-hidden]') ? 'gl-replaced' : 'opacity');
      if (cs.visibility !== 'visible') reasons.push('visibility');
      const c = clipOf(el);
      if (c) reasons.push('clip-path');
      if (el.querySelector('.rv-line') && __maskedFrac(el) < 0.98) reasons.push('masked-lines');
      for (const reason of reasons) {
        const key = info.id + ' | ' + reason;
        let ev = qa.events[key];
        if (!ev) ev = qa.events[key] = { id: info.id, reason, first: Math.round(now), last: 0, count: 0,
                                         boot: info.boot, intro: info.intro, detail: reason === 'clip-path' ? c : (reason === 'opacity' ? o.toFixed(2) : '') };
        ev.last = Math.round(now); ev.count++;
      }
    }
    requestAnimationFrame(sample);
  }
  requestAnimationFrame(sample);
})();
""" % (json.dumps(TRACK_SEL), HELPERS)

# Rest check: everything that carries content is visible now.
REST_JS = r"""
(opts) => {
  %s
  const bad = [];
  const docW = document.documentElement.scrollWidth, docH = document.documentElement.scrollHeight;
  const { effOp, clipOf } = __memo();
  let n = 0;
  for (const el of document.querySelectorAll(%s)) {
    if (__skip(el)) continue;
    const isImg = el.tagName === 'IMG';
    const text = (el.textContent || '').trim();
    if (!isImg && !text && !el.querySelector('img')) continue;
    n++;
    const d = __desc(el);
    const cs = getComputedStyle(el);
    if (cs.display === 'none') { bad.push(d + ': display none'); continue; }
    const o = effOp(el);
    if (o < 0.99 && !(opts.allowGl && el.matches('[data-gl-hover-hidden]'))) bad.push(d + ': opacity ' + o.toFixed(2));
    if (cs.visibility !== 'visible') bad.push(d + ': visibility ' + cs.visibility);
    if (el.checkVisibility && !el.checkVisibility({ visibilityProperty: true, contentVisibilityAuto: true })) bad.push(d + ': checkVisibility() false');
    const c = clipOf(el);
    if (c) bad.push(d + ': clip-path ' + c);
    if (el.querySelector('.rv-line, .rv-line-mask')) bad.push(d + ': still split into masked lines');
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) bad.push(d + ': zero size');
    // A lazy image the visitor has not scrolled near yet is allowed to be unloaded (destination-page check).
    const lazyFar = opts.lazyOk && el.loading === 'lazy' && (r.top > innerHeight * 2 || r.bottom < -innerHeight);
    if (isImg && !lazyFar && (!el.complete || !el.naturalWidth)) bad.push(d + ': image not loaded');
    // Horizontal travel is the design inside a live pin or marquee: no geometric checks there.
    if (el.closest('[data-pin].is-pinned, [data-marquee].is-live')) continue;
    const L = r.left + scrollX, T = r.top + scrollY;
    if (L + r.width <= 0 || L >= docW || T + r.height <= 0 || T >= docH) { bad.push(d + ': transformed off the page'); continue; }
    if (isImg) continue; // media is cropped by its frame on purpose (cover, reveal scale, parallax over-scale)
    for (let a = el.parentElement; a && a !== document.documentElement; a = a.parentElement) {
      const acs = getComputedStyle(a);
      const cx = /hidden|clip/.test(acs.overflowX), cy = /hidden|clip/.test(acs.overflowY);
      if (!cx && !cy) continue;
      const ar = a.getBoundingClientRect();
      const fx = cx ? Math.max(0, Math.min(r.right, ar.right) - Math.max(r.left, ar.left)) / Math.max(r.width, 1) : 1;
      const fy = cy ? Math.max(0, Math.min(r.bottom, ar.bottom) - Math.max(r.top, ar.top)) / Math.max(r.height, 1) : 1;
      if (fx < 0.98 || fy < 0.98) { bad.push(d + ': cut by overflow of ' + __desc(a) + ' (' + fx.toFixed(2) + ', ' + fy.toFixed(2) + ')'); break; }
    }
  }
  return { checked: n, bad };
}
""" % (HELPERS, json.dumps(TRACK_SEL))

# Transforms left behind on revealed elements after their motion finished.
RESIDUE_JS = r"""
() => [...document.querySelectorAll('[data-reveal], [data-reveal] > *, [data-intro], [data-intro-item], [data-intro-media]')]
  .filter((el) => !el.closest('[data-pin], [data-stack]') && !el.hasAttribute('data-parallax'))
  .map((el) => { const cs = getComputedStyle(el); return [el, cs.transform, cs.translate, cs.scale]; })
  .filter(([, t, tr, s]) => (t !== 'none' && t !== 'matrix(1, 0, 0, 1, 0, 0)') || (tr !== 'none' && tr !== '0px') || (s !== 'none' && s !== '1'))
  .map(([el, t, tr, s]) => el.tagName.toLowerCase() + ' ' + (el.textContent || el.alt || '').trim().slice(0, 30) + ': ' + [t, tr, s].join(' / '))
"""

STATE_JS = r"""
() => {
  const q = (s) => document.querySelector(s);
  const pin = q('[data-pin="horizontal"]');
  const track = pin && pin.querySelector('[data-pin-track]');
  const panels = pin ? [...pin.querySelectorAll('[data-pin-panel]')].map((p) => p.getBoundingClientRect()) : [];
  return {
    motion: document.documentElement.dataset.motion || null,
    lenisClass: document.documentElement.classList.contains('lenis'),
    lenisInstance: !!(window.__motion && window.__motion.lenis),
    motionCore: !!window.__motion,
    introOwned: document.documentElement.hasAttribute('data-intro-owned'),
    hasIntro: !!q('[data-intro]'),
    hasMarquee: !!q('[data-marquee]'),
    marqueeLive: !!q('[data-marquee].is-live'),
    marqueeBtnHidden: q('[data-marquee-toggle]') ? q('[data-marquee-toggle]').hidden : null,
    hasPin: !!pin,
    pinned: !!q('[data-pin].is-pinned'),
    pinSpacer: !!q('.pin-spacer'),
    pinTrackTransform: track ? getComputedStyle(track).transform : null,
    pinDistance: track && pin ? Math.max(0, track.scrollWidth - pin.clientWidth) : 0,
    panelsVertical: panels.length > 1 && panels.every((r, i) => i === 0 || r.top >= panels[i - 1].bottom - 1),
    toggleHidden: q('[data-motion-toggle]') ? q('[data-motion-toggle]').hidden : null,
    webgl: !!q('[data-hero]'),
    heroCanvas: !!q('canvas[data-hero-canvas]'),
    hoverCanvas: !!q('canvas[data-gl-hover-canvas]'),
    overflowX: document.scrollingElement.scrollWidth - innerWidth,
  };
}
"""

NO_WEBGL_JS = r"""
(() => {
  const orig = HTMLCanvasElement.prototype.getContext;
  HTMLCanvasElement.prototype.getContext = function (type, ...rest) {
    if (/^(webgl2?|experimental-webgl)$/.test(String(type))) return null;
    return orig.call(this, type, ...rest);
  };
})();
"""

WEBGL_READY_JS = r"""
async () => {
  const d = window.__webglDemo;
  if (!d || !d.hover) return null;
  const [h, s] = await Promise.all([d.hover.ready, d.hero.ready]);
  return { hover: h, hero: s, heroState: d.hero.state(), hoverState: d.hover.state() };
}
"""
HERO_STATE_JS = "() => window.__webglDemo && window.__webglDemo.hero ? window.__webglDemo.hero.state() : null"
HOVER_STATE_JS = "() => window.__webglDemo && window.__webglDemo.hover ? window.__webglDemo.hover.state() : null"

# ---------------------------------------------------------------------------------------------
# Static server
# ---------------------------------------------------------------------------------------------

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):  # keep the table readable
        pass

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()


def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(HERE)))
    httpd.daemon_threads = True
    thread = threading.Thread(target=httpd.serve_forever, name='recipes-http', daemon=True)
    thread.start()

    stopped = []

    def stop():
        if stopped:
            return
        stopped.append(True)
        httpd.shutdown()
        httpd.server_close()

    atexit.register(stop)
    return httpd, stop


# ---------------------------------------------------------------------------------------------
# Run bookkeeping
# ---------------------------------------------------------------------------------------------

class Run:
    def __init__(self, scenario, page, out, shots, verbose):
        self.scenario, self.page, self.out, self.shots, self.verbose = scenario, page, out, shots, verbose
        self.checks = []          # (name, ok, detail)
        self.notes = []
        self.n = 0
        self.console, self.pageerrors, self.failed = [], [], []

    def check(self, name, ok, detail=''):
        self.checks.append((name, bool(ok), detail))
        if self.verbose or not ok:
            print(f"    {'PASS' if ok else 'FAIL'} {name}" + (f'  [{detail}]' if detail not in ('', None) else ''))

    def shot(self, pg, label=''):
        if not self.shots:
            return None
        self.n += 1
        path = self.out / f'{self.scenario}-{self.page}-{self.n}.png'
        try:
            pg.screenshot(path=str(path))
        except PWError as err:
            self.notes.append(f'screenshot {self.n} failed: {err}')
            return None
        if label:
            self.notes.append(f'{path.name}: {label}')
        return path

    @property
    def ok(self):
        return bool(self.checks) and all(ok for _, ok, _ in self.checks)

    def attach(self, pg):
        pg.on('console', lambda m: self.console.append((m.type, m.text, pg.url)))
        pg.on('pageerror', lambda e: self.pageerrors.append(f'{e} @ {pg.url}'))
        pg.on('requestfailed', lambda r: self.failed.append(f'{r.url[:120]} ({r.failure})'))
        pg.on('response', lambda r: r.status >= 400 and self.failed.append(f'{r.url[:120]} (HTTP {r.status})'))
        pg.on('crash', lambda: self.pageerrors.append('renderer crashed'))


# ---------------------------------------------------------------------------------------------
# Steps
# ---------------------------------------------------------------------------------------------

STEADY_JS = r"""
() => new Promise((resolve) => {
  // Freeze GSAP's ticker (it drives Lenis and every tween) so the capture sees one consistent frame, then wait
  // until the scroll offset has been identical for two frames (native smooth wheel scrolling settles too).
  const g = window.__motion && window.__motion.gsap;
  if (g) g.ticker.sleep();
  let last = -1, same = 0;
  const tick = () => {
    if (scrollY === last) { if (++same >= 2) return resolve(!!g); } else { same = 0; last = scrollY; }
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
  setTimeout(() => resolve(!!g), 1000);
})
"""


def steady_shot(pg, run, label):
    """Screenshot mid-scroll without the capture artifact: Playwright frames a viewport shot from the scroll offset
    it reads just before capturing, so while Lenis moves the page on the main thread a band of one frame's scroll
    height comes out blank at the top edge (it cut plain images as well as text, so it is not the page). Freezing
    the ticker keeps mid-flight reveals in the shot, in a steady frame; waking it resumes them where they were."""
    frozen = False
    try:
        if run.scenario == 'nojs':
            # Page rAF/timers never fire with scripting disabled: poll the (native) scroll offset from here.
            last = None
            for _ in range(20):
                y = scroll_info(pg)[0]
                if y == last:
                    break
                last = y
                time.sleep(0.05)
        else:
            frozen = pg.evaluate(STEADY_JS)
        return run.shot(pg, label)
    finally:
        if frozen:
            pg.evaluate('() => window.__motion.gsap.ticker.wake()')


def scroll_info(pg):
    return pg.evaluate('() => [Math.round(scrollY), Math.max(0, document.scrollingElement.scrollHeight - innerHeight), innerHeight]')


def wheel_walk(pg, run, step=240, pause=0.05, max_steps=900, label='scroll'):
    """Scroll the whole page with real wheel events (Lenis handles them when it is on), taking a viewport
    screenshot roughly every viewport height. Returns (reached_bottom, steps, final_y, max_y)."""
    pg.mouse.move(VIEWPORT['width'] * 0.5, VIEWPORT['height'] * 0.55)
    y, maxy, vh = scroll_info(pg)
    last_shot, still, steps = y, 0, 0   # the caller has already shot the top of the page
    for steps in range(1, max_steps + 1):
        pg.mouse.wheel(0, step)
        time.sleep(pause)
        y, maxy, vh = scroll_info(pg)
        # Shot every ~0.7 viewport: smoothed scroll keeps moving after the wheel stops, so consecutive
        # shots still overlap and together cover every pixel of the page, reveals caught mid-flight.
        if y - last_shot >= vh * 0.7:
            steady_shot(pg, run, f'{label} y={y}')
            last_shot = scroll_info(pg)[0]
        if y >= maxy - 2:
            still += 1
            if still >= 10:
                break
        else:
            still = 0
    if y > last_shot + 10:
        steady_shot(pg, run, f'{label} y={y} (bottom)')
    return y >= maxy - 2, steps, y, maxy


def canvas_not_blank(pg, selector):
    """Screenshot the centre of the element and require real pixel variation (not a flat clear colour)."""
    if Image is None:
        return None, 'Pillow missing: skipped'
    box = pg.evaluate("""(s) => { const r = document.querySelector(s).getBoundingClientRect();
        return { x: r.left + r.width * 0.3, y: Math.max(0, r.top) + r.height * 0.25, width: r.width * 0.4, height: r.height * 0.5 }; }""", selector)
    png = pg.screenshot(clip=box)
    im = Image.open(io.BytesIO(png)).convert('L')
    sd = ImageStat.Stat(im).stddev[0]
    lo, hi = im.getextrema()
    return sd > 6 and hi - lo > 40, f'stddev {sd:.1f}, range {lo}-{hi}'


def mask_clearance_check(pg, run):
    """"Clear the cut": re-split every split-able heading with motion-core's SplitText config, lines at rest
    (yPercent 0) inside their overflow-clip masks, and require the pixels to match the unsplit heading. A mask
    that shaves descenders/accents, or padding that shifts the layout, shows up as a pixel difference."""
    if Image is None:
        run.check('split masks clear every glyph at rest', True, 'Pillow missing: skipped')
        return
    sels = pg.evaluate("""() => [...document.querySelectorAll('h1[data-intro], h2[data-reveal="lines"], h3[data-reveal="lines"]')]
        .map((e, i) => { e.dataset.qaMask = i; return `[data-qa-mask="${i}"]`; })""")
    worst = []
    for sel in sels:
        pg.evaluate(f"document.querySelector('{sel}').scrollIntoView({{ block: 'center' }})")
        time.sleep(0.25)
        box = pg.evaluate(f"""() => {{ const r = document.querySelector('{sel}').getBoundingClientRect();
            return {{ x: Math.max(0, r.left - 10), y: Math.max(0, r.top - 30), width: r.width + 20, height: r.height + 60 }}; }}""")
        a = Image.open(io.BytesIO(pg.screenshot(clip=box))).convert('L')
        n = pg.evaluate(f"""() => {{ window.__qaSplit = window.__motion.SplitText.create(document.querySelector('{sel}'),
            {{ type: 'lines', mask: 'lines', linesClass: 'rv-line', aria: 'auto' }}); return window.__qaSplit.lines.length; }}""")
        time.sleep(0.05)
        b = Image.open(io.BytesIO(pg.screenshot(clip=box))).convert('L')
        pg.evaluate("() => { window.__qaSplit.revert(); window.__qaSplit = null; }")
        diff = ImageChops.difference(a, b)
        worst.append((sel, n, diff.getextrema()[1], ImageStat.Stat(diff).mean[0]))
    bad = [w for w in worst if w[2] > 40 or w[3] > 0.2]
    run.check(f'split masks clear every glyph at rest ({len(worst)} headings, pixel-identical to unsplit)', not bad,
              '; '.join(f'{s} lines={n} maxdiff={m} MAD={d:.2f}' for s, n, m, d in (bad or worst)))


def rest_checks(pg, run, allow_gl=False, residue=True):
    res = pg.evaluate(REST_JS, {'allowGl': allow_gl})
    run.check(f"all content visible, unclipped, on the page ({res['checked']} elements)", not res['bad'], '; '.join(res['bad'][:8]))
    if residue:
        left = pg.evaluate(RESIDUE_JS)
        run.check('no transforms left on revealed/intro elements', not left, '; '.join(left[:6]))
    st = pg.evaluate(STATE_JS)
    run.check('no horizontal page overflow', st['overflowX'] <= 1, f"{st['overflowX']}px")
    return st


def monitor_events(pg):
    return pg.evaluate('() => window.__qa ? { frames: window.__qa.frames, events: Object.values(window.__qa.events), vt: window.__qa.vt, lcp: window.__qa.lcp } : null')


def marquee_check(pg, run):
    info = pg.evaluate("""() => { const b = document.querySelector('[data-marquee-toggle]');
        return b ? { hidden: b.hidden, display: getComputedStyle(b).display } : null; }""")
    run.check('marquee pause button shown (motion on)', info and not info['hidden'] and info['display'] != 'none', str(info))
    if not info or info['hidden']:
        return
    pg.evaluate("document.querySelector('[data-marquee]').scrollIntoView({ block: 'center' })")
    time.sleep(0.5)
    anim_js = """() => { const t = document.querySelector('[data-marquee-track]');
        const a = t.getAnimations().find((x) => x.animationName === 'marquee');
        const m = document.querySelector('[data-marquee]'), b = document.querySelector('[data-marquee-toggle]');
        return { t: a ? a.currentTime : null, state: a ? a.playState : 'none', pressed: b.getAttribute('aria-pressed'),
                 paused: m.classList.contains('is-paused') }; }"""
    away = "() => { document.activeElement && document.activeElement.blur(); }"
    a0 = pg.evaluate(anim_js)
    run.check('marquee loop running before pause', a0['state'] == 'running', str(a0))
    pg.click('[data-marquee-toggle]')
    pg.mouse.move(5, 5)
    pg.evaluate(away)
    time.sleep(0.15)
    a1 = pg.evaluate(anim_js)
    time.sleep(0.6)
    a2 = pg.evaluate(anim_js)
    run.check('pause button: aria-pressed=true, is-paused, loop frozen',
              a1['pressed'] == 'true' and a1['paused'] and a2['state'] == 'paused' and a1['t'] == a2['t'], f'{a1} -> {a2}')
    run.shot(pg, 'marquee paused')
    pg.click('[data-marquee-toggle]')
    pg.mouse.move(5, 5)
    pg.evaluate(away)
    time.sleep(0.15)
    b1 = pg.evaluate(anim_js)
    time.sleep(0.6)
    b2 = pg.evaluate(anim_js)
    run.check('play again: aria-pressed=false, loop advances',
              b1['pressed'] == 'false' and not b1['paused'] and b2['state'] == 'running' and (b2['t'] or 0) > (b1['t'] or 0),
              f'{b1} -> {b2}')


def hover_check(pg, run):
    """Sweep the pointer across one image: planes must draw, and the <img> must come back at rest."""
    pg.evaluate("document.querySelector('img[data-gl-hover]').scrollIntoView({ block: 'center' })")
    time.sleep(0.6)
    try:
        pg.wait_for_function("() => window.__webglDemo.hover.state().planes >= 1", timeout=8000)
    except PWError:
        pass
    before = pg.evaluate(HOVER_STATE_JS)
    r = pg.evaluate("() => { const b = document.querySelector('img[data-gl-hover]').getBoundingClientRect(); return { x: b.left, y: b.top, w: b.width, h: b.height }; }")
    hid, shot_taken = False, False
    for i in range(31):
        pg.mouse.move(r['x'] + r['w'] * (0.1 + 0.8 * i / 30), r['y'] + r['h'] * (0.45 + 0.1 * (i % 2)))
        time.sleep(0.016)
        if not hid:
            hid = pg.evaluate("() => !!document.querySelector('img[data-gl-hover-hidden]')")
        if hid and not shot_taken and i > 12:
            run.shot(pg, 'image hover plane mid-sweep')
            shot_taken = True
    after = pg.evaluate(HOVER_STATE_JS)
    run.check('image hover: planes render while the pointer moves',
              after['renders'] > before['renders'] and hid, f"renders {before['renders']} -> {after['renders']}, img handed to GL: {hid}")
    time.sleep(1.5)
    back = pg.evaluate("() => [...document.querySelectorAll('img[data-gl-hover]')].map((i) => getComputedStyle(i).opacity + (i.hasAttribute('data-gl-hover-hidden') ? '*' : ''))")
    run.check('image hover: every <img> visible again with a still pointer', all(v == '1' for v in back), str(back))


def navigate_check(pg, run, scenario, js=True):
    dest = NAV_TARGET[run.page]
    link = pg.locator(f'nav[aria-label="Harness pages"] a[href="{dest}"]').first
    link.scroll_into_view_if_needed()
    time.sleep(0.3)
    link.click()
    try:
        pg.wait_for_url(f'**/{dest}', timeout=10000)
        arrived = True
    except PWError:
        arrived = False
    time.sleep(0.35)
    run.shot(pg, f'after clicking the page-transition link to {dest} (mid-transition)')
    run.check(f'page-transition link navigates to {dest}', arrived, pg.url)
    if not arrived:
        return
    pg.wait_for_load_state('load')
    time.sleep(2.6 if scenario == 'cdn-blocked' else 1.8)
    if js:
        mon = monitor_events(pg) or {}
        vt = mon.get('vt')
        if scenario == 'reduced':
            run.check('no View Transition under reduced motion', not (vt and vt['reveal']), str(vt))
        elif scenario in ('normal', 'nowebgl'):
            run.check('cross-document View Transition ran', bool(vt and vt['reveal']), str(vt))
    res = pg.evaluate(REST_JS, {'allowGl': True, 'lazyOk': True})
    top = res['bad']
    h1 = pg.evaluate("() => { const h = document.querySelector('h1'); const r = h.getBoundingClientRect(); return { top: r.top, clip: getComputedStyle(h).clipPath, text: h.textContent.trim().slice(0, 40) }; }")
    run.check('destination page: h1 visible and unclipped', h1['clip'] == 'none', str(h1))
    run.check('destination page: content visible', not top, '; '.join(top[:5]))
    run.shot(pg, f'destination {dest} at rest')


# ---------------------------------------------------------------------------------------------
# One scenario on one page
# ---------------------------------------------------------------------------------------------

def run_one(p, base, scenario, page, out, shots, verbose, headed):
    run = Run(scenario, page, out, shots, verbose)
    js = scenario != 'nojs'
    launch = {'args': GPU_ARGS, 'headless': not headed}
    try:
        browser = p.chromium.launch(channel='chromium', **launch)
    except PWError:
        browser = p.chromium.launch(**launch)
        run.notes.append('channel "chromium" unavailable: used the default headless shell')
    try:
        ctx_opts = {'viewport': VIEWPORT, 'device_scale_factor': 1}
        if scenario == 'nojs':
            ctx_opts['java_script_enabled'] = False
        if scenario == 'reduced':
            ctx_opts['reduced_motion'] = 'reduce'
        ctx = browser.new_context(**ctx_opts)
        if js:
            ctx.add_init_script(MONITOR_JS)
        if scenario == 'nowebgl':
            ctx.add_init_script(NO_WEBGL_JS)
        if scenario == 'cdn-blocked':
            ctx.route('https://cdn.jsdelivr.net/**', lambda route: route.abort())
        pg = ctx.new_page()
        run.attach(pg)
        pg.goto(base + PAGES[page], wait_until='load')

        # ---- boot ---------------------------------------------------------------------------
        if scenario == 'cdn-blocked':
            time.sleep((INTRO_DEADLINE_MS + DEADLINE_SLACK_MS) / 1000)
        elif js:
            try:
                pg.wait_for_function('() => !!window.__motion', timeout=15000)
            except PWError:
                pass
            if scenario in ('normal', 'nowebgl'):
                try:
                    pg.wait_for_function("() => document.documentElement.classList.contains('lenis')", timeout=10000)
                except PWError:
                    pass
            time.sleep(1.6)  # intro plays out (<= 1.4s by the tokens)
        else:
            time.sleep(0.5)

        st = pg.evaluate(STATE_JS)
        wg = None
        if st['webgl'] and js:
            try:
                wg = pg.evaluate(WEBGL_READY_JS)
            except PWError as err:
                wg = {'error': str(err)}
        run.shot(pg, 'boot, top of page')

        if scenario in ('normal', 'nowebgl'):
            run.check('motion-core booted (data-motion=full)', st['motionCore'] and st['motion'] == 'full', f"motion={st['motion']}")
            run.check('Lenis active (html.lenis + instance)', st['lenisClass'] and st['lenisInstance'])
            if st['hasIntro']:
                run.check('intro handed to JS (data-intro-owned)', st['introOwned'])
            if st['hasPin']:
                run.check('pin engaged at 1440px (is-pinned + pin-spacer)', st['pinned'] and st['pinSpacer'])
            if st['hasMarquee']:
                run.check('marquee live (clone + loop)', st['marqueeLive'])
        if scenario == 'reduced':
            run.check('data-motion=reduce from the OS setting', st['motion'] == 'reduce')
            run.check('no Lenis smoothing (no html.lenis, no instance)', not st['lenisClass'] and not st['lenisInstance'],
                      f"class={st['lenisClass']} instance={st['lenisInstance']} core={st['motionCore']}")
            if st['hasPin']:
                run.check('pin falls back to a vertical stack', not st['pinned'] and not st['pinSpacer'] and st['panelsVertical']
                          and st['pinTrackTransform'] in ('none', None), f"pinned={st['pinned']} vertical={st['panelsVertical']} transform={st['pinTrackTransform']}")
            if st['hasMarquee']:
                run.check('marquee static, no pause button needed', not st['marqueeLive'] and st['marqueeBtnHidden'])
        if scenario in ('nojs', 'cdn-blocked'):
            run.check('no Lenis, no pin, no live marquee (static page)', not st['lenisClass'] and not st['pinned'] and not st['marqueeLive'])
            if st['hasMarquee']:
                run.check('JS-only marquee button stays hidden', st['marqueeBtnHidden'] is True)
            if st['toggleHidden'] is not None:
                run.check('JS-only motion toggle stays hidden', st['toggleHidden'] is True)
            if st['hasPin']:
                run.check('pin section is a vertical stack', st['panelsVertical'])

        hero_renders0 = None
        if st['webgl']:
            if scenario == 'normal':
                ok = wg and wg.get('hover') is True and wg.get('hero') is True and wg['heroState'].get('live')
                run.check('WebGL live: three-hero + image hover ready', ok, str(wg))
                if ok:
                    nb, detail = canvas_not_blank(pg, '[data-hero]')
                    run.check('three-hero canvas drew a non-blank frame', nb is not False, detail)
                    run.check('three-hero scroll move armed (shared ScrollTrigger)', wg['heroState'].get('scroll') is True, str(wg['heroState']))
                    hero_renders0 = wg['heroState']['renders']
            elif scenario == 'reduced':
                ok = wg and wg.get('hover') is False
                run.check('image hover never boots under reduced motion', ok and not st['hoverCanvas'], str(wg))
                hs = (wg or {}).get('heroState') or {}
                run.check('three-hero: one still frame or the poster', hs.get('renders', 0) <= 1 and not hs.get('running') and not hs.get('scroll'), str(hs))
                if hs.get('live'):
                    nb, detail = canvas_not_blank(pg, '[data-hero]')
                    run.check('three-hero still frame is not blank', nb is not False, detail)
                hero_renders0 = hs.get('renders', 0)
            elif scenario in ('nowebgl', 'cdn-blocked'):
                ok = wg and wg.get('hover') is False and wg.get('hero') is False
                run.check('both WebGL recipes fell back (ready=false)', ok, str(wg))
                run.check('no WebGL canvas was inserted', not st['heroCanvas'] and not st['hoverCanvas'])
            elif scenario == 'nojs':
                run.check('no canvas without JS', not st['heroCanvas'] and not st['hoverCanvas'])
            poster = pg.evaluate("() => { const i = document.querySelector('[data-hero-poster]'); const cs = getComputedStyle(i); return { op: cs.opacity, vis: cs.visibility, loaded: i.complete && i.naturalWidth > 0, cur: (i.currentSrc || '').slice(0, 22) }; }")
            run.check('hero poster visible and loaded', poster['op'] == '1' and poster['vis'] == 'visible' and poster['loaded'], str(poster))

        # ---- scroll the whole page ----------------------------------------------------------------
        bottom, steps, y, maxy = wheel_walk(pg, run)
        run.check('wheel scroll reached the bottom', bottom, f'y={y} max={maxy} steps={steps}')
        time.sleep(2.4)            # longest reveal is dur-6 x 1.15 = 1.6s
        pg.mouse.move(8, 8)
        time.sleep(0.4)

        # ---- at rest --------------------------------------------------------------------------------
        st2 = rest_checks(pg, run, allow_gl=False, residue=js)
        if scenario == 'normal' and st2['hasPin']:
            import re
            m = re.match(r'matrix\(1, 0, 0, 1, (-?[\d.]+), 0\)', st2['pinTrackTransform'] or '')
            tx = float(m.group(1)) if m else None
            run.check('pin track travelled its full distance', tx is not None and abs(tx + st2['pinDistance']) <= 2,
                      f"x={tx} distance={st2['pinDistance']}")
        if st2['hasPin'] and scenario == 'reduced':
            run.check('pin still vertical after scrolling', not st2['pinned'] and st2['panelsVertical'])
        if st['webgl'] and scenario == 'normal' and hero_renders0 is not None:
            hs = pg.evaluate(HERO_STATE_JS)
            run.check('three-hero followed the scroll (renders increased, loop stopped at rest)',
                      hs['renders'] > hero_renders0 and not hs['running'], f"{hero_renders0} -> {hs}")
        if st['webgl'] and scenario == 'reduced':
            pg.mouse.move(300, 300)
            pg.mouse.move(900, 500)
            time.sleep(0.5)
            hs = pg.evaluate(HERO_STATE_JS) or {}
            run.check('three-hero: pointer and scroll caused no renders', hs.get('renders', 0) == (hero_renders0 or 0), f'{hero_renders0} -> {hs}')

        # ---- per-frame monitor ------------------------------------------------------------------------
        if js:
            mon = monitor_events(pg)
            if mon is None:
                run.check('frame monitor ran', False, 'window.__qa missing')
            else:
                ev = mon['events']
                fmt = lambda es: '; '.join(f"{e['id']} {e['reason']}{'=' + e['detail'] if e['detail'] else ''} @{e['first']}-{e['last']}ms x{e['count']}" for es_ in [es] for e in es_[:6])
                if scenario == 'reduced':
                    run.check(f"no hidden state in any of {mon['frames']} frames", not ev, fmt(ev))
                elif scenario == 'cdn-blocked':
                    stuck = [e for e in ev if not e['intro'] or e['last'] > INTRO_DEADLINE_MS + DEADLINE_SLACK_MS]
                    intro = [e for e in ev if e['intro']]
                    run.check(f"only the deadline-guarded intro was ever hidden, and only until the deadline ({mon['frames']} frames)",
                              not stuck, fmt(stuck) or (('intro released @' + str(max(e['last'] for e in intro)) + 'ms') if intro else 'nothing was ever hidden'))
                else:
                    boot = [e for e in ev if e['boot'] and not e['intro'] and e['reason'] != 'gl-replaced']
                    run.check(f"nothing on screen at boot was re-hidden (except the deadline-guarded intro; {mon['frames']} frames)",
                              not boot, fmt(boot))
                    if scenario == 'normal':
                        run.notes.append('hidden-while-animating (expected, lazy-armed): ' + fmt([e for e in ev if not e['boot']])[:600])
                if mon.get('lcp'):
                    run.notes.append(f"LCP entries: {mon['lcp']}")

        # ---- scenario extras --------------------------------------------------------------------------
        if scenario == 'normal' and st['motionCore'] and pg.evaluate("() => !!document.querySelector('h1[data-intro], [data-reveal=\"lines\"]')"):
            mask_clearance_check(pg, run)
        if scenario == 'normal' and st['hasMarquee']:
            marquee_check(pg, run)
        if scenario == 'normal' and st['webgl'] and wg and wg.get('hover'):
            hover_check(pg, run)

        # ---- errors -------------------------------------------------------------------------------------
        errs = [f'{t}: {m}' for t, m, _ in run.console if t == 'error']
        if scenario in ('normal', 'reduced'):
            run.check('no console errors', not errs, '; '.join(errs[:5]))
            run.check('no failed requests', not run.failed, '; '.join(run.failed[:5]))
        if js:
            run.check('no uncaught page errors', not run.pageerrors, '; '.join(run.pageerrors[:5]))
        warns = [f'{t}: {m}' for t, m, _ in run.console if t in ('warning', 'error')]
        if warns:
            run.notes.append('console: ' + ' | '.join(w[:200] for w in warns[:6]))

        # ---- page transition (last: it leaves the page) -------------------------------------------
        navigate_check(pg, run, scenario, js=js)
        if js:
            errs2 = [e for e in run.pageerrors]
            run.check('no uncaught page errors after navigating', not errs2, '; '.join(errs2[:5]))
        return run
    finally:
        try:
            browser.close()
        except PWError:
            pass


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--scenarios', default=','.join(SCENARIOS))
    ap.add_argument('--pages', default=','.join(PAGES))
    ap.add_argument('--out', default=str(DEFAULT_OUT))
    ap.add_argument('--no-shots', action='store_true')
    ap.add_argument('--headed', action='store_true')
    ap.add_argument('-v', '--verbose', action='store_true')
    args = ap.parse_args()
    scenarios = [s for s in args.scenarios.split(',') if s]
    pages = [p for p in args.pages.split(',') if p]
    bad = [s for s in scenarios if s not in SCENARIOS] + [p for p in pages if p not in PAGES]
    if bad:
        ap.error(f'unknown scenario/page: {bad}')
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    httpd, stop = start_server()
    base = f'http://127.0.0.1:{httpd.server_address[1]}/'
    print(f'serving {HERE} at {base}')
    runs = []
    try:
        with sync_playwright() as p:
            for scenario in scenarios:
                for page in pages:
                    for old in out.glob(f'{scenario}-{page}-*.png'):
                        old.unlink()
                    print(f'-- {scenario} / {page}')
                    t0 = time.time()
                    attempt, run = 0, None
                    while attempt < 2:
                        attempt += 1
                        try:
                            run = run_one(p, base, scenario, page, out, not args.no_shots, args.verbose, args.headed)
                            break
                        except PWError as err:
                            msg = str(err).splitlines()[0]
                            if attempt < 2 and ('closed' in msg.lower() or 'disconnected' in msg.lower() or 'crash' in msg.lower()):
                                print(f'    browser went away ({msg}); retrying once')
                                continue
                            run = Run(scenario, page, out, False, args.verbose)
                            run.check('run completed without a driver error', False, msg)
                            break
                    if attempt > 1:
                        run.notes.append('retried once after the browser disconnected')
                    run.secs = time.time() - t0
                    runs.append(run)
    finally:
        stop()

    # ---- table ----------------------------------------------------------------------------------------
    print('\n' + '=' * 96)
    print(f"{'scenario':<12} {'page':<7} {'result':<6} {'checks':>7} {'secs':>5}  failures")
    print('-' * 96)
    for r in runs:
        passed = sum(1 for _, ok, _ in r.checks if ok)
        fails = [n for n, ok, _ in r.checks if not ok]
        print(f"{r.scenario:<12} {r.page:<7} {'PASS' if r.ok else 'FAIL':<6} {passed:>3}/{len(r.checks):<3} {r.secs:>5.0f}  {'; '.join(fails)[:60]}")
    print('=' * 96)
    total_fail = sum(1 for r in runs if not r.ok)
    print(f'{len(runs) - total_fail}/{len(runs)} scenario-page runs passed; screenshots in {out}')

    (out / 'test_recipes_results.json').write_text(json.dumps([
        {'scenario': r.scenario, 'page': r.page, 'ok': r.ok, 'secs': round(r.secs, 1),
         'checks': [{'name': n, 'ok': ok, 'detail': d} for n, ok, d in r.checks], 'notes': r.notes}
        for r in runs], indent=1))
    return 1 if total_fail else 0


if __name__ == '__main__':
    sys.exit(main())
