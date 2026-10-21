# Imagery and art direction on award-winning sites (2025–2026)

Last updated: 2026-09-24

This covers what winners put in the frame and how they treat it: photography, renders, real-time 3D, illustration, video, type-as-image and AI imagery, plus how an agent builds each one. Motion systems, 3D engineering and type systems have their own research files. This file covers only the image layer of those topics.

**Evidence base.** Sources are:

- The skill corpus (`data/corpus.jsonl`, 732 Awwwards records scraped 2026-09-24), including 201 Site of the Day (SOTD) records dated 2025-01-07 to 2026-09-25. 186 of those come from the six newest SOTD listing pages, which cover 2026-03-23 to 2026-09-25.
- Awwwards award and tag listings fetched with curl on 2026-09-24.
- Eight live sites probed with `site_probe.py`. Screenshots are in `evidence/imagery-probes/`, and each one was reviewed separately.
- Awwwards element stills.
- Studio write-ups, standards documents and caniuse/webstatus data, all fetched 2026-09-24.

**Labels.** "Observed" means seen on a live site or in a probe. "Documented" means stated by the maker or in a spec. My own recommendations are labelled **(rec.)**.

**House rule.** The anti-slop design law (`deslop-law.md`) overrides award-site habits. Wherever a common winner pattern is a slop tell under that law, this file says so and gives the crafted alternative.

---

## 0. Ten decisions to make before touching code

