# Proven implementation patterns

Patterns that worked in tested builds. They are structures, not looks: apply them to your concept.
(Do not reuse a tested build's concept; your concept must come from your subject.)

## 1. The driver module (one variable → every concept-bearing visual)

Concept sites feel inevitable when everything is lit/colored/positioned by the same source.
Write one module that owns the variable and fans it out:

```ts
// src/motion/<concept>.ts
import { onPage, onScroll, setBackground } from '@/engine';

const FRAG = /* glsl */ `...`;                    // reads uniform float uState (see webgl.md)
const map = (p: number) => ({ /* derive everything from p: dark, label, uniform, transform... */ });

const uniforms = { uState: { value: 0 } };       // the shader reads these objects by reference
let targets: HTMLElement[] = [];
let current = 0;                                 // latest driver value (the idle hookup reads it)
function apply(p: number, drift = 0) {           // drift: the idle input, see below
  const s = map(p);                              // discrete state from the real value only,
  const c = drift ? map(p + drift) : s;          // so a drift near a threshold never flickers
  document.documentElement.classList.toggle('is-dark', s.dark);    // global ink switch
  const label = document.querySelector('[data-label]');
  if (label && label.textContent !== s.label) label.textContent = s.label; // UI that narrates the state
  uniforms.uState.value = c.uniform;                               // GL follows the same variable
  for (const el of targets) el.style.transform = c.transform;      // concept transforms (cheap props only)
}
// A page can pin its state (404 at night, a case page in its own chapter):
const pinned = () => { const v = document.querySelector<HTMLElement>('[data-state]')?.dataset.state; return v ? +v : null; };

export function startConcept() {                 // call from setupMotion
  setBackground(FRAG, uniforms);                 // returns null without GL: the static fallback takes over
  onScroll(({ progress }) => apply((current = pinned() ?? progress)));
  onPage(() => {
    targets = [...document.querySelectorAll<HTMLElement>('[data-concept]')];
    apply((current = pinned() ?? 0));
    return () => { targets = []; };
  });
}
```
Call `startConcept()` once from `setupMotion`. Drivers can be scroll progress (time of day,
depth, temperature, zoom), the pointer (light source, wind), a chapter index (pinned sections),
real time (the local hour, which personalizes revisits), or audio level (opt-in).

Add a little pointer influence on top of the scroll driver (for example ±12% of the light
angle). That way the signature reacts before the visitor scrolls, which is the first thing
people try.

Add an **idle input** too: a slow term from `gsap.ticker` time (a drifting light, a second
hand, a breathing exposure) passed to `apply` as `drift`, small enough that the state stays
readable. With it, the concept keeps moving while the visitor reads, instead of freezing the
moment they stop scrolling. `references/motion.md` ("Idle state") has the rules, the `idle`
module and the ticker hookup, which pauses off screen and stays at rest under reduced motion.

## 2. Sticky stage hero (the signature plays while the hero is in view)

If the signature is scroll-driven, give it scroll distance while the hero is still on screen:
```css
.hero { height: 190svh; }                         /* 90svh of scroll belongs to the hero */
.hero__stage { position: sticky; top: 0; height: 100svh; overflow: clip; container-type: inline-size; }
```
Cheaper and more robust than a GSAP pin. Use 150svh on phones.

## 3. Static fallbacks per section

Sections declare their state in markup (`data-sky="dawn"`, `data-chapter="2"`, `data-tone="dark"`).
With GL on, they are transparent over the canvas; without GL (reduced motion, no WebGL, Save-Data)
each paints its own static version:
```css
html:not(.gl-on) [data-sky='dawn'] { background: linear-gradient(var(--dawn-top), var(--dawn-bottom)); }
html:not(.gl-on) [data-sky='night'] { background: var(--night); }
```
The reduced-motion screenshot then looks designed, not broken.

## 4. Decorative text copies (shadows, reflections, outlines, echoes)

```html
<div class="name">
  <h1 class="name__word" data-split="chars" data-intro>Name</h1>
  <span class="name__echo" aria-hidden="true">Name</span>   <!-- sibling, never inside the h1 -->
</div>
```
A projected shadow: `transform-origin: 50% 100%; transform: scaleY(-L) skewX(Sdeg)`, a mask
gradient fading with distance, a static `filter: blur(1-2px)`; drive L and S from the driver.
Transforms only: it costs nothing per frame.

## 5. Loader → UI handoff

Put the loader's counter exactly where a persistent UI element lives (a corner clock, a page
counter, a progress line), in the same type style. When the loader background fades, the counter
"becomes" the UI. `setLoaderFormat()` turns 0→100 into the concept's unit (a time, a year, a depth).
`setLoaderExit()` owns the choreography. Keep progress + exit ≤ 2.6 s (`loaderMs` in the shoot report).

## 6. Frame that steps aside

```ts
// in setupMotion
let last = 0;
onScroll(({ y }) => {
  if (Math.abs(y - last) < 4) return;
  document.documentElement.classList.toggle('frame-away', y > 160 && y > last);
  last = y;
});
```
```css
html.frame-away .frame__tl, html.frame-away .frame__tr { translate: 0 -220%; }
.frame__tl, .frame__tr { transition: translate 0.6s cubic-bezier(0.16, 1, 0.3, 1); }
```
Use the individual `translate` property so it never fights GSAP transforms.

## 7. Index as concept (the work list is part of the idea)

A tested build presented projects as days on a calendar because its concept was about time: the index
format itself expressed the concept (a frame wall, a contact sheet, a timetable, a map, a
dial). On phones, collapse to only the meaningful entries in a single column.

## 8. Transitions that belong to the concept

A tested build about light used "a shadow passes": a dark band with a soft gradient leading edge
sweeping in the light's direction. Derive yours from the concept's physics (a frame closing, a page turning,
film advancing, water rising) and keep it ≤ 1 s each way.
