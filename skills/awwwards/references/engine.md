<!-- Generated from tests/nexttest by tests/_gen/build.py; edit there, not here. -->
# Motion engine (framework-agnostic)

The plumbing that award-level sites get wrong, solved once:
- one clock (GSAP ticker drives Lenis, ScrollTrigger and WebGL)
- a page lifecycle that reverts every effect on navigation
- a loader that tracks real progress
- page transitions that overlap with the page fetch
- declarative reveals that stay accessible
- reduced-motion and no-JS paths that keep content visible

It is plain TypeScript with no framework imports and no DOM access at import time, so it is
safe under SSR. A small adapter connects it to the router: `nextjs.md`, `astro.md`, or the
contract below for any other stack.

The engine is not the design. The loader look, the transition, the tokens and every page are
authored per project. Shipping the defaults is a failure.

Dependencies: `npm i gsap lenis` (+ `ogl` for WebGL, see webgl.md).

## Files

```
src/engine/
  env.ts           media queries + the shared easing names
  scroll.ts        Lenis on the GSAP ticker; onScroll feed (y, velocity, progress)
  reveal.ts        data-split / data-reveal / data-parallax / data-intro
  loader.ts        first-load progress + exit (setLoaderFormat, setLoaderExit)
  interactions.ts  data-magnetic, cursor follower (data-cursor)
  transition.ts    curtain leave/enter (setTransition)
  index.ts         lifecycle core: boot, leave, cleanup, enter, onPage
  gl/              optional WebGL module (webgl.md)
  next.tsx | astro.ts   the adapter for your router
tokens.css         design tokens (names below are the contract; values are yours)
engine.css         foundation + engine CSS
```

## Adapter contract (wire these four hooks in any framework)

| When | Call |
|---|---|
| First load, after the DOM is ready (client only) | `boot()`: flags, scroll, GL, cursor, page init, loader, intro |
| A route change starts (internal link click) | `await leave()`: covers the screen with the curtain. Fetch the next page in parallel when the router allows it |
| Just before the old page's DOM is removed | `cleanup()`: reverts tweens, ScrollTriggers and splits, and removes GL planes |
| After the new page's DOM is in place | `enter()`: scroll to top, init page, uncover, play the intro. Back/forward: `enter({ transition: false, scrollTop: false })` |

SvelteKit: `beforeNavigate` → leave + cleanup, `afterNavigate` → enter. Nuxt: `page:start` /
`page:finish` hooks. Vite + React Router: intercept link clicks like the Next adapter, then call
`enter` in a `useEffect` on `location.pathname`.

## Layout contract (markup every page shares)

```html
<html lang="en">                     <!-- inline script in <head> adds .js and .motion before paint -->
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <div id="gl" aria-hidden="true"></div>              <!-- WebGL canvas host, persists -->
  <div id="curtain" aria-hidden="true"><div class="curtain__panel"></div></div>
  <div id="cursor" aria-hidden="true"><span data-cursor-label></span></div>   <!-- optional -->
  <div id="loader" role="status" aria-label="Loading">                         <!-- optional -->
    <span data-loader-out>Name</span> <span data-loader-out data-loader-count>000</span>
    <div data-loader-bar></div>
  </div>
  <header>…</header>
  <main id="main" tabindex="-1">…page…</main>
  <footer>…</footer>
</body>
```
Before first paint, the inline head script must run:
`document.documentElement.classList.add('js'); if (!matchMedia('(prefers-reduced-motion: reduce)').matches) document.documentElement.classList.add('motion');`
Hidden-before-reveal styles are gated on `html.motion`, so content stays visible without JS
and under reduced motion. `#gl`, `#curtain` and `#cursor` must survive navigation (persistent
layout in Next, `transition:persist` in Astro). The loader is hidden (not removed) when done
and sets `html.is-loaded`. QA scripts detect any `#loader` element.

## Markup API (data attributes)

