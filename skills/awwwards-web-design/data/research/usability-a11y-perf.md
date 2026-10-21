# Usability, accessibility and performance on award-level sites

Last updated: 2026-09-24

Scope: how Site-of-the-Day (SOTD) sites stay usable, accessible and fast (or fail to), and the rules the `awwwards-web-design` skill enforces when it builds. Audience: an agent that ships code. Every rule here sits under the house anti-slop law (`deslop-law.md`); where an award habit is a slop tell, section 6 says so and gives the crafted replacement.

Evidence base, in order of weight:
1. Normative specs and vendor docs, read live on 2026-09-24 (WCAG 2.2, WAI-ARIA 1.2, web.dev, MDN, webstatus.dev, library READMEs and source).
2. Our corpus: `data/corpus.jsonl` (732 Awwwards records), analysed with `evidence/a11y/dev_scores.py` (output in `dev_scores.out`).
3. A static probe of 60 live 2025-2026 Developer-Award SOTD homepages (`evidence/a11y/probe_static.py`, results in `probe_static.jsonl` and `probe_summary.txt`). This is "observed in use". Everything else is "documented".
4. Secondary write-ups (case studies, blogs), flagged as such.

---

## 1. What the dev scores say

### 1.1 How Awwwards scores engineering (documented)

- Main jury weights: Design 40%, Usability 30%, Creativity 20%, Content 10%. Honorable Mention needs 6.5+. Every SOTD goes to a developer jury and gets a Developer Award if it scores higher than 7 ([Awwwards evaluation](https://www.awwwards.com/about-evaluation/)).
- Developer jury categories and weights ([Developer Award guidelines, Google Doc linked from the evaluation page](https://docs.google.com/document/d/1Gvmg6Z60UQ-4BOM3XyUcBKvq2shd4J-l_MoXT26JFEg/edit)): WPO 0.20, RWD/Mobile 0.20, Semantics/SEO 0.20, Markup/Metadata 0.15, Animations/Transitions 0.15, Accessibility 0.10.
- The doc's revision line is still "v0.7 - 14/12/2016". A banner announces a Q1 revision by named studio developers but gives no year, and no revised version was reachable (see Retrieval gaps). Several checklist items are dated (YSlow, "No iframes", "Avoid filters", keyword meta tags). Treat the doc as a floor. Our real bar is WCAG 2.2 AA plus Core Web Vitals.
- Checklist items that still matter and that award sites commonly break (paraphrased, same source): content must work without CSS and without JS; auto-starting animation longer than 5 s needs pause controls; no relevant information may live only on hover; browser history (back, forward, refresh) must work; tap targets must be adequately sized; frame rate must be smooth and stable; GPU work must be tested for garbage collection, GLSL cost, asset management and memory leaks.
- Mobile Excellence: launched with Google in 2017 at a 75/100 pass mark ([announcement](https://www.awwwards.com/google-and-awwwards-present-the-mobile-excellence-award.html)), lowered to 70/100 in v2 in 2018 ([v2 update](https://www.awwwards.com/update-version-2-of-the-google-awwwards-mobile-excellence-award.html)). Its [checklist PDF](https://www.awwwards.com/mobile-excellence-guidelines.pdf) uses retired metrics (First Meaningful Paint, Estimated Input Latency). None of the 732 corpus pages carried a MOB badge, so whether the award is still given is (unverified).

### 1.2 The sample, and its bias

- 732 records, 360 SOTDs with jury scores, 308 with a full six-part dev breakdown.
- The dev breakdown is printed only on pages that carry the "DEV AWARD" block. A 2026 SOTD without a Developer Award (`21-hrs-on-the-moon`) has no dev block; one with the award (`20-years-inspired-by-people`) has it (checked in the cached HTML). So the 308 are Developer Award winners, and 99.0% of them score above 7.0 overall.
- Read every number below as the best-engineered slice of award sites. The rest of the field is worse.

### 1.3 Per-aspect distribution (n = 308 Developer Award SOTDs)

| Aspect (weight) | Mean | Median | SD | P10 | P90 | Share below 7.0 | Weakest aspect on | Strongest aspect on |
|---|---|---|---|---|---|---|---|---|
| Accessibility (0.10) | **6.93** | 6.80 | 0.54 | 6.40 | 7.60 | **51.0%** | **71%** of sites | 3% |
| Markup (0.15) | 7.22 | 7.20 | 0.46 | 6.67 | 7.80 | 21.1% | 23% | 2% |
| Semantics/SEO (0.20) | 7.27 | 7.33 | 0.46 | 6.80 | 7.80 | 18.2% | 17% | 4% |
| WPO (0.20) | 7.54 | 7.60 | 0.50 | 7.00 | 8.20 | 9.4% | 10% | 18% |
| Responsive (0.20) | 7.60 | 7.60 | 0.56 | 7.00 | 8.33 | 5.5% | 6% | 19% |
| Animations (0.15) | **8.10** | 8.00 | 0.68 | 7.29 | 9.00 | 2.3% | 2% | **73%** |

Ties count for each aspect, so the weakest/strongest columns sum above 100%.

What this says:
1. **Accessibility is the lowest dev aspect and animation the highest, even among winners.** The mean gap is +1.18 points (median +1.20). Animation beats accessibility on 93% of sites and by 1.5 points or more on 33%. Only 4.2% score 8.0+ on accessibility; 17.1% score 6.5 or less.
2. **The weights are still live (inferred).** `dev_overall` matches the published weighted sum with a mean absolute residual of 0.032, against 0.058 for a plain mean.
3. **The flat line.** Mean accessibility has sat between 6.66 and 7.14 every year from 2017 to 2026 (2026: 6.81, n = 168). Nothing in the award ecosystem is pulling it up.

### 1.4 What the main jury rewards (correlations)

Pearson r / Spearman rho between each dev aspect and the jury scores (n = 308):

| Dev aspect | vs jury overall | vs jury usability | vs dev_overall |
|---|---|---|---|
| Animations | **+0.36 / +0.38** | +0.20 / +0.22 | +0.54 / +0.60 |
| Responsive | +0.27 / +0.32 | +0.27 / +0.31 | +0.38 / +0.51 |
| Accessibility | +0.17 / +0.16 | +0.18 / +0.20 | +0.60 / +0.55 |
| Markup | +0.11 / +0.10 | +0.07 / +0.07 | +0.67 / +0.65 |
| WPO | +0.10 / +0.10 | +0.09 / +0.10 | +0.52 / +0.59 |
| Semantics/SEO | +0.05 / +0.13 | +0.04 / +0.13 | +0.46 / +0.56 |

`dev_overall` vs jury overall: r = +0.40.

Also from the corpus:
- **The jury sees motion and responsive polish, and barely sees accessibility or performance.** An award is no evidence that a site is accessible or fast. The skill has to enforce both on its own.
- **Accessibility is not traded against motion; it is ignored.** Accessibility correlates with animations at +0.03 and with WPO at +0.02. Its only real partner is markup (+0.43). Good motion and good accessibility come from separate decisions, so doing both costs nothing structural.
- **Motion quality and performance travel together.** Animations correlates with WPO at +0.47, the strongest pair among the six aspects. The best animators ship the smoothest, lightest code.
- **3D does not cost engineering points among winners.** The 185 sites tagged 3D/WebGL/Three.js/R3F average WPO 7.54 vs 7.55 for the rest, and accessibility 6.98 vs 6.85. Webflow sites (38) trail on animations (7.74 vs 8.16) and WPO (7.33 vs 7.57).
- **Usability is the jury's weakest criterion too.** Across all 360 jury-scored SOTDs, usability averages 7.33, against 7.71 design, 7.83 creativity and 7.67 content. It is the lowest of the four on 83% of them, and it correlates +0.66 with design (a halo).
- Engineering exemplars (3D-tagged, highest WPO + accessibility): [Apple AirPods Pro](https://www.awwwards.com/sites/apple-airpods-pro) (WPO 8.67 / a11y 8.33), [Messenger by Abeto](https://www.awwwards.com/sites/messenger) (8.8 / 7.6), [Lusion v3](https://www.awwwards.com/sites/lusion-v3) (9.0 / 7.4, animations 10.0), [Umami Land](https://www.awwwards.com/sites/umami-land) (8.33 / 7.67).

### 1.5 What winners actually ship (static probe, observed)

We fetched the homepage HTML, up to 4 stylesheets and up to 3 script bundles for 60 Developer-Award SOTDs from 2025-2026 (every third of the 181 in the corpus, ordered by slug; 60/60 fetched; 58 with CSS). No JS was executed, so this is what crawlers, no-JS users and the first paint get. CSS and JS figures are lower bounds, because code-split bundles were not all fetched.

| Signal | Result | Why it matters |
|---|---|---|
| `<html lang>` present | 55/60 (92%) | 3.1.1 language of page |
| Viewport meta blocks zoom (`user-scalable=no` / `maximum-scale=1`) | **6/60 (10%)** | 1.4.4 resize text |
| `<h1>` in server HTML | 45/60 (75%) | semantics, SEO, SR navigation |
| `<main>` landmark | 48/60 (80%) | landmarks |
| Skip link to main | **1/60 (2%)** | 2.4.1 bypass blocks |
| Server HTML with under 200 chars of visible text (JS-only content) | 8/60 (13%) | no-JS, crawlers, LCP |
| `prefers-reduced-motion` in CSS or inline HTML | 19/58 (33%) | 2.3.3, vestibular safety |
| `prefers-reduced-motion` in CSS or fetched JS | **27/60 (45%)** | same |
| Lenis present (HTML/CSS/JS) | 34/60 (57%) | smooth scroll prevalence |
| Lenis present and no reduced-motion string anywhere | **18/60 (30%)** | smooth scroll likely forced on everyone (heuristic) |
| `:focus-visible` used | 28/58 (48%) | 2.4.7 |
| `outline: none/0` somewhere | 38/58 (66%) | the usual 2.4.7 break |
| `cursor: none` (native cursor hidden) | **10/58 (17%)** | low-vision cursor settings ignored |
| `scroll-padding` / `scroll-margin` | 14/58 (24%) | 2.4.11 under sticky headers |
| `font-size: <n>vw` | 21/58 (36%) | 1.4.4 zoom risk |
| `dvh/svh/lvh` units | 48/58 (83%) | mobile viewport correctness |
| `(hover: hover)` / `(pointer: …)` queries | 34/58 (59%) | hover effects gated by input type |
| `font-display: swap` | 53/58 (91%) | flash of fallback, CLS risk |
| Metric-matched fallback (`@font-face` `size-adjust` / `ascent-override`) | 11/58 (19%) each | the CLS fix most skip |
| `fetchpriority="high"` in HTML | 13/60 (22%) | LCP resource priority |
| Font preload | 15/60 (25%) | text LCP |
| AVIF referenced / WebP referenced | 9/60 (15%) / 32/60 (53%) | bytes |
| `<canvas>` in server HTML | 25/60 (42%) | WebGL prevalence |
| `<img>` with `alt` attribute | 2,488/2,842 (88%) | presence only, not quality |
| `<img>` with `width`+`height` | 1,344/2,842 (47%) | CLS |
| `<img loading="lazy">` / with `srcset` | 1,323 (47%) / 755 (27%) | bytes |
| `<video>`: autoplay / playsinline / poster | 154 (62%) / 244 (98%) / **37 (15%)** of 250 | 2.2.2, LCP, blank frames |
| `animation-timeline` / `view-transition` in CSS | 1/58 (2%) / 5/58 (9%) | modern CSS still rare |

Among these 60, the dev jury's accessibility mean did not differ with reduced-motion support (6.83 with, 6.83 without; n = 19 vs 39). The dev score does not track this, so the skill must.

---

## 2. Non-negotiable checklist (the gate)

The skill ships nothing that fails a line here. Each line is testable. "SC" means a WCAG 2.2 success criterion from the [W3C Recommendation of 12 December 2024](https://www.w3.org/TR/WCAG22/).

### A. Content exists without motion or JS
- [ ] All text, links and controls are in server HTML and readable with JS disabled. The Awwwards dev checklist asks for this too, and 13% of probed winners fail it.
- [ ] No content element has an authored initial state of `opacity: 0`, `visibility: hidden`, `clip-path` fully closed, or translated out of a clip, waiting for JS to undo it. Hidden "from" states may exist only under `:root[data-motion="full"]` (set by script) and must have a failsafe (recipe 3.2). House law: content is visible by default.
- [ ] The LCP element (hero heading or poster) is never faded from 0, never lazy-loaded and never behind a preloader. Chromium drops `opacity: 0` elements from LCP candidacy ([web.dev LCP](https://web.dev/articles/lcp)). Shopify documents the mechanism ([Shopify dev docs](https://shopify.dev/docs/storefronts/themes/best-practices/performance/dont-hide-lcp-image-behind-animations)), and a Shopify performance-team case study (Case-Mate) found an opacity reveal delaying LCP by about 6 s ([case summary](https://seoprocheck.com/case-studies/web-performance/improve-largest-contentful-paint-lcp-by-removing-image-trans/)). web.dev warns never to lazy-load the LCP image ([optimize LCP](https://web.dev/articles/optimize-lcp)).
- [ ] WebGL/canvas never holds the only copy of any text, heading or control. Canvas is decoration over or beside DOM content.

### B. Motion
- [ ] `prefers-reduced-motion` is honored by CSS, GSAP, the smooth-scroll library, WebGL and video (recipe 3.1). "Reduce" means remove or replace movement (translate, scale, rotate, parallax, scroll-linked transforms, camera drift, smooth-scroll inertia) and keep opacity/color state feedback. MDN defines the preference as a request to remove, reduce or replace motion-based animation ([MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)). WebKit lists the triggers: scaling/zooming, spinning/vortex, multi-speed or multi-directional movement (parallax), plane shifting (2.5D), and peripheral motion near text ([WebKit, Responsive Design for Motion](https://webkit.org/blog/7551/responsive-design-for-motion/)). The feature has been Baseline since January 2020 (MDN).
- [ ] Motion-heavy sites also expose an in-page motion toggle, persisted per viewer. GSAP's accessibility guide recommends one because not everyone who is affected knows the OS setting ([GSAP a11y](https://gsap.com/resources/a11y/)). Understanding SC 2.3.3 (AAA) lists a user control that turns off non-essential animation as one valid solution, next to honoring the OS setting ([Understanding 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)).
- [ ] Anything that moves on its own for more than 5 s alongside other content (marquee, background video, auto-carousel, ambient canvas next to text) has a visible pause/stop control, whatever the motion preference. That is SC 2.2.2 (A), and the Awwwards dev checklist repeats it. Treating ambient WebGL near text as in scope is our conservative reading (see gaps).
- [ ] Nothing flashes more than 3 times in any one second (SC 2.3.1, A). Watch glitch, strobe and RGB-split transitions.
- [ ] No scroll-jacking. Scroll speed and direction stay native (in NN/g usability testing, scroll-jacking disoriented and frustrated most participants, worst when text changed while the scroll rate was altered, and worse on mobile ([NN/g](https://www.nngroup.com/articles/scrolljacking-101/))). House rule: at most one vertical-to-horizontal pinned section per page, desktop only, no body copy inside it, with the nav reachable.
- [ ] Scroll-triggered reveals play once and never replay on scroll-up. NN/g recommends scroll-triggered effects fire only on the first pass down the page ([NN/g scroll animations](https://www.nngroup.com/articles/scroll-animations/)). Reveals apply to secondary content, never main body text (same source). House duration cap: 0.7 s per element, 1.2 s for a staggered group.

### C. Keyboard and focus
- [ ] Everything is operable by keyboard (SC 2.1.1, A) with no traps (SC 2.1.2, A) and a meaningful focus order (SC 2.4.3, A). No positive `tabindex` (0/60 probed sites used one: keep it that way).
- [ ] Focus is visible (SC 2.4.7, AA) through `:focus-visible` ([W3C technique C45](https://www.w3.org/WAI/WCAG22/Techniques/css/C45)). House spec meets SC 2.4.13 (AAA): the indicator covers at least a 2 CSS px perimeter and changes contrast by at least 3:1. Never remove `outline` without a replacement; 66% of probed winners have `outline: none/0` somewhere.
- [ ] Focus is never fully hidden under a sticky header, cookie bar or footer (SC 2.4.11, AA). Fix: `scroll-padding-top`/`bottom` equal to the sticky element's size ([technique C43](https://www.w3.org/WAI/WCAG22/Techniques/css/C43)). Understanding 2.4.11 calls out cookie banners and sticky headers by name ([Understanding 2.4.11](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html)). Only 24% of probed sites set scroll padding or margin.
- [ ] A skip link to `#main` is the first focusable element (SC 2.4.1, A). 1/60 winners had one.
- [ ] Custom widgets expose role, name and state. Modals use `<dialog>` with `showModal()` or make the background `inert` (both Baseline widely available per [webstatus.dev dialog](https://webstatus.dev/features/dialog) and [inert](https://webstatus.dev/features/inert)), pause smooth scroll while open, close on Esc and return focus to the trigger.

### D. Contrast, color and legibility
- [ ] Text contrast is at least 4.5:1. Large text (at least 18 pt / 24 CSS px, or 14 pt / about 18.66 CSS px bold) needs 3:1 (SC 1.4.3, AA; "large scale" definition in WCAG 2.2). Over photos, video or WebGL, measure the worst frame behind the text, not the average.
- [ ] UI component boundaries, states, focus indicators and meaningful graphics reach 3:1 against adjacent colors (SC 1.4.11, AA).
- [ ] Color is never the only cue (SC 1.4.1, A). Links inside body copy keep a static underline or another non-color cue.
- [ ] Text reaches 200% with browser zoom (SC 1.4.4, AA). Never block zoom in the viewport meta (10% of winners do). Fluid type never uses bare `vw`. With `clamp(min, calc(rem + vw), max)`, keep max at or below 2.5 × min ([Smashing, Barvian 2023](https://www.smashingmagazine.com/2023/11/addressing-accessibility-concerns-fluid-type/); background in [Roselli, Responsive Type and Zoom](https://adrianroselli.com/2019/12/responsive-type-and-zoom.html)). 36% of winners set `font-size` in `vw` somewhere.
- [ ] Content reflows at 320 CSS px without two-dimensional scrolling (SC 1.4.10, AA), and user text-spacing overrides (line-height 1.5, letter-spacing 0.12em, word-spacing 0.16em, paragraph spacing 2em) lose nothing (SC 1.4.12, AA). So no fixed-height text boxes, including SplitText line masks after they finish (revert them).
- [ ] No information only on hover (Awwwards dev checklist). Content that appears on hover or focus is dismissible, hoverable and persistent (SC 1.4.13, AA).

### E. Pointer and touch
- [ ] Targets are at least 24×24 CSS px, or meet the spacing exception (SC 2.5.8, AA). House: 44×44 for primary nav, CTAs and media controls (the SC 2.5.5 AAA size).
- [ ] Every drag interaction (drag carousel, orbit control, before/after slider) has a single-pointer alternative such as buttons or arrow keys (SC 2.5.7, AA).
- [ ] The native cursor is never hidden. A decorative follower is allowed only under `(hover: hover) and (pointer: fine)` with full motion, and must be `aria-hidden` and `pointer-events: none` (recipe 3.9).

### F. Scroll and navigation
- [ ] Native scroll mechanics survive: keyboard scrolling, find-in-page, anchor links with `scroll-margin-top`, scrollbar drag, back/forward restoration. Smooth scroll is a wrapper over native scroll (Lenis, GSAP ScrollSmoother), never a transform-driven virtual scroller (recipe 3.4).
- [ ] Client-side page transitions update `document.title`, move focus to the new page's `<h1>` or `<main>`, and restore scroll position on Back.

### G. Performance budgets
Official thresholds, measured at the 75th percentile of page loads, mobile and desktop separately. All three must pass ([web.dev Web Vitals](https://web.dev/articles/vitals), last updated 2024-10-31):

| Metric | Good | Poor | Source |
|---|---|---|---|
| LCP | ≤ 2.5 s | > 4.0 s | [web.dev LCP](https://web.dev/articles/lcp) (updated 2025-09-04) |
| INP | ≤ 200 ms | > 500 ms | [web.dev INP](https://web.dev/articles/inp) (updated 2025-09-02); replaced FID |
| CLS | ≤ 0.1 | > 0.25 | [web.dev CLS](https://web.dev/articles/cls) |

House build gates (our choices, not standards):
- The LCP element renders with JS disabled. No LCP path depends on hydration, GSAP or three.js.
- Exactly one `fetchpriority="high"` image, the likely LCP image. web.dev notes that marking more than one or two images high cancels the benefit ([web.dev optimize LCP](https://web.dev/articles/optimize-lcp)).
- No synchronous `<script>` in `<head>` except the tiny inline motion/theme gate. Motion libraries load `defer`/module. The three.js chunk loads after `load` + idle.
- At most two preloaded font files, WOFF2, subset, with a metric-matched fallback (recipe 3.7).
- Every `img`, `video`, `canvas` and embed reserves its box with `width`/`height` or `aspect-ratio` ([web.dev optimize CLS](https://web.dev/articles/optimize-cls)). 53% of images on winning homepages do not.
- Animate only `transform`, `opacity` and `filter` on the compositor. Layout-property animation is flagged by Lighthouse's [non-composited animations audit](https://developer.chrome.com/docs/lighthouse/performance/non-composited-animations).
- WebGL: device-pixel-ratio cap 2 (1.5 on the lite tier), render loop stopped off-screen, shaders compiled before the first visible frame (recipe 3.5).
- No main-thread task over 200 ms after first paint from our own code. Split work, and yield with `scheduler.yield()` where it exists: Chrome 129 and Firefox 142, not Safari ([MDN BCD](https://github.com/mdn/browser-compat-data/blob/main/api/Scheduler.json)). Otherwise fall back to the `requestAnimationFrame` + `setTimeout` pattern ([web.dev optimize INP](https://web.dev/articles/optimize-inp)).

### H. Semantics (35% of the dev score with markup)
- [ ] `lang`, unique `<title>`, meta description, one `<h1>`, landmarks (`header`, `nav`, `main`, `footer`), Open Graph tags, a descriptive `alt` or `alt=""` on every image, valid HTML, real `<a href>` links for navigation, `<button>` for actions.

---

## 3. Recipes

### 3.1 Reduced-motion architecture (CSS + GSAP matchMedia + libraries)

Principle: **no-motion first.** The authored CSS is the final, static state. Motion is added only when (a) JS runs and (b) the viewer's effective preference is "full". This follows the no-motion-first approach ([Tatiana Mac](https://www.tatianamac.com/posts/prefers-reduced-motion); [W3C technique C39](https://www.w3.org/WAI/WCAG22/Techniques/css/C39)). Without JS, a viewer gets no motion and all content.

**Step 1: the gate.** Inline in `<head>`, before any stylesheet. It hides nothing.

```html
<script>
  (() => {
    const root = document.documentElement;
    let saved = null;
    try { saved = localStorage.getItem('motion'); } catch (e) {} // private mode can throw
    const osReduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    root.dataset.motion = saved === 'reduce' || saved === 'full' ? saved : (osReduce ? 'reduce' : 'full');
  })();
</script>
```

**Step 2: CSS.** Every movement rule is scoped to `[data-motion="full"]`. A safety net catches anything that slipped out and keeps color and opacity feedback.

```css
/* base.css: static final state for everyone */
.marquee__track { display: flex; gap: 4rem; }

/* motion rules exist only under the gate */
:root[data-motion="full"] .marquee__track { animation: marquee 40s linear infinite; }
:root[data-motion="full"] .marquee[data-paused="true"] .marquee__track { animation-play-state: paused; }
@keyframes marquee { to { transform: translateX(-50%); } }

/* safety net: reduce means no movement, feedback stays */
:root[data-motion="reduce"] *,
:root[data-motion="reduce"] *::before,
:root[data-motion="reduce"] *::after {
  animation-duration: 0.01ms !important;
  animation-iteration-count: 1 !important;
  transition-property: opacity, color, background-color, border-color, outline-color, box-shadow !important;
  scroll-behavior: auto !important;
}
```

Optional bandwidth saver: move motion-only CSS into a file loaded with `media="(prefers-reduced-motion: no-preference)"` (Tatiana Mac, above). Caveat: an in-page toggle cannot re-enable a stylesheet the OS setting kept from loading, so scope its rules to `[data-motion="full"]` as well.

**Step 3: JS motion under `gsap.matchMedia()`.** GSAP 3.15.0 is current on npm (2026-04-13). All of GSAP, SplitText included, has been free for commercial use under Webflow's "no charge" license since 2025-04-30. The one prohibition is using it in visual animation builders that compete with Webflow ([GSAP standard license](https://gsap.com/standard-license/)). `matchMedia()` reverts every tween and ScrollTrigger made inside a handler when its conditions change. With the conditions syntax, the handler runs when *any* condition matches ([gsap.matchMedia docs](https://gsap.com/docs/v3/GSAP/gsap.matchMedia())). Listing both preferences guarantees a run and a live re-run when the OS setting flips.

```js
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { pending, setupReveals } from './reveals.js'; // recipe 3.2
gsap.registerPlugin(ScrollTrigger);

let mm = gsap.matchMedia();

function setupMotion() {
  mm.add(
    {
      osFull: '(prefers-reduced-motion: no-preference)',
      osReduce: '(prefers-reduced-motion: reduce)',
      finePointer: '(hover: hover) and (pointer: fine)',
      wide: '(min-width: 64em)',
    },
    (ctx) => {
      const { osReduce, finePointer, wide } = ctx.conditions;
      const root = document.documentElement;
      let saved = null;
      try { saved = localStorage.getItem('motion'); } catch (e) {}
      const next = saved || (osReduce ? 'reduce' : 'full');           // follow live OS changes unless the viewer chose
      if (root.dataset.motion !== next) {
        root.dataset.motion = next;
        dispatchEvent(new CustomEvent('motionchange', { detail: next })); // Lenis, WebGL, video listen
      }
      if (root.dataset.motion !== 'full') {
        // Reduced: no transforms, no parallax, no scroll-linked motion.
        // Content is already visible; optionally add short opacity crossfades for state changes.
        return;
      }
      setupReveals();                 // recipe 3.2
      setupSplitHeadings();           // recipe 3.3
      if (wide) setupPinnedChapter(); // desktop-only set pieces
      const offCursor = finePointer ? setupCursorFollower() : null; // recipe 3.9
      return () => {                  // GSAP objects revert automatically; clean up the rest
        pending.clear();
        offCursor && offCursor();
      };
    }
  );
}
setupMotion();

// In-page toggle: <button data-motion-toggle aria-pressed="false">Reduce motion</button> (constant label; pressed = reduced)
document.querySelector('[data-motion-toggle]')?.addEventListener('click', (e) => {
  const root = document.documentElement;
  const next = root.dataset.motion === 'full' ? 'reduce' : 'full';
  root.dataset.motion = next;
  e.currentTarget.setAttribute('aria-pressed', String(next === 'reduce'));
  try { localStorage.setItem('motion', next); } catch (err) {}
  mm.revert();                // tears down every tween/ScrollTrigger from the handler
  mm = gsap.matchMedia();
  setupMotion();
  window.dispatchEvent(new CustomEvent('motionchange', { detail: next })); // Lenis, WebGL, video listen
});
```

**Step 4: every other moving system subscribes to the same flag.**

| System | Full | Reduce |
|---|---|---|
| Smooth scroll (Lenis) | on (recipe 3.4) | Lenis ≥ 1.3.26 honors the OS preference by default (`respectReducedMotion: true`: `lerp` forced to 1, instant `scrollTo`) ([Lenis README](https://github.com/darkroomengineering/lenis)). That arrived in [v1.3.26 on 2026-08-05](https://github.com/darkroomengineering/lenis/releases/tag/v1.3.26), so older installs do not; we also skip init when `data-motion="reduce"`, which covers the in-page toggle |
| CSS `scroll-behavior: smooth` | only if no Lenis | `auto` |
| WebGL hero | animated scene | poster only, or a single rendered still frame; no camera drift, no pointer parallax |
| Background/hero video | plays in view, with pause button | no autoplay; poster shows; a play button is offered |
| Marquee/ticker | runs, with pause button | static row |
| Hover micro-interactions | transform + color | color/opacity only |
| Page transitions | wipe/slide | instant, or a ≤ 200 ms crossfade |

### 3.2 Reveals without the invisible-content trap

House law: never gate text on an animation finishing. Award sites often use `autoAlpha: 0` / `opacity: 0` reveals (even GSAP's own docs examples use `autoAlpha: 0` ([SplitText docs](https://gsap.com/docs/v3/Plugins/SplitText/))). That is a slop tell and an LCP bug. The crafted version is a **settle** (a small transform on already-visible content) plus a failsafe.

```js
// reveals.js: below-the-fold only. The hero and the LCP element never use this.
// Every tween that starts from a displaced or clipped state registers here (3.3 uses it too).
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

export const pending = new Set();

const flush = () => pending.forEach((t) => {
  const trg = t.scrollTrigger && t.scrollTrigger.trigger;
  if (!trg || trg.getBoundingClientRect().top < innerHeight) { t.progress(1); pending.delete(t); }
});
// Failsafe, installed once: throttled tabs, anchor jumps, restored scroll, screenshots, print.
const armFailsafe = () => setTimeout(flush, 3000);
if (document.readyState === 'complete') armFailsafe();
else addEventListener('load', armFailsafe, { once: true });
addEventListener('scrollend', flush);   // Baseline newly available 2025-12 (webstatus.dev); harmless elsewhere
addEventListener('beforeprint', () => pending.forEach((t) => t.progress(1)));

export function setupReveals(root = document) {
  root.querySelectorAll('[data-reveal]').forEach((el) => {
    if (el.getBoundingClientRect().top < innerHeight) return; // on screen (or above) at init: leave it alone
    const tween = gsap.from(el, {
      y: 28,               // settle, not appear: no opacity 0, no autoAlpha
      duration: 0.6,
      ease: 'power3.out',
      scrollTrigger: { trigger: el, start: 'top 90%', once: true },
      onComplete: () => pending.delete(tween),
    });
    pending.add(tween);
  });
  armFailsafe(); // re-arm after a motion toggle re-runs setup
}
```

If a design truly needs a masked line-rise (text starts clipped), it is allowed only below the fold, only under `data-motion="full"`, and only when registered with the same failsafe. For above-the-fold motion with an entrance feel, use CSS `@keyframes` that start on first render with opacity above 0. A keyframe animation begins at the element's first render, so the element becomes an LCP candidate immediately ([Shopify dev docs](https://shopify.dev/docs/storefronts/themes/best-practices/performance/dont-hide-lcp-image-behind-animations)). Starting at a non-zero opacity keeps first-paint LCP candidacy ([DebugBear](https://www.debugbear.com/blog/opacity-animation-poor-lcp)). Verify the LCP time with and without motion (section 7).

### 3.3 Accessible SplitText

Facts (from [GSAP SplitText docs](https://gsap.com/docs/v3/Plugins/SplitText/)): v3.13.0 was a major rewrite. By default (`aria: "auto"`) it puts `aria-label` on the split element and `aria-hidden` on the generated line/word/char elements. `autoSplit: true` re-splits when fonts load or width changes, and animations must be created and returned inside `onSplit()`. `mask: "lines" | "words" | "chars"` adds a clipping wrapper. `revert()` restores the original DOM. The docs warn: split only what you animate (chars are expensive), avoid `text-wrap: balance` on split elements, set `font-kerning: none` if characters shift, and SplitText does not work on SVG `<text>`.

The trap the docs do not stress: WAI-ARIA 1.2 **prohibits naming** the `generic`, `paragraph`, `caption`, `code`, `emphasis`, `strong`, `deletion`, `insertion`, `subscript`, `superscript` and `presentation` roles ([WAI-ARIA 1.2 §5.2.8.6](https://www.w3.org/TR/wai-aria-1.2/#namefromprohibited)). `aria: "auto"` on a `<p>`, `<div>` or `<span>` therefore puts an `aria-label` where authors must not, with every child `aria-hidden`. How screen readers treat that varies (unverified per AT), and text can go silent.

Rules:
1. Split only **headings** (`h1`-`h6` accept a name) with the default `aria: "auto"`.
2. Never split text that contains links, buttons or other interactive children. A screen-reader-only duplicate creates focusable ghosts with no visible focus, which fails SC 2.4.7.
3. For a non-heading text block with no interactive children, use `aria: "hidden"` on the visual copy plus a visually-hidden plain copy. The docs' option table recommends `"hidden"` with a duplicate; a later paragraph says `"none"`. `"hidden"` is the one that avoids double reading.
4. Split `lines` or `words,lines`. Use chars only with `smartWrap: true` and only for short display lines.
5. Under reduced motion, do not split at all.
6. Revert after the animation, which restores selection, find-in-page matching, translation and text-spacing behavior.

```js
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { SplitText } from 'gsap/SplitText';
import { pending } from './reveals.js'; // shared failsafe from 3.2
gsap.registerPlugin(SplitText, ScrollTrigger);

function setupSplitHeadings() {
  gsap.utils.toArray('h2[data-split], h3[data-split]').forEach((heading) => {
    if (heading.querySelector('a, button, input, select, textarea')) return; // rule 2
    if (heading.getBoundingClientRect().top < innerHeight) return;         // visible at load: static
    SplitText.create(heading, {
      type: 'lines',
      mask: 'lines',
      autoSplit: true,   // re-split after fonts load: no mis-broken lines
      aria: 'auto',      // valid because headings accept aria-label
      onSplit(self) {
        const tween = gsap.from(self.lines, {
          yPercent: 100,
          duration: 0.7,
          ease: 'expo.out',
          stagger: 0.06,
          scrollTrigger: { trigger: heading, start: 'top 85%', once: true },
          onComplete: () => { pending.delete(tween); self.revert(); },
        });
        pending.add(tween); // same failsafe as 3.2, because masked lines start clipped
        return tween;        // returned tweens are cleaned up and time-synced on re-split
      },
    });
  });
}
```

```css
.visually-hidden {
  position: absolute !important; width: 1px; height: 1px; margin: -1px; padding: 0;
  overflow: hidden; clip-path: inset(50%); white-space: nowrap; border: 0;
}
```

### 3.4 Smooth scroll that keeps keyboard, anchors, find-in-page and history

Why Lenis: it wraps the browser's own scroll instead of replacing it, so `position: sticky`, anchor links and accessibility features keep working ([Lenis README](https://github.com/darkroomengineering/lenis); `lenis@1.3.26`, MIT, npm 2026-08-05). The core source registers no keyboard listener, so arrow, Space and PageDown scrolling stay native and Lenis syncs through the native `scroll` event ([lenis.ts](https://github.com/darkroomengineering/lenis/blob/main/packages/core/src/lenis.ts), checked 2026-09-24). Defaults smooth only wheel input (`smoothWheel: true`, `syncTouch: false`), so touch scrolling stays native.

Contrast: Locomotive Scroll v4 (transform-driven) admitted that with it, Ctrl/Cmd+F counts matches but cannot scroll the page to them ([Locomotive, 2022](https://medium.com/@LocomotiveMTL/should-i-use-locomotive-scroll-on-my-project-7fc8fa38bcc5)). v5 is rebuilt on Lenis with a native scrollbar ([Locomotive Scroll docs](https://scroll.locomotive.ca/docs/)). GSAP ScrollSmoother also keeps native scroll and the real scrollbar, applying transforms to a content wrapper. Fixed elements must sit outside that wrapper, and touch smoothing is off by default ([ScrollSmoother docs](https://gsap.com/docs/v3/Plugins/ScrollSmoother/)).

```js
// same module as 3.1 (gsap and ScrollTrigger already imported and registered)
import Lenis from 'lenis';
import 'lenis/dist/lenis.css'; // recommended CSS: nested-scroll containment, stopped state, iframe handling

let lenis = null;
gsap.ticker.add((time) => { if (lenis) lenis.raf(time * 1000); }); // one rAF loop, added once
gsap.ticker.lagSmoothing(0);

function startLenis() {
  if (document.documentElement.dataset.motion !== 'full') return; // reduced: stay native
  lenis = new Lenis({
    anchors: true,               // default false: without it Lenis blocks anchor links during scroll
    stopInertiaOnNavigate: true, // stop inertia when an internal link is clicked
    allowNestedScroll: true,     // simplest nested-scroll fix; costs a DOM walk per event
    // smoothWheel: true, syncTouch: false (defaults): touch stays native
  });
  lenis.on('scroll', ScrollTrigger.update);
}
startLenis();
addEventListener('motionchange', () => { lenis?.destroy(); lenis = null; startLenis(); });
```

```css
:root { --header-h: 4.5rem; }
html { scroll-padding-top: var(--header-h); } /* SC 2.4.11: focus and anchor targets clear the sticky header */
:target, [id] { scroll-margin-top: var(--header-h); }
```

What the source shows about anchors: the click handler does not call `preventDefault`, so the URL hash updates natively, and `scrollTo` accounts for the target's `scroll-margin-top` and the container's `scroll-padding-top` (lenis.ts, above). Still move focus for skip links, so the next Tab continues from the target:

```js
document.querySelector('.skip-link')?.addEventListener('click', () => {
  const main = document.getElementById('main');
  main.setAttribute('tabindex', '-1');
  main.focus({ preventScroll: true }); // Lenis or native anchor handles the scroll
});
```

Modals and nested scrollers: call `lenis.stop()` on open and `lenis.start()` on close (the recommended CSS applies `overflow: clip` when stopped). Put `data-lenis-prevent` on any scrollable panel; it is cheaper than `allowNestedScroll` (README). Documented limits: no CSS scroll-snap (use `lenis/snap`), capped at 60 fps on Safari and 30 fps in Low Power Mode, no smoothing over iframes (README "Limitations").

Scroll restoration: leave `history.scrollRestoration` at `"auto"` for full page loads. With `"manual"`, the browser does not restore the position and the user has to scroll back by hand ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/History/scrollRestoration)). Award sites often set it to force every visit to start at the top, which breaks Back. If a client-side router must own scroll, store `scrollY` per history entry, restore it on `popstate` with `lenis.scrollTo(y, { immediate: true })`, and scroll to top only on forward navigation.

Find-in-page and hidden content: collapsed panels (accordions, "read more") should use `hidden="until-found"`, whose content stays reachable by find-in-page and fragment navigation ([MDN hidden](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/hidden)). Support is limited: Chromium 102+ and Firefox 148+, not Safari ([webstatus.dev](https://webstatus.dev/features/hidden-until-found)). Treat it as enhancement over `<details>`.

### 3.5 WebGL hero: poster, then lazy init, then fade

Facts that shape this:
- LCP candidates are `<img>`, `<image>` inside SVG, `<video>` (poster load or first frame, whichever is earlier), `url()` background images and block-level text. `<canvas>` is not on the list. Chromium also excludes `opacity: 0` elements, elements that cover the full viewport (treated as background) and low-entropy placeholders ([web.dev LCP](https://web.dev/articles/lcp)). So a WebGL hero's LCP is the poster image or, if the poster is full-viewport, most likely the `<h1>`, which makes the display font's delivery the LCP path (3.7). One secondary guide claims "the LCP element is usually the canvas" ([Utsubo](https://www.utsubo.com/blog/webgl-three-js-site-seo-rankable-guide)); the web.dev list contradicts it.
- three.js `r186` (`three@0.186.1`, npm 2026-09-24, MIT) documents `compileAsync(scene, camera)`, which uses `KHR_parallel_shader_compile` and is the recommended variant wherever available. Its docs also advise defining the loop with `setAnimationLoop()` rather than raw `requestAnimationFrame`, and offer `setPixelRatio()`, `forceContextLoss()` and `failIfMajorPerformanceCaveat` ([WebGLRenderer docs](https://threejs.org/docs/pages/WebGLRenderer.html)).
- `requestIdleCallback` is Chromium/Firefox only ([webstatus.dev](https://webstatus.dev/features/requestidlecallback)), so it needs a fallback. `navigator.deviceMemory` and `connection.saveData` are Chromium-only ([MDN BCD Navigator](https://github.com/mdn/browser-compat-data/blob/main/api/Navigator.json), [NetworkInformation](https://github.com/mdn/browser-compat-data/blob/main/api/NetworkInformation.json)): use them as hints, never gates. OffscreenCanvas is Baseline widely available (since 2023-03-27) if you move rendering to a worker ([webstatus.dev](https://webstatus.dev/features/offscreen-canvas)). WebGL2 is widely available; WebGPU is limited (Chrome 144, Safari 26) ([webstatus.dev](https://webstatus.dev/features/webgpu)).
- Observed pattern in the wild (secondary, numbers unverified): poster first, WebGL after idle, IntersectionObserver pausing, DPR capped at 2, static image on mobile ([Utsubo](https://www.utsubo.com/blog/webgl-three-js-site-seo-rankable-guide); [DeepSee case study](https://www.hontran.dev/blog/deepsee-commerce-3d-ecommerce-website-case-study); tiered A/B/C fallback with frame-time downgrade in [Dodecaidr/MeteoHealth](https://dodecaidr.pro/en/articles/r3f-generative-landing/)).

Markup (loading mechanics only; the composition must still follow the house layout rules):

```html
<section class="hero" aria-labelledby="hero-title">
  <div class="hero__stage">
    <picture>
      <source type="image/avif" srcset="/hero-960.avif 960w, /hero-1600.avif 1600w, /hero-2400.avif 2400w" sizes="100vw">
      <source type="image/webp" srcset="/hero-960.webp 960w, /hero-1600.webp 1600w, /hero-2400.webp 2400w" sizes="100vw">
      <!-- poster = a real frame rendered from the scene, same camera and crop -->
      <img class="hero__poster" src="/hero-1600.jpg" width="1600" height="900" alt="" fetchpriority="high">
    </picture>
    <canvas class="hero__canvas" width="1600" height="900" aria-hidden="true"></canvas>
  </div>
  <h1 id="hero-title">…</h1>
  <!-- copy and the one primary action live in DOM, never in the canvas -->
</section>
```

```css
.hero { position: relative; min-height: 100svh; }
.hero__stage { position: absolute; inset: 0; }
.hero__poster, .hero__canvas { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.hero__canvas { opacity: 0; transition: opacity 0.6s ease; } /* decoration only: the poster stays visible beneath */
.hero__canvas.is-live { opacity: 1; }
:root[data-motion="reduce"] .hero__canvas { display: none; }
```

Starting the canvas at `opacity: 0` is fine here: the canvas holds no content, and the poster underneath is already painted.

```js
const stage = document.querySelector('.hero__stage');
const canvas = stage.querySelector('.hero__canvas');

function pickTier() {
  if (document.documentElement.dataset.motion !== 'full') return 'poster';
  if (navigator.connection && navigator.connection.saveData) return 'poster'; // Chromium hint
  if (!document.createElement('canvas').getContext('webgl2')) return 'poster';
  const mem = navigator.deviceMemory ?? 8;                                   // Chromium hint
  const coarse = matchMedia('(pointer: coarse)').matches;
  return mem <= 2 || (coarse && mem <= 4) ? 'lite' : 'full';
}
const whenIdle = (fn) =>
  'requestIdleCallback' in window ? requestIdleCallback(fn, { timeout: 2000 }) : setTimeout(fn, 1200);

async function boot(tier) {
  const { createScene } = await import('./hero-scene.js'); // three.js and assets live only in this chunk
  const { renderer, scene, camera, tick, dispose } = await createScene(canvas, { tier });
  renderer.setPixelRatio(Math.min(devicePixelRatio, tier === 'lite' ? 1.5 : 2));
  await renderer.compileAsync(scene, camera); // no shader-compile hitch on the first visible frame
  renderer.render(scene, camera);             // draw frame 1 before revealing
  canvas.classList.add('is-live');

  const io = new IntersectionObserver(([e]) => renderer.setAnimationLoop(e.isIntersecting ? tick : null));
  io.observe(stage);

  // Frame-time watchdog (inside tick): if the rolling mean frame time stays above ~33 ms for
  // ~90 frames, step down a tier (fewer particles, lower DPR) or fall back to the poster.

  canvas.addEventListener('webglcontextlost', (ev) => {
    ev.preventDefault();
    renderer.setAnimationLoop(null);
    canvas.classList.remove('is-live'); // poster shows again
  });
  addEventListener('motionchange', () => {
    renderer.setAnimationLoop(null); io.disconnect(); dispose(); canvas.classList.remove('is-live');
  }, { once: true });
}

const tier = pickTier();
if (tier !== 'poster') {
  if (document.readyState === 'complete') whenIdle(() => boot(tier));
  else addEventListener('load', () => whenIdle(() => boot(tier)), { once: true });
}
addEventListener('motionchange', (e) => { // viewer switched motion back on
  if (e.detail === 'full' && !canvas.classList.contains('is-live')) {
    const t = pickTier();
    if (t !== 'poster') whenIdle(() => boot(t));
  }
});
```

In a client-routed app, dispose geometries, materials, textures and the renderer on unmount. Budget draw calls and triangles with `renderer.info` (three.js docs).

### 3.6 Preloaders

Default: **no full-screen preloader on first visit.** A preloader moves LCP to whenever the overlay lifts, hides content from people who scroll quickly, and on bad networks becomes the whole experience. In NN/g's parallax testing, some users scrolled into near-empty screens because effects had not loaded ([NN/g](https://www.nngroup.com/articles/parallax-usability/)).

When a heavy scene truly needs load time:
1. Scope the loader to the scene region (the canvas stage). The DOM text, nav and CTA are live and readable at first paint.
2. Progress is honest: it counts real asset promises (`THREE.LoadingManager` or `Promise.all` over fetches), never a timer. Expose it as `role="progressbar"` with `aria-valuenow`, or keep it `aria-hidden` if it is purely decorative and the content is already available.
3. An intro sequence is capped (house: 1.5 s), skippable (click or Esc), shown once per session (`sessionStorage`), and skipped under reduced motion.
4. For page-to-page theatre, use View Transitions instead of an overlay. Same-document view transitions are Baseline newly available (Firefox 144, 2025-10-14); cross-document transitions are limited (Chromium 126+, Safari 18.2+, no Firefox) ([webstatus.dev](https://webstatus.dev/features/view-transitions), [cross-document](https://webstatus.dev/features/cross-document-view-transitions)). Browsers without support get an instant navigation, which is the correct fallback.

### 3.7 Font loading without CLS

Facts: `font-display` block/swap periods are `block` 2-3 s / infinite, `swap` 0 ms / infinite, `fallback` 100 ms / 3 s, `optional` 100 ms / none ([web.dev font best practices](https://web.dev/articles/font-best-practices)). `optional` guarantees no swap-related layout shift but may not use the web font on a first visit. `swap` shows text fast but shifts unless the fallback matches (same source). Preload ignores `unicode-range`, so preload only the one or two faces the first viewport needs (same source). Use WOFF2 only (same source). `size-adjust` is Baseline widely available ([MDN size-adjust](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@font-face/size-adjust)). `ascent-override` / `descent-override` / `line-gap-override` have limited availability, not in Safari ([MDN ascent-override](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@font-face/ascent-override); [webstatus.dev font-metric-overrides](https://webstatus.dev/features/font-metric-overrides)), so on Safari only `size-adjust` corrects the fallback. The override formula is `ascent-override = ascent / unitsPerEm` (likewise descent and line gap) ([Chrome: font fallbacks](https://developer.chrome.com/blog/font-fallbacks)).

Generate fallback values; never hand-guess them:
- Next.js: `next/font` has applied metric overrides and `size-adjust` automatically since Next 13 (Chrome blog above). `next@16.3.6` is current (npm 2026-09-22). Default flags in 16.x: (unverified).
- Nuxt: `@nuxtjs/fontaine`. Anything else: `fontaine` (`1.0.0`, npm 2026-09-21), or Capsize `createFontStack()` (`@capsizecss/core@4.1.3`), with metrics from `@capsizecss/metrics` or, for licensed fonts, `@capsizecss/unpack` `fromFile()` / `fromUrl()` ([Capsize README](https://github.com/seek-oss/capsize)).

```html
<link rel="preload" href="/fonts/brand-display-700.latin.woff2" as="font" type="font/woff2" crossorigin>
<style>
  @font-face {
    font-family: "Brand Display";
    src: url("/fonts/brand-display-700.latin.woff2") format("woff2");
    font-weight: 700;
    font-display: swap;       /* display face: swap, made safe by the matched fallback below */
  }
  @font-face {                /* values below are placeholders: paste the generator's output */
    font-family: "Brand Display Fallback";
    src: local("Arial");
    size-adjust: 104.1%;      /* all engines */
    ascent-override: 91.2%;   /* Chromium, Firefox */
    descent-override: 24.3%;
    line-gap-override: 0%;
  }
  h1, h2 { font-family: "Brand Display", "Brand Display Fallback", sans-serif; }
  body { font-family: "Brand Text", "Brand Text Fallback", system-ui, sans-serif; } /* body may use font-display: optional */
</style>
```

Motion coupling: anything that measures text (SplitText lines, ScrollTrigger pin distances, marquee widths) must wait for fonts. Use SplitText `autoSplit: true`, and run `document.fonts.ready.then(() => ScrollTrigger.refresh())`.

### 3.8 Images and video

- **Formats.** AVIF became Baseline widely available on 2026-07-25 (Chrome 85, Edge 121, Firefox 113, Safari 16.4 / iOS 16.1) ([webstatus.dev AVIF](https://webstatus.dev/features/avif)). Ship AVIF first and WebP as the `<picture>` fallback for older engines. Only 15% of probed winners reference AVIF.
- **Priority.** Images start at Low priority and are boosted after layout. `fetchpriority="high"` makes the LCP image start at High ([web.dev Fetch Priority](https://web.dev/articles/fetch-priority)). Fetch Priority is Baseline newly available since Firefox 132 (2024-10-29) ([webstatus.dev](https://webstatus.dev/features/fetch-priority)). For CSS background LCP images, preload with `fetchpriority="high"` (web.dev). Set `fetchpriority="low"` on carousel slides after the first.
- **Lazy.** `loading="lazy"` on images is widely available ([webstatus.dev](https://webstatus.dev/features/loading-lazy)). `loading="lazy"` on `<video>` is Chrome 150 only ([webstatus.dev loading-lazy-media](https://webstatus.dev/features/loading-lazy-media)), so lazy-start video with IntersectionObserver. `sizes="auto"` is limited (Chrome 126, Firefox 150).
- **Video attributes.** `poster` shows while downloading; without it the element stays empty until the first frame arrives. `preload` accepts `none` / `metadata` / `auto`, its default varies by browser, and `autoplay` overrides it ([MDN video](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/video)). Autoplay blocking does not apply to muted or audio-less media ([MDN Autoplay guide](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Autoplay)). `navigator.getAutoplayPolicy()` is Firefox-only (BCD Navigator), so do not depend on it. Only 15% of probed winner videos have a poster: the rest paint an empty box until frame 1.

```html
<figure class="reel">
  <video class="reel__video" muted playsinline loop preload="none" controls
         poster="/reel-poster-1600.avif" width="1600" height="900" aria-describedby="reel-cap">
    <source src="/reel-1600.mp4" type="video/mp4">
  </video>
  <figcaption id="reel-cap">…</figcaption>
  <button class="reel__toggle" type="button" hidden>Pause video</button>
</figure>
```

```js
document.querySelectorAll('.reel').forEach((fig) => {
  const v = fig.querySelector('video');
  const btn = fig.querySelector('.reel__toggle');
  v.removeAttribute('controls');   // no JS: native controls and poster; with JS: our toggle
  btn.hidden = false;
  let userPaused = document.documentElement.dataset.motion !== 'full'; // reduced: never autoplay
  const sync = () => { btn.textContent = v.paused ? 'Play video' : 'Pause video'; }; // label carries state; no aria-pressed as well
  new IntersectionObserver(([e]) => {
    if (e.isIntersecting && !userPaused) { v.preload = 'auto'; v.play().catch(() => {}); }
    else v.pause();
  }, { threshold: 0.25 }).observe(v);
  btn.addEventListener('click', () => { userPaused = !v.paused; userPaused ? v.pause() : v.play().catch(() => {}); });
  addEventListener('motionchange', (e) => { if (e.detail !== 'full') { userPaused = true; v.pause(); } });
  v.addEventListener('play', sync); v.addEventListener('pause', sync); sync();
});
```

Video with meaningful audio needs captions (`<track kind="captions">`) and a transcript (Awwwards dev checklist; WCAG 1.2.x).

### 3.9 Custom cursor, done so it cannot hurt

Custom CSS cursors override OS cursor-size and color settings that low-vision users depend on ([Eric Bailey](https://ericwbailey.design/published/dont-use-custom-css-mouse-cursors/)). Custom cursors do not scale with the Windows size setting, and there is no media query that exposes the user's cursor size ([David Bushell, 2025](https://dbushell.com/2025/10/27/custom-cursor-accessibility/)). 17% of probed winners hide the native cursor.

Rule: keep the native cursor, always. A follower is an extra decorative layer:

```css
.cursor-follower { position: fixed; inset: 0 auto auto 0; pointer-events: none; z-index: 1000; display: none; }
@media (hover: hover) and (pointer: fine) {
  :root[data-motion="full"] .cursor-follower { display: block; }
}
/* never: body { cursor: none; } */
```

```js
function setupCursorFollower() { // called only inside the finePointer + full-motion branch (3.1)
  const el = document.querySelector('.cursor-follower');
  el.setAttribute('aria-hidden', 'true');
  const xTo = gsap.quickTo(el, 'x', { duration: 0.35, ease: 'power3' });
  const yTo = gsap.quickTo(el, 'y', { duration: 0.35, ease: 'power3' });
  const move = (e) => { xTo(e.clientX); yTo(e.clientY); };
  addEventListener('pointermove', move, { passive: true });
  return () => removeEventListener('pointermove', move);
}
```

Any state the follower communicates ("drag", "view") must also be visible on the element itself, so keyboard and touch users get it.

---

## 4. Mobile excellence patterns

1. **Compose for the phone; do not shrink the desktop.** NN/g: scroll-jacks on mobile run longer and disorient more, and participants did much better on sites that dropped the desktop scroll-jack on mobile ([NN/g](https://www.nngroup.com/articles/scrolljacking-101/)). Pinned horizontal chapters, cursor effects and pointer parallax are desktop-only (`mm.add` with a width plus `(pointer: fine)` condition).
2. **Native touch scroll.** Lenis leaves touch native by default (`syncTouch: false`), and ScrollSmoother does no touch smoothing by default. Keep it that way; the README flags `syncTouch` as unstable on iOS below 16.
3. **Viewport units.** Size the hero with `svh`/`dvh` (viewport-unit variants widely available since 2022-12 ([webstatus.dev](https://webstatus.dev/features/viewport-unit-variants))). Use `svh` for the first frame so the URL-bar collapse does not cause jumps. 83% of probed winners already do.
4. **Input-aware effects.** Gate hover reveals and magnetic effects behind `(hover: hover) and (pointer: fine)`. Interaction media features are widely available ([webstatus.dev](https://webstatus.dev/features/interaction)). Anything hover-revealed on desktop is visible by default on touch.
5. **Targets and gestures.** Primary targets 44×44; nothing under 24×24 without spacing (SC 2.5.8). Swipe carousels get buttons (SC 2.5.7). Never lock orientation or block pinch-zoom.
6. **GPU budget.** Cap DPR at 1.5 on the lite tier. Safari caps rAF-driven scroll smoothing at 60 fps, and at 30 fps in Low Power Mode (Lenis README), so design motion that still reads at 30 fps. On the lowest tier or with Save-Data, ship the poster (3.5). A secondary case study reports a static mobile hero outperforming worker-rendered WebGL on phones (Utsubo, unverified numbers).
7. **Type.** Fluid type obeys max ≤ 2.5 × min. Test at 320 CSS px (SC 1.4.10) and at 200% zoom (SC 1.4.4).
8. **Media weight.** Serve phone-width AVIF sources, lazy-start video with IntersectionObserver, and give phones a shorter, lower-bitrate cut, or the poster.
9. **Test on real hardware**: a mid-tier Android over a throttled network, plus an iPhone in Low Power Mode with Reduce Motion on.

---

## 5. Failure modes common on award sites

| # | Failure | Breaks | Seen in probe (n=60) | Fix |
|---|---|---|---|---|
| 1 | Sections start at `opacity: 0` and wait for a reveal | House law; LCP; blank sections on stalled JS; NN/g saw blank screens | pattern is common; 13% ship almost no server text | 3.2 settle + failsafe; LCP element never animated from 0 |
| 2 | Full-screen preloader before any content | LCP, bounce, no-JS | not measured statically | 3.6: scene-scoped loader, honest progress, skippable |
| 3 | Scroll-jacking (rate or direction), long horizontal hijacks | NN/g usability; SC 2.3.3 | n/a statically | native scroll; one desktop-only pinned chapter, no body copy |
| 4 | Transform-driven virtual scroll | find-in-page, scrollbar drag, keyboard | Locomotive 1/60 (v4 vs v5 unknown) | Lenis ≥ 1.3.26 or ScrollSmoother |
| 5 | Smooth scroll forced under reduced motion | 2.3.3; vestibular safety | **30%** (Lenis with no PRM string; heuristic) | upgrade Lenis; skip init when reduced (3.4) |
| 6 | No reduced-motion handling at all | 2.3.3; WebKit triggers | **55%** have no PRM string in CSS or fetched JS | 3.1 architecture |
| 7 | Native cursor hidden for a custom one | low-vision cursor settings | **17%** | 3.9: follower only, native cursor kept |
| 8 | `outline: none` without a `:focus-visible` replacement | 2.4.7 | 66% set outline none/0; 48% use `:focus-visible` | 2px ring, 3:1 change, offset 2-3px |
| 9 | Focus hidden behind a sticky header or cookie bar | 2.4.11 | 76% lack scroll-padding/margin | `scroll-padding-top` (C43) |
| 10 | No skip link | 2.4.1 | **98%** | skip link + focus move (3.4) |
| 11 | Zoom blocked in viewport meta | 1.4.4 | **10%** | remove `user-scalable=no` / `maximum-scale=1` |
| 12 | `vw`-driven display type | 1.4.4 | 36% | `clamp()` with max ≤ 2.5 × min, rem-anchored |
| 13 | Autoplay video/marquee without pause | 2.2.2 | 154/250 videos autoplay | pause toggle; no autoplay when reduced (3.8) |
| 14 | Video without poster | blank frame, LCP | 85% of videos | poster rendered from the video |
| 15 | Split text read letter by letter, or silenced | 1.3.1, 4.1.2; ARIA naming | SplitText-like code on 28% | 3.3 rules: headings only, v3.13+ aria, revert |
| 16 | Text rendered only inside WebGL | 1.1.1, SEO, no-JS | 42% ship `<canvas>` | DOM text over canvas |
| 17 | Hover-only information | dev checklist; 1.4.13 | n/a | visible by default on touch; hover only enhances |
| 18 | Low-contrast "tonal" copy over imagery or grain | 1.4.3 | n/a | measure worst frame; scrim behind text only |
| 19 | Web-font swap reflow; SplitText lines broken after fonts load | CLS; broken lines | 81% lack metric-matched fallbacks | 3.7 + `autoSplit` |
| 20 | Main-thread shader compile/texture decode right after first paint | INP, jank | n/a | `compileAsync`, idle boot, worker/OffscreenCanvas |
| 21 | Glitch/strobe transitions | 2.3.1 | n/a | ≤ 3 flashes/s; reduced motion removes them |
| 22 | SPA transitions: title not updated, focus lost, `scrollRestoration = "manual"` | 2.4.3, Back button | n/a | 3.4 restoration + focus to `<h1>` |
| 23 | Drag-only carousels and orbit controls | 2.5.7 | n/a | buttons and keys |
| 24 | Images without dimensions | CLS | 53% of `<img>` | `width`/`height` or `aspect-ratio` |

---

## 6. Where award habits collide with the house law

| Award-site habit | Why it fails here | Crafted alternative |
|---|---|---|
| Content fades in from `opacity: 0` on scroll | House law's invisible-content trap; also delays LCP and hides text when JS stalls | Settle motion on visible content (3.2); masked line-rise only below the fold with a failsafe |
| Underline that grows or wipes in on hover | Slop tell (house law); links still need a non-color cue (SC 1.4.1) | Static underline in body copy (`text-decoration-thickness` / `text-underline-offset` chosen with intent). On hover, change underline color or thickness with no travel, or shift the link tone. Nav items change weight or tone |
| Button "boop" (translateY/scale on hover) | Slop tell; movement for its own sake; removed under reduced motion anyway | State change: fill/tone shift, icon slides inside the button, focus ring identical in weight to hover |
| Saturated accent focus ring or CTA pop | Saturated accent is a slop tell, but focus must reach 3:1 (SC 1.4.11, 2.4.13) | Tonal ring: ink- or surface-derived color, 2px, 2-3px offset, checked at 3:1 against both the element and the page |
| Tonal, low-contrast accent text (the house's preferred accent) | Can fall below 4.5:1 | Tonal accents only on decorative or large text meeting 3:1; body and UI text meets 4.5:1. The tonal step comes from value, not from dropping contrast below the threshold |
| Grain over the whole page, including text | House law: grain belongs on the substrate; it also muddies contrast | Grain on background layers only (z-index below content); measure contrast with grain on |
| Cream/beige "editorial" background | House slop tell; unrelated to a11y, but palettes drift low-contrast on cream | Brand-specific surface; verify every text/surface pair |
| Custom cursor with `cursor: none` | Breaks OS cursor accessibility | Native cursor plus optional follower (3.9) |
| Full-screen preloader counting to 100 | LCP and bounce; content hidden | Scene-scoped honest loader; DOM content live (3.6) |
| Floating/bobbing elements on loop | Slop tell (floating cards) and peripheral motion trigger (WebKit) | Motion tied to interaction or scroll, off under reduce, paused off-screen |

---

## 7. Verification protocol (run before calling a build done)

1. **No-JS pass.** Playwright `browser.newContext({ javaScriptEnabled: false })` ([Playwright Browser API](https://playwright.dev/docs/api/class-browser)): screenshot every section. All text and links must be present.
2. **Reduced-motion pass.** `browser.newContext({ reducedMotion: 'reduce' })` or `page.emulateMedia({ reducedMotion: 'reduce' })` (added in Playwright v1.12, [Page API](https://playwright.dev/docs/api/class-page)). Confirm no transforms animate, Lenis is off or 1:1, WebGL shows the poster or a still, and video does not autoplay.
3. **Keyboard pass.** Tab through the page. Every focus stop is visible, never covered by sticky UI, in logical order, with no traps. Esc closes overlays and focus returns. The skip link lands in main.
4. **Find and anchors.** Ctrl/Cmd+F a phrase deep in the page: the page scrolls to it and the text is visible. Click every in-page link: the target clears the header. Back restores the position.
5. **Zoom and reflow.** 200% and 400% browser zoom, 320 CSS px width: no clipped text, no horizontal scroll, and display type actually grows.
6. **Contrast.** Check every text/surface pair, including text over the worst frame of video/WebGL and over grain; also focus rings and control borders at 3:1.
7. **LCP truth.** In the page:
   ```js
   new PerformanceObserver((list) => {
     const e = list.getEntries().at(-1);
     console.log('LCP', Math.round(e.startTime), e.element);
   }).observe({ type: 'largest-contentful-paint', buffered: true });
   ```
   Run it with motion on and with reduced motion. A large difference means motion is delaying LCP (the Shopify diagnostic: a gap of more than 500 ms between image download and LCP means something hides the element).
8. **Lab CWV.** Lighthouse mobile preset: LCP ≤ 2.5 s, CLS ≤ 0.1, no non-composited animations. Record INP on real interactions (menu open, filter, first scroll) with 4× CPU throttle. Field data (CrUX/RUM) after launch at p75.
9. **Axe or WAVE sweep** (both listed in the Awwwards dev tool appendix), then a manual screen-reader skim of headings, landmarks, split headings and the media controls.

---

## Retrieval gaps

- **Revised Awwwards dev guidelines not found.** The linked Google Doc still reads "v0.7 - 14/12/2016" under a banner announcing an update with no date. We have no rubric for how jurors turn accessibility into a 1-10 score.
- **Dev scores exist only for Developer Award winners** (verified by page comparison), so there is no data for SOTDs that missed the award, or for HM/nominee sites. Corpus numbers describe the upper tail.
- **Mobile Excellence status is unverified.** No MOB badge in 732 pages, and the guideline PDF is 2017-2018 era.
- **Probe limits.** Static HTML plus ≤ 4 CSS and ≤ 3 JS files per site, so reduced-motion, SplitText and matchMedia detection are lower bounds (code-split bundles missed). `alt` counts measure presence, not quality. No runtime CWV was measured, and no CrUX field data was pulled for award sites.
- **W3C Understanding pages** returned 403 (Cloudflare) on the first batch; normative SC text comes from the WCAG 2.2 TR. Understanding 2.3.3 and 2.4.11 were read on retry. Others (2.2.2, 2.5.8, 1.4.11) were not read in full.
- **Interpretations flagged:** whether SC 2.2.2 covers ambient WebGL background motion; how specific screen readers handle `aria-label` on name-prohibited roles; whether a text element that first paints clipped by a mask registers a smaller LCP entry. All (unverified).
- **Secondary WebGL case studies** (First Byte LinkedIn post, Utsubo, DeepSee, Dodecaidr/MeteoHealth) report numbers we could not verify. Utsubo's claim that the canvas is usually the LCP element conflicts with web.dev's element list.
- **NN/g "Scroll Fading 101"** recommended fade duration range was cut off in the retrieved text; the house cap of 0.7 s is our choice.
- **Library behaviors not verified in docs:** SplitText `autoSplit` listening after `revert()`; `next/font` fallback defaults in Next 16.x; whether Next.js still ships a route announcer; ScrollTrigger's automatic refresh on font load (we call `ScrollTrigger.refresh()` explicitly).
- **`scheduler.yield`** support comes from MDN BCD (Chrome 129, Firefox 142, no Safari); webstatus.dev has no feature entry to cross-check.