1. **Pick one medium and one world first.** Photo, render, real-time 3D, illustration, video, type or collage. Winners build the whole site around one signature artifact. Lusion rejected Oryzo's first concept because it "looked like one of those typical Awwwards Site of the Day concepts… Clean, stylish, and abstracted… lifeless." They replaced it with a believable, lived-in desk scene ([Lusion BTS part 3](https://blog.lusion.co/oryzo-bts-part-3-7-website-ux-ui-and-illustrations)). The deslop law's "one signature artifact" and "'Creative' is not 'realistic'" rules say the same thing.
2. **Keep UI color and type quiet so the imagery can be loud.** Oryzo uses four colors, and about 99% of its type is one family ([Lusion part 3](https://blog.lusion.co/oryzo-bts-part-3-7-website-ux-ui-and-illustrations)).
3. **Sample page surfaces from the imagery, not from a UI kit.** Observed examples:
   - Era Residence's section blue `#B5CEDB` is the sky in its renders.
   - Son Daven's sand `#A89474` is the façade and bronze tone.
   - Oryzo's `#100904`/`#FF8539` is the cork and its lit background.

   Palettes are from the [Awwwards site pages](https://www.awwwards.com/sites/era-residence).
4. **Write an image bible before sourcing anything (rec.).** It fixes light direction, time of day, lens range, camera height, grade/LUT, crop ratios and a subject-to-negative-space ratio. See §4.3.
5. **Content is visible by default.** Every treatment in §2 degrades to a plain, correctly cropped image when JavaScript, WebGL or `animation-timeline` is missing, or when `prefers-reduced-motion: reduce` is set.
6. **Type over an image must pass contrast at the worst glyph-sized spot, not on average** (WCAG [1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)). Choose the text color per image first, and add a scrim only if that still fails (§3.1).
7. **Serve AVIF → WebP → JPEG through `<picture>`.** Give the LCP image `fetchpriority="high"` and never lazy-load it. Use `<picture>` media sources for real re-crops, not just resizes (§4.4).
8. **Video loops play muted, inline, with a poster.** Loops of 5 s or more that start automatically need a pause control ([WCAG 2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html)). Alpha video puts HEVC first and VP9 second (§4.5).
9. **Use AI for exploration, base plates and jokes. Don't use it for people, products or places you present as real** (§1.9). Finish AI output by hand, and composite it with your own renders and photos.
10. **Heavy is common but not good.** Probed winners shipped about 7–42 MB of media in five scroll steps (§1.4). Set a budget (rec. ≤ 3 MB above the fold on mobile, streamed video beyond that) and lazy-load everything below the fold.

---

## 1. What the evidence says about media on winning sites

### 1.1 Tag shares among SOTD winners (corpus, n = 201, 2025-01 → 2026-09)

Awwwards tags are self-selected by submitters and each listing card shows only about 8 of them, so treat these as lower bounds. Detail-page tags from the corpus were used where available.

| Media archetype (tags counted) | SOTD share | Mean jury overall |
|---|---|---|
| Real-time 3D (`WebGL`, `Three.js`, `3D`, `GLSL`, `PixiJS`) | 114/201 = **57%** | 7.43 |
| Photography (`Photography`, `Photographic`, `Photo & Video`, `Big Background Images`) | 41/201 = **20%** | 7.35 |
| Typography-led (`Typography`) | 38/201 = 19% | 7.35 |
| Illustration (`Illustration`, `Art & Illustration`, `Flat Design`) | 31/201 = **15%** | 7.48 |
| Video / film (`Video`, `Film & TV`, `Photo & Video`) | 27/201 = 13% | 7.37 |
| Filters and Effects | 16/201 = 8% | 7.45 |
| DCC-rendered 3D (`Blender`, `Cinema 4D`) | 15/201 = 7% | 7.49 |
| No media tag at all (excluding Typography) | 45/201 = 22% | — |
| All SOTD | — | 7.42 |

What this means for a builder:

- **Hybrids dominate.** 18 of 41 photography winners are also tagged 3D/WebGL, and so are 18 of 31 illustration winners. The typical winner mixes a still medium with a GPU layer: photo planes in WebGL, illustration with shader transitions.
- **The medium doesn't win on its own.** Mean scores by archetype sit within 0.14 of each other (7.35–7.49). Execution and concept make the difference.
- **Treatments shown as highlights** (element titles across all 732 records): gallery 150, video 142, parallax 82, reveal 68, shader 48, glass 25, particles 22, mask 22, pixel 21, ascii 19, liquid 13, cursor trail 10, distort 9, dither 2. *Grain*, *duotone* and *halftone* never appear as a highlighted element. They are substrate treatments, not showpieces.

### 1.2 Tag-listing cadence (fetched 2026-09-24)

Each listing page holds 31 submissions (winners and nominees). The date span the 31 cover shows how often each tag is used:

- [Photography](https://www.awwwards.com/websites/photography/): 31 entries in about 5 weeks (2026-08-18 → 09-24). 5 of the 31 are AI image/video tools (photiu ai, MagicShot.ai, Seedance 2.0, Upscale Image, an "AI Filmmaker").
- [Video](https://www.awwwards.com/websites/video/): 31 in about 4 weeks. 6 of the 31 are AI generator or dubbing products.
- [Blender](https://www.awwwards.com/websites/blender/): 31 in about 9 weeks (2026-07-22 → 09-22).
- [Cinema 4D](https://www.awwwards.com/websites/cinema-4d/): 31 in about 8 months (2026-01-23 → 09-21).

Implications: Blender is now the tagged DCC of record, and C4D tags appear at roughly a quarter of Blender's rate. The Photography and Video tag feeds are increasingly marketing pages for AI generators, not photography-led design. When browsing for reference, filter by award, not by tag. The `/websites/illustration/` listing returned HTTP 429 (see gaps).

### 1.3 Sites of the Month listing, 2025–2026 (dated by their SOTD)

The SOTM listing covers 20 sites since 2025. By tag, 11/20 are 3D, 10/20 WebGL, 4/20 Art & Illustration, and 2/20 photo-led. Media read from probes and element stills:

| SOTD date | Site | Primary imagery (observed) |
|---|---|---|
| 2026-08-31 | [Era Residence](https://www.awwwards.com/sites/era-residence) | Arch-viz renders styled like 1960s Riviera lifestyle photos; alpha-video bougainvillea overlays |
| 2026-07-20 | [Lama Lama](https://www.awwwards.com/sites/lama-lama-2) | Graphic design + WebGL |
| 2026-06-05 | [Son Daven](https://www.awwwards.com/sites/son-daven) | Overcast, desaturated arch-viz; patterned image edges; hand illustration |
| 2026-05-13 | [Floema](https://www.awwwards.com/sites/floema) | Product renders on a seamless sweep, environmental photography, scroll-zoomed video |
| 2026-04-13 | [Oryzo AI](https://www.awwwards.com/sites/oryzo-ai) (Lusion) | Houdini/Redshift renders → Gaussian splats; macro renders; hand-drawn Procreate illustration; AI used only for jokes |
| 2026-03-26 | [GQ × AP Extraordinary Lab](https://www.awwwards.com/sites/gq-ap-the-extraordinary-lab) | Real-time 3D watch (Blender) |
| 2026-02-09 | [The Renaissance Edition](https://www.awwwards.com/sites/the-renaissance-edition) (Shopify) | AI-founded, human-finished "Renaissance paintings" split into 3D layers |
| 2026-01-21 | [Bruno Simon](https://www.awwwards.com/sites/brunos-portfolio) | Real-time 3D world |
| 2025-12-29 | [MindMarket](https://www.awwwards.com/sites/mindmarket) | Flat character illustration animated in Rive |
| 2025-11-17 | [Lando Norris](https://www.awwwards.com/sites/lando-norris) | Photo + real-time 3D |
| 2025-10-22 | [Ponpon Mania](https://www.awwwards.com/sites/ponpon-mania) | Illustrated comic + WebGL |
| 2025-07-22 | [Tracing Art](https://www.awwwards.com/sites/tracing-art) (Getty/Resn) | Artwork photography + data visualization |
| 2025-03-18 | [Siena Film Foundation](https://www.awwwards.com/sites/siena-film-foundation) | Film stills and video, film-strip WebGL slider |

### 1.4 Probe summary (8 sites, desktop 1440×900, 5 wheel steps, 2026-09-24)

Bytes are declared `content-length` values for requests during the probe only, so they undercount.

| Site | Media observed | Heaviest bytes | Notes |
|---|---|---|---|
| era-residence.com | 22 webp, 10 avif, 8 webm + 7 .mov alpha flowers | webm 25.6 MB, webp 11.7 MB | GSAP 3.15.0, Lenis, Barba, Webflow; `<video>` has an AVIF poster; 0 `<picture>` |
| sondaven.com | 132 webp, 39 mp4 | webp 19.6 MB, mp4 4.8 MB | Screenshot timed out after the first frame under software WebGL |
| floema.com | png/avif stills, video | "mpeg" 14.7 MB, png 2.5 MB | three r181; consent modal covers the hero |
| oryzo.ai | 80 webp, 8 avif, 17 `<picture>`, HLS `.m3u8`, 4 `.riv` | splats ("other") 7.4 MB, webp 6.6 MB, mp4 6.5 MB | three "178 – modified by Lusion"; 106 elements with CSS `filter` |
| shopify.com/editions/winter2026 | 10 glb, 4 ktx2, 14 webp | glb 5.2 MB, mp4 2.1 MB, ktx2 1.2 MB | three r181; screenshot timed out after the first frame |
| siena.film | jpg/webp, 3 mp4 | mp4 24.2 MB | Content sits behind an ENTER gate; the probe never got past it |
| white-desert.com | Cloudflare Stream mp4 hero, webp | mp4 4.4 MB | 22 `backdrop-filter` uses; faint column lines drawn over the photos |
| mindmarket.com | Illustration, Rive | — | Probe finished only 2 steps |

6 of the 7 probes with CSS data had zero `prefers-reduced-motion` rules. Floema was the exception, with 5. JS-level handling was not measured.

### 1.5–1.10 Archetypes: how winners art-direct each

Each block gives when to use it, the direction rules, what was observed, and slop to avoid.

#### 1.5 Editorial / documentary photography

- **Use for** travel, hospitality, fashion, culture, and anything where "real" is the product.
- **Direction.** One honest light condition across the series. White Desert keeps flat, high-key polar light with a cold grade throughout, plus one warm counterpoint (a single orange parka among the climbers, the penguin's orange patch). Documentary crops put the subject at the frame edge with large negative space (tiny climbers on a diagonal ice wall, [element still](https://assets.awwwards.com/awards/element/2026/07/6a6b044d36000427759158.jpg)).
- **Trend context (documented, not Awwwards-specific).** Stills' 2026 report pushes direct flash, wide-angle distortion and "rawness" as "proof of life", and says "Hyper-polished imagery is cheap to produce and boring to consume" ([Stills 2026 report](https://res.cloudinary.com/stills-website/image/upload/v1768316101/Marketing/Stills_2026_Design_Trend_Report.pdf)). Adobe's 2026 forecast lists "Local Flavors": candid, place-specific imagery made with local creators ([Adobe](https://business.adobe.com/resources/creative-trends-report.html)).
- **Scale contrast.** Full-bleed documentary frames alternate with small inset frames. Era Residence places a 374×187 px image under a viewport-wide condensed headline (probe, desktop_03).
- **Slop and fix.**
  - Stock "diverse team laughing at laptop" imagery. Shoot or commission instead, or use one photographer's coherent series.
  - Faint grid or column lines drawn over photographs, as observed on White Desert. This is the law's "faint grid" tell. Let the photo be the surface.
  - A single strong hero followed by flat fills (the law's "flat fill under everything after the hero"). Carry imagery down the scroll.

#### 1.6 Product still-life (photographed or rendered)

- **Use for** physical products, furniture, packaging and hardware.
- **Direction.** One seamless sweep color sampled from the brand, one key light, a soft contact shadow, and the same camera height and focal length for every product. Floema shows benches and signage on the same warm sweep with the same shadow direction, and the product carries the one saturated color (coral legs) (probe, desktop_04).
- **Product in front of type.** Oryzo floats the coaster in front of a viewport-width word so the object hides two letters ("it's w[ea]rable") (probe, desktop_04). Still's can appears through an aperture cut in the wordmark ([element still](https://assets.awwwards.com/awards/element/2026/07/6a63b3256dc0b164703865.png)).
- **Hands** borrow the language of Apple product ads. Lusion bought a scanned real hand and rigged it for Oryzo, and the site then jokes about AI hands: "We said high five. It heard six." ([Lusion part 2](https://blog.lusion.co/oryzo-bts-part-2-7-3d-design-and-motion-graphics), probe desktop_02).
- **Slop and fix.**
  - A centered product with a radial glow halo behind it (law: "Radial glow halo behind an object"). Light it with a directional key and real falloff. Oryzo's warm light enters from one lower corner.
  - A floating info pill pinned to the image corner (law). Put specs in the layout, not on the picture.

#### 1.7 Pre-rendered 3D / CGI and arch-viz

- **Use for** unbuilt architecture, impossible products, and controlled hero scenes where interactivity isn't needed.
- **Direction on real estate winners.**
  - Era Residence stages renders as a period lifestyle shoot: saturated Mediterranean sky, bougainvillea, styled 1960s-looking guests by the pool. The period reference is my reading. The same sky blue becomes the page color, and a sky-masked building cut-out bleeds into that color at the section edge (probe, desktop_04–05).
  - Son Daven goes the other way: overcast, desaturated, watercolour-soft skies, bronze façades, and image edges that break into a vertical-bar pattern in the sand accent instead of a hard crop ([element still](https://assets.awwwards.com/awards/element/2026/05/69fb54cfd800a816559795.png)).
- **Pipeline (documented).** Oryzo was built in SideFX Houdini and rendered in Maxon Redshift, with rigid-body sims to scatter small props ([Lusion part 2](https://blog.lusion.co/oryzo-bts-part-2-7-3d-design-and-motion-graphics)).
- **Slop and fix.** Default HDRI studio lighting, uniform glossy plastic and a centered hero orbit. Build a believable environment instead (Lusion's rejected "abstract product study" versus the lived-in desk they shipped).

#### 1.8 Real-time 3D as imagery

- **Use when** interaction is the point: rotate it, explore it, play it.
- **Direction.** Real-time 3D is judged on how close it gets to pre-rendered quality.
  - Lusion tried image sequences and video (not interactive enough) and real-time PBR (not good enough). They shipped Gaussian splats trained on Houdini renders.
  - Rendering the exact scroll camera path gave *worse* splats. A hemispherical camera spread worked better.
  - 900,000 splats still showed flaws. Restricting splats to props and desk reflections looked better at about 78,233 splats on desktop and 44,683 on mobile. Everything else used baked textures.
  - A shader warped texture coverage so the centre 50% of the desk got about 90% of the texture detail.

  All of this is from [Lusion part 2](https://blog.lusion.co/oryzo-bts-part-2-7-3d-design-and-motion-graphics).
- **Renaissance Edition** shipped compressed `.glb` plus KTX2 textures (probe). Its makers credit texture compression for keeping 60 fps on mobile, which carried 70% of sessions ([RGD](https://rgd.ca/hiring-designers/award-winners/2026-in-house-award-winners/the-renaissance-edition)).
- **Current versions.** three.js 0.186.1 (npm, published 2026-09-24); probed winners ran r178–r181. The engine and performance details belong in the 3D research file.

#### 1.9 Illustration

- **Use for** services and abstract products (research, finance, SaaS), editorial storytelling, and brands that want warmth.
- **Direction.**
  - MindMarket: one flat character style, consistent line weight, 5–6 saturated flat colors, animated subtly in Rive, with copy on solid white panels above the art (probe desktop_01; [Envato](https://elements.envato.com/learn/web-design-trends) notes the characters "animate very subtly").
  - Oryzo: hand-drawn Procreate sketches in the manner of technical and da Vinci studies, painted directly onto 3D props so they "belong to the scene". None of the illustration was AI-assisted ([Lusion part 3](https://blog.lusion.co/oryzo-bts-part-3-7-website-ux-ui-and-illustrations)).
  - Ponpon Mania and Navigate use illustration as the whole world.
- **Slop and fix.** Crude CSS/SVG "illustrations" (div bar charts, floating spheres, orbit rings) are a law tell. Crafted SVG is explicitly "good" under the law. Don't mix illustration styles, and don't put generic 3D-blob characters from packs next to bespoke art.

#### 1.10 Motion video

- **Use for** film and production studios, hospitality and expeditions, anything where movement is the content.
- **Observed patterns.**
  - Full-bleed documentary hero loop: White Desert serves a Cloudflare Stream MP4, autoplay, muted, looped.
  - Hover-to-preview directors list: Partizan shows background video on list hover ([Awwwards](https://www.awwwards.com/sites/partizan)).
  - Scroll-zoomed video: Floema's element "Scroll video zooming".
  - Alpha-channel overlays: Era Residence's animated flowers.
  - Film-strip WebGL slider: Siena.
- **Slop and fix.**
  - An autoplaying hero with no pause control (WCAG 2.2.2).
  - A video that exists only as mood and delays the LCP.
  - Content gated behind an ENTER click. Siena's content never appeared to the probe (§5.2).

#### 1.11 Type-only and type-as-image

- **Use for** brands where the word is the asset: film titles, spirits, luxury, fashion.
- **Observed.**
  - Era Residence opens on plum `#340C24` with the wordmark and a huge tonal script watermark, before any photo (probe desktop_00).
  - Siena's condensed display logotype stands alone on black.
  - Still cuts a lens aperture through its wordmark, and the product shows through it.
- **Slop and fix.** Gradient-filled headline text (law) and one serif italic word "for taste" (law: Cormorant tell). Use image-in-type only as a single signature moment (§3.3).

#### 1.12 Collage and mixed media

- **Use for** changelogs and campaigns that need an editorial wrapper, and archives.
- **Observed.**
  - Renaissance Edition parodies *The Creation of Adam* with sneakers, a coffee cup and a magenta skateboard. The one saturated color is the modern object, and it carries the joke. The copy column sits in the painting's cloud negative space with a hairline golden-ratio construction frame ([element still](https://assets.awwwards.com/awards/element/2025/12/6940c23049240952533982.jpg)).
  - Hearst's photography exhibit stacks real magazine covers with a WebGL paper curl ([element still](https://assets.awwwards.com/awards/element/2026/06/6a2e77ef835dd895613018.jpg)).
- Adobe's 2026 forecast flags "Surreal Silliness" and collage ([Adobe Express](https://www.adobe.com/express/learn/blog/design-trends-2026)).

#### 1.13 Generative / AI imagery: what juries and critics reward

**Documented winner practice**

- **Renaissance Edition (Shopify, SOTD 2026-02-09, 7.92).** "AI generated each artwork's foundations while human artists fine-tuned depth, lighting and character animation." Brushstroke-edge transitions link the sections, and Theatre.js gave designers timeline control. The site drew 3.5M+ sessions and 260+ press stories ([RGD](https://rgd.ca/hiring-designers/award-winners/2026-in-house-award-winners/the-renaissance-edition), [One Club](https://www.oneclub.org/awards/theoneshow/-award/64482/the-renaissance-edition/)).
- **Oryzo (Lusion).**
  - Midjourney was used only for composition and mood. After approval "the work moved into full non-AI 3D production."
  - Google Flow composited AI gags onto their own renders: "the source material was ours."
  - AI was also used to build one microscopic asset: Nano Banana Pro reference views → Hunyuan 3D → ZBrush → procedural detail.

  Their rule, verbatim: "AI was not generating the core idea or the final look." Sources: [part 3](https://blog.lusion.co/oryzo-bts-part-3-7-website-ux-ui-and-illustrations) and [part 2](https://blog.lusion.co/oryzo-bts-part-2-7-3d-design-and-motion-graphics).
- **AI-imagery-first winners exist but score mid-pack.** Detroit ("AI production house… for luxury brands", SOTD 7.35), Fourmula AI (7.27) and Nothin' (7.45, with an element called "IA Video background" tagged *weird, wtf*). The corpus mean is 7.42, and the sample is small.

**Jury and critic perception**

- An Awwwards young-jury member who reviewed 100+ sites wrote that the standout sites "None of them felt like a prompt." AI-heavy work "exists in an aesthetic nowhere… culturally placeless" ([Medium, 2026-06-07](https://medium.com/design-bootcamp/i-judged-100-websites-for-awwwards-ai-is-winning-the-wrong-race-38efd7f3e3cc)). This is one juror's opinion.
- Jury weighting is Design 40%, Usability 30%, Creativity 20%, Content 10%, as shown on SOTD pages such as [Oryzo's](https://www.awwwards.com/sites/oryzo-ai). A juror-practitioner warns that "stock-grade imagery" bleeds the Content score ([hontran.dev](https://www.hontran.dev/blog/awwwards-judging-criteria)).

**Audience trust data**

- Getty VisualGPS (30,000+ adults, 25 countries, 2022–2024): 98% say "authentic" images and video are pivotal to trust, and nearly 90% want to know when an image is AI-made. AI depictions of *non-human subjects* were seen as less misleading than AI people or products ([Getty newsroom](https://newsroom.gettyimages.com/en/getty-images/nearly-90-of-consumers-want-transparency-on-ai-images-finds-getty-images-report)).
- A 2026 follow-up interview reports that respondents prefer real images to AI ones, 38% vs 15% ([CX Network, 2026-09-03](https://www.cxnetwork.com/artificial-intelligence/interviews/ai-generated-images-customer-trust-advertising)).

**Rules for the agent**

- **Yes:** mood and composition exploration; painted or surreal base plates that humans then finish; background worlds with no people and no products; deliberate jokes about AI.
- **No:** AI people presented as real (team, testimonials, "customers"); AI renderings of the actual product or food; AI views of real places presented as photographs; AI as a stock-photo substitute.
- **Always:**
  - One style reference and one light direction across the whole set.
  - Inpaint or paint over hands, text, faces and edges.
  - Composite AI with your own renders, photos or scans.
  - Grade the whole set with one LUT.
  - Label AI imagery where trust matters: health, finance, travel, and any testimonial ([Getty](https://newsroom.gettyimages.com/en/getty-images/nearly-90-of-consumers-want-transparency-on-ai-images-finds-getty-images-report)).
- **AI tells to reject in QA (rec.):**
  - Waxy skin and over-smooth micro-detail.
  - Teal-orange "cinematic" grading on every frame.
  - Centered symmetrical subject with bokeh.
  - Light direction that changes between images in a set.
  - Garbled text on signs or labels.
  - Extra or fused fingers.
  - Everything shares the same generic polish (the "aesthetic nowhere").

---

## 2. Treatments: recipes and when each is slop

Each treatment below lists the rule for when it is legitimate, the slop condition, and a checked recipe. Browser support and versions are as of 2026-09-24, from caniuse data at GitHub commit `1.0.30001812` and from [webstatus.dev](https://webstatus.dev).

### 2.1 Color grade and tonal unification

- Bake the grade into the assets with one LUT for the whole set. Use CSS `filter` only for state changes (e.g. hover desaturation), not as the grade. CSS filters cost paint on every frame and don't reach `<video>` posters rendered outside the element.
- Pull page tokens from the graded set: the darkest shadow becomes the ink, a mid-tone becomes the surface, and one image-native accent becomes the tonal accent.
- **Law check.** Saturated color belongs inside the image as a story device (Renaissance's magenta skateboard, White Desert's orange parka). It does not belong on UI chrome. White Desert's saturated orange "Enquire" button and side tab break the law's "Saturated accent color" rule. Use a tonal step off the page color for UI instead.

### 2.2 Duotone and tritone

- **Legitimate** when the brand owns two colors and the photo set is inconsistent (archive or stock material), or when a hover state needs to switch between treated and original.
- **Slop** when it is a Spotify-era default (e.g. magenta/cyan) with no link to the brand, or when it is applied to people's faces in a way that reads as a filter.

```html
<!-- One hidden SVG per page. color-interpolation-filters="sRGB": the default is linearRGB,
     which shifts midtones (MDN: color-interpolation-filters). -->
<svg width="0" height="0" aria-hidden="true" style="position:absolute">
  <filter id="duo-ink" color-interpolation-filters="sRGB">
    <!-- 1) luminance to grey -->
    <feColorMatrix type="matrix" values="
      0.2126 0.7152 0.0722 0 0
      0.2126 0.7152 0.0722 0 0
      0.2126 0.7152 0.0722 0 0
      0      0      0      1 0"/>
    <!-- 2) map black->shadow (#141A12), white->highlight (#D7DEC8); add a 3rd value for tritone -->
    <feComponentTransfer>
      <feFuncR type="table" tableValues="0.078 0.843"/>
      <feFuncG type="table" tableValues="0.102 0.871"/>
      <feFuncB type="table" tableValues="0.071 0.784"/>
    </feComponentTransfer>
  </filter>
</svg>
<style>
  .duo img { filter: url(#duo-ink); }
  @media (hover: hover) { .duo:hover img { filter: none; transition: filter .6s ease; } }
</style>
```

For LCP or hero images, bake the duotone into the file with a gradient map in the grading tool instead **(rec.)**. Syntax checked against [MDN feColorMatrix](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/feColorMatrix) and [color-interpolation-filters](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/color-interpolation-filters), where the default is `linearRGB`.

### 2.3 Grain and noise, applied behind the content

- **Legitimate** on large tonal transitions and dark renders, to kill banding. The law: "Any large color transition should carry grain… a clean banded one reads as cheap."
- **Slop** as a fixed full-page noise sheet on top of text and controls (law: "Grain sitting on top of the content"). The exception is grain deliberately masked onto one display word.
- **Performance.** Pre-render the noise tile as a PNG instead of running a live SVG `feTurbulence` chain. CSS-Tricks notes that heavy filter chains are better served as a JPEG or PNG ([CSS-Tricks](https://css-tricks.com/creating-patterns-with-svg-filters/)). A tile can be generated once from the [grainy-gradients technique](https://css-tricks.com/grainy-gradients/): `feTurbulence type="fractalNoise" baseFrequency≈0.65–0.95 numOctaves=3 stitchTiles="stitch"`.

```css
.surface-grain {                 /* the section or media wrapper, never the whole page */
  position: relative;
  isolation: isolate;            /* keep the grain inside this stacking context */
  background: var(--surface);
}
.surface-grain::before {
  content: "";
  position: absolute; inset: 0;
  z-index: -1;                   /* BEHIND text and controls */
  pointer-events: none;
  background: url("/tex/grain-256.png") 0 0 / 256px 256px;
  opacity: .07;                  /* 0.04–0.10 (rec.) */
  mix-blend-mode: soft-light;    /* Safari lacks only hue/saturation/color/luminosity modes (caniuse) */
}
```

AVIF at default quality (sharp's default is `quality: 50`) tends to smear baked-in fine grain **(unverified; test visually)**. Either overlay grain in CSS as above, or raise quality for grain-heavy assets. caniuse notes that some Safari versions don't decode AVIF film-grain ("noise synthesis") images, so don't rely on AVIF grain synthesis ([caniuse AVIF](https://caniuse.com/avif)).

### 2.4 Dithering, ASCII and pixelation

- **Legitimate** when it is the brand's concept (retro computing, data or dev tools, print heritage). Also as a post-process that unifies mixed 3D sources: Codrops' ordered-dither pass is "for styling and flattening. Think more zine than render farm" ([Codrops 2025-06-04](https://tympanus.net/codrops/2025/06/04/building-a-real-time-dithering-shader/)). ASCII and pixel post-processing appear as highlighted elements on 2026 winners (corpus: *ascii* 19, *pixel* 21).
- **Slop.** Dither is now a drop-in component ([Aceternity Dither Shader](https://ui.aceternity.com/components/dither-shader), [Paper Shaders ImageDithering](https://shaders.paper.design/image-dithering), 21st.dev), so an unmotivated dithered hero background is becoming a template tic. It is the 2026 version of the gradient blob.
- **Recipe.** Use [@paper-design/shaders](https://shaders.paper.design/image-dithering) (npm 0.0.81, Apache-2.0) `ImageDithering` with `type="8x8"`, two brand colors and `size` 2–3. Or write a Bayer8 threshold in your own pass: Codrops shows 8×8 is where perceptual gains stop ([Codrops 2025-07-30](https://tympanus.net/codrops/2025/07/30/interactive-webgl-backgrounds-a-quick-guide-to-bayer-dithering/)).
- Keep the original image as the DOM `<img>` fallback, pause the canvas off-screen, and render nothing under `prefers-reduced-motion` if the dither is animated.

### 2.5 Halftone

- **Legitimate** for print, press or editorial brands and archival material, used on one image or motif.
- **Slop** on every image, or on faces as a gimmick.
- Ana Tudor's pure-CSS method uses three declarations ([Master.dev, 2024-12-03](https://blog.master.dev/pure-css-halftone-effect-in-3-declarations/)):

```css
/* A LEAF element: `filter` also applies to children, so never put text inside it. */
.halftone {
  aspect-ratio: 4 / 5;
  --pattern: radial-gradient(closest-side, #777, #fff) 0 / 1em 1em space;
  --map: conic-gradient(#888 0 0), url("/img/archive-1200.avif") 50% / cover grey;
  background: var(--pattern), var(--map);
  background-blend-mode: multiply, screen, luminosity;
  filter: contrast(16);          /* raise with pattern size; ~2-3x any blur px (source) */
}
```

```html
<div class="halftone" role="img" aria-label="1968 press photo of the founding crew"></div>
```

Dot size is set by the pattern's `background-size` (`1em`). Keep the map's darkest value slightly above 50% grey, as the source recommends. For the CMYK variant and blur "ink bleed", see [Lean Rada](https://leanrada.com/notes/pure-css-halftone/).

### 2.6 Blur and depth of field

- **Legitimate uses.**
  - Real optical depth of field in the photo or render itself.
  - Blur as a *state*: White Desert's gallery blurs inactive accordion panels and keeps the active one sharp (probe desktop_02).
  - Frosted panels over a busy photograph (White Desert's camp cards over an ice texture).
- **Slop.** The law's "Botched glass": banding, a shadow leaking under the element, a blur that pops on hover, glass over a flat field with nothing to refract. Also blurring an image to hide low resolution.
- **Recipe.** `backdrop-filter: blur(16px) saturate(1.2)` on a panel over a detailed photo. It has been Baseline "newly available" since 2024-09-16 ([webstatus](https://webstatus.dev/features/backdrop-filter)). Give it a solid-color fallback via `@supports not (backdrop-filter: blur(1px))`. Never animate the blur radius on hover.

### 2.7 Masks and clip-path shapes

- **Legitimate uses.**
  - Feathered edges that melt an image into the page (law, "Hard image seams").
  - Apertures and shapes that belong to the brand: Still's lens cut through the wordmark, Siena's ticket-notched frames.
  - Scroll-scrubbed *widening* of an image that is already visible.
- **Slop.** Images that start fully clipped (`inset(100%)`) and rely on a reveal to appear. That is the law's invisible-content trap. Rounded-rectangle masks on every image are also a tell.
- **Support.** CSS masks are Baseline widely available since 2026-06-07 ([webstatus](https://webstatus.dev/features/masks)). `clip-path` is widely available.

```css
/* Feathered full-bleed image. Four conditions from the law's verified recipe:
   mask the image itself, 10+ stops, a tall section, the same page color above and below. */
.bleed { min-height: 116vh; background: var(--page); }
.bleed img {
  width: 100%; height: 116vh; object-fit: cover;
  -webkit-mask-image: var(--feather); mask-image: var(--feather);
  --feather: linear-gradient(to bottom,
    transparent 0%, rgb(0 0 0/.02) 3%, rgb(0 0 0/.07) 6%, rgb(0 0 0/.15) 9%, rgb(0 0 0/.27) 12%,
    rgb(0 0 0/.42) 16%, rgb(0 0 0/.58) 20%, rgb(0 0 0/.74) 24%, rgb(0 0 0/.88) 28%, #000 31%,
    #000 65%, rgb(0 0 0/.88) 69%, rgb(0 0 0/.74) 73%, rgb(0 0 0/.58) 77%, rgb(0 0 0/.42) 81%,
    rgb(0 0 0/.27) 85%, rgb(0 0 0/.15) 89%, rgb(0 0 0/.07) 93%, rgb(0 0 0/.02) 97%, transparent 100%);
}

/* A clip that is visible at rest and opens further on scroll.
   Never start from a fully hidden state. */
.frame img { clip-path: inset(0 round 2px); }
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .frame img {
      animation: frame-open linear both;
      animation-timeline: view();          /* must come AFTER the `animation` shorthand, which resets it */
      animation-range: entry 10% cover 40%;
    }
    @keyframes frame-open {
      from { clip-path: inset(10% 16% round 2px); }   /* still ~65% visible */
      to   { clip-path: inset(0 round 2px); }
    }
  }
}
```

Syntax checked against [MDN animation-range](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-range), [MDN view()](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline/view) and [MDN mask-image](https://developer.mozilla.org/en-US/docs/Web/CSS/mask-image). Scroll-driven animations are **Limited availability**: Chrome since 2023-07, Safari 26 since 2025-09-15, not in Firefox ([webstatus](https://webstatus.dev/features/scroll-driven-animations)). The static fallback above is the intended Firefox experience. Use GSAP (§2.9) if parity matters.

### 2.8 WebGL distortion on hover

- **Legitimate** when the distortion means something: liquid for a drinks brand, heat for an energy brand, paper curl for print (Hearst). It works on a small set of large images, and the DOM image stays the source of truth.
- **Slop.** A generic ripple or "liquid" on every card of a portfolio grid. This has been a tutorial staple since 2018–2019 ([Codrops 2018](https://tympanus.net/codrops/2018/04/10/webgl-distortion-hover-effects/), [2019](https://tympanus.net/codrops/2019/10/21/how-to-create-motion-hover-effects-with-image-distortions-using-three-js/)). Under the law it is the image equivalent of the hover boop. Also slop: a distortion strong enough to hurt legibility of any text in the image.
- **Pattern.** DOM-synced planes: the `<img>` stays in the DOM and a fixed canvas draws a plane at each image's rect every frame. This is the setup in [Codrops/Adoratorio 2025-10-08](https://tympanus.net/codrops/2025/10/08/how-to-animate-webgl-shaders-with-gsap-ripples-reveals-and-dynamic-blur-effects/), which caps DPR at 1.5. Checked against three 0.186.1 docs. `ShaderMaterial` must include `colorspace_fragment` itself, or colors come out wrong ([three.js color management](https://threejs.org/manual/#en/color-management)).

```js
import * as THREE from "three";          // 0.186.1
import { gsap } from "gsap";             // 3.15.0

if (!matchMedia("(prefers-reduced-motion: reduce)").matches) {
  const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 1.5));
  renderer.setSize(innerWidth, innerHeight);
  renderer.domElement.className = "gl-layer";   /* CSS: position:fixed; inset:0; pointer-events:none; z-index:1 */
  document.body.append(renderer.domElement);
  renderer.domElement.addEventListener("webglcontextlost", () =>
    document.querySelectorAll(".is-gl").forEach((el) => el.classList.remove("is-gl")));

  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-innerWidth / 2, innerWidth / 2, innerHeight / 2, -innerHeight / 2, -10, 10);

  const vertexShader = `varying vec2 vUv;
    void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`;
  const fragmentShader = `uniform sampler2D uMap; uniform vec2 uMouse; uniform float uHover; uniform vec2 uCover;
    varying vec2 vUv;
    void main(){
      vec2 uv = (vUv - 0.5) * uCover + 0.5;                    // object-fit: cover
      float d = distance(vUv, uMouse);
      float f = smoothstep(0.35, 0.0, d) * uHover;             // local, eased falloff
      uv += normalize(vUv - uMouse + 1e-5) * f * 0.025;        // keep amplitude <= ~0.03 UV
      gl_FragColor = texture2D(uMap, uv);
      #include <colorspace_fragment>
    }`;

  const loader = new THREE.TextureLoader();
  const items = [...document.querySelectorAll("[data-gl-image]")].map((fig) => {
    const img = fig.querySelector("img");
    const uniforms = { uMap: { value: null }, uMouse: { value: new THREE.Vector2(0.5, 0.5) },
                       uHover: { value: 0 }, uCover: { value: new THREE.Vector2(1, 1) } };
    const mesh = new THREE.Mesh(new THREE.PlaneGeometry(1, 1),
                                new THREE.ShaderMaterial({ uniforms, vertexShader, fragmentShader }));
    mesh.visible = false;
    scene.add(mesh);
    loader.loadAsync(img.currentSrc || img.src).then((tex) => {        // needs CORS on the image host
      tex.colorSpace = THREE.SRGBColorSpace;
      uniforms.uMap.value = tex;
      mesh.userData.aspect = tex.image.width / tex.image.height;
      mesh.visible = true;
      requestAnimationFrame(() => fig.classList.add("is-gl"));          // hide the DOM img only after GL draws
    });
    fig.addEventListener("pointerenter", () => gsap.to(uniforms.uHover, { value: 1, duration: .6, ease: "power2.out" }));
    fig.addEventListener("pointerleave", () => gsap.to(uniforms.uHover, { value: 0, duration: .8, ease: "power2.out" }));
    fig.addEventListener("pointermove", (e) => {
      const r = fig.getBoundingClientRect();
      uniforms.uMouse.value.set((e.clientX - r.left) / r.width, 1 - (e.clientY - r.top) / r.height);
    });
    return { fig, mesh, uniforms };
  });

  gsap.ticker.add(() => {                      // same frame as the scroll engine (Lenis/ScrollTrigger)
    for (const { fig, mesh, uniforms } of items) {
      const r = fig.getBoundingClientRect();
      mesh.scale.set(r.width, r.height, 1);
      mesh.position.set(r.left + r.width / 2 - innerWidth / 2, innerHeight / 2 - r.top - r.height / 2, 0);
      const pa = r.width / r.height, ia = mesh.userData.aspect || pa;
      uniforms.uCover.value.set(pa > ia ? 1 : pa / ia, pa > ia ? ia / pa : 1);
    }
    renderer.render(scene, camera);
  });
  addEventListener("resize", () => {
    renderer.setSize(innerWidth, innerHeight);
    Object.assign(camera, { left: -innerWidth / 2, right: innerWidth / 2, top: innerHeight / 2, bottom: -innerHeight / 2 });
    camera.updateProjectionMatrix();
  });
}
```

```css
[data-gl-image].is-gl img { opacity: 0; }   /* set only after the GL plane has drawn; removed on context loss */
```

Other rules for this pattern:

- The fixed canvas sits above the page. Captions or controls placed over a GL image need `position: relative; z-index: 2`, or must sit outside the frame. Otherwise the plane paints over them.
- On touch devices there is no hover. Show the untreated image or trigger once on scroll-into-view.
- Stop rendering when no uniform is animating and no scroll happened (render on demand) **(rec.)**.
- Use DPR ≤ 1.5 and ≤ 8 live planes per viewport **(rec.)**.

### 2.9 Scroll-linked scale and parallax

- **Legitimate.** Slow settling of a full-bleed image (scale 1.12–1.2 → 1) while its section scrolls through, or 5–15% differential parallax between image layers. Era Residence scroll-dollies into its render (probe desktop_01→02). The law endorses quiet parallax on already-visible elements, gated by reduced motion.
- **Slop.** Opacity-from-0 reveals, parallax on text blocks, scroll-jacked full-page image slideshows that override native scroll, and more than two parallax speeds in one viewport.
- **CSS-first (no JS).** Same structure as §2.7. The image is visible at every scroll position:

```css
.media-settle { overflow: clip; }
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .media-settle img {
      animation: settle linear both;
      animation-timeline: view();
      animation-range: entry 0% cover 60%;
    }
    @keyframes settle { from { scale: 1.15; } to { scale: 1; } }
  }
}
```

- **GSAP version** for Firefox parity or when you're already on ScrollTrigger. GSAP 3.15.0 on npm is under the "Standard 'no charge' license" ([npm](https://www.npmjs.com/package/gsap)). `gsap.matchMedia()` reverts everything when the query stops matching ([GSAP docs](https://gsap.com/docs/v3/GSAP/gsap.matchMedia())):

```js
gsap.registerPlugin(ScrollTrigger);
gsap.matchMedia().add("(prefers-reduced-motion: no-preference)", () => {
  gsap.utils.toArray(".media-settle img").forEach((img) => {
    gsap.fromTo(img, { scale: 1.15 }, {
      scale: 1, ease: "none",
      scrollTrigger: { trigger: img.parentElement, start: "top bottom", end: "center center", scrub: true },
    });
  });
});
```

### 2.10 Image sequences (scroll-scrubbed frames)

- **Legitimate** for a product turntable or assembly where video scrubbing stutters. More Nutrition (SOTD 2025-11-03) tied render frames to scroll with GSAP. Swapping `img.src` "got laggy when scrolling fast", so they drew to canvas instead ([Awwwards case study](https://www.awwwards.com/more-nutrition-you-deserve-more.html)). GSAP ships an official [imageSequenceScrub helper](https://gsap.com/docs/v3/HelperFunctions/helpers/imageSequenceScrub). Lusion rejected sequences for Oryzo only because they needed interactivity ([part 2](https://blog.lusion.co/oryzo-bts-part-2-7-3d-design-and-motion-graphics)).
- **Slop.** 300+ frames, or the whole page pinned for one spin. Also a blank canvas while frames load.
- **Budget (rec.).** 60–150 frames of WebP/AVIF at 1600 px wide, 40–90 KB each (about 3–10 MB). Use a half-resolution set with every second frame on mobile. Load frame 0 eagerly and the rest after `load`.

```html
<section class="seq" style="height:400vh">
  <div class="seq__stage" style="position:sticky;top:0;height:100svh">
    <img class="seq__poster" src="/seq/f000.avif" alt="The Mk II kettle, exploded into its 14 parts" width="1600" height="900">
    <canvas class="seq__canvas" aria-hidden="true"></canvas>  <!-- shown only after frame 0 is drawn -->
  </div>
</section>
```

```js
gsap.matchMedia().add("(prefers-reduced-motion: no-preference)", () => {
  const canvas = document.querySelector(".seq__canvas"), ctx = canvas.getContext("2d");
  const urls = Array.from({ length: 120 }, (_, i) => `/seq/f${String(i).padStart(3, "0")}.webp`);
  const frames = urls.map((u) => Object.assign(new Image(), { decoding: "async", src: u }));
  const size = () => { const r = canvas.getBoundingClientRect(), d = Math.min(devicePixelRatio, 2);
                       canvas.width = r.width * d; canvas.height = r.height * d; };
  const draw = (i) => { const img = frames[i]; if (!img.complete || !img.naturalWidth) return;
    const s = Math.max(canvas.width / img.naturalWidth, canvas.height / img.naturalHeight);
    const w = img.naturalWidth * s, h = img.naturalHeight * s;
    ctx.drawImage(img, (canvas.width - w) / 2, (canvas.height - h) / 2, w, h); };
  const play = { f: 0 };
  size(); addEventListener("resize", () => { size(); draw(Math.round(play.f)); });
  frames[0].onload = () => { draw(0); canvas.classList.add("is-live"); };   /* CSS: poster stays under the canvas */
  gsap.to(play, { f: urls.length - 1, ease: "none", onUpdate: () => draw(Math.round(play.f)),
    scrollTrigger: { trigger: ".seq", start: "top top", end: "bottom bottom", scrub: 0.3 } });
});
```

### 2.11 Cursor image trails and stacks

- They appear as highlighted elements (corpus *trail* 10: Bornfight "Image Trail", Nightkidz "Cursor Image Stack").
- **Slop** as a portfolio default, because the images carry no information and they fail on touch.
- **Legitimate** only when the trail *is* the content, e.g. an archive you browse by moving the cursor. It then needs a grid or list alternative and a non-hover path.

### 2.12 Hover on image cards: the law wins

- No card lift, no shadow bloom, no animated underline under the caption (law: "card hover-lift", "hover boop", "underline-fill").
- The frame stays still. If anything changes, it happens inside the frame:
  - the image scales ≤ 1.04 within `overflow: clip` over ≥ 500 ms, or
  - a still swaps to a muted video preview (Partizan directors list), or
  - the caption makes a tonal color step.
- **(rec.)**

---

## 3. Image + type composition

### 3.1 Legibility over images: measure it, don't guess

**Thresholds.**

- WCAG 1.4.3 requires 4.5:1, or 3:1 for large text (≥ 24 px, or ≥ 18.66 px bold) ([W3C](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)).
- Failure F83 covers background images that don't provide sufficient contrast.
- Technique G145 allows shading the area behind letters or adding a halo to reach 3:1 for large text ([W3C G145](https://www.w3.org/WAI/WCAG22/Techniques/general/G145)).

**Measure the worst case, not the average.**

- Use the worst-contrast pixel ([CSS-Tricks](https://css-tricks.com/nailing-the-perfect-contrast-between-light-text-and-a-background-image/)).
- Better, use the maximum mean luminance over a glyph-sized window. Picking the text color per image first removed the need for a scrim on 189 of 240 images in one study ([Rork Lab, 2026-08-06](https://rorklab.net/en/articles/app-dev/overlay-text-legibility-ingest-time-scrim-metadata-measurement)).
- For white text on a black overlay, you never need more than about 0.54 overlay opacity to reach AA ([CSS-Tricks](https://css-tricks.com/nailing-the-perfect-contrast-between-light-text-and-a-background-image/)).

**Decision ladder (from Rork Lab, adapted):**

1. White text passes everywhere → no scrim.
2. Black text passes everywhere → dark text, no scrim.
3. Otherwise → compute the minimum black-scrim alpha for white text. Apply it only behind the text band, fading to 0 before any section edge (law: "Hard image seams").
4. Over budget (alpha > 0.5) → use a solid plate for the copy. Son Daven's dark data panel and MindMarket's white card are observed examples. Or move the text to negative space, or re-crop.

**Observed failure.** White Desert sets a white condensed "ANTARCTICA" over a penguin's white and grey chest (probe desktop_00). Part of the word visibly fails, and captions in white also sit over bright snow (desktop_02). The fix is ladder step 2 or 4, or `object-position` so the dark head sits behind the type.

Build-time check (Node, sharp 0.35.4). It returns the black scrim alpha that white text needs over a region. It is a heuristic in the Rork Lab style, so confirm the worst spot visually or with G145. It was smoke-tested on the probe screenshots and runs in under 0.4 s for a 1160×210 region. Feed it the clean source image: screenshots that already contain the white text overstate the scrim.

```js
import sharp from "sharp";
const lin = (v) => ((v /= 255) <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4);
const lum = (r, g, b) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);

// box: {left, top, width, height} of the source image that sits under the text after cropping
// win: glyph-sized window in source px; ratio: 4.5 body, 3 for large display type
export async function whiteTextScrim(src, box, win = { w: 120, h: 40 }, ratio = 4.5) {
  const { data, info: { width: W, height: H } } =
    await sharp(src).extract(box).removeAlpha().raw().toBuffer({ resolveWithObject: true });
  const limit = 1.05 / ratio - 0.05;                     // max background luminance for white text
  const I = new Float64Array((W + 1) * (H + 1));         // integral image of luminance
  for (let y = 0; y < H; y++) for (let x = 0, row = 0; x < W; x++) {
    const i = (y * W + x) * 3; row += lum(data[i], data[i + 1], data[i + 2]);
    I[(y + 1) * (W + 1) + x + 1] = I[y * (W + 1) + x + 1] + row;
  }
  let worst = { x: 0, y: 0, m: -1 }; const n = win.w * win.h;
  for (let y = 0; y + win.h <= H; y++) for (let x = 0; x + win.w <= W; x++) {
    const m = (I[(y + win.h) * (W + 1) + x + win.w] - I[y * (W + 1) + x + win.w]
             - I[(y + win.h) * (W + 1) + x] + I[y * (W + 1) + x]) / n;
    if (m > worst.m) worst = { x, y, m };
  }
  if (worst.m <= limit) return 0;
  const meanWith = (a) => { let s = 0;                   // CSS composites the scrim in sRGB
    for (let y = worst.y; y < worst.y + win.h; y++) for (let x = worst.x; x < worst.x + win.w; x++) {
      const i = (y * W + x) * 3; s += lum(data[i] * (1 - a), data[i + 1] * (1 - a), data[i + 2] * (1 - a)); }
    return s / n; };
  let lo = 0, hi = 1;
  for (let k = 0; k < 16; k++) { const mid = (lo + hi) / 2; meanWith(mid) <= limit ? (hi = mid) : (lo = mid); }
  return Math.ceil(hi * 100) / 100;                      // > 0.5: use a plate or dark text instead
}
```

CSS for the result. The scrim sits only behind the copy, and a text-shadow does the rest:

```css
.hero { position: relative; isolation: isolate; min-height: 100svh; }
.hero > img { position: absolute; inset: 0; z-index: -2; width: 100%; height: 100%; object-fit: cover; object-position: 50% 30%; }
.hero__copy { position: relative; }
.hero__copy::before {                       /* band behind the text only; transparent well before section edges */
  content: ""; position: absolute; z-index: -1; inset: -12% -8%;
  background: linear-gradient(to top, rgb(12 14 10 / var(--scrim, .32)) 0%, rgb(12 14 10 / 0) 100%);
}
.hero__copy h1 { color: #F2F0EA; text-shadow: 0 1px 2px rgb(0 0 0 / .35), 0 0 18px rgb(0 0 0 / .18); }
```

### 3.2 Composition patterns observed on 2025–26 winners

- **Type in the image's negative space.**
  - Era Residence's wordmark sits in open sky, with the building mass in the bottom third.
  - Renaissance Edition's copy column sits in the painting's cloud gap between the two figures.
  - Direct at the shoot or render stage: leave a clean sky or wall zone of at least 35% of the frame on the side where the type will go **(rec.)**.
- **Object in front of type.** Oryzo layers giant type, then the product, then the UI. The object covers 1–2 letters and the word stays readable. Keep occlusion under about 25% of a word's letters **(rec.)**.
- **Scale contrast.** Viewport-wide display type is paired with a small image (Era: roughly 20:1 in width). Or a full-bleed image is paired with small, precise captions.
- **Page color sampled from the image.** Era's sky blue, Son Daven's sand, Oryzo's cork brown. It makes the image boundary disappear. The law reaches the same end with a cyanotype example: "a cyanotype's own blue became the page's blue: zero seams".
- **Cut-out subject bleeding into the page.** Era's sky-masked building corner rises from the section edge.
- **Patterned image edges instead of hard crops.** Son Daven's bar-pattern dissolve. Use a mask or clip shape drawn from the brand's motif.
- **Image as texture inside type or through type.** Still's aperture shows the product through the wordmark. See §3.3 for the recipe and limits.

### 3.3 Image inside type

- Use it once, as the signature. It needs heavy, large type (≥ 8vw display, weight ≥ 700) and an image with a narrow tonal range, so every part of every letter passes 3:1 against the page **(rec.)**.
- webstatus.dev lists `background-clip: text` as **Limited availability** (Chrome since 2023-12, Safari since 2020; Firefox not listed) ([webstatus](https://webstatus.dev/features/background-clip-text)). Ship the `-webkit-` form with a solid-color fallback:

```css
.word-image { color: var(--ink); }                      /* fallback: solid, readable */
@supports ((background-clip: text) or (-webkit-background-clip: text)) {
  .word-image {
    background: url("/img/cork-macro-1600.avif") 50% 50% / cover;
    -webkit-background-clip: text; background-clip: text;
    color: transparent;
  }
}
```

- For an aperture *through* a wordmark (Still), use an SVG `<mask>` or an inline-SVG `clip-path: url(#aperture)` on the image layer, with the wordmark as real text for assistive tech.
- Don't pour a gradient into type (law), and don't put grain on more than one word (law).

---

## 4. Production pipeline

### 4.1 Sourcing: pick per asset, in this order (rec.)

| Source | Use when | Winner evidence | Rules |
|---|---|---|---|
| Own shoot / commissioned photography | Real people, places, food, and products that exist | White Desert (expedition photography); Hearst (archive covers) | Shoot to the image bible; plan type zones; shoot plates for masks (clean sky, clean wall) |
| Commissioned 3D renders (Blender, Houdini/Redshift, C4D) | Unbuilt, impossible or configurable products; controlled heroes | Era Residence, Son Daven (arch-viz); Oryzo (Houdini + Redshift) | Same HDRI or light rig, lens and camera height across the set; render passes (beauty, shadow, alpha) for web compositing |
| Scans / photogrammetry | Material truth, real objects in 3D | Oryzo: ~180 photos → RealityScan mesh for the cork; a purchased hand scan ([part 2](https://blog.lusion.co/oryzo-bts-part-2-7-3d-design-and-motion-graphics)) | Clean in ZBrush; bake to textures |
| Licensed stock | Budget-limited supporting imagery | Juror warning: "stock-grade imagery" costs Content ([hontran.dev](https://www.hontran.dev/blog/awwwards-judging-criteria)) | Only whole series by one photographer; re-crop and re-grade to the LUT; never the hero; check web + social + paid usage in the licence |
| AI generation | Mood and composition exploration; painted or surreal base plates; jokes | Renaissance Edition (AI foundations + human finishing); Oryzo (Midjourney mood only) | §1.13 rules; composite with own assets; never people, products or real places presented as real; disclose where trust matters |
| Hand illustration | Warmth, abstract services, "made by a person" signal | MindMarket; Oryzo (Procreate, zero AI) | One style, one line weight, a limited palette sampled into UI tokens |

### 4.2 Motion assets

- **Rive** (`.riv` on Oryzo, Renaissance and MindMarket) handles character and UI animation.
- **Lottie** appears on Era Residence.
- **Theatre.js** gave Renaissance designers timeline control ([RGD](https://rgd.ca/hiring-designers/award-winners/2026-in-house-award-winners/the-renaissance-edition)).
- Prefer Rive or Lottie over video for flat illustrated motion, because they are vector and themeable **(rec.)**.

### 4.3 The image bible: one page, decided before sourcing (rec.)

| Axis | Decide | Example |
|---|---|---|
| Key light | Direction and quality | "Hard sun from camera-left 30–45°, late morning" / "Overcast, soft, no hard shadows" (Son Daven) |
| Color temperature and grade | One LUT for everything | Cold polar, lifted blacks (White Desert); Mediterranean saturated sky (Era) |
| Lens / focal length | A range | Documentary 24–35 mm; product 85–100 mm equivalent; the same in 3D cameras |
| Camera height | Fixed per series | Product at 15° above the object; architecture at eye level (1.6 m) |
| Crop ratios | 2–3 only | 4:5 portrait cards, 3:2 inline, 21:9 bleed; mobile re-crops defined per hero |
| Negative space | Where type goes | "Top 35% clean sky on every hero" |
| Accent | The one saturated element, inside the image | Orange parka (White Desert); coral bench legs (Floema) |
| Surface tokens | Sampled from the graded set | Page, ink and accent hex values taken from the images |
| Treatments | 0–1 global treatment | "Grain on substrates only; no duotone"; or "halftone on archive images only" |
| Banned | Explicit list | Radial halos, glossy default plastic, AI people, teal-orange grade |

Review every final asset one at a time at full resolution against this sheet, not as a contact-sheet montage (house QA practice).

### 4.4 Still formats, sizes and delivery

Support data was pulled 2026-09-24 from caniuse feature JSON (commit 2026-09-24) and webstatus.dev.

| Format | Support | Use |
|---|---|---|
| AVIF | 95.35% global full; Chrome 85+, Firefox 93+, Safari 16.4+ (16.1 partial), iOS 16+. Baseline widely available since 2026-07-25 ([caniuse](https://caniuse.com/avif), [webstatus](https://webstatus.dev/features/avif)) | First `<source>` for photos and renders |
| WebP | 96.74% global; Safari 16+ full ([caniuse](https://caniuse.com/webp)) | Second `<source>`; also alpha stills |
| JPEG XL | **Conflicting.** caniuse lists Chrome 155+ and Firefox 158+ as supported and Safari 17+ as partial. webstatus.dev still shows Limited (Safari only) ([caniuse](https://caniuse.com/jpegxl), [webstatus](https://webstatus.dev/features/jpegxl)) | Don't depend on it; at most an extra first source |
| JPEG / PNG | Universal | `<img src>` fallback |

**Encoding (sharp 0.35.4 defaults: AVIF `quality 50, effort 4, chromaSubsampling '4:4:4', bitdepth 8`; WebP `quality 80, effort 4`, per the [sharp docs](https://sharp.pixelplumbing.com/api-output)):**

```js
import sharp from "sharp";                 // 0.35.4
const widths = [640, 960, 1280, 1600, 2400, 3200];
for (const w of widths) {
  const base = sharp("src/hero.tif").resize({ width: w, withoutEnlargement: true });
  await base.clone().avif({ quality: 50, effort: 6 }).toFile(`dist/hero-${w}.avif`);  // raise quality for grain or dark gradients
  await base.clone().webp({ quality: 78, effort: 6 }).toFile(`dist/hero-${w}.webp`);
  await base.clone().jpeg({ quality: 80, mozjpeg: true }).toFile(`dist/hero-${w}.jpg`);
}
```

For dark renders with smooth falloff, test `bitdepth: 10` to avoid banding **(unverified: check decode in Safari and Firefox)**, or add grain (§2.3).

**Art-directed responsive hero.** Use real re-crops per breakpoint, not only resizes:

```html
<link rel="preload" as="image" fetchpriority="high"
      imagesrcset="/img/hero-p-800.avif 800w, /img/hero-p-1200.avif 1200w" imagesizes="100vw"
      media="(max-width: 767px)" type="image/avif">
<picture>
  <source media="(max-width: 767px)" type="image/avif" sizes="100vw"
          srcset="/img/hero-p-800.avif 800w, /img/hero-p-1200.avif 1200w" width="1200" height="1600">
  <source media="(max-width: 767px)" type="image/webp" sizes="100vw"
          srcset="/img/hero-p-800.webp 800w, /img/hero-p-1200.webp 1200w" width="1200" height="1600">
  <source type="image/avif" sizes="100vw"
          srcset="/img/hero-1600.avif 1600w, /img/hero-2400.avif 2400w, /img/hero-3200.avif 3200w">
  <source type="image/webp" sizes="100vw"
          srcset="/img/hero-1600.webp 1600w, /img/hero-2400.webp 2400w, /img/hero-3200.webp 3200w">
  <img src="/img/hero-1600.jpg" width="3200" height="1800" fetchpriority="high"
       alt="Five climbers crossing a blue ice wall under an overcast sky">
</picture>
```

Delivery rules:

- **LCP.** Candidates include `<img>`, `<image>` in SVG, `<video>` (poster or first frame, whichever comes first) and `url()` background images ([web.dev LCP](https://web.dev/articles/lcp)). `fetchpriority` is Baseline newly available since 2024-10-29 ([webstatus](https://webstatus.dev/features/fetch-priority)). Never `loading="lazy"` on the LCP image.
- **Placeholders.** Since Chrome 112, images under 0.05 bits per displayed pixel are ignored as LCP candidates. Blurry placeholders don't count, and the real image's arrival becomes the LCP ([Chromium changelog](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/speed/metrics_changelog/2023_04_lcp.md)).
- **Below the fold:** `loading="lazy"` (Baseline widely available since 2026-06-19, [webstatus](https://webstatus.dev/features/loading-lazy)) and `decoding="async"`. `sizes="auto"` is still **Limited** (Chrome 2024-06, Firefox 2026-04, no Safari) ([webstatus](https://webstatus.dev/features/sizes-auto)), so write real `sizes`.
- Always set `width`/`height` (or `aspect-ratio`) to prevent CLS. `<source width height>` for art-directed crops is in the HTML spec **(exact browser versions unverified)**, so also set `aspect-ratio` per breakpoint in CSS.
- `image-set()` for CSS backgrounds is Baseline widely available since 2026-03-18 ([webstatus](https://webstatus.dev/features/image-set)). Prefer `<img>`/`<picture>` for anything meaningful (it gets alt text and gives better LCP discovery).
- 3D textures: KTX2 (Basis) and compressed `.glb`, as observed on Renaissance. Details are in the 3D research file.

### 4.5 Video: loops, posters, alpha

**Codec support ([caniuse](https://caniuse.com/av1)).**

- AV1: 80.4% full plus 14.6% partial. Safari only decodes AV1 on devices with a hardware decoder (e.g. iPhone 15 Pro, M3).
- HEVC: full in Safari; partial or hardware-dependent in Chrome 107+.
- WebM: 96% overall, but Safari **does not support alpha transparency** in WebM ([caniuse WebM](https://caniuse.com/webm)).

**Loop encoding.** Starting points **(rec.)**; web.dev's reference commands use CRF 25 for H.264 and CRF 41 for VP9 ([web.dev](https://web.dev/articles/replace-gifs-with-videos)):

```bash
# H.264 fallback, 1080p, no audio, fast start
ffmpeg -i master.mov -an -vf "scale=1920:-2" -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p -movflags +faststart hero-1080-h264.mp4
# AV1 primary (needs an ffmpeg build with libsvtav1)
ffmpeg -i master.mov -an -vf "scale=1920:-2" -c:v libsvtav1 -preset 6 -crf 35 -pix_fmt yuv420p -movflags +faststart hero-1080-av1.mp4
# Poster = the first frame, so the static state matches frame 0
ffmpeg -i hero-1080-h264.mp4 -frames:v 1 hero-poster.png   # then encode to AVIF with sharp
```

```html
<video class="loop" autoplay muted loop playsinline preload="metadata"
       poster="/v/hero-poster.avif" width="1920" height="1080" aria-hidden="true">
  <source src="/v/hero-1080-av1.mp4"  type='video/mp4; codecs="av01.0.08M.08"'>
  <source src="/v/hero-1080-h264.mp4" type='video/mp4; codecs="avc1.640028"'>
</video>
<button class="loop-toggle" type="button">Pause background video</button>  <!-- WCAG 2.2.2 for loops >= 5 s; label changes, no aria-pressed -->
```

```js
const v = document.querySelector("video.loop"), btn = document.querySelector(".loop-toggle");
const rm = matchMedia("(prefers-reduced-motion: reduce)");
if (rm.matches) { v.removeAttribute("autoplay"); v.pause(); }                 // poster stays
let userPaused = rm.matches;
btn.addEventListener("click", () => { userPaused = !v.paused; userPaused ? v.pause() : v.play().catch(() => {});
  btn.textContent = userPaused ? "Play background video" : "Pause background video"; });
new IntersectionObserver(([e]) => { if (userPaused) return;
  e.isIntersecting ? v.play().catch(() => {}) : v.pause(); }).observe(v);  // don't decode off-screen
```

Other video rules:

- Long or high-bitrate film: use adaptive streaming (HLS/DASH) through a video host. Oryzo loads an `.m3u8`; White Desert uses Cloudflare Stream.
- Precise sync to video frames: `requestVideoFrameCallback()` is Baseline newly available since 2024-10-29 ([webstatus](https://webstatus.dev/features/request-video-frame-callback)).

**Alpha (transparent) video.** HEVC-with-alpha must come **first** because Safari supports VP9 but not VP9 alpha. VP9 alpha comes second for Chrome and Firefox ([Jake Archibald](https://jakearchibald.com/2024/video-with-transparency/)):

```html
<video playsinline muted autoplay loop poster="/v/flowers-poster.avif">
  <source type="video/quicktime; codecs=hvc1.1.6.H120.b0" src="/v/flowers-hevc.mov">
  <source type="video/webm; codecs=vp09.00.41.08" src="/v/flowers-vp9.webm">
</video>
```

- VP9 alpha: `ffmpeg -i frames/%04d.png -c:v libvpx-vp9 -b:v 0 -crf 25 -pix_fmt yuva420p out.webm` ([ben.terhech.de](https://ben.terhech.de/posts/2025-02-02-transparent-video-safari.html)).
- HEVC alpha needs macOS VideoToolbox or Compressor, and is roughly 3× the VP9 size in Archibald's test.
- The smallest option is Archibald's [stacked-alpha-video](https://github.com/jakearchibald/stacked-alpha-video): AV1 or HEVC with alpha stored as the bottom half, composited in WebGL.
- **Observed risk.** Era Residence lists `.webm` before `.mov`, so Safari would pick the VP9 file and lose alpha **(not tested in Safari)**.

---

## 5. Failure modes (checklist for review)

### 5.1 Performance and delivery

1. **Media bloat.** In five scroll steps, probes recorded 25.6 MB of WebM on Era Residence, 19.6 MB of WebP on Son Daven and 24.2 MB of MP4 on Siena (§1.4). Winners get away with it; your client's mobile users won't. Budget per viewport, and lazy-load and stream the rest.
2. **GL pages that choke weak GPUs.** Renaissance and Son Daven screenshots timed out (30 s) after the first frame under software WebGL. That is a hint, not proof, of main-thread or GPU load on low-end devices. Profile on a mid-tier Android.
3. **LCP mistakes.** A lazy-loaded hero; a hero discovered late through a CSS background or JS-injected image; a low-entropy placeholder mistaken for the LCP; video with no poster.
4. **Wrong source order for alpha video** (Safari loses transparency). HEVC goes first.
5. **ShaderMaterial without `colorspace_fragment`** gives washed-out or dark planes that don't match the DOM image they replace.
6. **Missing CORS** on the image CDN: WebGL textures fail, and so do canvas contrast checks.

### 5.2 Content visibility and access

7. **Images hidden until a reveal fires** (opacity 0 or `clip-path: inset(100%)`). This is the law's invisible-content trap. Start visible (§2.7).
8. **Content behind an ENTER gate or an endless preloader.** The Siena probe saw only the gate (document height 900 px) through all 5 scroll steps.
9. **Hover-only information** (distortion reveals, cursor trails, preview videos) with no touch or keyboard path.
10. **Autoplay loops ≥ 5 s with no pause control** (WCAG 2.2.2). No `prefers-reduced-motion` handling: 6 of 7 probed winners had zero CSS rules for it.
11. **Background-image photos with meaning but no text alternative.** Use `<img alt>`, or `role="img"` plus `aria-label` for CSS-only art such as halftone.

### 5.3 Art direction

12. **Mixed light and grade across a set** (stock + AI + renders): the page stops reading as one world. Enforce the image bible.
13. **White display type over a pale subject** (White Desert "ANTARCTICA"), or captions over bright snow or sky. Measure (§3.1).
14. **Scrims that end at the section boundary** create a hard band at the seam (law). Fade before the edge.
15. **Hard image seams**: full-bleed photos butting into flat sections. Use the feathered mask (§2.7).
16. **Default arch-viz or product lighting**: centered radial halo, glossy plastic, orbit hero (law). Use a directional key and a believable environment.
17. **AI tells** (§1.13), and AI people or products presented as real.
18. **Grain over text, faint grid lines over photos, botched glass** (law). All three were observed on or near 2026 winners (White Desert column lines, frosted cards).
19. **Cream or UI-grey page surfaces by default.** Several winners use cream (Siena `#FAF7EF`, Renaissance `#F7F7EE`), but the law flags it. Sample the surface from the imagery instead.
20. **Commodity effects as the concept**: dither, ASCII, liquid hover or cursor trail with no link to the brand. One signature, tied to the idea, or none.
21. **Flat fill after the hero.** Carry imagery or texture down the page (law).
22. **Over-banded dark gradients and renders** from low-bitrate encodes. Add grain, raise quality, or test 10-bit.

---

## Retrieval gaps

- **`/websites/illustration/` listing returned HTTP 429** on 2026-09-24, so illustration-tag cadence is uncounted. Illustration shares come from corpus detail tags only.
- **Awwwards tags are submitter-chosen** and listing cards truncate them. Archetype shares are lower bounds, and some sites carry photos or renders with no media tag. The "months" for SOTM entries are inferred from listing order; SOTD dates are exact.
- **Probe coverage.**
  - Renaissance Edition and Son Daven screenshots timed out after the first frame under software (SwiftShader) WebGL.
  - Floema and White Desert shots are partly covered by consent banners, because the probe never clicks.
  - Siena stayed behind its ENTER gate.
  - MindMarket completed only 2 of 5 steps.
  - No mobile captures (`--no-mobile`). Byte totals are declared `content-length` during a 5-step scroll, not full-page weight.
- **Not verified in Safari:** Era Residence's alpha-video source order, 10-bit AVIF decode, AVIF grain smearing at quality 50, and `<source width/height>` version support.
- **JPEG XL support is contradictory** between caniuse (Chrome 155+, Firefox 158+) and webstatus.dev (Safari only). It was not resolved against Chrome or Firefox release notes.
- **`background-clip: text`:** webstatus.dev lists no Firefox implementation. This was not cross-checked with MDN browser-compat data.
- **Lusion's Oryzo BTS parts 4–7** (WebGL implementation) were not published or reachable. Only parts 1–3 were read.
- **Renaissance Edition's AI tooling** (which model, which prompts) is not disclosed in the RGD or One Club write-ups. Only "AI generated each artwork's foundations" is documented.
- **No official Awwwards statement on AI-generated imagery in judging was found.** The terms and FAQ mention plagiarism and templates but not AI. The jury perception here is one young-jury member's essay plus practitioner blogs.
- **Consumer-trust figures come from Getty (2022–2024 fieldwork, 2024 report) and a 2026 interview.** No 2026 primary Getty report was retrieved.
- **ffmpeg CRF and preset values** for AV1 and H.264 loops, and the scrim/occlusion/budget numbers marked (rec.), are working recommendations, not benchmarked results.
- **The Codrops/Adoratorio 2025-10-08 tutorial was only partially extracted** (the page was truncated). The DOM-sync recipe here was written against three.js 0.186.1 docs and was not run in a browser for this document.