| Attribute | Effect |
|---|---|
| `data-split="lines\|words\|chars"` | Masked text reveal via SplitText (re-splits on resize/font load, stays accessible) |
| `data-reveal="up\|fade\|clip\|scale"` | Block reveal. `clip` wipes up, `scale` opens from an inset |
| `data-intro` | Play with the page intro instead of on scroll (use in heroes) |
| `data-delay="0.2"` | Extra delay in seconds (works with split, reveal, GL) |
| `data-parallax="0.15"` | Scrubbed drift, fraction of the element height. Put it on an inner element inside an `overflow: clip` frame |
| `data-magnetic="0.35"` | Element leans toward the pointer |
| `data-cursor="View"` | Cursor follower grows with this label over the element |
| `data-gl`, `data-gl="procedural"`, `data-gl-*` | WebGL planes (webgl.md) |

Put `data-split` only on text that never re-renders on the client (server-rendered or static).
SplitText rewrites the DOM inside the element.

## Script API (`import { … } from '@/engine'` or a relative path)

```ts
onPage(({ intro, path }) => {        // every page load, inside a gsap.context; returns an unsubscribe
  const el = document.querySelector('[data-marquee]');
  if (!el) return;                   // global modules register once: check presence
  intro.add(gsap.from('.hero-meta', { autoAlpha: 0, y: 20 }), 0.4); // extend the page intro
  return () => { /* remove listeners you added to window/document */ };
});
// React: usePage(fn) from the adapter does the same for one component (registers on mount).

setTransition({ leave: (curtain) => tl, enter: (curtain) => tl }); // replace the default wipe
setLoaderFormat((p) => `${p}`);                                    // counter text, p: 0 → 100 (a clock, a year…)
setLoaderExit((root) => gsap.timeline()…);                         // the loader → hero handoff
onScroll(({ y, velocity, progress }) => {});                       // one-clock scroll feed; returns an unsubscribe
scrollToTarget('#work');  stopScroll();  startScroll();
setBackground(fragmentGLSL, uniforms); clearBackground(); hideGL(0.6);   // webgl.md
ease.out | ease.inOut | ease.soft | ease.spring                    // the shared easing names
prefersReducedMotion(), isTouch(), isMobile()
```

Call global setup (`setTransition`, `setLoaderFormat`, `setLoaderExit`, `setBackground`, the
driver module) once on the client **before** `boot()` runs: in Astro, from a script imported
right after the adapter; in Next, at module level of a client module imported by the
component that renders `<Engine />`. These setters touch no DOM, so they are safe in modules
that also render on the server.

## Lifecycle

- **First load:** the head script flags `html.js.motion`, then the loader runs with real
  progress (fonts + critical images, 1.1 s floor, 2.6 s cap), then page init, then the
  `data-intro` timeline plays.
- **Navigation:** the leave animation runs while the next page loads, then cleanup reverts the
  old page, then the swap, a scroll reset, page init, the enter animation and the intro.
- **Reduced motion:** native scroll, no GL, no reveals (content visible), short fades for the
  loader and transitions.

## Pitfalls already handled (do not undo)

- CSS transforms on GSAP-animated elements stack with GSAP's: the curtain panel has none.
- Lenis reports progress 1 on pages that cannot scroll: `scroll.ts` normalizes it to 0.
- SplitText turns lines into blocks: `text-indent` is kept on the first line only.
- A revealed text stays revealed when SplitText re-splits after a font load or resize.
- Hidden-before-reveal is gated on `html.motion`, set before the first paint (no flash).
- The loader is hidden instead of removed, because React owns that node in Next.

## Code

Copy each file verbatim, then customize the parts marked as yours (loader look, transition,
eases). Keep the hooks and names: other references assume them.

### `src/engine/env.ts`

```ts
export const prefersReducedMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
export const isTouch = () => matchMedia('(hover: none), (pointer: coarse)').matches;
export const isMobile = () => matchMedia('(max-width: 767px)').matches;

// Shared easing vocabulary. Use these names everywhere; never invent per-component curves.
export const ease = {
  out: 'expo.out', // default entrance
  inOut: 'expo.inOut', // curtains, page transitions
  soft: 'power3.out', // small UI
  spring: 'back.out(1.6)', // playful pops, use rarely
} as const;
```

### `src/engine/scroll.ts`

