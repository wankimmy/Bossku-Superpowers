# Motion and choreography

Last updated: 2026-09-25

Use this when: you are choosing the scroll model, easing and duration tokens, reveal grammar, page transitions or preloader for an award-level build, and need the numbers and recipes before writing motion code.

## Rules

1. **Content is visible by default.** HTML and CSS render every word, image and control at rest. JS creates a hidden start state only in the frame its tween starts, and never on anything already on screen at boot. The one CSS-armed element is the above-the-fold intro, and it carries a 2s deadline ([../recipes/boot.html-snippet.html](../recipes/boot.html-snippet.html)). House law outranks the 6+ winners that ship content hidden until JS arrives (see the boot contract).
2. **Stack: GSAP 3.15 (ScrollTrigger, SplitText, CustomEase) plus Lenis 1.3.26 on `gsap.ticker` (`autoRaf: false`), `lerp: 0.1`.** Lenis runs on 36/51 winners and 85/117 recent SOTDs; ScrollTrigger on 84/117 [motion-stack §1.3]. One smoother only. [../recipes/motion-core.js](../recipes/motion-core.js). In a React app, Motion 13 (`motion/react`) handles layout, presence and gestures, and GSAP handles the scroll scenes via `useGSAP`. Motion renders `initial` into server HTML, so never ship `initial={{ opacity: 0 }}` on content [motion-stack §0, §1.1].
3. **Eight curves, fixed roles.** Out for entrances (`--ease-enter`, `--ease-reveal`), in for exits (`--ease-exit`), in-out for on-screen travel (`--ease-move`), `linear` / `"none"` for anything scrubbed or looped. The same beziers drive CSS and GSAP ([../recipes/tokens.css](../recipes/tokens.css)).
4. **Duration scales with distance, not importance.** Hover 200ms (`--dur-2`), menus and cards 600ms (`--dur-4`), one masked line or media reveal 1000ms (`--dur-5`), the whole hero intro capped at 1400ms (`--dur-6`). Exits run about 0.6x the matching enter.
5. **Stagger follows reading order and caps the total spread at 0.6s** (`--stagger-max`). Lines 0.08s, words 0.05s, chars 0.02s.
6. **One hero moment per viewport.** At most one element travels more than about 20% of the viewport at a time. Order: world or object first, type second, chrome last (17 teardowns named under Choreography follow it; hubtown is the exception).
7. **Triggered for content, scrubbed for space.** Text and UI reveal on a time-based trigger so they always finish. Parallax, frames, horizontal travel and camera moves are scrubbed. Never scrub text out of legibility.
8. **Overlap, do not queue.** Start the next beat at 60-75% of the previous one.
9. **Velocity effects are clamped and decay.** They change speed, blur, bend, skew (≤ 3deg, images only) or playback rate (≤ 4x), never a text baseline, and settle to rest within about 0.8s of the scroll stopping.
10. **A preloader needs real weight behind it and shows honest progress.** Once assets are ready, the hero intro takes 1.4s (`--dur-6`) against a house cap of 1.5s [usability-a11y-perf §3.6]. The best award Elements finish loader plus intro in about 1.9s, and 3.5s is their ceiling [elements-catalog §1]. The loader has a hard cap of 4s: after that the page shows no matter what is still loading [motion-stack §4.12]. No timer counters.
11. **Page transitions:** cross-document View Transitions for multi-page sites; Taxi or Swup with same-document View Transitions only when WebGL, audio or scroll state must persist. No new Barba builds.
12. **Reduced motion removes movement and keeps feedback.** About 5/51 winners gate part of their motion and none gates all of it (see Reduced motion). Gate CSS, GSAP, Lenis, WebGL and video.
13. **Hover never moves the box and never animates an underline.** State changes are tonal, typographic, or happen inside a static box ([../recipes/magnetic.js](../recipes/magnetic.js)).
14. **One signature verb per site, repeated.** Two or three curves and one reveal grammar read as authored. The signature comes from one bespoke moment, not ten different fades.
15. **Calm is allowed; dead is not (house law).** Every page ships at least a hero intro, one signature moment that responds to scroll, pointer or state, a nav that enters and responds, and crafted hover states. A motion that only loops in place does not count as the signature [motion-stack §5.10].

## What winners ship

