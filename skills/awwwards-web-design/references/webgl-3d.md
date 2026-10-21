# 3D and WebGL

Last updated: 2026-09-25

Use this when: a brief might put a canvas on the page, from one hero object to an explorable world, and you must pick the rung, build it, budget it and give it a fallback.

## Rules

1. **3D carries the subject** (the product, the place, the brand's own object) or it is cut. 15/51 winners have no 3D layer and still won (bennett-clive, shed, fluid-glass, made-with-gsap-1). Abstract floating spheres, blobs and "3D shapes" are the law's crude-illustration tell in a new medium.
2. **Take the lowest rung** of the decision tree that delivers the interaction the brief needs. If scroll is the only input, pre-render it (opal-tadpole, terminal-industries).
3. **Poster and DOM copy paint first.** The canvas is `aria-hidden` decoration that fades in after `compileAsync` and its first frame. It is never the LCP element and never the only copy of any text [usability-a11y-perf §2 A, §3.5].
4. **One WebGL context per page.** Images become DOM-synced planes on one fixed canvas (gil-huybrecht), never a canvas per element (son-daven runs 15 contexts, one short of Chromium's 16).
5. **Bake what does not move:** lighting into atlases, camera moves and art-direction keyframes into animation-only GLBs authored in Blender or C4D (the-power-of-storytelling, leo-parpeix-portfolio-2026).
6. **Light with one 1k HDR/EXR environment plus at most one directional key.** Always give ground contact. Shoot products on a long lens, 15-35° vertical FOV (three-hero default 24).
7. **Tone-map by content:** none (or `toneMapped: false`) for unlit, painted and photo planes; `NeutralToneMapping` for lit product and brand colour; AgX or ACES only for mood. Never leave a lit PBR scene on `NoToneMapping` [webgl-3d-stack §5].
8. **Post is restraint:** bloom threshold ≥ 1.0 (only HDR emissives bloom) at strength ≤ 0.3, chromatic aberration ≤ 1 px at the canvas edges, grain on the canvas substrate, and no post effect over text, DOM or in-canvas.
9. **The canvas uses the page palette.** Clear colour = fog = the page background at the canvas edge; no cool blue-charcoal void, no cream studio backdrop, no violet-cyan iridescence; every gradient, fog and sky is dithered so it never bands.
10. **Compress and stream:** KTX2 textures capped at 2048, Meshopt (Draco for dense scans), self-hosted decoders, ≤ 1.5 MB of 3D before first interaction on mobile and ≤ 3 MB on desktop; stream the rest per chapter.
11. **DPR** `min(dpr, 2)` for light scenes, 1.25-1.5 for full-screen post, ≤ 1.5 on coarse pointers; then adapt from measured frame time.
12. **Render on demand,** pause offscreen and in hidden tabs, render only the scenes on screen.
13. **Tier the experience** (poster, lite, full) and test the poster path on every build.
14. **Text, headings and controls live in the DOM.** In-canvas type is an echo; every 3D hotspot has a real `<button>`.
15. **Reduced motion** gets a still or hard cuts between held beats: no scrubbed camera, no cursor fluid, no idle spin.
16. **Ship nothing dead:** no debug GUI, no unused engine, no LAN URL. depo-luxe bundles three r158 with no renderer set up in its app code; the-power-of-storytelling ships Tweakpane 4.0.5; david-whyte-experience ships lil-gui, Tweakpane and stats.js.

## How often and how winners use 3D

| Measure | Count | Basis |
|---|---|---|
| Any 3D/WebGL layer | 36/51 | teardowns `three_d.present` |
| three.js, any wrapper | 28/36: 24 vanilla or in-house engines, 4 R3F (san-rita, the-renaissance-edition, vast, shader-development-studio) | teardowns |
| Other engines | Hydra 2 (active-theory-v6, slosh-seltzer), OGL 2 (ponpon-mania, siena-film-foundation), raw WebGL2 1 (lama-lama-2), Spline 1 (zentry) | teardowns |
| Pre-rendered 3D as the 3D | image sequences on 2 (opal-tadpole, terminal-industries); video-only CGI on thelinestudio-com, era-residence | teardowns |
| WebGPURenderer + TSL live | 2/51 (brunos-portfolio, shader-development-studio) | [probe] webgpu contexts 2 |
| three.js revision range | r148 (everswap) to r185 (gil-huybrecht), median r176 over 28 sites: winners do not chase releases | teardowns |
| Pages that load 3D assets | 26/51: glb 19, ktx2 14, exr 7, hdr 4, drc 2, basis 1 | [probe] |
| Theatre.js for authored timelines | 4 (gq-ap-the-extraordinary-lab, hubtown, the-renaissance-edition, active-theory-v6) | teardowns |
| Imagery led by realtime 3D | 18/51 primary medium; 3 more name it inside a mixed medium (iyo, leo-parpeix-portfolio-2026, the-renaissance-edition) | teardowns `imagery` |

Wider signal: 22 of the last 31 SOTDs and 9 of the last 12 SOTMs carry a WebGL, 3D or Three.js tag [webgl-3d-stack §1]. In the 2024+ corpus the tags read WebGL 82/575, 3D 80, Three.js 51, but that corpus over-samples 3D and WebGL listings (62 each) [stats]. Canvas contexts (webgl2 41/51 [probe]) overcount: mindmarket's 15 webgl2 contexts are inferred to be Rive, and son-daven's 16th comes from a third-party probe.

Scores: 3D sites average creativity 8.05 vs 7.82 without, overall 7.74 vs 7.69, developer accessibility 6.81 vs 7.07 (n = 36/15, teardowns). Across 308 dev-scored SOTDs, the 185 tagged 3D/WebGL score WPO 7.54 vs 7.55 and accessibility 6.98 vs 6.85 [usability-a11y-perf §1.4]. Decision: 3D buys creativity and costs nothing inherent; the accessibility gap in the sample is self-inflicted (see the UI section).

Who builds worlds: studios with an engine of their own around three or instead of it (Active Theory's Hydra; Lusion on everswap and oryzo-ai; 60fps on the-watch and, with Immersive Garden, cartier-watches-wonders-2025; OFF+BRAND on lando-norris and steven-com; abeto on messenger). One solo developer shipped a full world (brunos-portfolio). Take the architecture: a thin layer that registers scenes by DOM attribute (lando-norris mounts scenes from `[data-gl='head'|'tracks'|'background'|...]`), so pages declare where GL lives and the engine keeps one canvas.

## Decision tree: which rung

Answer in order and stop at the first yes. Then check the budget table.

```
Q0 Does 3D carry the subject: the product, the place, the data, the brand's own object?
   no  -> NONE. Spend it on type, photography or a crafted SVG scene. (15/51 winners)
Q1 Is scroll or time the only input (no pointer-driven geometry, no user choice)?
   yes -> PRE-RENDERED. Ambience: <video muted playsinline loop poster>. Scrub: image sequence on a 2D
          canvas, 60-150 WebP/AVIF frames, or all-intra video. (opal-tadpole, terminal-industries)
Q2 One designer-owned object on Webflow/Framer, 2-4 states, no custom shader?
   yes -> SPLINE <spline-viewer> on Hobby ($12/seat/mo) or above: Free watermarks, and Spline hosts
          the scene below Enterprise. (zentry)
Q3 Only a flat image or field effect (dither, halftone, distortion, film strip), no scene graph?
   yes -> one fullscreen-quad shader: a three ShaderMaterial if three ships anyway, else raw WebGL2 or OGL
          (lama-lama-2, siena-film-foundation, son-daven). No-code: Unicorn Studio, Legend tier for commercial.
Q4 Authored camera, custom shaders, strict budget, SOTD intent?
   yes -> THREE.JS vanilla behind a thin scene registry. (24 winners)
          R3F only when the site is React/Next AND 3D state is UI-coupled: configurator, routed scenes,
          many 3D cards. Tween uniforms directly so React never re-renders per frame. (san-rita, vast)
Q5 GPU compute (100k+ simulated particles), node post (TRAA, SSR) or one shader codebase for both backends?
   yes -> WebGPURenderer + TSL; test forceWebGL: true on every build. ShaderMaterial, onBeforeCompile and
          EffectComposer do not run there. (brunos-portfolio, shader-development-studio)
Q6 A real captured place or object whose view-dependent detail is the point?
   yes -> Gaussian splats (Spark 2.x inside three), on props and reflections first.
          (oryzo-ai keeps ~78k splats on desktop, ~44k on mobile; the rest is baked meshes)
```

| Rung | 3D payload seen | Skills needed | Exemplars |
|---|---|---|---|
| Pre-rendered sequence | winners ship 321 (opal-tadpole, per colourway) to 410 frames (terminal-industries); house budget 60-150 frames at 40-90 KB [imagery §2.10] | 3D artist + front-end | opal-tadpole, terminal-industries |
| Spline object | runtime + Spline-hosted scene | designer | zentry |
| Flat shader field | no geometry, media only | one WebGL developer | lama-lama-2, siena-film-foundation |
| three.js hero object | 0.09-1.54 MB (akaru-2 92 KB, iyo 1.03 MB, lando-norris 1.54 MB) | WebGL developer + 3D artist | akaru-2, lando-norris, iyo |
| Explorable world | 1-20 MB streamed (messenger 1.07, everswap ~6.9 incl. webp, san-rita 12.7, cartier-watches-wonders-2025 19.5, declared) | a studio with its own engine, or one expert (brunos-portfolio) | messenger, igloo-inc, cartier-watches-wonders-2025 |

House rule: if first-interaction 3D tops 1.5 MB on mobile, drop a rung or load the 3D on intent behind a poster [webgl-3d-stack §3]. Default when unsure: a poster plus one lit object with [three-hero.js](../recipes/three-hero.js), upgraded later. Scroll-scrubbed sequences: [imagery.md](./imagery.md).

## Roles, each with a build note

Counts are a teardown classification; one site can hold several roles.

**World, 21/36.** The page is a place the camera travels (igloo-inc, messenger, cartier-watches-wonders-2025, everswap, hubtown).
- Put the camera on rails authored in the DCC. david-whyte-experience scrubs a baked `Camera_Action_Baked` clip. the-power-of-storytelling ships camera and shader keyframes as animation-only GLBs (cam.glb 235 KB, dev.glb 164 KB, one scroll section = one timeline second) plus a portrait `cam-mob.glb`. Use Theatre.js sheets when designers tune in the browser (hubtown, gq-ap-the-extraordinary-lab).
- Put 3-5 held beats in the clip, each aligned to a DOM copy block. Damp progress with `1 - exp(-dt * k)`, k ≈ 6. Never `LoopOnce` + `clampWhenFinished`: scrubbing back freezes; clamp progress to 0.9999 instead [webgl-3d-stack §4.1].
- Render only what is on screen: active-theory-v6 scissors the two scenes inside a wipe; igloo-inc renders one or two scene composers at a time.
- Stream per chapter: the-renaissance-edition lazy-loads 13 scene chunks, steven-com builds each room on demand and disposes it, ponpon-mania loads chapter textures per route.

**Painted 2.5D, a cheaper world.** Unlit planes in perspective with the light painted or baked into the texture: david-whyte-experience (instanced painted billboards with per-instance atlas remaps, a paper normal map, fog by depth and height), ponpon-mania (sprite layers per panel rendered onto paper boards), the-renaissance-edition (painted KTX2 backgrounds behind compressed props), leo-parpeix-portfolio-2026 (full bake, the fragment is just `texture(uTexture, vUv)`). Build with `MeshBasicMaterial` or a one-line ShaderMaterial, no tone mapping, one atlas per object family. One authored medium is what makes a world cohere; the law's "creative is not realistic" field note applies.

**Object hero or product, 16/36** (lando-norris, the-watch, oryzo-ai, akaru-2, slosh-seltzer).
- One GLB, long lens (lando-norris FOV 15 in its bundle, the-power-of-storytelling 25, akaru-2 28), 1k environment, one key, ground contact. The stage is 100svh and the object fills about 70% of the frame (three-hero `view.fill 0.7`), so the hero owns the first screen.
- Render the expensive object once into a render target and composite it (lando-norris's helmet, MSAA samples 2).
- Move the light, not only the object: the-watch rotates its environment reflections with scroll (`uGlobalEnvmapRotation`) and adds a second EXR for highlights, so specular travels across the metal.
- Spend realism where the pointer is: oryzo-ai composites a realtime coaster over a pre-rendered desk plate with an analytic soft shadow.
- Recipe: [three-hero.js](../recipes/three-hero.js) (lathe placeholder or your geometry, clearcoat, RoomEnvironment + one key, contact shadow, optional scrubbed camera, poster fallback).

**Configurator or finish swap, 7/36.** iyo (3 matcap colourways at 0.82 over PBR, OrbitControls), slosh-seltzer (one shared metal-rough-AO map, flavour base colour swapped as KTX2), floema (a material cube swaps texture sets as a scroll-driven ring reaches each swatch), the-watch (colourway wheel), lando-norris (Lime helmet 06:00-18:00 local time, Dark otherwise), opal-tadpole (a second pre-rendered set swapped at the same frame index under a 480 ms crossfade), vast (interior/exterior switch, hotspots defined as data with 3D positions).
- Variants are texture or material swaps on one mesh: share ORM, swap base colour; or ship `KHR_materials_variants`.
- `frameloop="demand"` + `invalidate()`; re-render shadow maps only on change (floema sets `shadowMap.autoUpdate = false`).
- Crossfade 400-500 ms and keep the pose; mirror the configuration to the URL. Every swatch is a real radio button; drag-to-orbit gets arrow-key and button alternatives (SC 2.5.7).

**Image planes, 10/36** (gil-huybrecht, siena-film-foundation, pacome-pertant-portfolio, tracing-art, floema, artefakt, leo-parpeix-portfolio-2026, immersive-garden-website, why-zero, lama-lama-2).
- One fixed canvas, orthographic camera in CSS pixels, planes synced from `getBoundingClientRect()` inside rAF; the `<img>` stays in layout and the accessibility tree [webgl-3d-stack §4.4].
- Hide the DOM image only after its plane has drawn. siena-film-foundation sets it to opacity 0 in its mesh classes, which blanks the image if WebGL stalls.
- KTX2 per capture behind an LRU cache (gil-huybrecht: 64 textures, ref-counted); video textures updated with `requestVideoFrameCallback` and paused by IntersectionObserver.
- One motion for every image, driven by input: pacome-pertant-portfolio bows each plane and smears it sideways by wheel velocity. Photo planes use `toneMapped: false`.
- Gate on `(hover: hover) and (pointer: fine) and (min-width: 650px)` like gil-huybrecht; touch gets the plain images.
- Recipe: [webgl-image-hover.js](../recipes/webgl-image-hover.js) (one shared canvas at DPR ≤ 1.5, velocity drag that is zero at rest, the `<img>` never leaves the DOM).

**Particles and type fields, 10/36.** artefakt seeds particles from logo vertices in a GPGPU texture sized `max(256, ceil(sqrt(vertexCount)))` and raycasts against a separate low-poly GLB. iyo runs 1,638,400 particles in 1280x1280 float ping-pong targets as 1 px points, with text targets pre-sampled once from dark pixels. active-theory-v6 tiers its count from 16,384 to 1,048,576 by GPU. oryzo-ai simulates 1,024 beans on the CPU (576 on mobile).
- Up to ~100k points: attributes plus vertex math. Beyond: GPGPU (`GPUComputationRenderer`) or TSL compute.
- Particles form the subject (a logo, a product, a word). The real heading stays in the DOM: iyo's haiku manifesto lives only in canvas particles, and its accessibility score is 6.0.
- One ink colour; normal blending on light grounds; point size attenuated by depth [webgl-3d-stack §4.5].

**Globe, 0 observed.** No data globe was captured; the-renaissance-edition's bundle holds a draggable globe in a chapter the probe did not reach, and messenger's planet is a world. If the brief needs one: cobe 2.0.1 (~5 KB) with CSS-anchored DOM labels, or three-globe 2.45.2 for data arcs. No atmosphere halo; one directional key; stop the spin offscreen and under reduced motion [webgl-3d-stack §4.6].

**Fluid and cursor sims, 15/36.** Pressure-solve fluids on 7: lando-norris, active-theory-v6 (256 px sim, 512 px dye), slosh-seltzer (20 pressure iterations), gq-ap-the-extraordinary-lab, igloo-inc (128x128, 2 iterations), leo-parpeix-portfolio-2026 (0.2x resolution, 1 Poisson iteration), ponpon-mania. Cheaper velocity trails, flowmaps or cursor-cut fields on 8, including lama-lama-2 (gaussian stamp radius 0.04, frame-time-normalised decay), why-zero (half-res ping-pong, decay 0.97/0.95), immersive-garden-website (flowmap for cursor extrusion) and gil-huybrecht.
- The sim is a texture other passes read: lando-norris reveals the helmet through it; leo-parpeix-portfolio-2026 blurs and brightens the frame by velocity.
- 1/4-1/8 resolution, half float, 1-2 pressure iterations; displacement ≤ 0.04 UV; decay 0.94-0.97; one palette colour [webgl-3d-stack §4.7].
- Gate it to one section (everswap enables its screen-paint distortion only in the final section), off on touch without hover (leo-parpeix-portfolio-2026 binds an empty 256x256 velocity texture instead), off under reduced motion.
- When touch must paint: lando-norris ships a `TAP TO LOCK` control (`aria-pressed`, updated `aria-label`) that locks page scroll so drags paint instead of scrolling.

**Captured reality, 1/36.** oryzo-ai trained splats on Houdini renders, found 900k splats still flawed, and kept splats only for props and the desk reflection (`props.sog`, `table_reflection.sog` at 50%) [imagery §1.8]. Frame tightly, keep the camera on rails, and cover the load with a poster from the same viewpoint [webgl-3d-stack §4.10].

**Noise-displaced surfaces.** Only when the surface is the subject (cloth, liquid, a material sample): amplitude 0.05-0.15 × radius, speed 0.1-0.2, normals rebuilt from displaced neighbours [webgl-3d-stack §4.9]. A free-floating iridescent blob is the tell, not the move.

**Post styles that sign a site.**
- Ink outlines: messenger (MRT info buffer with depth, normal and object ID; outline #373f42 fading from view-z 50 to 300; thickness normalised to a 1300 px height), gq-ap-the-extraordinary-lab (edges drawn as `LineSegments2` with per-edge overshoot, jitter, thickness and opacity exported from the model), ponpon-mania (inverted hull), lando-norris (contours from stepped noise), the-renaissance-edition (inverted Sobel pencil). Build one full-screen pass on depth and normal discontinuities, ink = a dark tint from the palette, and let materials opt out.
- Dither, halftone, ASCII: artefakt (ASCII pass at 0.3x resolution, 180 columns = 8 px cells at 1440, 90 on mobile), lama-lama-2 (4x4 cells whose 16 sub-pixels spell the logo as brightness rises), son-daven (halftone bars coloured from CSS variables). Pixelate, take luminance in display space, remap, threshold on Bayer 8x8 with a half-level offset, two palette colours, canvas layer only [webgl-3d-stack §4.8].
- LUT grades: messenger (tetrahedral 3D LUT from `lut.ktx2`), igloo-inc (3D LUT + diagonal gradient), gq-ap-the-extraordinary-lab (per-scene LUT strength), david-whyte-experience (LUT pass with exposure). Grade a rendered frame in a colour tool, export a 3D LUT texture, apply it last before dither or grain. One LUT ties realtime, pre-rendered and photo into one world.
- Film: siena-film-foundation (gate mask, corner burns, blur along the strip by scroll velocity; its grain is additive-only and lifts blacks, so centre grain on zero), shader-development-studio (gamma, sepia matrix, motion blur skipped on mobile, grain scaled by DPR), cartier-watches-wonders-2025 (pointer-steered vignette, after-image remanence).

## Taste: materials, light and post that read expensive

- **Bake first.** 9 winners carry their light in textures: active-theory-v6 (Cycles COMBINED as KTX2), igloo-inc (lightmap crossfaded to an exploded-state lightmap), leo-parpeix-portfolio-2026, lacoste-polo-factory, everswap (inferred: no light rig found), steven-com (shadow bakes as KTX2), hubtown (baked AO plus fake lights injected into the material instead of real lights), the-watch (packed ARM texture with specular occlusion), oryzo-ai (pre-rendered plate). Real-time lights are the exception; if one casts shadows, use `PCFShadowMap` or `VSMShadowMap` (r186 removed `PCFSoftShadowMap`).
- **Environment.** 1k HDR/EXR is the norm (lando-norris, the-power-of-storytelling, cartier-watches-wonders-2025 at 1k and 256 px); the-renaissance-edition ships a pre-baked PMREM as KTX2. Jewellery and watches get an environment per material family (cartier-watches-wonders-2025: leather, metal, diamond).
- **Tone mapping.** brunos-portfolio (stylised node materials with a replaced output) and pacome-pertant-portfolio (image planes) leave `NoToneMapping` so authored hexes survive; that only works when nothing is lit past 1.0. akaru-2 and floema's product viewer run ACES. Watch colour spaces: lando-norris converts declared hexes linear to sRGB, so #F8F8F3 renders #fcfcfa. Pick colours on screen, not in code.
- **Materials.** Vary roughness with a map. Clearcoat for lacquer, sheen for fabric. Transmission only on the hero, over something worth refracting (the law's real translucency, not a frosted box): igloo-inc's crystal is #e0e8ef, roughness 0.65 + map, IOR 1.18, env intensity 0.91; iyo's glass is transmission 1, roughness 0.05, IOR 1.6. When the material is the product, give it real parameters: the-power-of-storytelling exposes 23 glass tunables and keyframes many of them along the story.
- **Ground contact, every time:** oryzo-ai's analytic soft shadow, leo-parpeix-portfolio-2026's full-viewport `ShadowMaterial` at 0.25 (which also darkens its type: keep the catcher out from under text), the two-layer contact shadow in [three-hero.js](../recipes/three-hero.js).
- **Bloom.** Winners range from luminosity threshold 0 (active-theory-v6, per-scene bloom values up to 3.82) and strength 2.2 at threshold 0.38 (immersive-garden-website) to threshold 1 at strength 0.25 (brunos-portfolio) and threshold 1 (the-power-of-storytelling). Take the last two.
- **CA, grain and post shades stay off text.** shader-development-studio's aberration (up to 2.5) fringes its ~20 px in-canvas nav and body copy; the-watch's post shade and particle ribbons lie over DOM type because its canvas sits above the DOM. Stack the canvas under the copy.
- **No banding.** Fog, sky and vignette gradients get dither: `material.dithering = true` on lit materials, or blue noise in the final pass (everswap's final pass, igloo-inc's crystal sampling). A banded canvas gradient is the law's banded-gradient tell.
- **Antialias.** With post: `antialias: false` plus SMAA, FXAA or TAA (akaru-2 SMAA, hubtown and cartier-watches-wonders-2025 FXAA, oryzo-ai TAA). brunos-portfolio skips AA at DPR ≥ 2.
- **Palette.** Fog = clear colour = page background at the canvas edge, so the world dissolves into the page. Hand section colours through the canvas instead of cutting them (lando-norris scrubs the GL background per section and mirrors it to the body). The law holds inside the canvas: no cream studio backdrop (floema's fog is #f3efea; cartier-watches-wonders-2025's beige floors are its own teardown's slop flag), no default blue-charcoal void, no violet-cyan iridescence (zentry's glowing wireframe flower), no saturated rim light (why-zero's cyan rim and mint #C5FFCB freeze edge).
- **Motion.** No idle auto-rotate under copy (messenger's camera laps the title planet once a minute, acceptable only on a game title screen) and no bobbing float. Objects move with scroll or pointer and settle.

## Asset pipeline

1. **Author** in Blender or C4D: 1 unit = 1 m, transforms applied, Principled BSDF only, procedurals baked, every node you animate, raycast or swap named. C4D exports no lights, no node shaders and one UV set [webgl-3d-stack §7.1].
2. **Bake** Cycles Combined or Diffuse + AO into atlases (2048 mobile, 4096 for one desktop hero atlas); pack AO into the R channel of ORM. Bias texel density toward what the camera sees: oryzo-ai warps coverage so the centre 50% of the desk gets about 90% of the texels [imagery §1.8].
3. **Export GLB with Draco off**, split by job: visual, physics and placement files (brunos-portfolio); per layer and per locale (san-rita swaps only `sanrita-trails@fr.glb` on a language change); desktop and mobile or high and low (cartier-watches-wonders-2025 `productsMobile.glb`, immersive-garden-website `reliefs_low_compressed.glb`); a low-poly raycast proxy (artefakt); animation-only camera GLBs (the-power-of-storytelling).
4. **Optimize once** with glTF Transform 4.5: `gltf-transform optimize in.glb out.glb --compress meshopt --texture-compress ktx2 --texture-size 2048`; add `--flatten false` for rigs and `--simplify false` for hard-surface silhouettes. That routes normal and ORM to UASTC and colour to ETC1S (needs KTX-Software ≥ 4.4). Meshopt by default, Draco for dense scans, and serve with brotli [webgl-3d-stack §7.2]. 14/51 winners ship KTX2 and 19 ship GLB [probe].
5. **Environment:** 1k HDR/EXR (`HDRLoader`, renamed from `RGBELoader` in r180) or an UltraHDR gain-map JPEG (`UltraHDRLoader`), run through PMREM once and reused, or shipped pre-baked as KTX2.
6. **Load** with `GLTFLoader` + `KTX2Loader.detectSupport(renderer)` + `MeshoptDecoder`, decoders self-hosted (drei pulls Draco from gstatic, detect-gpu pulls benchmarks from unpkg) [webgl-3d-stack §7.3].
7. **Source** your own models first. Poly Haven is CC0; Fab assets may not be redistributed standalone, so ship them merged and compressed, never as a clean GLB; CC-BY needs a credit [webgl-3d-stack §7.5].

Counterexample: the-power-of-storytelling ships a 4.35 MB Draco phoenix (121,364 triangles, 237-joint skin), no KTX2 and raw TTF fonts. It won on art direction, not on pipeline. Custom binaries (Lusion's `.buf` on everswap and oryzo-ai, Hydra's `.bin` geometry on slosh-seltzer) only pay off with an engine you own.

## Budgets and render-loop rules

| Budget | Mobile | Desktop | Basis |
|---|---|---|---|
| DPR, light scene | `min(dpr, 2)`, 1.5 on coarse pointers | `min(dpr, 2)` | floema, pacome-pertant-portfolio, tracing-art, gil-huybrecht; three-hero |
| DPR, full-screen post | 1.15-1.5 | 1.25-1.5 | lando-norris 1.25 above 768 px; igloo-inc and messenger 1.15 on ≤ 2x screens, 1.5 above; artefakt, shader-development-studio 1.5 |
| 3D before first interaction | ≤ 1.5 MB | ≤ 3 MB | house rule [webgl-3d-stack §6.1]; met by iyo and messenger (~1 MB declared in total); 9 winners declare 9-19.5 MB (vast, the-watch, gq-ap-the-extraordinary-lab, steven-com, lacoste-polo-factory, san-rita, leo-parpeix-portfolio-2026, hubtown, cartier-watches-wonders-2025) |
| Texture edge | 2048 | 4096 for one hero atlas | 2048² with mips = 22.4 MB as RGBA, 5.6 MB as KTX2 8 bpp [webgl-3d-stack §6.1] |
| Draw calls | < 100 | < 300 | house rule [webgl-3d-stack §4.2] |
| Hero triangles | ≤ 100k | ≤ 300k | house rule |
| Real-time shadow lights | 0-1 | 1 | house rule |
| WebGL contexts | 1 | 1 | Chromium keeps 16 and drops the oldest |
| Frame delta clamp | 1/30 s | 1/30 s | lando-norris; pacome-pertant-portfolio uses 50 ms |

- **Init after LCP.** igloo-inc serves a 1.4 KB HTML shell, then a 16.5 KB loader, then imports the 1.49 MB 3D chunk. Import three after `load`, the first LCP entry and idle (`setTimeout` fallback: Safari has no `requestIdleCallback`). Wiring: [boot.html-snippet.html](../recipes/boot.html-snippet.html) import map plus the lazy import inside [three-hero.js](../recipes/three-hero.js).
- **Compile before reveal.** cartier-watches-wonders-2025 runs `compileAsync` on every universe behind its loader; everswap compiles in the preloader; why-zero prewarms its shatter pass into a 1x1 target and drops DPR to 0.8x while the gate runs, so the payoff never hitches.
- **Render on demand.** Stop the loop when nothing moves ([three-hero.js](../recipes/three-hero.js); R3F `frameloop="demand"`). Refresh static layers on change only: floema's shadow map, shader-development-studio's text texture on its first 4 frames and then at most every 400 ms.
- **Pause offscreen and hidden.** IntersectionObserver on the section plus `visibilitychange`, and `THREE.Timer.connect(document)` so the delta does not spike on return [webgl-3d-stack §6.2]. akaru-2 pauses outside its section; pacome-pertant-portfolio pauses 500 ms after leaving its route; shader-development-studio renders scenes only inside offset windows.
- **Adapt from measured frame time.** why-zero: 60-frame window, downgrade above 22 ms, upgrade below 12 ms, 180-frame cooldown, DPR tiers 2 / 1.5 / 1. igloo-inc: DPR multiplier -0.1 below 30 fps and +0.1 at 60 over ~4 s windows (floor 0.6), stop after 4 direction flips. the-renaissance-edition: step quality below 45 fps, cap the low tier at 30 fps, DPR from a pixel budget of 1280 / 1920 / 3840 px. hubtown: 2 → 1.5 → 1.25.
- **GPU tier is a first guess.** detect-gpu runs on 3/51 (akaru-2, ponpon-mania, the-renaissance-edition); ponpon-mania maps tier to DPR (tier 3: 1.5-2, below tier 2: 1.15) and ships `-small.basis` textures; hubtown drops bloom when the renderer string says Intel HD. detect-gpu's benchmark data froze in Dec 2025: self-host it and let measured frame time overrule it [webgl-3d-stack §2].
- **Instance and atlas.** tracing-art draws ~1,000 thumbnails and 640-960 blank rects in a few draw calls with instanced attributes and up to 3 atlases.
- **Workers only when the main thread is the bottleneck.** floema renders each scene on an OffscreenCanvas worker, and each worker ships its own three (~1.04-1.17 MB).

## Mobile and no-WebGL fallbacks

What winners do: of 34 realtime 3D sites, 28 run the scene on phones (seen at 390 px or confirmed in code), 4 ship a static path (gil-huybrecht, lama-lama-2, the-renaissance-edition, vast inferred) and 2 are unverified (siena-film-foundation, slosh-seltzer). Partial degradation shows on artefakt (only the particle logo below 1200 px), zentry (intro Spline becomes a vertical mp4), leo-parpeix-portfolio-2026 (no fluid on coarse pointers below 1025 px). 11/51 sites have any reduced-motion rule [probe]; among the 3D sites only the-renaissance-edition gates motion in both CSS and JS, and vast scales every CSS duration by a `--motion` token.

| Tier | Trigger | Ships | Basis |
|---|---|---|---|
| Poster | no JS, no WebGL2, `failIfMajorPerformanceCaveat`, Save-Data, GPU tier 0, reduced motion | DOM poster + copy; the canvas never loads | vast's `data-webgl-fb` stills; the-renaissance-edition's fallback image scene |
| Lite | coarse pointer, < 1025 px, tier 1, `deviceMemory` ≤ 4 (Chromium hint only) | same scene with mobile GLBs and textures, DPR ≤ 1.5, no DOF, motion blur or grain, fewer particles, no cursor sims | cartier-watches-wonders-2025, messenger (low-memory path for iPhones), oryzo-ai (576 particles) |
| Full | fine pointer, tier 2-3, measured fps holds | everything | rule 11 |

- **Re-author for portrait, don't shrink.** A portrait camera track (the-power-of-storytelling), a portrait render set (terminal-industries, 409 frames), a pulled-back camera with its own texture and a slider instead of hover (steven-com), a letterboxed band (hubtown), a mask scaled 1.5x (ponpon-mania).
- **A static phone path is a design choice.** the-renaissance-edition routes every phone through painted stills in the same transition shader and still made the SOTM list.
- **Hover effects need hover.** Gate with `(hover: hover) and (pointer: fine)` (gil-huybrecht); lama-lama-2 gives touch the plain media.
- **Do not hijack scroll.** `touch-action: pan-y` on the canvas; a real gesture gets an explicit switch (lando-norris).
- **The poster page is the unsupported-browser page.** Never redirect to `unsupported.html` (active-theory-v6, slosh-seltzer).
- **Context loss:** fade the canvas out and rebuild PMREM and render targets on restore. Both recipes test this path, plus reduced motion (OS and in-page toggle, live), no JS, blocked CDN and SwiftShader.
- **Reduced motion:** one still, or hard cuts between held beats. The recipes follow `<html data-motion>` and the `motionchange` event from [motion-core.js](../recipes/motion-core.js); see [motion.md](./motion.md).

## UI drawn in WebGL and its accessibility cost

Who does it: messenger draws every string with GPU vector glyphs (no DOM headings, no DOM buttons, the BEGIN CTA is not focusable, and its off-white on mustard sits near 1.3:1). slosh-seltzer draws type as MSDF and mirrors it into a DOM shadow layer (GLA11y). shader-development-studio renders UI inside the canvas with pmndrs uikit and rasterises titles to render targets. gq-ap-the-extraordinary-lab's title is a video texture with no `h1`. brunos-portfolio has no DOM heading on its first screen. steven-com's 3D is its navigation (armillary dial, slider on phones). MSDF labels inside the scene appear on cartier-watches-wonders-2025, david-whyte-experience, igloo-inc (the logo), lando-norris (GL marquee), oryzo-ai and hubtown.

The cost: 3D winners average 6.81 on accessibility vs 7.07 without; the floor is 6.0 (gq-ap-the-extraordinary-lab, iyo, lacoste-polo-factory), then the-watch at 6.2 (teardowns). The wider corpus shows no gap (6.98 vs 6.85), so the loss comes from choices like these, not from WebGL.

Crafted version:
1. The DOM owns every word and control; the canvas is `aria-hidden`. A GL echo of a headline (MSDF, particles) sits over a real `h1` that stays in the accessibility tree (lando-norris keeps its headings as `.screen-reader` elements). If the DOM copy must be visually hidden, use a clip pattern, never opacity 0 waiting on a reveal.
2. Every raycast target has a DOM `<button>` positioned each frame from its projected 3D anchor (`Vector3.project` → CSS transform), in tab order, with a visible focus state. Enter runs the same camera move as a click.
3. Native scroll stays the input, so keyboard, anchors and find-in-page drive the story [usability-a11y-perf §3.4].
4. Anything that moves on its own for more than 5 s beside text gets a pause control (SC 2.2.2) [usability-a11y-perf §2 B].
5. Measure contrast against the worst frame behind the text [usability-a11y-perf §2 D]; never set `user-scalable=no` (active-theory-v6, leo-parpeix-portfolio-2026 and immersive-garden-website do).
6. When canvas UI is the point (a game, messenger), ship a DOM start button and a skip link to the plain content.

## Crafted vs slop

| Award habit | Slop version | Crafted version |
|---|---|---|
| Iridescent hero object (zentry's violet, cyan and magenta wireframe flower) | A glowing purple-cyan blob or orb with no subject | The brand's real object in one considered material under one directional key with falloff |
| Whole-frame bloom (active-theory-v6 threshold 0, immersive-garden-website strength 2.2) | Everything glows; a radial halo sits behind the hero | Threshold ≥ 1, strength ≤ 0.3, only true emissives bloom (brunos-portfolio) |
| Lit disc behind the product (cartier-watches-wonders-2025's Icons universe, flagged in its teardown) | A concentric glow ring as the hero's backdrop | A rake or single directional key with falloff and a contact shadow |
| Idle auto-rotate (messenger's title planet) | A turntable spinning under body copy | The object rests; scroll or pointer moves it; the loop stops when it settles |
| Headline drawn only in canvas (iyo particles, gq-ap-the-extraordinary-lab video title) | Empty accessibility tree; a blank hero if WebGL stalls | A DOM `h1` always visible; the GL version is an echo |
| Copy waiting on the GL intro (cartier-watches-wonders-2025 sets title chars to opacity 0 in CSS) | The invisible-content trap | Poster and copy paint first; only the canvas fades in, after its first frame |
| CA and grain over UI (shader-development-studio, the-watch) | Fringed nav text, muddy body copy | CA ≤ 1 px on canvas edges, grain on the substrate, text crisp above both |
| Cursor fluid on every section | Rainbow swirls at 0.08 UV | One ink colour, ≤ 0.04 UV, one section (everswap), off on touch and reduced motion |
| Particle field behind the page | A twinkling starfield on a fixed layer that trails the scroll | Particles form the subject (artefakt's logo) and react to input; a fixed field must recolour and respond per section (lando-norris's contours) |
| Neon rim light (why-zero's cyan rim) | A saturated accent rim | A tonal rim tinted toward the background |
| Warm studio fog (floema #f3efea) | A cream canvas backdrop | Fog = a chosen brand surface; the canvas edge disappears into the page |
| Offset quad as a UI shadow (messenger's HUD tiles) | A hard second box behind the element | A tight directional shadow, or an outline system that owns the whole look |
| Full scene on every phone (28/34) | 12 MB over 4G behind a black loading frame | Poster, lite and full tiers chosen from measured fps (the-renaissance-edition, why-zero) |
| `unsupported.html` redirect (active-theory-v6, slosh-seltzer) | A dead page on older browsers | The poster page is the fallback |

## Exemplars

- **lando-norris**: fluid-sim reveal of a render-target helmet over a displaced portrait relief; DPR 1.25; 1.54 MB of 3D; the touch paint switch; per-section GL colour hand-off.
- **messenger**: the outline + 3D LUT pipeline, adaptive DPR, a low-memory iPhone path, and what all-canvas UI costs.
- **igloo-inc**: baked lightmap crossfades, a transmission crystal done right, adaptive DPR that gives up after 4 flips, a 1.4 KB shell.
- **oryzo-ai**: pre-rendered plate + realtime hero + splats only on props; realism spent where the pointer is.
- **the-renaissance-edition**: painted dioramas, lazy scene chunks, detect-gpu + fps guard, and the best phone fallback in the sample.
- **gil-huybrecht**: one canvas, KTX2 per image with an LRU cache, the `has-gl` media gate.
- **the-power-of-storytelling**: camera and art direction as animation-only GLBs, a portrait camera track, a custom glass keyframed along the story.
- **gq-ap-the-extraordinary-lab**: sketch lines from per-edge model attributes, a LUT grade, Theatre.js; accessibility at 6.0 as the warning.
- **brunos-portfolio**: WebGPU + TSL with a WebGL2 fallback, split visual/physics/placement GLBs, authored colour kept by skipping tone mapping.
- **terminal-industries**: a 410-frame scroll film loaded coarse-to-fine, with its own 409-frame portrait render.
- **lama-lama-2**: raw WebGL2 dither of real media, a velocity trail, plain media on touch.
- **cartier-watches-wonders-2025**: per-material environments, every scene precompiled, mobile GLB variants, a one-pass post shader.

## Evidence

- `data/teardowns/<slug>.json`, fields `three_d`, `imagery`, `performance_accessibility`, `slop_risks` and `scores`, for all 51 sites. Role, engine and fallback counts above are my classification of those fields; items marked "inferred" in the teardowns are labelled inferred here. Payloads are declared bytes, not transfer. lando-norris's FOV 15 comes from its bundle dump (`evidence/probe/landonorris.com.txt`, `new A8(15, aspect, 0.1, 1000)`).
- `evidence/digests/three_d.md`: the same fields concatenated across the 51 sites.
- [probe]: `data/probe_summary.json`: canvas contexts (webgl2 41, 2d 35, webgl 9, webgpu 2; the counts include Rive and third-party probes), 26 sites loading 3D assets, asset types glb 19 / ktx2 14 / exr 7 / hdr 4 / drc 2 / basis 1, reduced-motion rules on 11.
- [stats]: `data/stats.md`, recent_2024_plus cut: tags WebGL 82, 3D 80, Three.js 51 of 575, with 3D and WebGL listings sampled at 62 each.
- [webgl-3d-stack]: `data/research/webgl-3d-stack.md`: live bundle probe of 22 recent winners (§1), versions and licensing (§2), decision tree (§3), role recipes (§4, incl. §4.9 displaced surfaces, §4.10 splats), taste (§5), budgets, render loop and bootstrap (§6), pipeline and sources (§7), failure modes (§8).
- [usability-a11y-perf]: `data/research/usability-a11y-perf.md` §1.4 (3D vs non-3D dev scores, n = 185 tagged of 308), §2 (gate), §3.4 (smooth scroll), §3.5 (WebGL hero boot).
- [imagery]: `data/research/imagery.md` §1.7-1.8 (pre-rendered vs realtime 3D, Oryzo splats), §2.10 (image sequences).
- Recipes: [three-hero.js](../recipes/three-hero.js), [webgl-image-hover.js](../recipes/webgl-image-hover.js), [boot.html-snippet.html](../recipes/boot.html-snippet.html), [motion-core.js](../recipes/motion-core.js), test harness [demo/webgl.html](../recipes/demo/webgl.html) (neutral on purpose; not a design template).
- Casebook entries for every slug above: [casebook.md](./casebook.md). Sequences and imagery treatments: [imagery.md](./imagery.md).