```ts
// Smooth scroll on ONE clock: Lenis is driven by gsap.ticker, ScrollTrigger reads Lenis.
// Reduced motion → native scroll, no Lenis.
import Lenis from 'lenis';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { prefersReducedMotion } from './env';

gsap.registerPlugin(ScrollTrigger);

let lenis: Lenis | null = null;
const listeners = new Set<(s: ScrollState) => void>();

export type ScrollState = { y: number; velocity: number; progress: number };
const state: ScrollState = { y: 0, velocity: 0, progress: 0 };

export function initScroll() {
  if (lenis || prefersReducedMotion()) {
    // Still publish native scroll position for WebGL sync.
    if (!lenis) addEventListener('scroll', nativeTick, { passive: true });
    return;
  }
  lenis = new Lenis({ lerp: 0.1, wheelMultiplier: 1, touchMultiplier: 1.2, anchors: true });
  lenis.on('scroll', (l: Lenis) => {
    state.y = l.scroll;
    state.velocity = l.velocity;
    state.progress = l.limit > 0 ? l.scroll / l.limit : 0; // Lenis reports 1 on pages that cannot scroll
    ScrollTrigger.update();
    listeners.forEach((fn) => fn(state));
  });
  gsap.ticker.add((time) => lenis?.raf(time * 1000));
  gsap.ticker.lagSmoothing(0);
}

function nativeTick() {
  const max = document.documentElement.scrollHeight - innerHeight;
  state.velocity = scrollY - state.y;
  state.y = scrollY;
  state.progress = max > 0 ? scrollY / max : 0;
  listeners.forEach((fn) => fn(state));
}

export const onScroll = (fn: (s: ScrollState) => void) => {
  listeners.add(fn);
  return () => listeners.delete(fn);
};
export const scrollState = () => state;
export const stopScroll = () => lenis?.stop();
export const startScroll = () => lenis?.start();
export function resetScroll() {
  if (lenis) lenis.scrollTo(0, { immediate: true, force: true });
  else scrollTo(0, 0);
  state.y = 0;
  state.velocity = 0;
}
export function scrollToTarget(target: string | HTMLElement | number) {
  if (lenis) lenis.scrollTo(target, { duration: 1.4, easing: (t) => 1 - Math.pow(1 - t, 4) });
  else if (typeof target === 'number') scrollTo({ top: target });
  else (typeof target === 'string' ? document.querySelector(target) : target)?.scrollIntoView();
}
```

### `src/engine/reveal.ts`

