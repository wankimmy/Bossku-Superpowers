# Motion stack for award-level sites: what ships, and how to use it well

Last updated: 2026-09-24

Scope: the JavaScript and CSS motion layer of Awwwards Site-of-the-Day (SOTD) work in 2026. That covers smooth scroll, scroll-linked and scroll-triggered animation, text splitting, page transitions, cursor and hover micro-interactions, and preloaders. WebGL/3D gets only a brief mention here. Every version and support claim below was checked on 2026-09-24 against the npm registry, the GitHub API, vendor docs, MDN browser-compat-data, caniuse data and webstatus.dev. **Documented** means a vendor or spec says it. **Observed** means it turned up in shipped code on live SOTD sites (probe method in §1.3). Anything I could not confirm is marked (unverified).

House rule: the anti-slop design law (`deslop-law.md`) overrides award-site habits. The law's single most important motion rule is **content is visible by default**. If JavaScript never runs or an animation never fires, the page still shows everything. Every recipe here is built to that contract, and §7 maps common award-site habits to crafted alternatives.

---

## 0. Decisions (read this first)

| Need | Use | Why |
|---|---|---|
| Timeline and scroll choreography | GSAP 3.15 core + ScrollTrigger + SplitText + CustomEase (+ Flip, Observer, Draggable as needed) | 100% free including former Club plugins since 3.13 (2025-04-30). Observed on 72% of probed SOTD sites. |
| Smooth wheel scroll | Lenis 1.3.26 driven by `gsap.ticker` (`autoRaf: false`) | Uses native scroll, so `position: sticky`, find-in-page and the scrollbar keep working. Honors reduced motion by default since 1.3.26. Observed on 73% of probed sites. |
| Decorative scroll-linked effects with no JS (parallax, image un-clip, progress) | CSS `animation-timeline: view()/scroll()` inside `@supports` | Chrome/Edge 115+ and Safari 26+. Firefox stable has no support, so the page stays static there and the 0% keyframe must be a readable state. |
| Page transitions, multi-page site | CSS `@view-transition { navigation: auto; }` | Chrome 126+ and Safari 18.2+. Firefox navigates normally. No JS needed. |
| Page transitions where WebGL, audio or scroll state must persist | PJAX: Taxi 1.9.1 or Swup 4.10 (`native: true`), with same-document `startViewTransition` and a GSAP fallback | Same-document View Transitions are Baseline (Firefox 144+), so a PJAX router gets them in all three engines. |
| React app-like UI | Motion 13 (`motion/react`) for layout, presence and gestures; GSAP with `useGSAP` for scroll scenes | Motion's `scroll()` uses ScrollTimeline where available. |
| Avoid for new builds | Barba.js (no npm release since 2024-08-12), Theatre.js as a runtime dependency (public repo dormant since 2024-08), ScrollSmoother combined with Lenis (two smoothers), `ScrollTrigger.normalizeScroll()` on content sites | See §1 |

---

## 1. Verified versions, licensing, support

### 1.1 Libraries (npm registry and GitHub API, fetched 2026-09-24)

