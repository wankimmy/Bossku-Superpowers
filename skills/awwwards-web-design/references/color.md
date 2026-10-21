# Color and surface

Last updated: 2026-09-25

Use this when: choosing a site's palette, surfaces, section colour changes, grain and gradients, or auditing a build for colour slop and contrast.

## Rules

1. Ship two anchors (a near-black and a near-white on one hue angle) plus at most one owned colour. 246 of the 275 recent winners that record a palette list exactly two colours, and none lists more [stats].
2. Pick dark, light or coloured fields by what carries the chroma: dark when footage, client work or a render brings the colour; light when a lit object or paper subject does; flat colour fields only when the brand is 2D or illustrated (section 2).
3. Tint both anchors toward the brand's own hue or keep them neutral. Never ship the cool blue-charcoal dark or a cream sheet by default. Winners' darks are neutral in 130 of 167 recorded cases and cool in only 21 [stats*].
4. The owned colour lives in a field, an object, a material or a light, never sprayed on chips, dots and eyebrow labels. UI chrome gets tonal steps of ink and ground. Of 51 audited winners, only 3 carry their colour mainly as a CTA-and-dot accent, and all 3 use lime (section 4).
5. Every saturated field carries a same-hue ink at OKLCH L 0.25-0.30. White text fails 4.5:1 on any field lighter than about OKLCH L 0.56, which covers most brand oranges, reds, greens and sky blues (computed). 8 of the 51 teardowns log brand-colour text/field pairs that fail because the two sit too close in lightness (section 10).
6. Show at most two hues in one viewport, plus imagery (champions-for-good, slosh-seltzer). The one exception is a palette that is itself the subject, such as a brand identity mosaic, and even there every field carries its own same-hue ink (dropbox-brand).
7. A section colour change is an event: a scrubbed hand-off across empty space, or a new colour that arrives as a thing (sheet, disc, curtain, shaped seam). A flat butt-join is not an event. 37 of 51 winners shift section colour (51 teardowns).
8. Text never interpolates. The ground morphs and the ink flips once. Check contrast at the midpoint of every morph (lando-norris failed there at 1.5:1).
9. Grade imagery into the palette with one LUT, duotone, multiply layer or dither, so pictures and page read as one set [imagery §2.1].
10. Grain sits on the substrate or inside the WebGL post pass at strength 0.03-0.07, masked by luminance and reduced on mobile. It never sits as a sheet over text. Only 1 of 51 winners layers CSS noise over type, and it measures near-invisible (son-daven).
11. A gradient describes light: one hue, lightness steps only, a directional falloff and dithering. Never a two-hue glow, a corner blob or gradient-filled text.
12. Secondary text is a solid mixed token at 4.5:1 or better. Alpha is for lines and fills. Alpha-dimmed text is the second most common contrast failure in the teardowns.
13. The contrast floor holds everywhere, over media included: 4.5:1 for body and UI text, 3:1 for text of at least 24px and for control and focus boundaries. Measure the worst frame, not the average [usability-a11y-perf §D].
14. Tokens go raw anchors → semantic `--bg/--fg` → derived mixes, and the derived mixes are declared again under every theme scope (section 9).

## 1. What winners actually do

**Palettes are tiny.** Awwwards records a palette for 275 of the 575 winners from 2024 on. Of those, 246 list 2 colours, 29 list 1 and none lists 3 [stats]. The base structure (n=275) splits into dark+light contrast pairs 86, dark-dominant 79, mid-tone 66 and light-dominant 44 [stats]. The dark-leaning bases outnumber the light-leaning ones by almost two to one.

**Anchors are near-black and near-white.** Hue families by recorded entry are near-black 152, near-white 115, blue 48, neutral grey 41, orange 38, red 36, tinted off-white 23, green 22, yellow 17, cyan 15, magenta 10 and violet 4 [stats]. Among the recorded lights (L > 0.85), 66 of 155 are pure `#fff`, 99 are neutral within about 5 levels, 44 lean warm and 11 lean cool. Among the darks (L < 0.15), 62 of 167 are pure `#000`, 130 are neutral, 21 cool and 13 warm [stats*].

**Accents are unique per site.** 105 of those palettes contain a saturated mid-lightness colour. The 126 such colours are all distinct: no two winners share an accent hex [stats*]. By hue they split blue 33, red 31, orange 19, yellow 15, green 13, magenta 8, cyan 5 and violet 2. Violet is the rarest winning accent, and the law bans it as a default [stats*].

**In the 51 teardowns**, the colour mode splits into section-shifting 37, single dark 9, light 3 and mixed 2. The primary base is dark on 19 sites (17 near-black, 7 of them pure `#000`, plus 2 deep greens), near-white on 22 (7 pure `#fff`, 9 warm off-white) and a mid-tone or coloured field on 10 (51 teardowns, color.base).

**The measured CSS is quiet.** `mix-blend-mode` appears on 17/51 sites, `backdrop-filter` on 16/51 and filters on 18/51, while oklch/color-mix appear on only 10/51 [probe]. 41/51 run WebGL2 [probe], and most of the colour work (grades, fog, grain) happens in shaders rather than in CSS.

## 2. Dark or light: decide by direction

