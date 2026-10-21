# Quality gates: usability, accessibility, performance and QA

Last updated: 2026-09-25

Use this when: you are setting the accessibility, performance and loading rules before the build starts, or verifying your own build (probe, screenshots, failure scenarios, vitals, jury self-score) before calling it award-ready.

## Rules

1. **Accessibility is where winners lose points.** It is the lowest developer sub-score, or tied for lowest, on 41/51 teardowns (mean 6.88, against 8.42 for animations). The recent corpus shows the same gap: 6.83 against 8.01 [stats]. Plan it as a feature from day one. Do not leave it as a final polish pass.
2. **Content is visible by default.** Every word, link, image and control renders from server HTML and CSS with no JS, no WebGL and no CDN. A hidden start state exists only in the frame its tween starts. This is house law, and 45/51 teardowns break it ([./typography.md](./typography.md)).
3. **Reduced motion is a designed state.** CSS, GSAP, Lenis, WebGL and video all follow one `<html data-motion>` flag, and an in-page toggle can set it too. 11/51 winners have any rule [probe], and only about 5 have a real path.
4. **Keyboard works under smooth scroll.** The skip link is the first focusable element. The focus ring is 2px and 3:1 against both neighbours, and a sticky header never covers it. Esc closes overlays and returns focus. Arrow keys, Space, anchors and find-in-page stay native.
5. **Contrast floor: 4.5:1 for body and UI text, 3:1 for text of 24px or larger and for control and focus boundaries.** Measure against the worst frame behind the text. Every teardown logs at least one weak spot ([./color.md](./color.md)).
6. **Targets are at least 24×24 CSS px, and 44×44 for primary actions.** Every drag has a button or key alternative. Zoom is never blocked.
7. **Anything that moves on its own for more than 5s next to content gets a pause control.** Nothing flashes more than 3 times a second. Sound is opt-in.
8. **Core Web Vitals at p75 on mobile: LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1.** The LCP element is DOM text or a poster image. It is never a canvas, never faded in from 0 and never behind a loader.
9. **Set the budget before you design the signature moment.** First-route JS ≤ 350 KB compressed, not counting the 3D chunk. 3D before first interaction ≤ 1.5 MB on mobile and 3 MB on desktop. KTX2 textures at 2048 max. At most 2 preloaded WOFF2 files. DPR capped at 2 (1.25-1.5 under full-screen post). One WebGL context.
10. **Load in this order: HTML, CSS and the LCP element; then fonts; then motion modules; then 3D after load plus idle; then streamed chapters.** A loader has to earn its place. It shows honest progress, is scoped to the scene and ends within 1.5s.
11. **The canvas is `aria-hidden` decoration.** The DOM owns every heading, word and control (15/51 winners draw text in WebGL ([./typography.md](./typography.md))).
12. **QA your own build the way the corpus was audited.** Probe at 1440 and 390, view each screenshot on its own, compare the numbers with the targets, then run the no-JS, reduced-motion, no-WebGL and CDN-blocked scenarios. Only then self-score with [./jury-lens.md](./jury-lens.md).
13. **Nothing ships with a house-law failure,** whatever the self-score says: hidden content, a slop tell, a dead control.

## 1. Where winners lose points

| Dev category (weight) | 51 teardowns: mean (range) | Lowest sub-score on | Recent corpus mean [stats] | 308 Dev Award SOTDs [usability-a11y-perf §1.3] |
|---|---|---|---|---|
| Accessibility (0.10) | **6.88** (6.0-7.6) | **41/51** | **6.83** | 6.93; below 7.0 on 51% |
| Markup (0.15) | 7.25 (6.2-8.2) | 9/51 | 7.16 | 7.22 |
| Semantics/SEO (0.20) | 7.27 (6.6-8.2) | 8/51 | 7.23 | 7.27 |
| WPO (0.20) | 7.78 (6.8-8.8) | 2/51 | 7.56 | 7.54 |
| Responsive (0.20) | 7.66 (6.8-8.6) | 1/51 | 7.51 | 7.60 |
| Animations (0.15) | **8.42** (7.2-9.6) | 0/51 | **8.01** | 8.10 |

Ties count for every category that shares the minimum. Teardown means come from `scores.dev` in all 51 files. The weights are from the Developer Award guideline, and they reproduce the published totals [usability-a11y-perf §1.1].

What the numbers mean for the build:
- **The main jury rates usability lowest too.** In the recent corpus, usability averages 7.2 against design 7.51, creativity 7.61 and content 7.48 [stats]. It is the lowest main criterion on 47/51 teardowns ([./jury-lens.md](./jury-lens.md) rule 6).
- **The jury barely sees accessibility or bytes.** Correlation with the jury overall is +0.17 for accessibility and +0.10 for WPO, against +0.36 for animations. Mean accessibility has sat between 6.66 and 7.14 every year from 2017 to 2026 [usability-a11y-perf §1.3-1.4].
- **The dev score cannot stand in for real accessibility or speed.** messenger scores 7.6 on accessibility, yet its title screen has no DOM text and its BEGIN block is not focusable. artefakt scores WPO 8.0 while declaring 185 MB of mp4 on its first run. Among 60 probed winners, dev accessibility was identical with and without reduced-motion support (6.83 and 6.83) [usability-a11y-perf §1.5]. The skill enforces its own gates because the score does not.
- **Nothing structural forces a trade-off.** Accessibility correlates with animations at +0.03. Animations and WPO rise together at +0.47 [usability-a11y-perf §1.4]. In the corpus, 3D costs no WPO (7.54 against 7.55). Within the 51 teardowns, 3D sites average 6.81 on accessibility against 7.07 without 3D, and the gap is canvas-only text (teardowns `three_d.present`).
- **Cheapest points:** raising accessibility, markup and semantics to 8.0 adds about +0.37 to the dev total. The ship gate is dev ≥ 7.9 with no category under 7.5 ([./jury-lens.md](./jury-lens.md) §7.4).

## 2. Non-negotiables

Each gate is testable, and section 5 says how to test it. "SC" means a WCAG 2.2 success criterion.