```ts
// Declarative motion through data attributes. Authoring happens in markup:
//   data-split="lines|words|chars"   masked text reveal (SplitText), on scroll or on intro
//   data-reveal="up|fade|clip|scale"  block reveal
//   data-intro                        play with the page intro instead of on scroll
//   data-delay="0.2"                  extra delay (seconds)
//   data-parallax="0.15"              scrubbed vertical drift (fraction of element height)
// Every effect is skipped under reduced motion; CSS keeps content visible without JS.
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { SplitText } from 'gsap/SplitText';
import { ease, prefersReducedMotion } from './env';

gsap.registerPlugin(ScrollTrigger, SplitText);

const durations = { lines: 1.2, words: 1.1, chars: 0.9 } as const;
const staggers = { lines: 0.08, words: 0.035, chars: 0.018 } as const;

// autoSplit re-splits after font load / resize. A text that already revealed must stay revealed,
// so the state lives outside onSplit.
function splitTween(el: HTMLElement, isIntro: boolean) {
  const type = (el.dataset.split || 'lines') as keyof typeof durations;
  const delay = parseFloat(el.dataset.delay || '0');
  const s = { tween: undefined as gsap.core.Tween | undefined, done: false, requested: false };
  SplitText.create(el, {
    type: type === 'lines' ? 'lines' : `lines,${type}`,
    mask: 'lines',
    autoSplit: true,
    linesClass: 'split-line',
    onSplit(self) {
      gsap.set(el, { visibility: 'visible' });
      if (s.done) return;
      const targets = type === 'lines' ? self.lines : type === 'words' ? self.words : self.chars;
      s.tween = gsap.from(targets, {
        yPercent: 110,
        rotate: type === 'chars' ? 0 : 2,
        duration: durations[type],
        stagger: staggers[type],
        ease: ease.out,
        delay,
        paused: isIntro && !s.requested,
        onComplete: () => { s.done = true; },
        scrollTrigger: isIntro ? undefined : { trigger: el, start: 'top 88%', once: true },
      });
      return s.tween;
    },
  });
  return () => { s.requested = true; s.tween?.play(); };
}

function blockTween(el: HTMLElement, paused: boolean) {
  const kind = el.dataset.reveal || 'up';
  const delay = parseFloat(el.dataset.delay || '0');
  const from: gsap.TweenVars =
    kind === 'fade' ? { autoAlpha: 0 }
    : kind === 'clip' ? { clipPath: 'inset(100% 0% 0% 0%)', autoAlpha: 1 }
    : kind === 'scale' ? { scale: 1.15, clipPath: 'inset(12% 12% 12% 12%)', autoAlpha: 1 }
    : { y: 48, autoAlpha: 0 };
  const to: gsap.TweenVars = kind === 'clip' || kind === 'scale' ? { clipPath: 'inset(0% 0% 0% 0%)', scale: 1 } : {};
  gsap.set(el, { visibility: 'visible' });
  return gsap.fromTo(el, from, {
    ...to,
    y: 0,
    autoAlpha: 1,
    duration: kind === 'fade' ? 1 : 1.3,
    ease: ease.out,
    delay,
    paused,
    scrollTrigger: paused ? undefined : { trigger: el, start: 'top 90%', once: true },
  });
}

/** Wire every reveal inside `root`. Returns the intro timeline (paused) for the page entrance. */
export function initReveals(root: ParentNode = document) {
  const intro = gsap.timeline({ paused: true });
  if (prefersReducedMotion()) return intro;

  root.querySelectorAll<HTMLElement>('[data-split]').forEach((el) => {
    const isIntro = el.hasAttribute('data-intro');
    const play = splitTween(el, isIntro);
    if (isIntro) intro.add(play, 0);
  });
  root.querySelectorAll<HTMLElement>('[data-reveal]').forEach((el) => {
    const isIntro = el.hasAttribute('data-intro');
    const t = blockTween(el, isIntro);
    if (isIntro) intro.add(() => t.play(), 0);
  });
  root.querySelectorAll<HTMLElement>('[data-parallax]').forEach((el) => {
    const amount = parseFloat(el.dataset.parallax || '0.15');
    gsap.fromTo(el, { yPercent: -amount * 100 }, {
      yPercent: amount * 100,
      ease: 'none',
      scrollTrigger: { trigger: el.parentElement || el, start: 'top bottom', end: 'bottom top', scrub: true },
    });
  });
  return intro;
}
```

### `src/engine/loader.ts`