| Library | Current | Date | License / cost | Maintenance signal | Observed on SOTD (n=117) |
|---|---|---|---|---|---|
| [gsap](https://registry.npmjs.org/gsap) | **3.15.0** | 2026-04-13 | GSAP Standard "no charge" license (Webflow). Commercial use free. **Prohibited:** use in no-code visual animation builders that compete with Webflow ([license](https://gsap.com/community/standard-license/), effective 2025-04-30, last modified 2025-05-30) | Previous releases: 3.14.0/3.14.1 on 2025-12-08, 3.14.2 on 2025-12-12, 3.13.0 on 2025-04-30 | 84 (72%) ship ScrollTrigger |
| [@gsap/react](https://registry.npmjs.org/@gsap/react) | 2.1.2 | 2025-01-15 | same as GSAP | stable, `useGSAP()` | n/a |
| [lenis](https://registry.npmjs.org/lenis) | **1.3.26** (`dev` tag 2.0.0-dev.5, 2026-09-18) | 2026-08-05 | MIT | active, repo pushed 2026-09-22 | 85 (73%) |
| [motion](https://registry.npmjs.org/motion) (formerly Framer Motion; `framer-motion` publishes in lockstep) | **13.4.3** (13.4.4 is in the [changelog](https://github.com/motiondivision/motion/blob/main/CHANGELOG.md) dated 2026-09-24 but was not on npm at check time) | 2026-09-24 | MIT. Motion+ is paid: one-time personal licence or annual per-seat business plan ([motion.dev/plus](https://motion.dev/plus); price unverified) | very active | ~13 (11%, heuristic) |
| [swup](https://registry.npmjs.org/swup) | **4.10.0** | 2026-09-03 | MIT | active, repo pushed 2026-09-24 | 11 (9%) |
| [@unseenco/taxi](https://registry.npmjs.org/@unseenco/taxi) | **1.9.1** | 2025-11-01 | BSD-3-Clause | low cadence; last push 2025-11-01 ([craftedbygc/taxi](https://github.com/craftedbygc/taxi)) | 8 (7%) |
| [@barba/core](https://registry.npmjs.org/@barba/core) | **2.10.3** | 2024-08-12 | MIT | dormant: repo last pushed 2024-12-02 ([barbajs/barba](https://github.com/barbajs/barba)) | 17 (15%): legacy-heavy |
| [@theatre/core](https://registry.npmjs.org/@theatre/core) / studio | **0.7.2** | 2024-05-19 | core Apache-2.0, **studio AGPL-3.0-only** | public repo last pushed 2024-08-14. README says 1.0 development moved to a private repo ([theatre-js/theatre](https://github.com/theatre-js/theatre)). A community fork, "Encore", says Theatre.js is unmaintained ([ikanishakm/encore](https://github.com/ikanishakm/encore); fork health unverified) | 2 (2%) |
| [locomotive-scroll](https://registry.npmjs.org/locomotive-scroll) | 5.0.1 | 2026-01-15 | MIT | v5 is "built on top of Lenis" and pins `lenis@1.3.17` ([README](https://unpkg.com/locomotive-scroll@5.0.1/README.md)) | 5 (4%) |

GSAP facts that matter when building:

- **Free since 3.13.0 (2025-04-30):** all former Club plugins (SplitText, MorphSVG, ScrollSmoother, DrawSVG, ScrambleText, Inertia, etc.) are in the public npm package. No private registry or tokens are needed ([3.13 blog](https://gsap.com/blog/3-13/), [release commit](https://github.com/greensock/GSAP/commit/9f8eca1cc21cab9fc41fa1a3edb984d7ef02fd89), [Webflow announcement](https://webflow.com/blog/gsap-becomes-free)).
- **3.15.0 (2026-04-13)** adds `easeReverse`, a separate ease used when a tween or timeline plays backwards. It is recalculated from wherever the playhead turned, and it deprecates `yoyoEase` ([3.15 blog](https://gsap.com/blog/3-15/)). Use it for toggles: menus, drawers, modals.
- **3.14 (2025-12-08):** MorphSVG `smooth` and `curveMode` ([3.14 blog](https://gsap.com/blog/3-14/)).
- **SplitText was rewritten in 3.13** ([docs](https://gsap.com/docs/v3/Plugins/SplitText/)):
  - `mask: "lines" | "words" | "chars"` wraps each piece in an `overflow: clip` element. The mask class is `<class>-mask`.
  - `autoSplit: true` re-splits when fonts load or width changes. Create animations inside `onSplit()` and return them, so SplitText reverts them and time-syncs the replacement.
  - `aria: "auto"` (default) puts `aria-label` on the split element and `aria-hidden` on the pieces. `"hidden"` and `"none"` are the alternatives.
  - Other options: `deepSlice`, `propIndex` (CSS vars such as `--line: 1`), `ignore`, `prepareText`, `smartWrap`, `revert()`. SplitText also runs standalone without the core.
  - Docs warn: avoid `text-wrap: balance` on split text, and split only what you animate.
- **Observer ships inside ScrollTrigger.** `ScrollTrigger.min.js` 3.15.0 contains `function Observer(...)`, verified in the [dist file](https://unpkg.com/gsap@3.15.0/dist/ScrollTrigger.min.js). The same file contains the string "Requires GSAP 3.11.0 or later", so naive bundle greps report a false "GSAP 3.11.0".
- **ScrollSmoother** smooths with a `matrix3d` transform on `#smooth-content`. Defaults: `smooth` 0.8s, ease `"expo"`, no smoothing on touch-only devices. `position: fixed` elements must live **outside** the wrapper ([docs](https://gsap.com/docs/v3/Plugins/ScrollSmoother/)).
- **Official agent skills:** [greensock/gsap-skills](https://github.com/greensock/gsap-skills), created 2026-03-04, last push 2026-07-29.

Lenis facts ([README on main](https://github.com/darkroomengineering/lenis), [v1.3.26 release](https://github.com/darkroomengineering/lenis/releases/tag/v1.3.26), [1.3.26 dist source](https://unpkg.com/lenis@1.3.26/dist/lenis.mjs)):

- **Options that matter:**
  - `lerp` (default `0.1`, frame-rate-independent damping via `damp()`)
  - `duration` and `easing`. There is **no default duration** in the 1.3.26 constructor. If you pass `duration`, the duration/easing path runs *instead of* lerp: the code checks `duration && easing` first, which contradicts the README's "duration useless if lerp defined". Pass one or the other, never both.
  - `smoothWheel` (true), `syncTouch` (false; "can be unstable on iOS<16"), `autoRaf` (false), `anchors`, `allowNestedScroll`, `prevent`, `autoToggle` (needs `transition-behavior`), `stopInertiaOnNavigate`, `wheelMultiplier` / `touchMultiplier` (1)
- **`respectReducedMotion` (default `true`) is new in 1.3.26.** Under `prefers-reduced-motion: reduce`, lerp is forced to 1 and programmatic scrolls jump instantly. The 1.3.25 dist does not contain the option. **Only 5 of 77 probed SOTD sites with a detectable Lenis version run 1.3.26**, so most award sites smooth-scroll regardless of the OS setting.
- Lenis writes scroll with `scrollTo({ behavior: "instant" })` (1.3.26 source), so CSS `scroll-behavior` does not double-smooth its frames.
- Documented limitations:
  - no CSS scroll-snap (use `lenis/snap`)
  - capped at 60fps on Safari and 30fps in Low Power Mode
  - smoothing stops over iframes
  - "position fixed seems to lag on MacOS Safari pre-M1"
  - nested scrollers need `data-lenis-prevent*` or `allowNestedScroll`
- Recommended CSS ([lenis.css](https://unpkg.com/lenis@1.3.26/dist/lenis.css)): `html.lenis, html.lenis body { height: auto }`, `.lenis-stopped { overflow: clip }`, `overscroll-behavior: contain` on prevented nodes, `pointer-events: none` on iframes while smoothing.

Motion (motion.dev) current API surface:

- **Vanilla (`import { … } from "motion"`):** `animate`, `scroll` ([docs](https://motion.dev/docs/scroll): runs on `ScrollTimeline` "where possible" for hardware acceleration; options `container`, `target`, `axis`, `offset`), `inView` ([docs](https://motion.dev/docs/inview): `amount` "some"/"all"/0–1), `hover` (filters emulated touch hovers, [docs](https://motion.dev/docs/hover)), `press`, `stagger`, `spring`, `animateView` (View Transitions with springs and interruption; moved into the main library in 12.41.0, [docs](https://motion.dev/docs/animate-view)).
- **React (`motion/react`):** `motion.*`, `AnimatePresence`, `useScroll`, `useTransform`, `useReducedMotion`, `<MotionConfig reducedMotion="user">` (disables transform and layout animation, keeps opacity and colour; [docs](https://motion.dev/docs/react-accessibility)), and `AnimateView` for React 19.3 `ViewTransition` (13.4.0).
- 13.0.0 (2026-08-05) removed the optional `@emotion/is-prop-valid` dependency. 13.2.0 added `motion/three` and `motion/vgpu` effects ([changelog](https://github.com/motiondivision/motion/blob/main/CHANGELOG.md)).
- **Trap:** the `initial` state is rendered into server HTML ([docs](https://motion.dev/docs/vue-motion-component): "the initial state of the component will be reflected in the server-generated output"). `initial={{ opacity: 0 }}` therefore ships invisible content until hydration.

Page-transition libraries:

- Taxi: `new Core({ transitions: { default: T } })`. A `Transition` has `onLeave({ from, trigger, done })` and `onEnter({ to, trigger, done })`. Markup is `data-taxi` > single child `data-taxi-view`. Prefetches on hover and focus by default. Events are `NAVIGATE_OUT`, `NAVIGATE_IN`, `NAVIGATE_END` ([docs](https://taxi.js.org/transitions/), [Core.js 1.9.1](https://unpkg.com/@unseenco/taxi@1.9.1/src/Core.js)). It replaced the unmaintained Highway.js.
- Swup: `new Swup({ native: true })` uses the View Transitions API and adds `html.swup-native` when supported. Target `:not(.swup-native)` for a CSS fallback ([options](https://swup.js.org/options/), [animations](https://swup.js.org/getting-started/animations/)). 4.10.0 skips the history animation when the browser already ran a native visual transition ([changelog](https://github.com/swup/swup/blob/main/CHANGELOG.md)).
- Barba: `barba.init({ transitions: [{ leave(data), enter(data) }] })` with `data.current.container` and `data.next.container`, plus `sync: true` and `barba.hooks.*` ([docs](https://barba.js.org/docs/advanced/transitions)). Keep it only for existing codebases.

### 1.2 Browser support (current stable on 2026-09-24: Chrome 154 [2026-09-22, now on a 2-week cadence per [Chromium Dash](https://chromiumdash.appspot.com/fetch_milestone_schedule?mstone=154)], Firefox 156, Safari 27, per [caniuse agent data](https://github.com/Fyrd/caniuse) updated 2026-09-23)

| Feature | Chrome/Edge | Safari | Firefox (stable) | Status | Source |
|---|---|---|---|---|---|
| Scroll-driven animations (`animation-timeline: scroll()/view()`, `animation-range`, `view-timeline`) | 115 | 26 (2025-09-15) | **no**: Nightly/preview only | **Limited availability** (not Baseline) | [webstatus](https://webstatus.dev/features/scroll-driven-animations), [BCD animation-timeline](https://github.com/mdn/browser-compat-data/blob/main/css/properties/animation-timeline.json), [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline) |
| `timeline-scope` | 116 (`all` removed in 138) | 26 | preview | Limited | BCD |
| Same-document View Transitions (`document.startViewTransition`) | 111 | 18 | **144** | **Baseline newly available 2025-10-14** | [webstatus](https://webstatus.dev/features/view-transitions), [caniuse](https://caniuse.com/view-transitions) |
| `startViewTransition({ update, types })` / `ViewTransition.types` | 125 | 18.2 | 147 | shipped in all three | [BCD ViewTransition](https://github.com/mdn/browser-compat-data/blob/main/api/ViewTransition.json) |
| `view-transition-class` | 125 | 18.2 | 144 | Baseline newly 2025-10-14 | [webstatus](https://webstatus.dev/features/view-transition-class) |
| `:active-view-transition` | 125 | 18.2 | 147 | Baseline newly 2026-01-13 | [webstatus](https://webstatus.dev/features/active-view-transition) |
| `view-transition-name: match-element` | 137 | 18.4 | 144 | shipped in all three | [BCD](https://github.com/mdn/browser-compat-data/blob/main/css/properties/view-transition-name.json) |
| Cross-document View Transitions (`@view-transition { navigation: auto }`, `pageswap`/`pagereveal`, `CSSViewTransitionRule`) | 126 | 18.2 | **no** (level 1 only) | **Limited availability** | [webstatus](https://webstatus.dev/features/cross-document-view-transitions), [caniuse](https://caniuse.com/cross-document-view-transitions), [BCD @view-transition](https://github.com/mdn/browser-compat-data/blob/main/css/at-rules/view-transition.json) |
| `<link rel="expect" blocking="render">` | 124 | 18.2 | no | Limited | [webstatus](https://webstatus.dev/features/link-rel-expect) |
| Element-scoped view transitions (`element.startViewTransition`) | 147 | no | no | Limited | [webstatus](https://webstatus.dev/features/view-transitions-element-scoped) |
| CSS `linear()` easing (spring curves in CSS) | 113 | 17.2 | 112 | **Baseline widely available** (2026-06-11) | [webstatus](https://webstatus.dev/features/linear-easing) |
| `scrollend` event | 114 | 26.2 | 109 | Baseline newly 2025-12-12 | [webstatus](https://webstatus.dev/features/scrollend) |
| `transition-behavior: allow-discrete` (Lenis `autoToggle`) | 117 | 17.4 | 129 | Baseline newly 2024-08-06 | [webstatus](https://webstatus.dev/features/transition-behavior) |
| `overflow: clip` (SplitText masks) | 90 | 16 | 81 | Baseline widely | [webstatus](https://webstatus.dev/features/overflow-clip) |

Feature tests:

- Cross-document View Transitions: `'CSSViewTransitionRule' in window` (Chrome 126, Safari 18.2, not Firefox; [BCD](https://github.com/mdn/browser-compat-data/blob/main/api/CSSViewTransitionRule.json)).
- Same-document: `typeof document.startViewTransition === 'function'`.
- Scroll timelines: `CSS.supports('animation-timeline: view()')`.

View Transitions rules that bite ([Chrome docs](https://developer.chrome.com/docs/web-platform/view-transitions/cross-document), [MDN view-transition-name](https://developer.mozilla.org/en-US/docs/Web/CSS/view-transition-name)):

- Cross-document transitions are same-origin only, with no cross-origin redirects in the chain.
- `navigation: auto` covers traverse and push/replace navigations that were not started from browser UI. Address-bar navigation and reloads are excluded.
- Chrome skips the transition with a `TimeoutError` if the navigation takes more than 4 seconds.
- A `pagereveal` listener must be registered in a classic, parser-blocking `<head>` script.
- Duplicate `view-transition-name` values rendered at the same time reject `ready` and **skip the whole transition**. Use `match-element` or assign names at runtime.

### 1.3 What SOTD sites actually ship (observed, static probe)

Method: I took the 120 most recent SOTDs from the skill corpus (`data/corpus.jsonl`), dated 2026-05-29 to 2026-09-25; 117 fetched. For each I pulled landing HTML plus up to 30 linked JS/CSS assets and grepped for library signatures. Code-split chunks loaded later are missed, so **every count is a lower bound**. The probe scripts and raw JSONL are in `evidence/motion/` (`motion_probe.py`, `ease_census.py`, `ease_context.py`, `probe_sotd120.jsonl`, `ease_census120.json`, `ease_context120.json`).

| Signal | Sites (of 117) |
|---|---|
| GSAP ScrollTrigger | 84 (72%) |
| Lenis | 85 (73%) |
| Lenis **and** GSAP together | 66 (56%) |
| SplitText | 54 (46%) |
| CustomEase | 40 (34%) |
| Flip / Draggable / ScrambleText / DrawSVG / MorphSVG | 20 / 13 / 9 / 9 / 8 |
| ScrollSmoother (strict heuristic) | ~8 (7%) |
| Any PJAX router (Barba 17, Swup 11, Taxi 8; overlapping) | 36 (31%) |
| `view-transition-name` in shipped CSS/JS | 19 (16%) |
| `animation-timeline` / `view-timeline` / `ScrollTimeline(` | 14 (12%), e.g. [Seasats](https://www.awwwards.com/sites/seasats), [PP Neue Montreal](https://www.awwwards.com/sites/pp-neue-montreal), [Podium](https://www.awwwards.com/sites/podium) |
| `@view-transition` (cross-doc opt-in) in landing CSS | 0 (lower bound) |
| `startViewTransition` string | 52 (44%), but 51 of 52 also ship a framework, router or Webflow, so this is mostly framework code, not authored transitions |
| `prefers-reduced-motion` string present | 77 (66%), presence only, not proof it is honored |
| Three.js | 52 (44%) |
| Lottie | 23 (20%) |
| Webflow | 29 (25%); 25 of those load GSAP (Webflow now hosts GSAP and its plugins as a site-settings toggle) |

GSAP version in the wild (80 sites with a detectable core version): 3.15.0 ×35, 3.14.x ×24, 3.13.0 ×14, 3.12.x ×7. **91% run 3.13 or later**, the free-plugin era.

Across all recent awarded elements in the corpus (575 sites, 2024 onward; 3,257 featured "elements"), motion-bearing element titles and tags break down as: scroll 414, transition 233, hover 134, loader/preloader 129, reveal 66, parallax 69, cursor 25, horizontal 23, marquee/ticker 20, stacking 9, magnetic 1. Juries feature **scroll storytelling, page transitions and loaders** far more than cursor gimmicks.

---

## 2. Easing tokens, durations, staggers

### 2.1 What award sites use (observed, n=117 SOTD bundles, per-site presence, library-internal literals discounted)

- **GSAP ease literals, most common:** `power2.out` 65, `none` 61 (scrubs and loops), `power2.inOut` 51, `power3.out` 43, `power2.in` 39, `power1.inOut` 29, `expo.out` 29, `power3.inOut` 28, `power1.out` 25, `power4.out` 22, `expo.inOut` 21, `power4.inOut` 20, `sine.inOut` 17. By family across sites: out 227, inOut 174, in 86.
- **What each ease drives** (co-occurring keys in the same tween object):
  - `yPercent` (masked text): `power2.out`, `power3.out`, `expo.out`, `power4.out`
  - `clipPath`: `power2.out`, `power4.inOut`, `expo.inOut`, `expo.out`
  - `stagger`: `power2.out` > `power3.out` > `expo.out` > `power4.out`
  - `scale`: `power2.out`, `expo.out`, `back.out` (the bouncy tail)
- **Durations by ease (seconds, most frequent first):**
  - `power2.out`: .5, .3, .4, .6, 1
  - `power3.out`: .5, 1, .3, .6, .9
  - `expo.out`: 1, .4, .8, 1.2, 2
  - `power2.in`: .3, .4, .25
  - `power2.inOut`: 1, .5, .4, .3, .6
  - `power3.inOut`: 1, .65, .6, .75, 1.2–1.5
- **Stagger literals:** .1 (25 sites), .05 (25), .08 (16), .04 (15), .02 (12), .15 (11), .2 (11), .025 (10), .03 (10).
- **Authored CSS curves**, excluding bundled easing tables and Tailwind defaults (`.4,0,.2,1` etc.):
  - `.19,1,.22,1` (classic expo out) 17
  - `.16,1,.3,1` (easings.net expo out) 15
  - `.23,1,.32,1` (classic quint out) 14
  - `.215,.61,.355,1` (classic cubic out) 12
  - `.22,1,.36,1` (easings.net quint out) 8
  - `.645,.045,.355,1` (classic cubic inOut) 8
  - `.34,1.56,.64,1` (back out) 7
  - `.55,0,.1,1` 5
  - `.65,.05,.36,1` 4
  - `.625,.05,0,1` 3: the named CustomEase `"osmo"`, a studio curve that spread through Webflow resources
- Two cubic-bezier sets circulate:
  - "Classic" Penner/Ceaser values, e.g. expo out `.19,1,.22,1`, quint out `.23,1,.32,1`, quart inOut `.77,0,.175,1` ([postcss-easings v2](https://unpkg.com/postcss-easings@2.0.0/index.js))
  - Newer easings.net values, e.g. expo out `.16,1,.3,1`, quint out `.22,1,.36,1`, quart inOut `.76,0,.24,1` ([easings.net](https://easings.net/), [postcss-easings v4](https://unpkg.com/postcss-easings/index.js))
  - Both are approximations. Pick one set per project.

### 2.2 Token catalog (the one to build with)

GSAP name mapping is documented in the [Ease Visualizer](https://gsap.com/docs/v3/Eases/): quad = power1, cubic = power2, quart = power3, quint/strong = power4. GSAP's default ease is `power1.out`; its default duration is 0.5s (the `duration:.5` default in the 3.15 core). GSAP power eases are exact polynomials, so a CSS `cubic-bezier` only approximates them. **For exact CSS/JS parity, register the bezier with CustomEase and use the same curve in both** (`CustomEase.create(id, ".16,1,.3,1")` is documented, [CustomEase](https://gsap.com/docs/v3/Eases/CustomEase/)).

| Token | cubic-bezier | GSAP equivalent | Role on award sites | Duration band |
|---|---|---|---|---|
| `--ease-out-soft` | `.33, 1, .68, 1` | `power2.out` | Micro: hover colour/fill, small y shifts, icon slide, tooltip in. The single most common ease on SOTDs. | 0.18–0.5s |
| `--ease-out` | `.25, 1, .5, 1` | `power3.out` | Default entrance: cards, meta rows, words | 0.5–0.9s |
| `--ease-out-strong` | `.22, 1, .36, 1` | `power4.out` | Large travel: masked line reveals, hero title, full-width panels | 0.8–1.2s |
| `--ease-out-expo` | `.16, 1, .3, 1` | `expo.out` | Signature reveals: line masks, image un-clip plus scale-settle, counters landing. Fast start, long settle; reads as "award". | 0.9–1.4s |
| `--ease-in` | `.32, 0, .67, 0` | `power2.in` | Exits only: leaving page content, closing overlays. Never for entrances. | 0.25–0.4s |
| `--ease-in-out` | `.76, 0, .24, 1` | `power3.inOut` | A→B on-screen travel: page curtains, clip-path wipes, menu panels, Flip layout moves | 0.6–1.0s |
| `--ease-in-out-expo` | `.87, 0, .13, 1` | `expo.inOut` | Dramatic curtains or full-screen takeovers. At most one per site. | 0.9–1.4s |
| `--ease-drift` | `.37, 0, .63, 1` | `sine.inOut` | Ambient loops: float, bob, breathing gradients (with yoyo) | 3–8s per leg |
| `linear` | `linear` | `"none"` | Anything scrubbed by scroll, marquees, `containerAnimation` (required), progress bars that mirror real progress | scroll-mapped |
| (avoid on UI) | `.34, 1.56, .64, 1` | `back.out(1.7)` | Observed on scale/rotate pops. **Slop tell on buttons and text** (law: "never bouncy"). Allowed only on an illustrative object, once. | — |

```css
:root {
  --ease-out-soft: cubic-bezier(.33, 1, .68, 1);
  --ease-out: cubic-bezier(.25, 1, .5, 1);
  --ease-out-strong: cubic-bezier(.22, 1, .36, 1);
  --ease-out-expo: cubic-bezier(.16, 1, .3, 1);
  --ease-in: cubic-bezier(.32, 0, .67, 0);
  --ease-in-out: cubic-bezier(.76, 0, .24, 1);
  --ease-in-out-expo: cubic-bezier(.87, 0, .13, 1);
  --ease-drift: cubic-bezier(.37, 0, .63, 1);

  --dur-press: 120ms;   /* :active feedback */
  --dur-micro: 200ms;   /* hover colour/fill, focus ring */
  --dur-short: 350ms;   /* exits, small UI enter */
  --dur-base: 600ms;    /* menus, overlays, cards */
  --dur-reveal: 1000ms; /* line or media reveal */
  --dur-hero: 1400ms;   /* hero intro or curtain, total */
}
```

```js
// motion-tokens.js: one source of truth, identical curves in CSS and GSAP
import { gsap } from 'gsap';
import { CustomEase } from 'gsap/CustomEase';
gsap.registerPlugin(CustomEase);

export const EASE = {
  outSoft: '.33,1,.68,1', out: '.25,1,.5,1', outStrong: '.22,1,.36,1', outExpo: '.16,1,.3,1',
  in: '.32,0,.67,0', inOut: '.76,0,.24,1', inOutExpo: '.87,0,.13,1', drift: '.37,0,.63,1',
};
// ids: no dots (GSAP parses "name.out" itself) and a prefix so they can't shadow built-in/legacy ease names
for (const [k, v] of Object.entries(EASE)) CustomEase.create('motion' + k[0].toUpperCase() + k.slice(1), v);
gsap.defaults({ ease: 'motionOut', duration: 0.6 });
// registered ids: motionOutSoft, motionOut, motionOutStrong, motionOutExpo, motionIn, motionInOut, motionInOutExpo, motionDrift
// usage: gsap.to(el, { ease: 'motionOutExpo' })
```

### 2.3 Duration and stagger scale

- **Duration scales with distance and area**, not with importance:
  - ≤ 24px travel or colour: 0.18–0.35s
  - one line of display type (100–110% of its line height inside a mask): 0.8–1.1s
  - full-bleed media un-clip: 1.1–1.4s
  - full-screen curtain: 0.5–0.7s per leg, legs overlapped
- **Exit ≈ 0.6 × enter.** An exit that uses an ease-in and is shorter than the entrance feels decisive. Observed: `power2.in` sits at 0.25–0.4s against `expo.out` at 0.8–1.2s.
- **Stagger per unit:**
  - chars 0.015–0.03
  - words 0.04–0.06
  - lines 0.07–0.12
  - cards and grid items 0.06–0.1
  - For large sets, cap the total spread with `stagger: { amount: 0.6 }` so nobody waits more than about 0.6s for the last item.
- **Hover and press never exceed 0.25s** to start responding. A lagged follower (cursor ring, magnet) may settle over 0.35–0.5s, but the state change (fill or colour) must be immediate.

---

## 3. Foundation: the visible-by-default boot contract

Three layers, each safe on its own:

1. **HTML/CSS alone renders every piece of content at rest.** No stylesheet hides text, media or controls waiting for JS.
2. **A capability flag, never a hide.** A tiny classic script in `<head>` adds `motion-ok` only when reduced motion is not requested. Hidden start states are applied by JS **in the same frame the animation starts**, or, for the one above-the-fold intro, by CSS with a **deadline** that un-hides the content even if the bundle never boots.
3. **All motion code runs inside `gsap.matchMedia()` under `(prefers-reduced-motion: no-preference)`**, so reduced-motion users get the at-rest page, and switching the OS setting live reverts everything ([matchMedia docs](https://gsap.com/docs/v3/GSAP/gsap.matchMedia())).

```html
<head>
  <script>
    /* classic, inline, before CSS that depends on it: flags capability only */
    (function (root) {
      try { if (!matchMedia('(prefers-reduced-motion: reduce)').matches) root.classList.add('motion-ok'); }
      catch (e) {}
    })(document.documentElement);
  </script>
  <link rel="stylesheet" href="/site.css">
</head>
```

```js
// main.js: module entry
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { SplitText } from 'gsap/SplitText';
gsap.registerPlugin(ScrollTrigger, SplitText);

export const mm = gsap.matchMedia();
// Every recipe below registers inside mm.add('(prefers-reduced-motion: no-preference)', …)
// or a stricter query. Returning a cleanup fn is optional; mm reverts tweens and triggers.
```

Rules:

- **Never set a hidden state outside the no-preference branch.** Under `reduce` the page must already be at rest.
- **Never re-hide something that is already on screen.** If an element is in the viewport at boot (`ScrollTrigger.isInViewport(el)`, [docs](https://gsap.com/docs/v3/Plugins/ScrollTrigger/static.isInViewport())), either it belongs to the deadline-guarded intro or it does not animate in.
- **Start states must be readable** for anything CSS scroll-driven (`view()`). Unsupported browsers and full-page screenshots render the 0% keyframe for below-the-fold elements (`fill: both`). Use clip `inset(10%)` rather than `inset(100%)`, `scale(1.12)` rather than `opacity: 0`.

---

## 4. Recipes

All code targets GSAP 3.15.0, Lenis 1.3.26 and Taxi 1.9.1, checked against the docs linked in §1.

### 4.1 Lenis + ScrollTrigger (the base layer)

```js
// smooth.js — imported by every other recipe as { lenis }
import Lenis from 'lenis';
import 'lenis/dist/lenis.css';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

export const lenis = new Lenis({
  lerp: 0.1,          // 0.08–0.12. Below ~0.07 feels floaty or "jacked". Don't also pass duration.
  smoothWheel: true,
  syncTouch: false,   // keep native touch momentum (syncTouch is unstable on iOS < 16)
  anchors: true,      // Lenis handles in-page #links
  autoRaf: false,     // GSAP's ticker drives Lenis: exactly one rAF loop
  // respectReducedMotion: true  ← default since 1.3.26; on older versions, skip `new Lenis` under reduce
});

lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((time) => lenis.raf(time * 1000)); // seconds → ms
gsap.ticker.lagSmoothing(0);                       // no catch-up jumps against the smoothed scroll

// layout changes after boot move trigger positions: re-measure
document.fonts.ready.then(() => ScrollTrigger.refresh());
addEventListener('load', () => ScrollTrigger.refresh());
ScrollTrigger.config({ ignoreMobileResize: true }); // iOS address-bar show/hide

// scroll lock for menus/modals; mark scrollable panels <div data-lenis-prevent>
export const lockScroll = () => lenis.stop();
export const unlockScroll = () => lenis.start();
```

Checks: the integration snippet is the one in the Lenis README. `ScrollTrigger.scrollerProxy` is **not** needed because Lenis scrolls the real document. Do not combine Lenis with ScrollSmoother (two smoothers fighting over one scroll). With Lenis already smoothing, prefer `scrub: true` or a small number (≤ 0.3); `scrub: 1` on top of lerp stacks two lags.

### 4.2 Masked line reveal with SplitText (headings, visible without JS)

The DOM is split at boot while the text stays visible. The hidden state (`yPercent: 110` inside the mask) exists **only while the tween runs**, because `immediateRender: false` defers the `from` values until the trigger plays it. The trigger point is the first pixel entering the viewport, so nothing on screen is ever re-hidden.

```html
<h2 class="display" data-reveal="lines">Built for the long quiet middle of the day</h2>
```

```css
/* SplitText mask elements get "<linesClass>-mask". Pad so descenders and accents aren't clipped by tight line-height. */
.line-mask { padding-block: 0.12em; margin-block: -0.12em; }
.display[data-reveal] { text-wrap: wrap; } /* SplitText docs: avoid text-wrap: balance on split text */
```

```js
mm.add('(prefers-reduced-motion: no-preference)', () => {
  gsap.utils.toArray('[data-reveal="lines"]').forEach((el) => {
    if (ScrollTrigger.isInViewport(el, 0.01)) return; // on screen at boot: leave it alone
    SplitText.create(el, {
      type: 'lines',
      mask: 'lines',
      linesClass: 'line',
      autoSplit: true,           // re-split on font load / width change…
      onSplit(self) {            // …so build the tween here and RETURN it
        return gsap.from(self.lines, {
          yPercent: 110,
          duration: 1.0,
          ease: 'motionOutExpo',
          stagger: 0.08,
          immediateRender: false,   // hidden only while playing
          scrollTrigger: { trigger: el, start: 'top bottom', once: true },
          onComplete: () => self.revert(), // restore the original DOM (a11y, node count)
        });
      },
    });
  });
});
```

Accessibility, verified:

- SplitText's default `aria: "auto"` puts `aria-label` on the split element and `aria-hidden` on every piece.
- ARIA 1.2 **prohibits naming** the `generic` and `paragraph` roles ([§5.2.8.6](https://www.w3.org/TR/wai-aria-1.2/#namefromprohibited)). On a `<p>`, `<div>` or `<span>` the label may be ignored while the children are hidden, and the text can disappear for screen-reader users.
- **Split headings (h1–h6) only.** For paragraphs, use `aria: "hidden"` plus a visually hidden copy (the docs' own recommendation for nested links and emphasis), or do not split body copy at all.
- For SEO on a split `<h1>`, keep `aria: "auto"` and real `<title>`/meta description ([docs](https://gsap.com/docs/v3/Plugins/SplitText/)).

Variants:

- **Words:** `type: 'words'`, `mask: 'words'`, stagger 0.04–0.06.
- **Chars:** `type: 'words,chars'`, `mask: 'chars'`, stagger 0.015–0.03. Include words so line breaks stay natural. Docs note kerning shifts; `font-kerning: none` fixes it.
- **Many identical blocks:** `ScrollTrigger.batch()` with `interval: 0.1` and `batchMax` to stagger groups that enter together ([docs](https://gsap.com/docs/v3/Plugins/ScrollTrigger/static.batch())).

### 4.3 Above-the-fold hero intro, with a CSS deadline

The hero is on screen at first paint, so the only way to "reveal" it without a flash of the finished state is to arm it in CSS. That hide is legitimate only with a **deadline**: if the bundle is slow or broken, CSS un-arms it by itself.

```css
.motion-ok [data-intro] {
  clip-path: inset(0 0 100% 0);                   /* armed: clipped, not opacity 0 */
  animation: intro-deadline 1ms 2.5s forwards;     /* un-arms even if JS never runs */
}
.motion-ok.intro-owned [data-intro] { clip-path: none; animation: none; } /* JS took over */
@keyframes intro-deadline { to { clip-path: inset(0 0 0 0); } }
```

```js
mm.add('(prefers-reduced-motion: no-preference)', () => {
  const root = document.documentElement;
  const intro = document.querySelector('[data-intro]');
  if (!intro) return;
  document.fonts.ready.then(() => {
    const deadline = intro.getAnimations().find((a) => a.animationName === 'intro-deadline');
    if (!deadline || deadline.playState === 'finished') { root.classList.add('intro-owned'); return; } // too late: never re-hide
    const split = SplitText.create(intro.querySelector('h1'), { type: 'lines', mask: 'lines', linesClass: 'line' });
    gsap.set(split.lines, { yPercent: 110 });   // same frame as un-arming: no flash
    root.classList.add('intro-owned');
    const tl = gsap.timeline({ onComplete: () => split.revert() })
      .to(split.lines, { yPercent: 0, duration: 1.1, ease: 'motionOutExpo', stagger: 0.08 })
      .from('[data-intro-meta]', { y: 16, duration: 0.8, ease: 'motionOut' }, '<0.35'); // y only, stays visible
    setTimeout(() => tl.progress(1), 3000);     // starved ticker (background tab): finish anyway
  });
});
```

Keep the total intro ≤ 1.4s and start it at DOMContentLoaded plus fonts, not `window.load`. A hero clipped until the intro plays probably delays Largest Contentful Paint (LCP) (unverified how Chrome's LCP treats `clip-path`-hidden text). Measure it.

### 4.4 Image reveal: clip plus scale-settle

JS version (triggered, time-based). The start state is only partly clipped, so it is readable even if frozen.

```js
mm.add('(prefers-reduced-motion: no-preference)', () => {
  gsap.utils.toArray('[data-reveal="media"]').forEach((fig) => {
    if (ScrollTrigger.isInViewport(fig, 0.01)) return;
    const media = fig.querySelector('img, video');
    gsap.timeline({
      defaults: { immediateRender: false },
      scrollTrigger: { trigger: fig, start: 'top bottom', once: true },
    })
      .fromTo(fig, { clipPath: 'inset(14% 10% 14% 10% round 6px)' },
                   { clipPath: 'inset(0% 0% 0% 0% round 0px)', duration: 1.2, ease: 'motionOutExpo', clearProps: 'clipPath' }, 0)
      .fromTo(media, { scale: 1.18 }, { scale: 1, duration: 1.6, ease: 'motionOutExpo' }, 0);
  });
});
```

Use `fromTo` with both ends as `inset()`. GSAP cannot interpolate `none` → `inset()`.

CSS scroll-driven version (scrubbed, no JS, Chrome/Safari 26; static in Firefox):

```css
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .media-reveal { view-timeline-name: --media; }
    .media-reveal {
      animation: media-open linear both;
      animation-timeline: --media;              /* MUST come after the `animation` shorthand, which resets it */
      animation-range: entry 0% entry 100%;
    }
    .media-reveal > img {
      animation: media-settle linear both;
      animation-timeline: --media;
      animation-range: entry 0% cover 50%;
    }
  }
}
@keyframes media-open { from { clip-path: inset(12% 8% round 6px); } to { clip-path: inset(0 round 0); } }
@keyframes media-settle { from { scale: 1.15; } to { scale: 1; } }
```

The `animation` shorthand resets `animation-timeline` ([MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline)). Range names are defined on [MDN timeline-range-name](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/timeline-range-name). Chrome documents that scroll-driven animations of compositor-friendly properties can run off the main thread ([Chrome for Developers](https://developer.chrome.com/docs/css-ui/scroll-driven-animations)).

### 4.5 Pinned horizontal scroll section

Progressive enhancement: without JS, on small screens, or under reduced motion, the track is a native, keyboard-scrollable, snap-aligned horizontal scroller. JS turns it into a pinned, vertically driven track only on wide screens.

```html
<section class="hscroll" aria-label="Selected work">
  <div class="hscroll__track">
    <article class="hscroll__panel">…</article>
    <article class="hscroll__panel">…</article>
  </div>
</section>
```

```css
.hscroll { overflow-x: clip; }              /* the translated track must not widen the page */
.hscroll__track { display: flex; gap: 4vw; padding-inline: 4vw;
  overflow-x: auto; scroll-snap-type: x mandatory; overscroll-behavior-x: contain; }
.hscroll__panel { flex: 0 0 min(80vw, 56rem); scroll-snap-align: start; }
.hscroll.is-pinned .hscroll__track { overflow: visible; scroll-snap-type: none; }
```

```js
mm.add('(min-width: 60em) and (prefers-reduced-motion: no-preference)', () => {
  const section = document.querySelector('.hscroll');
  const track = section.querySelector('.hscroll__track');
  section.classList.add('is-pinned');
  const distance = () => track.scrollWidth - document.documentElement.clientWidth;

  const tween = gsap.to(track, {
    x: () => -distance(),
    ease: 'none',                        // required when children use containerAnimation
    scrollTrigger: {
      trigger: section, start: 'top top', end: () => '+=' + distance(),
      pin: true, scrub: true, anticipatePin: 1, invalidateOnRefresh: true,
    },
  });

  // per-panel effects driven by horizontal position (pin/snap are unavailable here)
  track.querySelectorAll('.hscroll__panel img').forEach((img) => {
    gsap.fromTo(img, { scale: 1.12 }, { scale: 1, ease: 'none',
      scrollTrigger: { trigger: img, containerAnimation: tween, start: 'left right', end: 'right left', scrub: true } });
  });

  // keyboard users: tabbing to an off-screen panel scrolls the page to it
  const onFocus = (e) => {
    const panel = e.target.closest('.hscroll__panel'); if (!panel) return;
    const st = tween.scrollTrigger;
    const p = gsap.utils.clamp(0, 1, panel.offsetLeft / distance());
    lenis.scrollTo(st.start + p * (st.end - st.start), { immediate: true });
  };
  track.addEventListener('focusin', onFocus);
  return () => { track.removeEventListener('focusin', onFocus); section.classList.remove('is-pinned'); };
});
```

Rules:

- The containerAnimation must be linear.
- Pinning and snapping are unavailable on triggers that use `containerAnimation` ([ScrollTrigger docs](https://gsap.com/docs/v3/Plugins/ScrollTrigger/)).
- Keep extra scroll length ≤ about 1.5 viewports per pin. Longer reads as scroll-jacking.
- Don't animate the pinned element itself, only its children (docs warning).
- If the pinned parent is `display: flex`, `pinSpacing` defaults to false (docs).

### 4.6 Scrubbed hero-to-section transition

A full-bleed hero frames down into a card while the title drifts. The motion is tied to scroll position, so it is spatial storytelling rather than a content reveal. **Never scrub text in or out of legibility.** Readers stop mid-scroll.

```css
.hero__media { clip-path: inset(0 0 0 0 round 0px); } /* matching function for interpolation */
```

```js
mm.add('(prefers-reduced-motion: no-preference)', () => {
  gsap.timeline({
    defaults: { ease: 'none' },
    scrollTrigger: { trigger: '.hero', start: 'top top', end: '+=80%', scrub: true, pin: true, anticipatePin: 1 },
  })
    .to('.hero__media', { clipPath: 'inset(8% 6% 8% 6% round 12px)' }, 0)
    .to('.hero__media img', { scale: 1.12, yPercent: -6 }, 0)
    .to('.hero__title', { yPercent: -35 }, 0);
});
```

CSS-only variant (Chrome/Safari 26). Sticky provides the "pin". For a subject taller than the viewport, `contain 0%–100%` is exactly the stuck phase ([MDN range names](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/timeline-range-name)).

```css
.hero { height: 180svh; view-timeline-name: --hero; }
.hero__stage { position: sticky; top: 0; height: 100svh; overflow: clip; }
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .hero__media { animation: hero-frame linear both; animation-timeline: --hero; animation-range: contain 0% contain 100%; }
  }
}
@keyframes hero-frame { from { clip-path: inset(0 round 0); } to { clip-path: inset(8% 6% round 12px); } } /* both ends inset(): `none` doesn't interpolate */
```

### 4.7 Sticky stacking cards

Stacking works with CSS alone: sticky cards, later ones painting over earlier ones. JS only adds the tonal recede of the covered card.

```html
<section class="stack">
  <article class="stack__card" style="--i:0">… <span class="stack__shade" aria-hidden="true"></span></article>
  <article class="stack__card" style="--i:1">… <span class="stack__shade" aria-hidden="true"></span></article>
</section>
```

```css
.stack { display: grid; gap: 12vh; padding-block: 10vh 30vh; }
.stack__card { position: sticky; top: calc(10svh + var(--i) * 1.25rem); min-height: 70svh;
  transform-origin: 50% 0; isolation: isolate; }
.stack__shade { position: absolute; inset: 0; background: var(--ink); opacity: 0; pointer-events: none; border-radius: inherit; }
```

```js
mm.add('(prefers-reduced-motion: no-preference)', () => {
  const cards = gsap.utils.toArray('.stack__card');
  cards.forEach((card, i) => {
    const next = cards[i + 1]; if (!next) return;
    const settle = () => `top ${innerHeight * 0.10 + (i + 1) * 20}px`; // where `next` sticks
    gsap.timeline({ defaults: { ease: 'none' },
      scrollTrigger: { trigger: next, start: 'top bottom', end: settle, scrub: true, invalidateOnRefresh: true } })
      .to(card, { scale: 0.94 }, 0)
      .to(card.querySelector('.stack__shade'), { opacity: 0.35 }, 0); // composited opacity, not filter: brightness()
  });
});
```

Rationale for the shade layer: animating `filter` on large layers repaints every frame, while animating the opacity of an overlay element composites. The CSS view-timeline version is not recommended here: how a stuck sticky subject's view progress behaves was not verified.

### 4.8 Marquee (CSS core, WAAPI velocity boost, WCAG pause)

```html
<div class="marquee" data-marquee>
  <div class="marquee__track">
    <ul class="marquee__group">…</ul>
    <ul class="marquee__group" aria-hidden="true">…</ul> <!-- visual duplicate for the loop -->
  </div>
  <button class="marquee__toggle" type="button" aria-pressed="false">Pause</button>
</div>
```

```css
.marquee { overflow: clip; }
.marquee__track { display: flex; width: max-content; }
.marquee__group { display: flex; flex-shrink: 0; gap: var(--gap, 3rem); padding-inline-end: var(--gap, 3rem); }
@media (prefers-reduced-motion: no-preference) {
  .marquee__track { animation: marquee var(--marquee-duration, 40s) linear infinite; }
  .marquee:is(:hover, :focus-within, .is-paused) .marquee__track { animation-play-state: paused; }
}
@media (prefers-reduced-motion: reduce) { .marquee { overflow-x: auto; } }
@keyframes marquee { to { translate: -50% 0; } }
```

```js
document.querySelectorAll('[data-marquee]').forEach((m) => {
  const track = m.querySelector('.marquee__track');
  const group = m.querySelector('.marquee__group');
  track.style.setProperty('--marquee-duration', `${group.offsetWidth / 60}s`); // constant ~60px/s at any width
  const btn = m.querySelector('.marquee__toggle');
  btn.addEventListener('click', () => {
    const paused = m.classList.toggle('is-paused');
    btn.setAttribute('aria-pressed', String(paused));
    btn.textContent = paused ? 'Play' : 'Pause';
  });

  const anim = track.getAnimations().find((a) => a.animationName === 'marquee');
  if (!anim || !lenis) return; // `lenis` = the instance exported in §4.1 (window.lenis is only a version object in 1.3.26)
  let boost = 0;
  lenis.on('scroll', (l) => { boost = gsap.utils.clamp(-3, 3, l.velocity / 15); }); // velocity units: px/frame (unverified)
  gsap.ticker.add(() => {
    boost *= Math.pow(0.9, gsap.ticker.deltaRatio()); // fps-independent decay
    const rate = 1 + Math.abs(boost);
    if (Math.abs(anim.playbackRate - rate) > 0.01) anim.updatePlaybackRate(rate);
  });
});
```

Moving content that starts automatically, lasts more than 5 seconds and runs alongside other content needs a pause, stop or hide mechanism: **WCAG 2.2.2, Level A** ([Understanding 2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html)). Hover-to-pause alone does not satisfy keyboard or touch users, hence the button. Animate `translate` (composited), never `left` or `margin`.

### 4.9 Magnetic button without the hover boop

The law says a button that lifts or scales on hover is slop, and the button should not move. So the **box never moves**. Only the inner label drifts a few pixels toward the pointer inside a static hit area, and the state change itself is a tonal fill.

```html
<a class="btn" href="/contact" data-magnetic><span class="btn__label">Start a project</span></a>
```

```css
.btn { display: inline-grid; place-items: center; padding: 1rem 1.6rem; border-radius: 999px;
  background: var(--btn-bg); color: var(--btn-ink);
  transition: background-color var(--dur-micro) var(--ease-out-soft); }
.btn:hover { background: var(--btn-bg-hover); }  /* a tonal step (lighter/darker, desaturated), not a saturated pop */
.btn:active { background: var(--btn-bg-press); }
.btn__label { display: inline-block; will-change: transform; }
```

```js
mm.add('(hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference)', () => {
  const offs = [];
  document.querySelectorAll('[data-magnetic]').forEach((btn) => {
    const label = btn.querySelector('.btn__label');
    const xTo = gsap.quickTo(label, 'x', { duration: 0.45, ease: 'motionOut' });
    const yTo = gsap.quickTo(label, 'y', { duration: 0.45, ease: 'motionOut' });
    const MAX = 6; // px: a pull, not a jump
    let r;
    const enter = () => { r = btn.getBoundingClientRect(); };        // read once, not per move
    const move = (e) => {
      const dx = (e.clientX - (r.left + r.width / 2)) / (r.width / 2);
      const dy = (e.clientY - (r.top + r.height / 2)) / (r.height / 2);
      xTo(gsap.utils.clamp(-1, 1, dx) * MAX);
      yTo(gsap.utils.clamp(-1, 1, dy) * MAX * 0.5);
    };
    const leave = () => { xTo(0); yTo(0); };
    btn.addEventListener('pointerenter', enter);
    btn.addEventListener('pointermove', move);
    btn.addEventListener('pointerleave', leave);
    offs.push(() => { btn.removeEventListener('pointerenter', enter); btn.removeEventListener('pointermove', move); btn.removeEventListener('pointerleave', leave); });
  });
  return () => offs.forEach((f) => f());
});
```

`gsap.quickTo` is the documented fast path for pointer followers ([docs](https://gsap.com/docs/v3/GSAP/gsap.quickTo())). Keyboard focus gets a visible ring and no magnet.

### 4.10 Custom cursor, done accessibly

Keep the **native cursor**. The follower is decoration that can carry a contextual label ("View", "Drag") which duplicates information already present in the link text.

```html
<div class="cursor" aria-hidden="true"><span class="cursor__label"></span></div>
```

```css
.cursor { position: fixed; left: 0; top: 0; z-index: 90; pointer-events: none;
  width: 2.5rem; height: 2.5rem; margin: -1.25rem 0 0 -1.25rem; border-radius: 50%;
  border: 1px solid color-mix(in oklab, currentColor 55%, transparent);
  opacity: 0; transition: opacity var(--dur-micro) var(--ease-out-soft); }
.cursor.is-visible { opacity: 1; }                       /* decoration only: fine to start hidden */
@media (hover: none), (pointer: coarse), (forced-colors: active), (prefers-reduced-motion: reduce) {
  .cursor { display: none; }
}
```

```js
mm.add('(hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference)', () => {
  const el = document.querySelector('.cursor');
  const label = el.querySelector('.cursor__label');
  const xTo = gsap.quickTo(el, 'x', { duration: 0.35, ease: 'motionOut' });
  const yTo = gsap.quickTo(el, 'y', { duration: 0.35, ease: 'motionOut' });
  const move = (e) => { el.classList.add('is-visible'); xTo(e.clientX); yTo(e.clientY); };
  const out = (e) => { if (!e.relatedTarget) el.classList.remove('is-visible'); };
  const over = (e) => { const t = e.target.closest('[data-cursor]'); label.textContent = t ? t.dataset.cursor : ''; };
  addEventListener('pointermove', move, { passive: true });
  document.addEventListener('pointerout', out);
  document.addEventListener('pointerover', over);
  return () => { removeEventListener('pointermove', move); document.removeEventListener('pointerout', out); document.removeEventListener('pointerover', over); };
});
```

Rules:

- No `cursor: none` on `body`. A lagging replacement makes the true pointer position ambiguous.
- If one region must replace the cursor (a drag gallery), use native `cursor: grab` there. Any replacement must track 1:1, with any lagging ring as a second layer.
- Mount the cursor at `body` level, **outside** any transformed or filtered page container (see §6.5), or it will drift.

### 4.11 Page transitions: View Transitions first, PJAX where state must persist

**A. Multi-page site (Chrome 126+, Safari 18.2+; Firefox navigates instantly):**

```css
@view-transition { navigation: auto; }

@media (prefers-reduced-motion: no-preference) {
  ::view-transition-old(root) { animation: 420ms var(--ease-in) both vt-recede; }
  ::view-transition-new(root) { animation: 900ms var(--ease-out-expo) both vt-wipe; }
}
@media (prefers-reduced-motion: reduce) {
  ::view-transition-group(*), ::view-transition-old(*), ::view-transition-new(*) { animation: none !important; }
}
@keyframes vt-recede { to { translate: 0 -4vh; filter: brightness(.6); } }
@keyframes vt-wipe { from { clip-path: inset(100% 0 0 0); } to { clip-path: inset(0 0 0 0); } }

/* shared element: the detail page's hero pairs with the clicked thumbnail */
.project-hero__media { view-transition-name: project-media; }
```

```html
<!-- index page, classic script in <head> -->
<script>
  addEventListener('pageswap', (e) => {
    if (!e.viewTransition || !e.activation) return;
    const path = new URL(e.activation.entry.url).pathname;
    const img = document.querySelector(`a[data-project][href="${path}"] img`);
    if (!img) return;
    img.style.viewTransitionName = 'project-media';   // exactly one element carries the name
    e.viewTransition.finished.finally(() => { img.style.viewTransitionName = ''; }); // bfcache-safe
  });
</script>
```

Keep pages fast: the transition is skipped after 4s in Chrome. Pair it with prerendering through Speculation Rules where appropriate (the Chrome docs recommend this). Use `<link rel="expect" blocking="render" href="#hero">` only when you can measure the Core Web Vitals cost.

**B. Persistent-state sites (WebGL canvas, audio, Lenis instance): Taxi with same-document View Transitions and a GSAP fallback.** Same-document View Transitions are Baseline, so this path also animates in Firefox 144+.

```html
<canvas class="gl" aria-hidden="true"></canvas>            <!-- persists: outside the swapped view -->
<main data-taxi><div data-taxi-view>…page…</div></main>
<div class="curtain" aria-hidden="true"></div>              <!-- only the curtain ever covers content -->
```

```css
.curtain { position: fixed; inset: 0; z-index: 80; pointer-events: none;
  background: var(--surface-2); clip-path: inset(100% 0 0 0); } /* parked below the fold, at body level */
```

```js
import { Core, Transition } from '@unseenco/taxi';
import { lenis } from './smooth.js'; // the §4.1 instance

const canVT = typeof document.startViewTransition === 'function';
const reduce = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
const curtain = document.querySelector('.curtain');

class PageTransition extends Transition {
  onLeave({ done }) {
    if (reduce()) return done();
    if (canVT) {
      // Old page is snapshotted; rendering stays frozen until onEnter resolves the swap.
      // Keep fetches warm (Taxi prefetches on hover/focus by default). A long freeze may be aborted (unverified timeout).
      this.vt = document.startViewTransition(() => new Promise((resolve) => { this.swap = resolve; done(); }));
      return;
    }
    gsap.fromTo(curtain, { clipPath: 'inset(100% 0 0 0)' },
      { clipPath: 'inset(0% 0 0 0)', duration: 0.5, ease: 'motionInOut', onComplete: done });
  }
  onEnter({ done }) {
    lenis.scrollTo(0, { immediate: true, force: true });
    if (this.swap) { this.swap(); this.swap = null; this.vt.finished.finally(done); return; }
    if (reduce()) return done();
    gsap.to(curtain, { clipPath: 'inset(0 0 100% 0)', duration: 0.6, ease: 'motionInOut', onComplete: done });
  }
}

const taxi = new Core({ transitions: { default: PageTransition } });

// per-page motion lives in a context so it can be reverted wholesale
let pageCtx = initPage(document.querySelector('[data-taxi-view]'));
taxi.on('NAVIGATE_OUT', () => pageCtx?.revert());
taxi.on('NAVIGATE_END', () => {
  pageCtx = initPage(document.querySelector('[data-taxi-view]'));
  ScrollTrigger.refresh();
});
function initPage(root) { return gsap.context(() => { /* recipes 4.2–4.8 scoped to root */ }, root); }
```

With View Transitions, style the pseudo-elements the same way as in A (`::view-transition-old/new(root)`, named groups for shared elements). The curtain path is the fallback for browsers without View Transitions. The curtain has `pointer-events: none` and is removed in `finally` on error paths.

**Barba mapping (existing codebases only):** `leave(data)` gets `data.current.container` and `enter(data)` gets `data.next.container`. Return the GSAP tween (it is thenable). Put `gsap.context` revert and re-init in `barba.hooks.before` / `barba.hooks.after`.

**Swup:** `new Swup({ native: true })`. Define `::view-transition-*` CSS and a fallback under `html.is-changing:not(.swup-native)`.

**Framework routers** (Astro, Next, Nuxt) have their own View Transition integrations. In React 19.3, Motion 13.4 `AnimateView` wraps React's `ViewTransition`.

### 4.12 Preloader with honest progress

Only show a preloader when there is something real to wait for, such as a GLB scene, a video, or a large texture atlas. The number shown must be the weighted fraction of real loads, and it may only increase.

```html
<div class="loader" aria-hidden="true"><span class="loader__count" data-loader-count>0</span></div>
```

```css
.loader { position: fixed; inset: 0; z-index: 100; display: grid; align-items: end; padding: 4vw;
  background: var(--surface); clip-path: inset(0 0 0 0);          /* inset() start so the exit wipe interpolates */
  animation: loader-deadline 1ms 4s forwards; }                    /* dies even if JS does */
html:not(.motion-ok) .loader { display: none; }                               /* no-JS / reduced motion: no loader */
@keyframes loader-deadline { to { visibility: hidden; } }
```

```js
function xhrProgress(url, onProgress, responseType = 'arraybuffer') {
  return new Promise((resolve, reject) => {
    const x = new XMLHttpRequest();
    x.open('GET', url); x.responseType = responseType;
    x.onprogress = (e) => { if (e.lengthComputable) onProgress(Math.min(1, e.loaded / e.total)); };
    x.onload = () => (x.status < 400 ? (onProgress(1), resolve(x.response)) : reject(new Error(String(x.status))));
    x.onerror = () => reject(new Error('network'));
    x.send();
  });
}

async function preload({ hardCapMs = 4000 } = {}) {
  const tasks = [
    { w: 1, run: (p) => document.fonts.ready.then(() => p(1)) },
    { w: 2, run: (p) => (document.querySelector('.hero img')?.decode() ?? Promise.resolve()).catch(() => {}).then(() => p(1)) },
    { w: 7, run: (p) => xhrProgress('/scene.glb', p) },
  ];
  const total = tasks.reduce((s, t) => s + t.w, 0);
  const got = tasks.map(() => 0);
  const shown = { v: 0 };
  const out = document.querySelector('[data-loader-count]');
  const render = () => { out.textContent = Math.round(shown.v); };
  const toTarget = () => {
    const target = (100 * got.reduce((s, v, i) => s + v * tasks[i].w, 0)) / total;
    gsap.to(shown, { v: Math.max(shown.v, target), duration: 0.4, ease: 'motionOut', overwrite: true, onUpdate: render });
  };
  const all = Promise.allSettled(tasks.map((t, i) => t.run((f) => { got[i] = Math.max(got[i], f); toTarget(); })));
  await Promise.race([all, new Promise((r) => setTimeout(r, hardCapMs))]);   // never hold the page hostage
  return gsap.to('.loader', { clipPath: 'inset(0 0 100% 0)', duration: 0.7, ease: 'motionInOut',
    onComplete: () => document.querySelector('.loader')?.remove() });
}
```

Why XHR: with `fetch()` streams, `Content-Length` is the *encoded* size while the chunks are *decoded*, so gzip or brotli responses overshoot 100%. XHR progress events remain the practical option ([Jake Archibald, 2025-09-15](https://jakearchibald.com/2025/fetch-streams-not-for-progress/), [whatwg/fetch#1358](https://github.com/whatwg/fetch/issues/1358)). Skip the loader on repeat visits: set a `sessionStorage` flag inside try/catch. Timer-driven 0→100 counters are fake progress. Don't build them.

### 4.13 React: Motion equivalents (brief)

- `<MotionConfig reducedMotion="user">` at the root.
- **Never `initial={{ opacity: 0 }}` on content.** SSR ships it invisible. Use `initial={false}` for above-the-fold content, or transform-only initials (`initial={{ y: 24 }}`) with `whileInView={{ y: 0 }}` and `viewport={{ once: true, amount: 0.2 }}`.
- For scroll scenes, `useScroll({ target, offset: ['start end', 'end start'] })` plus `useTransform`. The vanilla `scroll()` uses ScrollTimeline where supported.
- GSAP in React goes through `useGSAP(() => { … }, { scope })` from `@gsap/react` (automatic `gsap.context` cleanup, strict-mode safe).

---

## 5. Choreography principles

1. **Hierarchy of motion, four tiers with separate budgets:**
   - (a) Signature: one authored moment per viewport (hero morph, horizontal gallery, WebGL scene reacting to scroll).
   - (b) Structural: page transitions and section entrances, all on the same 2–3 tokens.
   - (c) Micro: hover, press and focus, ≤ 0.25s, state changes without displacing the element box.
   - (d) Ambient: loops (marquee, drift), slow, low amplitude, pausable.
   - When two tiers compete, the lower tier yields: micro and ambient hold still while a signature scene scrubs.
2. **One hero moment per viewport.** At most one element travels more than about 20% of the viewport at a time. Everything else is at rest or does micro-motion. If a screen has two scrubbed scenes, cut one.
3. **Triggered for content, scrubbed for space.** Text and UI reveal on a time-based trigger so they always finish. Parallax, frames, horizontal travel and 3D camera moves are scrubbed because they *belong* to a scroll position. Never scrub legibility.
4. **Overlap, don't queue.**
   - Start the next beat at 60–75% of the previous one: `'<0.3'` or `'-=0.4'` position parameters.
   - Page curtains: the enter leg starts at about 80% of the exit leg.
   - Sequential waits (`'>'`) everywhere make sites feel slow.
5. **Stagger follows reading order and caps the spread.**
   - Lines top to bottom; grids by row (`stagger: { grid: 'auto', from: 'start' }`).
   - Total spread ≤ 0.6s (`amount`).
   - Stagger direction matches travel direction.
6. **Direction coherence.** Scrolling down brings content up from below and exits go up; back navigation reverses. Use `easeReverse` (3.15) so reversing toggles close with an ease-in instead of a mirrored ease-out.
7. **Easing roles are fixed:**
   - out for entrances
   - in for exits
   - inOut for A→B travel on screen (curtains, Flip)
   - none for scrub and loops
   - Observed SOTD usage matches this split: out 227, inOut 174, in 86 site-presences.
8. **Velocity-aware effects are bounded and decay.**
   - Map Lenis `velocity` or ScrollTrigger `getVelocity()` to marquee speed, a slight skew (≤ 3–4°) or image lag.
   - Clamp it, decay it with `gsap.ticker.deltaRatio()`, and never let velocity move text off its baseline.
   - `fastScrollEnd` (default 2500 px/s) forces triggered reveals to finish when the user flies past, and `preventOverlaps` completes earlier sequences before starting new ones ([ScrollTrigger docs](https://gsap.com/docs/v3/Plugins/ScrollTrigger/)).
9. **Consistency beats variety.** Two or three easing tokens and one reveal grammar across the site. Most award sites use `power2.out`, `power3.out` and `expo.out` over and over. The signature comes from *one* bespoke moment, not ten different fades.
10. **Motion responds to something:** scroll, pointer, state or loading. A signature that only loops in place is the "fixed background costume" the law rejects.

---

## 6. Failure modes and fixes

**6.1 Scroll-jacking.**
- Symptoms: wheel hijacked into slide steps (`Observer` fullpage decks, aggressive `snap`), `lerp` < 0.07, `wheelMultiplier` ≠ 1, `syncTouch` on phones, pins longer than about 1.5 viewports, `ScrollTrigger.normalizeScroll(true)` (which forces scrolling onto the JS thread) on content pages.
- Fix: smoothing that rides native scroll (Lenis or ScrollSmoother, never both), lerp 0.08–0.12, native touch, short pins, no snap on reading content.
- Observer-driven "experience" decks only on dedicated pages, with keyboard arrows and a visible escape.

**6.2 FOUC before JS.**
- (a) Visible-then-hidden flash: JS re-hides content that already painted. Fix: skip on-screen elements (`isInViewport`) and use the deadline pattern for the intro (§4.3).
- (b) Line-break jump: text is split before fonts load. Fix: `autoSplit: true` with animations created in `onSplit`, or wait for `document.fonts.ready`.
- (c) Invisible SSR: Motion `initial` ships `opacity: 0`. Fix per §4.13.
- (d) Clipped descenders inside line masks. Fix: pad the `-mask` element (§4.2).

**6.3 Reveal never firing.** Causes and fixes:
- Trigger positions measured before fonts, images or late sections loaded: `ScrollTrigger.refresh()` after `document.fonts.ready` and `load`. Give images `width`/`height` attributes.
- Start beyond the maximum scroll near the page end: `start: 'clamp(top 85%)'` (3.12+).
- Pins created out of document order: create top to bottom, or use `refreshPriority`.
- A second smoother or scroller the triggers don't know about: create ScrollSmoother before triggers, and set `scroller` for custom containers.
- Hidden tabs or accordions (`display: none` at measure time): refresh on open.
- Background tab starving rAF: the timeout failsafe in §4.3.
- Screenshot or print passes: nothing below the fold is ever armed with the lazy pattern. Keep CSS `view()` 0% keyframes readable.
- **The root fix is structural: lazy arming means a trigger that never fires leaves content visible.**

**6.4 Layout thrash and jank.**
- Animate `transform`, `opacity` and `clip-path`. Never animate `top`/`left`/`width`/`height`/`margin`.
- Don't read layout (`getBoundingClientRect`, `offsetTop`) in scroll or pointer handlers after writes. Cache rects on `pointerenter` or on ScrollTrigger `refreshInit`.
- Use `quickTo`/`quickSetter` for high-frequency updates.
- Split lines or words, not chars, on long text, and `revert()` after the reveal.
- Avoid animated `filter: blur()` or `brightness()` on big layers; use overlay opacity.
- `will-change` only on elements that are actually about to animate. It costs memory and creates containing blocks (6.5).

**6.5 Jank or drift with Lenis, pins and `position: fixed`.**
- `fixed` resolves against the nearest ancestor with `transform`, `translate`/`scale`/`rotate`, `filter`, **`backdrop-filter`**, `perspective`, `contain: layout|paint`, `will-change: transform|filter`, or `content-visibility: auto` ([MDN containing block](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_display/Containing_block)).
- A page-transition container animated with transform, a ScrollSmoother content wrapper, or a glass header with `backdrop-filter` will capture the nav, cursor, loader, WebGL canvas and even ScrollTrigger pins.
  - Keep fixed UI at `body` level.
  - `clearProps: 'transform'` after transitions.
  - Use `pinReparent: true` if a pin sits inside such an ancestor.
- Lenis documents lag of fixed elements on pre-M1 macOS Safari, and 60fps caps (30fps in Low Power Mode) on Safari.
- iOS toolbar resizes cause refresh jumps: `ScrollTrigger.config({ ignoreMobileResize: true })`, and size pinned stages in `svh`.
- Fast-scroll pin snap: `anticipatePin: 1`.
- Double lag: Lenis lerp plus `scrub: 1`. Use `scrub: true`.

**6.6 Reduced motion (check under `prefers-reduced-motion: reduce`).** Expected behaviour:
- Lenis is off or 1:1 (automatic in 1.3.26; guard older versions yourself).
- Every `gsap.matchMedia` no-preference branch reverted, so no hidden states remain.
- No scrubbed parallax, pins or horizontal hijack. The horizontal section falls back to a native scroller.
- View Transition pseudo-elements `animation: none`.
- Marquee static and scrollable.
- Cursor follower and magnet off.
- State changes (colour, focus, open/close) still happen, instantly or as ≤ 200ms crossfades.
- Autoplaying loops have controls.

Relevant criteria: WCAG 2.2.2 Pause, Stop, Hide (Level A) and 2.3.3 Animation from Interactions (AAA, [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)). Remember 94% of probed Lenis installs predate automatic reduced-motion support.

---

## 7. Anti-slop crosswalk (award habit → crafted alternative)

| Common award-site move | Why the law rejects it | Do this instead |
|---|---|---|
| Nav/link underline that grows, wipes or travels in on hover | "Do not animate underlines at all." A template tic. | Tonal colour step on hover (200ms, `--ease-out-soft`), or a small arrow or glyph sliding 4–6px. Inline body links keep a static underline for affordance. |
| Button lifts (`translateY`) or scales on hover | The hover boop. A button should not move on hover. | Tonal fill change. If "magnetic" is wanted, only the inner label drifts ≤ 6px (§4.9). Press is a darker tonal step, not a bounce. |
| Content at `opacity: 0` in CSS until a reveal fires (incl. `view()` reveals from 0, Motion `initial={{opacity:0}}`) | Invisible-content trap: blank sections when the reveal doesn't run | Visible by default. Lazy-armed JS reveals (§4.2), deadline-guarded intro (§4.3), readable 0% keyframes for `view()` (§4.4). Animate y and clip, not opacity to 0. |
| Card hover: lift, shadow bloom, glowing accent border | Card hover-lift is listed slop | Image scales 1.03–1.05 *inside* its clip over ~0.6s `--ease-out`; caption shifts a tonal step. The card box stays grounded. |
| Saturated accent on progress bars, cursor rings, hover fills | Saturated accent pop | Tonal accent: a lighter or darker, desaturated step off the surface or ink. |
| Cream or beige preloader and page backgrounds | Cream "editorial" is the new safe default | A specific brand surface. Preloader surface = the page surface, so the reveal reads as continuous. |
| Animated grain canvas fixed over the whole page, text included | Grain on top of content | Grain on the substrate only (behind content), or masked into one display word deliberately. |
| `back.out` / `elastic` pops on UI text and buttons | "Never bouncy" | `--ease-out` or `--ease-out-expo`. Keep overshoot for one illustrative object, if any. |
| Fake 0→100 preloader counter on a timer | Dead-control / fake-interactivity family | Honest weighted progress with a hard cap, or no preloader (§4.12). |
| `cursor: none` with a laggy blob replacing the pointer | Hurts precision; decoration posing as function | Native cursor plus decorative follower on fine pointers only (§4.10). |
| A fixed background animation trailing behind every section and the nav | "The fixed background that just follows the scroll" | Make the background respond to sections (colour or state per section via ScrollTrigger), or drop it as the signature. |
| Every section fades up the same way | Dead-looking and templated at once | One signature moment per viewport, quiet consistent entrances elsewhere, plus authored micro-interactions. |

---

## Sources (primary, fetched 2026-09-24)

- GSAP:
  - npm registry: https://registry.npmjs.org/gsap
  - blogs: [3.15](https://gsap.com/blog/3-15/), [3.14](https://gsap.com/blog/3-14/), [3.13](https://gsap.com/blog/3-13/)
  - [Standard license](https://gsap.com/community/standard-license/)
  - docs: [SplitText](https://gsap.com/docs/v3/Plugins/SplitText/), [ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/), [ScrollSmoother](https://gsap.com/docs/v3/Plugins/ScrollSmoother/), [Flip](https://gsap.com/docs/v3/Plugins/Flip/), [Observer](https://gsap.com/docs/v3/Plugins/Observer/), [CustomEase](https://gsap.com/docs/v3/Eases/CustomEase/), [Eases](https://gsap.com/docs/v3/Eases/), [matchMedia](https://gsap.com/docs/v3/GSAP/gsap.matchMedia()), [quickTo](https://gsap.com/docs/v3/GSAP/gsap.quickTo()), [context](https://gsap.com/docs/v3/GSAP/gsap.context())
  - [dist files](https://unpkg.com/gsap@3.15.0/dist/)
- Webflow: https://webflow.com/blog/gsap-becomes-free
- Lenis:
  - [README](https://github.com/darkroomengineering/lenis), [releases](https://github.com/darkroomengineering/lenis/releases), npm registry https://registry.npmjs.org/lenis
  - [1.3.26 source](https://unpkg.com/lenis@1.3.26/dist/lenis.mjs)
- Motion: [changelog](https://github.com/motiondivision/motion/blob/main/CHANGELOG.md), [scroll](https://motion.dev/docs/scroll), [inView](https://motion.dev/docs/inview), [hover](https://motion.dev/docs/hover), [animateView](https://motion.dev/docs/animate-view), [React accessibility](https://motion.dev/docs/react-accessibility), [Motion+](https://motion.dev/plus)
- Taxi: [docs](https://taxi.js.org/how-to-use/), [transitions](https://taxi.js.org/transitions/), [repo](https://github.com/craftedbygc/taxi)
- Swup: [changelog](https://github.com/swup/swup/blob/main/CHANGELOG.md), [options](https://swup.js.org/options/)
- Barba: [repo](https://github.com/barbajs/barba), [docs](https://barba.js.org/docs/advanced/transitions)
- Theatre.js: [repo](https://github.com/theatre-js/theatre)
- Browser support:
  - [webstatus.dev](https://webstatus.dev/) API
  - [MDN browser-compat-data](https://github.com/mdn/browser-compat-data) (main branch)
  - [caniuse data](https://github.com/Fyrd/caniuse) (data updated 2026-09-23)
  - [Chromium Dash schedule](https://chromiumdash.appspot.com/)
- Chrome for Developers: [cross-document view transitions](https://developer.chrome.com/docs/web-platform/view-transitions/cross-document), [scroll-driven animations](https://developer.chrome.com/docs/css-ui/scroll-driven-animations)
- MDN: [animation-timeline](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline), [timeline-range-name](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/timeline-range-name), [view-transition-name](https://developer.mozilla.org/en-US/docs/Web/CSS/view-transition-name), [containing block](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_display/Containing_block)
- W3C: [WAI-ARIA 1.2](https://www.w3.org/TR/wai-aria-1.2/#namefromprohibited), [WCAG 2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html), [WCAG 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)
- Easing values: [easings.net](https://easings.net/), [postcss-easings v2](https://unpkg.com/postcss-easings@2.0.0/index.js) (classic set)
- Observed data: Awwwards SOTD pages (e.g. https://www.awwwards.com/sites/seasats) through the skill corpus. Probe outputs are in `evidence/motion/`.

## Retrieval gaps

- **Static probe only.** Library detection used landing HTML plus ≤ 30 linked assets. Lazily loaded chunks, runtime-injected scripts and CSS-in-JS were not executed, so all "observed" percentages are lower bounds. Motion/Framer detection is heuristic. ScrollSmoother detection needed a count heuristic because ScrollTrigger embeds the string "ScrollSmoother" 3×. The ease-context census only sees ease literals in flat object literals (nested `scrollTrigger: {scrub}` objects were not parsed). 3 of 120 sites failed (404, 403, 429).
- **Motion+ price** is not stated here: the pricing page renders it client-side. Motion 13.4.4 appears in the changelog but was not on npm at check time.
- **Lenis 2.0** exists only as `2.0.0-dev.*` prereleases. Its API changes were not reviewed. The unit of Lenis `velocity` (px per frame) and the README's `direction` sign convention were not verified in source.
- **Same-document View Transition update-callback timeout** (relevant when a PJAX fetch runs inside `startViewTransition`) was not verified in the spec or Chrome docs. Only the 4s cross-document navigation timeout is documented.
- **LCP accounting of `clip-path`-hidden hero text** (deadline pattern §4.3) was not verified.
- **Sticky subjects and view timelines:** how a stuck `position: sticky` element's view progress behaves was not verified, so the CSS-only stacking-cards variant is deliberately omitted.
- **Theatre.js 1.0** private-repo status is only the README's claim, and it is undated. The health of the Encore fork was not assessed.
- Barba's GitHub releases list was not enumerated. "Dormant" rests on npm (2024-08-12) and last push (2024-12-02).
- Firefox's scroll-driven animations ship date is unknown. BCD marks them "preview" (Nightly) only.
- Firefox `pageswap`/`pagereveal` support was taken from BCD (`false`). It was not tested in a live browser.