### 2.1 Visible by default (house law, the gate that outranks all others)

- Server HTML carries every text node, link and the `h1`. 8/60 probed winners ship under 200 characters of server text [usability-a11y-perf §1.5]. odd-ritual's hero is blank without JS (`.hero-slider_item{display:none}` until the script shows slide 1).
- No authored `opacity: 0`, `visibility: hidden`, closed `clip-path` or off-screen translate waits for JS. Offenders include era-residence (`[data-prevent-flicker]{visibility:hidden}`), cartier-watches-wonders-2025 (title chars at opacity 0 in CSS), pacome-pertant-portfolio (gallery tiles at opacity 0 and scale .5), made-with-gsap-1 (paragraph chars `display:none` until scrolled) and iyo (whole body at `autoAlpha 0` until boot).
- The one allowed arm is the above-the-fold `[data-intro]` in [../recipes/boot.html-snippet.html](../recipes/boot.html-snippet.html). A 1ms CSS animation releases it after 2s, even when no JS arrives. Everything else follows the settle-plus-failsafe contract in [../recipes/motion-core.js](../recipes/motion-core.js) and [./motion.md](./motion.md).
- Mid-reveal is a real state that screenshots, jurors and slow phones all see. shed's mobile_01 caught an ultramarine block empty except for its label.

### 2.2 Reduced motion

- One flag, `<html data-motion="full|reduce">`, set before first paint from the OS setting and a saved in-page choice ([../recipes/boot.html-snippet.html](../recipes/boot.html-snippet.html)). A `[data-motion-toggle]` button (`aria-pressed`) flips it live and fires `motionchange` ([../recipes/motion-core.js](../recipes/motion-core.js)).
- Under reduce: no translate, scale, rotate, parallax, pinning or scroll-linked transforms. Lenis is off (1.3.26 `respectReducedMotion` forces lerp 1). WebGL shows one still. Video does not autoplay. Marquees are static. View Transition animations are `none`. Colour, opacity, focus and open/close still change, instantly or as crossfades of 200ms or less ([../recipes/tokens.css](../recipes/tokens.css) reduced-motion block).
- Real winner paths to learn from: thelinestudio-com wraps every CSS transition in `no-preference` (82 rules), shed does the same (45 rules), vast multiplies every CSS duration by a `--motion` variable that reduce sets to 0, and the-renaissance-edition uses 9 CSS blocks plus a JS store. The first three leave their GSAP timelines running, so gate JS as well, inside `gsap.matchMedia`. gil-huybrecht reads the flag into state that nothing ever consumes.

### 2.3 Keyboard and focus, with smooth scroll

- A skip link to `#main` is the first focusable element. On click it moves focus (`tabindex="-1"` plus `focus({preventScroll:true})`). 1/60 probed winners ship one, and none of the 51 teardowns records one.
- Use `:focus-visible` with a 2px ring, a 2-3px offset and 3:1 against both the element and the page (SC 2.4.7, plus the 2.4.13 AAA geometry). Never set `outline: none` without a replacement: 38/58 winners have one somewhere, and odd-ritual sets `outline:none !important` on `:focus-visible` itself.
- Focus is never hidden under a sticky header, cookie sheet or chat bubble (SC 2.4.11). Use `html { scroll-padding-top: var(--header-h) }`. Only 14/58 winners set scroll padding or margin.
- Smooth scroll wraps native scroll and never replaces it. Lenis registers no keyboard listener, so arrow keys, Space and PageDown stay native. Set `anchors: true` (the default is false) and `stopInertiaOnNavigate: true`. Call `lenis.stop()` while a modal is open and put `data-lenis-prevent` on nested scrollers [usability-a11y-perf §3.4]. mindmarket's `html.is-ready:not(:has(:focus-visible)){scroll-behavior:smooth}` switches CSS smooth scroll off while a keyboard ring shows. Copy it when you use CSS smooth scroll.
- No transform-driven virtual scroller: find-in-page cannot reach the text. oryzo-ai's custom scroller keeps the native position real and maps the arrow and Page keys. Even so, `touch-action:none` on `body` takes native momentum away from phones, and everswap's forced camera flight did not advance under the probe's mobile scroll.
- Modals use `<dialog>` with `showModal()` or an `inert` background, close on Esc and return focus to their trigger. Client-side transitions update `document.title`, move focus to the new `h1` or `main`, and leave `history.scrollRestoration` at `"auto"` (oryzo-ai sets `manual`, which breaks Back).
- Canvas UI gets a DOM mirror in tab order. shader-development-studio draws its focus ring in WebGL when its hidden DOM mirror has focus. dont-board-me's gate works from the keyboard only by accident, through an unlabelled ball `<button>`.

### 2.4 Contrast and legibility