```ts
// First-load sequence. Progress follows REAL work (fonts + critical images), eased by GSAP,
// with a floor so it reads as intentional and a ceiling so it never becomes a usability problem.
// Markup (#loader) lives in the layout; its look is authored per project.
import { gsap } from 'gsap';
import { ease, prefersReducedMotion } from './env';

let format = (p: number) => String(Math.round(p)).padStart(3, '0');
/** Customize the counter text, e.g. a clock, a year, a frame count. p goes 0 → 100. */
export const setLoaderFormat = (fn: (p: number) => string) => { format = fn; };
let exit: ((root: HTMLElement) => gsap.core.Timeline) | null = null;
/** Replace the exit choreography (the loader → hero handoff). Return a timeline. */
export const setLoaderExit = (fn: (root: HTMLElement) => gsap.core.Timeline) => { exit = fn; };

const MIN = 1.1; // seconds: long enough to read as a designed moment
const MAX = 2.6; // seconds: a longer loader is a usability problem

function criticalAssets(): Promise<unknown>[] {
  const imgs = [...document.querySelectorAll<HTMLImageElement>('img[data-critical], [data-intro] img, [data-gl-instant] img')];
  return [document.fonts.ready, ...imgs.map((i) => (i.complete ? Promise.resolve() : i.decode().catch(() => {})))];
}

export async function runLoader(): Promise<void> {
  const root = document.getElementById('loader');
  if (!root) return;
  if (prefersReducedMotion()) {
    await Promise.race([Promise.all(criticalAssets()), wait(MAX)]);
    await gsap.to(root, { autoAlpha: 0, duration: 0.3 });
    return finish(root);
  }
  const count = root.querySelector<HTMLElement>('[data-loader-count]');
  const bar = root.querySelector<HTMLElement>('[data-loader-bar]');
  const tasks = criticalAssets();
  let done = 0;
  const shown = { v: 0 };
  const target = { v: 0 };
  tasks.forEach((t) => t.then(() => { done++; target.v = (done / tasks.length) * 100; }));
  const start = performance.now();

  await new Promise<void>((resolve) => {
    const tick = () => {
      const elapsed = (performance.now() - start) / 1000;
      const timeCap = Math.min(100, (elapsed / MIN) * 100); // never faster than MIN
      const goal = elapsed > MAX ? 100 : Math.min(target.v, timeCap);
      shown.v += (goal - shown.v) * 0.12;
      if (goal === 100 && shown.v > 99.5) shown.v = 100;
      if (count) count.textContent = format(shown.v);
      if (bar) bar.style.transform = `scaleX(${shown.v / 100})`;
      if (shown.v === 100) { gsap.ticker.remove(tick); resolve(); }
    };
    gsap.ticker.add(tick);
  });

  // Exit. Author per project with setLoaderExit(): it is the first handoff every visitor sees.
  if (exit) { await exit(root); return finish(root); }
  await gsap.timeline()
    .to(root.querySelectorAll('[data-loader-out]'), { yPercent: -110, duration: 0.7, ease: ease.inOut, stagger: 0.05 })
    .to(root, { clipPath: 'inset(0% 0% 100% 0%)', duration: 1, ease: ease.inOut }, '-=0.35');
  finish(root);
}

// Hide rather than remove: in React apps the loader node belongs to React.
function finish(root: HTMLElement) {
  root.hidden = true;
  document.documentElement.classList.add('is-loaded');
}

const wait = (s: number) => new Promise((r) => setTimeout(r, s * 1000));
```

### `src/engine/interactions.ts`

```ts
// Pointer craft. Fine pointers only; never hides the native cursor (accessibility, usability).
//   data-magnetic="0.35"   element leans toward the pointer
//   data-cursor="View"     follower grows and shows a label over this element
import { gsap } from 'gsap';
import { isTouch, prefersReducedMotion } from './env';

export function initMagnetic(root: ParentNode = document) {
  if (isTouch() || prefersReducedMotion()) return;
  root.querySelectorAll<HTMLElement>('[data-magnetic]').forEach((el) => {
    const strength = parseFloat(el.dataset.magnetic || '0.35');
    const x = gsap.quickTo(el, 'x', { duration: 0.6, ease: 'power3.out' });
    const y = gsap.quickTo(el, 'y', { duration: 0.6, ease: 'power3.out' });
    const move = (e: PointerEvent) => {
      const r = el.getBoundingClientRect();
      x((e.clientX - (r.left + r.width / 2)) * strength);
      y((e.clientY - (r.top + r.height / 2)) * strength);
    };
    const leave = () => { x(0); y(0); };
    el.addEventListener('pointermove', move);
    el.addEventListener('pointerleave', leave);
  });
}

let follower: HTMLElement | null = null;
export function initCursor() {
  if (follower || isTouch() || prefersReducedMotion()) return;
  follower = document.getElementById('cursor');
  if (!follower) return;
  const label = follower.querySelector<HTMLElement>('[data-cursor-label]');
  const x = gsap.quickTo(follower, 'x', { duration: 0.45, ease: 'power3.out' });
  const y = gsap.quickTo(follower, 'y', { duration: 0.45, ease: 'power3.out' });
  addEventListener('pointermove', (e) => {
    x(e.clientX); y(e.clientY);
    const target = (e.target as HTMLElement).closest<HTMLElement>('[data-cursor]');
    const text = target?.dataset.cursor || '';
    follower!.classList.toggle('is-active', !!text);
    if (label && label.textContent !== text) label.textContent = text;
  }, { passive: true });
  document.addEventListener('pointerleave', () => follower!.classList.remove('is-active'));
  follower.classList.add('is-ready');
}
```

### `src/engine/transition.ts`

