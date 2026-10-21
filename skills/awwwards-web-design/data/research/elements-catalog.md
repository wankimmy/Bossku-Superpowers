# Awwwards Elements: breadth catalog of motion patterns

Last updated: 2026-09-24

Scope: a pattern taxonomy built from 43 recent Awwwards Element videos across 8 categories. Each one was frame-sampled and timed. The file lists what recurs, how to build each pattern, the numbers behind it, and where a pattern collides with the house anti-slop law (`deslop-law.md`, which wins). Use it to pick a pattern and build it. It is not a gallery.

---

## 0. Read this first: what the Elements library is (and is not)

- **Elements are uploaded by the people who submitted the site, not picked by the jury.** The Awwwards FAQ tells submitters to "personalize" a submission by "selecting the specific parts of your website you want to showcase". It adds that "the more elements you include, the better visibility", recommends videos, and gives 1600x1200px as the ideal size ([Awwwards FAQ](https://www.awwwards.com/faqs/)). The index page calls itself "100s of examples of forms, great UX/UI, footers, transitions and much more" ([Elements index](https://www.awwwards.com/elements/)). So an element's presence in the library is not a quality signal.
- **The jury signal is the parent site's award status.** An Honorable Mention needs a jury score of 6.5 or more *and* a user score of 6.5 or more, and a site stays eligible for Site of the Day for up to 3 months after approval ([Awwwards FAQ](https://www.awwwards.com/faqs/)). The 43 sampled elements come from **28 parent sites**. On 2026-09-24 the page titles showed **3 SOTD** (Warm & Fuzzy, Cerebrium, Noho) and **25 Nominee** (see the evidence index). Most of these were submitted in Aug–Sep 2026, so their status can still change.
- **An award does not validate every element on the site.** The Cerebrium dropdown ([E11]) sits on a SOTD site and still shows three slop tells from the house law: a saturated magenta CTA, icons in tinted tiles, and monospace as the house voice. Judge each element on its own merits.
- **Presentation bias.** All 43 clips are 4:3. Forty are exactly 1600x1200 (measured with ffprobe), which matches the FAQ's recommended size. Many are recorded inside a fake browser chrome or on a blurred chromatic backdrop ([E3], [E8], [E15]). The frame is presentation, not the site: do not copy it. A fake macOS window used as a UI element is itself a slop tell in the house law.
- **Library composition (observed 2026-09-24).** I parsed the first page of 20 category pages: 568 unique elements, 63% of them video. Tags are optional and self-declared, so the counts below are lower bounds. WebGL, three.js, shader or WebGPU appear on 72 elements. "3d" appears on 58, typography or text reveal on 50, "gsap" on 16, Lottie or Rive on 12, and matter.js, physics or gravity on 7. Only 3 elements mention view transitions or Barba.

### Method (so you can trust or discount the numbers)

- **Sources.** Category pages were fetched on 2026-09-24 with a desktop User-Agent: loading, menu, navigation, transition, mouse_interaction, interaction, gallery, products, footer, header, scroll, hero_image, animation, thumbnail, layout, 404_page, photo and video. Each card embeds a `data-collectable-model-value` JSON (title, tags, `main_image` = mp4) plus an `/inspiration/<slug>` link.
- **Frames.** `scripts/element_frames.py --frames 6` produced 6 evenly spaced frames per clip. For short bursts I added 4–6 dense frames. I reviewed every frame individually and in order, never as a montage.
- **Timing.** Each clip was decoded at 30 fps and at 60 fps (160x120, greyscale). I computed the mean absolute frame difference per frame ("motion energy"). The **active window** is where energy exceeds 8% of the burst peak. **Ease shape** comes from where the energy peaks inside the window: a peak at 0–30% means the motion is front-loaded (ease-out), about 50% means symmetric (in-out), and 80–100% means it accelerates (ease-in). The limits: the recordings run at 24–60 fps, the tails of eases fall below the threshold, and cursor or scroll movement adds noise. Treat durations as ±15% lower bounds.

---

## 1. Measured timing (the numbers to reuse)

| Element | Motion | Active window | Energy peak inside window | Read as |
|---|---|---|---|---|
| [E1] Indisea loader | counter-edge curtain sweep | 0.52 s | 45% | symmetric in-out (`power3.inOut`) |
| [E1] Indisea loader | counter 050→100 | ~1.0 s | n/a (text) | count eases out (050→085 in the first 0.48 s, 085→100 in the next 0.48 s) |
| [E5] Warm & Fuzzy intro | rotating aperture expands to cover | 0.63 s | 97% | accelerating ease-in (covering exit) |
| [E7] Forge menu open | page shrinks to thumbnail, links blur in | 0.82 s | 22% | front-loaded ease-out |
| [E7] Forge menu close | thumbnail grows back to page | ~1.0 s | early spike + plateau | ease-out with long settle |
| [E14] NightKidz grid memory | shared-element morph PDP→grid cell | 1.18 s | 14% | strong ease-out (expo-like) |
| [E18] A24 Films→TV | disc flip + rule retract + title write | 1.25 s | 28% | ease-out |
| [E2] A24 preloader→hero | disc carousel builds | 1.32 s | 25% (90% of work done at 63%) | ease-out, long tail |
| [E3] NightKidz entry | site resolves (scramble + depixelate) | 1.43 s | 21% | front-loaded, stepped |
| [E16] Emotion WebGL | block-glitch scene swap | 2.03 s | 2% (decays) | burst then decay |
| [E37] Inherited intro | noise-dissolve letters | ~0.9 s | 56% | symmetric |
| [E13] A24 detail | subject-matte video rise (scroll) | ~0.9 s | 61% | scroll-shaped, symmetric |

**Rules that fall out of the measurements:**

- **Spatial moves that end on screen are ease-out.** Menus, shared elements and carousels are strongly front-loaded (peak at 14–28%). Use `expo.out`, `power3.out` or `cubic-bezier(0.16, 1, 0.3, 1)`.
- **A mask sweep that starts and ends inside the viewport is symmetric.** Use `power3.inOut` or `cubic-bezier(0.65, 0, 0.35, 1)` over 0.5–0.6 s.
- **A cover that grows past the viewport accelerates.** Use `power2.in`/`expo.in` over about 0.6 s ([E5]). Never ease-out a cover: it stalls just before the cut.
- **Durations: 0.5–0.8 s for masks and menus, 1.1–1.3 s for shared-element or 3D moves, and 2 s or less for an entire intro** in the best examples ([E1] ≈ 1.9 s including the count; [E5] ≈ 1.9 s). [E2] takes about 3.5 s before the hero, which is the upper limit.

---

## 2. Pattern taxonomy

Format per pattern: **what it is**, **evidence**, **build**, **numbers**, **why it reads premium or gimmicky**, and **house-law check** where relevant.

### 2.1 Preloader / intro

**P1. Counter-as-curtain.** A monospace counter (`050 → 085 → 100`) counts up in the bottom-left. At 100 the counter travels up the screen, and its lower edge is the top edge of a clip mask that uncovers the finished hero beneath it. The CTA pill slides up from its own mask about 0.1 s earlier. The logo and menu arrive last. Evidence: [E1]. Build: animate one variable `--edge` (100→0) with GSAP. Drive both `clip-path: inset(calc(var(--edge)*1%) 0 0 0)` on the hero and `translate` on the counter, so they cannot drift apart. Numbers: count about 1 s, sweep 0.52 s in-out. Premium because the loader's own object performs the reveal (no second "wipe" layer) and the whole thing is over in under 2 s. See recipe R1 for the progressive-enhancement version.

**P2. The product is the loader.** The loading object becomes the first piece of content. At A24 a 3D disc turns from edge-on to face-on while a Didone counter and a year odometer (`2012→2025`, digits rolling inside a clip) count. The status label reads "Projecting ↻". The disc then drops into a diagonal 3D carousel, and film metadata writes into a ruled table ([E2]). At Warm & Fuzzy a tilted square aperture spins while the showreel plays inside it, then accelerates to overscan into the full-bleed reel ([E5]). Build: a three.js disc (texture = cover art) or a CSS `clip-path: polygon()` square on a rotating wrapper with `overflow: hidden`, and `scale` to about 3.5 so the rotated corners leave the viewport. Numbers: aperture expansion 0.63 s ease-in, rotation about 15–20° between sampled frames. Premium: there is no dead time, because the wait shows the product.

**P3. Typographic progress.** App State's "we ___ are": a hairline sits between two heavy slab-serif words. As loading goes from 64% to 95% the gap closes, so progress is expressed as kerning. A small italic rust verb cycles under the words ("mixing", "guiding"), with the percentage in tiny type. At 100% the words fade to grey over a photo mosaic whose giant italic verb ("explore") keeps cycling ([E4]). Build: `column-gap: calc((1 - var(--p)) * 30vw)` on a two-item flex row, with the verb swapped every about 400 ms. The page ships a pause button (bottom right) for its looping hero, which satisfies WCAG 2.2.2: auto-starting motion that lasts more than 5 s needs a pause control ([W3C SC 2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html)). Warm & Fuzzy also ships one ([E5]).

**P4. Quantized resolve.** A giant pixel-block mosaic shrinks through 4–6 visible block sizes to a crisp katakana logotype. Then UI labels scramble from katakana to Latin ("WHEELS", "Sign in") while product images depixelate in steps ([E3]; the same system is reused in [E14] and [E22]). Build: draw to a canvas at `w/blockSize`, upscale with `imageSmoothingEnabled = false`, and step the block size 32→16→8→4→1 about every 80–120 ms (the step timing is estimated, not measured). Use stepped timing on purpose: a smooth ease breaks the pixel metaphor. Numbers: entry burst 1.43 s, peak at 21%. Premium only because it matches the brand (JDM, night-market, pixel era). On a bank site it is a gimmick.

**P5. Mark-to-logo handoff (the safe default, and a caution).** A small morphing gradient blob sits on cream. The hero video fades in over about 0.5 s, and the blob shrinks to a white dot at the logo position, then becomes the logo mark. The nav items fade in with a stagger ([E6]). It is competent but generic: a centred fade-up headline over video is the "default hero stack". House law: the cream background is a named slop tell. Use P1 or P2 instead.

**P6. Themed status microcopy.** The loader and transition status label changes verb per context: A24 uses "Projecting", "Rewinding" and "Printing" ([E2], [E13], [E18]). It costs nothing and is strongly on-brand, and it is fresher than a percentage.

**House-law check for this whole category.** Every preloader hides content until an animation finishes, which is exactly the "invisible-content trap". The only acceptable form: the loader exists **only** when JS runs **and** motion is allowed **and** this is the first visit in the session. A hard `setTimeout` failsafe must remove it, and the no-JS page must render the finished hero (R1).

### 2.2 Menu / navigation

**M1. The page becomes a thumbnail.** Opening the menu shrinks the current page into a small centred window. At Forge a `clip-path` rectangle contracts from full viewport to about 35% width, then to about 8%, over an oxblood menu layer ([E7]). At Brandon Yasin the menu is a horizontal row of real page miniatures ("cases / archive / about", about 28% scale). Clicking one zooms it to full screen ([E9]). Numbers: open 0.82 s, peak at 22% (ease-out). Close about 1.0 s: the rectangle grows from the centre, briefly shows an inset frame, then settles. Why premium: spatial continuity, because you see where the page went and where it comes back from. Build: animate the page wrapper's `clip-path: inset(a% b% round r)` and `scale` (0.96→1 settle). Do not animate width or height.

**M2. Blur-to-focus link entrance with sibling dimming.** Forge's full-screen links (condensed serif caps: BUILDS / STOCK / CONTACT) enter blurred and slightly large (about 8px blur, scale about 1.1 → 0 and 1). Hovering one drops its siblings to about 25% opacity and opens a small image window behind the centre of the text (a clip-path expanding from the centre) ([E7]). Build: `filter: blur()` plus `scale` on each link, staggered 60–80 ms. Hover dimming via `.menu:has(a:hover) a:not(:hover) { opacity: .25 }` (`:has()` has been Baseline Widely Available since 2026-06-19 ([web-features](https://web-platform-dx.github.io/web-features-explorer/features/has/))). Keep the dimmed state readable (at least 3:1 against the background for large type), or dim to a tonal step rather than opacity.

**M3. Outline to fill on stacked display type.** A language picker set as a vertical stack of big high-contrast serif words: unhovered words are outline-only (`-webkit-text-stroke`), and the hovered word fills solid. A WebGL-cloth dollar bill drifts behind ([E10]). This is a state change, not a slide, so it is the house-law-approved alternative to underline-fill hovers. Caution: outlined text at small sizes fails legibility, so use it only at 64px and above.

**M4. Glass bar that grows into a panel, with scramble labels.** A blurred glass nav bar extends downward into a white panel. Hovering an item gives it a tinted pill. Labels **scramble one or two characters** ("CASEJ", "DOCQ", "BLOC") and then resolve. Row icons invert (tile turns black) and an arrow slides in on the right ([E11], SOTD site). Keep: the single-character scramble (subtle, techy) and the arrow slide. Drop: the saturated magenta CTA, the icon-in-tinted-tile rows and the monospace house voice (all house-law tells). Recipe R8.

**M5. Physical dock entrance.** A dark ball drops into the bottom centre with a squash and a ghost trail, then stretches horizontally into a two-button dock pill ("Introduction" | "Get in touch") ([E12]). Springy overshoot (the 25 fps recording is too coarse for a curve fit). On the same load, the full-bleed hero photo shrinks into an inset rounded card while the headline rises above it. Premium: the dock arrives as an object with mass instead of fading in. Caution: the stats band below shows `00 / 000 / 0` placeholders until counters fire, which is the invisible-content trap. Ship the real numbers in the HTML and animate *from* them.

**M6. Counterexample: the static luxury overlay.** A full-screen nav in Cormorant-style serif, a gold-gradient glowing "Reserve" pill and a radial navy glow, with nothing moving ([E8]). Every visible choice here is on the house slop list (Cormorant, glowy pill, radial glow halo, and a fake macOS window frame in the recording). Include it in your mental model as "what the library also contains".

### 2.3 Page transitions

**T1. Shared-element return to the exact cell.** Going back from a product page, the product image flies from the PDP's centre column into its **exact** cell in the collection grid. Everything else cuts or resolves around it: the other grid images depixelate and labels scramble ([E14]; tags: "view transitions api", "nextjs"). Numbers: 1.18 s, peak at 14% (strong ease-out). Build: the View Transitions API. Same-document transitions are supported in Chrome 111+, Safari 18.0+ and Firefox 144+. Cross-document transitions (`@view-transition { navigation: auto; }`) are in Chrome 126+ and Safari 18.2+, with only partial support in Firefox 144–157 ([caniuse same-doc](https://caniuse.com/view-transitions), [caniuse cross-doc](https://caniuse.com/cross-document-view-transitions)). The fallback is a normal navigation, so it is safe to ship (R6).

**T2. Scroll-through next-project handoff.** At the end of a case study the next project's title and preview sit in the middle ("(Projet suivant) DAVID DIEU"). Scrolling past, the preview grows from about 45% width to full-bleed and becomes the next page's hero. The page then swaps, and the next title builds in huge grotesk ([E15]). A cursor-following "SUIVANT →" chip labels the action. Build: a ScrollTrigger scrub on the preview's `clip-path`/`scale`, then navigate at `onLeave` with a shared `view-transition-name` on the image, so the swap is seamless.

**T3. Object flip with an edge-on swap.** A24's Films → Television switch: the metadata table's hairlines retract, the carousel empties, and one disc flips on Y. At the edge-on moment its face changes to the new category's art, with the status label "Printing ↻". The disc then settles and the new title writes in with an underline being drawn ([E18]). Numbers: 1.25 s, peak at 28%. **Edge-on swap** is the transferable trick: change content while the surface is invisible (see S1 and R9).

**T4. Rules draw in, then the subject rises through the page.** On the A24 detail page, hairline rules draw in from the left at staggered lengths, like a table being ruled, while the Didone title sits centred. The trailer video then rises from the bottom with its **top edge following the silhouette of the actors' heads**, so the white page reads as a layer cut out around the subjects. Quote words scatter one per grid row across the video ("I … HAVE … A …") ([E13]). Build: the rules are `scale: 0 1 → 1 1` with `transform-origin: left`, staggered 40–60 ms. The silhouette edge needs a per-frame matte: an alpha video (WebM VP9 alpha or HEVC with alpha) layered over the page, or a canvas `globalCompositeOperation` with a matte video. The site does not document its method (unverified).

**T5. Shader block-glitch dissolve.** The Emotion Agency 3D room hero breaks into grid blocks with RGB channel split and datamosh displacement. The headline shreds into green and magenta slivers, and the new scene (a curved card carousel on a reflective floor) resolves out of the blocks ([E16]). Numbers: about 2.0 s, energy front-loaded then decaying. Build: a full-screen quad shader. Step a noise threshold per block cell over time, offset UVs per cell, sample R/G/B with different offsets, and mix `texOld`/`texNew` per cell. It belongs to brands whose identity is signal or glitch. Elsewhere it is a gimmick, and the purple glow environment trips the house law's "purple" and "radial glow" tells.

**T6. Lightbox with editor-timeline chrome.** A photographer's horizontal film strip. Clicking an image zooms it into a lightbox, and dragging moves through the set. A bottom **ruler of ticks with a red playhead** tracks position, next to a `09/09` counter. Bracketed mode toggles sit in the corners: `ZOOM:[ON] SOUND:[ON] GESTURES:[OFF]`. The last image hands off to "NEXT PROJECT O_STUDIOZA / CLIENT: ADIDAS" ([E17]). This is domain-borrowed UI (a video-editor timeline) used as navigation, and it is specific and fresh. The ticks are real, not a decorative grid.

### 2.4 Hover / cursor

**H1. Blend-mode dot.** A 12px dot, light on dark and dark on light, via `mix-blend-mode: difference`, with no lag ring and no growth ([E19]). Support: Baseline Widely Available, with Chrome 41, Firefox 32 and Safari 8 as the first versions ([web-features](https://web-platform-dx.github.io/web-features-explorer/features/mix-blend-mode/)). It works because it is tiny and exact. The big trailing ring with lerp lag is the overused version. Recipe R4 (keep the native cursor, or hide it only on `pointer: fine`).

**H2. Action-labelled cursor chip.** A small dark pill trails about 20px below-right of the pointer and names the action of whatever is under it: "CHOISIR +" over option pills, "CONTINUER →" over the next button, "ENVOYER ↗" over submit ([E23]). Buttons change state by inverting outline to filled cream, with **no lift**, which is house-law compliant. Failure mode: the chip repeats the button's own label ("CONTINUER" on a "CONTINUER" button), which is noise. Use the chip only where the target has no text: images, cards, drag areas.

**H3. Word parts to make room.** In a project index set in large italic grotesk, hovering a title splits the word at its centre. The halves slide apart and 3–4 small rotated thumbnails pop in **inside the word** ([E20], matter.js + GSAP). On scroll-in, the letters of each title arrive wobbling on arcs and settle straight. Premium: the image preview lives inside the typography instead of floating near it. Build: split the title into chars. On hover, `gsap.to(leftChars, {x: -gap/2})` and `gsap.to(rightChars, {x: gap/2})`, then insert the thumbnails absolutely positioned in the gap with a `back.out(1.7)` scale-in and ±6° rotation. Physics is optional.

**H4. Velocity chromatic split.** Hovering an image adds a faint red/cyan fringe that scales with pointer velocity. A tiny "View Project" pill follows the pointer with the same split ([E21]). The low intensity is the point: 1–3px of offset at most. Build: WebGL plane (three.js/OGL) with `uOffset = velocity * k` sampling R and B at ±offset, lerped back to 0.

**H5. Deck trail, not scatter trail.** The cursor pulls a **stack** of photos offset by about 6–8px each, like a fanned deck, instead of dropping scattered images. When the pointer stops, the deck collapses into the top card, which glitches out in horizontal pixel scanlines ([E22]). The trail is clipped to the hero section. Build: a ring buffer of N image elements. Every d px of pointer travel, move the oldest to the pointer and z-index it on top, and render with `translate` only.

**H6. The 2D accordion grid (no lift).** In a features grid, the hovered card's **row gets taller and its column gets wider** while siblings shrink. The "+" rotates to "×" and a description appears bottom-left ([E24]). The hover gives space to content instead of floating the card, which makes it the house-law-compliant replacement for the card hover-lift. Grid track interpolation (`grid-template-columns/rows`) has been Widely Available since 2025-04, with Chrome 107, Firefox 66 and Safari 16 as the first versions ([web-features](https://web-platform-dx.github.io/web-features-explorer/features/grid-animation/)). Recipe R5. House-law note: in the original the description exists only on hover. Show a one-line teaser by default and let hover or focus expand it.

**H7. Packshot to lifestyle swap.** On a watch PLP, hovering a card cross-fades the packshot to an on-wrist photo (about 0.3 s, mid-blend visible in the frames). The card also carries a mono spec tag ("+1.5MM AUTOMATIC") and hairline-separated meta rows: model/price, edition, colourway dots ([E29]). Restrained and correct for e-commerce. Do not add a zoom as well.

**H8. Lens distortion on artwork.** On an infinite canvas of paintings, hovering an artwork applies a local radial warp and refraction under the pointer ([E27]). Build: a WebGL plane per image, with the fragment shader displacing UVs by a radial falloff around `uMouse`.

### 2.5 Gallery / slider / product

**G1. Scroll fisheye column.** One narrow vertical column of image slices. The slice at the viewport centre is full size (about 250x240px in the recording), and slices get **shorter and narrower** with distance from the centre, down to about 50px strips. Images crop with `object-fit: cover` and never squash ([E26]). Build: a pinned stage with a wheel layout driven by scroll progress (R7). Do not animate `height` in document flow with a view timeline: every height change moves every later item and feeds back into the timeline. Failure seen in the clip: the column scrolls *under* the nav labels (collision).

**G2. Infinite drag canvas with real silhouettes.** A 2D grid you drag in any direction. It wraps infinitely and decelerates with inertia (about 1.3 s) into a centred grid. The artworks keep their real non-rectangular shapes (triangles, diamonds). There is a grid/column view toggle, and captions (title + series) sit under each piece ([E27]). Build: absolutely positioned tiles, `translate` = `((i*cell + offset) mod total)`, velocity decay about 0.92 per frame, then snap.

**G3. A ring of titles around a WebGPU object.** A central stone monolith in a foggy landscape carries the active project's image as marbled strata. Project names in extra-bold wide grotesk caps sit on a curved horizontal ring: the active one filled, neighbours outlined and fading around the curve. On change, letters flip between outline and fill one by one with an ink-noise dissolve, and the whole scene's colour grade shifts per project: red, teal, green ([E25]). Build: three.js `WebGPURenderer`, which uses WebGPU when available and falls back to a WebGL 2 backend (`import * as THREE from 'three/webgpu'`, `await renderer.init()`) ([three.js docs](https://github.com/mrdoob/three.js/blob/dev/docs/pages/WebGPURenderer.html)). WebGPU is on by default in Chrome 113+ and Safari/iOS 26, partial in desktop Safari 26, and disabled by default in Firefox through 157 ([caniuse](https://caniuse.com/webgpu)). Design for the fallback. The title ring can be HTML with `transform: rotateY()` on a cylinder (`translateZ(r)`), which keeps it selectable and indexable.

**G4. Split-screen 3D product compare.** Two chairs side by side, each a rotatable 3D model. The drag handle is a circular cursor with "‹ ›". Colour swatches change the model's material (the seat cushion colour), and a "+" opens a vertical swatch rail. "Learn more" makes that product's half take over the frame (a split-pane resize), revealing a testimonial and an image slider with a circular "Next" cursor ([E30], SOTD site). Build: `<model-viewer>` (4.3.1, Apache-2.0 on npm as of 2026-06-04) or three.js with a `GLTFLoader` and `material.color.set()`. The pane takeover is a `grid-template-columns` transition (see H6).

**G5. Luxury-default parallax reveal (caution).** Scroll-linked blur-to-sharp words, an image parallaxing inside its frame, giant ghost outline type at about 5% opacity behind the sections, a rotating circular-text seal, letterspaced serif caps, a script name, and navy + gold ([E28]). Each part is common and several are house-law tells: the letterspaced serif wordmark, and a rotating badge with no function. Parallax *inside* a frame (image translate at about 0.85x) is the one move worth keeping.

**G6. Curved 3D card carousel on a reflective floor.** Cards on a cylinder segment with glowing rims and floor reflections ([E16]'s destination scene). It is common in 3D portfolios, and the glow rims plus purple fail the house law. If you use the cylinder, drop the glow and the reflections and let the cards' content carry it.

### 2.6 Footer

**F1. Breakable wordmark, with repair.** The footer's giant logotype sits flush on the bottom edge, as the house law's "wordmark placed right" requires. A cursor chip says "CASSER" (break). Clicking turns the letters into rigid bodies that fall and tumble. You can grab ("SAISIR") and throw them, and a "RÉPARER" (repair) chip tweens them back into the wordmark ([E31]; also [E20]). The repair action makes it premium: the toy is reversible, so the brand mark is never left broken. Recipe R10 (matter.js 0.20.0, MIT, last published 2024-06-23 per the npm registry).

**F2. Curtain reveal with a letter colour wake.** The content slides up off a fixed footer beneath it. The wordmark's letters arrive at staggered baselines and settle. Hovering lifts nearby letters about 10px and tints each **with one of the product's colourways** (olive, sage, lilac, tan, rust, yellow), and the tint decays after the pointer leaves ([E33], SOTD site). Premium: the palette *is* the product line, so the interaction is brand-specific. It is not random colour.

**F3. Generative modular wordmark.** The footer name is built from modular geometric pieces (bars, quarter circles) that slowly and continuously rearrange inside each glyph ([E34]). Build: a custom SVG glyph system with cells whose pieces tween between presets. Or a variable font with custom axes (unverified whether the site uses one). If it loops more than 5 s it needs a pause control (WCAG 2.2.2) unless it stops on its own. Surrounding tells to avoid: the purple gradient header and pill chips.

**F4. Text on a path that ends in an orb.** A sentence travels along a curved path driven by scroll (SVG `<textPath>` with `startOffset` scrubbed), coloured by a gradient along the path. The final period becomes a dot that grows into the grainy footer card ([E35]). The mechanic is good. The orange→purple→red gradient and the purple footer are house-law tells ("purple / blue-to-purple gradients"). Use a tonal ramp from the brand's own ink.

**F5. Typed tagline with a glowing pill (counterexample).** "Work, Hone, Play." types in word by word (about 0.4 s cadence) beside the logo. A full-width white "Get in touch" pill has a rotating red/blue conic glow ([E32]). The glowy pill button is on the house slop list. The word-by-word type is fine.

### 2.7 Text / typography reveal

**X1. Scroll-scrubbed letter rise with a ragged baseline and read-state dimming.** Condensed bold caps. Each letter rises from below its own line mask, scrubbed by scroll rather than time, and **letters within a line sit at different heights mid-rise**, giving a ragged, wave-like baseline. Lines you have already scrolled past **dim to light grey** while the current lines stay dark. A giant section word ("SKILLS") sits at about 4% ink behind the content ([E36]). The dimming is the reusable idea: it marks reading progress **without ever hiding text before you reach it** (R3b).

**X2. Noise-dissolve letters composed around the subjects.** A band name forms from grainy vertical strokes that dissolve into distressed letters. The letters are **placed in the gaps between the members' heads** ("IN · HE · RI · TED"), and a small offset "I" nudges up. Genre words then type in ([E37]). On the member pages, names materialise from noise and roles stagger in with ragged indents ([E39]). Premium: the layout comes from the photograph, and the type is spaced to leave the faces clear.

**X3. Blur-from-depth word build.** A headline assembles word by word. Each word arrives larger and blurred (as if from nearer the camera) and settles sharp: roughly `scale 1.2→1`, `blur(10px)→0`, staggered about 120 ms ([E40]). Scrolling blurs the hero out and builds the next statement the same way. It is overused as a generic fade-in. It works here because the serif is high-contrast and the pacing reads like a film title card.

**X4. Text flowing around a 3D subject.** A holographic point-cloud figure stands centre. Two columns of small uppercase lines scroll past, **wrapping around the figure's silhouette** line by line (left column right-aligned to the figure's left contour, right column left-aligned to its right contour), framed by HUD side panels ([E38]). The same family: [E13] (quote words around heads), [E37] (letters between faces). For a static silhouette, use CSS `shape-outside: url(matte.png)` with `shape-image-threshold`. It is Widely Available (Chrome 37, Firefox 62, Safari 10.1) ([web-features](https://web-platform-dx.github.io/web-features-explorer/features/shape-outside/)), and only floats wrap around it. For a moving figure, measure each line against the projected silhouette per frame in JS.

**X5. Masked line rise (the baseline technique).** Lines slide up from their own clip masks with about 80 ms stagger. The midpoint frame shows each line cut at the mask ([E9]). This is the most common text reveal in the sample. GSAP's SplitText (free since 3.13, including commercial use, [GSAP 3.13 release](https://gsap.com/blog/3-13/)) has a built-in `mask: "lines"` wrapper with `overflow: clip`, and `autoSplit` re-splits when fonts load or the width changes ([GSAP SplitText docs](https://gsap.com/docs/v3/Plugins/SplitText)). R3a.

### 2.8 Scroll storytelling

**S1. Pinned device with an edge-on content swap.** Three phones in the hero. On scroll the centre phone travels right, **rotates 90° until edge-on** (you see only the orange frame), then turns back with a different screen. It stays pinned while steps 1–3 change on the left, with a vertical dot/line indicator and inactive steps dimmed ([E42]). The swap happens when the screen has no visible area, so the content change is never seen. R9.

**S2. A scroll-rotated monogram that composes the type.** A 3D-extruded monogram spins on Y with scroll. The name text tilts back in perspective and recedes. At the edge-on angle the monogram becomes a thin vertical bar that **divides "art director" (low left) from "creative developer" (high right)** ([E41]). Premium: each rest angle of the object produces a composed layout. Tell: the animated orange/pink/purple mesh gradient behind it is the "candy aurora" on the house slop list.

**S3. Aperture zoom: inset frame to full-bleed.** An image sits inset in the viewport (about 35px margins or a smaller rectangle) and grows to full-bleed as you scroll, while the image inside counter-scales so the crop stays calm ([E40], [E39], [E12]). This is the single most repeated mechanic in the sample: clip-path apertures and masks appear in at least 9 of 43 clips. R2 (pure CSS scroll-driven, with a feature-query fallback).

**S4. Pinned glass panel over a zoom-blur sequence.** A frosted panel holds a pinned italic display title ("MANIFESTO"). Full-bleed photos behind it change with a radial zoom-blur, and the body sentence swaps per step with a blur cross-fade ([E43]). Build: a WebGL radial blur (sample along `uv - center` N times, weighted) with the strength peaking mid-transition. The panel makes the text readable over any frame.

**S5. Colour block before image.** In the band-member sequence, a solid red block wipes in *before* the photograph appears in that block. Extreme close-ups alternate with medium shots in inset frames, all in a strict two-colour system: red and black, with cream type ([E39]). The block-first reveal gives the eye a shape to track, and the colour constraint makes a busy sequence read as one system.

**S6. Progress you can read.** A hairline scroll-progress bar in the bottom-left ([E40]), the step indicator in [E42], the editor timeline in [E17] and read-state dimming in [E36]. The best sites show *where you are* in the story instead of adding a generic "scroll" hint.

---

## 3. Cross-cutting observations

**What recurs (frequency in the 43 samples, from direct viewing):**

1. **Clip-path apertures and masks as the reveal primitive** (curtains, rotating apertures, menus, inset to full-bleed, subject mattes): about 9 clips ([E1], [E5], [E7], [E9], [E12], [E15], [E39], [E40], [E13]). Cheap and GPU-friendly, and they read as editing (a "cut"), not decoration.
2. **Type interacting with a subject or object**: letters between faces, lines wrapping a figure, a word opening to hold thumbnails, a monogram dividing two phrases ([E13], [E20], [E37], [E38], [E41]). This is where the freshest work is.
3. **Blur as a transition material** (blur-to-focus links, words from depth, zoom-blur): [E7], [E28], [E40], [E43]. Very common. It is a generic fade unless the pacing is authored.
4. **Scramble, dither and pixel vocabulary**: [E3], [E11], [E14], [E22]. On-trend. The tag counts show ascii, pixel, dither or bitmap on 9 of 568 elements.
5. **Physics toys (matter.js)**: [E20], [E31] in the sample, 7 tagged across the library. They work when reversible and on-brand ([E31] repair, [E33] palette).
6. **Hairline rules and ruled tables as structure**: A24 metadata ([E2], [E13], [E18]), Unimatic meta rows ([E29]), the editor ruler ([E17]). The rules carry information. They are not decoration.
7. **Themed microcopy and status labels**: "Projecting / Rewinding / Printing" ([E2], [E13], [E18]), "CASSER / RÉPARER" ([E31]), "ZOOM:[ON]" ([E17]).

**What is overused (seen 3+ times, usually generic):**

- Purple/magenta gradients and glow environments ([E16], [E34], [E35], [E41], [E11]). House law: slop.
- Glowing pill CTAs ([E8], [E32]) and saturated single-accent buttons ([E11], [E24]'s red "+" buttons). House law: slop (saturated accent, glowy pill).
- Cream "editorial" backgrounds ([E1] loader, [E6], [E20], [E26]). House law: slop.
- Centred headline over full-bleed video with a staggered nav fade ([E6], [E28]).
- Counters starting at zero that hold placeholders ([E12] stats).
- Generic blur-fade on every block ([E28]).

**What felt freshest (build these first):**

- **The page as a thumbnail menu** ([E7], [E9]): spatial memory instead of an overlay.
- **Shared-element return to the exact grid cell** ([E14]): platform API, tiny code, big payoff.
- **Edge-on swaps** ([E18], [E42], [E41]): content changes when the surface is invisible.
- **Typographic progress** ([E4]): the loader is layout, not a bar.
- **Read-state dimming** ([E36]): progress without hiding content.
- **Reversible physics** ([E31]) and **brand-palette wakes** ([E33]).
- **Borrowed professional UI** as navigation: the video-editor ruler ([E17]), film metadata tables ([E13]).

**Premium vs gimmicky: the recurring discriminators.**

| Premium when… | Gimmicky when… |
|---|---|
| the moving object *is* content (disc, reel, page thumbnail) | a separate decorative layer wipes over content |
| motion states map to meaning (edge-on swap, read-state, "Printing") | motion loops with no state behind it |
| one authored move per interaction, ≤0.8 s for UI | 3+ stacked effects (blur + scale + glitch + glow) |
| vocabulary fits the brand (pixels for JDM, film UI for A24) | the same glitch/blur on any brand |
| reversible and interruptible (repair, close, scrub back) | a toy that leaves the brand broken or blocks input |
| content visible without JS; motion layered on | content at opacity 0 until a trigger fires |

---

## 4. House-law reconciliation (award habit → verdict → crafted alternative)

| Award-site habit seen here | Law verdict | Do this instead |
|---|---|---|
| Preloader hides the page ([E1]–[E6]) | Invisible-content trap | R1: JS-only loader class, first visit only, `prefers-reduced-motion` respected, 3 s failsafe, no-JS page complete |
| Lines/letters start below a mask on scroll ([E9], [E36]) | Hidden until the trigger fires | Hero-only masked rise on load (R3a); below the fold, dim *after* reading (R3b) or scrub a visible property |
| Card hover-lift | Slop | Space-giving 2D accordion (H6, R5) or image swap (H7) |
| Underline grows on hover | Slop | Outline→fill (M3), sibling tonal dim (M2), scramble 1–2 chars (M4), arrow slide |
| Button lifts or scales ("boop") | Slop | Invert fill in place ([E23]) |
| Saturated single accent (red/magenta buttons) | Slop | Tonal accent off the ink. Keep colour for content (product colourways, [E33]) |
| Purple gradient / candy aurora backgrounds ([E35], [E41]) | Slop | Photographic or brand-material backgrounds; a ramp built from the brand's own ink |
| Glowing pill CTA ([E32], [E8]) | Slop | Plain filled or outlined control with a crafted state change |
| Cream background ([E6], [E20], [E26]) | Slop | Brand-derived neutral (paper white, cool grey, or the product's own material colour) |
| Grain over the whole page ([E35] footer card) | Slop when over text | Grain only on the substrate behind text |
| Counters showing `00` until they fire ([E12]) | Invisible content | Real numbers in HTML; animate from them, or count only on user action |
| Custom cursor hides the native pointer ([E19], [E23]) | (not in the law; my usability call) | Keep the native cursor; add the dot/chip as a companion, only on `(hover: hover) and (pointer: fine)` |

---

## 5. Build recipes (checked against current docs, 2026-09-24)

Library versions from the npm registry on 2026-09-24: **gsap 3.15.0** ("Standard 'no charge' license", published 2026-04-13), **lenis 1.3.26** (MIT, 2026-08-05), **three 0.186.1** (MIT, 2026-09-24), **matter-js 0.20.0** (MIT, 2024-06-23), **@barba/core 2.10.3** (MIT, 2024-08-12), **@google/model-viewer 4.3.1** (Apache-2.0, 2026-06-04). GSAP is free for commercial use, including SplitText and MorphSVG ([GSAP standard license](https://gsap.com/community/standard-license/)).

Platform support used below: **scroll-driven animations** (`animation-timeline`) ship in Chrome/Edge 115+ and Safari 26.0+ but are **not supported in Firefox** stable through 158 on caniuse ([caniuse](https://caniuse.com/wf-scroll-driven-animations)). MDN marks the feature "Limited availability" ([MDN animation-timeline](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline)). Always gate with `@supports`. `clip-path` is Widely Available ([web-features](https://web-platform-dx.github.io/web-features-explorer/features/clip-path/)). `@starting-style` and `transition-behavior` are Newly Available since 2024-08-06 ([web-features](https://web-platform-dx.github.io/web-features-explorer/features/starting-style/)).

### R1. Progressive intro (counter-as-curtain, P1) with a failsafe

```html
<!-- in <head>, before CSS paints: opt in only when JS runs, motion is OK, first visit this session -->
<script>
  (() => {
    let seen = false;
    try { seen = sessionStorage.getItem('intro-seen') === '1'; } catch {}
    const motionOK = matchMedia('(prefers-reduced-motion: no-preference)').matches;
    if (motionOK && !seen) document.documentElement.classList.add('intro');
  })();
</script>
<style>
  .loader { display: none; }                       /* no JS / reduced motion: page is complete */
  .intro .loader {
    display: block; position: fixed; inset: 0; pointer-events: none; z-index: 10;
  }
  .intro .loader__count {
    position: absolute; left: 5vw; top: 0;
    font: 700 clamp(3rem, 6vw, 5rem)/1 ui-monospace, monospace;
    font-variant-numeric: tabular-nums;
    translate: 0 calc(var(--edge, 100) * 1vh - 110%); /* counter's bottom rides the mask edge */
  }
  .intro .hero { clip-path: inset(calc(var(--edge, 100) * 1%) 0 0 0); } /* hero is 100vh tall, so % = vh */
</style>
<!-- markup: <div class="loader" aria-hidden="true"><span class="loader__count">000</span></div> -->

```

```js
import { gsap } from 'gsap';

const root = document.documentElement;
if (root.classList.contains('intro')) {
  const out = document.querySelector('.loader__count');
  const state = { n: 0 };
  const finish = () => {
    clearTimeout(failsafe);
    root.classList.remove('intro');                 // hero fully visible, loader gone
    try { sessionStorage.setItem('intro-seen', '1'); } catch {}
  };
  const failsafe = setTimeout(finish, 3000);        // never strand the page
  gsap.timeline({ onComplete: finish })
    .to(state, {
      n: 100, duration: 1.0, ease: 'power2.out',
      onUpdate: () => { out.textContent = String(Math.round(state.n)).padStart(3, '0'); },
    })
    .fromTo(root, { '--edge': 100 }, { '--edge': 0, duration: 0.55, ease: 'power3.inOut' });
}
```

Why it passes the law: without JS or with reduced motion the `intro` class never exists, so nothing is clipped. A backgrounded tab pauses rAF, but the `setTimeout` still fires (throttled) and releases the page. The single `--edge` variable keeps the counter and the mask in lockstep.

### R2. Aperture: inset to full-bleed on scroll (S3), CSS only

```css
.aperture { overflow: hidden; }               /* default: full image, nothing hidden */
.aperture img { display: block; width: 100%; height: 100%; object-fit: cover; }

@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .aperture {
      animation: aperture-open 1ms linear both;  /* shorthand first… */
      animation-timeline: view();                /* …timeline after it, or the shorthand resets it */
      animation-range: entry 10% cover 45%;
    }
    .aperture img {
      animation: aperture-counter 1ms linear both;
      animation-timeline: view();
      animation-range: entry 10% cover 45%;
    }
  }
}
@keyframes aperture-open {
  from { clip-path: inset(10% 14% round 12px); }
  to   { clip-path: inset(0 0 round 0); }
}
@keyframes aperture-counter { from { scale: 1.18; } to { scale: 1; } }
```

The ordering and `1ms` duration follow MDN: `animation-timeline` is a reset-only part of the `animation` shorthand and must come after it. A non-zero duration keeps Firefox's flagged implementation consistent ([MDN timelines guide](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations/Timelines)). Even the start state shows about 70% of the image, so nothing is ever hidden. For Firefox parity, use a GSAP ScrollTrigger scrub with the same keyframes (the CSS does nothing there; the static image is the fallback).

### R3a. Hero masked line rise on load (X5)

```js
import { gsap } from 'gsap';
import { SplitText } from 'gsap/SplitText';
gsap.registerPlugin(SplitText);

gsap.matchMedia().add('(prefers-reduced-motion: no-preference)', () => {
  const split = SplitText.create('.hero h1', {
    type: 'lines',
    mask: 'lines',            // wraps each line in overflow:clip (v3.13+)
    autoSplit: true,          // re-splits on font load / width change
    onSplit: (self) => gsap.from(self.lines, {
      yPercent: 105, duration: 0.9, ease: 'expo.out', stagger: 0.08,
    }),                       // returned tween is reverted/re-synced on re-split
  });
  return () => split.revert();
});
```

API per the GSAP SplitText docs, which also cover the default `aria: "auto"`: it puts an aria-label on the parent and hides the split children from screen readers ([docs](https://gsap.com/docs/v3/Plugins/SplitText)). Use it for the hero only, on load, with a total under 1.2 s. Do not attach it to below-the-fold ScrollTriggers.

### R3b. Below the fold: read-state dimming (X1) instead of hide-then-reveal

```css
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .statement .line {
      animation: read-dim 1ms linear both;
      animation-timeline: view();
      animation-range: exit 0% exit 70%;   /* dims only as the line leaves the top */
    }
  }
}
@keyframes read-dim { to { color: var(--ink-read); } }  /* --ink-read must still pass 4.5:1 */
```

The text is at full ink when you arrive and only de-emphasises after you pass it. Nothing is ever invisible.

### R4. Blend-mode dot companion cursor (H1)

```css
.cursor-dot { display: none; }
@media (hover: hover) and (pointer: fine) {
  .cursor-dot {
    display: block; position: fixed; left: 0; top: 0; z-index: 1000;
    width: 12px; height: 12px; margin: -6px 0 0 -6px; border-radius: 50%;
    background: #fff; mix-blend-mode: difference; pointer-events: none;
    translate: var(--x, -99px) var(--y, -99px);
  }
}
```

```js
const dot = document.querySelector('.cursor-dot');
let x = -99, y = -99, queued = false;
addEventListener('pointermove', (e) => {
  x = e.clientX; y = e.clientY;
  if (!queued) { queued = true; requestAnimationFrame(() => {
    dot.style.setProperty('--x', x + 'px'); dot.style.setProperty('--y', y + 'px'); queued = false;
  }); }
}, { passive: true });
```

No lerp lag: [E19]'s dot sits exactly on the pointer. Keep the native cursor. Over mid-grey backgrounds `difference` goes muddy, so check it on every surface it crosses.

### R5. 2D accordion features grid (H6)

```css
.row {
  display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px;
  transition: grid-template-columns .45s cubic-bezier(.2,.8,.2,1);
}
.row:has(> :nth-child(1):is(:hover, :focus-within)) { grid-template-columns: 1.6fr 1fr 1fr; }
.row:has(> :nth-child(2):is(:hover, :focus-within)) { grid-template-columns: 1fr 1.6fr 1fr; }
.row:has(> :nth-child(3):is(:hover, :focus-within)) { grid-template-columns: 1fr 1fr 1.6fr; }

.card { min-block-size: 10rem; transition: min-block-size .45s cubic-bezier(.2,.8,.2,1); }
.row:has(.card:is(:hover, :focus-within)) .card { min-block-size: 14rem; }  /* row grows */
.card p { display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 1; overflow: hidden; }
.card:is(:hover, :focus-within) p { -webkit-line-clamp: unset; }  /* teaser → full, never hidden */
.card .toggle { transition: rotate .3s; }
.card:is(:hover, :focus-within) .toggle { rotate: 45deg; }        /* + → × */
@media (prefers-reduced-motion: reduce) { .row, .card { transition: none; } }
```

The rows animate their tracks (Widely Available). The hovered row grows via `min-block-size`, and siblings keep the same content. On touch, make each card a `<button aria-expanded>` that toggles a class with the same styles.

### R6. Cross-document shared element: grid ⇄ product "exact cell" (T1)

```css
/* both pages */
@view-transition { navigation: auto; }
::view-transition-group(product-hero) {
  animation-duration: .9s;
  animation-timing-function: cubic-bezier(.16, 1, .3, 1);   /* front-loaded, per E14 */
}
@media (prefers-reduced-motion: reduce) {
  ::view-transition-group(*), ::view-transition-old(*), ::view-transition-new(*) { animation: none; }
}
/* product page */
.pdp__image { view-transition-name: product-hero; }
```

```js
// collection page: name only the one card involved, then clear it (bfcache-safe)
const KEY = 'vt-product';
addEventListener('click', (e) => {
  const card = e.target.closest('[data-product]');
  if (card) try { sessionStorage.setItem(KEY, card.dataset.product); } catch {}
});
const cardImg = () => {
  let id = null; try { id = sessionStorage.getItem(KEY); } catch {}
  return id && document.querySelector(`[data-product="${CSS.escape(id)}"] img`);
};
addEventListener('pageswap', async (e) => {          // leaving grid → product
  const img = e.viewTransition && cardImg(); if (!img) return;
  img.style.viewTransitionName = 'product-hero';
  await e.viewTransition.finished; img.style.viewTransitionName = 'none';
});
addEventListener('pagereveal', async (e) => {        // back from product → grid
  const img = e.viewTransition && cardImg(); if (!img) return;
  img.style.viewTransitionName = 'product-hero';
  await e.viewTransition.ready; img.style.viewTransitionName = 'none';
});
```

The pattern of setting names in `pageswap`/`pagereveal` and clearing them afterwards follows MDN's examples ([pageswap](https://developer.mozilla.org/en-US/docs/Web/API/Window/pageswap_event), [pagereveal](https://developer.mozilla.org/en-US/docs/Web/API/Window/pagereveal_event)). I used `sessionStorage` instead of `navigation.activation` so the code does not depend on the Navigation API. `pageswap`/`pagereveal` availability per browser: MDN says "Limited availability" (per-browser versions unverified). Where they are missing, the plain cross-fade or a normal navigation happens, so it is safe to ship. Cross-document view transitions need same-origin navigations ([MDN @view-transition](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@view-transition)).

### R7. Scroll fisheye "wheel" column (G1)

```js
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

gsap.matchMedia().add('(prefers-reduced-motion: no-preference)', () => {
  const stage = document.querySelector('.wheel');           // no JS: a normal vertical list
  const items = [...stage.querySelectorAll('figure')];
  stage.classList.add('is-wheel');   // CSS: .is-wheel{position:relative;height:100vh;contain:layout paint}
                                     //      .is-wheel figure{position:absolute;left:50%;top:0;translate:-50% 0;overflow:hidden}
  const H_MAX = 0.36, H_MIN = 0.07, W_MAX = 24, W_MIN = 16, GAP = 8, REACH = 3;
  const layout = (p) => {
    const vh = innerHeight, hs = [], tops = []; let acc = 0;
    items.forEach((el, i) => {
      const d = Math.min(Math.abs(i - p) / REACH, 1);
      const t = 1 - d * d * (3 - 2 * d);                    // smoothstep falloff
      const h = (H_MIN + (H_MAX - H_MIN) * t) * vh;
      el.style.width = `${W_MIN + (W_MAX - W_MIN) * t}rem`;
      el.style.height = `${h}px`;
      hs.push(h); tops.push(acc); acc += h + GAP;
    });
    const i0 = Math.floor(p), i1 = Math.min(i0 + 1, items.length - 1), f = p - i0;
    const c = (tops[i0] + hs[i0] / 2) * (1 - f) + (tops[i1] + hs[i1] / 2) * f;
    const shift = vh / 2 - c;                                // keep index p centred
    items.forEach((el, i) => { el.style.transform = `translateY(${tops[i] + shift}px)`; });
  };
  const st = ScrollTrigger.create({
    trigger: stage, start: 'top top', end: () => `+=${items.length * 0.45 * innerHeight}`,
    pin: true, scrub: true, invalidateOnRefresh: true,
    onUpdate: (s) => layout(s.progress * (items.length - 1)),
  });
  layout(0);
  return () => { st.kill(); stage.classList.remove('is-wheel'); items.forEach((el) => el.removeAttribute('style')); };
});
```

Absolutely positioned items inside a `contain: layout paint` stage keep the per-frame size changes local. Images inside use `width:100%;height:100%;object-fit:cover` so they crop and never squash. Keep the column clear of fixed nav labels (the collision seen in [E26]).

### R8. One-to-two-character scramble hover with a stable accessible name (M4)

```html
<a href="/docs" class="nav-link"><span class="sr-only">Docs</span><span aria-hidden="true" data-scramble>DOCS</span></a>
```

```js
const GLYPHS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
function scramble(node, { flips = 2, duration = 280 } = {}) {
  const target = (node.dataset.text ??= node.textContent);
  const idx = [...target].map((c, i) => (c.trim() ? i : -1)).filter((i) => i >= 0)
    .sort(() => Math.random() - 0.5).slice(0, flips);          // only 1–2 letters flip
  const start = performance.now();
  cancelAnimationFrame(node._raf);
  const tick = (now) => {
    const done = now - start >= duration;
    node.textContent = [...target].map((c, i) =>
      !done && idx.includes(i) ? GLYPHS[(Math.random() * GLYPHS.length) | 0] : c).join('');
    if (!done) node._raf = requestAnimationFrame(tick);
  };
  node._raf = requestAnimationFrame(tick);
}
if (matchMedia('(prefers-reduced-motion: no-preference)').matches) {
  document.querySelectorAll('[data-scramble]').forEach((n) =>
    n.parentElement.addEventListener('pointerenter', () => scramble(n)));
}
```

Use a monospace or `font-variant-numeric: tabular-nums` face, or fix the label's width, so the glyph swaps do not reflow the nav.

### R9. Edge-on swap for 3D devices and objects (S1, T3)

```js
// p: 0..1 progress of one step transition (e.g. from a scrubbed ScrollTrigger)
function edgeOnSwap(p, device, screenA, screenB) {
  device.rotation.y = (Math.PI / 2) * Math.sin(Math.PI * p);  // 0° → 90° (edge-on) → 0°
  const showB = p >= 0.5;                                     // swap exactly at edge-on
  screenA.visible = !showB;                                   // two screen meshes: no texture
  screenB.visible = showB;                                    // re-upload, no material recompile
}
```

Pair it with a DOM step list whose active item changes at the same `p = 0.5`, so the copy and the device swap together ([E42]).

### R10. Breakable wordmark with repair (F1), matter.js 0.20.0

```js
import { Engine, Bodies, Composite, Body } from 'matter-js';
import { gsap } from 'gsap';

// .wordmark contains one <span class="ch" aria-hidden="true"> per glyph (CSS: .ch{display:inline-block},
// transforms do not apply to plain inline spans); the heading keeps its aria-label
function breakWordmark(wordmark) {
  const engine = Engine.create();
  const box = wordmark.getBoundingClientRect();
  const chars = [...wordmark.querySelectorAll('.ch')];
  const bodies = chars.map((el) => {
    const r = el.getBoundingClientRect();
    const b = Bodies.rectangle(r.left - box.left + r.width / 2, r.top - box.top + r.height / 2,
                               r.width, r.height, { restitution: 0.2, friction: 0.6 });
    Body.setAngularVelocity(b, (Math.random() - 0.5) * 0.2);
    return { el, b, x0: b.position.x, y0: b.position.y };
  });
  const floor = Bodies.rectangle(box.width / 2, box.height + 25, box.width * 2, 50, { isStatic: true });
  const wallL = Bodies.rectangle(-25, 0, 50, box.height * 4, { isStatic: true });
  const wallR = Bodies.rectangle(box.width + 25, 0, 50, box.height * 4, { isStatic: true });
  Composite.add(engine.world, [...bodies.map((o) => o.b), floor, wallL, wallR]);

  let raf;
  const step = () => {
    Engine.update(engine, 1000 / 60);
    bodies.forEach(({ el, b, x0, y0 }) => {
      el.style.transform = `translate(${b.position.x - x0}px, ${b.position.y - y0}px) rotate(${b.angle}rad)`;
    });
    raf = requestAnimationFrame(step);
  };
  raf = requestAnimationFrame(step);

  return function repair() {                       // the "RÉPARER" action
    cancelAnimationFrame(raf);
    bodies.forEach(({ el, b, x0, y0 }) =>          // hand the physics pose to GSAP first
      gsap.set(el, { x: b.position.x - x0, y: b.position.y - y0, rotation: b.angle * 180 / Math.PI }));
    gsap.to(chars, { x: 0, y: 0, rotation: 0, duration: 0.9, ease: 'expo.out', stagger: 0.03 });
    Composite.clear(engine.world, false); Engine.clear(engine);
  };
}
```

The API calls (`Engine.create`, `Bodies.rectangle`, `Composite.add`, `Engine.update`) follow the matter.js docs ([matter-js README/autodocs](https://github.com/liabru/matter-js)). Add a drag constraint (`MouseConstraint`) for the "SAISIR" grab. Trigger on a real `<button>`, never on hover, and skip the feature entirely under reduced motion.

### Smooth scroll, if you use it

If you add smooth scroll, Lenis honours `prefers-reduced-motion` by default: smoothing is off and programmatic scrolls jump. It syncs with ScrollTrigger via `lenis.on('scroll', ScrollTrigger.update)`, `gsap.ticker.add(t => lenis.raf(t * 1000))` and `gsap.ticker.lagSmoothing(0)` ([Lenis README](https://github.com/darkroomengineering/lenis/blob/main/README.md)). None of the patterns above needs it.

---

## 6. Evidence index (43 sampled elements, fetched 2026-09-24)

Parent-site status is taken from the `/sites/<slug>` page title on 2026-09-24. "Dur" is the clip length in seconds.

| # | Bucket | Element (studio) | Parent site: status | Dur | What it shows |
|---|---|---|---|---|---|
| [E1] | Preloader | A loader that releases a masked hero (J.C. Hardt) | Indisea: Nominee | 2.9 | counter-as-curtain |
| [E2] | Preloader | Preloader -> Hero (Ravi Klaassens) | A24: Nominee | 7.7 | 3D disc loader → carousel, odometer |
| [E3] | Preloader | Pixel Block Entry — Logo Resolves (zhenlong.design) | NightKidz.shop: Nominee | 3.9 | mosaic resolve, scramble, depixelate |
| [E4] | Preloader | "We are …" Preloader (Mark Nystrom) | App State Dept. of Art: Nominee | 5.1 | typographic progress, verb cycle |
| [E5] | Preloader | Intro Animation (Neutral Studio) | Warm & Fuzzy: **SOTD** | 3.0 | rotating aperture → reel |
| [E6] | Preloader | Load homepage (Mees Verberne) | Driessen Architectuur: Nominee | 16.7 | blob → logo, video fade |
| [E7] | Menu | Clip-Path Menu Transition (12 Studio) | Forge Automotive: Nominee | 17.0 | page → thumbnail, blur links |
| [E8] | Menu | Elegant Full-Screen Navigation (Red Dash Media) | Qissa: Nominee | 15.4 | counterexample (static luxury) |
| [E9] | Menu | Editorial Menu (Brandon Yasin) | Brandon Yasin: Nominee | 9.6 | page-miniature menu, line masks |
| [E10] | Menu | Language menu — Expressive typography (cloudstudio) | Money in Check: Nominee | 9.7 | outline→fill, themed loader |
| [E11] | Menu | Simple Dropdown Navigation (Louis Paquet) | Cerebrium: **SOTD** | 11.8 | glass bar→panel, 1-char scramble |
| [E12] | Menu | Floating Dock w/ Ball-Drop Entrance (MOREMEDIA) | MOREMEDIA®: Nominee | 4.7 | ball→pill dock, hero shrink |
| [E13] | Transition | Films -> Detail page (Ravi Klaassens) | A24: Nominee | 6.9 | rules draw, subject-matte rise |
| [E14] | Transition | Grid Memory — Returns to Its Exact Cell (zhenlong.design) | NightKidz.shop: Nominee | 3.8 | view-transition shared element |
| [E15] | Transition | Smooth Page Transition (studiors) | studiors: Nominee | 6.7 | next-project scroll handoff |
| [E16] | Transition | WebGL Grid Shift Transition (Emotion Agency) | Emotion Agency: Nominee | 2.9 | shader block glitch |
| [E17] | Transition | Project Transition (Arc Marumo) | RemyShoots: Nominee | 10.3 | lightbox + editor ruler |
| [E18] | Transition | Films -> Television (Ravi Klaassens) | A24: Nominee | 4.6 | disc flip, edge-on swap |
| [E19] | Hover | A custom cursor that inverts… (J.C. Hardt) | Indisea: Nominee | 5.3 | 12px difference dot |
| [E20] | Hover | Kinetic Project Index (Guillaume Zhu) | Guillaume Zhu: Nominee | 8.3 | word splits to hold thumbnails |
| [E21] | Hover | Channel split hover animation (Juan Mora Romero) | Juan Mora Romero: Nominee | 2.8 | velocity RGB split |
| [E22] | Hover | Night Drive Trail — Cursor Image Stack (zhenlong.design) | NightKidz.shop: Nominee | 6.1 | deck trail + glitch out |
| [E23] | Hover | Dynamic Contextual Cursor (studiors) | studiors: Nominee | 9.0 | action-label chip |
| [E24] | Hover | SWSH Card Hover Interaction (Kyrylo Orlov) | SWSH: Nominee | 6.0 | 2D accordion grid |
| [E25] | Gallery | Carousel (Guillaume Colombel) | G. Colombel Portfolio 2026: Nominee | 9.8 | WebGPU monolith + title ring |
| [E26] | Gallery | Scroll-Driven Gallery (Guillaume Zhu) | Guillaume Zhu: Nominee | 7.0 | fisheye column |
| [E27] | Gallery | Infinite Canvas Art Gallery (Ne Kulturno) | Nala Kun: Nominee | 3.2 | drag canvas, lens warp |
| [E28] | Gallery | Parallax Photo Reveals (Southmates) | La Dolfina Jumping: Nominee | 9.3 | luxury-default parallax |
| [E29] | Product | Product Listing (Made In Evolve) | Unimatic: Nominee | 8.3 | packshot→lifestyle swap |
| [E30] | Product | Product - 3D interaction (Eugene Morev) | Noho: **SOTD** | 30.3 | 3D compare + configurator |
| [E31] | Footer | Physics-Based Breakable Footer (studiors) | studiors: Nominee | 5.9 | breakable wordmark + repair |
| [E32] | Footer | Animated Footer CTA (WHP) | WHP Creative: Nominee | 4.0 | typed tagline, glow pill |
| [E33] | Footer | Footer Reveal - Playful interaction (Eugene Morev) | Noho: **SOTD** | 8.3 | curtain + palette wake |
| [E34] | Footer | Let's talk (Tim Wijnhoven) | Superhuge: Nominee | 8.0 | generative modular wordmark |
| [E35] | Footer | Orb Footer Reveal (Guillaume Zhu) | Guillaume Zhu: Nominee | 7.1 | textPath → orb footer |
| [E36] | Text | Text Reveal Animations (Light mode) (Alexander Löhn) | loehx.com: Nominee | 12.1 | ragged letter rise, read-dim |
| [E37] | Text | Intro (Eder Anaya) | Inherited Band: Nominee | 3.5 | noise letters between faces |
| [E38] | Text | Interactive Text Scroll (Liubomyr Ulytskyi) | Unbelievably Crap: Nominee | 1.6 | text wraps a 3D figure |
| [E39] | Scroll | Scroll reveal (Eder Anaya) | Inherited Band: Nominee | 8.3 | colour block → image, apertures |
| [E40] | Scroll | Introduction Scrubbing (12 Studio) | Forge Automotive: Nominee | 10.2 | blur-from-depth words, aperture |
| [E41] | Scroll | Scroll-Driven Hero (Guillaume Zhu) | Guillaume Zhu: Nominee | 10.1 | rotating monogram composes type |
| [E42] | Scroll | SWSH Events Product Scroll (Kyrylo Orlov) | SWSH: Nominee | 7.4 | pinned phone, edge-on swap |
| [E43] | Scroll | Scroll-Driven Manifesto (Ne Kulturno) | Nala Kun: Nominee | 3.3 | glass panel over zoom-blur |

[E1]: https://www.awwwards.com/inspiration/a-loader-that-releases-a-masked-hero-indisea
[E2]: https://www.awwwards.com/inspiration/preloader-hero-a24
[E3]: https://www.awwwards.com/inspiration/pixel-block-entry-logo-resolves-nightkidz-shop
[E4]: https://www.awwwards.com/inspiration/we-are-preloader-appalachian-state-art-dept
[E5]: https://www.awwwards.com/inspiration/intro-animation-warm-fuzzy-1
[E6]: https://www.awwwards.com/inspiration/load-homepage-driessen-architectuur
[E7]: https://www.awwwards.com/inspiration/clip-path-menu-transition-forge-automotive
[E8]: https://www.awwwards.com/inspiration/elegant-full-screen-navigation-qissa-a-tale-of-food
[E9]: https://www.awwwards.com/inspiration/editorial-menu-brandon-yasin
[E10]: https://www.awwwards.com/inspiration/language-menu-expressive-typography-money-in-check-a-novel-by-oscar-perez
[E11]: https://www.awwwards.com/inspiration/simple-dropdown-navigation-cerebrium
[E12]: https://www.awwwards.com/inspiration/floating-dock-navigation-with-ball-drop-entrance-moremedia-r
[E13]: https://www.awwwards.com/inspiration/films-detail-page-a24
[E14]: https://www.awwwards.com/inspiration/grid-memory-returns-to-its-exact-cell-nightkidz-shop
[E15]: https://www.awwwards.com/inspiration/smooth-page-transition-studiors
[E16]: https://www.awwwards.com/inspiration/webgl-grid-shift-transition-emotion-agency-1
[E17]: https://www.awwwards.com/inspiration/project-transition-remyshoots
[E18]: https://www.awwwards.com/inspiration/films-tv-a24
[E19]: https://www.awwwards.com/inspiration/a-custom-cursor-that-inverts-whatever-it-sits-on-indisea
[E20]: https://www.awwwards.com/inspiration/kinetic-project-index-guillaume-zhu-portfolio
[E21]: https://www.awwwards.com/inspiration/channel-split-hover-animation-juan-mora-romero
[E22]: https://www.awwwards.com/inspiration/night-drive-trail-cursor-image-stack-nightkidz-shop
[E23]: https://www.awwwards.com/inspiration/dynamic-contextual-cursor-studiors
[E24]: https://www.awwwards.com/inspiration/swsh-card-hover-interaction-swsh
[E25]: https://www.awwwards.com/inspiration/webgpu-slider-g-colombel-portfolio-2026
[E26]: https://www.awwwards.com/inspiration/scroll-driven-gallery-guillaume-zhu
[E27]: https://www.awwwards.com/inspiration/infinite-canvas-art-gallery-nala-kun
[E28]: https://www.awwwards.com/inspiration/parallax-photo-reveals-la-dolfina-jumping
[E29]: https://www.awwwards.com/inspiration/product-listing-unimatic
[E30]: https://www.awwwards.com/inspiration/product-3d-interaction-noho
[E31]: https://www.awwwards.com/inspiration/physics-based-breakable-footer-studiors
[E32]: https://www.awwwards.com/inspiration/animated-footer-cta-whp-creative
[E33]: https://www.awwwards.com/inspiration/footer-reveal-playful-interaction-noho
[E34]: https://www.awwwards.com/inspiration/let-s-talk-superhuge
[E35]: https://www.awwwards.com/inspiration/orb-footer-reveal-guillaume-zhu-portfolio
[E36]: https://www.awwwards.com/inspiration/text-reveal-animations-light-mode-loehx-com
[E37]: https://www.awwwards.com/inspiration/intro-inherited-band-official
[E38]: https://www.awwwards.com/inspiration/interactive-text-scroll-unbelievably-crap
[E39]: https://www.awwwards.com/inspiration/scroll-reveal-inherited-band
[E40]: https://www.awwwards.com/inspiration/introduction-scrubbing-forge-automotive
[E41]: https://www.awwwards.com/inspiration/scroll-driven-hero-guillaume-zhu-portfolio
[E42]: https://www.awwwards.com/inspiration/swsh-events-product-scroll-swsh
[E43]: https://www.awwwards.com/inspiration/scroll-driven-manifesto-nala-kun

Video files follow the pattern `https://assets.awwwards.com/awards/element/YYYY/MM/<id>.mp4`. The mapping from each element to its mp4 is in scratch at `evidence/elements-breadth/selection.json`, with frames and `meta.json` in `evidence/elements-breadth/<n>/`.

---

## Retrieval gaps

- **Implementation details are inferred, not documented.** No element page includes a write-up. The only technical signals are self-declared tags ("three.js", "gsap", "matter.js", "view transitions api", "barba.js", "webgpu"). Every "Build" line is my reconstruction from frames plus those tags. In particular, the A24 subject-matte method ([E13]), the Superhuge glyph system ([E34]) and the Colombel stone shader ([E25]) are (unverified).
- **Easing curves are estimated.** Timings come from motion-energy on screen recordings at 24–60 fps with visible cursor and scroll noise. Durations are ±15% lower bounds, and curve names (`expo.out` and so on) are best fits, not extracted values. The pixel-mosaic step timing in [E3] and the [E12] dock spring could not be fitted (25 fps and stepped motion).
- **Scroll-driven clips have no intrinsic duration.** For [E13], [E26], [E35], [E36] and [E39]–[E43], the recorded speed reflects the recorder's scrolling, not a timeline.
- **Only page 1 of each category was sampled** (about 31 cards per category, dated 2026-01-29 to 2026-09-23). Pages 2+ and the other roughly 25 categories (forms, pricing, 404 beyond page 1, modal, cookie and so on) were not reviewed. Tag frequencies are lower bounds, because tags are optional.
- **Award status is a snapshot.** Parent-site titles were read on 2026-09-24. 25 of 28 sites were "Nominee", and many can still win SOTD within their 3-month window. I did not read jury scores, which are visible only to SOTD winners per the FAQ.
- **`pageswap`/`pagereveal` per-browser versions** were not retrieved. MDN only states "Limited availability". R6 degrades safely either way.
- **Firefox scroll-driven status** relies on caniuse (not supported in stable through 158) plus MDN "Limited availability". I did not check a Firefox release note for a flag flip after 2026-09-16.
- **Rate limiting.** awwwards.com returned HTTP 429 on rapid category fetches. They were retried with backoff and all succeeded. No content was missing, but a large re-crawl needs 2–3 s spacing.