| Direction | Winners do | Evidence |
|---|---|---|
| Footage-led (film, production, reels) | Black ground with white or warm-white ink, so the film is the only chroma | (artefakt), (depo-luxe), (siena-film-foundation), (gil-huybrecht). Counter-case: (bennett-clive) stays white and lets a difference-blend nav carry the type |
| Real-time 3D studio or tech showcase | Near-black on neutral, green or warm-brown darks; colour arrives as scene light | (steven-com) `#121212`, (lama-lama-2) `#1A1C1C`, (oryzo-ai) `#100904`, (shader-development-studio) `#0a0a0a` |
| Lit luxury object | A studio value: light grey for the exterior, relit to near-black for the "inside" chapter | (the-watch) `#ebebeb` to `#0a0a0a`; (cartier-watches-wonders-2025) alternates white and black fades per universe |
| Product with finishes | The theme follows the finish or the page | (opal-tadpole): the black colourway turns the page black; (iyo): dark home, pale `#DDDEE3` configurator |
| Culture, museum, archive | White or a fog grey, with the artworks as the only colour | (tracing-art) pure white "no cream"; (aim-ai-modernism-of-kharkiv); (david-whyte-experience) fog `#E6E7E2` |
| Architecture, B2B manufacturing | Light neutral sections with dark floors for weight | (fluid-glass), (floema), (vast), (terminal-industries) |
| Illustrated, playful, kids, health, drinks | Saturated flat fields in strict pairs | (maxima-therapy), (champions-for-good), (slosh-seltzer), (ponpon-mania), (dont-board-me) |

Decision: first list what brings colour into the page (media, product, illustration or brand identity). If media brings it, keep the ground neutral and near-black. If a lit object brings it, choose the studio value the object reads best on, and relight rather than recolour for mood changes (the-watch dims the IBL to 15% in the same ScrollTrigger that fades the DOM ground). Choose coloured fields only when the identity or illustration system owns those colours.

## 3. The two anchors