```ts
// Page transitions. Adapters run leave() while the next page loads, so a transition adds
// little or no latency. Override the look with setTransition().
import { gsap } from 'gsap';
import { ease, prefersReducedMotion } from './env';

export type Transition = {
  leave: (curtain: HTMLElement) => Promise<unknown> | gsap.core.Animation;
  enter: (curtain: HTMLElement) => Promise<unknown> | gsap.core.Animation;
};

// Default: a solid panel wipes up over the page, then lifts off the new one.
let current: Transition = {
  leave: (c) => gsap.timeline()
    .set(c, { autoAlpha: 1 })
    .fromTo(c.querySelector('.curtain__panel'), { yPercent: 100 }, { yPercent: 0, duration: 0.8, ease: ease.inOut }),
  enter: (c) => gsap.timeline()
    .to(c.querySelector('.curtain__panel'), { yPercent: -100, duration: 0.9, ease: ease.inOut })
    .set(c, { autoAlpha: 0 }),
};

const reduced: Transition = {
  leave: (c) => gsap.timeline().set(c, { autoAlpha: 1 }).fromTo(c, { opacity: 0 }, { opacity: 1, duration: 0.2 }),
  enter: (c) => gsap.to(c, { autoAlpha: 0, duration: 0.2 }),
};

export const setTransition = (t: Transition) => { current = t; };
const pick = () => (prefersReducedMotion() ? reduced : current);
const curtain = () => document.getElementById('curtain') as HTMLElement;

export const playLeave = () => Promise.resolve(pick().leave(curtain()));
export const playEnter = () => Promise.resolve(pick().enter(curtain()));
```

### `src/engine/index.ts`

```ts
// Engine core: framework-agnostic page lifecycle. No DOM access at import time (SSR-safe).
// A framework adapter calls:
//   boot(setup)            once, on first load: setup → loader → page init → intro
//   leave() → cleanup()    before the route swaps (leave can run in parallel with the fetch)
//   enter()                after the new page is in the DOM: init → enter animation → intro
// Project code hooks in with onPage(fn): fn runs on every page load inside a gsap.context, so the
// tweens and ScrollTriggers it creates are reverted automatically. Return a cleanup for the rest.
// No WebGL? Delete the five lines marked `// GL`.
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { initScroll, resetScroll, startScroll, stopScroll } from './scroll';
import { initReveals } from './reveal';
import { initGL, mountGL, unmountGL } from './gl'; // GL
import { initCursor, initMagnetic } from './interactions';
import { runLoader } from './loader';
import { playEnter, playLeave } from './transition';
import { prefersReducedMotion } from './env';

export { onScroll, scrollState, scrollToTarget, stopScroll, startScroll } from './scroll';
export { setTransition } from './transition';
export { setLoaderFormat, setLoaderExit } from './loader';
export { hideGL, setBackground, clearBackground, glSupported } from './gl'; // GL
export { ease, isTouch, isMobile, prefersReducedMotion } from './env';

export type PageFn = (page: { intro: gsap.core.Timeline; path: string }) => void | (() => void);
const pageFns = new Set<PageFn>();
const cleanups: (() => void)[] = [];
let ctx: gsap.Context | null = null;
let intro: gsap.core.Timeline | null = null;
let ready = false;
let booted = false;

/** Run fn on every page load (and now, if a page is ready). Returns an unsubscribe. */
export function onPage(fn: PageFn) {
  pageFns.add(fn);
  if (ready) runPageFn(fn);
  return () => { pageFns.delete(fn); };
}

function runPageFn(fn: PageFn) {
  ctx?.add(() => {
    const c = fn({ intro: intro!, path: location.pathname });
    if (typeof c === 'function') cleanups.push(c);
  });
}

// Flags on <html>. Re-applied on every page because some routers swap root attributes.
export function syncFlags() {
  const h = document.documentElement.classList;
  h.add('js', 'is-booted');
  h.toggle('motion', !prefersReducedMotion());
  if (document.querySelector('.gl-canvas')) h.add('gl-on');
}

