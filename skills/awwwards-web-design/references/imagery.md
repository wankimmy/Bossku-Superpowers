# Imagery and art direction

Last updated: 2026-09-25

Use this when: you are choosing, directing, treating, compositing or shipping the photos, renders, footage, illustration or generated images of an Awwwards-level site.

Citations: `[imagery §n]` is [research/imagery.md](../data/research/imagery.md), `[usability-a11y-perf §n]` is [research/usability-a11y-perf.md](../data/research/usability-a11y-perf.md), `[probe]` is [probe_summary.json](../data/probe_summary.json), `[stats]` is [stats.md](../data/stats.md) (recent_2024_plus cut), and a bare slug is `../data/teardowns/<slug>.json`. "(rec.)" marks a working target, not a measured winner value.

## Rules

1. Pick one primary medium and one world before sourcing. Allow at most 3 image registers, each with a fixed light and grade. Across the 51 teardowns, the lead medium is realtime 3D on 18, a mixed set on 16, video on 7, illustration on 6, photography on 3 and a pre-rendered film on 1 [teardowns].
2. Colour lives in the imagery and the chrome stays quiet. Sample page, ink and accent from the graded set (era-residence, son-daven, oryzo-ai). Never add a saturated UI accent that the pictures do not already contain.
3. Write a one-page image bible before sourcing: light direction, grade/LUT, lens, camera height, 2-3 crop ratios, the type zone, one in-image accent, 0-1 global treatment and a banned list [imagery §4.3]. Then review every final asset on its own at full resolution against it.
4. Content is visible by default. An image un-clip starts with more than half its area showing (motion-core's `inset(14% 10%)` leaves 58%), every canvas and video sits over a poster, and no image waits behind an ENTER gate or a preloader.
5. Measure text over imagery at the worst glyph-sized window of the worst frame. 25/51 teardowns log text-over-image contrast failures, and flat 10-20% black veils did not rescue bright frames (bennett-clive, depo-luxe, vast).
6. One treatment per site, tied to the concept and applied to the whole set, never a drop-in effect. Grain goes in a WebGL post pass drawn under DOM type, or on a `::before` substrate at opacity 0.04-0.10, never as a sheet over type. The one allowed exception is grain masked onto a single display word.
7. Image hovers happen inside a frame that stays still: a scale of at most 1.04 over 500 ms or more inside `overflow: clip`, a still-to-preview swap, or a velocity-driven distortion on a few large images ([webgl-image-hover.js](../recipes/webgl-image-hover.js)). No card lift, no underline fill, no overlay-caption card.
8. Scroll motion on images is a settle or drift of media that is already visible: scale 1.15-1.2 → 1, or yPercent ±5-15 inside a clipped frame (`data-parallax="0.1"`-`"0.15"` in motion-core.js, a fraction of viewport height), over-scaled so no edge shows, gated by reduced motion.
9. Pre-render whatever the visitor does not steer, and use realtime 3D only where input changes the picture. Sequences run 60-150 frames, use frame 0 as the poster, and load coarse-to-fine.
10. Ship AVIF → WebP → JPEG through `<picture>`, with real re-crops per breakpoint, one `fetchpriority="high"`, KTX2 for GPU textures, and a separate portrait master for any full-bleed film or sequence.
11. Video loops are muted and playsinline, use frame 0 as the poster, get a pause control when they run 5 s or longer, pause off-screen, and stream (HLS) when long. Only 37 of 250 `<video>` elements on 60 SOTD homepages ship a poster [usability-a11y-perf §1.5].
12. Use AI only for exploration, painted or surreal base plates, non-human worlds and jokes. It is always human-finished and disclosed, and never shows people, products or places as real. 3/51 use it (aim-ai-modernism-of-kharkiv, the-renaissance-edition, oryzo-ai).
13. Keep media above the fold on mobile to 3 MB or less (rec.) and stream the rest. Heavy winners declare 37-185 MB of mp4 (active-theory-v6 37.1 MB, artefakt 184.9 MB). Do not copy the weight.

## 1. What winners put in the frame

| Archetype | Leads the site (n=51) | Appears anywhere (n=51) | Wider corpus signal |
|---|---|---|---|
| Realtime 3D (models, worlds) | 18 | 29 | WebGL 82 and 3D 80 of 575 recent tags [stats]; 57% of 201 SOTDs [imagery §1.1] |
| Photography | 3 (akaru-2, odd-ritual, shed) | ~27 | Photography 11, Photographic 8, Photo & Video 17 tags [stats]; 20% of SOTDs |
| Product still (photo or render as the subject) | 11 product-led sites | 9 of the 11 go realtime at some point | E-Commerce 23 tags [stats] |
| Pre-rendered CGI and film | 1 (terminal-industries) | ~10 | Blender 12, Cinema 4D 3 tags [stats]; 7% of SOTDs |
| Scrubbed image sequences | (terminal-industries, as above) | 3 on canvas + 2 sprite-sheet systems | GSAP ships an official helper [imagery §2.10] |
| Illustration and painted media | 6 | ~19 | Art & Illustration 26, Illustration 16 [stats]; 15% of SOTDs |
| Video | 7 | ~32 (mp4 requested on 22, m3u8 on 4 during the probe [probe]) | `video` element tag 86 [stats]; 13% of SOTDs |
| Type-led first screen | 8 own the first screen | 0 sites are type-only | Typography 42 tags [stats]; 19% of SOTDs |
| Generated (AI) imagery | 0 | 3 | AI-imagery-first SOTDs score 7.27-7.45 against a 7.42 mean [imagery §1.13] |

- **Hybrids are the norm.** 37/51 draw media through a canvas: 29 run realtime 3D, 6 put only 2D images or video through GPU shaders (gil-huybrecht, lama-lama-2, pacome-pertant-portfolio, siena-film-foundation, son-daven, tracing-art), and 2 draw only pre-rendered frames on a 2D canvas (opal-tadpole, terminal-industries). The probe found webgl2 on 41/51 sites and 2d on 35/51, but some of those contexts are third-party feature probes, not media [probe; son-daven].
- **Who owns the first screen:** 3D on 18, a mix on 13, type on 8, video on 6, a still image on 6 [teardowns first_screen].
- **The medium does not win on its own.** SOTD jury means by archetype sit within 0.14 of each other (7.35-7.49) [imagery §1.1].
- **Treatments are substrate, not showpiece.** Words in element-highlight titles across 732 records (title matches, not the element tags in stats.md): gallery 150, video 142, parallax 82, reveal 68, shader 48, mask 22, pixel 21, ascii 19, distort 9, dither 2. Grain, duotone and halftone never appear [imagery §1.1].
- **Decision: choose the medium from what the thing is.**
  - A real, physical thing where trust matters: your own photography plus one GPU layer.
  - A thing that does not exist yet, or cannot: pre-rendered CGI, or realtime if the visitor steers it.
  - An abstract service: illustration in one hand, animated in Rive or Lottie.
  - Moving image is the work: untouched video in a monochrome shell.
  - The word is the asset: type owns screen one and imagery arrives by screen two.
  - The brief says "creative" or "maximal": one authored, limited-palette medium (a single illustration hand, cyanotype, riso, painted plates), not stock realism. Its own ink then becomes the page colour (law: "Creative" is not "realistic").

## 2. Art direction by archetype

### 2.1 Photography (editorial, documentary, lifestyle)
- **One light condition per series.** Fluid-glass uses soft overcast daylight, ungraded and lightly desaturated (fluid-glass). Vast uses bright, even cleanroom light with a slightly warm grade (vast). Floema uses natural, slightly warm daylight (floema).
- **Registers follow content type, not page.** Odd-ritual keeps three: warm-grey seamless studio shots in soft window light with a lifted, desaturated film grade; dawn lifestyle in golden haze; and black-and-white reportage reserved for community partners. Its packshots are flat (odd-ritual). Cap it at 3 registers.
- **Use 2-3 crop ratios per site.**
  - odd-ritual: 16:10 hero, 4:5 cards, 2:1 partner strips (odd-ritual).
  - fluid-glass: 4:5 cards and 16:9 film (fluid-glass).
  - aim: one-third-width, full-height panels plus square gallery tiles (aim-ai-modernism-of-kharkiv).
- **Compose scale contrast on purpose.**
  - A 372x187 landscape under a viewport-wide headline (era-residence).
  - 200-550px crops mixed in one horizontal track (lando-norris).
  - Index squares that halve per step, from 432px down to about 27px (depo-luxe).
- **Let the framing carry the meaning.** Shed shoots its own interiors symmetrical, frontal and flash-bright (shed). Tracing-art shows museum photography untouched, as alpha cut-outs that float without frames (tracing-art).
- **Decision.**
  - Commission or shoot one coherent series.
  - Reserve the type zone at the shoot: at least 35% clean sky or wall on the type side [imagery §3.2].
  - If you must use stock, take one photographer's series re-graded to your LUT, and never use it for the hero.

### 2.2 Product stills
- **The backdrop is a brand or collection tone.** Floema puts cut-outs on flat collection colours: coral, celadon, kraft, white (floema). Odd-ritual's packshots sit on #F4F4F4 (odd-ritual), which is the law's slop-grey family, so tint the sweep instead.
- **One key light with real falloff.**
  - Oryzo: a single warm key rakes in from lower-left and falls off into deep brown (oryzo-ai).
  - The Watch: a grey seamless and two EXR environments, with no hard shadows. Colour appears only in the movement's gold wheels, blue screws and ruby jewels (the-watch).
- **Close crop at true scale.** Opal shows the product in real hands at real size. Its turntable is rendered on pure white or black with no floor, cropped so the object fills the frame (opal-tadpole).
- **The engineering view is the second register.**
  - A white hairline isometric drawing where only two parts carry colour (opal-tadpole).
  - An exploded view with leader lines (the-watch).
  - Monoline wireframes pixel-registered to the photo (floema).
- **Product in front of type.** The can crops its own wordmark on purpose (slosh-seltzer). Keep occlusion under about 25% of a word's letters [imagery §3.2].
- **Live product state.** The watch hands and date come from the visitor's clock, so every visit is a new product shot (the-watch).
- **Decision.** 11/51 are product-led. 9 of them go realtime at some point (the-watch, slosh-seltzer, cartier-watches-wonders-2025, gq-ap-the-extraordinary-lab, oryzo-ai, iyo, vast, lacoste-polo-factory, floema). Go realtime only if the visitor rotates, configures or explodes the product.

### 2.3 Pre-rendered CGI and image sequences
- **About 10/51 ship pre-rendered CGI as imagery.** Three scrub a frame sequence on a 2D canvas: terminal-industries (410 frames), opal-tadpole (321 frames per finish, 2 finishes x 2 widths) and son-daven (120 frames). Two play sprite sheets: shader-development-studio (AVIF sheets) and lacoste-polo-factory (sprites with separate shadow sprites).
- **Render twins from one camera so a state change is a crossfade.**
  - Day and night renders, re-staged as well as relit (era-residence).
  - Day and night sets chosen by the visitor's clock (son-daven).
  - One turntable per colourway, swapped behind a 0.48 s fade (opal-tadpole).
- **Give the same render a second grade instead of new assets.** One camera move runs golden-hour photoreal (low sun, lavender-to-amber sky), then a sensor look: white and cyan wireframe with point-cloud dust (terminal-industries).
- **Render for compositing.**
  - Cut along the skyline so the section colour becomes the sky, #B5CEDB (era-residence).
  - Export shadows as their own sprites (lacoste-polo-factory).
  - Render clips on pure black so a shader can luma-key them (son-daven).
- **Stage renders like a photo shoot.** Era's arch-viz is styled as a period lifestyle shoot with figures, props and bougainvillea (era-residence). Default HDRI studio light, glossy plastic and a centred orbit are the slop version [imagery §1.7].
- **Decision.** Pre-render when the camera path is fixed. For the same budget it looks better than realtime: Oryzo composites a baked desk plate with one live object, gobo and contact shadow included (oryzo-ai).

### 2.4 Realtime 3D as imagery
- **One material system per world.**
  - A toon ramp and one palette atlas (brunos-portfolio).
  - A screen-space ink outline plus a 3D LUT (messenger).
  - Monochrome plaster bas-relief, with colour only inside project windows (immersive-garden-website).
  - Hand-painted albedo on low poly (everswap).
  - Emissive electric blue on dark terrain (hubtown).
  - Architecture built from the product's own geometry (cartier-watches-wonders-2025).
- **Grade once, in post.**
  - A 3D LUT (igloo-inc, messenger, gq-ap-the-extraordinary-lab).
  - A preset table interpolated per scene on scroll (bloom, sepia 0.1-0.81, chromatic aberration, grain). It also pulls photo cut-outs and models into one world (shader-development-studio).
- **The world re-grades any photo put inside it.** Client video plays on refracting glass slabs (active-theory-v6). Far planes fog to 97% white (tracing-art).
- **The bar is pre-rendered quality.** Lusion rejected image sequences (not interactive) and realtime PBR (not good enough), then shipped splats plus baked textures [imagery §1.8].
- **Build it.** Engine choices are in [webgl-3d-stack](../data/research/webgl-3d-stack.md). The hero pattern (poster first, canvas fades over it) is [three-hero.js](../recipes/three-hero.js).

### 2.5 Illustration and painted media
- **One hand, one line weight, and a palette equal to the section ink.**
  - Athletes built only from hard-edged polygons in the section's single ink (champions-for-good).
  - Commissioned brush-stroke dogs, big and cropped by type or edges, never boxed (dont-board-me).
  - Black-and-white comic panels with one spot colour per chapter (ponpon-mania).
- **Twin states instead of new art.** Every icon exists as a colour fill and a white outline, and hover swaps between them (dropbox-brand).
- **Illustration binds a mixed photo set.** Illustrated props always overlap the stock-style photos (maxima-therapy). A ribbon splits into back and front layers around a photo cut-out (mindmarket).
- **Painted media inside 3D.**
  - Commissioned watercolour cut-outs on torn paper, with skewed shadows (david-whyte-experience).
  - A marker layer over machined 3D (steven-com).
  - Procreate construction sketches, made without AI (oryzo-ai).
- **Motion.** Lottie runs on 6/51 and Rive on 6/51 [probe]. Drawn things move in stepped time, not smooth tweens:
  - line boil at 5, 10 or 12 steps per second (ponpon-mania)
  - UI and text quantized to 1.3-8 Hz (messenger)
- **Law.** Crafted SVG is premium. Crude CSS or SVG stand-ins (div charts, floating spheres, orbit rings) are slop. Never mix styles or put pack characters next to bespoke art.

### 2.6 Video
- **Leave client footage in its own grade and unify through the shell.**
  - Every commercial keeps its own look inside a black-and-white terminal shell (artefakt).
  - Grades stay intact under a flat 14% veil (depo-luxe).
  - The only interventions are a 20% dim and the type (bennett-clive).
- **Colour lives only in the media on 7/51:** artefakt, bennett-clive, depo-luxe, gil-huybrecht, immersive-garden-website, lama-lama-2 and aim-ai-modernism-of-kharkiv.
- **Tint only as a brand gesture.** A red acetate multiplies over the hero footage; everywhere else, colour stays as delivered (thelinestudio-com).
- **The film can be the ambient backdrop.** The focused film reappears at blur 100px, scale 2 and a 25% veil under the index (depo-luxe).
- **Keep playback under control.**
  - Case films have autoplay off, and the GL layer drives playback (artefakt).
  - Play and pause per section on ScrollTrigger enter and leave (made-with-gsap-1).
  - Crossfade 0.2 s in and 0.3 s out (depo-luxe).
- **Cut a portrait master.** Cover-cropping 16:9 to about 0.46:1 on phones is brutal (depo-luxe). Opal ships a 1280x2310 portrait hero (opal-tadpole); Terminal ships a 409-frame portrait set (terminal-industries).

### 2.7 Type-led first screens and type as image
- **No winner is type-only.** 8/51 let type own the first screen: aim-ai-modernism-of-kharkiv, akaru-2, champions-for-good, dont-board-me, dropbox-brand, mindmarket, siena-film-foundation and slosh-seltzer. Imagery arrives within the next viewport.
- **The wordmark is drawn geometry and becomes the image.** Constructivist slabs morph in Lottie (aim-ai-modernism-of-kharkiv). Per-letter SVGs fill a 318px-tall column (akaru-2).
- **Type can live inside the render.**
  - MSDF text placed in the 3D scene (cartier-watches-wonders-2025).
  - A luma-keyed title video (gq-ap-the-extraordinary-lab).

  Keep a real DOM heading. GQ's is `visibility:hidden`, so screen readers get nothing.
- **Put an image inside type once, as the signature.** Recipe and limits: [imagery §3.3].

### 2.8 Generated (AI) imagery
- **aim-ai-modernism-of-kharkiv.** A Midjourney set art-directed as printed matter:
  - flat frontal light
  - muted paper grounds
  - visible noise
  - five colours: vermilion, cobalt, ochre, black, bone

  The tool is disclosed in a display-copy footnote.
- **the-renaissance-edition.** AI-founded paintings, finished by human artists, cut into depth layers and rebuilt as 3D dioramas [imagery §1.13].
- **oryzo-ai.** Midjourney for composition only, then full non-AI 3D. Google Flow only for AI-joke images over Lusion's own renders, plus a footnote disclaimer.
- **Process.**
  - One style reference and one light direction for the whole set.
  - Inpaint hands, text, faces and edges.
  - Composite with your own renders or photos.
  - Grade everything with one LUT.
  - Disclose wherever trust matters.
- **Reject in QA:** waxy skin, a teal-orange grade on every frame, a centred symmetrical subject with bokeh, light direction that drifts between images, garbled text, fused fingers, and the same generic polish on everything [imagery §1.13].

## 3. Holding a mixed set together

- **Sampled surface.** The page colour is a colour from the image:
  - the sky of the renders, #B5CEDB (era-residence)
  - sand from wool and hay (son-daven)
  - cork brown (oryzo-ai)
  - fog that equals the page (david-whyte-experience)
  - the loader's flat #c6b6a3 matches the first WebGL frame, so the handoff is invisible (cartier-watches-wonders-2025)
- **Monochrome shell.** Chrome in black, white or one ink, with colour only inside the media: 7/51, listed in §2.6.
- **One lens over everything.** A LUT, a per-scene grade preset (shader-development-studio), or one brand treatment on every source: dither (lama-lama-2) or line screen (son-daven).
- **Same-camera twins** for every state (§2.3).
- **Registers by content type.**
  - Black and white for community photos (odd-ritual) and team portraits (lama-lama-2).
  - Archival black-and-white prints mapped onto curved planes (cartier-watches-wonders-2025).
- **Decision.** Before sourcing, fill in three hex values from the set (page, ink, one in-image accent) and name the single lens. If a new asset breaks either, re-grade it or cut it.

## 4. Treatments: when, numbers, recipe

### 4.1 Tint, duotone, black and white
- **Winners.**
  - The hero portrait turns into an olive duotone as it scrolls out: `uFilter` 0 → 1 over the first viewport (grayscale, contrast 0.8, then hardLight with #50593F) (lando-norris).
  - A red acetate multiplies over the footage (thelinestudio-com).
  - Black and white used as a register (odd-ritual, lama-lama-2).
- **Duotone recipe.** SVG filter with `color-interpolation-filters="sRGB"` [imagery §2.2]. Bake it into LCP assets. Use it as a state: hover or scroll restores the original.
- **Acetate recipe.** Use a deep, desaturated tone of the brand hue so the tint stays tonal:
```css
.media { position: relative; isolation: isolate; }
.media::after { content: ""; position: absolute; inset: 0; pointer-events: none;
  background: var(--tint); mix-blend-mode: multiply; }          /* --tint sampled from the brand, not a stock red */
.media > .copy { position: relative; z-index: 1; }             /* type sits above the acetate, never under it */
```
- **Slop.** A magenta/cyan duotone unrelated to the brand, duotone on faces as a filter, or a tint laid over UI text.

### 4.2 Dither, halftone, ASCII, pixel
- **5/51 use one as an image treatment.**
  - A vertical line screen whose bar width follows darkness, one texel per cell, so edges step (son-daven).
  - A 4x4 ordered dither whose first 7 sub-pixels are the logo. Cells are 8px on content and 16px in the intro; the cell size tweens 160 → 16 over 3.75 s (lama-lama-2).
  - Client films hand off through a band of 13px greyscale ASCII cells. The particle logo's ASCII pass uses 180 columns (8px cells at 1440, 90 on mobile) with the composer at 0.3x resolution, and its glyph ramp ` .:-=+*#%@` ends in the brand letters `4RT3F` (artefakt).
  - Black-and-white halftone portraits behind the names on the About hover (aim-ai-modernism-of-kharkiv).
  - A halftone illustration multiplied onto the red footer floor (thelinestudio-com).
- **Reveal by moving the levels, not opacity.** Tween `blackPoint`/`whitePoint` from 25/200 to 45/175 on scroll. To hide an outgoing scene, send it to 254/255. For an idle scene, yoyo to 55/150 over 4 s (son-daven).
- **Guardrails.**
  - Keep the original `<img>` in the DOM.
  - Share one WebGL context. Son Daven gives each halftone canvas its own: 15 live contexts, one short of Chrome's usual limit of 16.
  - Keep some imagery raw, as Son Daven does in its gallery.
- **Slop.** A drop-in dither component on a hero with no concept [imagery §2.4], or an ASCII field that only twinkles behind everything (law: fixed background).
- **Crafted.** The treatment is the brand's lens: the logo is the dither pixel (lama-lama-2), and the glyph ramp is seeded with the name (artefakt).

### 4.3 Grain placement
- **What winners do.**
  - 38/51 add no grain layer.
  - 8/51 put grain in a WebGL shader pass (cartier-watches-wonders-2025, gq-ap-the-extraordinary-lab, hubtown, leo-parpeix-portfolio-2026, shader-development-studio, siena-film-foundation, ponpon-mania, why-zero). On 7 it sits under DOM type. Shader Development Studio draws its visible type in WebGL and grains after the UI composite, so its grain lies over text, damped by luminance. Strengths: Cartier 0.03-0.06, Siena 0.07, Leo Parpeix 0.07 (off below 1025px), why-zero 0.04.
  - 4/51 keep grain inside the assets (aim-ai-modernism-of-kharkiv, bennett-clive, thelinestudio-com, dont-board-me).
  - 1/51 fixes a CSS noise sheet over everything, type included: opacity 0.1, soft-light, measured standard deviation about 0.9 levels (son-daven). That is the law's grain-over-content tell, even when faint.
- **Recipe, in-canvas.** Luminance-masked grain collects in the darks and mostly skips bright pixels (shader-development-studio). Run it before any in-canvas type is composited, so no text gets grain:
```glsl
float n = smoothstep(0.0, 0.49, fract(sin(dot(vUv, vec2(12.9898, 78.233))) * 43758.5453 + uTime * uVelocity));
color.rgb += n * (1.0 - color.rgb) * uGrain;   // uGrain 0.026-0.055; x0.65 on mobile; uVelocity 0.05 reading, 1 default
```
- **Recipe, DOM.** A pre-rendered 256px tile on `::before` at `z-index:-1` inside an `isolation: isolate` section, opacity 0.04-0.10 (rec.), soft-light, on the section only [imagery §2.3].
- **Banding.** Dark renders also get blue-noise dithering against banding (oryzo-ai, igloo-inc, the-power-of-storytelling). Do this on every large gradient.

### 4.4 Masks and clip shapes
- **clip-path runs on 29/51 [probe].** The good shapes come from the brand:
  - an arch (era-residence)
  - a film gate and ticket notch (siena-film-foundation)
  - notched section seams (terminal-industries)
  - a tab silhouette (lando-norris)
  - a 45° chamfer (active-theory-v6)
  - slanted and stepped polygons (maxima-therapy)
  - irregular painted cut-outs, with no rectangle anywhere (david-whyte-experience)
- **Recipes.**
  - `data-reveal="image"` in [motion-core.js](../recipes/motion-core.js) opens `inset(14% 10%)` to 0 while the media settles from 1.18 → 1. A frozen frame still shows the image.
  - Feathered full-bleed edge [imagery §2.7]. The law's four conditions: mask the image's own pixels, 10+ stops over about 30%, a 116vh section, and the same colour above and below.
  - Wipe with counter-parallax: a polygon clip while the inner image, 120% tall, moves yPercent ±10 (odd-ritual).
- **Pixel-register two layers.** Trace a line drawing from the exact photo. Wipe it off with `inset(0 0 0% 0)` → `inset(0 0 100% 0)` while the shared mask scales 1 → 1.1 (fluid-glass). Floema's blueprint-to-photo reveal is the same move (floema).
- **Slop.**
  - Slides at `display:none` until JS runs (odd-ritual).
  - A rounded rectangle on every image.
  - A notch that shaves text. Law: clear the cut, and zoom into the edge before shipping.

### 4.5 WebGL hover distortion
- **About 9/51 drive media with the pointer on the GPU, and each effect is tied to the concept:**
  - a paint-in brush (david-whyte-experience)
  - burn (gil-huybrecht)
  - frost wiped away by the cursor (why-zero)
  - a dither trail (lama-lama-2)
  - a fluid mask painting the helmet over the portrait (lando-norris)
  - brighten plus blur only where stirred (leo-parpeix-portfolio-2026)
  - velocity bend (immersive-garden-website)
  - velocity smear (pacome-pertant-portfolio)
  - a UV data-texture (artefakt)

  None ships a generic ripple on every card.
- **Recipe.** [webgl-image-hover.js](../recipes/webgl-image-hover.js). One shared canvas; the DOM `<img>` stays the source of truth; distortion comes from eased pointer velocity, so nothing warps at rest. It boots after load plus idle and skips touch, reduced motion, Save-Data and software GL.
- **Numbers.** Maximum drag 5% of the short side, DPR at most 1.5, at most 8 live planes per viewport [imagery §2.8].
- **Watercolour paint-in** (david-whyte-experience). A 256² fluid sim gives `m`. Then `paint = smoothstep(0.468, 0.51, m + (noise - 0.5) * 0.39)`, and the edge band darkens 15% like pooled pigment.
- **Slop.**
  - A ripple on every portfolio card.
  - Distortion strong enough to break text inside the image.
  - Hover isolation that drops the other items to 20% alpha, about 1.7:1 (gil-huybrecht).

### 4.6 Scroll-linked scale and parallax
- **Winner numbers.**
  - A reveal zoom of 1.2 → 1 over 1.8 s, plus scale and counter-scale inside moving windows (akaru-2).
  - Inner scale 1.1 with xPercent -25 → 25 across a horizontal panel (fluid-glass).
  - yPercent -15 → 15 on cut-outs (era-residence).
  - 20% parallax inside overflow-hidden frames (odd-ritual).
  - A 4rem per-image drift in a pinned track (lando-norris).
  - A cover bleed of 1.05, or 1.155 below 1025px, so parallax never shows an edge (leo-parpeix-portfolio-2026).
- **Recipes.** `data-parallax="0.15"` in [motion-core.js](../recipes/motion-core.js) over-scales the media automatically. A CSS `view()` settle is in [imagery §2.9]. Timing and easing are in [motion](./motion.md).
- **Slop.** Parallax on text blocks, more than two speeds in a viewport, a fixed background trailing the scroll (law), or scroll-jacked slideshows.
- **Reduced motion.** Only 11/51 sites had any reduced-motion CSS [probe]. Gate every image move.

### 4.7 Image sequences on canvas
- **Winner numbers.**
  - 410 frames of 1920x1080 WebP at 14-153 KB each (50.4 MB declared), plus a 409-frame portrait set (terminal-industries).
  - 321 frames per finish at q80, in 1920 and 1280 widths: 1,284 files (opal-tadpole).
  - 120 frames (about 19 MB), desktop only (son-daven).
- **Target (rec.).** 60-150 frames of 40-90 KB each at 1600px, about 3-10 MB, with a half-resolution, every-second-frame set on mobile [imagery §2.10]. Draw cover-fit, snap to whole frames, and use a scrub of 0.25-0.5.
- **Don't pin the whole page.** Opal scrubs through the viewport without a pin, from `top 85%` to `85% 0%` (opal-tadpole).
- **Always put a poster `<img>` of frame 0 under the canvas.** Opal hides its container until the current frame loads, and Son Daven locks scroll until all 120 frames arrive. Both leave a fast scroller staring at nothing.
- **Use sprite sheets when the post pass must grade the frames.** AVIF sheets (6x9 = 54 frames, grid inferred) with a manifest and a mobile set below 700px (shader-development-studio).
- **Load coarse-to-fine** (adapted from terminal-industries, which batches every 8th remaining frame in a Worker). The loop and canvas code are in [imagery §2.10].
```js
function loadOrder(n, step = 8) {              // 0, 8, 16 ... then 4, 12 ... then 2, 6 ... then the odd frames
  const order = [0], seen = new Set(order);
  for (let s = step; s >= 1; s = Math.floor(s / 2))
    for (let i = 0; i < n; i += s) if (!seen.has(i)) { seen.add(i); order.push(i); }
  return order;
}
const nearest = (frames, i) => { while (i > 0 && !frames[i]?.naturalWidth) i--; return frames[i]; };
```

### 4.8 Veils, blur and ambient backdrops
- **Flat veils fail on bright frames.** Observed: 0.20 (bennett-clive), 0.14 in the film view and 0.25 in the index (depo-luxe), 0.10 (vast). ADIDAS over snow measures about 1.5:1 (bennett-clive); white over moon rock, 2.27:1 (vast).
- **What held up.** The video renders at opacity 0.8 over #212325, with a transparent-to-black gradient behind the statement (fluid-glass).
- **Blur works as a state.**
  - The ambient film backdrop (depo-luxe).
  - A gallery overlay at blur(10px) over #0e0e0ec2 (aim-ai-modernism-of-kharkiv).
  - A focus lightbox over dark video (artefakt).
- **backdrop-filter runs on 16/51 [probe].** Put it only over a detailed image. Never animate the radius on hover, and never blur to hide low resolution (law: botched glass).

## 5. Image and type composition

- **Type over full-bleed media** on about 10/51: bennett-clive, depo-luxe, artefakt, fluid-glass, vast, thelinestudio-com, odd-ritual, shed, floema, era-residence.
- **Object in front of type** on at least 6/51: slosh-seltzer, the-watch, oryzo-ai, dont-board-me, zentry, leo-parpeix-portfolio-2026. Figures also break their own frame edge (lando-norris footer card, champions-for-good sticker tiles). Keep the word readable, with occlusion at about 25% or less.
- **Type in the image's negative space.** A wordmark in open sky (era-residence); a copy column in the painting's cloud gap (the-renaissance-edition).
- **Blend chrome over media.** mix-blend-mode runs on 17/51 [probe]. With difference blending, render the element that must keep its true colour as an un-blended "solver" duplicate (opal-tadpole). Otherwise a blended button turns into its complement.
- **Choreograph type to the frames.** Terminal's titles land over darker frames of the film, not over frame 0's bright amber sky (terminal-industries).

**Legibility ladder.** Targets: 4.5:1 for body, 3:1 at 24px or above (18.66px bold) [imagery §3.1].
1. Pick the text colour per image first. If white or black passes everywhere, use no scrim.
2. Otherwise compute the minimum scrim alpha over the worst glyph-sized window, with the sharp script in [imagery §3.1]. For video, run it on the brightest frame under the text.
3. Put the scrim only behind the text band, and fade it to 0 before any section edge (law: hard seams). Display type can add a halo such as `0 0 18px rgb(0 0 0/.18)` (WCAG G145).
4. If the alpha exceeds 0.5, use a solid plate, move the text into negative space, or re-crop with `object-position`.

Two more guards:
- Never put text of 12px or smaller over media. White 12px mono over a yellow film fails (artefakt), and so do 8px caps over an olive photo at about 1.5:1 (lando-norris).
- Give fixed chrome a collision rule per section. Leo Parpeix's nav disappears over dark slides (leo-parpeix-portfolio-2026), and Akaru's logo drops to 1.1:1 on dark floors (akaru-2).

## 6. Production pipeline

**6.1 Sourcing order**
1. Your own shoot or commissioned photography: real people, places and products.
2. Commissioned renders (Blender, Houdini/Redshift) for unbuilt or impossible subjects.
3. Scans and photogrammetry for material truth. Oryzo used about 180 photos in RealityScan for its cork, plus a purchased hand scan [imagery §4.1].
4. Hand illustration: one style, one line weight.
5. AI: mood and composition, base plates, jokes (§2.8).
6. Stock last, as one photographer's series, never the hero. A juror warns that "stock-grade imagery" costs Content points [imagery §4.1].

**6.2 Stills**
- **What winners ship.** WebP on 29/51, JPG on 27/51, PNG on 43/51, AVIF on only 8/51 [probe].
- **SOTD homepages.** AVIF is referenced on 9/60 and WebP on 32/60, and 47% of images carry width and height [usability-a11y-perf §1.5].
- **Width ladder.** 640/960/1280/1600/2400/3200.
- **Encoder settings.** AVIF q50, effort 6 (raise the quality for grain or dark gradients). WebP q78. mozjpeg q80.
- **Delivery.** `<picture>` with `media` re-crops per breakpoint, one `fetchpriority="high"`, never lazy on the LCP image, lazy plus `decoding="async"` below the fold. Full markup: [imagery §4.4].

**6.3 Video**
- **Encoding.** AV1 plus an H.264 fallback, no audio track, `+faststart`, and the poster extracted from frame 0 [imagery §4.5].
- **Loop control.** Pause off-screen with IntersectionObserver, and add a pause control [usability-a11y-perf §3.8].
- **Long films** stream from a video host on 5/51: HLS on lama-lama-2 (Bunny), oryzo-ai (Vimeo), pacome-pertant-portfolio and shader-development-studio (Mux); Mux static MP4 renditions on gil-huybrecht.
- **Alpha video.** HEVC comes first and VP9 alpha second, because Safari cannot play VP9 alpha. Era handles it by stripping its WebM on Safari (era-residence).
- **Size.** HEVC alpha runs about 3x the VP9 size; the smallest route is stacked-alpha AV1/HEVC composited in WebGL [imagery §4.5]. Era ships 41.1 MB of WebM across 16 files, mostly alpha flower loops, and plays them only in view.

**6.4 GPU textures and mobile sets**
- **GPU textures.** KTX2 on 14/51, glb on 19/51, EXR on 7/51, HDR on 4/51 [probe].
  - 159 KTX2 thumbnails transcoded through Basis (gil-huybrecht).
  - `-small.basis` textures swapped in on low-tier devices (ponpon-mania).
- **Separate mobile media on 9/51:** a portrait frame set (terminal-industries), portrait video and a 1280px sequence (opal-tadpole), `title-narrow.mp4` (gq-ap-the-extraordinary-lab), desktop/ and mobile/ mp4 sets (david-whyte-experience), dk/mb videos (cartier-watches-wonders-2025), a mobile sprite manifest (shader-development-studio), `-small.basis` (ponpon-mania), a portrait camera track (the-power-of-storytelling), and posters instead of video in the index (depo-luxe). Decide the portrait crop per hero; do not let `object-fit: cover` decide it.

**6.5 Budget**
- Above the fold on mobile: 3 MB or less. Stream everything past it.
- Winners run far over, as declared mp4: artefakt 184.9 MB, thelinestudio-com 159.8 MB (not all eager), bennett-clive 96.7 MB, gil-huybrecht 66 MB plus 26.2 MB of KTX2, leo-parpeix-portfolio-2026 49 MB.
- It can be done light: about 6 MB declared in total, 3D and JS included (iyo 5.8 MB, why-zero 6.4 MB).

## 7. Failure modes (review checklist)

1. Images hidden until a reveal fires: opacity 0, `clip-path: inset(100%)`, `display:none` (odd-ritual hero slides) or `visibility:hidden` (era-residence `[data-prevent-flicker]`).
2. Canvas or video with no poster under it. 85% of winner videos ship none [usability-a11y-perf §1.5].
3. Text over bright frames behind a flat veil (§4.8), or small text over media (§5).
4. Mixed light and grade across a set; stock, AI and renders side by side with no lens (§3).
5. Grain, a faint grid or a dot screen laid over content, or a fixed background trailing the scroll (son-daven noise sheet over type, artefakt's fixed full-screen screen door). A dot grid kept behind one real technical drawing is the allowed blueprint form (opal-tadpole).
6. A commodity effect as the concept: dither, ASCII, liquid hover or a cursor trail with no link to the brand. A hover trail that piles photos onto the headline (champions-for-good).
7. A radial halo, glossy default plastic or a centred orbit on a product (§2.2).
8. A cream, bone or UI-grey surface under imagery (akaru-2 #F1EFEB, fluid-glass #f3f0ec, odd-ritual #F4F4F4) instead of a sampled one (§3).
9. A hard seam where a full-bleed image meets a flat section. A scrim that ends at the section edge (§4.4, §5).
10. AI people or products presented as real, or AI output undisclosed (§2.8).
11. Media bloat, a preloader that waits on every frame (son-daven locks scroll on ~19 MB), or one WebGL context per image (son-daven: 15) (§6.5).
12. Pulsing hotspot rings or info pills pinned to images (era-residence, floema). Put the specs in the layout.
13. The overlay-caption card: a portrait tile with a bottom scrim, uppercase meta, a serif name and a link arrow (law). Put captions beside or under the frame in the page grid, not on a gradient over the picture.
14. A strong image hero, then a flat fill with boxes for every section after it (law). Carry imagery, sampled surfaces or the one treatment down the whole scroll.

## Crafted vs slop

| Award habit | Slop version | Crafted version |
|---|---|---|
| Flat veil under type over footage (bennett-clive 0.20, depo-luxe 0.14, vast 0.10) | Uniform dim on every frame; white type fails on snow and sky | Measure the worst glyph window; choose text colour per frame; scrim only behind the text band; place titles over dark frames (terminal-industries) |
| Film grain | Fixed noise sheet over the whole page, type included (son-daven) | Luminance-masked grain in the post pass under DOM type, or a `::before` substrate at z-index -1, 0.03-0.10 |
| Cream or bone base behind imagery (akaru-2, fluid-glass, era-residence) | Oat-milk default surface | Page colour sampled from the graded set: a render's sky (era-residence), cork (oryzo-ai), pure white with a cool chapter shift (tracing-art) |
| Image un-clips on scroll | Starts at `inset(100%)` or opacity 0 and stays blank if the trigger fails | Starts with more than half the area showing and widens; `data-reveal="image"` in motion-core.js |
| Hover on image cards | Card lift, shadow bloom, underline-fill caption, ripple on every card | The frame stays still; the inside scales at most 1.04, swaps to a muted preview, or distorts with pointer velocity on a few large images |
| Saturated brand colour next to photos (lando-norris lime, odd-ritual #050FFF) | Poster-bright buttons and dots across the UI | Saturated colour lives inside the image (a livery, a product part, a prop); UI accents are tonal steps off the page or ink |
| Dither, ASCII, halftone | A drop-in dither component on a random hero | The treatment is the brand lens (the logo as the dither pixel, a line screen that reads as woven wool); the original `<img>` stays in the DOM; some imagery stays raw |
| Duotone | Magenta/cyan filter with no brand link, on faces | Two inks sampled from the set, baked into LCP files, used as a state that returns to the original (lando-norris scroll-out) |
| Grid or dot field behind media (artefakt's fixed screen door) | Static faint grid trailing behind every section and the nav | A field that moves and relates to content (terminal-industries' masked grid), a 15px dot grid only behind the technical drawings (opal-tadpole), or none |
| Project or product card | Portrait tile, bottom scrim, uppercase meta, serif name, arrow | The image alone in the grid; caption set beside or below it in the page's type; hover acts inside the frame (tracing-art's hover restores a desaturated painting's colour) |
| Glow behind the hero product | Centred radial halo | One directional key with falloff, a contact shadow and a gobo (oryzo-ai) |
| Cursor image trail | Photos piled over the headline on every mouse move | Only when the trail is the content (an archive), never over type, with a list or grid alternative for touch |
| Autoplay loops everywhere | Empty box until frame 1, no pause, all films eager | Poster = frame 0, pause control at 5 s or more, paused off-screen, playback owned by scroll or GL (artefakt, made-with-gsap-1) |
| AI imagery | AI "customers", AI product shots, undisclosed | Human-finished plates, non-human worlds and jokes, one LUT, disclosed in a footnote (aim-ai-modernism-of-kharkiv, oryzo-ai) |

## Exemplars

- **son-daven**: a line-screen halftone on renders and clips keyed on black; levels-scrub reveals; a day/night 120-frame hero. Also study its failures: noise over type, a scroll-locking preloader, 15 WebGL contexts.
- **era-residence**: CGI staged as a lifestyle shoot, same-camera day/night twins, the section colour as the sky of cut-out renders, alpha-video foliage.
- **oryzo-ai**: a baked plate composited with one live object; a single raking key; AI kept to jokes and disclosed; hand-drawn sketches.
- **depo-luxe**: client films left in their own grades, the film as its own blurred backdrop, a halving-square index drawn on canvas.
- **terminal-industries**: a 410-frame pre-rendered film scrubbed on canvas, a second sensor grade from the same camera, coarse-to-fine loading, a portrait set.
- **opal-tadpole**: three registers (studio photo, a turntable per colourway, two-colour engineering line art), and a sequence scrubbed without a pin.
- **david-whyte-experience**: commissioned watercolour cut-outs, fluid-sim paint-in, and no rectangular image anywhere.
- **lama-lama-2**: one dither lens over all brand media, with client work as the only full colour.
- **fluid-glass**: a line drawing pixel-registered to the photo and wiped off on scroll, with the dimmed-video legibility that held.
- **tracing-art**: museum photography untouched, depth fog toward the page white, and hover that restores full colour.
- **aim-ai-modernism-of-kharkiv**: a disclosed Midjourney set art-directed as printed matter, with colour arriving only through the artworks.
- **lando-norris**: the portrait as a displaced relief, a duotone scroll-out, a photo track with per-image drift, and a livery motif shared by image and graphics.

Full entries: [casebook](./casebook.md).

## Evidence

- **Teardowns.** `data/teardowns/<slug>.json` for all 51 sites. Fields used: `imagery` (primary_medium, art_direction, treatments, crops_and_ratios, formats), `color.texture`, `first_screen.what_owns_it`, `three_d.stack/role`, `performance_accessibility.contrast_issues`, `steal_this`, `slop_risks`.
  - Counts marked [teardowns] are hand classifications of those fields: primary medium, first-screen owner, grain placement, text-over-image failures, product-led sites, mobile media sets, video presence and photography presence.
  - "About" or "~" marks counts that required judgment.
- **Digest.** `evidence/digests/imagery.md` (all 51 sites; the imagery and first-screen dimensions).
- **Research.** `data/research/imagery.md`:
  - §1.1: 201 SOTD tag shares, jury means and element highlights.
  - §1.7-1.13: archetypes and AI practice, including the Lusion BTS and RGD sources.
  - §2.2-2.10: treatment recipes.
  - §3.1-3.3: legibility, including the sharp scrim script.
  - §4.1-4.5: sourcing, image bible, formats and video.
- **Research.** `data/research/usability-a11y-perf.md` §1.5 (60 SOTD homepages: AVIF 9/60, img width/height 47%, video posters 37/250) and §3.8. `data/research/webgl-3d-stack.md` for engines.
- **Probe.** `data/probe_summary.json`: clip_path 29, filters 18, mix_blend_mode 17, backdrop_filter 16, reduced-motion rules 11, webgl2 41 and 2d 35 contexts, asset extensions, 3D asset types, and Lottie and Rive library counts.
- **Stats.** `data/stats.md`, recent_2024_plus cut (575 sites): tags_top and element_tags_top.
- **Recipes linked, not duplicated.** `../recipes/motion-core.js` (data-reveal="image", data-parallax), `../recipes/webgl-image-hover.js`, `../recipes/three-hero.js`.
- **House law.** `deslop-law.md` sections: grain on top of content, hard image seams, the fixed background that follows the scroll, cream/beige background, slop gray, saturated accent, radial glow halo, card hover-lift, hover boop, underline-fill, invisible-content trap, clear the cut, botched glass, crude CSS illustrations, floating tag pinned to an image, the image card with overlay caption, a flat fill under everything after the hero, faint grid background, premium noise, grainy gradients, "Creative" is not "realistic".
- **Inferred or unverified, kept marked.**
  - Shader Development Studio's 6x9 sheet grid is inferred from bundle numbers.
  - Era Residence's Safari alpha behaviour is taken from its code path, not tested in Safari.
  - Son Daven's context count is the teardown's code reading (15 scene canvases); the probe's extra 16 webgl2 contexts are attributed to third-party scripts (inferred).
  - Audit 2026-09-25: 40+ numbers, colours and attributions re-checked against the teardowns, probe, stats and research; the artefakt ASCII split, Son Daven's context count, the Shader Development Studio grain placement, the canvas-media count and the light-site weights were corrected.
  - AVIF smearing baked grain at q50 is unverified [imagery §2.3].
  - Scrim, occlusion, frame and byte budgets marked as recommendations in research are working targets, not benchmarks.