- 4.5:1 for text, 3:1 for text of 24px or more (18.66px bold) and for UI boundaries and focus rings (SC 1.4.3, 1.4.11). Measure the worst frame of video, WebGL or grain under the text, and the midpoint of every colour morph. lando-norris's 8px labels drop to 1.5:1 mid-morph.
- Secondary text is a solid mixed token, never alpha. Alpha-dimmed labels fail on the-watch (40% white on #0a0a0a, 3.8:1), gil-huybrecht (20% on black, about 1.7:1) and leo-parpeix-portfolio-2026 (30% ink, 2.2:1).
- Brand pairs are checked before they become tokens. thelinestudio-com's #f8f8f8 on #ff391e is 3.38:1, and it carries the whole footer. slosh-seltzer's #FF0837 on #FFC1FF is 2.68:1. Fix: [./color.md](./color.md) §10.
- Flat 10-20% veils over footage do not rescue bright frames (bennett-clive, depo-luxe, vast). Choose the text colour per image, and put any scrim behind the text band only, fading out before section edges ([./imagery.md](./imagery.md)).
- Size floors: body 16px, captions 12-13px, no text under 12px. Winners run 8-10px caps (lando-norris, era-residence, san-rita, hubtown) that the teardowns log as unreadable ([./typography.md](./typography.md) §7).
- Zoom and reflow: text reaches 200% (SC 1.4.4) and reflows at 320 CSS px (SC 1.4.10). The text-spacing overrides lose nothing (SC 1.4.12), so revert SplitText masks after the tween. Set `clamp()` in rem with max ≤ 2.5 × min. Never derive the root font size from the viewport (12/51 do).

### 2.5 Pointer, touch and zoom

- Targets are 24×24 minimum (SC 2.5.8) and 44×44 for nav, CTAs and media controls. akaru-2's large MENU pill is the model.
- Drag, orbit, draw and hold each get a single-pointer or key alternative (SC 2.5.7). son-daven's knob drives hidden real tab buttons. lando-norris swaps hover for a `role="switch"` tap-to-lock with `aria-pressed`.
- No `user-scalable=no` or `maximum-scale=1`: active-theory-v6, immersive-garden-website and leo-parpeix-portfolio-2026 block zoom (6/60 in the static probe). Never hide the scrollbar on a long page (leo-parpeix-portfolio-2026 hides it on a 13,231px document).
- The native cursor stays; only 2/51 hide it [probe]. A follower runs only under `(hover: hover) and (pointer: fine)` with full motion, as `aria-hidden` and `pointer-events: none` ([./interaction.md](./interaction.md) rule 4).
- On touch, anything revealed on hover is visible by default. `touch-action: pan-y` on a canvas unless it has a real gesture.

### 2.6 Pause, flash and sound

- A pause control on every autoplaying loop over 5s that sits beside content: marquee, background video, auto-advancing slider, ambient canvas next to text (SC 2.2.2). Missing on made-with-gsap-1 (hero advances every 2.5s), maxima-therapy (10s idle auto-advance) and odd-ritual (a carousel ticker that never stops). The recipe marquee ships one ([../recipes/motion-core.js](../recipes/motion-core.js) `data-marquee`).
- At most 3 flashes in any second (SC 2.3.1). artefakt's title flicker (opacity 1/0/1 inside 0.17s) is the kind of effect to check. Reduced motion removes glitch and strobe transitions entirely.
- Sound starts only on an explicit, labelled toggle. Audio files are not fetched while muted: champions-for-good ships 15 `<audio preload="auto">` elements (2.0 MB) that load with sound off.

### 2.7 Fallbacks: no JS, no WebGL, blocked CDN, old browser

- **No JS:** every page reads fully and navigation works through real `<a href>` links. A `noscript` line that only says "Please enable javascript" (slosh-seltzer) is a failure.
- **No WebGL / software GL / Save-Data / tier 0:** the poster tier is the page. It is a DOM poster plus copy, and the canvas never loads ([./webgl-3d.md](./webgl-3d.md) tiers, [../recipes/three-hero.js](../recipes/three-hero.js)). Without WebGL, steven-com loses its dial navigation. vast's `data-webgl-fb` stills and gil-huybrecht's plain DOM grid on touch are the model.
- **Old browser:** never redirect to `unsupported.html` (active-theory-v6, slosh-seltzer). The poster page is the unsupported page.
- **Blocked or slow CDN:** pin exact versions in one import map ([../recipes/boot.html-snippet.html](../recipes/boot.html-snippet.html)). When the module never arrives, nothing is hidden and the intro deadline releases the page. odd-ritual loads libraries from six CDN hosts plus CodeSandbox, so any one outage breaks it.
- **Context loss:** fade the canvas out so the poster shows, then rebuild on restore ([./webgl-3d.md](./webgl-3d.md)).

### 2.8 Semantics the dev jury counts (35% of the dev weight with markup)

`lang` set. One `h1`, present in server HTML. Ordered headings. Landmarks (`header`, `nav`, `main`, `footer`). A unique `<title>`, description and canonical per route. Open Graph tags. `alt` or `alt=""` on every image. `width`/`height` or `aspect-ratio` on media. `<button>` for actions and `<a href>` for navigation. Failures: ponpon-mania (empty `lang`, `h1` only as 9px SEO text), odd-ritual and siena-film-foundation (no `h1`), mindmarket (phones get only the `aria-hidden` duplicate, so no `h1`), everswap and immersive-garden-website (`h1` set to `visibility:hidden` because WebGL draws it, which removes it from the accessibility tree). A split heading uses SplitText 3.13+ `aria: "auto"` on headings only. iyo and lama-lama-2 use `aria:'none'`, so their split text can be read character by character [usability-a11y-perf §3.3]. lando-norris's screen-reader clones and made-with-gsap-1's `sr-only` headings over `aria-hidden` visual copy are the patterns to copy. Ship no dev leftovers: siena-film-foundation links `http://localhost:8000/app.js` and bundles a lil-gui panel.

### 2.9 Core Web Vitals (web.dev, read 2026-09-24)

| Metric | Good | Poor | Scope | House build gate |
|---|---|---|---|---|
| LCP | ≤ 2.5s | > 4.0s | p75, mobile and desktop separately | LCP element renders with JS off; one `fetchpriority="high"` image; never lazy |
| INP | ≤ 200ms | > 500ms | p75 of real interactions | no main-thread task > 200ms after first paint from your own code; yield with `scheduler.yield()` where it exists (not Safari) |
| CLS | ≤ 0.1 | > 0.25 | p75 | media boxes reserved; metric-matched font fallback; split masks padded with zero shift ([../recipes/motion-core.css](../recipes/motion-core.css)) |

All three must pass [usability-a11y-perf §2 G]. Canvas is not an LCP candidate, and neither is anything at opacity 0 or anything covering the full viewport. So a WebGL hero's LCP is the poster or the `h1`, and the display font's delivery is on the LCP path [usability-a11y-perf §3.5]. Measured on the recipes: the heading's LCP lands when the intro ends, about boot + 1.3s. motion-core.js shows the intro at rest when the module boots later than 800ms (`introMaxStart`), which caps the worst case near 2.1s ([./motion.md](./motion.md)).

## 3. Budgets for heavy sites

House budgets unless marked. Winners often blow past them because the jury does not weigh bytes (section 1). Your visitors on phones do.

| Budget | Mobile | Desktop | Basis |
|---|---|---|---|
| Before LCP | HTML, CSS, the inline gate, ≤ 2 font preloads; no sync `<script>` | same | [usability-a11y-perf §2 G] |
| First-route JS, compressed, 3D chunk excluded | ≤ 350 KB | ≤ 350 KB | Lean motion-rich winners declare mindmarket 219 KB, made-with-gsap-1 ~260 KB, akaru-2 294 KB, shed ~344 KB, maxima-therapy ~353 KB. Heavy end: odd-ritual 2.27 MB, gq-ap-the-extraordinary-lab 6.1 MB |
| 3D payload before first interaction (runtime + scene) | ≤ 1.5 MB | ≤ 3 MB | [webgl-3d-stack §6.1]. iyo and messenger sit near 1 MB. 8 winners declare 9-19.5 MB ([./webgl-3d.md](./webgl-3d.md)) |
| Textures | KTX2, 2048 edge; GPU texture memory ≤ 64-100 MB | one 4096 hero atlas; ≤ 200 MB | 2048² with mips: 22.4 MB as RGBA against 5.6 MB as KTX2 [webgl-3d-stack §6.1] |
| DPR | `min(dpr, 2)` light scene; 1.15-1.5 full-screen post or lite tier | `min(dpr, 2)`; 1.25-1.5 with full-screen post | lando-norris 1.25 above 768px; igloo-inc and messenger 1.15 / 1.5 |
| WebGL contexts | 1 | 1 | son-daven runs 15, one short of Chromium's 16 |
| Draw calls / hero triangles | < 100 / ≤ 100k | < 300 / ≤ 300k | [webgl-3d-stack §6.1] |
| Frame rate during the signature | ≥ 30 fps, worst frame < 50ms | ≥ 55 fps | [./jury-lens.md](./jury-lens.md) U4 |
| Fonts | ≤ 2 preloaded WOFF2, ≤ 200 KB WOFF2 on the first route | same | Winners ship 28 KB (shader-development-studio, one file) to 246 KB (terminal-industries). Failures: dropbox-brand 1.86 MB TTF, maxima-therapy 663 KB in 5 files, siena-film-foundation TTF only |
| Images above the fold | ≤ 3 MB, AVIF then WebP, exactly one `fetchpriority="high"` | same | [imagery rule 10]. AVIF has been Baseline widely available since 2026-07-25, yet only 9/60 winners reference it |
| Video | poster always, `preload="none"`, start on IntersectionObserver, a shorter lower-bitrate phone cut | hero ≤ 1080p | fluid-glass ships a 2160p hero (36.3 MB). Only 37/250 winner videos have a poster [usability-a11y-perf §1.5] |
| Audio | compressed (ogg/aac/mp3), fetched on unmute | same | hubtown declares 38.4 MB of WAV |
| Third parties | one origin plus one pinned CDN; trackers only after consent | same | gq-ap-the-extraordinary-lab: 419 requests, most of them ad-tech |

Adapt at runtime instead of guessing. Measure frame time over a rolling window and step DPR, then post, then the poster. why-zero steps down above 22ms and up below 12ms, with a 180-frame cooldown. Pause the render loop off-screen and in hidden tabs ([./webgl-3d.md](./webgl-3d.md) budgets and render-loop rules).

Weight can be progressive and still score. terminal-industries declares 50 MB of WebP frames and still takes WPO 8.2, because frames load in a worker, coarse to fine, with frame 0 first. made-with-gsap-1's 33 muted loops play only in view. Streaming per chapter is allowed. Blocking on the total is not.

## 4. Loading strategy

Order of work, each step safe on its own:
1. **Server HTML:** every word, link, `h1` and poster. The inline gate sets `data-motion` and hides nothing ([../recipes/boot.html-snippet.html](../recipes/boot.html-snippet.html)).
2. **CSS in `<head>`:** the only pre-JS hide is the `[data-intro]` arm with its 2s deadline.
3. **LCP element:** the `h1` in the display face (preload that WOFF2, `swap` plus a generated metric-matched fallback, [./typography.md](./typography.md) §6), or a poster `<img>` with `width`/`height` and `fetchpriority="high"`. Only 11/58 winners ship the metric-matched fallback, and only 13/60 set `fetchpriority` [usability-a11y-perf §1.5].
4. **Motion modules:** `type="module"` through the pinned import map, never blocking. Anything that measures text waits for `document.fonts.ready`.
5. **3D:** import the three chunk after `load`, the first LCP entry and idle time (with a `setTimeout` fallback, because Safari has no `requestIdleCallback`). Run `compileAsync`, draw frame 1, then fade the `aria-hidden` canvas in over the poster ([../recipes/three-hero.js](../recipes/three-hero.js)). igloo-inc does this well: a 1.4 KB HTML shell, then a 16.5 KB loader, then the 1.49 MB 3D chunk.
6. **Below the fold:** lazy images with `sizes`, video started on intersection, and 3D and frame sequences streamed per chapter.
7. **Navigation:** cross-document View Transitions where they are supported (Chromium 126+, Safari 18.2+). Other browsers get an instant navigation, which is the correct fallback ([../recipes/page-transitions.js](../recipes/page-transitions.js)). With same-document routing, that recipe only wraps the swap. Your router still owns the title, focus and scroll restoration (2.3).

Loader rules ([./interaction.md](./interaction.md) rule 7, [usability-a11y-perf §3.6]):
- The default is no full-screen loader. Use one only when real asset weight must arrive before the first meaningful frame. Scope it to the scene stage, and keep the DOM text, nav and CTA live underneath.
- Progress counts real promises (`LoadingManager`, `Promise.all`), never a timer. Expose it as `role="progressbar"` with `aria-valuenow`, or mark it `aria-hidden` when the content is already available.
- Cap the intro at 1.5s (house). The CSS deadline is 2s, and 3.5s is the outer limit on Elements [elements-catalog §1]. The intro is skippable by click or Esc, shows once per session and is skipped under reduced motion. mindmarket skips its preloader on touch and small screens (~1.25s to usable).
- Never block on the whole archive. gil-huybrecht holds its mask until every project texture and video reaches `loadeddata` (66 MB of mp4 plus 26 MB of KTX2). son-daven locks scroll until about 19 MB of frames arrive. era-residence locks scroll for about 10.2s. igloo-inc shows about 6s of near-blank grey.
- A consent sheet covers no more than 25% of the first phone screen ([./jury-lens.md](./jury-lens.md) U10). floema's Cookiebot covered the whole phone screen, vast's about 50% and dropbox-brand's about 22%. lacoste-polo-factory's 80% white veil also washed out the scene.

## 5. QA procedure for your own build

Run the steps in order. Put the output in the project's scratch folder (in this repo: `evidence/qa/`). A step passes only when its evidence is on disk.

### 5.1 Serve and probe at 1440 and 390

```bash
# from the skill directory (the folder that contains SKILL.md)
python3 -m http.server 8080 --directory /path/to/dist &     # or the framework's preview server, production build
python3 scripts/site_probe.py http://localhost:8080/ --out evidence/qa --name home --steps 8
python3 scripts/site_probe.py http://localhost:8080/work/ --out evidence/qa --name work --steps 6
python3 scripts/site_probe.py http://localhost:8080/404 --out evidence/qa --name 404 --steps 2
python3 scripts/site_probe.py http://localhost:8080/ --out evidence/qa --name home-swgl --gpu swiftshader --no-mobile
```

[../scripts/site_probe.py](../scripts/site_probe.py) writes `desktop_00…NN.jpg` (1440×900, one per wheel step, so Lenis and ScrollTrigger actually fire), `mobile_00.jpg` and `mobile_01.jpg` (390×844 with touch) and `probe.json`. It runs with `reduced_motion="no-preference"`, never clicks and never dismisses banners, so a gate or cookie sheet appears exactly as a juror's thumbnail shows it. The default settle is 6s: if `desktop_00` still shows your loader, the loader is too long (david-whyte-experience and ponpon-mania were caught at shot 00). When your tier check creates its context with `failIfMajorPerformanceCaveat: true` (the [../recipes/three-hero.js](../recipes/three-hero.js) default), the `swiftshader` run must land on the poster tier with no errors.

### 5.2 Read every screenshot, one at a time

Open each JPG on its own at full resolution with the image reader. Never build a contact sheet or montage: small tiles hide exactly the defects this step exists to catch. To zoom, crop the region to a new file and view the crop on its own. For each frame:
- **Voids:** any region that should hold content but is empty or mid-reveal.
- **Legibility:** text over media at its worst glyph window. The nav and logo over every section (akaru-2's logo vanishes on #0E0E0E floors; thelinestudio-com's background-less header overprints content).
- **Collisions:** fixed chrome over display type (shader-development-studio titles run through the nav links; leo-parpeix-portfolio-2026's "Archives" slides under its name).
- **Cuts:** zoom into every mask, notch and clipped edge for shaved caps and descenders (clear the cut). the-watch clips display type on both sides at 390.
- **Fold:** frame 00 is one composition, with no stray sliver of the next section.
- **Phone:** the layout is re-composed rather than shrunk, the consent UI takes no more than 25%, there is no horizontal scroll, and hover effects have become tap or scroll.

### 5.3 Compare the measured numbers with the targets

| `probe.json` field | Target | Source |
|---|---|---|
| `measure.largest_text[0].size` at 1440 | the chosen regime: quiet < 60px, statement 60-150px, poster ≥ 150px; `ls` ≤ 0 | [./typography.md](./typography.md) rules 1, 5 |
| `mobile_measure.largest`, `.h1` | 40-80px, one or two lines (count the lines in mobile_00) | [./jury-lens.md](./jury-lens.md) D3 |
| `measure.font_sizes_px` | nothing under 12px; body 16px | typography rule 7 |
| `measure.font_families_rendered`, `fonts_loaded` | declared families only; no Arial, Times or Helvetica nodes; no `Trial`/`Test`/`Demo` names | typography rule 13 (pacome-pertant-portfolio, oryzo-ai buttons, san-rita's 14 Times nodes) |
| `measure.easings`, `measure.durations` | only [../recipes/tokens.css](../recipes/tokens.css) beziers and the 120/200/350/600/1000/1400ms scale | [./motion.md](./motion.md) rules 3-4. Same-origin CSS only, so grep your bundle for GSAP eases too |
| `measure.reduced_motion_rules`, `measure.sheets` | > 0 with `blocked` = 0 | Blocked sheets make the count a lower bound: champions-for-good and the-renaissance-edition read 0 |
| `measure.css_usage.cursor_none` | 0 | 2.5 |
| `measure.text_colors` × `measure.bg_colors` | every real pair passes 2.4 | 5.4 |
| `mobile_measure.overflow_x` | `false` (also at 320, see 5.6) | SC 1.4.10 |
| `measure.headings`, `lang`, `meta.description`, `title` | one visible `h1`, `lang` set, description present | 2.8 |
| `contexts` | `webgl`/`webgl2` ≤ 1 (`2d` contexts from Rive or Lottie are fine) | section 3 |
| `request_count`, `bytes_by_type_declared`, `top_hosts` | inside section 3; every third-party host justified | Declared `Content-Length` is often missing for streamed media: confirm transfer size in Lighthouse |
| `load_seconds_to_settle`, `renderer_crashed` | loader gone by shot 00; `false` | section 4 |

Also run the in-page probe from [./jury-lens.md](./jury-lens.md) §7.1 at both widths. It returns `skipLink`, `zoomBlocked`, `textHiddenNow`, `textUnder12px`, `targetsUnder24px`, exposed `canvases`, `nativeCursorHidden` and fps with the worst frame.

### 5.4 Contrast pairs

axe handles flat DOM pairs. Text over an image, video, canvas or grain comes back as "incomplete" (the recipes demo returned 6 such nodes), and you measure those yourself. Sample the ground beside the glyphs, never the glyph pixels: JPEG anti-aliasing makes 12-14px text read lighter, which is why immersive-garden-website's first figures came out too harsh. For light text, use the brightest frame behind it; for dark text, the darkest; for colour morphs, the midpoint.

```python
import re  # contrast.py: WCAG 2.x ratio; alpha text is composited over its opaque ground first
def rgba(s):  # 'rgb(1, 2, 3)' | 'rgba(1, 2, 3, .5)' | '#rrggbb'
    if s.startswith('#'): return [int(s[i:i+2], 16) for i in (1, 3, 5)] + [1.0]
    v = [float(x) for x in re.findall(r'[\d.]+', s)]; return v[:3] + [v[3] if len(v) > 3 else 1.0]
def lum(c):
    f = lambda x: x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0] / 255) + 0.7152 * f(c[1] / 255) + 0.0722 * f(c[2] / 255)
def ratio(fg, bg):
    f, b = rgba(fg), rgba(bg); a = f[3]; f = [f[i] * a + b[i] * (1 - a) for i in range(3)]
    hi, lo = sorted((lum(f), lum(b)), reverse=True); return round((hi + 0.05) / (lo + 0.05), 2)
# ratio('#f8f8f8', '#ff391e') -> 3.38 (thelinestudio-com); ratio('rgba(0, 0, 0, 0.4)', '#ebebeb') -> 2.78 (the-watch)
```

### 5.5 Failure scenarios (the test_recipes.py pattern)

Copy the harness structure of [../recipes/test_recipes.py](../recipes/test_recipes.py) into the project's QA folder. Point `PAGES` at your routes and replace the demo-specific hooks (`__webglDemo`, the marquee and hover checks) with your own. Keep these parts: a fresh browser per scenario, the context options, the `NO_WEBGL_JS` init script, the route abort, `wheel_walk`, and the `MONITOR_JS` sampler, which checks every tracked element on every animation frame from first paint, so a hidden state that lasts one frame is still caught.

| Scenario | How | Pass |
|---|---|---|
| normal | default context, wheel-scroll the whole page | no console errors or failed requests; at rest every heading, paragraph, link, image and caption is at opacity 1, unclipped and on screen; split text reverted; pause buttons pause |
| nojs | `java_script_enabled=False` | all text and images visible and loaded; navigation works; JS-only controls stay hidden |
| reduced | `reduced_motion='reduce'` | no hidden state in any sampled frame from first paint; no Lenis; pins become stacks; WebGL shows one still or the poster; video paused; no transition animation |
| nowebgl | init script returns `null` for `getContext('webgl'…)` | poster and copy stay; no canvas inserted; no uncaught errors; the rest of the motion layer runs |
| cdn-blocked | `ctx.route('https://your-cdn-host/**', lambda r: r.abort())` | everything visible once the CSS deadline passes; nothing stuck hidden; no uncaught errors |

Add three more: a live OS flip mid-session (`page.emulate_media(reduced_motion='reduce')` must revert motion without a reload), the in-page toggle (it persists across a reload), and a slow module boot (delay the motion module by about 1.2s: the intro must appear at rest and LCP must stay under 2.5s). motion-core.js was verified against all three ([../recipes/motion-core.js](../recipes/motion-core.js) header).

### 5.6 Keyboard, find, anchors, zoom

```python
# focus_walk.py URL: Tab through the page; flag stops that are invisible, covered (SC 2.4.11) or ringless (SC 2.4.7)
# Tested 2026-09-25: recipes demo index, 24 stops clean; a fixture with outline:none and a fixed header, all 4 stops flagged
import sys
from playwright.sync_api import sync_playwright
STOP = """() => { const el = document.activeElement;
  if (!el || el === document.body) return null;
  if (el.dataset.qaSeen) return 'loop'; el.dataset.qaSeen = '1';
  const r = el.getBoundingClientRect(), s = getComputedStyle(el);
  const hit = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2);
  return { el: el.tagName + ' ' + (el.innerText || el.getAttribute('aria-label') || '').trim().slice(0, 30),
    inView: r.bottom > 0 && r.top < innerHeight && r.width > 0,
    covered: !!hit && !el.contains(hit) && !hit.contains(el),
    ring: (s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 2) || s.boxShadow !== 'none',
    size: [Math.round(r.width), Math.round(r.height)] }; }"""
with sync_playwright() as p:
    pg = p.chromium.launch().new_page(viewport={'width': 1440, 'height': 900})
    pg.goto(sys.argv[1], wait_until='load'); pg.wait_for_timeout(2500)
    for i in range(300):
        pg.keyboard.press('Tab'); pg.wait_for_timeout(120)   # let smooth scroll settle
        st = pg.evaluate(STOP)
        if st in (None, 'loop'): break
        print('FAIL' if (not st['inView'] or st['covered'] or not st['ring']) else 'ok  ', i, st)
```

- The first stop is the skip link. Enter on it moves focus into `main`. Esc closes the menu and every dialog, and focus returns to the trigger. Screenshot one focus stop per component type for evidence (E7).
- **Find:** in a headed run, Cmd/Ctrl+F a phrase from the last section; the page must scroll to it. As an automated check, call `scrollIntoView()` on the last paragraph and confirm that its rect lands inside the viewport and `scrollY` changed. A transform-driven scroller fails this.
- **Anchors and history:** click every in-page link and confirm the target clears the header. Navigate away and back: `scrollY` is restored.
- **Zoom and reflow:** 200% browser zoom at 1440 lays out at 720 CSS px, and 400% at 360. Run contexts at 720, 360 and 320 wide: `overflow_x` stays false, no text is clipped and display type still steps. Inject the SC 1.4.12 overrides (`* { line-height: 1.5 !important; letter-spacing: .12em !important; word-spacing: .16em !important } p { margin-bottom: 2em !important }`) and screenshot: nothing is cut.

### 5.7 Vitals and the axe sweep

```js
// page.evaluate at load, once with full motion and once with reducedMotion 'reduce'
() => new Promise((res) => { let lcp = null, cls = 0;
  new PerformanceObserver((l) => { const e = l.getEntries().at(-1); lcp = [Math.round(e.startTime), e.element && e.element.tagName]; })
    .observe({ type: 'largest-contentful-paint', buffered: true });
  new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) cls += e.value; })
    .observe({ type: 'layout-shift', buffered: true });
  setTimeout(() => res({ lcp, cls: +cls.toFixed(3) }), 500); })
```

- LCP should name the `h1` or poster, and CLS should stay at or below 0.1. A gap of more than 500ms between the full-motion and reduced LCP means motion is holding the element back [usability-a11y-perf §7.7]. To find a shift, register the observer in an init script (`context.add_init_script`) so it sees first paint, then log each entry's `sources` with their previous and current rects. A shift that appears only with full motion comes from the motion layer, often a JS-only control un-hiding inside the header after boot. Reserve its box in CSS.
- Lighthouse (13.5.0 on npm, 2026-09-25), mobile default: `npx lighthouse http://localhost:8080/ --only-categories=performance,accessibility --output=json --output-path=<qa>/lh-home.json`. The target is LCP ≤ 2.5s, CLS ≤ 0.1, and no "non-composited animations" audit.
- INP: open a CDP session and send `Emulation.setCPUThrottlingRate` with `{rate: 4}`. Then open the menu, apply a filter, toggle motion and start the first scroll, and read the longest `event` entry (`PerformanceObserver` with `{type: 'event', durationThreshold: 16}`). Every interaction must stay ≤ 200ms.
- axe: `page.add_script_tag(url='https://cdn.jsdelivr.net/npm/axe-core@4.13.0/axe.min.js')`, then `axe.run(document, {runOnly: ['wcag2a','wcag2aa','wcag21aa','wcag22aa']})`. Expect 0 violations, and review every `incomplete` node by hand (5.4). Finish with a screen-reader skim of headings, landmarks, split headings and media controls.
- After launch, read field data at p75 (CrUX or RUM). Lab numbers are the gate, not the verdict.

### 5.8 Jury self-score

Run the rubric in [./jury-lens.md](./jury-lens.md) §7. Steps 5.1-5.7 produce evidence E1, E2 and E4-E8. Add the element recordings (E3), the string dump (E9) and composed thumbnails (E10). Score the yes/no checks, map them to bands, then run the developer self-score (§7.4). A failure on U9 or D8 is a house-law failure: fix it before you score anything. The ship gate is jury ≥ 7.55 with no criterion under its SOTD band, dev ≥ 7.9 with no category under 7.5, and zero house-law failures. Every failed check goes on the fix list. It is not a caveat to mention in the handoff. Re-run 5.1-5.7 after the fixes.

## 6. Pre-ship checklist

Tick each line only when its evidence file exists.

**Visible and fallback**
- [ ] No-JS screenshots of every route show all text, images and links (5.5 nojs)
- [ ] The per-frame monitor finds no hidden state outside `[data-intro]`, in normal and reduced (5.5)
- [ ] The no-WebGL, swiftshader and CDN-blocked runs show the poster tier with no uncaught errors (5.1, 5.5)
- [ ] Every canvas is `aria-hidden`; every drawn word has a DOM twin; no `unsupported.html` redirect

**Motion**
- [ ] Reduced motion: no transforms, Lenis off, WebGL still, video paused, still composed (5.5 reduced)
- [ ] The in-page toggle works live and persists; a live OS flip reverts without a reload
- [ ] Every loop over 5s has a pause control; nothing flashes more than 3 times a second; sound is opt-in, with no audio fetched while muted
- [ ] Loader: honest progress, ≤ 1.5s intro, skippable, once per session, gone by probe shot 00

**Keyboard, pointer, legibility**
- [ ] The skip link comes first and focus lands in `main`; focus_walk reports 0 FAIL; Esc returns focus
- [ ] Find-in-page and anchors land below the header; Back restores the scroll position
- [ ] All text ≥ 4.5:1 (3:1 at ≥ 24px) at the worst frame; focus rings and control edges ≥ 3:1
- [ ] `textUnder12px` = 0; body ≥ 16px; targets ≥ 24px, primary ≥ 44px; a drag alternative exists
- [ ] No `user-scalable=no`; reflow is clean at 720, 360 and 320; text spacing overrides cut nothing
- [ ] The native cursor is visible; the follower runs only on fine pointers with full motion

**Performance**
- [ ] Mobile LCP ≤ 2.5s on DOM text or poster; CLS ≤ 0.1; INP ≤ 200ms under a 4× CPU throttle
- [ ] Full-motion and reduced LCP differ by less than 500ms
- [ ] Section 3 budgets met: JS, 3D, textures, fonts, DPR, one context, frame rate
- [ ] One `fetchpriority="high"`; every media box reserved; a metric-matched font fallback; WOFF2 only

**Semantics and hygiene**
- [ ] `lang`, one server-HTML `h1`, landmarks, unique title, description, canonical and OG per route; axe 0 violations
- [ ] No console errors, no localhost URLs, no debug GUI, no unused engine, no Trial or Test font files
- [ ] The consent UI covers ≤ 25% of the first phone screen and never washes out the scene

**Judgement**
- [ ] Every screenshot viewed on its own at full resolution; every clipped edge zoom-checked
- [ ] [./jury-lens.md](./jury-lens.md) §7 scored with evidence on disk; the ship gate is met; zero house-law failures

## Crafted vs slop

| Award habit | Slop version | Crafted version |
|---|---|---|
| Scroll reveals | Sections authored at `opacity: 0`, waiting for an observer (45/51) | Content at rest in CSS; a small y-settle created in the frame its tween starts, a failsafe, never on screen at boot ([../recipes/motion-core.js](../recipes/motion-core.js)) |
| Preloader | A full-screen 0-100 counter on a timer that waits for the whole archive | A scene-scoped loader counting real promises, ≤ 1.5s intro, skippable, DOM live underneath |
| Custom cursor | `cursor: none` plus a laggy blob | The native pointer plus a follower that names a target, on fine pointers only |
| Focus state | `outline: none`, or a saturated accent ring | A 2px tonal ring drawn from the ink, 2-3px offset, 3:1 against both neighbours |
| Link and button hover | An underline that grows or wipes; a button that lifts | Body links keep a static underline (the non-colour cue). Hover shifts the tone, weight or fill, or slides an icon inside the box ([./interaction.md](./interaction.md)) |
| Secondary text | White or ink at .3-.5 alpha | A solid mixed token verified at ≥ 4.5:1 ([./color.md](./color.md)) |
| Type over footage | A flat 10-20% black veil on every frame | Text colour chosen per frame; a scrim only behind the text band, fading out before section edges ([./imagery.md](./imagery.md)) |
| Texture | Grain laid over the whole page, including text | Grain on the substrate below the content; contrast measured with grain on |
| WebGL typography | MSDF or particle text as the only copy; `h1` set to `visibility:hidden` | A real `h1` in the accessibility tree; the canvas echo is `aria-hidden` |
| Immersive scroll | A virtual scroller, `touch-action:none` on `body`, `scrollRestoration='manual'` | Lenis on wheel only, native touch, off under reduce, anchors on, restoration auto |
| Ambient life | Loops and drifting elements that never stop | Motion tied to input or scroll, paused off-screen, with a pause control past 5s |
| Old-browser handling | A redirect to `unsupported.html`, or a noscript line asking for JS | The poster tier as the complete page |
| Consent | A full-screen sheet or a white veil over the scene | A small sheet under 25% of the phone screen, placed in the brand's own type and ground |

## Exemplars

- **the-renaissance-edition**: the most complete reduced-motion path in the set (9 CSS blocks plus a JS store), painted stills on phones, View Transitions, and quality stepped from measured fps.
- **messenger**: the best dev total (8.21, WPO 8.8) on about 1 MB of 3D from one origin. Study its budget discipline. Do not copy its canvas-only title screen or its unfocusable BEGIN.
- **lando-norris**: screen-reader clones for split lines, a `role="switch"` tap-to-lock on touch, DPR 1.25 above 768px. It also shows the trap of 8px labels dropping to 1.5:1 mid-morph.
- **made-with-gsap-1**: an `sr-only` `h1` and headings over an `aria-hidden` visual copy, video that plays only in view, and native horizontal scroll replacing drag on phones. Its hero autoplay has no pause control.
- **mindmarket**: a 1.3 MB page, a preloader skipped on touch, and smooth scroll switched off while a focus ring shows. Avoid its phone view, whose only `h1` is `aria-hidden`.
- **thelinestudio-com** and **shed**: every CSS transition gated by `no-preference` (82 and 45 rules). They show the gap too: their JS timelines ignore the flag.
- **vast**: one `--motion` multiplier that turns all CSS motion off, plus `data-webgl-fb` stills as the no-WebGL path.
- **terminal-industries**: 50 MB of frames loaded progressively (worker, coarse to fine, frame 0 first) and still WPO 8.2.
- **shader-development-studio**: a hidden DOM mirror whose focus draws a ring in WebGL. Frame-budgeted text textures.
- **son-daven**: responsive 8.4 from a static phone hero and 7 scenes gated below 992px. Avoid its 15 WebGL contexts and its 19 MB scroll lock.
- **why-zero**: a frame-time quality controller: a 60-frame window, a step down above 22ms and up below 12ms, a 180-frame cooldown, and DPR tiers of 2, 1.5 and 1.

## Evidence

- **Teardowns** (`data/teardowns/<slug>.json`, all 51): `scores.dev` (means, ranges and lowest-category counts computed in this session: accessibility lowest or tied on 41/51; 3D sites 6.81 against 7.07 without), `performance_accessibility.*`, `three_d.performance_tactics`, `motion.preloader`, `steal_this`. Cross-site digest: `evidence/digests/tech_perf_a11y.md`.
- **[stats]** `data/stats.md`, cut recent_2024_plus (575): dev means for semantics 7.23, animations 8.01, accessibility 6.83, WPO 7.56, responsive 7.51, markup 7.16; jury means for design 7.51, usability 7.2, creativity 7.61, content 7.48.
- **[probe]** `data/probe_summary.json`: reduced-motion rules on 11/51, `cursor_none` 2/51, webgl2 contexts on 41/51, 3D assets on 26/51.
- **[usability-a11y-perf]** `data/research/usability-a11y-perf.md`: §1.3-1.4 (308 Developer Award SOTDs, correlations), §1.5 (static probe of 60 winners from 2025-2026), §2 (the WCAG 2.2 checklist and CWV thresholds read from web.dev on 2026-09-24), §3.1-3.9 (recipes), §7 (verification protocol). Also [webgl-3d-stack §6.1], [elements-catalog §1] and [imagery rule 10].
- **Sibling references:** [./jury-lens.md](./jury-lens.md) §7 (rubric and in-page probe), [./motion.md](./motion.md), [./typography.md](./typography.md), [./color.md](./color.md), [./imagery.md](./imagery.md), [./interaction.md](./interaction.md), [./webgl-3d.md](./webgl-3d.md).
- **Tools:** [../scripts/site_probe.py](../scripts/site_probe.py) (docstring and fields read 2026-09-25) and [../recipes/test_recipes.py](../recipes/test_recipes.py) (scenario design). The `contrast.py` and `focus_walk.py` snippets and the LCP/CLS observer were run on 2026-09-25 against the recipes demo in headless Chromium through Playwright; the contrast outputs match the teardowns' computed ratios. axe-core 4.13.0 and lighthouse 13.5.0 are the npm versions on 2026-09-25.
- **Gaps:** the dev jury's accessibility rubric is unpublished (the guideline doc still reads v0.7, 2016), so section 1 treats the scores as descriptive. Declared bytes are `Content-Length` and undercount streamed media. The 350 KB JS, 200 KB font, 1080p video and 1.5s intro budgets are house rules anchored to lean winners, not standards. Whether SC 2.2.2 covers ambient WebGL beside text is a conservative reading [usability-a11y-perf, retrieval gaps].