function initPage() {
  syncFlags();
  document.getElementById('cursor')?.classList.remove('is-active'); // stale label from the previous page
  ctx = gsap.context(() => {
    intro = initReveals(document);
    initMagnetic(document);
  });
  mountGL(document); // GL
  ready = true;
  pageFns.forEach(runPageFn);
  requestAnimationFrame(() => ScrollTrigger.refresh());
}

/** First load. `setup` runs once on the client after scroll/GL init and before the first page:
 *  register setTransition, setLoaderFormat, setLoaderExit, setBackground and driver modules there. */
export async function boot(setup?: () => void) {
  if (booted) return;
  booted = true;
  syncFlags();
  initScroll();
  initGL(); // GL
  initCursor();
  setup?.();
  stopScroll();
  initPage();
  await runLoader();
  startScroll();
  intro?.play();
}

/** Play the leave animation (resolve when the screen is covered). */
export async function leave() {
  stopScroll();
  await playLeave();
}

/** Tear down the current page: reverts every tween, ScrollTrigger and split; removes GL planes. */
export function cleanup() {
  if (!ready) return;
  ready = false;
  cleanups.splice(0).forEach((c) => c());
  ctx?.revert();
  ctx = null;
  unmountGL(); // GL
}

/** Init the new page. `transition: false` for back/forward, where no leave ran. */
export async function enter({ transition = true, scrollTop = true } = {}) {
  if (!booted) return;
  cleanup(); // no-op if the adapter already cleaned up
  if (scrollTop) resetScroll();
  initPage();
  if (transition) await playEnter();
  startScroll();
  intro?.play();
}
```

## CSS

### Tokens (`tokens.css`)

```css
/* DESIGN TOKENS: rewrite every value per project from the art-direction plan. The NAMES are the
   contract the engine CSS uses; the neutral values only exist so the engine renders. */


:root {
  /* Color: name by role, not by hue. */
  --c-bg: #f2f2f2;
  --c-fg: #101010;
  --c-muted: #6b6b6b;
  --c-line: rgb(16 16 16 / 0.14);
  --c-accent: #101010;
  --c-curtain: var(--c-fg);

  /* Type families */
  --f-display: 'Display', system-ui, sans-serif; /* Next: var(--font-display) from next/font */
  --f-body: system-ui, sans-serif;

  /* Fluid type scale (min @ 375px → max @ 1440px) */
  --t-mega: clamp(4rem, 1.2rem + 14vw, 16rem);
  --t-xl: clamp(2.5rem, 1.4rem + 4.8vw, 6rem);
  --t-l: clamp(1.75rem, 1.3rem + 1.9vw, 3rem);
  --t-m: clamp(1.25rem, 1.1rem + 0.6vw, 1.625rem);
  --t-body: clamp(1rem, 0.95rem + 0.2vw, 1.125rem);
  --t-s: 0.875rem;
  --t-xs: 0.75rem;

  /* Space: one fluid unit, multiplied. Vary section rhythm deliberately. */
  --u: clamp(0.5rem, 0.35rem + 0.6vw, 1rem);
  --gutter: clamp(1rem, 0.6rem + 1.6vw, 2.5rem);
  --cols: 12;

  /* Shape: one radius rule for the whole site. */
  --radius: 0px;

  /* Layers */
  --z-gl: 0;
  --z-content: 1;
  --z-header: 50;
  --z-cursor: 80;
  --z-curtain: 90;
  --z-loader: 100;
}
```

### Engine foundation (`engine.css`)

```css
/* ENGINE + FOUNDATION. The project look lives in tokens and component styles; edit this file
   only to change engine behavior. */

*, *::before, *::after { box-sizing: border-box; }
* { margin: 0; }
html {
  -webkit-text-size-adjust: none;
  text-size-adjust: none;
  background: var(--c-bg);
  color: var(--c-fg);
}
body {
  min-height: 100dvh;
  font-family: var(--f-body);
  font-size: var(--t-body);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
  font-kerning: normal;
  overflow-x: clip;
}
img, picture, video, canvas, svg { display: block; max-width: 100%; }
img { height: auto; }
input, button, textarea, select { font: inherit; color: inherit; }
button { background: none; border: 0; cursor: pointer; }
a { color: inherit; text-decoration: none; }
h1, h2, h3, h4 { font-weight: inherit; font-size: inherit; text-wrap: balance; }
p { text-wrap: pretty; }
::selection { background: var(--c-fg); color: var(--c-bg); }