**Near-black.** Winners pick neutral (`#101010` iyo, `#121212` steven-com, `#0a0a0a` pacome-pertant-portfolio) or a hue that belongs to the brand: green-black (lama-lama-2, leo-parpeix-portfolio-2026 ink `#022016` tied to its theme-color `#083D2A`), warm brown-black (oryzo-ai `#100904`) or plum-black (brunos-portfolio `#1f1619`). The one navy base (hubtown `#020A19`) sits right next to the generic dark-SaaS blue, and its teardown says it earns that only because the blue is emissive light in a lit world. Where a dark UI drifts to indigo plus periwinkle, the teardown flags it (active-theory-v6 work view, zentry's violet `#5542FF`).

**Near-white.** Winners use pure white (tracing-art, shed, odd-ritual, opal-tadpole), a neutral grey that is lit as a material (immersive-garden-website `#e8e8e8`, which reads premium only because it is a shaded plaster relief), or an off-white. 9 of 51 bases are warm off-whites, the law's cream flag: aim-ai-modernism-of-kharkiv, akaru-2, dont-board-me, era-residence, floema, fluid-glass, lando-norris, mindmarket and vast. The good versions tie the tint to something real. Floema matches its hero fog (`#f3efea`) to the page, so product planes emerge from the background. Lando's off-white leans toward its olive ink and lime livery. Era's bone is the weak part of that site, and its powder-sky field is the strong one (section 5).

**Ink.** On the 22 light grounds, 6 winners use a clearly hue-bearing ink instead of a near-`#000`: olive-black `#282c20` (lando-norris), dark green `#052424` (terminal-industries), navy `#17233B` (era-residence), forest `#2d3329` (san-rita), green-black `#022016` (leo-parpeix-portfolio-2026) and red (dont-board-me). Several more tint it faintly (floema `#241f21`, mindmarket `#2c2e2a`). The greige the-renaissance-edition does the same with olive `#292919`. On dark grounds the ink is often a warm or tinted white: `#FAF7EF` (siena-film-foundation), `#fcf9f3` (shader-development-studio), `#ffedd7` (oryzo-ai), green-tinted `#fbfff4` (everswap).

Decision:
- Choose one hue angle `h` from the brand mark or the graded imagery.
- Set the near-black at OKLCH L 0.12-0.18, C ≤ 0.02 on `h`, and the near-white at L 0.96-0.99, C ≤ 0.01 on `h`, or at pure white.
- Anchor pairs land at 15-19:1.
- Reject the result if `h` falls in 250-290, or if the light reads as cream, unless the subject is literally paper. 250-290 is the indigo-slate band: the law's `#0c0e15` sits at 272 and the gray-100 family at 257-265 (computed).

## 4. Where the accent lives

The law says a saturated accent sprayed on type, dots and buttons is slop, and that the premium accent is tonal. The winners agree more than their award pages suggest. Each of the 51 teardowns was classified by where its strongest chroma mainly sits. Some field-led sites also fill buttons with their field hues (maxima-therapy's orange and blue pills, mindmarket's per-card button colours, zentry's lime pill), and their teardowns flag that part.

| Carrier | Sites | Count |
|---|---|---|
| None in the UI; chroma only from content (film, client work, art, product) | aim-ai-modernism-of-kharkiv, artefakt, bennett-clive, cartier-watches-wonders-2025, depo-luxe, fluid-glass, gil-huybrecht, gq-ap-the-extraordinary-lab, igloo-inc, immersive-garden-website, iyo, lama-lama-2, son-daven, the-renaissance-edition, the-watch, tracing-art | 16 |
| A field or surface (floors, rooms, bands, tiles) | akaru-2, champions-for-good, dont-board-me, dropbox-brand, era-residence, floema, lacoste-polo-factory, maxima-therapy, mindmarket, ponpon-mania, shed, siena-film-foundation, slosh-seltzer, thelinestudio-com, zentry | 15 |
| An object, material or light in a rendered world | active-theory-v6, brunos-portfolio, everswap, hubtown, messenger, oryzo-ai, shader-development-studio, steven-com, the-power-of-storytelling, why-zero | 10 |
| Small UI marks | rationed to one job: opal-tadpole (hover fill only), leo-parpeix-portfolio-2026 (cursor pill), odd-ritual (motion band and hover row, never a button fill), pacome-pertant-portfolio (sticker, under 1%), vast (data markers, never buttons). Tonal: david-whyte-experience (earth tones), san-rita (pale `#e2ffcc`). Sprayed on CTAs and dots: lando-norris, made-with-gsap-1, terminal-industries | 10 |

Findings:
- Only 3 of 51 make the banned move their main colour idea, and all three reach for the same lime (`#d2ff00`, `#C9FE6E`, `#abff02`). Lime CTA plus dots is the winners' own emerging template. Lando's lime is the helmet livery, which is the only reason it works, and its teardown still flags it.
- The strongest colour sites put the hue on a surface: Shed gives each hue "one job and one surface" (blue for sectors, orange for the menu, violet for the cursor). Siena uses red once, at full scale, as the contact floor. Zentry uses its lime as a whole section field or one pill, never as scattered highlights.
- Object-carried accent: in oryzo-ai the cork product is the only saturated object on dark screens; its studio calls the system four values (a cream, a near black, a muted olive, an orange). Steven-com's venture colours appear only as room light, marker strokes and radio fills, never as fills or buttons.
- Content-carried accent: in the-renaissance-edition the hot pink lives on merch props inside the paintings, and the UI stays black and white.

The crafted versions the law allows:
1. **Owned colour as a field.** The field fills a section, room or band, and its text is a same-hue dark ink. Dropbox ships every identity colour with an "on-" ink of the same hue at roughly 20% lightness (`#FAD24B`/`#684505` measures 5.9:1) (dropbox-brand). Floema's collection chips carry ink, not white, and reach 5.56:1 (floema).
2. **Owned colour as an object or light.** Put the chroma in the product render, in the scene's key light, or in hue-tinted ambient occlusion (lacoste-polo-factory ramps its AO to a darker step of the room hue, so the room reads as coloured clay and 2-3 props carry the saturated colour).
3. **Tonal UI.** Hover, active and selected states use ink/ground steps (a label moving from `--fg-2` to `--fg`, a raised surface one step lighter). Steven-com's label steps `#A0A0A0` to `#fff` while the venture colour is drawn as a stroke. The law bounds headline emphasis the same way: a tonal shift, never a colour pop.
4. **Several hues.** Allowed only with a pairing rule. Never show more than 2 colours at once (champions-for-good). Keep one field/type pair per band (slosh-seltzer). Take every hue from one illustration system (mindmarket, ponpon-mania). "Blue AND green AND a warm accent" with no rule is the law's colliding-colour failure.

## 5. Section palettes and colour hand-offs

Winners change the ground in six ways:

| Move | How | Evidence |
|---|---|---|
| Scrubbed hand-off | Section pairs declare from/to tokens; a scrubbed tween interpolates the canvas colour and writes `body.style.backgroundColor` in the same frame | (lando-norris) `data-gl-change-from/to`; (the-watch) DOM ground plus relight in one trigger; (oryzo-ai) the hero plate mixed toward the dark ground: "lights out" |
| Graded scene | Per-scene grade presets (sepia, saturation, bloom) interpolated with scroll | (shader-development-studio), (everswap), (why-zero) |
| Timed flip | A class or token swap with a colour transition of 0.2-1s | (odd-ritual) body flood 0.2s; (made-with-gsap-1) 0.3s + 0.1s delay; (leo-parpeix-portfolio-2026) nav token 0.4s; (opal-tadpole) 0.48s with separate eases for ground and text; (maxima-therapy) 1s; (steven-com) 1s theme crossfade |
| Shaped seam | The boundary has a drawn silhouette that moves | (terminal-industries) notch clip-path scrubbed with scroll, 40px desktop, 20px mobile, inferred to run tab → flat → notch; (son-daven) line-screen comb; (dont-board-me) 1520px circle arc; (slosh-seltzer) liquid fill line; (the-renaissance-edition) torn-paper shader; (lama-lama-2) dithered wipe |
| Sheet over | The new colour is a physical sheet sliding over the old one | (mindmarket) 50px-radius sheets, with the covered hero scaling to 0.8 under a charcoal overlay at progress × 0.4; (made-with-gsap-1) inset sheets with 20-25px radii; (thelinestudio-com) paper cels; (floema) dark floor unrolls with scaleY |
| Transition as colour | The page transition paints the destination's ground | (champions-for-good) balls in the destination theme; (maxima-therapy) fan curtain in the route's main colour; (leo-parpeix-portfolio-2026) disc per destination |

The law objects to one specific failure: a glow or gradient on one screen cut dead at the boundary, where the colour context stops without an event. All six moves above avoid that. Choose one or two moves for the whole site, not a different one per edge.

**The sky trick.** Take the section colour from the imagery itself. Era cuts its architecture renders out along the roofline and sets them on a powder-sky field `#B5CEDB` taken from the renders' own sky, pushed pale, so the brand swatch reads as real sky and the next disc or wash in that colour joins without a seam (era-residence). This is the strongest light-palette idea in the set.

**The chrome follows the ground.** A fixed nav must recolour with the section beneath it. Winners do this three ways:
- per element: each header item reads the `[data-bg]` section under its own centre (era-residence);
- a `--navbar-fg` token on the nav (leo-parpeix-portfolio-2026, which forgets its dark carousel slides and loses the nav there);
- a difference blend, with un-blended duplicates wherever true brand colour must show (opal-tadpole).

Recipe: scrubbed ground with a discrete ink flip. It reuses the GSAP instance from [../recipes/motion-core.js](../recipes/motion-core.js). A colour change is not movement, so it stays on under reduced motion [usability-a11y-perf §B].

```html
<section class="ground" style="--sec-bg:#0a0f0b; --sec-fg:#f4f8f5">…</section>
<section class="ground" style="--sec-bg:#f4f8f5; --sec-fg:#0a0f0b">…</section>
```
```css
.ground { background: var(--sec-bg); color: var(--sec-fg); }          /* no-JS: plain hard cuts */
html.ground-live { background: var(--bg); color: var(--fg); }
html.ground-live .ground { background: transparent; color: inherit; } /* one surface morphs */
```
```js
import { init } from './motion-core.js';                   // a copy of ../recipes/motion-core.js
const { gsap, ScrollTrigger } = init();
const root = document.documentElement;
const secs = [...document.querySelectorAll('.ground')];
const tok = (el, k) => getComputedStyle(el).getPropertyValue(k).trim(); // hex/rgb only: GSAP parses hex, rgb(), hsl()
const hand = [];                                           // filled before use: create() fires onRefresh synchronously
secs.slice(1).forEach((sec) => hand.push(ScrollTrigger.create({
  trigger: sec, start: 'top bottom', end: 'top 40%',        // run the morph across padding, not over copy
  onUpdate: paint, onRefresh: paint,
})));
function paint() {
  let i = -1; hand.forEach((st, j) => { if (st.progress > 0) i = j; }); // last hand-off that has begun
  const from = secs[Math.max(i, 0)], to = i < 0 ? from : secs[i + 1], p = i < 0 ? 0 : hand[i].progress;
  const bg = gsap.utils.interpolate(tok(from, '--sec-bg'), tok(to, '--sec-bg'), p);
  root.style.setProperty('--bg', bg);
  root.style.setProperty('--fg', tok(p < 0.5 ? from : to, '--sec-fg')); // ink flips, never interpolates
  window.dispatchEvent(new CustomEvent('groundchange', { detail: bg })); // WebGL: uniforms.uBg.value.set(bg)
}
root.classList.add('ground-live'); paint();
```

Checks:
- Give each section top padding of at least 30vh, so no text sits on mid-morph values. A dark-to-light morph passes a mid grey where one or both inks drop under 4.5:1. For the section 9 anchors, the oklab midpoint gives 4.2-4.3:1 against both (computed). Lando's 8px labels sat on the mid-morph `#9c9d95` at 1.5:1 (lando-norris).
- Put the ease on the tween, not inside the `scrollTrigger` vars. Lando declares `cubic-bezier(1,0,0.37,1)` there, and GSAP ignores it (lando-norris).
- Timed variant: an IntersectionObserver with `rootMargin: '-50% 0px -50% 0px'` sets `html[data-ground]`, and `html` transitions `background-color .48s cubic-bezier(.39,.575,.565,1), color .48s cubic-bezier(.215,.61,.355,1)` (opal-tadpole's pair of eases).
- A WebGL canvas behind the page takes its clear colour from the page, not black. [../recipes/three-hero.js](../recipes/three-hero.js) `background: 'auto'` reads the first opaque ancestor. Floema matches its fog to the page for the same reason (floema).
- If the ground lives on a fixed canvas, it must visibly react (morph per section, respond to the cursor). A fixed sheet that only trails the scroll is banned, and the nav needs its own treated layer above it.

## 6. Grade imagery into the palette

The palette and the pictures must read as one set. The winners' tools:
- **One LUT over the whole render**: messenger (3D LUT), igloo-inc (tetrahedral LUT plus a diagonal exposure ramp), gq-ap-the-extraordinary-lab (a single composite pass with LUT, grain and chroma).
- **Per-scene grade presets**: shader-development-studio.
- **A pure-CSS duotone**: a `#000` layer at `mix-blend-mode: saturation` plus a `#282c20` layer at `plus-lighter` over each image (lando-norris menu).
- **A multiply "acetate"**: one flat `#ff0000` div in `mix-blend-mode: multiply` turns a multicolour showreel into one brand hue, then peels off to reveal full colour (thelinestudio-com).
- **A two-colour line-screen shader** that reads its two colours from `:root` variables at init (son-daven).
- **The content's own colour, blurred**: the focused film at `blur(100px) scale(2)` under a 25% veil becomes the index backdrop, so the ambient colour always belongs (depo-luxe).
- **Depth fog to paper**: distant images fade toward `vec3(0.97)`, the page colour, instead of toward black (tracing-art).

Decisions:
- Pull the page tokens from the graded set: the darkest shadow becomes the ink, a mid-tone becomes a surface, and one image-native hue becomes the owned colour [imagery §2.1].
- Bake the grade into the assets and use CSS filters only for state changes. The duotone SVG filter is at [imagery §2.2](../data/research/imagery.md). Full treatment catalogue: [./imagery.md](./imagery.md).
- Keep saturated colour inside the image as a story device. It does not transfer to UI chrome [imagery §2.1].

## 7. Texture and grain

What the 51 do:
- **A separate grain layer on 9/51**, and 8 of those keep it inside the WebGL post pass, never as a DOM sheet. Shader-development-studio renders its UI inside the scene, so its grain is luminance-masked instead:
  - cartier-watches-wonders-2025 (`USE_NOISE`)
  - gq-ap-the-extraordinary-lab
  - hubtown (soft-light noise)
  - leo-parpeix-portfolio-2026 (0.07)
  - siena-film-foundation (0.07)
  - shader-development-studio (effective 0.026-0.055)
  - why-zero (0.04)
  - ponpon-mania (behind the comic cards)
- **The one CSS noise sheet over type** is son-daven: `noise.avif`, opacity .1, `soft-light`, z-index max. It measures a std-dev of about 0.9 levels on flat sand, so it is effectively invisible, and its teardown still flags it.
- **Material instead of grain on the rest**: plaster with a noise map (immersive-garden-website), a paper normal map (david-whyte-experience), brush-painted albedo (everswap), cork and wood maps (oryzo-ai), terrain textures (san-rita).
- **Dithering against banding**: blue-noise dithering on long gradients (oryzo-ai, igloo-inc; the-power-of-storytelling loads a blue-noise texture, inferred for the same purpose).

Decisions:
1. Put texture in the substrate first (a material, the paper or the paint), then add grain only where large tonal transitions would band. The law says any large colour transition should carry grain.
2. Grain strength is 0.03-0.07 in a post pass, or 0.04-0.10 opacity for a CSS tile with `soft-light` behind content ([imagery §2.3](../data/research/imagery.md) has the tile recipe with `z-index:-1` and `isolation:isolate`).
3. Mask grain by luminance so it collects in the darks and skips bright type: `g = n * (1.0 - color.rgb); out = color.rgb + g * k` (shader-development-studio).
4. Step it rather than boiling it every frame. Re-seed at 10 steps/s with `hash(uv + floor(uTime*10.)/10.)` (ponpon-mania), and use near-static grain on reading pages (shader-development-studio's noiseVelocity 0.05 for its newspaper scene).
5. Scale it down on small screens: ×0.65 on mobile and ×0.7 at DPR 1 (shader-development-studio), or off below 1025px (leo-parpeix-portfolio-2026).
6. A patterned texture (dots, screen-door, grid) must mean something and stay on dark substrates only. Artefakt's 5px screen-door at opacity .07 and `z-index:-1` sets up its terminal language. Pacome's fixed grid, masked with a 250px blur, bands into visible concentric rings and trails every route. That is the failure: a fixed texture that ignores the content.
7. The law allows one exception: grain masked onto a single display word as a chosen move. Never lay it over body text or controls.

## 8. Gradients done right

The good examples are gradients of light:
- **Igloo** multiplies the frame by a diagonal exposure ramp `mix(0.8, 1.0, (uv.x+uv.y)/2)` and fogs the terrain from `#afb6c7` to `#d1d6e3` with a pow-2 curve. It reads as a photographed sky, not a CSS wash (igloo-inc).
- **Oryzo**'s warm pool is a shader radial from `#0f0804` to `#6d3916` with a `pow(1-d, 4)` falloff and blue-noise dither. It stays in the ground's own hue family, and the product sits in it (oryzo-ai).
- **Mindmarket** shades its path where it folds under itself with same-hue stops `#8ED462` → `#378e43` → `#439745` → `#8ED462`. The gradient is the shading of an object (mindmarket).
- **Opal** fades a 40vh feather in the page colour under the hero and scrubs it out as the hero leaves (opal-tadpole).

Gradients that winners ship but you should not copy:
- a cyan-to-violet distance fog (brunos-portfolio)
- a violet corner glow on a stats card (zentry)
- a near-white to pale-blue `background-clip: text` on the giant headline words, at 1.44-1.63:1 (the-power-of-storytelling)
- a mint-to-white radial wash, flagged as the site's riskiest colour choice (why-zero)

Decisions:
- One hue with lightness steps, or a ramp between the ground and the ink. Never two adjacent saturated hues.
- The falloff has a direction and a motive: a light source, an object it lights, or a horizon. Prefer a linear or angled ramp to a centred radial. A radial blob of the accent from a corner and a halo behind an object are both banned.
- Dither every gradient larger than about a quarter of the viewport with grain or blue noise.
- Make image edges with a feathered `mask-image` on the image, not a colour overlay (law, "Hard image seams").
- Solid text only.

```css
.stage { position: relative; isolation: isolate;
  background: linear-gradient(160deg, oklch(0.24 0.02 var(--h)) 0%, var(--bg) 60%); }   /* key light upper-left, one hue */
.stage::before { content: ""; position: absolute; inset: 0; z-index: -1; pointer-events: none;
  background: url(/tex/grain-256.png) 0 0 / 256px; opacity: .06; mix-blend-mode: soft-light; } /* behind content */
```

## 9. Token recipe

Evidence for the structure:
- **An inversion pair swapped by one class.** Son-daven's `.theme_on-dark` redefines base-0 and base-1000 so a whole section flips (son-daven). Immersive Garden swaps `#030303`/`#e8e8e8` on dark sections (immersive-garden-website).
- **Greys mixed from the two anchors.** `color-mix(in hsl, var(--color--bg) X%, var(--color--text) Y%)`, so one flip drives both themes (steven-com).
- **Glass and dimmed text from color-mix.** `color-mix(in srgb, #0b1012 80%, transparent)` with `blur(2rem)` makes the glass, and `color-mix(currentcolor 40%)` dims menu siblings, across 104 color-mix/oklch uses (fluid-glass).
- **Ink alpha steps for lines and fills.** `#17233B` at 99/4d/1a/0d (era-residence).
- **Same-hue on-colour pairs.** (dropbox-brand)
- **Named material ramps.** brightIvory 25-400 and stoneBrown 100-800 (floema); geology names (vast).
- **A per-route colour record** with main, secondary, tertiary and curtain fields (maxima-therapy).
- **Palette tokens in a shader.** Son-daven reads them once at canvas init, so theme classes never reach the canvas (son-daven). Send colour changes to WebGL as events, as in the section 5 recipe.

No teardown documents an oklch-authored brand palette. Oklch below is a recommendation (rec.): it keeps hue fixed while lightness steps, and color-mix in oklab gives even tonal steps. All current browsers support both.

```css
/* palette.css: pairs with ../recipes/tokens.css (motion and type only, deliberately no palette) */
:root {
  --h: 150;                                    /* ONE hue angle from the brand mark or graded imagery (example) */
  --c-dark:  oklch(0.16 0.012 var(--h));       /* ≈ #0a0f0b */
  --c-light: oklch(0.975 0.006 var(--h));      /* ≈ #f4f8f5, tinted, not cream */
  --brand:    oklch(0.72 0.17 40);             /* the client's owned colour (example): fields, objects, light only */
  --on-brand: oklch(0.28 0.08 40);             /* same hue, L .25-.30: 5.7:1 on --brand; white would be 2.65:1 */
  --bg: var(--c-dark); --fg: var(--c-light);
}
[data-theme="light"] { --bg: var(--c-light); --fg: var(--c-dark); }
/* Derived tokens resolve where they are declared, so declare them on every theme scope. */
:root, [data-theme] {
  --fg-2:  color-mix(in oklab, var(--fg) 65%, var(--bg));   /* secondary text ≈ 7:1 with these anchors */
  --fg-3:  color-mix(in oklab, var(--fg) 45%, var(--bg));   /* ≥ 24px text only ≈ 3.6:1 */
  --raise: color-mix(in oklab, var(--fg) 6%, var(--bg));    /* tonal elevation, no border */
  --line:  color-mix(in oklab, var(--fg) 14%, transparent); /* hairlines and fills: alpha is fine here */
  --glass: color-mix(in srgb, var(--bg) 80%, transparent);  /* + backdrop-filter; only over a backdrop worth showing */
  background: var(--bg); color: var(--fg);
}
::selection { background: var(--brand); color: var(--on-brand); }
:focus-visible { outline: 2px solid var(--fg); outline-offset: 3px; }   /* tonal ring, ≥ 3:1 on both sides */
```

The contrast figures in the comments were computed for these example anchors (18:1 apart). With these anchors, a 55% mix drops to about 5:1 and 50% to about 4.2:1, so recompute for your own pair. A token set with more than about 12 colour values, or an accent without an on-colour, has drifted. Dont-board-me declares 29 `--c-*` tokens and holds together only because the rendered page uses red on pink almost everywhere (dont-board-me).

## 10. Contrast floor

Every one of the 51 teardowns logs at least one contrast weak spot, and the jury's accessibility mean (6.83) is the lowest developer sub-score, against 8.01 for animations [stats]. The failure classes, by keyword pass over the teardowns' contrast notes:

1. **Text over footage, renders or photos, about 35 of 51.** A flat full-frame veil does not rescue it: depo-luxe uses a 14% veil and bennett-clive a 20% one, and bennett's ADIDAS sits over snow at 1.5:1. Use the scrim ladder [imagery §3.1]: no scrim if the text passes, dark text if that passes, otherwise a local scrim behind the text only (never more than about 0.54 black for white text), otherwise a plate.
2. **Alpha-dimmed secondary text, about 27 of 51.** Examples: rgba white at .4 on black (gq-ap-the-extraordinary-lab, the-watch), 20% hover isolation at 1.7:1 (gil-huybrecht), 50% sand on ink at 2.3:1 (son-daven), 30% labels at 2.2:1 (leo-parpeix-portfolio-2026). Fix: a solid mixed token (section 9).
3. **Brand-colour text/field pairs chosen by hue, not value, 8 sites with computed ratios:**
   - white on `#FD4401`, 3.5:1 (maxima-therapy)
   - white on `#8ed462`, 1.8:1 (mindmarket)
   - `#f8f8f8` on `#ff391e`, 3.38:1 (thelinestudio-com)
   - `#FF0837` on `#FFC1FF`, 2.68:1 (slosh-seltzer)
   - red on pink, 2.8:1 (dont-board-me)
   - yellow on orange, 1.64:1 (shed)
   - white on `#b3aba3`, 2.27:1 (vast)
   - cream on orange, 1.6:1 (ponpon-mania)

   White reaches 4.5:1 only on fields at relative luminance ≤ 0.18, roughly OKLCH L ≤ 0.56. `#0061FE` at L 0.55 passes at 5.07:1, while most brand oranges, reds, greens and sky blues sit at L 0.60-0.80 and fail (computed). Give those fields a same-hue dark ink. The pairs that pass all do this: champions-for-good duotones at 9.1-18.1:1, dropbox-brand at 5.9:1, floema at 5.56:1.
4. **Same-value chrome.** A `#1A1A1A` logo on a `#0E0E0E` floor measures 1.1:1 (akaru-2), and a fixed nav that keeps its dark ink over dark slides disappears (leo-parpeix-portfolio-2026).
5. **Mid-animation states.** Mid-morph grounds (lando-norris). Reading-fill text whose resting state is 10% ink (opal-tadpole) or `#ddd` on white at 1.4:1 (terminal-industries). That is the law's invisible-content trap in colour: the resting state must already pass, and the fill adds emphasis from `--fg-2` to `--fg`.

The floor: body and UI text at 4.5:1 or better; text of at least 24px (or 18.66px bold) at 3:1; focus rings, control boundaries and meaningful graphics at 3:1 against both neighbours [usability-a11y-perf §D]. Tonal accents meet the same thresholds: the tone comes from value, not from dropping below the floor. Measure with grain on and over the worst video frame. Tiny labels compound the problem: the teardowns log 8-10px caps as unreadable on lando-norris, era-residence and san-rita. Label size floors: [./typography.md](./typography.md).

## 11. Failure modes

- A lime or neon CTA plus matching dots: the winners' template (lando-norris, made-with-gsap-1, terminal-industries). Move the colour to a field or object and make the button tonal.
- Cream or UI-kit grey chosen because it feels safe. Terminal's surfaces fall back to stock greys (`#f0f0f0` cards, a flat mid-grey nav) while only its hairlines are tinted, and odd-ritual's `#F4F4F4` wells read the same way.
- Indigo drift on dark: colour-dodge or bloom pushes a chosen dark toward violet plus periwinkle (active-theory-v6 work view). Check a screenshot's sampled ground, not just the token.
- Purple kept alive in code-only chapters. Everswap's hero has none, but a lavender wash and a purple Voronoi pass wait in unscreenshotted chapters (everswap). Audit every chapter's grade.
- A shader palette read once at init, so a theme toggle recolours the DOM but not the canvas (son-daven).
- A canvas clear colour left at black or white, so its edge shows against the page (section 5).
- A banded blur mask or gradient with no dither (pacome-pertant-portfolio rings).
- Colour defined on `html{}` instead of `:root` is harmless, but a probe or audit reading `:root` will miss it (akaru-2). Keep palette tokens on `:root` for tooling.
- Two gradients fighting: gradient text over a gradient sky (the-power-of-storytelling). One surface carries the gradient and the type stays solid.

## Crafted vs slop

| Award habit | Slop version | Crafted version |
|---|---|---|
| Saturated brand accent (lando-norris lime) | The same vivid swatch on the CTA fill, the eyebrow dot, a headline word and the hover state | The owned hue as a whole field or a lit object with a same-hue on-ink; UI states as tonal ink/ground steps |
| Warm off-white base (9/51) | Oat-milk cream sheet under everything | A light tinted to the brand hue, a lit material (immersive-garden-website plaster), fog matched to the page (floema), or pure white with imagery doing the work (tracing-art) |
| Dark tech ground | `#0c0e15` blue-charcoal with a periwinkle accent | Neutral `#101010`-`#121212` or a brand-hue black (green, brown, plum) with warm-white ink |
| Section-shifting colour (37/51) | A glow that stops dead at a flat section edge | A scrubbed hand-off across padding, or colour arriving as a sheet, disc, curtain or shaped seam; chrome recolours with it |
| Film grain | A fixed noise sheet over type and controls | Grain in the post pass or a `z-index:-1` tile, strength 0.03-0.07, luminance-masked, stepped, reduced on mobile |
| Atmospheric gradient | Two-hue glow, corner blob, halo behind the object, candy pastel wash | One-hue directional light ramp with dither, motivated by a light or an object; or the content's own blurred colour (depo-luxe) |
| Fixed textured background (pacome-pertant-portfolio grid) | A static pattern trailing every section and the nav, with banding | A texture that means the concept (artefakt screen-door), stays on dark substrates, reacts or changes per section, and sits under a treated nav |
| Dimmed secondary text | White or ink at .3-.5 alpha | A solid `color-mix` token verified at 4.5:1 or better; alpha only for lines and fills |
| Multi-hue illustration palette | Four brand colours sprinkled across buttons and labels | At most two hues per viewport, one field/ink pair per section, every hue from the illustration system |
| Text over footage | A flat 14-20% veil over the whole frame | A worst-frame measurement, then dark text, a local scrim at ≤ .5 that fades before section edges, or a plate |
| Reading-fill statement | Words resting at 10% ink until scroll fills them | Words resting at `--fg-2` (4.5:1 or better), with the fill adding emphasis to `--fg` |
| Glass nav | Frosted box with a blue glow over a flat field | `color-mix(in srgb, var(--bg) 80%, transparent)` with blur, only over live footage or imagery, and only if it blends without banding (fluid-glass) |

## Exemplars

- **lando-norris**: the scrubbed canvas and DOM ground hand-off, an olive-tinted neutral system, a livery-owned accent, and the mid-morph contrast trap to avoid.
- **dropbox-brand**: same-hue on-ink pairs that keep eight saturated fields coherent and legible.
- **champions-for-good**: strict duotone pairs, two colours per viewport, every pair at 9:1 or better.
- **son-daven**: a two-token duotone system flipped by one class, with a shader drawing every illustration in the same two colours.
- **immersive-garden-website**: a monochrome palette made premium by a lit material rather than by an accent.
- **oryzo-ai**: a four-value system where the product is the accent; a dithered one-hue light pool; the "lights out" hero transition.
- **the-watch**: relighting the material for mood instead of recolouring the page.
- **era-residence**: a section colour taken from the render's sky, plus per-element header recolouring.
- **fluid-glass**: hierarchy from value with near-zero accent, and color-mix tokens for glass and dimmed text.
- **thelinestudio-com**: a multiply acetate that brand-tints uncontrolled footage, then peels away.
- **shed**: one hue, one job, one surface. Colour as architecture.
- **tracing-art**: pure white, and depth fog to paper instead of grain or tint.

## Evidence

- **Stats.** [stats] = `data/stats.md`, recent_2024_plus cut (n=575): palette_size_distribution, palette_base, palette_hue_families, saturated_accents_top, score means. [stats*] = recomputed in this session from `data/corpus.jsonl` with the same cut: lightness and tint of the recorded lights and darks; saturated mid-lightness colours (HLS S > 0.5, 0.2 < L < 0.8) counted, deduplicated and bucketed by hue.
- **Probe.** [probe] = `data/probe_summary.json`: css_features_by_sites (modern-color 10/51), css_usage_by_sites (mix_blend_mode 17, backdrop_filter 16, filters 18), canvas_contexts_by_sites (webgl2 41). Per-site modern-colour counts: `evidence/probes/<slug>/probe.json`.
- **Teardowns.** Site slugs in parentheses = `data/teardowns/<slug>.json` (color, performance_accessibility.contrast_issues, steal_this, slop_risks). The counts marked (51 teardowns) are hand classifications of the color.mode, color.base and color.accents fields in this session. The failure-class counts in section 10 come from a keyword pass over contrast_issues and are approximate.
- **Research files.**
  - [imagery §2.1-2.3, §3.1, §5] = `data/research/imagery.md`
  - [usability-a11y-perf §B, §D] = `data/research/usability-a11y-perf.md`
  - the tiny-palette editorial reading = `data/research/awwwards-editorial.md` (section 7, "Tiny palettes, owned colour")
- **Law.** `deslop-law.md`: saturated accent, cream background, slop grey, cool blue-charcoal, purple gradients, pastel candy gradient, drifting blobs, background glow, radial halo, grain over content, grainy gradients, colliding colours and hard seams, hard image seams, fixed background, text you cannot read, tonal elevation, considered light, premium noise, cohesion.
- **Computed.** WCAG ratios and OKLCH conversions for the example tokens and the brand fields were computed in this session from the published hex values.
- **Tested.** Headless Chromium via Playwright 1.58, gsap 3.15.0 from jsDelivr, 2026-09-25.
  - Section 5 recipe: the ground morphs mid-hand-off, the ink flips at 0.5, and jumps to the top and bottom resolve to the right section. The first draft threw "Cannot access 'hand' before initialization" because `ScrollTrigger.create` fires `onRefresh` synchronously. That is fixed in the snippet.
  - Section 9 tokens: `--fg-2` measures 7.0:1 in both themes, `--fg-3` 3.6:1 and `--on-brand` 5.7:1.
  - Firefox and WebKit were not run.
- **Inferred, carried over from the teardowns.** The-power-of-storytelling's blue-noise use. The ground seam mechanics of vast, where the hand-off was not visible between screenshots, are omitted.
- **Recipes linked, not duplicated.** [../recipes/motion-core.js](../recipes/motion-core.js), [../recipes/three-hero.js](../recipes/three-hero.js), [../recipes/tokens.css](../recipes/tokens.css). Related references: [./imagery.md](./imagery.md), [./typography.md](./typography.md), [./motion.md](./motion.md), [./casebook.md](./casebook.md).