| Layer | 51 teardowns | Wider sample | Decision |
|---|---|---|---|
| Smooth scroll | Lenis 36 (incl. mindmarket's Locomotive v5, which wraps Lenis; ponpon-mania and san-rita ship it but their homepages do not scroll), custom virtual scroll 9, ScrollSmoother 1, native 2, no scroll 3 | Lenis 85/117, Lenis+GSAP 66/117 [motion-stack §1.3] | Lenis, unless the page is one WebGL scene |
| Timeline engine | GSAP on most; own tween engines on the WebGL studios (active-theory-v6, everswap, messenger, lacoste-polo-factory); oryzo-ai uses SplitText but zero `gsap.to` calls | ScrollTrigger 84/117, SplitText 54/117, CustomEase 40/117; 91% on GSAP 3.13+ [motion-stack §1.3] | GSAP 3.15, all plugins free |
| Text splitting | SplitText, SplitType or a TextSplitter in about 30/51 motion sections | | SplitText `mask: "lines"`, headings only |
| Router | Taxi 4, Barba 4, Swup 2; framework routers or single-page scenes elsewhere; View Transitions confirmed on 1 (the-renaissance-edition) | PJAX 36/117; `view-transition-name` 19/117; `@view-transition` 0 [motion-stack §1.3] | View Transitions first |
| Authored assets | Lottie 8, Rive 6, Theatre.js 4 (teardowns); Lottie 6, Rive 6 [probe] | | Only for drawn or illustrated brands |
| Clip-path / sticky | clip-path on 29/51, sticky on 20/51 [probe] | | Clip is the reveal primitive |
| Reduced motion | rules on 11/51 [probe] (same-origin sheets only; blocked sheets hid the rules of the-renaissance-edition and champions-for-good); partial gating on about 5, complete on none | the string on 77/117, presence only [motion-stack §1.3] | Ship a full path |

Juries reward scroll storytelling, transitions and loaders far more than cursor tricks. Element titles and tags across 575 recent winners: scroll 414, transition 233, hover 134, loader 129, parallax 69, reveal 66, cursor 25, horizontal 23, marquee 20, stacking 9, magnetic 1 [motion-stack §1.3]. "Animation" (107) and "GSAP" (106) are the top two site tags of 575. The developer jury scores animations highest of its six criteria (mean 8.01) and accessibility lowest (6.83) [stats]. Among dev scores, animations correlates most with performance (WPO, r = +0.47) [usability-a11y-perf]: the best animators also ship the lightest code.

## Build order

1. Paste [../recipes/boot.html-snippet.html](../recipes/boot.html-snippet.html) into `<head>`: motion gate, intro deadline, pinned import map.
2. Load [../recipes/tokens.css](../recipes/tokens.css), then [../recipes/motion-core.css](../recipes/motion-core.css). Override family tokens only if the brand has its own curve.
3. Write the page complete and static first. Check it with JS disabled.
4. Mark up motion with data attributes (`data-intro`, `data-reveal`, `data-parallax`, `data-marquee`, `data-pin="horizontal"`, `data-stack`) and call `init()` from [../recipes/motion-core.js](../recipes/motion-core.js).
5. Decide the one signature moment per viewport, then build it (scrubbed scene, WebGL via [../recipes/three-hero.js](../recipes/three-hero.js) and [./webgl-3d.md](./webgl-3d.md), or a pinned sequence).
6. Add page transitions ([../recipes/page-transitions.css](../recipes/page-transitions.css), [../recipes/page-transitions.js](../recipes/page-transitions.js)) and micro-motion ([../recipes/magnetic.js](../recipes/magnetic.js), [../recipes/webgl-image-hover.js](../recipes/webgl-image-hover.js)).
7. Verify: no JS, reduced motion, the in-page toggle, 390px, a blocked CDN, a background tab, and LCP. The recipe demos in `../recipes/demo/` show the markup contracts.

## Smooth scroll

Measured Lenis settings across the 36 Lenis winners:

| Setting | Values seen | Use |
|---|---|---|
| `lerp` | .04 (hubtown, heavy), .07 (akaru-2), .085 (leo-parpeix-portfolio-2026), **.1** (the plurality: explicit on lando-norris and steven-com, `new Lenis()` defaults on aim-ai-modernism-of-kharkiv and odd-ritual; floema, lama-lama-2 and terminal-industries show only the library default because their call-site options were not isolated), .125 (iyo), .15 (gil-huybrecht), .18 (champions-for-good), .2 (shed, thelinestudio-com), .3 (vast) | 0.1 default; 0.15-0.2 for tool-like or dense-index sites; never below 0.07 |
| `duration` + easing | 0.6 (zentry), 0.8 easeOutQuart (bennett-clive), 1.0-1.2 with `1.001 - 2^(-10t)` (the-renaissance-edition, era-residence, pacome-pertant-portfolio, son-daven) | Pass `lerp` OR `duration`, never both [motion-stack §1.1] |
| `wheelMultiplier` | 2 (akaru-2), 1.25 (gil-huybrecht, shed), .8 (pacome-pertant-portfolio) | Keep 1; anything else fights the user's hardware |
| `syncTouch` | true on lando-norris, leo-parpeix-portfolio-2026, steven-com and maxima-therapy's overlay scrollers; false or unset elsewhere | false: native touch momentum |
| Reduced motion | `respectReducedMotion` exists only from 1.3.26; 5/77 probed Lenis installs run it [motion-stack §1.1] | On (motion-core.js sets it explicitly) |

- **One clock.** Drive Lenis from `gsap.ticker` with `lagSmoothing(0)` and `lenis.on('scroll', ScrollTrigger.update)`, as akaru-2, fluid-glass, son-daven and zentry do. `init()` in motion-core.js does this.
- **No double lag.** With Lenis smoothing, use `scrub: true`. `scrub: 1` stacks a second lag; lando-norris's horizontal track runs `scrub: 1` and carries a 1s catch-up [motion-stack §4.1].
- **Custom virtual scroll only for a single stage.** The 9 custom scrollers (active-theory-v6, cartier-watches-wonders-2025, depo-luxe, everswap, igloo-inc, immersive-garden-website, oryzo-ai, slosh-seltzer, why-zero) all serve a fixed WebGL stage or an infinite index. They break find-in-page, anchors and the scrollbar. If you write one, normalise the lerp to frame rate as active-theory-v6, igloo-inc, why-zero and everswap (`1 - exp(-12 dt)`) do.
- **Snap only on scene or relay sites.** Winners snap after idle: bennett-clive 0.5s after scroll stops, era-residence 40ms after stop when a section is more than 50% in view, igloo-inc after 1.4s between scenes, siena-film-foundation with an always-on magnet. No snap on reading content [motion-stack §6.1].
- **Stop Lenis under overlays.** Call `lenis.stop()` while a menu, modal or drag is open (odd-ritual during its menu and carousel drag, steven-com during its menu and manifesto overlay), and mark nested scrollers `data-lenis-prevent`. shed and dont-board-me also hold Lenis stopped through the intro, which is acceptable only when the intro is 2s or less.

## Easing tokens

Token names are exactly those in [../recipes/tokens.css](../recipes/tokens.css). motion-core.js reads each family token at boot and registers it as a GSAP CustomEase named `motion<Name>` (`motionOutExpo`, `motionInOutQuart`, and so on), so CSS and JS share one curve.

| Token | Bezier | GSAP | Role alias | Evidence |
|---|---|---|---|---|
| `--ease-out-cubic` | .33, 1, .68, 1 | `power2.out` | `--ease-micro` | Most common GSAP ease on SOTDs, 65/117 [motion-stack §2.1]; lando-norris x36, hubtown x48, ponpon-mania x87, steven-com x54 |
| `--ease-out-quart` | .25, 1, .5, 1 | `power3.out` | `--ease-enter` | era-residence 'Out' x50 and son-daven 'Out' x42 use exactly this; the classic fit .165,.84,.44,1 is on 6/51 [probe] and is akaru-2's house curve (x122) |
| `--ease-out-quint` | .22, 1, .36, 1 | `power4.out` | | lama-lama-2 x62, zentry x22 (entrances), depo-luxe x18 |
| `--ease-out-expo` | .16, 1, .3, 1 | `expo.out` | `--ease-reveal` | The classic fit .19,1,.22,1 on 11/51 is the most common non-framework CSS curve [probe]; thelinestudio-com x146, david-whyte-experience x83, floema x70; the GSAP default on siena-film-foundation and steven-com |
| `--ease-in-cubic` | .32, 0, .67, 0 | `power2.in` | `--ease-exit` | depo-luxe's house exit ease (x61); zentry uses power2.in for exits only |
| `--ease-in-out-quart` | .76, 0, .24, 1 | `power3.inOut` | `--ease-move` | son-daven and era-residence 'InOut'; the-watch x97; fluid-glass x25; classic .77,0,.175,1 on 6/51 [probe] |
| `--ease-in-out-expo` | .87, 0, .13, 1 | `expo.inOut` | | made-with-gsap-1 house ease; terminal-industries panels 1.2s; .9,0,.1,1 on 3/51 [probe]. One takeover per site |
| `--ease-in-out-sine` | .37, 0, .63, 1 | `sine.inOut` | `--ease-ambient` | immersive-garden-website house ease (about 80 uses), gq-ap-the-extraordinary-lab's slow luxury pacing |
| `--ease-standard` | .4, 0, .2, 1 | | | 13/51, mostly framework defaults [probe]: toggles and focus rings only |
| `linear` | | `"none"` | | cartier-watches-wonders-2025 x86, david-whyte-experience x114, dont-board-me x43: every scrub and marquee |

- **One family per project.** Classic Penner fits and easings.net fits both circulate; they look nearly identical, and mixing them reads as noise [motion-stack §2.1].
- **The most coherent studios run one family.** fluid-glass uses power3 only ("inOut for things that travel, out for things that arrive"); the-watch uses power3.inOut 97 times; era-residence and son-daven share five named eases and a 400/800/1200 duration set.
- **A studio signature curve is allowed:** a hard start with a long tail, such as .65,.05,0,1 (lando-norris, steven-com), .625,.05,0,1 (why-zero, iyo), .62,.05,.01,.99 (vast), .32,.94,.6,1 (bennett-clive). To adopt one, override the family token it replaces (for example `--ease-out-expo`) on `:root`. motion-core.js reads family tokens, not role aliases, so overriding only `--ease-reveal` changes CSS and leaves JS on the old curve.
- **Bouncy curves:** the easeOutBack bezier .175,.885,.32,1.275 is on 3/51 and .34,1.56,.64,1 on 2/51 [probe]. Elastic or back strings appear in 21 teardown motion sections, mostly on character-scale pops (maxima-therapy overshoots everything except its curtain). They never go on UI text or buttons. One illustrative object may overshoot when the whole world is a toy (brunos-portfolio's cartoon physics).

## Duration and stagger

| Token | Value | Use | Evidence |
|---|---|---|---|
| `--dur-1` | 120ms | `:active` press | |
| `--dur-2` | 200ms | hover, focus | 200ms and 300ms are the top CSS durations, 34/51 each [probe] |
| `--dur-3` | 350ms | exits, small UI enters | zentry's title exits run 0.5s power2.in against 1-1.6s entrances (its BigTitle slide exit is the exception, 1s power4.out); era-residence hides in 0.4s against 1.2s reveals |
| `--dur-4` | 600ms | menus, overlays, cards, page-transition legs | lama-lama-2 UI .35-.85s; vast primary .65s |
| `--dur-5` | 1000ms | one line or media reveal | 1000ms on 27/51 [probe]; fluid-glass `duration: 1` x21 |
| `--dur-6` | 1400ms | hero intro total, full-bleed un-clip | the cap |
| `--stagger-chars` | 0.02s | short display lines only | champions-for-good 16-22ms, iyo 20ms, cartier loader 12ms |
| `--stagger-words` | 0.05s | | son-daven 25ms from random, zentry 70ms |
| `--stagger-lines` | 0.08s | | david-whyte-experience 80ms, fluid-glass 100ms, leo-parpeix-portfolio-2026 115ms, lando-norris 150ms |
| `--stagger-items` | 0.08s | cards, grid cells | probe literals .1 on 25 SOTDs and .05 on 25 [motion-stack §2.1] |
| `--stagger-max` | 0.6s | cap on total spread | hubtown spreads headline chars over 1.1s in random order, past the cap: a HUD decode, not a reading line |

- **Exits are fast.** era-residence runs exits three times faster than entrances with the mirrored ease and half the enter stagger; depo-luxe leaves on ease-in and arrives on ease-out.
- **Two clocks are allowed on WebGL sites.** steven-com's world moves over 4-7s on power2.inOut while DOM text moves in 0.5s and lands inside the world's motion. The DOM clock still follows this table.
- **Ambient loops** (`--ease-ambient`) run 3-8s per leg at low amplitude and pause off-screen.

## Choreography

**Who moves first: world, then type, then chrome.** 17 teardowns below follow this order; hubtown is the one recorded exception.
- Camera or scene first: cartier-watches-wonders-2025 (the title types in 500ms after the universe becomes active), oryzo-ai, everswap (camera dolly and vignette, then the title as a line, then words, then fill and chrome), active-theory-v6, the-power-of-storytelling (text resolves after the camera settles), shader-development-studio (the colour grade leads the geometry).
- Object or frame first: the-watch (the object moves first and alone), zentry (frame z and scale at t=0, text at +0.4s), shed (photos, then type), the-renaissance-edition, david-whyte-experience, slosh-seltzer (the can acts, type reacts).
- Shader first: artefakt (WebGL, then decoded text a beat later, chrome last), lama-lama-2, leo-parpeix-portfolio-2026.
- Surface first: fluid-glass (the entering page rises, then scales about .3-.4s later; the menu background scales while its links stagger in, and the label fades in after .3s), maxima-therapy (the route's colour curtain arrives before its content).
- Exception: hubtown puts the frame and HUD up before the world, so the page never looks empty during the 3D load.

**One mover at a time.** floema ("one thing moves at a time"), depo-luxe ("very little moves at once"), gil-huybrecht ("one entrance, then stillness"), the-watch (big transitions separated by quiet stretches), cartier-watches-wonders-2025 (chrome never animates during travel), pacome-pertant-portfolio (the helix is the only big mover). When a signature scene scrubs, micro and ambient motion hold still [motion-stack §5].

**Overlap.** lando-norris starts the colour block's exit at half the clip duration (+0.3s of 0.6s), so the block reads as a cursor running ahead of the text. san-rita overlaps its intro legs by 0.3s (`'>=-0.3'`). In igloo-inc "nothing waits for a previous tween to end". Use `'<0.3'` or `'-=0.4'` position parameters; start a curtain's enter leg at about 80% of its exit [motion-stack §5.4].

**Direction coherence.** Scrolling down brings content up from below; back navigation reverses (page-transitions.js adds a "back" type). For toggles (menu, drawer, modal), build one tween and call `play()` / `reverse()`. By default a reversed ease-out plays as an ease-in, which already follows the exit rule. GSAP 3.15's `easeReverse` (`true` or a named ease) recalculates the ease from wherever the playhead turned, so a menu closed mid-open does not jerk [motion-stack §1.1]. thelinestudio-com enters every sheet on one tilt and leaves on the counter-tilt, from an off-centre `transform-origin`. steven-com always moves type away from the object on exit.

**Triggered versus scrubbed.**
- terminal-industries makes a 410-frame film the conductor: the hero is a pure scrub and the titles are slaved to the same progress value, so text and camera never drift.
- fluid-glass keeps scroll-linked motion linear and physical (parallax, clip, scale) and eases only triggered motion.
- why-zero gates its set pieces: a user gesture fires an authored 3-3.5s film instead of a passive scrub.
- Decision: scrub space, trigger content, gate spectacle behind a gesture.

**Velocity-aware effects** (18 teardown motion sections mention velocity; keyword tally, lower bound).
- What winners map velocity to: DOM overlay blur of `blur(speed*10px)` (siena-film-foundation); plane bend and stretch, plus a "fast mode" that switches the page to an index when you scroll hard (immersive-garden-website); a logo ring spinning at 30+10|v| deg/s that flips with scroll direction (era-residence); marquee `timeScale` sign flipped by direction (vast); a thumbnail video that starts only when speed drops below 100 (depo-luxe).
- Velocity skew: none of the 51 ships a scroll-velocity skew. Skew appears only as a triggered entrance: akaru-2's skewY 3deg settles in its reveals, and champions-for-good's chars skid in from 80px at a 14deg skew that straightens last. The clamps below come from motion-stack §5.8 and are not a measured winner value.
- Rules: clamp (skew ≤ 3deg, playback rate ≤ 4x), decay with `gsap.ticker.deltaRatio()` or a settle tween, only on images and frames, never on text [motion-stack §5.8]. Velocity skew has no recipe file; this is the whole build (run it inside the no-preference `gsap.matchMedia` branch):

```js
const proxy = { skew: 0 };
const setSkew = gsap.quickSetter('[data-skew]', 'skewY', 'deg');
const clampSkew = gsap.utils.clamp(-3, 3);
ScrollTrigger.create({
  onUpdate(self) {
    const s = clampSkew(self.getVelocity() / -300);  // px/s -> deg
    if (Math.abs(s) > Math.abs(proxy.skew)) {
      proxy.skew = s;
      gsap.to(proxy, { skew: 0, duration: 0.8, ease: 'power3.out', overwrite: true,
        onUpdate: () => setSkew(proxy.skew) });                 // settles to 0 when scrolling stops
    }
  },
});
```
- Recipes: the marquee boost in [../recipes/motion-core.js](../recipes/motion-core.js); the pointer-velocity warp in [../recipes/webgl-image-hover.js](../recipes/webgl-image-hover.js).

**Stepped and quantized motion as style** (about 15 teardown motion sections, scramble and decode included).
- messenger quantizes glyph reveals to 3-4 steps, with a boil that re-rolls each glyph about every 780ms; its camera stays smooth under the stepped graphics.
- ponpon-mania boils lines at 5/10/12 steps per second and grain at 10.
- thelinestudio-com blinks UI text on frame steps (opacity 0 at 0s, 1 at .09s, 0 at .15s, 1 at .21s), a nod to animating on twos.
- aim-ai-modernism-of-kharkiv rolls a counter one line at a time with hold plateaus; artefakt and hubtown decode labels by scramble.
- It works when the medium is drawn, film, pixel or terminal, and reads as a gimmick elsewhere [elements-catalog §2.1 P4]. Build with CSS `steps()` or `floor(t * fps) / fps` in a shader; keep large surfaces smooth.

**A signature verb.** champions-for-good's sprint skid (chars brake with a skew that settles last); thelinestudio-com's rotated sheet throws; zentry's rigid 3D slab with words snapping on inside it; son-daven's vertical-bar vocabulary shared by illustrations, loader and transition grid. Take one verb from the brand and run every reveal through it.

## The visible-by-default boot contract

Three layers, each safe on its own [motion-stack §3]:
1. **HTML/CSS at rest.** Nothing is hidden waiting for JS.
2. **A capability flag, never a hide.** The inline gate in [../recipes/boot.html-snippet.html](../recipes/boot.html-snippet.html) sets `<html data-motion="full|reduce">` from the OS setting and a saved in-page choice. The only CSS arm covers `[data-intro]` (clipped), `[data-intro-item]` (shifted by `--intro-shift`, still visible) and `[data-intro-media]` (over-scaled by `--intro-scale`, still visible). A 1ms animation releases them after `--intro-deadline` (2s), even if no JS arrives.
3. **All motion inside `gsap.matchMedia('(prefers-reduced-motion: no-preference)')`.** Below-the-fold reveals are lazily armed: the start state is created in `onEnter`, so a trigger that never fires leaves content visible. motion-core.js also skips anything on screen at boot and anything reached by an anchor jump or a fling faster than 3000px/s.

Measured cost (recipe tests, Chromium 145): the heading's LCP entry lands when the intro ends, about boot + 1.3s. motion-core.js shows the intro at rest if the module boots later than 800ms (`introMaxStart`), for a worst-case LCP of about 2.1s. Put `data-intro` on the heading, never on the LCP image. Never start the LCP element at opacity 0: Chromium drops `opacity: 0` elements from LCP candidacy, and a documented opacity reveal delayed LCP by about 6s [usability-a11y-perf §2].

What winners get wrong (never copy):
- Content hidden until JS or a class arrives: champions-for-good (`visibility: hidden` until `.fonts-loaded`), cartier-watches-wonders-2025 (`.st-char` at opacity 0 in CSS), mindmarket (tile copy at opacity 0 until `.is-inview`), iyo (the body at `autoAlpha 0` until the app boots), pacome-pertant-portfolio (gallery tiles at opacity 0 and scale .5 in CSS), maxima-therapy (an SSR overlay with no noscript fallback).
- Masks that shave glyphs mid-flight: fluid-glass (desktop_02 caught descenders clipped), aim-ai-modernism-of-kharkiv (an x-height sliced flat). motion-core.css pads `.rv-line-mask` by 0.12em and cancels it with negative margins, measured at 0px layout shift.
- The safe winner pattern: lando-norris applies its line clip from JS, so no-JS still shows the text.

CSS scroll-driven animation (`animation-timeline: view()`, 4/51 [probe]; san-rita on inner pages) must start from a readable 0% keyframe, because Firefox stable and screenshot passes render that keyframe: `inset(10%)`, not `inset(100%)`; `scale(1.12)`, not `opacity: 0`. Gate it in `@supports` and `@media (prefers-reduced-motion: no-preference)` yourself: the tokens.css safety net does not stop it.

## Technique catalog

### Masked line reveal
- Seen on at least 13 teardowns: fluid-glass, gil-huybrecht, dont-board-me, leo-parpeix-portfolio-2026, era-residence, shed, lama-lama-2, aim-ai-modernism-of-kharkiv, odd-ritual, the-watch, opal-tadpole, lando-norris, akaru-2.
- Numbers: lines rise from `yPercent` 100-120 inside `overflow: clip` masks over 0.8-1.2s, out-expo or power3/4.out, 0.08-0.15s per line.
- Variants worth the effort: an alternating ±5% x offset per line (leo-parpeix-portfolio-2026); a 30deg un-rotate from the left edge (dont-board-me); a line clip that opens while a colour block sweeps off it (lando-norris).
- Split headings only; split paragraphs can lose their accessible name [motion-stack §4.2]. Revert the split on complete.
- Recipe: `data-reveal="lines"` and `data-intro` in [../recipes/motion-core.js](../recipes/motion-core.js).

### Clip and scale image reveal
- clip-path is on 29/51 [probe]. The frame un-clips from a partial inset while the media settles from about 1.18 to 1 over 1.2-1.6s on out-expo.
- Counter-motion is the premium detail: akaru-2 grows the box while the image scales down (box .6 to 1, image 1.4 to 1); bennett-clive slides the wrapper up while the inner figure slides down, so the picture holds still.
- Start partly clipped (`inset(14% 10%)`), so a frozen frame still shows the image. Both ends must be `inset()`: GSAP cannot interpolate from `none`.
- Recipe: `data-reveal="image"`.

### Pinned scrub
- A sticky stage inside a taller track, with progress mapped to one timeline on ease `"none"` (sticky on 20/51 [probe]).
- Keep extra scroll ≤ 1.5 viewports per pin; longer reads as scroll-jacking [motion-stack §4.5]. Animate the pinned element's children, never the pinned element.
- Hero-to-section framing (full bleed to inset card, image counter-scaling inside) is the most repeated aperture move [elements-catalog §2.8 S3]. GSAP and CSS-only versions: [motion-stack §4.6].

### Horizontal track
- lando-norris sets the section height to track width minus viewport width and hangs per-image drift on `containerAnimation`; akaru-2 scrubs a 14-unit paused timeline from a sticky wrapper.
- The container tween must be linear; pins and snap do not work on `containerAnimation` children.
- Below 60em, under reduced motion and without JS, it stays a native, snap-aligned, keyboard-scrollable row or stack; focus moving into an off-screen panel scrolls to it.
- Recipe: `data-pin="horizontal"` with `pinMinWidth`, `--pin-gap`, `--pin-pad`, `--pin-panel-w`.

### Stacking cards and sheets
- Seen on akaru-2, dont-board-me, mindmarket, odd-ritual, made-with-gsap-1, maxima-therapy, thelinestudio-com.
- CSS sticky does the stacking; JS only recedes the covered card (scale .94 plus a shade overlay at opacity .35). Animate overlay opacity, never `filter: brightness()` on a large layer.
- Do not copy odd-ritual's Barba leave, which animates `marginTop` (layout thrash).
- Recipe: `data-stack` with `--stack-top`, `--stack-step`, `--stack-gap`, `--stack-shade-color`.

### Marquee
- 13 teardown motion sections include one: CSS loops of 30s and 100s (lando-norris), 60s (floema), 40s (pacome-pertant-portfolio).
- Constant pixel speed (duration = group width / px per second), `translate` only, a velocity boost that decays; a direction flip is optional (vast).
- Any loop that runs longer than 5s needs a real pause button (WCAG 2.2.2). Hover-pause alone fails keyboard and touch; shed pauses its header marquee on hover and no button is recorded.
- Recipe: `data-marquee`, `data-marquee-speed`, `data-marquee-toggle`, `--marquee-gap`.

### Parallax
- 27 teardown motion sections mention parallax. The version to keep is parallax inside a frame [elements-catalog §2.5 G5].
- Numbers: odd-ritual moves images `yPercent` 0-20 scrubbed from `clamp(top bottom)`; era-residence runs -15 to 15 and a differential hero where text travels 1.25x the image; fluid-glass cards measure 0.91/1.0/1.09x relative speed. Travel 0.1-0.2 of the viewport and over-scale the media so the frame edge never shows.
- Recipe: `data-parallax="0.15"` (positive lags and reads deeper, negative leads).

### Colour and read-state scrub
- Colour that changes with position, instead of content that appears: lando-norris scrubs the WebGL background per section and mirrors it to `body`; tracing-art tints white to #DAE2E8 at a chapter boundary; opal-tadpole fades its render out, re-themes on a .48s beat while the render is invisible, and fades it back.
- Read-state fills mark progress through a statement on at least 8 winners (vast, opal-tadpole, terminal-industries, pacome-pertant-portfolio, steven-com, the-watch, iyo, dropbox-brand).
- Crafted form: vast keeps the base copy visible in a dim tone and fills a duplicate word by word, so nothing is ever unreadable. Floor the dim state at a readable contrast; steven-com's `autoAlpha 0.1` start is too faint.
- Floor numbers: the dim state holds at least 4.5:1 contrast for text under 24px and 3:1 for display text 24px and up (WCAG 1.4.3). Use a tonal step off the ink, not opacity 0.1.
- Build with SplitText words and a scrubbed timeline, or `animation-timeline: view()` from a readable 0% keyframe. Scrub a colour per section with one ScrollTrigger per section writing a custom property.

### Scramble and decode
- Labels resolve through random glyphs: artefakt about 0.2s per char with a 0.01-0.03s stagger; depo-luxe 0.8s per swap; hubtown scrambles over a width-reserving invisible copy so the layout never jumps.
- Keep it to one or two characters on UI [elements-catalog §2.2 M4]. Preserve the accessible name. Never on body copy. Scramble in the brand's own face: a monospace scramble layer turns into the "monospace as house voice" tell.

### Image sequences
- opal-tadpole (321 frames), terminal-industries (410), son-daven (120), shader-development-studio (AVIF sprite sheets).
- Canvas `drawImage` with cover math, frame index from scroll, snap to whole frames, redraw only when the index changes and the frame has decoded. Budget the bytes before choosing it.

### Preloader
- No preloader: champions-for-good, dropbox-brand, fluid-glass, iyo and made-with-gsap-1 let the hero intro do the job.
- Honest progress tied to real loads: brunos-portfolio's ring chases real progress; lama-lama-2 weights 90% of its counter to component instances; gil-huybrecht counts NN% while textures and video preload; akaru-2 waits for `document.fonts.ready` and every GLB promise; everswap's diamond hole grows with load and exposes the live scene; shader-development-studio's boot bar tracks video and sprite loading.
- Fake: era-residence drives a progress bar with a stepped CustomEase over 4s of timed "loading". That is the fake-progress tell.
- The best loaders become the first content: shed's window fast-cuts project photos, then scales to full bleed as the hero; son-daven re-parents the loader wordmark into the hero slot with Flip over 1.8s; terminal-industries splits its panels with counter-parallax over 1.2s expo.inOut.
- Rules:
  - JS only, first visit only (a sessionStorage flag inside try/catch), skipped under reduced motion, and skippable with a click or Esc.
  - Weighted XHR progress that only increases, a hard cap of 4s, and a CSS deadline that removes the layer if JS dies.
  - Scope it to the scene region when only the canvas needs to wait, so nav, text and CTA are live at first paint.
  - Expose it as `role="progressbar"` with `aria-valuenow`, or `aria-hidden` when the content is already available [usability-a11y-perf §3.6].
  - No recipe file ships a loader; the pattern is in [motion-stack §4.12]. Loader and intro-gate catalog: [./interaction.md](./interaction.md) section 6.

### Page transitions
- **Multi-page site:** `@view-transition { navigation: auto; }`, `data-vt-share` shared elements, a wipe-over-recede root animation on `--dur-4` / `--dur-5`, and a "back" type that reverses direction. Firefox navigates instantly, which is the intended fallback. Recipe: [../recipes/page-transitions.css](../recipes/page-transitions.css) plus [../recipes/page-transitions.js](../recipes/page-transitions.js) as a classic script in `<head>`.
- **Persistent WebGL, audio or Lenis state:** Taxi (artefakt, iyo, lando-norris, siena-film-foundation; current 1.9.1) or Swup (lama-lama-2, mindmarket; build on 4.10 with `native: true`), with same-document View Transitions inside and a curtain fallback [motion-stack §4.11]. `window.pageTransitions.swap()` wraps the update.
- **Barba** (era-residence, odd-ritual, son-daven, vast) has had no npm release since 2024-08: existing codebases only.
- **Timing seen:** fades of 0.15-0.2s with a background switch so the swap never flashes (iyo, artefakt); curtains of 1.2s on expo.inOut or power3.inOut (terminal-industries, akaru-2); a WebGL cell cover of .65s in, .25s hold, .65s out (lama-lama-2). Keep each leg 0.5-0.7s and overlap the legs. Chrome skips cross-document transitions after 4s, so prerender with speculation rules.
- **The freshest move is a shared element:** siena-film-foundation re-parents a title with Flip across a Taxi navigation; [elements-catalog §2.3 T1] returns a product image to its exact grid cell.

### Micro-motion
- Hover starts responding within 250ms. Cursor, hover, menu and button patterns in full: [./interaction.md](./interaction.md) sections 3-6.
- Winners' crafted hovers: a weight drop plus a tonal step (active-theory-v6: 700 to 400 and white over 0.4s); sibling dimming (fluid-glass's menu at `color-mix` 40%, odd-ritual's siblings to a tonal grey); a row fill or invert (artefakt, shed, siena-film-foundation); a label roll inside a static box, two stacked copies moved `yPercent -100` (champions-for-good, fluid-glass, zentry, made-with-gsap-1, oryzo-ai, lando-norris).
- Cursor: `cursor: none` on only 2/51 [probe]. Winners keep the native pointer and add a label chip or small follower; gil-huybrecht's label trails at +16px with `quickTo` over 0.35s on power3.
- Recipes: magnetic label with a static box, [../recipes/magnetic.js](../recipes/magnetic.js); WebGL hover warp, [../recipes/webgl-image-hover.js](../recipes/webgl-image-hover.js); hero object with pointer parallax and a scroll camera, [../recipes/three-hero.js](../recipes/three-hero.js).

## Reduced motion

What winners do: 11/51 carry `prefers-reduced-motion` rules [probe]. About five gate part of their motion, and none gates all of it:
- thelinestudio-com wraps every CSS transition in `no-preference` (82 rules), and shed does the same (45 rules). Neither site's JS checks the setting, so their preloaders, intros and scrubs still run.
- vast multiplies every CSS duration by a `--motion` variable that reduce sets to 0. Its GSAP tweens ignore the variable.
- the-renaissance-edition disables its drawings and `::view-transition` animations (9 blocks) and sets its pointer-follow lerp to 1. The teardown did not verify whether its WebGL intro is skipped.
- champions-for-good gates its scroll entrances behind `gsap.matchMedia('(prefers-reduced-motion: no-preference) and (min-width: 992px)')`, but its intro skid, transition balls and Lenis stay ungated.
- Most others have nothing: lando-norris's only check lives inside Webflow's runtime, and gil-huybrecht reads the flag into state that nothing consumes.

What to ship ([motion-stack §6.6]; all of it is wired in the recipes):
- Lenis at lerp 1 (`respectReducedMotion`), every `matchMedia` branch reverted, no pins, no parallax, the horizontal track as a native scroller, the marquee static and scrollable, cursor follower and magnet off, View Transition pseudo-elements at `animation: none`.
- Colour, opacity, focus and open/close still change, instantly or as crossfades of 200ms or less. tokens.css collapses `--dur-3` through `--dur-6` to `--dur-2` and zeroes the staggers.
- An in-page toggle (`[data-motion-toggle]`, saved as `localStorage` "motion") so a viewer on a full-motion OS can opt out. The `motionchange` event lets WebGL and video follow.
- Autoplaying loops longer than 5s get a pause control (WCAG 2.2.2).

## Crafted vs slop

| Award habit | Slop version | Crafted version |
|---|---|---|
| Reveal on scroll | Content at opacity 0 or hidden until a class or observer fires (cartier-watches-wonders-2025, mindmarket, iyo, champions-for-good) | Lazy-armed JS start state created in `onEnter`; y, clip or scale, never opacity to 0 (`data-reveal`) |
| Masked line rise | Tight leading slices descenders mid-flight (fluid-glass, aim-ai-modernism-of-kharkiv) | Mask padded 0.12em with cancelling margins (motion-core.css); split reverted on complete |
| Preloader | A timer counter or stepped fake bar (era-residence, 4s), often on a cream surface | Weighted real progress with a 4s cap and a CSS deadline, on the brand's own surface; or no loader (5 winners) |
| Link hover | An underline that grows, wipes or retracts (aim-ai-modernism-of-kharkiv, bennett-clive, cartier-watches-wonders-2025, david-whyte-experience, dont-board-me, leo-parpeix-portfolio-2026, thelinestudio-com) | A tonal colour or weight step, sibling dimming, or a label roll inside a static box. Inline body links keep a static underline |
| Button hover | The box scales or lifts with elastic (maxima-therapy's scale 1.1 `elastic.out`, messenger's tiles) | Box still; the fill steps tonally; the label drifts ≤ 6px ([../recipes/magnetic.js](../recipes/magnetic.js)) |
| Card hover | The card lifts or fans out with a springy scale (lando-norris's card fan) | The image scales 1.03-1.1 inside its clip (fluid-glass: 1.1 over 1s), or the grid track grows [elements-catalog §2.4 H6] |
| Overshoot | `back.out` or `elastic` on UI text and controls | `--ease-out-expo` or `--ease-out-quart`; overshoot only on one illustrative object in a toy world |
| Motion colour | A saturated accent on the leading edge of every reveal (lando-norris's lime blocks, terminal-industries's lime sweep) | The same leading-edge idea in a tonal step off the ink, or the brand's own material colour |
| Animated background | One fixed loop trailing behind every section and the nav | Background state that changes per section (colour scrub), or no fixed layer |
| Grain | An animated grain canvas fixed over the whole page, text included [motion-stack §7] | Grain on the substrate only, behind the text |
| Marquee | An infinite loop with hover-pause only | Constant px/s, a velocity boost, a real pause button (`data-marquee-toggle`) |
| Smooth scroll | Always on, whatever the OS setting (72 of 77 probed Lenis installs lack `respectReducedMotion`) | Lenis 1.3.26 at lerp 0.1, off under reduce, plus an in-page toggle |
| Pins and snap | Pins over 1.5 viewports; snap on reading content | Pins ≤ 1.5 viewports; snap only on scene or relay sites |
| Cursor | `cursor: none` plus a lagging blob | The native pointer plus a label chip on `(hover: hover) and (pointer: fine)` |
| Fill and progress bars | `scaleX` or `scaleY` on a rounded bar, so the caps flip from round to square mid-move, or a fill that stops short of its track | Animate `clip-path: inset()` or `width` on a bar with stable caps, fill the full track, ease on `--ease-out-expo` or `linear` when it mirrors real progress |
| Read-state fill | Unread words at `autoAlpha 0.1` (steven-com) | A dim tonal step that still passes 4.5:1 (text under 24px) or 3:1 (display text); the fill is a second tonal step |
| Scramble | A monospace glyph soup over every label | One or two characters, in the brand face, on UI labels only, with the accessible name kept |
| Section entrances | Every section fades up the same way, or nothing moves at all ("dead") | One signature per viewport, quiet shared entrances (`data-reveal="settle"`) elsewhere, plus authored hovers and a responsive nav |
| React reveals | `initial={{ opacity: 0 }}`, which Motion renders into the server HTML | Animate `y`, clip or scale from a visible state, or skip `initial` on SSR content |

## Exemplars

- **lando-norris**: the line clip with a colour block leaving at half-time, the pinned horizontal track with `containerAnimation` drift, the per-section background colour scrub. Swap the lime for a tonal step.
- **era-residence**: a complete motion token system (400/800/1200, stagger .1, five named eases, exits three times faster). Study the system; skip the fake loader.
- **fluid-glass**: one easing family for the whole site; big surfaces move before their contents; a masked line rise whose clipped descenders show why masks need padding.
- **thelinestudio-com**: two registers kept apart, stepped frame blinks for type and heavy rotated sheet throws for surfaces; every CSS transition sits inside a reduced-motion query (its JS does not check the setting).
- **terminal-industries**: a scrubbed film as the conductor, with titles slaved to the same progress value.
- **vast**: a read-state word fill over visible base copy; one `--motion` multiplier as the CSS reduced-motion switch (extend it to GSAP, which vast did not).
- **zentry**: the frame leads (text at +0.4s) and the words snap on inside a rigid 3D slab; slow decelerating entrances (1-1.6s) against 0.5s power2.in title exits.
- **steven-com**: two clocks, a slow WebGL world and fast DOM type that lands inside it.
- **siena-film-foundation**: velocity-driven blur, an always-on magnet snap, Flip shared elements across Taxi routes.
- **immersive-garden-website**: scroll velocity as a design input; hard scrolling switches the page to an index.
- **gil-huybrecht**: an honest percentage loader, one entrance, then stillness.
- **messenger**: quantized, boiling motion for drawn graphics over a smooth camera.

## Evidence

- Teardowns: `data/teardowns/<slug>.json` for all 51 sites, `motion` block (smooth_scroll, preloader, intro_sequence, scroll_techniques, text_animation, image_animation, page_transitions, hover_micro, cursor, easing_curves, duration_range_ms, stagger_ms, choreography_notes) and `performance_accessibility.reduced_motion`. Counts such as "36/51" and "13 teardown motion sections" were tallied from those fields on 2026-09-25; keyword tallies are lower bounds.
- Digest: `evidence/digests/motion.md` (the same motion blocks, concatenated across the 51 sites).
- [probe]: `data/probe_summary.json` (easings_by_sites, durations_by_sites, css_usage_by_sites, css_features_by_sites, libraries_by_sites, sites_with_reduced_motion_rules). CSS figures cover same-origin stylesheets only; GSAP timing comes from teardown bundle greps. The probe's view-transitions flag (4 sites) was confirmed by teardowns on 1.
- [motion-stack]: `data/research/motion-stack.md` (library versions, browser support, the SOTD n=117 bundle probe, ease census, recipes, failure modes).
- [elements-catalog]: `data/research/elements-catalog.md` (43 timed Awwwards Element videos, pattern taxonomy, house-law reconciliation).
- [usability-a11y-perf]: `data/research/usability-a11y-perf.md` (dev-score correlations, the LCP opacity mechanism, the reduced-motion architecture in §3.1).
- [stats]: `data/stats.md`, recent_2024_plus cut (575 sites): tags_top and dev_score_means.
- GSAP 3.15 `easeReverse` was checked against the official GSAP docs (gsap.com, via context7) on 2026-09-25.
- Recipes: `recipes/tokens.css`, `recipes/motion-core.js`, `recipes/motion-core.css`, `recipes/boot.html-snippet.html`, `recipes/page-transitions.css`, `recipes/page-transitions.js`, `recipes/magnetic.js`, `recipes/webgl-image-hover.js`, `recipes/three-hero.js`, demos in `recipes/demo/`. Their headers report tests in Chromium 145 only; Firefox and WebKit were not run.
- Per-site summaries: [./casebook.md](./casebook.md).
- Keyword tallies (velocity 18, parallax 27-28, marquee 13, elastic/back 21, stepped 15, text splitting about 30) are regex counts over the teardown `motion` blocks, so they are lower bounds and include passing mentions.
- Conflicts inside teardowns, resolved conservatively: zentry's choreography notes say its exits run 0.5s power2.in, but its audit notes put the BigTitle exit at 1s power4.out. fluid-glass's notes say its page scales .3s after rising, while its intro code shows .4s.
- Not verified: LCP treatment of clip-path-hidden hero text beyond the recipe measurements; Lenis `velocity` units (the skew snippet uses ScrollTrigger `getVelocity()` in px/s instead); whether any of the 13 marquee sites other than those named ship a pause control; the velocity-skew snippet has not been run in the recipe QA harness.
