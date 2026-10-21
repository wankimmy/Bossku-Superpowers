# 3D and WebGL on award-winning sites: stack, asset pipeline, effects, performance

Last updated: 2026-09-24

This is the reference an agent reads before putting a canvas on a page. It covers what Awwwards winners actually ship (checked in their live bundles on 2026-09-24), current versions and licensing, a decision tree for how much 3D to use, build recipes for each common 3D role, taste rules, performance budgets, fallbacks, and the failure modes that make 3D look cheap.

How claims are labelled:

- **Documented**: stated in vendor docs, source code, release notes or registry metadata. Linked inline.
- **Observed**: found in the production JS/HTML of an awarded site. The probe method is described in section 1.
- **House rule**: a working budget or taste call from this skill. It is not a vendor number, and it is labelled wherever it appears.
- **(unverified)**: I could not confirm it from a live source.

The house design law (`deslop-law.md`) takes priority over award-site habits. Where the two conflict, this file says so and gives the crafted alternative.

---

## 1. Evidence: what winners ship (observed 2026-09-24)

**Award share.** 22 of the last 31 Sites of the Day (2026-08-26 to 2026-09-25) carry a `WebGL`, `Three.js` or `3D` tag. So do 9 of the last 12 Sites of the Month (2025-09 to 2026-08). Only 10 SOTDs carry the `Three.js` tag itself. Submitters choose these tags, so they under-report the engine ([SOTD listing](https://www.awwwards.com/websites/sites_of_the_day/), [SOTM listing](https://www.awwwards.com/websites/sites_of_the_month/)).

**Probe method.** For each site I fetched the HTML and the same-origin JS, including chunk URLs referenced one level down, and ran a regex scan. The three.js revision comes from the `__THREE__ = <var>` assignment. Anything lazy-loaded deeper than one level is missed, so a "not found" result is weak evidence. Loader evidence uses strict signatures only:
- `basis_transcoder` or a `.ktx2` URL for KTX2
- `draco_decoder` or `draco_wasm_wrapper` for DRACOLoader
- `decodeVertexBuffer` for the Meshopt decoder

Extension-name strings don't count, because `GLTFLoader` contains all of them.

| Site | Award (listing date) | Engine observed | Asset signals | Other observed |
|---|---|---|---|---|
| [bruno-simon.com](https://bruno-simon.com) | SOTM (2026-01-21) | three **r183 `WebGPURenderer`** + TSL `RenderPipeline` | KTX2, Draco | drivable 3D "world" |
| [floema.com](https://www.floema.com/en) | SOTM (2026-05-13) | three **`WebGPURenderer`** + TSL | none found | Rive runtime, GSAP ScrollTrigger, Lenis |
| [oryzo.ai](https://oryzo.ai) | SOTM (2026-04-13) | three `WebGLRenderer` + its own `postprocessing` object | none found | Rive; custom post shader strings (chromatic, vignette, fbm) |
| [landonorris.com](https://landonorris.com/) | SOTM (2025-11-17) | three **r174** `WebGLRenderer` + three-addons `EffectComposer`/`UnrealBloomPass` | Draco, `.hdr` | Rive; `divergence` + simplex strings (fluid sim); Webflow |
| [shopify.com/editions/winter2026](https://www.shopify.com/editions/winter2026) | SOTM (2026-02-09) | engine not found in fetched chunks | 40 `.ktx2` URLs | Rive, Theatre.js, `detect-gpu` |
| [ponpon-mania.com](https://ponpon-mania.com/) | SOTM (2025-10-22) | not identified | KTX2 transcoder ref | `detect-gpu`; simplex + `divergence` (fluid) |
| [lamalama.com](https://lamalama.com/) | SOTM (2026-07-20) | no WebGL library found | none | 24 `<video>` tags, so pre-rendered motion (unverified whether a lazy WebGL chunk exists) |
| [sharplink.com](https://www.sharplink.com/) | SOTD 2026-08-27 | three **r179 `WebGPURenderer`** | none | Vue |
| [moto-card.com](https://www.moto-card.com/) | SOTD 2026-09-24 | three **0.181.1 `three/webgpu` + `three/tsl`** via a jsDelivr import map on Webflow | `GLTFLoader` | ships a leftover `http://192.168.1.15:3000/...` script tag (LAN dev server) |
| [illoca.unseen.co](https://illoca.unseen.co/) | SOTD 2026-09-04 | three r183 `WebGLRenderer` + three-addons `EffectComposer`/`OutputPass` | KTX2, Draco | Theatre.js (heavy use) |
| [gilhuybrecht.com](https://gilhuybrecht.com/) | SOTD 2026-09-21 | three r185 | none (strict) | `setPixelRatio(Math.min(2, devicePixelRatio))`; WebGL gallery with infinite scroll |
| [lisa.locomotive.ca](https://lisa.locomotive.ca/en) | SOTD 2026-09-16 | three r165 | Draco, `.hdr` | DPR clamp 2; Blender tag |
| [cerebrium.ai](https://cerebrium.ai/) | SOTD 2026-09-10 | three r183 + three-addons `EffectComposer`/`UnrealBloomPass`/`OutputPass` | Meshopt, Draco | DPR clamp 2; Cinema 4D tag |
| [usavionix.com](https://www.usavionix.com/) | SOTD 2026-09-09 | **R3F** + three r180 | Meshopt, Draco, 26 `.glb` refs | `frameloop: "demand"` |
| [seasats.com](https://www.seasats.com/) | SOTD 2026-09-08 | **R3F** + three r180 | KTX2, Meshopt, Draco | Cinema 4D tag |
| [why.zero.university](https://why.zero.university/) | SOTD 2026-09-07 | three | KTX2, Draco | DPR clamp 2; Blender tag |
| [gionatannese.com](https://www.gionatannese.com/) | SOTD 2026-09-05 | three r184 + three-addons `EffectComposer`/`UnrealBloomPass` | none | `ACESFilmicToneMapping`, exposure 1.1 |
| [noho.ink](https://noho.ink) | SOTD 2026-09-18 | three r182 on Webflow | KTX2, Meshopt, Draco | `toneMapping=7` (`NeutralToneMapping`) |
| [leoparpeix.com](https://leoparpeix.com/) | SOTD 2026-09-14 | three **r153** + three-addons `EffectComposer`/`ShaderPass` | KTX2, Draco | `divergence` strings (fluid); Blender tag |
| [aspensearch.com](https://www.aspensearch.com/) | SOTD 2026-09-15 | **R3F** | none | none |
| [pensatori-irrazionali.com](https://pensatori-irrazionali.com/) | SOTD 2026-09-20 | WebGPU strings; three not found in fetched chunks | KTX2 | none |
| [unbelievablycrap.com](https://www.unbelievablycrap.com/) | WebGL listing 2026-09-21 (award level not checked) | **R3F** | `.glb` | config for a "halftone echo layer": a dot-screened clone of the sphere |

What these results mean for a build:

1. **three.js is the engine.** Every probed winner with an identifiable engine used it. R3F turned up on 4 of 22 (USAvionix, Seasats, Aspen Search, Unbelievably Crap), which is about a sixth. Revisions ranged from r153 to r185, so winners do not chase the latest release.
2. **WebGPU is in production, but it's the minority path.** `WebGPURenderer` code ships on 4 winners (Bruno Simon, Floema, Sharplink, Moto). The rest use `WebGLRenderer`, and three's own manual still calls the WebGPU renderer "experimental" (section 2).
3. **Compressed assets are table stakes.** 12 probed sites bundle `GLTFLoader`, and 10 of those also ship DRACOLoader. Across the whole probe, 9 sites reference KTX2 textures and 4 bundle the Meshopt decoder. Draco is still more common than Meshopt in the wild. That is inertia, not a recommendation; see section 7.
4. **The DPR clamp at 2 is the norm.** `Math.min(devicePixelRatio, 2)` appears literally on Cerebrium, Gil Huybrecht, L.I.S.A. and Why Zero.
5. **Post-processing uses three's own addons.** Several winners use three's `EffectComposer`: `UnrealBloomPass` on Cerebrium, Gionatannese and Lando Norris, `ShaderPass` on Léo Parpeix. Oryzo runs its own pipeline. I found no pmndrs `postprocessing` signature, though my regex for it was weak. Bloom is used on winners. I did not check visually whether it is thresholded; the rule in section 5 applies either way.
6. **Rive is the common 2D companion** to the 3D layer: Floema, Oryzo, Lando Norris and Shopify Editions all ship it.
7. **Theatre.js is still used for authored camera timelines** (illoca, Shopify Editions), even though its last npm release is 0.7.2 from 2024-05-19 ([npm](https://www.npmjs.com/package/@theatre/core)).
8. **No-code runtimes were absent.** No Spline, Unicorn Studio, Needle or OGL runtime signature appeared in any probed winner. At SOTM level teams hand-build on three.js. That is absence in a sample of about 25 sites, not proof.
9. **Pre-rendered video is a winning path.** Lama Lama (SOTM) and several WebGL-tagged SOTDs showed heavy `<video>` use and no WebGL library in the fetched code.

---

## 2. Verified versions, support and licensing (as of 2026-09-24)

Versions and dates come from the npm registry `dist-tags.latest` and publish time unless another source is linked.

| Tool | Current | Status / license | What matters for a build | Source |
|---|---|---|---|---|
| **three.js** | **0.186.1 (r186)**, released 2026-09-24; r185 was 2026-07-01 | MIT | r186 adds a core `GaussianSplat` renderer and loader (TSL, WebGPU/WebGL, glTF import) and removes `PCFSoftShadowMap` (it now warns). It also removes top-level side effects from some modules for better tree-shaking. | [r186 release](https://github.com/mrdoob/three.js/releases/tag/r186) |
| three **WebGPURenderer** | ships in `three/webgpu` | "still in an experimental state although its maturity level has been greatly improved" | Falls back to WebGL2 automatically; `forceWebGL: true` forces it. Initialises asynchronously: use `setAnimationLoop` or `await renderer.init()`. **`ShaderMaterial`, `RawShaderMaterial`, `onBeforeCompile` and `EffectComposer` are not supported.** Port to node materials, TSL and `RenderPipeline`. | [manual](https://github.com/mrdoob/three.js/blob/dev/manual/pages/webgpurenderer.html) |
| three **TSL** | `three/tsl` | part of three | Transpiles to WGSL or GLSL. Post-processing is `THREE.RenderPipeline` (renamed from `PostProcessing` in r183) + `pass()`. | [post manual](https://github.com/mrdoob/three.js/blob/dev/manual/pages/webgpu-postprocessing.html), [r183](https://github.com/mrdoob/three.js/releases/tag/r183) |
| three API churn | r180–r183 | n/a | `RGBELoader` renamed `HDRLoader` (r180). `Clock` replaced by `Timer` (r183); `Timer.connect(document)` zeroes the delta while the tab is hidden. `UltraHDRLoader` loads gain-map JPEG HDRs (used in examples since r182). | [r180](https://github.com/mrdoob/three.js/releases/tag/r180), [Timer.js](https://github.com/mrdoob/three.js/blob/r186/src/core/Timer.js), [UltraHDRLoader](https://github.com/mrdoob/three.js/blob/r186/examples/jsm/loaders/UltraHDRLoader.js) |
| **Browser WebGPU** | see next column | caniuse data update 2026-09-24 | **Chrome/Edge 113+** (Linux support depends on hardware and drivers from 144). **Chrome Android** yes (current 152). **Safari 26+ macOS** partial: on by default only on macOS 26 Tahoe. **iOS Safari 26+** yes. **Firefox 141+** Windows only; **145+** adds macOS 26 on Apple Silicon; off by default on Linux and Android. Global usage: 85.72% full + 3.05% partial. **WebGL2: 96.44%.** | [caniuse WebGPU data](https://github.com/Fyrd/caniuse/blob/main/features-json/webgpu.json), [caniuse WebGL2](https://caniuse.com/webgl2) |
| **@react-three/fiber** | **9.8.1** (2026-09-24) | MIT | peer `react >=19 <19.4`. `gl` may be an async factory returning `WebGPURenderer`. **v10.0.0-alpha.5** (2026-09-08) is the pre-release with first-class WebGPU/TSL. | [releases](https://github.com/pmndrs/react-three-fiber/releases), [canvas docs](https://github.com/pmndrs/react-three-fiber/blob/master/docs/API/canvas.mdx) |
| **@react-three/drei** | **10.7.8** (2026-08-05) | MIT | peer fiber `^9`. drei 11 is alpha (pairs with R3F 10). `useGLTF` loads the Draco decoder from **gstatic 1.5.5 by default** and sets up no KTX2 loader. | [npm](https://www.npmjs.com/package/@react-three/drei), [Gltf.tsx](https://github.com/pmndrs/drei/blob/master/src/core/Gltf.tsx) |
| **postprocessing** (pmndrs) | **6.39.5** (2026-09-09) | Zlib | peer `three >=0.168 <0.187`. `WebGLRenderer` only. v7 is beta. `@react-three/postprocessing` **3.1.2** needs fiber `>=9.7`. | [repo](https://github.com/pmndrs/postprocessing), [npm](https://www.npmjs.com/package/@react-three/postprocessing) |
| **OGL** | **1.0.11** (2025-01-27) | Unlicense | Last commit 2025-04-13: small and stable, but dormant. No OGL signature was found in the probed winners (my regex was weak). | [repo](https://github.com/oframe/ogl) |
| **Spline** | `@splinetool/runtime` **2.0.57** (2026-09-24); `@splinetool/react-spline` 4.1.0 | proprietary | **Renders on WebGPU by default, falls back to WebGL.** Export options: Public URL (iframe), `<spline-viewer>` (lazy-loads by default, can capture page scroll), Code export (Vanilla/React/Next, plus three.js/R3F variants without animations or events). The scene file is served from Spline unless you use **Self-hosted export, which is Enterprise-only**. Pricing: **Free = watermark. Hobby $12/seat/mo annual ($15 monthly) removes it. Pro $25 ($30) adds downloadable code export and glTF with color and texture. Max $60 ($70).** | [pricing](https://spline.design/pricing), [code export](https://docs.spline.design/exporting-your-scene/web/exporting-as-code), [self-hosted](https://docs.spline.design/exporting-your-scene/web/exporting-as-self-hosted-project), [viewer](https://docs.spline.design/exporting-your-scene/web/exporting-as-spline-viewer) |
| **Unicorn Studio** | SDK `unicornstudio.js` **v2.2.14** (2026-09-12); `unicornstudio-react` 2.2.13 | proprietary SDK | Runtime is about 40–50 KB gzipped. **Free: up to 8 publishes with Unicorn branding, personal and non-commercial only. Legend: $168/yr or $20/mo**, adds commercial license, no watermark and JSON export for self-hosting (`data-us-project-src`). Knobs: `data-us-scale`, `-dpi` (default 1.5), `-fps`, `-lazyload`, `-production`. | [pricing](https://www.unicorn.studio/docs/pricing/), [embed](https://www.unicorn.studio/docs/embed/), [repo](https://github.com/hiunicornstudio/unicornstudio.js) |
| **Needle Engine** | npm **`latest` = 6.0.0-alpha.3**; **`stable` = 5.1.13** (2026-09-09) | proprietary | Plain `npm i @needle-tools/engine` installs an **alpha**, so pin `@stable`. Needle builds on its own three fork (`@needle-tools/three@0.169.x` for 5.x). **Hobby: free, non-commercial, Needle branding. Pro: €49/seat/mo billed annually**, for commercial use and self-hosting. | [pricing](https://needle.tools/pricing), [npm](https://www.npmjs.com/package/@needle-tools/engine) |
| **Spark** (Gaussian splats) | `@sparkjsdev/spark` **2.2.0** (2026-09-11) | MIT, by World Labs | three `>=0.180` peer, `WebGLRenderer`. Reads PLY, SOGS, SPZ, `.splat`, `.ksplat`. 2.0 adds LoD splat trees, streamable `.RAD` over HTTP Range and a 16M-splat paged GPU pool. | [site](https://sparkjs.dev/), [2.0 features](https://sparkjs.dev/docs/new-features-2.0/) |
| three core `GaussianSplat` | new in r186 | MIT | Landed on release day, so treat it as experimental. | [r186](https://github.com/mrdoob/three.js/releases/tag/r186) |
| PlayCanvas + SuperSplat | `playcanvas` **2.22.4**; `@playcanvas/splat-transform` **3.6.4** | MIT | **SOG is about 15–20× smaller than PLY** (lossy). SuperSplat auto-streams scenes of 1M Gaussians or more as LoD "Streamed SOG". | [SOG](https://developer.playcanvas.com/user-manual/gaussian-splatting/formats/sog/), [SplatTransform](https://developer.playcanvas.com/user-manual/splat-transform/) |
| **KHR_gaussian_splatting** | spec README says "Complete, Ratified" | Khronos | Release candidate announced 2026-02-03. SplatTransform already writes GLB with it. | [spec](https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Khronos/KHR_gaussian_splatting/README.md), [press](https://www.khronos.org/news/press/gltf-gaussian-splatting-press-release) |
| Older splat renderers | `@mkkellogg/gaussian-splats-3d` 0.4.7 (2025-01-25); `gsplat` 1.2.9 (2025-07-12) | MIT | Stale. Don't start new work on them. | npm |
| **Rive** | `@rive-app/webgl2` **2.43.1**, `@rive-app/canvas` 2.43.1, `@rive-app/react-canvas` 4.35.0 | runtimes MIT | Use **webgl2** (Rive Renderer) for fidelity; use canvas or canvas-lite when many instances are on screen. `@rive-app/webgl` is deprecated after 2.37.0. **Editor: Free lets you create; Cadet $9/seat/mo is the tier that lists "Export .riv files".** Voyager $32, Enterprise $120. | [renderer choice](https://rive.app/docs/runtimes/web/canvas-vs-webgl), [pricing](https://rive.app/pricing) |
| **glTF Transform** | CLI **4.5.0** (2026-09-01) | MIT | `optimize` defaults: Meshopt compression, `--texture-compress auto`, `--texture-size 2048`, simplify/weld/join/flatten/instance/palette/prune all on. `etc1s`/`uastc` need **KTX-Software ≥ 4.4.0** (`ktx` CLI). KTX-Software stable is v4.4.2 (2025-10-04); v5.0.0-rc2 is a pre-release. | [CLI](https://gltf-transform.dev/cli), [cli.ts](https://github.com/donmccurdy/glTF-Transform/blob/main/packages/cli/src/cli.ts), [toktx.ts](https://github.com/donmccurdy/glTF-Transform/blob/main/packages/cli/src/transforms/toktx.ts), [KTX-Software](https://github.com/KhronosGroup/KTX-Software/releases) |
| **Blender** | **5.2.2 LTS** (2026-09-15) | GPL | Built-in glTF exporter | [download](https://www.blender.org/download/) |
| **Cinema 4D** glTF export | 2026 help | proprietary | Node materials not supported, shaders must be baked, lights are not exported, one UV set per object; use "Flip Z" | [exporter](https://help.maxon.net/c4d/en-us/Content/html/FGLTFEXPORTER.html), [materials](https://help.maxon.net/c4d/2026/en-us/Content/html/FGLTFEXPORTER-GLTFEXPORTER_GRP_MATERIALS.html) |
| `@pmndrs/detect-gpu` | **6.0.23** (renamed from `detect-gpu`) | MIT | Tiers: 0 (no WebGL, blocklisted or under 15 fps), 1 (≥15), 2 (≥30), 3 (≥60). **Its gfxbench data source stopped updating in Dec 2025**, and it loads benchmarks from unpkg unless you self-host them. | [README](https://github.com/pmndrs/detect-gpu) |
| Globe libs | `cobe` **2.0.1** (~5 KB, MIT); `three-globe` 2.45.2 | MIT | cobe v2 supports CSS-anchor-bindable markers and arcs | [cobe](https://github.com/shuding/cobe) |
| Scroll/motion glue | `gsap` 3.15.0 ("Standard no charge license"); `lenis` 1.3.26 (MIT) | n/a | Lenis README gives the ScrollTrigger sync snippet (section 4.1) | [lenis](https://github.com/darkroomengineering/lenis) |
| Shader presets | `@paper-design/shaders` 0.0.81 | Apache-2.0 (npm field) | Pre-1.0. Not observed on winners. | [npm](https://www.npmjs.com/package/@paper-design/shaders) |

---

## 3. Decision tree: how much 3D, and which stack

Answer the questions in order and stop at the first "yes".

```
Q0  Does the 3D carry the subject (the product, the place, the data, the brand's own object)?
    no  -> NO 3D. Spend the effort on typography, photography, a crafted SVG scene.
           (Abstract floating spheres / blobs / "3D shapes" are the law's crude-illustration tell.)
Q1  Is the only interaction scroll or time (no free camera, no pointer-driven geometry, no user choice)?
    yes -> PRE-RENDERED: Blender/C4D render -> video or image sequence.
           Looping ambience: <video muted playsinline loop> with a poster.
           Scroll-scrubbed: image sequence drawn to <canvas> (WebP/AVIF frames), or video encoded
           with a short GOP / all-intra so seeking is instant. Lama Lama (SOTM) class.
Q2  Is it one hero object or scene, designer-owned, on Webflow/Framer, with simple states
    (hover, click, scroll between 2-4 states) and no custom shader?
    yes -> SPLINE (<spline-viewer> for page-scroll/mouse events), Hobby+ to remove the watermark.
           Know that the scene is hosted by Spline unless you are on Enterprise.
           For 2D shader/image effects only (gradients, distortion, dither on images): UNICORN STUDIO
           (Legend for any commercial site).
Q3  Custom art direction: authored camera choreography, custom shaders, strict performance budget,
    anything you'd submit for SOTD/SOTM?
    yes -> THREE.JS (vanilla). Default for award work (section 1).
           Use R3F instead when the site is already React/Next AND the 3D has many components or
           UI-coupled state (configurators, lists of 3D cards, route-driven scenes).
Q4  Only a fullscreen 2D shader (gradient field, image transitions, dither) and no scene graph?
    yes -> one three.js ShaderMaterial on a fullscreen quad (you probably ship three anyway),
           or raw WebGL2 / OGL if three isn't on the page. OGL is dormant (last commit 2025-04).
Q5  Is there a real captured place or object whose photoreal view-dependent detail is the point?
    yes -> GAUSSIAN SPLATS with Spark 2.x in three.js (SPZ/SOG in, LoD .RAD for large scenes).
           Only with a real capture and a phone budget of 1-3M splats (section 4.9).
Q6  Is the motion 2D vector: UI, character, logo state machine?
    yes -> RIVE (@rive-app/webgl2). Not 3D. Winners pair it with three (section 1).
Q7  Is the source a Unity/Blender project with components, physics, WebXR/AR?
    yes -> NEEDLE ENGINE (Pro license for commercial; pin @stable).
```

**WebGL or WebGPU renderer?**

- **Default: `WebGLRenderer` + GLSL.** Choose it when you depend on:
  - three-addons `EffectComposer` or pmndrs `postprocessing`
  - drei shader materials
  - `onBeforeCompile` patches
  - Spark splats
  - the widest reach (WebGL2 is at 96.44%)
- **`WebGPURenderer` + TSL.** Choose it when you need:
  - GPU compute (100k+ simulated particles)
  - one shader codebase for both backends
  - the new node post stack (TRAA, SSGI, SSR)

  Accept the "experimental" label and test the WebGL2 fallback path on every build. Bruno Simon's SOTM does exactly this on r183.

**Budget sanity check before committing** (house rule): if the 3D asset plus runtime would exceed about 1.5 MB compressed before first interaction on mobile, go down one rung of the tree, or ship a poster frame and load the 3D on intent (scroll into view, click).

---

## 4. The 3D roles seen on winners, with a build recipe each

Every recipe starts from the same progressive-enhancement bootstrap in section 6.4: a poster image is visible by default, and the canvas replaces it only after its first frame has rendered.

**Verification.** The GLSL, TSL and trail snippets below compiled and rendered without errors on three **r186** in a Chromium preview (TSL ran on the WebGL2 fallback, because WebGPU was not available there). The pmndrs dither effect ran on postprocessing **6.39.5**. The AnimationMixer scrub behaviour was checked in the same session. R3F/JSX snippets and the bootstrap were checked against the docs but not executed.

### 4.1 Hero object with a scroll-driven camera

**Observed on:** Oryzo (SOTM, "a cinematic product story that turns an ordinary cork coaster into an immersive digital experience", [Awwwards](https://www.awwwards.com/sites/oryzo-ai)), Seasats and USAvionix (R3F product heroes), Cerebrium.

**Recipe.**
1. **Author the camera move in Blender or C4D, not in code.** Keyframe a camera, export it with the GLB, then scrub the clip with scroll progress. The art director gets the exact framing, easing is baked in, and code stays small.
2. Put 3–5 **held beats** in the clip (flat keyframe segments), each aligned to a DOM section of copy. Text lives in the DOM, never baked into the canvas.
3. Damp scroll progress (critically damped, frame-rate independent). Never map raw wheel deltas to the camera.
4. **Do not use `LoopOnce` + `clampWhenFinished`.** When scrubbing reaches the end, the action is paused permanently and scrubbing back freezes. I verified this on r186: after progress 1.0, `setTime(0.5)` returns the start pose with `paused: true`. Keep the default loop and clamp progress below 1.

```js
// scroll-camera.js: three r186 + GSAP 3.15 + Lenis 1.3
import * as THREE from 'three';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import Lenis from 'lenis';
gsap.registerPlugin(ScrollTrigger);

export function attachScrollCamera({ gltf, scene, renderer, section, reducedMotion }) {
  const camera = gltf.cameras[0];                          // the Blender camera
  const clip = gltf.animations.find((c) => c.name === 'ShotCamAction');
  const mixer = new THREE.AnimationMixer(gltf.scene);
  mixer.clipAction(clip).play();                           // default LoopRepeat; we clamp progress instead
  const setAspect = () => { camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix(); };
  setAspect(); addEventListener('resize', setAspect);

  let target = 0, current = 0;
  const lenis = new Lenis();                               // wraps native scroll; sticky/anchors keep working
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((t) => lenis.raf(t * 1000));
  gsap.ticker.lagSmoothing(0);
  ScrollTrigger.create({ trigger: section, start: 'top top', end: 'bottom bottom',
    onUpdate: (self) => { target = self.progress; } });

  const timer = new THREE.Timer(); timer.connect(document);
  return function frame(ts) {                              // call from renderer.setAnimationLoop
    timer.update(ts);
    const dt = Math.min(timer.getDelta(), 1 / 30);
    current = reducedMotion ? target : current + (target - current) * (1 - Math.exp(-dt * 6));
    mixer.setTime(Math.min(current, 0.9999) * clip.duration);
    renderer.render(scene, camera);
  };
}
```

**Reduced motion.** Don't scrub. Snap `current` to the nearest held beat per section (a cut, not a fly-through), or render a single still.

**Taste.** Use a long lens (18–35° vertical FOV, i.e. 50–85 mm equivalent) for products; wide lenses distort the product and read as a game engine. One continuous move beats five orbit-arounds. Never auto-rotate the product in a loop while copy sits on screen; that is the law's "decorative motion with no purpose".

### 4.2 Environment world

**Observed on:** Bruno Simon (SOTM, a drivable world), illoca (Theatre.js camera timelines), L.I.S.A. and Why Zero (Blender-authored scenes).

**Recipe.**
- **Bake the lighting.** In Blender Cycles, bake Combined (or Diffuse + AO) into one to three atlases on a second UV. Render with `MeshBasicMaterial` + `map` (or `lightMap` on UV2 if some materials must stay PBR). Baked GI is the single biggest "expensive" lever, and it's the cheapest to render.
- Join static meshes per atlas: `gltf-transform join` / `flatten`, keeping named nodes you animate (section 7). Target **under 100 draw calls on mobile and under 300 on desktop** (house rule). R3F's docs call **1000 "the very maximum, optimally a few hundred or less"** ([R3F perf](https://r3f.docs.pmnd.rs/advanced/scaling-performance)).
- `scene.fog` color = `scene.background` = page `body` background at the canvas edge, so the world dissolves into the page instead of ending at a hard frame.
- For the camera, use rails: a `CatmullRomCurve3` sampled by scroll, or a Theatre.js sheet. Free-fly controls on a marketing site make people lose the story.
- For compressing lightmaps, use UASTC. ETC1S blocks up on smooth gradients (the `optimize` KTX2 path already sends occlusion/normal/metalRough slots to UASTC; see section 7).

### 4.3 Product configurator

**Observed on:** none in this sample. Winners here are storytelling sites. Build one only when the business needs it.

**Recipe (R3F).**
- Store variants in the file (`KHR_materials_variants`) or swap materials by name.
- Keep the canvas `frameloop="demand"` and call `invalidate()` on change.
- Light with IBL plus contact or accumulated shadows.
- Mirror state to the URL so a configuration can be shared.

```jsx
// Configurator.jsx: R3F 9 + drei 10 (checked against docs, not executed)
import { Canvas, useThree } from '@react-three/fiber';
import { useGLTF, Environment, ContactShadows, Bounds } from '@react-three/drei';
import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';

const ktx2 = new KTX2Loader().setTranscoderPath('/vendor/basis/');
useGLTF.setDecoderPath('/vendor/draco/');                 // self-host: default is gstatic 1.5.5

function Product({ finish }) {
  const gl = useThree((s) => s.gl);
  const { scene, materials } = useGLTF('/models/chair.glb', true, true,
    (loader) => loader.setKTX2Loader(ktx2.detectSupport(gl)));
  scene.traverse((o) => { if (o.isMesh && o.name === 'Shell') o.material = materials[finish]; });
  return <primitive object={scene} />;
}

export default function Configurator({ finish }) {
  return (
    <Canvas frameloop="demand" dpr={[1, 2]} camera={{ fov: 28, position: [0, 0.6, 4] }}
            gl={{ antialias: true, powerPreference: 'high-performance' }}>
      <Bounds fit clip observe margin={1.1}><Product finish={finish} /></Bounds>
      <Environment files="/env/studio_1k.hdr" environmentIntensity={0.9} />
      <ContactShadows position={[0, -0.001, 0]} opacity={0.55} blur={2.2} far={1.2} resolution={512} frames={1} />
    </Canvas>
  );
}
```

With `frameloop="demand"`, controls or tweens that mutate three objects must call `invalidate()` ([R3F perf](https://r3f.docs.pmnd.rs/advanced/scaling-performance)). `frames={1}` bakes the contact shadow once.

### 4.4 Image-plane shader effects (DOM-synced planes)

**Observed on:** Gil Huybrecht (SOTD, WebGL gallery with infinite scroll, three r185 + instancing), Peryton Film and Pensatori (WebGL + photography).

**Recipe.**
- **One canvas for all images.** Chromium keeps at most **16** active WebGL contexts (8 observed on Android) and silently drops the oldest ([SO](https://stackoverflow.com/questions/76380203/canvases-content-is-lost-when-the-context-is-lost), [pyvista #5207](https://github.com/pyvista/pyvista/issues/5207)). A canvas per image breaks at image 17.
- A fixed full-viewport canvas with an orthographic camera in CSS pixels. Each `<img>` stays in the DOM, in layout and in the accessibility tree; its plane is sized to `getBoundingClientRect()` inside the rAF loop.
- Hide the DOM `<img>` (opacity 0) **only after its plane has rendered**. If WebGL fails, the image is still there. This is the law's "content visible by default" rule applied to images.
- Crafted hover: a **local lens that is zero at the pointer**, damped on the CPU. The first version of this shader used `normalize(d) * falloff`, which tears at the pointer. The version below doesn't.
- Deslop: no RGB-split glitch on every hover, no full-frame wobble, no "liquid" ripple on product photos. One restrained lens or a scroll-velocity bend, applied the same way to every image.

**GLSL (`WebGLRenderer`)**, verified on r186:

```js
const imageMat = new THREE.ShaderMaterial({
  toneMapped: false,                                    // photos are display-referred: never tone-map them
  uniforms: {
    uMap: { value: texture },                           // texture.colorSpace = THREE.SRGBColorSpace
    uPointer: { value: new THREE.Vector2(0.5, 0.5) },   // pointer in plane UV
    uHover: { value: 0 },                               // damped 0..1
    uCover: { value: new THREE.Vector2(1, 1) },         // object-fit: cover (below)
  },
  vertexShader: /* glsl */`
    varying vec2 vUv;
    void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
  fragmentShader: /* glsl */`
    uniform sampler2D uMap; uniform vec2 uPointer, uCover; uniform float uHover;
    varying vec2 vUv;
    void main() {
      vec2 uv = (vUv - 0.5) * uCover + 0.5;
      vec2 d = vUv - uPointer;
      float fall = 1.0 - smoothstep(0.0, 0.35, length(d));   // edge0 < edge1: reversed edges are undefined in GLSL
      uv -= d * fall * 0.22 * uHover;                          // zero at the pointer: no pinch or tear
      gl_FragColor = vec4(texture2D(uMap, uv).rgb, 1.0);
      #include <colorspace_fragment>
    }`,
});

// object-fit: cover in UV space
function setCover(mat, planeW, planeH, imgW, imgH) {
  const pa = planeW / planeH, ia = imgW / imgH;
  mat.uniforms.uCover.value.set(pa > ia ? 1 : pa / ia, pa > ia ? ia / pa : 1);
}
// per frame: frame-rate independent damping
u.uHover.value += (hoverTarget - u.uHover.value) * (1 - Math.exp(-dt * 8));
```

**TSL (`WebGPURenderer`, WebGL2 fallback)**, verified on r186:

```js
import * as THREE from 'three/webgpu';
import { Fn, uniform, texture, uv, float, smoothstep } from 'three/tsl';

const uPointer = uniform(new THREE.Vector2(0.5, 0.5));
const uHover = uniform(0);
const uCover = uniform(new THREE.Vector2(1, 1));
const imageMat = new THREE.MeshBasicNodeMaterial({ toneMapped: false });
imageMat.colorNode = Fn(() => {
  const d = uv().sub(uPointer);
  const fall = float(1).sub(smoothstep(0.0, 0.35, d.length()));
  const st = uv().sub(0.5).mul(uCover).add(0.5).sub(d.mul(fall).mul(0.22).mul(uHover));
  return texture(map, st);
})();
// update: uHover.value = ...; uPointer.value.set(x, y);
```

Syncing planes to the DOM (orthographic camera in CSS pixels, origin at the viewport centre):

```js
const cam = new THREE.OrthographicCamera(-innerWidth / 2, innerWidth / 2, innerHeight / 2, -innerHeight / 2, -1000, 1000);
function syncPlane(mesh, el) {                        // call inside the rAF loop, not in a scroll handler
  const r = el.getBoundingClientRect();
  mesh.scale.set(r.width, r.height, 1);               // PlaneGeometry(1, 1)
  mesh.position.set(r.left + r.width / 2 - innerWidth / 2, -(r.top + r.height / 2) + innerHeight / 2, 0);
  mesh.visible = r.bottom > -100 && r.top < innerHeight + 100;   // cull offscreen planes
}
```

### 4.5 Particle and typography fields

**Observed on:** the WebGL listing is full of these (Austensor, Vizz, G. Colombel). I did not probe their internals.

**Recipe.**
- Rasterize the word into an offscreen 2D canvas and sample the filled pixels into a target-position buffer. Render with `THREE.Points` + `ShaderMaterial`, where each point eases from noise-driven drift to its target by a `uProgress` uniform.
- Up to about 100k points: attributes plus vertex-shader math. Beyond that: GPU simulation (`GPUComputationRenderer` in WebGL, TSL `compute()` + storage buffers in WebGPU).
- **The real heading stays in the DOM** (visually hidden when the particle version is live) so screen readers and search see text. Never render the only copy of a headline to canvas.
- Deslop: no twinkling starfield behind everything and no neon additive-blended bloom. Use one ink colour from the palette, `NormalBlending` or subtle additive on a dark ground only, and point size attenuated by depth.

```js
function sampleText(text, { font = '600 220px Inter Tight', step = 4, w = 1400, h = 320 } = {}) {
  const c = new OffscreenCanvas(w, h), g = c.getContext('2d');
  g.font = font; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(text, w / 2, h / 2);
  const { data } = g.getImageData(0, 0, w, h), pts = [];
  for (let y = 0; y < h; y += step) for (let x = 0; x < w; x += step)
    if (data[(y * w + x) * 4 + 3] > 128) pts.push((x - w / 2) / h, -(y - h / 2) / h, 0);
  return new Float32Array(pts);                       // -> geometry attribute 'aTarget'
}
```

`OffscreenCanvas` is at 95.52% support, Safari 17+ ([caniuse](https://caniuse.com/offscreencanvas)). Fall back to `document.createElement('canvas')`.

### 4.6 Globe

**Observed on:** none in this sample.

**Recipe.**
- For a dotted brand globe, use **cobe 2.0.1** (about 5 KB, MIT). v2 exposes markers and arcs that DOM elements can bind to with CSS anchor positioning, which keeps labels as real text ([cobe](https://github.com/shuding/cobe)).
- For data globes (many arcs, hex bins), use `three-globe` 2.45.2 inside your three scene.
- Deslop: no atmosphere glow halo. The law bans "radial glow halo behind an object". Light the sphere with one directional key and a rim term tinted toward the page background. Keep `mapBrightness` and `glowColor` restrained, and stop the idle spin when the globe is offscreen or reduced motion is on.

### 4.7 Fluid and cursor simulations

**Observed on:** Lando Norris (SOTM), Ponpon Mania (SOTM) and Léo Parpeix (SOTD). All three ship `divergence` + noise shader strings, the signature of a stable-fluids pressure solve.

**Recipe.**
- A real fluid (Navier–Stokes: advect → divergence → pressure Jacobi → gradient subtract) at **1/4–1/8 resolution** with half-float targets. [PavelDoGreat/WebGL-Fluid-Simulation](https://github.com/PavelDoGreat/WebGL-Fluid-Simulation) (MIT) is the usual base.
- For most sites a **velocity trail is enough**: one ping-pong buffer that stamps pointer velocity and decays. It is cheaper, stable, and it drives distortion of an image or the whole page backdrop.

Verified on r186:

```js
const SIM_SCALE = 0.25;                                   // 1/4 res is invisible after bilinear upsampling
const sim = new THREE.Vector2(); renderer.getDrawingBufferSize(sim).multiplyScalar(SIM_SCALE).floor();
const opts = { type: THREE.HalfFloatType, depthBuffer: false, minFilter: THREE.LinearFilter, magFilter: THREE.LinearFilter };
let read = new THREE.WebGLRenderTarget(sim.x, sim.y, opts), write = read.clone();
const trailMat = new THREE.ShaderMaterial({
  uniforms: { uPrev: { value: null }, uPointer: { value: new THREE.Vector2(-1, -1) }, uVel: { value: new THREE.Vector2() },
              uAspect: { value: sim.x / sim.y }, uDecay: { value: 0.955 }, uRadius: { value: 0.06 } },
  vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }`,
  fragmentShader: /* glsl */`
    uniform sampler2D uPrev; uniform vec2 uPointer, uVel; uniform float uAspect, uDecay, uRadius;
    varying vec2 vUv;
    void main() {
      vec4 prev = texture2D(uPrev, vUv - uVel * 0.02) * uDecay;   // advect along motion, then fade
      vec2 d = (vUv - uPointer) * vec2(uAspect, 1.0);
      float splat = exp(-dot(d, d) / (uRadius * uRadius));        // gaussian stamp
      gl_FragColor = vec4(prev.rg + uVel * splat, prev.b + splat * length(uVel), 1.0); // rg = velocity, b = intensity
    }`,
});
// each frame: trailMat.uniforms.uPrev.value = read.texture; render a 2x2 quad into `write`;
// swap [read, write]; sample read.texture in the display shader: uv - vel * 0.03
// clamp pointer velocity (e.g. vel.clampLength(0, 0.05)) and scale by dt: raw per-frame deltas differ at 60 vs 120 Hz
```

**Taste.** Displacement of 0.02–0.04 UV at most. My test at 0.08 produced visible swirls, which reads as a toy. Decay 0.94–0.97. Tint any visible "ink" with one palette colour, never a rainbow. Turn the effect off for reduced motion and on touch devices without hover.

### 4.8 Dithering and halftone post

**Observed on:** Unbelievably Crap, whose bundle configures a "halftone echo layer" (a dot-screened clone of its sphere). I found no Bayer shader in the 25 probed bundles, so this is a style option, not a winner staple.

**Recipe.**
- Pixelate to a cell grid, take luminance **in display space** (after tone mapping and sRGB), remap it with a contrast curve, then threshold against an 8×8 Bayer matrix. Use two palette colours: ink and paper.
- Two fixes found while testing: remap luminance, or dark areas become a speckled void; offset the threshold by half a level, or pure black still gets one lit pixel per 8×8 block.
- Deslop: apply it to the **canvas layer only** (DOM text stays crisp above it). The law bans grain and noise over text. Paper colour is not cream or beige; choose one from the brand palette.

**(a) three addons `ShaderPass` after `OutputPass`** (display space), verified on r186:

```js
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const raw = (hex) => new THREE.Color().setHex(hex, THREE.LinearSRGBColorSpace); // no sRGB->linear: this pass is in display space
const DitherShader = {
  uniforms: { tDiffuse: { value: null }, uResolution: { value: new THREE.Vector2() }, uPixel: { value: 3 },
              uInk: { value: raw(0x121416) }, uPaper: { value: raw(0xb9bec4) } },
  vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
  fragmentShader: /* glsl */`
    uniform sampler2D tDiffuse; uniform vec2 uResolution; uniform float uPixel; uniform vec3 uInk, uPaper;
    varying vec2 vUv;
    float bayer2(vec2 a) { a = floor(a); return fract(a.x * 0.5 + a.y * a.y * 0.75); }
    float bayer4(vec2 a) { return bayer2(0.5 * a) * 0.25 + bayer2(a); }
    float bayer8(vec2 a) { return bayer4(0.5 * a) * 0.25 + bayer2(a); }
    void main() {
      vec2 cell = floor(vUv * uResolution / uPixel);
      vec3 c = texture2D(tDiffuse, (cell + 0.5) * uPixel / uResolution).rgb;   // pixelate first
      float l = smoothstep(0.12, 0.92, dot(c, vec3(0.2126, 0.7152, 0.0722))); // solid ink darks, clean paper highlights
      gl_FragColor = vec4(mix(uInk, uPaper, step(bayer8(cell) + 0.5 / 64.0, l)), 1.0);
    }`,
};
const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
composer.addPass(new OutputPass());                         // tone mapping + sRGB happen here
const dither = new ShaderPass(DitherShader);
composer.addPass(dither);
renderer.getDrawingBufferSize(dither.uniforms.uResolution.value);   // redo on resize
```

**(b) pmndrs `postprocessing` custom `Effect`**, verified on 6.39.5. The effect uses the built-in `resolution` uniform ([wiki](https://github.com/pmndrs/postprocessing/wiki/Custom-Effects)). Its input is linear, so convert before thresholding:

```js
import { EffectComposer, RenderPass, EffectPass, Effect, BlendFunction } from 'postprocessing';
const frag = /* glsl */`
  uniform float uPixel; uniform vec3 uInk; uniform vec3 uPaper;
  float bayer2(vec2 a) { a = floor(a); return fract(a.x * 0.5 + a.y * a.y * 0.75); }
  float bayer4(vec2 a) { return bayer2(0.5 * a) * 0.25 + bayer2(a); }
  float bayer8(vec2 a) { return bayer4(0.5 * a) * 0.25 + bayer2(a); }
  void mainUv(inout vec2 uv) { vec2 g = resolution / uPixel; uv = (floor(uv * g) + 0.5) / g; }
  void mainImage(const in vec4 inputColor, const in vec2 uv, out vec4 outputColor) {
    vec3 srgb = pow(max(inputColor.rgb, 0.0), vec3(1.0 / 2.2));        // approx. display space
    float l = smoothstep(0.12, 0.92, dot(srgb, vec3(0.2126, 0.7152, 0.0722)));
    outputColor = vec4(mix(uInk, uPaper, step(bayer8(floor(uv * resolution / uPixel)) + 0.5 / 64.0, l)), inputColor.a);
  }`;
class DitherEffect extends Effect {
  constructor({ pixel = 3, ink = '#121416', paper = '#b9bec4' } = {}) {
    super('DitherEffect', frag, { blendFunction: BlendFunction.NORMAL, uniforms: new Map([
      ['uPixel', new THREE.Uniform(pixel)],
      ['uInk', new THREE.Uniform(new THREE.Color(ink))],     // linear here; EffectPass encodes sRGB on output
      ['uPaper', new THREE.Uniform(new THREE.Color(paper))],
    ]) });
  }
}
const composer = new EffectComposer(renderer, { frameBufferType: THREE.HalfFloatType });
composer.addPass(new RenderPass(scene, camera));
composer.addPass(new EffectPass(camera, new DitherEffect()));
```

**(c) TSL on `RenderPipeline`**, verified on r186 via the WebGL2 fallback:

```js
import * as THREE from 'three/webgpu';
import { Fn, uniform, pass, renderOutput, screenUV, screenSize, floor, fract, step, mix, luminance, smoothstep, vec3 } from 'three/tsl';

const raw = (hex) => { const c = new THREE.Color().setHex(hex, THREE.LinearSRGBColorSpace); return vec3(c.r, c.g, c.b); };
const bayer2 = Fn(([a]) => { const f = floor(a); return fract(f.x.mul(0.5).add(f.y.mul(f.y).mul(0.75))); });
const bayer4 = Fn(([a]) => bayer2(a.mul(0.5)).mul(0.25).add(bayer2(a)));
const bayer8 = Fn(([a]) => bayer4(a.mul(0.5)).mul(0.25).add(bayer2(a)));
const cellPx = uniform(3);

const pipeline = new THREE.RenderPipeline(renderer);
pipeline.outputColorTransform = false;                      // we tone-map + encode ourselves, then dither
const sceneTex = pass(scene, camera).getTextureNode('output');
pipeline.outputNode = Fn(() => {
  const grid = screenSize.div(cellPx);
  const cell = floor(screenUV.mul(grid));
  const col = renderOutput(sceneTex.sample(cell.add(0.5).div(grid)));   // display-space colour per cell
  const l = smoothstep(0.12, 0.92, luminance(col.rgb));
  return mix(raw(0x121416), raw(0xb9bec4), step(bayer8(cell).add(0.5 / 64), l));
})();
renderer.setAnimationLoop(() => pipeline.render());
```

### 4.9 Noise-displaced surfaces

Use these only when the surface *is* the subject: cloth, liquid, a material sample. A free-floating iridescent blob as the hero is the law's "abstract floating spheres" tell.

**Recipe.**
- Displace along the normal, then **rebuild the normals** from two displaced neighbours. Without that step the object is lit as if undisplaced, which reads as cheap.
- Amplitude 0.05–0.15 × radius; speed slow (0.1–0.2).
- Light with one directional key and an environment map.

**GLSL vertex core**, verified on r186. `vnoise` is a hash-based value noise; swap in simplex if you prefer.

```glsl
uniform float uTime, uAmp, uFreq, uSpeed;
varying vec3 vN;
float hash(vec3 p) { p = fract(p * 0.3183099 + 0.1); p *= 17.0; return fract(p.x * p.y * p.z * (p.x + p.y + p.z)); }
float vnoise(vec3 x) {
  vec3 i = floor(x), f = fract(x); f = f * f * (3.0 - 2.0 * f);
  return mix(mix(mix(hash(i), hash(i + vec3(1,0,0)), f.x), mix(hash(i + vec3(0,1,0)), hash(i + vec3(1,1,0)), f.x), f.y),
             mix(mix(hash(i + vec3(0,0,1)), hash(i + vec3(1,0,1)), f.x), mix(hash(i + vec3(0,1,1)), hash(i + vec3(1,1,1)), f.x), f.y), f.z);
}
vec3 displace(vec3 p, vec3 n) { return p + n * (vnoise(p * uFreq + uTime * uSpeed) - 0.5) * uAmp; }
void main() {
  vec3 t = normalize(cross(normal, abs(normal.y) < 0.99 ? vec3(0,1,0) : vec3(1,0,0)));
  vec3 b = cross(normal, t);
  vec3 p0 = displace(position, normal);
  vec3 p1 = displace(position + t * 0.01, normal);
  vec3 p2 = displace(position + b * 0.01, normal);
  vN = normalize(normalMatrix * normalize(cross(p1 - p0, p2 - p0)));
  gl_Position = projectionMatrix * modelViewMatrix * vec4(p0, 1.0);
}
```

**TSL**, verified on r186. This drives a lit `MeshStandardNodeMaterial`:

```js
import { Fn, uniform, time, positionLocal, normalLocal, mx_noise_float, cross, normalize, abs, select, vec3, transformNormalToView } from 'three/tsl';
const uAmp = uniform(0.12), uFreq = uniform(1.4), uSpeed = uniform(0.15);
const displace = Fn(([p, n]) => p.add(n.mul(mx_noise_float(p.mul(uFreq).add(time.mul(uSpeed))).mul(uAmp))));
const mat = new THREE.MeshStandardNodeMaterial({ color: 0xd8d4cc, roughness: 0.45 });
mat.positionNode = displace(positionLocal, normalLocal);
mat.normalNode = Fn(() => {
  const n = normalLocal;
  const t = normalize(cross(n, select(abs(n.y).lessThan(0.99), vec3(0, 1, 0), vec3(1, 0, 0))));
  const b = cross(n, t);
  const p0 = displace(positionLocal, n), p1 = displace(positionLocal.add(t.mul(0.01)), n), p2 = displace(positionLocal.add(b.mul(0.01)), n);
  return transformNormalToView(normalize(cross(p1.sub(p0), p2.sub(p0))));
})();
```

`mx_noise_float` returns roughly −1..1, so amplitude means ± `uAmp`. At 0.35 my test object turned lumpy; about 0.12 reads as organic.

### 4.10 Gaussian splats (captured reality)

**Maturity (2026-09).**
- **Spark 2.x** is the production choice inside three.js ([Spark](https://sparkjs.dev/)).
- PlayCanvas + SuperSplat is the production choice if you don't need three.
- three's own `GaussianSplat` shipped on 2026-09-24, so wait a release or two.
- The format standard exists: `KHR_gaussian_splatting` is ratified.

**Budgets** from Spark's performance docs ([source](https://sparkjs.dev/docs/performance/)):

| Device | Splat budget |
|---|---|
| Quest 3 | ≤ 1M |
| Android | 1–2M |
| iPhone | 1–3M |
| Desktop | 1–5M (10–20M+ on some) |

Other tuning from the same docs:
- Construct `WebGLRenderer` with `antialias: false`, because MSAA adds overhead and splats don't benefit.
- Consider a DPR below `devicePixelRatio` for splat-only scenes.
- For VR, `SparkRenderer.maxStdDev = Math.sqrt(5)`.

Pipeline:
1. Capture (phone or drone photogrammetry) and train.
2. Clean floaters in SuperSplat.
3. Export SPZ or SOG, or pre-build LoD: `npm run build-lod -- scene.ply --quality` produces `scene-lod.rad`.
4. Stream it with `new SplatMesh({ url: './scene-lod.rad', paged: true })` ([LoD guide](https://sparkjs.dev/docs/lod-getting-started/)).

```js
import { SparkRenderer, SplatMesh } from '@sparkjsdev/spark';     // 2.2.0, peer three >= 0.180
const renderer = new THREE.WebGLRenderer({ antialias: false });
scene.add(new SparkRenderer({ renderer }));
const splat = new SplatMesh({ url: '/splats/atelier-lod.rad', paged: true });
scene.add(splat);
```

**Taste.** Frame the capture tightly: splat edges and floaters are the cheap tell. Use a fixed camera path with small parallax rather than free orbit (the back side is usually unscanned), and hide the reveal behind a poster frame rendered from the same viewpoint.

---

## 5. Taste rules: what makes 3D read expensive or cheap

**Lighting**
- **Image-based light plus one key.** Use an HDRI environment for reflections and fill (a 1k–2k Poly Haven CC0 HDRI, or `PMREMGenerator.fromScene(new RoomEnvironment(), 0.04)` for a neutral studio), plus **one** directional key that gives shape and casts the shadow. Colored three-point rigs and rim lights in accent colors read as template. The law also bans "radial glow halo behind an object": light with a directional source that has falloff.
- **Ground contact is mandatory.** Use baked AO, a contact shadow, or an accumulated shadow. An object with no contact shadow looks pasted on. r186 removed `PCFSoftShadowMap`; use `PCFShadowMap`/`VSMShadowMap`, or better, bake it.
- **Bake whatever doesn't move.** Baked GI with `MeshBasicMaterial` beats real-time lights on both quality and frame time.

**Tone mapping and color**
- **Never leave a lit scene on `NoToneMapping`**; highlights clip.
- Use **`NeutralToneMapping`** (three: "based on the Khronos 3D Commerce Group standard tone mapping", [constants.js](https://github.com/mrdoob/three.js/blob/r186/src/constants.js)) when product or brand colours must match their sRGB values. Noho ships it.
- Use **`AgXToneMapping`** for scenes with hot highlights.
- `ACESFilmic` shifts and saturates hues. Gionatannese uses it with exposure 1.1, which fits a moody scene but not a product.
- Photos and UI textures on planes use `toneMapped: false`.
- Background colour = fog colour = clear colour = the page background at the canvas edge. Law palette rules apply to 3D too: no saturated accent rims, no blue-purple ramps, no cream "studio" backdrop.

**Materials**
- Roughness should vary via a map (smudges, micro-variation). Uniform `roughness: 0` chrome with no environment renders black or mirror-flat.
- Use `clearcoat` for paint and lacquer and `sheen` for fabric.
- Use transmission sparingly: every transmissive material adds a render pass.
- Metal needs an environment map; without one it's black.

**Camera and motion**
- Long lens for products (18–35° FOV). Use damped, frame-rate-independent easing (`1 - exp(-dt*k)`), never linear lerp per frame.
- No idle auto-rotate while copy is on screen. No bobbing "floating" objects: the law's floating-cards tell also applies to 3D.

**Post-processing** (the pass stack is the place people overdo it)
- Bloom only on emissive HDR values above 1 (threshold ≥ 1), never whole-frame glow.
- Chromatic aberration at 1 px or less, edges only, or not at all.
- Vignette subtle.
- Grain belongs on the canvas substrate; DOM text stays crisp above it (law: "grain sitting on top of the content").
- Antialias: with post, use SMAA/FXAA, or TRAA/SMAA nodes in WebGPU. Without post, use MSAA (`antialias: true`).

**Composition** (law's signature-artifact rule)
- The 3D object is the one signature artifact on the first screen and should cross layers (overlap copy edges or bleed off the fold). One 3D moment per page section, not a canvas in every section.

---

## 6. Performance budgets, fallbacks, reduced motion

### 6.1 Budgets

| Budget | Mobile | Desktop | Basis |
|---|---|---|---|
| Device pixel ratio | `min(dpr, 1.5)` for fragment-heavy post or fullscreen shaders; `min(dpr, 2)` otherwise | `min(dpr, 2)` | observed on 4 winners (section 1); R3F `dpr={[1, 2]}` |
| Draw calls | < 100 | < 300 (hard ceiling 1000) | house rule; R3F docs: max 1000, optimal "a few hundred or less" |
| Triangles, hero object | ≤ 100k | ≤ 300k | house rule; simplify further for background objects |
| Texture memory (GPU) | ≤ 64–100 MB total | ≤ 200 MB | house rule (unverified device limits); see the arithmetic below |
| 3D payload before first interaction | ≤ 1.5 MB compressed (runtime + scene) | ≤ 3 MB | house rule |
| Lights with real-time shadows | 0–1 | 1 | house rule; Spline recommends fewer than 3 lights ([Spline](https://docs.spline.design/exporting-your-scene/how-to-optimize-your-scene)) |
| Gaussian splats | 1–3M (iPhone), 1–2M (Android) | 1–5M | [Spark](https://sparkjs.dev/docs/performance/) |
| Frame time | 16.6 ms at 60 Hz; degrade before dropping below 30 fps | same | R3F `PerformanceMonitor` pattern |

**Texture memory arithmetic.** PNG, JPEG and WebP decode to **uncompressed** RGBA in GPU memory; KTX2/Basis stays GPU-compressed ([glTF Transform CLI help](https://github.com/donmccurdy/glTF-Transform/blob/main/packages/cli/src/cli.ts)). A full mip chain adds about 33%.

| Texture | RGBA8 (PNG/JPEG/WebP) | KTX2 → BC7/ASTC 4×4 (8 bpp) | KTX2 ETC1S → BC1/ETC (4 bpp) |
|---|---|---|---|
| 1024² + mips | 5.6 MB | 1.4 MB | 0.7 MB |
| 2048² + mips | **22.4 MB** | 5.6 MB | 2.8 MB |
| 4096² + mips | **89.5 MB** | 22.4 MB | 11.2 MB |

So one uncompressed 4k texture can use the whole mobile budget. Cap textures at **2048** (the gltf-transform default) and use 4k only for a single hero atlas on desktop.

### 6.2 Render-loop rules

- **Render on demand when nothing moves.** R3F: `frameloop="demand"` + `invalidate()` (observed on USAvionix). Vanilla: `renderer.setAnimationLoop(null)` when idle, then render once on change.
- **Pause offscreen and when the tab is hidden.** Use an `IntersectionObserver` on the canvas section plus `visibilitychange`. `THREE.Timer.connect(document)` keeps the delta from spiking after a tab switch.
- **Instance repeats**: `InstancedMesh`, `gltf-transform instance`, or `EXT_mesh_gpu_instancing`. **Merge statics**: `gltf-transform join`/`flatten`.
- **Compile before reveal**: `await renderer.compileAsync(scene, camera)` exists on `WebGLRenderer` r186 ([source](https://github.com/mrdoob/three.js/blob/r186/src/renderers/WebGLRenderer.js)). This removes the first-interaction shader-compile hitch.
- **Adapt quality**:
  - drei `<PerformanceMonitor onDecline={() => setDpr(1)} onIncline={() => setDpr(2)} />` ([R3F perf](https://r3f.docs.pmnd.rs/advanced/scaling-performance)).
  - Vanilla: measure the average frame time over 2 s windows and step DPR down by 0.25, then drop post, then fall back to the poster.
- **GPU tiers** (`@pmndrs/detect-gpu`): tier 0 gets the poster only; tier 1 gets DPR 1, no post, fewer particles; tiers 2–3 get the full experience. Self-host the benchmark JSON, and remember the data has been frozen since Dec 2025, so it won't recognise GPUs released after that.
- **One WebGL context per page** (section 4.4).
- **Lazy-init after LCP.** The LCP element must be the DOM poster or headline, never the canvas. Import three only after `load` plus idle time. `requestIdleCallback` is **not in Safari or iOS** (caniuse: Safari TP only, [caniuse](https://caniuse.com/requestidlecallback)), so fall back to `setTimeout`.

### 6.3 Mobile, reduced motion and no-WebGL

- **Reduced motion** (`prefers-reduced-motion: reduce`, 96.45% support):
  - render one still frame, or cut between held beats
  - no scroll-scrubbed camera, no hover distortion, no cursor fluid, no idle rotation
  - listen for `change` so the setting applies live
- **No WebGL, a software renderer, or `saveData`.** Probe with `getContext('webgl2', { failIfMajorPerformanceCaveat: true })` ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/getContext)) and release the probe context with `WEBGL_lose_context`. On failure the poster stays and nothing else changes.
- **Touch**: no hover state exists, so cursor effects become scroll-driven or are removed. Don't hijack touch scrolling over the canvas: use `touch-action: pan-y` on the canvas unless the canvas has a real gesture.
- **Context loss**: three's `WebGLRenderer` calls `preventDefault()` on `webglcontextlost` and re-initialises on restore ([source](https://github.com/mrdoob/three.js/blob/r186/src/renderers/WebGLRenderer.js)). Show the poster while the context is lost. Whether PMREM targets and render targets fully survive a restore is (unverified), so re-create them on `webglcontextrestored`.

### 6.4 Progressive-enhancement bootstrap (poster first, 3D only if it can pay its way)

```html
<section class="hero" data-hero>
  <img class="hero__poster" src="/img/hero-poster.avif" width="1600" height="1000"
       alt="Cork coaster, top view, raking morning light" fetchpriority="high">
  <canvas class="hero__gl" aria-hidden="true"></canvas>
  <div class="hero__copy"><h1>…</h1></div>
</section>
```

```css
.hero { position: relative; min-height: 100svh; }
.hero__poster, .hero__gl { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.hero__gl { opacity: 0; transition: opacity 500ms ease; touch-action: pan-y; }
.hero.is-live .hero__gl { opacity: 1; }       /* only the decorative canvas fades; the poster and copy are never hidden */
.hero__copy { position: relative; }           /* DOM text above the canvas, always visible */
```

```js
// boot-3d.js (syntax-checked; runtime path checked against docs)
const hero = document.querySelector('[data-hero]');
const canvas = hero.querySelector('.hero__gl');
const reduce = matchMedia('(prefers-reduced-motion: reduce)');
const saveData = navigator.connection?.saveData === true;

function canRunWebGL2() {
  try {
    const gl = document.createElement('canvas').getContext('webgl2', { failIfMajorPerformanceCaveat: true });
    gl?.getExtension('WEBGL_lose_context')?.loseContext();         // don't hold one of the ~16 context slots
    return !!gl;
  } catch { return false; }
}
const idle = (fn) => ('requestIdleCallback' in window ? requestIdleCallback(fn, { timeout: 2000 }) : setTimeout(fn, 200));
const afterLoad = (fn) => (document.readyState === 'complete' ? idle(fn) : addEventListener('load', () => idle(fn), { once: true }));

if (!saveData && canRunWebGL2()) afterLoad(async () => {
  const { createHero } = await import('./hero-scene.js');         // three.js downloads only here
  const app = await createHero(canvas, { reducedMotion: reduce.matches });   // resolves after compileAsync + first frame
  hero.classList.add('is-live');
  let onScreen = true;
  const sync = () => app.setRunning(onScreen && !document.hidden);
  new IntersectionObserver(([e]) => { onScreen = e.isIntersecting; sync(); }, { rootMargin: '200px' }).observe(hero);
  document.addEventListener('visibilitychange', sync);
  reduce.addEventListener('change', (e) => app.setReducedMotion(e.matches));
  canvas.addEventListener('webglcontextlost', () => hero.classList.remove('is-live'));
  canvas.addEventListener('webglcontextrestored', () => app.rebuild().then(() => hero.classList.add('is-live')));
});
```

`hero-scene.js` owns the renderer. It sets `setPixelRatio(Math.min(devicePixelRatio, 2))`, loads the GLB with the loaders from section 7, awaits `compileAsync`, renders one frame, and exposes `setRunning(on)`, which calls `renderer.setAnimationLoop(on && !reduced ? frame : null)`.

---

## 7. Asset pipeline: Blender or C4D → glTF → web

### 7.1 Authoring rules

**In Blender or C4D**
- 1 unit = 1 m. Apply transforms. Keep the origin where the object rotates.
- Use Principled BSDF only. C4D's exporter ignores node materials, doesn't export shaders (bake them) or lights, and takes only the first UV set ([C4D](https://help.maxon.net/c4d/en-us/Content/html/FGLTFEXPORTER.html)).
- Bake procedurals to images.
- Name every node you will animate, raycast or swap. Unnamed nodes get merged by `join`.

**Baking**
- **Baked lighting**: Cycles Combined or Diffuse + AO into an atlas on UV2; atlas 2048 (mobile) or 4096 (desktop hero). glTF packs occlusion into the **R channel of the ORM texture** (occlusion R, roughness G, metalness B). Pack AO there instead of shipping a separate map.
- **Camera animation**: keyframe in the DCC; export with the camera; name the action (section 4.1).

**Export**: GLB, +Y up. Leave the exporter's Draco **off**: compress once, at the end, with glTF Transform. Compression is lossy and repeated round-trips lose precision ([gltf-transform](https://gltf-transform.dev/modules/extensions/classes/EXTMeshoptCompression)).

### 7.2 glTF Transform commands (CLI 4.5.0)

```bash
npm i -g @gltf-transform/cli            # 4.5.0; KTX2 steps need KTX-Software >= 4.4.0 ('ktx' on PATH)

gltf-transform inspect hero.glb         # geometry-heavy? texture-heavy? draw calls?

# One-shot for a static hero. Keep named nodes; skip simplify on hard-surface silhouettes.
gltf-transform optimize hero.glb hero.web.glb \
  --compress meshopt --texture-compress ktx2 --texture-size 2048 \
  --join-named false --simplify false

# Granular pipeline when you need control:
gltf-transform weld     in.glb a.glb
gltf-transform simplify a.glb b.glb --ratio 0.5 --error 0.001          # background props only
gltf-transform resize   b.glb c.glb --width 2048 --height 2048
gltf-transform uastc    c.glb d.glb --slots "{normalTexture,occlusionTexture,metallicRoughnessTexture}" --level 4 --rdo
gltf-transform etc1s    d.glb e.glb --quality 255                       # remaining color slots
gltf-transform instance e.glb f.glb
gltf-transform meshopt  f.glb out.glb --level high
```

What the defaults do, from the CLI source:
- `optimize` defaults to `--compress meshopt`, `--texture-compress auto`, `--texture-size 2048`, and turns on `--simplify` (error 0.0001), `--weld`, `--join`, `--flatten`, `--instance`, `--palette`, `--prune` and `--resample`.
- With `--texture-compress ktx2` it sends normal, occlusion and metalRough slots to **UASTC** (level 4, RDO) and everything else to **ETC1S** at quality 255 ([cli.ts](https://github.com/donmccurdy/glTF-Transform/blob/main/packages/cli/src/cli.ts)).
- **`--flatten` and `--join` rewrite the hierarchy.** Set `--flatten false` for rigged or animated hierarchies.

**Meshopt or Draco?**
- **Default to Meshopt.** It has a lighter decoder, much faster decode, and it also compresses animation and morph targets. It **must be served with gzip or brotli** to reach its full size win.
- **Draco** can win on dense scanned meshes.
- Neither one improves frame rate. Only fewer vertices and draw calls do ([gltf-transform](https://gltf-transform.dev/modules/extensions/classes/EXTMeshoptCompression)).

### 7.3 Loader setup (three r186)

Self-host the decoders. The addon files live at `examples/jsm/libs/basis/`, `libs/draco/` and `libs/meshopt_decoder.module.js` in r186.

```js
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';
import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';

const ktx2 = new KTX2Loader().setTranscoderPath('/vendor/basis/').detectSupport(renderer);
const draco = new DRACOLoader().setDecoderPath('/vendor/draco/');     // only if any asset uses Draco
const loader = new GLTFLoader().setKTX2Loader(ktx2).setDRACOLoader(draco).setMeshoptDecoder(MeshoptDecoder);
const gltf = await loader.loadAsync('/models/hero.web.glb');
```

### 7.4 Environment maps

- Use 1k–2k HDRIs for lighting only. Display the HDRI as the background only when it *is* the scene. A blurry low-res HDRI backdrop is a cheap tell.
- Use `HDRLoader` (renamed from `RGBELoader` in r180) for `.hdr`.
- **`UltraHDRLoader`** reads gain-map JPEGs, which are far smaller than `.hdr`; the size ratio is (unverified). three's examples moved to it in r182, and its header links a converter.
- PMREM once, then reuse the result for every material.

### 7.5 Sources and licensing

| Source | License reality for a web build |
|---|---|
| **Own renders and models** | Best. It is the law's "one signature artifact", and uniqueness is the point on award sites. |
| **Poly Haven** (HDRIs, textures, models) | **CC0**: commercial use, no attribution, redistribution allowed ([license](https://polyhaven.com/license)) |
| **Fab** (Epic; Standard License) | Commercial use in your project is fine, and credit is not required. **You may not "resell or redistribute the asset … on a standalone basis".** "Reference-Only" tier gives no source format ([EULA](https://www.fab.com/eula)). A GLB served to browsers can be downloaded, so ship it compressed and merged into your scene, never as a clean standalone file. Whether client-side delivery counts as redistribution is (unverified); read the full EULA for high-value assets. |
| CC-BY models (Sketchfab-style) | Attribution is required (credits page). "Editorial" licenses bar commercial use. |
| AI-generated meshes | Topology, UVs and baked lighting are usually unusable for a hero. Use them only for background props after retopology (house rule). |
| Spline / Unicorn library assets | Covered by the plan's commercial terms. Unicorn Free is non-commercial. |

---

## 8. Failure modes that read as cheap (and the fix)

1. **The canvas is the LCP element or blocks first paint.** Fix: DOM poster + DOM copy first; import three after `load` + idle (section 6.4).
2. **Content hidden until WebGL reveals it** (opacity-0 text waiting on a timeline or a shader intro). This is the law's invisible-content trap. Fix: text and images are always in the DOM and visible; only the decorative canvas fades in, and only after it has rendered.
3. **A floating object with no contact shadow or AO.** Fix: baked AO, a contact shadow, or an accumulated shadow.
4. **Default grey `MeshStandardMaterial`, metal with no environment (renders black), uniform roughness.** Fix: an environment map, roughness maps, and clearcoat or sheen where physically right.
5. **Tone mapping wrong.** `NoToneMapping` clips; ACES skews brand colours; photos get tone-mapped. Fix: Neutral for product and brand colour, AgX for scenes; photo planes use `toneMapped: false`.
6. **Glow everywhere.** Whole-frame bloom, neon halos behind the hero, additive particle soup. These are the law's glow tells. Fix: bloom threshold ≥ 1 on real emissives only, and directional light with falloff.
7. **Uncompressed 4k PNG textures.** 89.5 MB each in GPU memory, and iOS tab crashes are likely. Fix: KTX2, 2048 cap, one atlas.
8. **Unclamped DPR** (3× on phones = 9× the fragments of 1×). Fix: `min(dpr, 2)`, or 1.5 for heavy shaders.
9. **A canvas per image.** The 17th image loses its context. Fix: one shared canvas with DOM-synced planes.
10. **The render loop never stops**, even offscreen, in a hidden tab, or on a static scene. Fix: IntersectionObserver + `visibilitychange` + `setAnimationLoop(null)` / `frameloop="demand"`.
11. **Shader-compile hitch on first hover or scroll.** Fix: `compileAsync` before reveal; warm up post passes by rendering once offscreen.
12. **Scroll camera that snaps, jitters or freezes.** Causes: raw scroll → camera with no damping, frame-rate-dependent lerp, or `LoopOnce` + `clampWhenFinished` freezing on scrub-back (verified). Fix: section 4.1.
13. **Hover distortion that tears at the pointer** (`normalize(d)` singularity), reversed `smoothstep` edges, or RGB-split on every image. Fix: section 4.4's zero-at-centre lens.
14. **Blob hero**: noise-displaced iridescent sphere, auto-rotating, with no subject. Fix: pick a real subject (Q0), or no 3D.
15. **Dithering or grain laid over text**, or a speckled dithered void. Fix: post on the canvas only; luminance remap; half-level threshold offset (section 4.8).
16. **Splat edges and floaters in frame, free orbit showing the unscanned back.** Fix: tight framing, rails, a poster from the same viewpoint.
17. **Watermarks and third-party hosting surprises.** Spline Free and Unicorn Free watermark; Unicorn Free is non-commercial; Spline scenes are hosted by Spline unless you are on Enterprise; drei pulls Draco from gstatic; detect-gpu pulls from unpkg. Fix: paid tiers where required, self-hosted decoders and benchmark data.
18. **Version traps.**
    - `npm i @needle-tools/engine` installs a 6.0 alpha.
    - pmndrs `postprocessing` 6.39.5 caps `three <0.187`.
    - `WebGPURenderer` silently ignores `ShaderMaterial`, `onBeforeCompile` and `EffectComposer`.
    - `PostProcessing` is now `RenderPipeline` (r183); `RGBELoader` is now `HDRLoader` (r180); `PCFSoftShadowMap` is gone (r186).

    Fix: pin versions and read the release notes for each three bump.
19. **Leftover dev artifacts in production.** Observed on an SOTD: a `<script src="http://192.168.1.15:3000/...">` tag, which is mixed content and a LAN request from every visitor's browser. Fix: CI grep for private IPs and `localhost` in built HTML.
20. **Only WebGPU tested.** The WebGL2 fallback path renders differently or breaks, and it's what Firefox on Linux/Android and older Safari users get. Fix: test with `forceWebGL: true` on every build. Snippets here were verified on that path.

---

## Retrieval gaps

- **Bundle probe coverage.** Regex scan of HTML plus one level of same-origin JS. Deeper lazy chunks were missed, so "engine not found" on Shopify Editions, Ponpon Mania, Pensatori, Lama Lama and others is inconclusive. Meshopt decoders loaded as separate files would not be counted, so the Draco-vs-Meshopt split is a lower bound. The Awwwards listing JSON carries a truncated tag list, and award level was not checked for Unbelievably Crap.
- **WebGPU runtime.** The preview browser had no `navigator.gpu`, so the TSL snippets were verified on the WebGL2 fallback only. The WGSL path was not executed.
- **Not executed**: the R3F/JSX configurator, the scroll-camera module (only the AnimationMixer scrub behaviour was tested), the bootstrap and `hero-scene.js`, Spark, cobe, Unicorn and Spline embeds.
- **Unverified numbers**:
  - device GPU-memory ceilings behind the texture budget
  - Spline runtime transfer size (npm unpacked size, 35.9 MB, is not transfer size)
  - UltraHDR vs `.hdr` size ratio
  - whether three fully restores PMREM and render targets after context restore
- **Licensing interpretation.** Whether serving a Fab asset as a client-downloadable GLB counts as "standalone redistribution" was not confirmed from the full EULA text. The Rive Free tier's export limits were inferred from the pricing table ("Export .riv files" is listed under Cadet).
- **Spline tier gating** (code-export download and glTF export from Pro up; self-hosted export on Enterprise only) was read from the check and cross icons in the pricing comparison table. The self-hosted docs page confirms the Enterprise part in text.
- **Not reached**: Awwwards per-site credits (agency names); the Unicorn Studio pricing page itself (JS-rendered, so I used its docs pricing page); the Chromium issue on the context limit (sign-in wall, so I used Stack Overflow and GitHub reports).
- **OGL, Paper Shaders and Needle** were not observed in winners. Their maturity claims rest on registry and repo metadata only.