/* Accessibility */
:focus-visible { outline: 2px solid var(--c-accent); outline-offset: 3px; border-radius: 2px; }
#main:focus { outline: none; }
.skip-link {
  position: fixed; left: var(--gutter); top: var(--gutter); z-index: calc(var(--z-loader) + 1);
  padding: 0.6em 1em; background: var(--c-fg); color: var(--c-bg);
  transform: translateY(-200%);
}
.skip-link:focus-visible { transform: none; }
.sr-only {
  position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0;
}

/* Lenis */
html.lenis, html.lenis body { height: auto; }
.lenis:not(.lenis-autoToggle).lenis-stopped { overflow: clip; }
.lenis [data-lenis-prevent] { overscroll-behavior: contain; }
.lenis.lenis-smooth iframe { pointer-events: none; }

/* Stacking: canvas under content so text can sit over GL images */
#gl { position: fixed; inset: 0; z-index: var(--z-gl); pointer-events: none; }
.gl-canvas { position: absolute; inset: 0; width: 100%; height: 100%; }
#main, [data-layer='content'] { position: relative; z-index: var(--z-content); }
/* GL replaces the pixels of [data-gl] media; the <img> stays for SEO, a11y and fallback. */
.gl-on [data-gl] img, .gl-on [data-gl] .gl-fallback { opacity: 0; }
/* The canvas sits UNDER the content: any background on a GL element would hide its plane. */
.gl-on [data-gl] { background: none !important; }
[data-gl='procedural'] .gl-fallback {
  position: absolute; inset: 0;
  background: radial-gradient(120% 90% at 30% 20%, var(--c-muted), var(--c-fg));
}
[data-gl] { position: relative; }

/* Hidden-until-revealed (only when motion is allowed and JS runs) */
.motion [data-split], .motion [data-reveal] { visibility: hidden; }
.split-line { padding-bottom: 0.08em; margin-bottom: -0.08em; } /* descender room inside masks */
/* SplitText turns each line into a block: keep text-indent on the first line only. */
[data-split] > * , [data-split] > * > * { text-indent: 0; }
[data-split] > :first-child, [data-split] > :first-child > :first-child { text-indent: inherit; }

/* Curtain (page transitions) */
#curtain { position: fixed; inset: 0; z-index: var(--z-curtain); pointer-events: none; visibility: hidden; overflow: hidden; }
/* No CSS transform here: GSAP owns it (CSS translate + yPercent would stack). #curtain visibility hides it. */
.curtain__panel { position: absolute; inset: 0; background: var(--c-curtain); }

/* Cursor follower: decorative, never replaces the native cursor */
#cursor {
  position: fixed; left: 0; top: 0; z-index: var(--z-cursor); pointer-events: none;
  display: grid; place-items: center; width: 0; height: 0; opacity: 0;
}
#cursor.is-ready { opacity: 1; }
#cursor span {
  display: grid; place-items: center; min-width: 5.5rem; aspect-ratio: 1; border-radius: 50%;
  background: var(--c-fg); color: var(--c-bg); font-size: var(--t-xs); letter-spacing: 0.02em;
  transform: translate(-50%, -50%) scale(0); transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
#cursor.is-active span { transform: translate(-50%, -50%) scale(1); }
@media (hover: none), (pointer: coarse) { #cursor { display: none; } }

/* Loader skeleton: restyle in the project, keep it covering the first paint */
#loader {
  position: fixed; inset: 0; z-index: var(--z-loader);
  display: grid; align-content: end; padding: var(--gutter);
  background: var(--c-fg); color: var(--c-bg);
  clip-path: inset(0% 0% 0% 0%);
}
.loader__inner { display: flex; justify-content: space-between; align-items: end; overflow: hidden; }
.loader__count { font-variant-numeric: tabular-nums; }
.loader__bar { height: 1px; margin-top: calc(var(--u) * 1.5); background: currentColor; transform: scaleX(0); transform-origin: left; }
html:not(.js) #loader, #loader[hidden] { display: none; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; scroll-behavior: auto !important; }
}
```
