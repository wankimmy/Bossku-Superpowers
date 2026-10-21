# Design directions: the art-direction archetypes of award winners

Last updated: 2026-09-25

Use this when: you hold a brief and must commit to one art direction (plus at most one supporting layer) before any layout, type or motion code exists.

## Rules

1. Commit to one primary direction before writing code. It fixes three things: what owns the first screen, the motion clock (one ease family and one duration ladder), and the palette structure. Everything else follows from those three.
2. Choose by the brief's evidence (an object, a place, footage, text, a body of work, a human service, a loud brand), not by the industry label. Real estate won as a flown world (hubtown), as material calm (era-residence) and as a process filter (son-daven).
3. Two directions at most. The secondary adds exactly one layer (type voice, image treatment, layout device or sound), never a second motion clock and never a second accent.
4. Derive the signature from the brand's own object, material, process or story, and bring it back at 3 or more touchpoints (loader, transition, nav, footer). See "Inventing the signature".
5. The signature must be played, not only watched. All 5 sites in the casebook's Sites of the Year section put the visitor's input into the idea: the cursor paints the helmet (lando-norris), a game (messenger), a scroll-driven camera crane (igloo-inc), a ball you bounce (dont-board-me), a colourway swatch that re-themes the page (opal-tadpole).
6. It must survive with motion off: one still frame states the idea. The probe found a `prefers-reduced-motion` CSS rule on only 11/51 winners (same-origin stylesheets only; JS `matchMedia` gates are not counted) [probe], so this is cheap differentiation.
7. Set display size by direction, not by habit. Material calm keeps DOM display at 48-58px (floema 57.2, fluid-glass 57.6, immersive-garden-website 56, cartier-watches-wonders-2025 48); object heroes run 110-350px with the object occluding the word; 9 of the 11 poster, editorial and illustrated primaries run 136-317px (odd-ritual stays flat at 42px, ponpon-mania at 35px); worlds keep DOM type at 30-82px or push it into WebGL, and only 4 of 10 set one giant word (108-281px). Corpus median: 80px at 1440, 46.8px at 390 [probe].
8. Palette = one ground, one ink, and at most one owned accent covering 5% of the area or less. Colour changes arrive as whole section fields, not sprinkles (shed runs ultramarine #0F00B0 as about 12% of the page, in full sections). In the 2024+ cut the two most-recorded hue families are near-black (152) and near-white (115), and the commonest base is a dark+light contrast pair (86 of 275 tagged) [stats].
9. One ease family per site (fluid-glass runs power3 only; era-residence runs one token set). A second clock is allowed only as slow world versus fast DOM text (steven-com: world 4-7s, DOM text 0.5s).
10. Use 3D only when it carries the subject [webgl-3d-stack §3 Q0]. 26/51 winners load 3D asset files [probe] and 36/51 teardowns mark a 3D layer present [teardowns]; among the editorial and reel primaries, only 1 of 4 each does.
11. Sound is opt-in, off by default, and never the only carrier of information. 21/51 ship it: toys 5/5, posters 3/3, worlds 5/10, and none of the 14 object, editorial and illustrated primaries [teardowns].
12. House law beats award habit: no cream by default (at least 9/51 winners sit on a warm off-white ground), no Google-shelf face carrying the signature (58/554 live winners call the Google Fonts service; Inter, the most-shipped family at 60/554, loads from Google on only 12 of them, so self-hosting hides how often open faces carry winners [fonts]), no saturated accent sprinkled on labels, no display type crushed below -0.04em tracking (the corpus p25 [probe]), and no content parked at opacity 0 waiting for a reveal.
13. No direction buys points. Jury means per direction in this corpus all sit between 7.63 and 7.79 [teardowns]; Usability was the lowest sub-score on 27 of 28 SOTM and annual score pages [awwwards-editorial §0]. Execution and usability decide.

## The ten directions at a glance

Clusters are this file's synthesis over the 51 teardowns (each site has one primary direction; secondaries are listed per direction). Counts are primaries only.

| # | Direction | Primaries (n) | First screen owned by | Display px (measured) | Palette structure | Motion clock | 3D / sound |
|---|---|---|---|---|---|---|---|
| 1 | Flown world | 10 | a lit scene, flown by an authored camera | DOM 30-82.5; giant word on 4/10 at 108-281; 2 all-WebGL | 75-92% scene or void, one emissive hue | camera leads; world 4-7s, DOM 0.3-0.7s | 10/10 / 5/10 |
| 2 | Playable toy | 5 | a toy you operate | UI 13-20; one statement 48-162 | one saturated field 70-84% | springs and held poses; no page scroll | 5/5 / 5/5 |
| 3 | Object hero | 6 | one lit product | 110-350 on 4/6, occluded by the object; quiet 33.6-83.9 on 2/6 | studio field 55-88%; colour from the material | object moves first and alone | 6/6 / 0/6 |
| 4 | Reel as interface | 4 | full-bleed footage | credit 39.6, or wordmark 90-175 | black or white shell, 0% UI accent | little moves at once; ease-in exits | 1/4 / 2/4 |
| 5 | Editorial catalogue | 4 | type on a visible grid | 136.8-231.3 (or flat 42/14) | paper, ink, one full field | masked rises 1.0-1.3s, scrubbed wipes | 1/4 / 0/4 |
| 6 | Kinetic poster | 3 | condensed caps plus one figure | 180-316.8 | duotone pair per section | snappy: 16-22ms char stagger | 2/3 / 3/3 |
| 7 | Illustrated story | 4 | commissioned characters | 144-293 (ponpon-mania 35: the comic letters itself) | section colour = chapter, flat fills | Rive/Lottie characters, plain UI | 1/4 / 0/4 |
| 8 | Material calm | 5 | a material in soft light | 48-58 DOM (one monument 172.8) | material neutral, deep ink, accent near 0 | slow, symmetric; 400/800/1200 ladder | 3/5 / 2/5 |
| 9 | Process filter | 5 | every image through one render grammar | 80-194 | a strict pair forced through the filter | shader leads; stepped time | 4/5 / 2/5 |
| 10 | Archive index | 5 | the body of work itself | 16.32 to 250 | neutral chrome; the work brings colour | one scroll value drives the machine | 3/5 / 2/5 |

## 1. Flown world

Primaries: igloo-inc, active-theory-v6, hubtown, everswap, the-power-of-storytelling, steven-com, san-rita, shader-development-studio, gq-ap-the-extraordinary-lab, terminal-industries. Study first: igloo-inc, everswap, active-theory-v6, steven-com. Secondary in: cartier-watches-wonders-2025, david-whyte-experience.

- **Fit:** offers that are abstract or invisible and need a place to stand in: a holding company (igloo-inc), a DeFi protocol (everswap), a yard operating system (terminal-industries), a property developer (hubtown), a creator holding (steven-com), studios proving real-time craft (active-theory-v6, shader-development-studio, san-rita). Rising: WebGL tags on 42.7% of recent SOTDs against 16.5% of Honorable Mentions [awwwards-editorial §4.2].
- **Signature pattern:** a metaphor place taken from the brand story (a peak for "DeFi at peak" in everswap, ice holding the portfolio in igloo-inc, a trail map for an expedition-minded studio in san-rita), crossed by one authored camera. Scroll is one legible axis; chapters are locations; neighbours hand over through a wipe (igloo-inc spectral diagonal, active-theory-v6 normal-map diagonal).
- **Palette:** 75-92% scene or void, 5-20% emissive or scene light, 5% ink or less (hubtown 75/20/5, igloo-inc 85/12/3, gq-ap-the-extraordinary-lab 92/8/0). Fog colour = clear colour = page background [webgl-3d-stack §5]. Colour may encode chapters: steven-com gives each venture room one hue (#FFDD4B, #FF5541, #5595FF, #51B75A).
- **Type:** the world owns scale. Text is a HUD (hubtown 30/12/9px on a clamp(12px, .8333vw, 24px) root; steven-com 51px h1 over 12px body; igloo-inc and active-theory-v6 draw nearly all type in WebGL, igloo-inc as 14px MSDF mono with 0 DOM headings) plus at most one giant word (the-power-of-storytelling 19.5vw = 281px; everswap 188.9px high-contrast serif at weight 200). Let caps echo the UI geometry: san-rita's F37 Stout has chamfered bowls that match its 10px chamfered cards.
- **Layout:** HUD pinned to the viewport over a full-bleed canvas, corner-anchored on one margin token so the four corners share axes (igloo-inc about 50px at 1440; hubtown a bevelled frame inset 30px); the law's "flung to the far edges" fails when each corner picks its own inset. No DOM grid (the-power-of-storytelling: 0 grid containers). Set scene length in vh: active-theory-v6 uses 105vh × (4, 1, 10, 2, 1.2, 4); the-power-of-storytelling maps 20 scroll sections to 20 seconds of one Blender timeline.
- **Motion:** camera first, words after; transit beats carry no type (everswap: dolly, vignette, title outline, words, fill over about 4s). Two clocks: world reveals 4-7s on power2.inOut, DOM text 0.5s (steven-com). Winners often hijack scroll (custom virtual scroll on igloo-inc, everswap, cartier); keep native scroll under Lenis and scrub the camera from progress instead, as active-theory-v6 (native scroll on a fixed div) and the-power-of-storytelling (ScrollSmoother) do [usability-a11y-perf §2.F]. Tokens: scrubs `linear`; camera damped `1 - exp(-k·dt)`; DOM lines `--ease-reveal` at `--dur-4` (600ms, near steven-com's 0.5s) ([../recipes/tokens.css](../recipes/tokens.css)). See [motion.md](motion.md) and [webgl-3d.md](webgl-3d.md).
- **Imagery and 3D:** real-time on 9/10 with glb + ktx2 + Draco and baked light (active-theory-v6 Cycles-baked maps; everswap painted, unlit textures); adaptive DPR (igloo-inc steps DPR with measured FPS). Budget variant: a 410-frame pre-rendered film scrubbed on a 2D canvas (terminal-industries). Start from [../recipes/three-hero.js](../recipes/three-hero.js) (poster first, canvas over it).
- **Sound:** 5/10, always opt-in: an ambient bed with a low-pass sweep on transitions (hubtown); narration that drives the camera, with timed subtitles (gq-ap-the-extraordinary-lab).
- **Slop version:** an abstract blob or torus in a blue-charcoal void, bloom halo, periwinkle HUD, idle auto-rotate, a long blank loader, every word inside WebGL. Winners brush it: hubtown pairs #020A19 with #D5E0FF periwinkle ink (the law's dark default); igloo-inc shows about 6s of near-blank grey and has 0 DOM headings. **Crafted:** ground hue from the metaphor (active-theory-v6 green-black, everswap painted greens, igloo-inc fog grey), HTML first paint with a poster frame, all text in the DOM and focusable [awwwards-editorial §3.4].

## 2. Playable toy

Primaries: brunos-portfolio, messenger, lacoste-polo-factory, leo-parpeix-portfolio-2026, why-zero. Secondary in: ponpon-mania, dont-board-me.

- **Fit:** the visit is the product: creative-developer portfolios (brunos-portfolio, leo-parpeix-portfolio-2026), a studio's game (messenger), a brand activation with a prize draw (lacoste-polo-factory), a campaign microsite (why-zero). Game mechanics are moving into brand and portfolio sites [awwwards-editorial §4.2]. Never for task-first pages.
- **Signature pattern:** one verb the visitor performs that is the brand's story: drive the world (brunos-portfolio); deliver on a tiny planet (messenger); press machines that dye and stitch the polo (lacoste-polo-factory); carry a fruit on the cursor and drop it onto the type, where it casts a real shadow (leo-parpeix-portfolio-2026); draw a zero on ice to unlock (why-zero).
- **Palette:** one saturated field at 70-84% (messenger teal #65c1bc about 70%; lacoste-polo-factory mint #c9e2ad about 84%), one ink (#0b4221 brand green), one object colour at 5% or less (messenger mustard #f0d054). Toon or clay light: hue-tinted AO per room (lacoste-polo-factory), ink outlines plus a 3D LUT (messenger).
- **Type:** small DOM, lettering in the world. UI 13-20px (brunos-portfolio 20px, lacoste-polo-factory 13px); one statement page at most (leo-parpeix-portfolio-2026 11.25vw = 162px caps, line-height .9, three lines composed as a block the fruit lands on; a three-line display that is just wrapping is the law's multi-line headline tell). messenger draws every word in WebGL; keep a DOM mirror anyway.
- **Layout:** fixed viewport, no document scroll (brunos-portfolio, messenger and lacoste-polo-factory all measure 900px document height); controls in corners; a visible way out (menu, skip, sound toggle, keyboard path).
- **Motion:** physics on objects, held poses on drawn things. messenger springs its title tiles and steps drawn graphics at 1.3-8 Hz; brunos-portfolio opens its reveal disc on back.out(1.7) over 2s. Overshoot belongs to world objects; DOM buttons stay on `--ease-micro` at `--dur-2` (lacoste-polo-factory's back-out UI pills are the habit to skip).
- **Imagery and 3D:** real-time 5/5: low-poly dioramas, custom toon or clay materials, WebGPU + TSL at the top end (brunos-portfolio, three r183).
- **Sound:** 5/5, unlocked by the first gesture: about 30 sound folders (brunos-portfolio), 54 OGG files with zone ambiences (messenger), a loop per machine (lacoste-polo-factory).
- **Slop version:** a game unrelated to the brand, input captured with no exit, a Google novelty display face, bouncy buttons. brunos-portfolio sets its signage in Amatic SC and its UI in Nunito, both Google faces. **Crafted:** the toy is the brand's own verb; licensed or drawn lettering; skip and keyboard paths; a poster still for reduced motion.

## 3. Object hero

Primaries: the-watch, opal-tadpole, oryzo-ai, vast, lando-norris, iyo. Secondary in: slosh-seltzer, the-power-of-storytelling, floema.

- **Fit:** a physical object whose form, material or mechanism is the argument: consumer hardware (opal-tadpole, iyo), a watch (the-watch), a space station (vast), a race helmet (lando-norris), a parody coaster (oryzo-ai).
- **Signature pattern:** the object does what only it can do, with the visitor. the-watch shows the visitor's own local time on its hands, then scroll dismantles and reassembles it; lando-norris lets the cursor paint the real helmet onto a displaced portrait; opal-tadpole's colourway swatch re-themes the page in about 1.4s; iyo shows its subject, sound, as 1.6M particles on Chladni lines.
- **Palette:** a studio field at 55-88% (vast 55, lando-norris 55, opal-tadpole 60, the-watch 75-85, iyo 88), chosen to light the material; the product supplies the colour. the-watch #ebebeb grey to near-black; oryzo-ai #100904 warm brown-black with #ffedd7 ink and #dc5000 under 5%; iyo #101010 "neutral, not blue"; opal-tadpole reserves #ffdb01 for interaction states only; vast uses #ff5623 on under 1% of the page, as 10px squares.
- **Type:** two tiers with nothing between, and the object occludes the display. the-watch Nekst 350px at line-height .8 against 12px body; vast a 24vw = 345.6px ghost wordmark; oryzo-ai 216px, line-height .9, -0.018em. Quiet alternative: opal-tadpole Roobert 300 at 83.9px, sentence case, -0.01em. Mono only where it is data (vast's Phonic on spec tables and dates).
- **Layout:** centred object with type staged behind and around it like a studio shoot; pinned statement sections; a spec rail.
- **Motion:** the object moves first and alone; copy scrubs around it (the-watch: power3.inOut 97 times, copy offset by innerHeight × .1 per element). Turntables are frame sequences scrubbed on canvas (opal-tadpole: 321 frames). Tokens: object travel `--ease-move`, scrubs `linear`, re-theme legs `--dur-4`.
- **Imagery and 3D:** 6/6: GLB + EXR (the-watch), an R3F model with 3D-anchored hotspots (vast), a pre-rendered sequence (opal-tadpole), a displaced relief plus glb (lando-norris). One key light, IBL and a contact shadow [webgl-3d-stack §5]; [../recipes/three-hero.js](../recipes/three-hero.js).
- **Sound:** 0/6. The object carries it.
- **Slop version:** a product on idle auto-rotate over a radial glow, bobbing, on a gradient backdrop. **Crafted:** long lens (18-35° FOV), one directional key with falloff, grounded contact shadow, rotation only from the visitor's scroll or drag.

## 4. Reel as interface

Primaries: depo-luxe, siena-film-foundation, bennett-clive, thelinestudio-com. Secondary in: artefakt, terminal-industries.

- **Fit:** companies whose work is moving image and already graded: production houses (depo-luxe, bennett-clive), a film foundation (siena-film-foundation), an animation studio (thelinestudio-com).
- **Signature pattern:** a cinema object becomes the UI. Projection-booth credits and a roman-numeral rail with a soft click on every reel change (depo-luxe); an infinite film strip that smears with scroll speed under a cinema-ticket nav (siena-film-foundation); one pinned wordmark row at 50vh that client names relay across (bennett-clive); animation-desk material, a red acetate gel peeled off by the first scroll and paper cels flung from a corner pivot (thelinestudio-com).
- **Palette:** a black or white shell; footage supplies 100% of the colour and the UI carries 0% accent (depo-luxe: about 95% footage and black, 3% type). A flat black veil of 14-25% over film for legible type (depo-luxe .14-.25; bennett-clive 20%).
- **Type:** a small credit or a tight wordmark. Credit: depo-luxe italic 39.6px, only three live sizes, -0.01em at every size. Wordmark or poster: siena-film-foundation 89.6px caps at line-height .77 and -0.03em; bennett-clive 10.41667vw = 150px at .77; thelinestudio-com 175px at -0.04em and .8. Take the sizes, not the faces: depo-luxe's credit is EB Garamond and bennett-clive's wordmark is Inter Bold at -0.07em, both open faces the law rejects as signature voices, and -0.07em is the corpus minimum [probe]. License a face with a cinema-credit cut and hold tracking at -0.04em or looser.
- **Layout:** one viewport per film; one centred credit line; UI reduced to one rail or one axis.
- **Motion:** very little moves at once. Exits ease in (depo-luxe Power2.easeIn 61 times); entrances expo-out at 0.8-1.0s (siena-film-foundation defaults to duration 1, expo.out); retitle only after the strip settles (siena-film-foundation 800ms queue); type blinks on in frame steps (thelinestudio-com 90/150/210ms). Tokens: `--ease-exit` at `--dur-3` out, `--ease-reveal` at `--dur-4` to `--dur-5` in.
- **Imagery and 3D:** video with posters [imagery §4.5]; WebGL only as image planes or a shader over film (siena-film-foundation, OGL).
- **Sound:** 2/4, UI only (depo-luxe click at volume .4; siena-film-foundation hover and menu cues). Films stay muted.
- **Slop version:** an autoplaying showreel behind a "play reel" pill, grain over everything, a hover-to-play thumbnail grid. **Crafted:** a credit grammar lifted from real film practice, one axis, grain only inside the canvas pass (siena-film-foundation adds noise at .07 in-shader, never over DOM text).

## 5. Editorial catalogue

Primaries: aim-ai-modernism-of-kharkiv, shed, tracing-art, odd-ritual. Secondary in: vast, the-renaissance-edition.

- **Fit:** text-substantial culture and archives (aim-ai-modernism-of-kharkiv, tracing-art), design agencies with strong photography (shed), apparel with editorial photography (odd-ritual). Fading as a default: the Typography tag fell from 27.3% (2023) to 18.7% (2026) and Minimal is 2.2x more common on HM-only sites [awwwards-editorial §4.3]. It still wins when the grid carries a concept.
- **Signature pattern:** the catalogue grammar performs the subject. aim's constructivist slabs grow the wordmark, restack behind the manifesto and rebuild at the footer (three Lottie files); tracing-art floats real collection objects on two depth layers and tells one painting's ownership history over them; odd-ritual runs one clip-path polygon wipe for slider, preloader, menu and page swap.
- **Palette:** paper, ink and one full-bleed field. aim #e7e4df/#141414 at 75/20/5; tracing-art pure #fff/#000, no cream; shed #fff/#1c1c1c with ultramarine #0F00B0 as whole sections (about 12%).
- **Type:** a two-tier poster scale on a viewport root. aim sets html to 1vw: display 9.5em = 136.8px at -0.035em and line-height .85, meta 1em = 14.4px, nothing between 1.2em and 5.5em. shed runs Owners 600 caps at 16.06vw = 231.3px, line-height .9. tracing-art runs Bradford serif 207px at -0.03em with roman and italic mixed in one line. Or deliberately flat: odd-ritual 42/14px. See [typography.md](typography.md).
- **Layout:** a visible grid in thirds (aim: a pinned split index at 1fr .33fr .66fr), numbered indexes, footnotes, pinned image stacks with a counter.
- **Motion:** masked line rises at 1.0-1.3s (aim heading rises 1200-1300ms, 100ms apart); scroll-scrubbed Lottie; polygon wipes with ±10% counter-parallax (odd-ritual). Tokens: `--ease-reveal` at `--dur-5`, `--stagger-lines`; wipes on `--ease-move`. Use [../recipes/motion-core.js](../recipes/motion-core.js) `data-reveal="lines"`, which moves text that is already visible.
- **Imagery and 3D:** photography or stills with their grade intact; 3D only as image planes (tracing-art).
- **Sound:** 0/4.
- **Slop version:** cream ground, a Cormorant or Fraunces H2 under a tracked-caps kicker, a hairline under every row, brackets on every label. aim itself carries several of these: #e7e4df ground, bracket labels throughout, 1px rules, an underline-slide hover, headings hidden by IX2 initial states until they fire, and a TRIAL font shipped to production. **Crafted:** a ground chosen for the subject (tracing-art pure white), rules only where the grid is the concept, labels that differ by role, a licensed grotesk.

## 6. Kinetic poster

Primaries: champions-for-good, zentry, slosh-seltzer. Secondary in: lando-norris, dont-board-me, made-with-gsap-1.

- **Fit:** loud brands with owned colours and a young or fan audience: a sports club (champions-for-good), web3 gaming (zentry), a drink (slosh-seltzer).
- **Signature pattern:** the poster moves with the body or the product. Pictogram athletes built from polygons play their sport as you scroll and stand on section edges as ground (champions-for-good); every image is a perspective-projected card that tilts on a 3D hinge (zentry); the can pops, tips and pours seltzer that floods the viewport as the section transition (slosh-seltzer).
- **Palette:** a strict duotone pair per section, 70-85% ground and 15-30% ink (champions-for-good 85/15; slosh-seltzer #FFC1FF/#FF0837 at 85/12/3 on the gate, then 70/30 band pairs).
- **Type:** condensed heavy caps at 180-317px, sized in vw. champions-for-good Druk Condensed Super at 22vw = 316.8px, line-height .51 (lines interlock only because the caps carry no descenders; proof it at size or use .8, the corpus p25 is .83 [probe]); zentry 180px at .82 and -0.01em, with wedge-cut alternates switched on per glyph; slosh-seltzer Steelfish 207px against a 16px mono (13:1).
- **Layout:** each section is one poster, full-bleed; section edges double as ground lines.
- **Motion:** snappy and physical. Lenis lerp .18 (champions-for-good, against the .1 default); characters skid in from 80px on a 14° skew that straightens last, 16-22ms per char; words snap 70-100ms apart on power4.out (zentry). Tokens: `--ease-out-quint` or `--ease-out-expo` at `--dur-4`; `--stagger-chars` .016-.022. For pull on a CTA, [../recipes/magnetic.js](../recipes/magnetic.js) moves the label, never the box.
- **Imagery and 3D:** Lottie figures (champions-for-good), a Spline hero object (zentry), a PBR can plus a fluid sim (slosh-seltzer).
- **Sound:** 3/3, opt-in: per-sport foley (champions-for-good), UI sprites and whooshes (zentry), a backing track and pour loop (slosh-seltzer).
- **Slop version:** Anton or Bebas from Google, neon lime on every CTA, a marquee of tags, skew for its own sake, purple duotones. Winners brush the last one: zentry leans on #5542FF violet and champions-for-good pairs #23002b with lilac #e894ff. **Crafted:** take the pair from the subject's own kit or product (slosh-seltzer's pink and red are the can), a licensed display with a real feature (wedge alternates), skew that encodes motion (the skid straightens last).

## 7. Illustrated story

Primaries: mindmarket, maxima-therapy, dont-board-me, ponpon-mania. Secondary in: champions-for-good, dropbox-brand.

- **Fit:** human services and causes where photography would be stock: a therapy nonprofit (maxima-therapy), dog walking (dont-board-me), B2B research services (mindmarket), a web comic (ponpon-mania). Flat illustration as a default is fading (Illustration tag 6.0% in 2026) but still wins when authored: mindmarket reached SOTM with no 3D [awwwards-editorial §4.3].
- **Signature pattern:** the service as a journey you move through. A scroll-drawn board-game trail with Rive characters staged along it (mindmarket); a colour fan curtain whose last frame is the hero's V-hills (maxima-therapy); bounce a ball to enter, then deal the process cards (dont-board-me); a camera flying from comic cover to page to panel (ponpon-mania).
- **Palette:** section colour = program or chapter. maxima-therapy switches #FDCB40 / #00B351 / #F780D4 / #2CD1D0 by life stage, with 0 shadows and 0 filters. Or one ink is the brand: dont-board-me sets red #e33529 as the text colour on pink, about 22% of the page.
- **Type:** big rounded or condensed caps over a plain body: maxima-therapy Robuck Rounded 214.3px at line-height .8 with a Dinamo Diatype Rounded body; dont-board-me 293px at .78-.8 and -0.02em; mindmarket 144px. Two of the three are law failures to fix, not copy: dont-board-me's display is Bayon (Google) and mindmarket's is self-hosted Inter at -0.06em. Keep the scale and the plain body, license the display, and hold tracking at -0.04em or looser.
- **Layout:** a path or a sequence (trail, fan, deal of cards) with plain cards riding over the illustration.
- **Motion:** characters live in Rive or Lottie state machines (mindmarket: 14 Rive instances); curtains at 1.0-1.2s (maxima-therapy GSAP 1s ×27, 1.2s ×16); overshoot only on props (dont-board-me ball on bounce.out, 1.2s). maxima-therapy's elastic.out on headings is the habit to drop. Tokens: UI `--ease-micro` at `--dur-2`; curtains `--ease-move` at `--dur-5` (1000ms, matching maxima-therapy's 1s ×27).
- **Imagery and 3D:** commissioned illustrators with one rule set (mindmarket and maxima-therapy both credit KOKI-KIKO and Louis Paquet; dont-board-me uses commissioned editorial dog portraits).
- **Sound:** 0/4.
- **Slop version:** stock vector people, a candy gradient, hand-coded SVG figures, a rounded Google face everywhere, bouncing buttons. **Crafted:** one illustrator's hand with a construction rule (polygon pictograms, rubber-hose limbs), flat fills, characters that act the content out.

## 8. Material calm

Primaries: era-residence, fluid-glass, floema, immersive-garden-website, cartier-watches-wonders-2025. Secondary in: son-daven, gq-ap-the-extraordinary-lab.

- **Fit:** high-consideration purchases where material quality is the argument: residences (era-residence), architectural glazing (fluid-glass), urban furniture (floema), luxury houses and their agencies (immersive-garden-website, cartier-watches-wonders-2025). The Luxury tag rose from 3.0% (2024) to 11.6% (2026) [awwwards-editorial §4.2].
- **Signature pattern:** the material or its making, shown in one continuous gesture. A hairline drawing wiped away bottom-up to the registered photograph of the same building (fluid-glass); the Mediterranean arch as preloader window and doorway (era-residence); product cut-outs streaming out of a fog tunnel while baked foliage shadows follow the cursor (floema); the whole page carved into a plaster bas-relief (immersive-garden-website); each watch's own geometry built into architecture (cartier-watches-wonders-2025).
- **Palette:** a neutral taken from the material, a deep ink, accent near zero. immersive-garden-website plaster #e8e8e8 at 90/8/2; floema ivory #f2efea, stone-brown #241f21 ink, flour-yellow floors about 7%; era-residence navy #17233B ink, plum #340C24 on the preloader only.
- **Type:** small, sentence case, often with a full stop: floema Zimula 57.2px at -0.04em; fluid-glass Aeonik 57.6px at -0.03em, line-height 1.0; immersive-garden-website PSTimes serif 56px at normal tracking. One monument allowed: era-residence at 172.8px and -0.024em, crossed by a script word. Its face is a compressed Didone-derived serif (Ambroise, Adobe Fonts), which is exactly the law's autopilot luxury choice; pick the serif for a detail tied to the place instead.
- **Layout:** airy; one thing moves at a time (floema); one frosted bar docked bottom-centre that becomes the menu (fluid-glass). Glass only over real imagery, with no banding, leak or pop (law: botched glass).
- **Motion:** slow and symmetric. A 400/800/1200ms token ladder (era-residence, and son-daven from the same studio); Lenis duration 1.2 with exponential easing; one ease family (fluid-glass, power3 only); big moves 2-6s on sine.inOut (immersive-garden-website). Tokens: override `--dur-3: 400ms; --dur-4: 800ms; --dur-5: 1200ms` in [../recipes/tokens.css](../recipes/tokens.css); the studio's CustomEase 'Out' (.25,1,.5,1) is `--ease-enter` and 'InOut' (.76,0,.24,1) is `--ease-move`; ambient loops on `--ease-ambient`.
- **Imagery and 3D:** architectural photography or CGI in real light; 3D (3/5) only where the material is the subject: a PBR product spin rendered in Web Workers (floema), a plaster relief under a cursor flowmap (immersive-garden-website).
- **Sound:** 2/5, opt-in ambience (immersive-garden-website; cartier-watches-wonders-2025 with six state stems).
- **Slop version:** cream ground, a letterspaced Didone wordmark, slow fades up from opacity 0, grain over text, Ken Burns pans. 3 of 5 primaries sit on warm off-white (era-residence #F3F3EC, floema #f2efea, fluid-glass #f3f0ec), era-residence's display is a Didone-derived compressed serif, and its first-visit preloader runs about 7.75s (1.2s hold, 1.2s watermark, a 4.0s fake progress bar, a 1.35s arch rise). **Crafted:** a ground sampled from the material (lit plaster grey, fog grey, stone), a licensed serif chosen for a detail tied to the place, reveals that move content that is already visible, and the arch-style signature preloader cut to under 2s (era-residence already serves return visits a short version with no text and no progress bar).

## 9. Process filter

Primaries: lama-lama-2, artefakt, son-daven, the-renaissance-edition, david-whyte-experience. Secondary in: messenger, ponpon-mania, gq-ap-the-extraordinary-lab.

- **Fit:** mixed-source imagery that needs one voice, or a brand whose craft is a graphic process: an agency with a pixel mark (lama-lama-2), a production company (artefakt), a resort rooted in Hutsul culture (son-daven), a poet's landscapes (david-whyte-experience), a release catalogue of 150+ updates (the-renaissance-edition).
- **Signature pattern:** one render grammar derived from the brand, applied to every image, transition and cursor trail. The 4x4 "LL" mark as ordered-dither sub-pixels (lama-lama-2); brand-seeded ASCII glyphs (artefakt); two-colour vertical line-screen bars like woven cloth (son-daven); watercolour cut-outs that paint themselves in under a fluid brush (david-whyte-experience); generative Renaissance paintings rebuilt as live dioramas that dissolve through a painterly edge (the-renaissance-edition).
- **Palette:** a strict pair the filter forces onto all media: son-daven sand #a89474 / ink #2c2824 at 55/35/10; lama-lama-2 #1A1C1C / #F9F4EB at 85/10/5; artefakt black and white at 97/3 in the shell.
- **Type:** tight caps at 80-194px (lama-lama-2 80px at .8 and -0.02em, with a terminal period; son-daven 144px at -0.064em, tighter than the corpus p25 [probe], so proof it at size before copying; the-renaissance-edition 193.7px at -0.03em and .9), or a hairline serif (david-whyte-experience Canela Thin 100 at 86px).
- **Layout:** the filter lives on a fixed full-viewport canvas behind the content, with a second canvas above it for transitions (lama-lama-2). A fixed layer passes the law only when it reacts (lama-lama-2's dither answers cursor velocity) and stays out from under the nav's text.
- **Motion:** the shader leads and the DOM follows (lama-lama-2). The filter keeps its own time signature: son-daven's 20x12 cell "spires" stagger 30ms per cell; artefakt's shader reveals take 2000ms; ponpon-mania boils its line work in stepped time; messenger holds poses. Tokens: the filter on `steps()` or a quantized uniform (son-daven: 30ms per cell); DOM on `--ease-reveal` at `--dur-5`, the filter's reveal at 2000ms (artefakt).
- **Imagery and 3D:** 5/5 run WebGL (4/5 are recorded as 3D; son-daven's is raw WebGL1 2D image processing only), mostly as a full-screen 2D shader (raw WebGL2 in lama-lama-2) [webgl-3d-stack §3 Q4, §4.8]. [../recipes/webgl-image-hover.js](../recipes/webgl-image-hover.js) is the base for DOM-synced image planes.
- **Sound:** 2/5, opt-in ambience (son-daven; david-whyte-experience with three crossfading loops).
- **Slop version:** a generic ASCII or dither shader over stock footage, or a fixed character field that twinkles behind every section including the nav. son-daven lays a noise sheet at opacity .1, soft-light, over the whole page, type included. **Crafted:** derive the cell from the mark or the craft (lama-lama-2's logo is the sub-pixel), run it on media and never on text, keep grain inside the shader.

## 10. Archive index

Primaries: gil-huybrecht, pacome-pertant-portfolio, akaru-2, made-with-gsap-1, dropbox-brand. Secondary in: tracing-art.

- **Fit:** range is the proof and visitors come to browse: independent designers (gil-huybrecht), motion designers (pacome-pertant-portfolio), agencies (akaru-2), an effects library (made-with-gsap-1), a design system (dropbox-brand).
- **Signature pattern:** the index itself is the instrument. Every capture of every project on one WebGL contact sheet (gil-huybrecht); a wheel-driven helix of thumbnails that smears with velocity and greys out beyond a band (pacome-pertant-portfolio); a rail of overlapping pastel project panels (akaru-2); numbered effects with a live "ON SCREEN 090" chip (made-with-gsap-1); a homepage that is the menu, eight chapter tiles pulled into a mosaic (dropbox-brand).
- **Palette:** neutral chrome, the work brings the colour: gil-huybrecht 60% black, 38% the client screenshots, 2% white type, no accent; pacome-pertant-portfolio #0a0a0a about 85%, mint under 1%; akaru-2 four project pastels of similar value (#BFCCD8, #B692A1, #798E7B, #E49366).
- **Type:** flat or single-size scales. gil-huybrecht uses one size, 16.32px, ratio 1:1, hierarchy from position alone; pacome-pertant-portfolio sets 94 of 101 text nodes at 18px. The loud exception saves size for one set piece (made-with-gsap-1 250px at -0.04em and .8).
- **Layout:** a 14-column grid with 2-column cells, so 7 visual columns (gil-huybrecht); one scroll value maps every tile (dropbox-brand, on native scroll); a paused timeline scrubbed by sticky progress (akaru-2, Lenis lerp .07).
- **Motion:** one entrance, then a still layout that still answers input (gil-huybrecht; the law's "dead-looking" fail is a page that ignores hover and scroll velocity), or one machine moving as a unit (pacome-pertant-portfolio's helix smears with wheel velocity). Tokens: scrubs `linear`; item settles on `--ease-enter` with `--stagger-items`, capped by `--stagger-max` 0.6s; open a project with a shared element via [../recipes/page-transitions.js](../recipes/page-transitions.js).
- **Imagery and 3D:** image-plane shaders (gil-huybrecht, pacome-pertant-portfolio) or plain DOM with video (made-with-gsap-1).
- **Sound:** 2/5: pacome-pertant-portfolio pairs 15 Howler cues with per-cue volumes; gil-huybrecht only in a hidden mode.
- **Slop version:** a masonry grid with hover-lift, image cards with overlay captions, a cursor-following preview, a horizontal gallery (tagged on only 2-4% of winners each year, and called the stock derivative move by a juror [awwwards-editorial §4.3]). **Crafted:** the index as one object with one gesture; hover changes tone in place (akaru-2's direction-aware row fill, a clip that fills the full row; the direction logic is inferred), never lifts.

## Direction picker

Read the brief, name its strongest evidence, then take the row.

| Brief attribute | Primary | Good secondary layer | Avoid |
|---|---|---|---|
| A physical product whose form, material or mechanism is the pitch | Object hero | Editorial (spec type), Kinetic poster (youth brand) | Flown world: the product gets lost in a place |
| An abstract or invisible offer (protocol, platform, holding, OS) | Flown world; budget: pre-rendered scrub (terminal-industries) | Object (one hero thing inside the world) | Material calm: nothing tangible to light |
| A place (residence, resort, destination, venue) | Material calm | Process filter if the place has a craft culture (son-daven); Flown world for night or scale (hubtown) | Kinetic poster |
| The work is moving image | Reel as interface | Process filter (artefakt) | Illustrated story |
| Archive, museum, research, long-form text | Editorial catalogue | Archive index (tracing-art's dataset view) | Playable toy |
| Portfolio where range is the proof | Archive index | Reel (motion work), Process filter | Flown world unless 3D is the craft on sale |
| Creative-dev portfolio or campaign where the visit is the product | Playable toy | Process filter (ink, boil) | Editorial catalogue |
| A warm human service, nonprofit, or B2B service with no photogenic product | Illustrated story | Kinetic poster (big caps) | Flown world |
| A loud youth, sport, drink or gaming brand with owned colours | Kinetic poster | Illustrated (figures), Object (the can) | Material calm |
| Mixed-source media that must read as one voice, or a brand with a graphic craft | Process filter | whichever direction owns the first screen | Two filters |

Tie-breakers, in order:
1. **Task-first pages** (checkout, catalogue, lead form) keep native scroll and DOM content: choose object, calm, editorial or index there. Winners that sell stay on those: floema (B2B catalogue, calm, 3D in workers), opal-tadpole (store page, object hero on native scroll), odd-ritual (Shopify, editorial). A toy or a world belongs on a campaign route or hero only.
2. **No 3D budget, or the 3D would not carry the subject:** editorial, kinetic poster with Lottie, illustrated with Rive, reel, index, or a filter on a 2D shader. Budget ceiling for any 3D: about 1.5 MB compressed before first interaction on mobile, else step down [webgl-3d-stack §3].
3. **Audience time:** toys and worlds ask for minutes; reels, indexes and catalogues pay back in seconds.
4. **Trend weight** [awwwards-editorial §4.2-4.3]: rising are real-time worlds, game mechanics in brand sites, luxury real-time cinema and expressive B2B; fading as defaults are type-only minimalism, parallax as the idea, flat illustration and horizontal galleries.

Write the decision as one line before designing: `<Direction> (+ <secondary layer>) for <brand>: <signature sentence>. Ground <hex>, ink <hex>, accent <hex or none>. Display <face> at <px>. Clock <ease family>, ladder <ms>.`

## Inventing the signature

The direction is a genre; the signature is the one owned idea inside it. Method:

1. **Inventory the brand's nouns** in four bins: object (product, mark, packaging), material (cork, plaster, glass, stone, cloth), process (how it is made, drawn, woven, poured, surveyed), story (a place, a founder, a ritual, a joke).
2. **Give each noun its verb**, the thing it physically does: pours, bounces, tells time, carves, weaves, dithers, projects, opens, narrates.
3. **Apply the verb to a page element** (cursor, scroll, loader, transition, nav, footer). The pair is the signature. Derivations from the corpus:

| Source | Verb | Signature (site) |
|---|---|---|
| Object: race helmet | paint on | the cursor paints the helmet onto his portrait (lando-norris) |
| Object: seltzer can | pour | the pour floods the viewport as the section transition (slosh-seltzer) |
| Object: watch | tell time | its hands show the visitor's local time (the-watch) |
| Object: ball | bounce | bounce it to enter; the site opens from where it lands (dont-board-me) |
| Material: plaster | carve | the page is a relief that birds and faces rise out of (immersive-garden-website) |
| Process: drawing to building | wipe | the line drawing wipes away to the matching photograph (fluid-glass) |
| Process: animation desk | peel, fling | acetate peeled by the first scroll, cels flung on a pivot (thelinestudio-com) |
| Process: weaving | weave | every image redrawn as two-colour line-screen bars (son-daven) |
| Process: sound | vibrate | particles trace Chladni lines and condense into haiku (iyo) |
| Mark: arch | open | the preloader arch rises, widens and dives into the pool (era-residence) |
| Mark: square "O" | multiply | cube, then preloader, map pins and city blocks (hubtown) |
| Mark: 4x4 logo | render | the logo is the dither sub-pixel of all media (lama-lama-2) |
| Story: narrated film | narrate | the voice drives the camera; scrub to take over (gq-ap-the-extraordinary-lab) |
| Story: "zero" university | draw | draw a zero on ice to unlock the manifesto (why-zero) |

4. **Run the tests.** Reject the idea at the first failure.
   - **Source:** it points at one noun in the brief. If it points at a trend (particles, blob, glass, ASCII for its own sake), reject.
   - **Swap:** put a competitor's name on it. If it still works, reject. A generic dither fits anyone; lama-lama-2's "LL" sub-pixel fits one agency.
   - **Play:** the visitor's input causes it (cursor, drag, scroll scrub, click, hold, voice). Watching alone fails; all five Sites-of-the-Year-section sites pass (Rule 5).
   - **Motion off:** freeze it at its most telling frame. The still must state the idea: the watch in the gap of 350px type (the-watch), the arch framing the pool (era-residence), the slab wordmark (aim-ai-modernism-of-kharkiv). Ship that frame as the reduced-motion and no-WebGL state [usability-a11y-perf §3.1, §3.5].
   - **Recurrence:** it returns at 3 or more of loader, transition, nav, hero, footer and 404. everswap's split diamond is the preloader portal, the chapter nav, the frame around the kicker and the closing mask; aim's slabs play at load, mid-scroll and footer; akaru-2's logo letters exit and re-enter on every route change.
   - **Sentence:** one sentence with one verb, no "and".
   - **Budget:** interactive within about 2s of first paint on a mid phone, with a poster before it. igloo-inc's roughly 6s blank loader and era-residence's 7.75s first-visit arch preloader are the counter-examples: the right signature, the wrong length.
   - **Formula:** check the rest of the page against the law's uniqueness formula: the signature artifact, atmosphere that carries below the fold, layered depth (one element crossing a layer), a character display face, one bespoke silhouette (hubtown's bevelled frame, san-rita's chamfered cards, the-watch's 350px type split around the object), a treated nav, real specifics.
5. **Write the spec:** `<Noun> <verb>s <page element> when the visitor <input>. At rest it reads as <still>. It returns at <touchpoints>. Cost: <assets + runtime>.`

## Combining two directions

- The primary owns the first-screen owner, the motion clock and the palette structure. The secondary contributes exactly one named layer: a type voice, an image treatment, a layout device or a sound layer.
- Two clocks only as world versus UI (steven-com: world 4-7s, DOM 0.5s; messenger: springs for objects, held poses for drawn marks; thelinestudio-com keeps stepped blinks and expo moves on separate elements). Never two DOM ease families.
- Never three.

| Pair (primary + secondary) | What the secondary adds | Site |
|---|---|---|
| Playable toy + Process filter | ink-outline render and held poses | messenger |
| Object hero + Editorial | 24vw ghost wordmark, mono spec tables | vast |
| Object hero + Kinetic poster | condensed-caps manifesto and Lando's lime #d2ff00 (about 7% of the page: the STORE button and line-wipe blocks) | lando-norris |
| Flown world + Object hero | one creature carrying the whole timeline | the-power-of-storytelling |
| Editorial + Archive index | a dataset view of about 1,000 thumbnails | tracing-art |
| Process filter + Reel | full-bleed client films as the only colour | artefakt |
| Kinetic poster + Illustrated | Lottie pictogram athletes | champions-for-good |
| Process filter + Material calm | the 400/800/1200 ladder and slow pace | son-daven |
| Archive index + Illustrated | icons that act each chapter out on hover | dropbox-brand |
| Material calm + Flown world | a camera through sculpted universes | cartier-watches-wonders-2025 |

Reject the combination when you see: two first-screen owners entering at once (a 3D object and a 300px kinetic headline); two accents, one per direction; a tempo clash (a 400/800/1200 ladder beside 16ms char skids); a filter on some media but not others; sound in only half the site. Incompatible by default: Material calm + Kinetic poster (tempo), Playable toy + Editorial (captured input against reading), Reel + Flown world unless the footage becomes the world's texture (active-theory-v6 plays its reel inside the chrome and water as one shared video texture).

## Crafted vs slop

| Award habit | Slop version | Crafted version |
|---|---|---|
| Warm off-white ground (at least 9/51: era-residence, floema, fluid-glass, akaru-2, aim-ai-modernism-of-kharkiv, mindmarket, dont-board-me, lando-norris, vast; plus bone panels on the-renaissance-edition and cream content pages on maxima-therapy) | oat-milk cream behind every section | a ground sampled from the subject: lit plaster #e8e8e8 (immersive-garden-website), fog #E6E7E2 (david-whyte-experience), sand #a89474 (son-daven), studio grey #ebebeb (the-watch), pure white (tracing-art) |
| Saturated accent (lando-norris #d2ff00, terminal-industries #abff02, made-with-gsap-1 #C9FE6E) | neon on dots, eyebrows, every button | the owned object colour as a field or a reserved state (opal-tadpole's yellow only on interaction; shed's ultramarine as whole sections); otherwise a tonal step off ground or ink |
| Content hidden until a reveal fires (aim-ai-modernism-of-kharkiv IX2 states; lando-norris clipped lines) | blank sections when a trigger misses | motion on already-visible content with a CSS deadline ([../recipes/boot.html-snippet.html](../recipes/boot.html-snippet.html), [../recipes/motion-core.js](../recipes/motion-core.js)) |
| Grain sheet over the page (son-daven noise at .1 over type) | noise laid over text | grain inside the canvas pass on imagery only (siena-film-foundation adds 0 to +.07 in the post shader, DOM text untouched). shader-development-studio is the near miss: its grain reaches its WebGL-drawn type and is only rescued by a (1 - colour) luminance mask; keep type out of the pass |
| Underline slide on links (aim-ai-modernism-of-kharkiv) | growing underline on hover | a tonal or weight change in place (active-theory-v6 drops links from 700 to 400 and white) |
| Overshoot on UI (maxima-therapy elastic headings; lacoste-polo-factory back-out pills) | bouncy buttons and titles | overshoot only on an illustrative object, once (dont-board-me's ball, brunos-portfolio's reveal disc); UI on `--ease-micro` |
| Periwinkle and violet palettes (hubtown, zentry, champions-for-good, the-power-of-storytelling) | blue-charcoal dark with a lilac accent | a chosen dark: green-black (active-theory-v6), warm brown-black #100904 (oryzo-ai), neutral #121212 (steven-com), #101010 "not blue" (iyo) |
| Fixed background behind everything (pacome-pertant-portfolio fixed grid at .4; artefakt fixed screen-door) | a static sheet trailing the scroll under the nav | the background is the medium and reacts (lama-lama-2's dither answers cursor velocity; floema's foliage shadows follow the cursor) |
| An open Google-shelf face carrying the signature (dont-board-me Bayon, depo-luxe EB Garamond, bennett-clive Inter Bold, mindmarket Inter at 144px, brunos-portfolio Amatic SC) | a free default as the brand voice | a licensed display with a feature that belongs to the brief (zentry's wedge alternates, san-rita's chamfers matching the UI, lando-norris's width axis) |
| Mono HUD labels everywhere (igloo-inc IBM Plex Mono; hubtown Commit Mono at +.16em) | mono as the house voice | mono only on real data (vast's Phonic on specs and dates); prose in the text face |
| Long loader (igloo-inc about 6s near-blank; era-residence about 7.75s on first visit, 4.0s of it a fake progress bar) | a percentage over an empty screen | HTML first, and a loader that is the signature and under about 2s (everswap's diamond hole shows the live scene; hubtown's squares assemble the wordmark) |
| Crushed display (bennett-clive -0.07em; mindmarket -0.06em; champions-for-good line-height .51) | caps jammed until counters close | tracking between -0.04em and -0.01em (corpus p25 to p75 [probe]); leading under .8 only for descender-free caps proofed at size |
| Atmosphere stops at the fold (a world or object hero, then flat sections with boxes) | the law's "flat fill under everything after the hero" | the direction's medium runs the whole scroll: the-watch keeps turning, dismantling and relighting its one object as the field shifts from studio grey to near-black; son-daven pushes every illustration on the page through the same line-screen shader |
| Lens halos and light spill (the-power-of-storytelling halo pass) | a glow ring behind the hero object | one directional key with falloff and a contact shadow [webgl-3d-stack §5] |

## Exemplars

- **lando-norris**: object plus poster at SOTY level: a cursor-played signature, a width-axis grotesk with a same-cap-height serif swap, an owned accent.
- **igloo-inc**: flown-world choreography: outline and shockwave, then geometry 1.1s later, bricks at 2s, HUD at 4.5s, environment last at 7.5s.
- **the-watch**: an object occluding 350px type; the still survives motion off; the visitor's local time on the hands.
- **depo-luxe**: reel as interface with three type sizes, a 14-25% veil and zero UI accent.
- **aim-ai-modernism-of-kharkiv**: a wordmark as the motion system across load, scroll and footer; the 9.5:1 two-tier scale.
- **champions-for-good**: kinetic poster: duotone pairs, 22vw caps, skid-in chars, opt-in foley.
- **mindmarket**: an illustrated B2B services site that reached SOTM without 3D.
- **fluid-glass**: material calm told as one mask from drawing to build, on a single ease family.
- **lama-lama-2**: a process filter derived from the mark itself.
- **gil-huybrecht**: an archive index with one type size and a contact-sheet grid.
- **messenger**: toy plus filter, with two motion languages kept apart.
- **everswap**: one mark reused at four touchpoints and camera-first pacing.

Full entries: [casebook.md](casebook.md). Colour and imagery detail: [color.md](color.md), [imagery.md](imagery.md).

## Evidence

- `data/teardowns/<slug>.json`, all 51: fields `signature`, `first_screen`, `typography`, `color`, `layout`, `motion`, `imagery`, `three_d`, `navigation_interaction.sound`, `slop_risks`, `scores`. The ten clusters, the per-direction counts (3D present, sound present, display px ranges, jury means 7.63-7.79) and the 9/51 warm off-white grounds were computed from these files on 2026-09-25 and are this file's synthesis, not an Awwwards category. Audit pass 2026-09-25 re-checked about 50 values (sizes, hexes, ratios, ease counts such as the-watch power3.inOut ×97 and depo-luxe Power2.easeIn ×61, era-residence and son-daven's 400/800/1200 ladder, steven-com's two clocks) against the teardowns.
- `references/casebook.md`, and the digests `evidence/digests/{signatures,typography,color,imagery,three_d,content}.md`.
- [probe] `data/probe_summary.json`: reduced-motion CSS rules 11/51 (same-origin stylesheets only); 3D asset files 26/51; display median 80px at 1440 and 46.8px at 390; display letter-spacing p25 -0.04em, min -0.07em; display line-height p25 .83.
- [stats] `data/stats.md`, recent_2024_plus cut: hue families near-black 152, near-white 115; palette_base dark+light pair 86, dark-dominant 79, mid-tone 66, light-dominant 44. The submission palette field holds at most two swatches in this cut (0: 300, 1: 29, 2: 246), so it is not evidence of how many colours a site uses.
- [fonts] `data/font_census.json` summary keys: the Google Fonts service on 58 of 554 live winners; Inter on 60 sites overall but loaded from Google on 12; Adobe Fonts on 37.
- Research: awwwards-editorial §0, §3.1, §3.4, §4.2, §4.3; webgl-3d-stack §3, §4.8, §5; motion-stack §2.2-2.3 (token names as shipped in ../recipes/tokens.css); usability-a11y-perf §2.F, §3.1, §3.5; imagery §4.5.
- House law: `deslop-law.md` (cream background, saturated accent, invisible-content trap, grain over content, underline-fill hover, hover boop, cool blue-charcoal, fixed background, Google font rotation, Didone serifs, monospace as house voice, radial glow halo, cramped display type, botched glass, flung-to-the-edges, flat fill after the hero, dead-looking, the signature formula).
- Retrieval gaps: sound is read from bundles and requests, so lazily loaded audio can be missed; iyo is tagged Sound-Audio but no audio code was found. cartier-watches-wonders-2025's hero type is WebGL MSDF, so its display size is inferred. zentry's awarded 2024 version is reconstructed from jury videos. dont-board-me's and igloo-inc's Site of the Year status is inferred from list membership. The akaru-2 row-fill direction logic is marked inferred in its teardown. The teardowns' `three_d.present` flag is inconsistent for 2D-shader-only sites (lama-lama-2 counted, son-daven not). Cluster membership is one analyst's call; hubtown, cartier-watches-wonders-2025 and the-power-of-storytelling sit near a boundary.
