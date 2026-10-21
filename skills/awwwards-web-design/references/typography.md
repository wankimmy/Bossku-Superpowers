# Typography for award-level sites

Last updated: 2026-09-25

Use this when: choosing typefaces, setting the type scale, or building a type-driven signature (poster display, split-line reveals, variable axes, type as image, WebGL text) for a site aimed at Awwwards SOTD or SOTM.

## Rules

1. Pick the display regime from what owns the first screen. Quiet (under 60px at 1440) when an object, film or world carries the scale: 12 of 47 measured winners. Statement (60-150px): 16. Poster (150px and up): 19, of which 11 reach 200px+ [teardowns]. Probe median is 80px at 1440 and 46.8px at 390 [probe].
2. The face that carries identity is licensed or self-hosted and off the Google shelf. 1,026 of the 1,169 family-name strings shipped by 554 live winners (88%) appear on exactly one site (996 of 1,143 case-folded), and only 58 of 554 (10.5%) load Google Fonts [fonts]. Check the banned list at the top of section 3 before picking.
3. One display voice, one quiet companion, an optional data mono. Median 2 families per site; 397 of 554 (72%) ship 1 to 3 [fonts]. The body may be `system-ui` (law).
4. Size display with `clamp()` anchored in `rem`, max at most 2.5x min, or treat the word as a logotype with the real text elsewhere. Never derive the root font-size from the viewport: about 12 of 51 teardowns do (son-daven, zentry, era-residence, maxima-therapy, the-watch) [teardowns], which breaks browser zoom (WCAG F94) [typography §4.2].
5. Tighten tracking as size grows and stop before glyphs touch. Grotesk: -0.02em at 48-100px, -0.03 to -0.05em at 100-200px, down to -0.065em only for a single poster word. Serif: 0 to -0.03em. Small caps labels: +0.04 to +0.1em. Probe display median -0.023em, range -0.07 to +0.02em [probe]. At the tightest setting zoom into the closest pair (`rn`, `LT`, a separator dot); if counters or joins touch, back off 0.01em (law, "Cramped display type").
6. Display leading 0.85-0.95 for one or two lines. Go to 0.77-0.8 only on caps-only or descender-free faces (siena-film-foundation, dont-board-me). Pad every line mask by 0.12em ([../recipes/motion-core.css](../recipes/motion-core.css) `.rv-line-mask`).
7. Build a two-tier scale: huge display, small text, few middle steps (13 of 51 teardowns describe exactly this). Floor body at 16px even though the winners' median body is 14.4px [probe].
8. Text is visible by default. A split reveal moves text that is already on screen, holds a hidden state only while its tween runs, has a completion failsafe and reverts. About 45 of 51 teardowns flag content hidden until a reveal fires.
9. Emphasis is one tonal step or one face swap inside a headline of one or two lines. Never a saturated word, never an accent word stranded at the foot of a 3+ line stack (multi-line display stacks flagged on 12-15/51).
10. Mono only on data tokens (times, prices, coordinates, IDs), and give each small role its own treatment. No tiny kicker above every section head (law). "One label treatment everywhere" is flagged on 24/51 teardowns, mono as the house voice on 15/51.
11. Every word drawn in canvas or WebGL has a DOM twin for assistive tech, search and no-WebGL visitors. About 15-17 of 51 draw text in WebGL.
12. Preload at most two WOFF2 files, use `swap` with a generated metric-matched fallback, and split or measure text only after `document.fonts.ready`. Only 11 of 58 probed winners ship the fallback [usability-a11y-perf §1.5].
13. Before shipping, grep production CSS for `Trial`, `Test` and `Demo`, and confirm every declared family renders. aim-ai-modernism-of-kharkiv ships a TRIAL cut and maxima-therapy serves `ABCDiatypeRoundedPlusVariable-Trial.woff2`; pacome-pertant-portfolio declares a family that never loads, so visitors get Helvetica Neue/Arial.

## 1. The measured scale

Probe values are from the 51 audited winners at 1440x900 and 390x844 [probe]:

| Metric | p25 | median | p75 | range |
|---|---|---|---|---|
| Display px at 1440 (n=47) | 40.8 | 80 | 150 | 11 to 345.6 |
| Display px at 390 (n=51) | 32 | 46.8 | 80 | 15 to 160 |
| Display tracking, em (n=27) | -0.04 | -0.023 | -0.01 | -0.07 to +0.02 |
| Display line-height ratio (n=44) | 0.83 | 1.0 | 1.0 | 0.77 to 1.5 |
| Body px at 1440 (n=51) | 12.6 | 14.4 | 17 | 9 up (max is an outlier) |

Desktop-to-phone display ratio is about 1.7x at the median (80 to 46.8) and 1.9x at p75.

Ladders to learn the logic from, not the values:

| Site | Display face | @1440 | @390 | Tracking | Leading |
|---|---|---|---|---|---|
| champions-for-good | Druk Condensed Super caps | 316.8 (22vw) | 72 | normal | 0.51, inline small words |
| shed | Owners 600 caps | 231.3 (16.06vw) | 100 | -0.01em | 0.9 |
| tracing-art | Bradford LL serif | 207 | 41.6 title, 29 headline | -0.03em | 1.0 |
| the-renaissance-edition | PP Neue Montreal 700 | 193.7 (clamp) | 72 | -0.03em | 0.9 |
| thelinestudio-com | Denim VF, wght 500 | 175 (12.15vw) | 72 | -0.04em | 0.8 |
| lando-norris | Brier serif / Mona Sans VF | 110 / 105.8 | 43.3 | -0.023 / -0.008em | 0.83 / 0.91 |
| siena-film-foundation | Neue Brücke caps | 89.6 | 32 | -0.03em | 0.77 |
| opal-tadpole | Roobert 300 | 83.9 | 40 (archived CSS) | -0.01em | 1.04 |
| floema | Zimula VF, wght 500 | 57.2 (clamp) | 32 | -0.04em | 1.05 |

Decisions:
- **Tracking and leading ladder.** made-with-gsap-1 is the cleanest measured ladder: 250px at -0.04em / 0.8, 140px at -0.03em / 0.85, 120px at -0.02em / 0.95, 48-65px at -0.02em / 1.02, 18px body at 0 / 1.4. son-daven sets every display size at -0.064em serif caps against +0.08em sans text: opposite tracking is the contrast. Full table in [typography §4.4].
- **Two tiers, no middle.** aim-ai-modernism-of-kharkiv has nothing between 16px and 79px; dont-board-me is "shout or caption" at 21:1; the-watch runs 350px against 12px body (29:1). A quiet tier works too: gil-huybrecht sets the whole index at one size (16.32px) and lets the grid carry hierarchy; steven-com holds its headline at 51px so the object owns the screen.
- **Scale inside one line.** champions-for-good sets 43.2px connector words (3vw) on the baseline beside 316.8px NETWORK (7:1 in one line).
- **Tokens.** Use the steps in [../recipes/tokens.css](../recipes/tokens.css): `--step-display` (probe median, 47 to 80px, max 96), `--step-hero` (56 to 121px, max 140), `--step-poster` (probe p75, 80 to 150px, max 180), all rem-anchored with max at most 2.5x min, plus `.fluid-type` for one-off sizes. Pick ONE display step per page. Formula: `clamp(MIN/16 rem, (MIN - slope*390)/16 rem + slope*100vw, MAX/16 rem)`, `slope = (px@1440 - px@390)/1050`.
- **Upper cap.** Test at 2560. akaru-2 wrote its large-screen step as an unknown media type that never matches, so its 9.6rem H2 grows to 171px at 2560.
- **Measure.** Display `max-width: 12-18ch` (the most common `ch` values across 80 winner stylesheets [typography §4.1]); body 30-65ch; `text-wrap: balance` on headings (13/51 ship `text-wrap` balance or pretty [probe]), but not on elements SplitText will split [motion-stack §4.2].

## 2. What winners ship: the font census

From 554 live winners of the 575-site 2024+ corpus [fonts]:
- 46 of 554 expose no web font at all (likely system stacks or canvas-only type).
- Families per site: 1 (126 sites), 2 (172), 3 (99), 4+ (111). Median 2, mean 2.82. Heavy counts come from mono, script and declared-but-unused faces.
- Hosting: Webflow CDN 72 sites, Framer 32, Google Fonts 58 (10.5%), Adobe Fonts 37 (6.7%). Inter appears on 60 sites but is Google-served on only 12, so most Inter copies are self-hosted.
- In the 51 audited teardowns only Neue Montreal and Inter load on two sites; every other family appears once [probe].

Top families and their standing under the house law ("Google shelf" = served by the Google Fonts CSS API, checked 2026-09-25):

| Family | Sites /554 | Law status |
|---|---|---|
| Inter | 60 | banned as signature; the law calls it the most common slop font |
| Geist Mono | 27 | Google shelf; data tokens only |
| PP Neue Montreal (+ "Neue Montreal" 13) | 24 + 13 | licensed (Pangram); the most shared licensed grotesk, so it needs a composition idea |
| Geist | 20 | Google shelf; reads as the dev-tool default by exposure (inference) |
| Fragment Mono, IBM Plex Mono, JetBrains Mono | 13, 12, 9 | banned |
| Poppins, Archivo, Instrument Sans, DM Sans, Manrope | 12, 11, 10, 10, 9 | Google shelf; Archivo banned by name |
| Playfair Display, Instrument Serif, Cormorant Garamond | 9, 8, 5 | banned (Didone, "tasteful swap", Cormorant) |
| Suisse Int'l | 9 | licensed (Swiss Typefaces) |
| Switzer, Satoshi, General Sans | 7, 5, 4 | Fontshare; General Sans flagged by the law, Satoshi by exposure (inference) |

The lesson is the long tail, not the head: winners are identified by a face nobody else ships. Typography is a featured element tag 198 times in the 2024+ corpus, sixth after animation, 3D, WebGL, scroll and interaction [stats].

## 3. Display archetypes

Banned from carrying the brand (law): Inter, Space Grotesk, Sora, Syne, Archivo, Onest, Darker Grotesque, Geologica, Hanken Grotesk, Spline Sans, Schibsted Grotesk, Gabarito, Figtree, Quicksand, Work Sans (the Fraunces + Work Sans pair); Bagel Fat One, Baloo, Fredoka, Chewy, Lobster; Fraunces, Cormorant, Bodoni and the Didones, Petrona, Hedvig Letters Serif, Brygada 1918, Young Serif; JetBrains Mono, IBM Plex Mono, Spline Sans Mono, Fragment Mono; the "tasteful swaps" Big Shoulders, Newsreader, Instrument Serif, Bricolage; Clash Display and General Sans. Any other Google Fonts face is still off-limits for the signature line (law rule 1).

Each archetype: when to use it, faces seen on winners (foundry, licence path), a free alternative that is off the Google shelf and not on the law's lists, and its slop tell. Licence metrics are from [typography §3].

**A. Characterful grotesk.** The brand is contemporary and the drama comes from scale and composition.
- Seen: Owners (shed, vast; OH no Type Co, confirmed on ohnotype.co 2026-09-25), Lay Grotesk (gil-huybrecht, made-with-gsap-1; Due Studio per [typography §2.1], from EUR 60 per style), Zimula VF (floema; La Bolde Vita), Neue Brücke (siena-film-foundation; Due Studio per [typography §2.7]), NB Architekt (active-theory-v6; Neubau), Roobert (opal-tadpole, david-whyte-experience; Displaay, perpetual, priced by company size), DB Sharp Grotesk VF (dropbox-brand; custom Sharp Type cut).
- Free: Apfel Grotezk (Collletttivo, OFL), Pally (Fontshare, named by the law), Karrik (Velvetyne, OFL).
- Tell: Space Grotesk, Syne, Sora, Clash, General Sans; Satoshi by exposure (Fontshare's most-viewed family, inference [typography §2.1]).

**B. Neutral neo-grotesk at poster scale.** Law conflict: "the identity never rests on a neutral grotesque." Use B only when a non-type artifact (3D object, film, photography) owns the first screen and the grotesk is the voice, not the signature. Even then give it one owned move: per-glyph optical margins, a drawn wordmark, a stylistic-set glyph, or a scale jump inside one line (section 5).
- Seen: Suisse Int'l (terminal-industries, lama-lama-2; Swiss Typefaces, lifelong, no domain or visitor limits), PP Neue Montreal (the-renaissance-edition, odd-ritual, champions-for-good body; Pangram, per domain, pageview cap, 1-year term), GT America (gq-ap-the-extraordinary-lab; Grilli, unique monthly visitors), Aeonik Pro (fluid-glass; CoType), Graphik and Atlas Grotesk (tracing-art, dropbox-brand; Commercial Type, domains plus unique monthly visitors), ABC Monument Grotesk (leo-parpeix-portfolio-2026 body; Dinamo, company size, self-host and subset allowed).
- Free: Switzer (Fontshare) only where neutrality is the point; `system-ui` for body.
- Tell: Inter carrying the brand. bennett-clive (Inter Bold, -0.07em, lh 0.77) and mindmarket (Inter 500, -0.06em) survive on choreography; the law still bans it as the signature.

**C. Condensed and compressed caps.** Poster energy, sport, film, drinks. Caps have no descenders, so leading can drop to 0.78-0.9.
- Seen: Druk Condensed Super plus its real italic (champions-for-good) and Druk Wide (artefakt; Commercial Type), F37 Stout (san-rita; F37), Robuck Rounded (maxima-therapy; foundry unknown), Steelfish (slosh-seltzer; inferred Typodermic), Field Gothic Trimmed (steven-com; inferred Frere-Jones), ZentryScreamer (zentry; bespoke), Bayon (dont-board-me; Google shelf, so not a model to copy).
- Settings: tracking 0 to -0.02em (the cut is already tight); +0.02 to +0.06em for wide-set caps [typography §2.6].
- Free: Tanker (Fontshare, named by the law).
- Tell: Anton, Bebas Neue, Oswald, Archivo Narrow (5, 5 and 2 sites in the census for the first three); one face shown solid, outlined and coloured as "three fonts".

**D. Editorial serif.** Culture, hospitality, publishing, considered luxury. The law's "signature serif headline": a serif with real character, set large. Thin high contrast alone is not premium.
- Seen: Canela Text Thin 100 (david-whyte-experience; Commercial Type), Bradford LL (tracing-art; Lineto), Reckless (shed accent; Displaay), Brier (lando-norris; Type Department per [typography §2.7], teardown: unidentified), Feature Display 200 (everswap; inferred Commercial Type), PSTimes (immersive-garden-website; unverified), HWCigars (the-renaissance-edition; inferred Heavyweight), KTF Metro Roman (son-daven; Kyiv Type Foundry). STIX Two Text (shader-development-studio) and Literata (oryzo-ai) are Google-shelf faces: not models for a signature.
- Free: Sentient and Gambarino (named by the law), Zodiak, Erode, Boska (all Fontshare ITF FFL); Ouroboros (Velvetyne, OFL) for art-nouveau display.
- Tell: Cormorant, Playfair, Bodoni and the Didones, Fraunces, Instrument Serif, Newsreader, Young Serif, EB Garamond carrying a brand (depo-luxe). Compressed Didone-derived caps (Ambroise on era-residence, served via Adobe Fonts) are defensible only with a brand-owned or clearly distinctive cut.

**E. Variable and kinetic.** Type itself is the interaction: weight or width answering scroll or pointer, a sans-to-serif axis. `variable-font-axes` appears on 18/51 sites [probe].
- Seen: DB Sharp Grotesk VF (dropbox-brand: wght 250-900, wdth, ital; specimen sliders), Mona Sans VF (lando-norris: `wdth` 93 at `wght` 660 for the manifesto, `wght` 800 `wdth` 86 for button caps; GitHub, OFL, and on the Google shelf, so only as neutral UI under a licensed voice), Denim VF (thelinestudio-com: weights 500 / 470 / 440 / 300 by role), Avantt VF (leo-parpeix-portfolio-2026; Displaay), Zimula (floema: custom `cnct` axis pinned at 1000).
- Free: Collletttivo Sprat, Halibut, Sinistre, Aujournuit (OFL); Fontshare variable cuts of Zodiak (100-900), Boska (200-900), Sentient (200-700) and Pally (400-700) for weight motion.
- Tell: axis motion on body text (every frame reflows), animating every word, proximity effects on touch.

**F. Mono for data.** Timecodes, specs, coordinates, counters.
- Seen: Aeonik Mono (fluid-glass), PP Neue Montreal Mono (made-with-gsap-1), Centra Mono (san-rita), Phonic (vast), FK Grotesk Mono (slosh-seltzer), ABC Diatype Rounded Mono (maxima-therapy), Geist Mono (terminal-industries, Google-served), Sometype Mono (lama-lama-2, Google-served).
- Free: Necto Mono (Collletttivo, OFL), Steps Mono (Velvetyne, OFL). Sometype Mono and Azeret Mono are also on the Google shelf: acceptable on data tokens only, never on labels.
- Tell: JetBrains, IBM Plex, Fragment, Spline Sans Mono; any mono on every label.

**G. Drawn lettering and bespoke faces.** 11 of 51 winners carry identity in a drawn wordmark: one SVG path per letter (akaru-2), a square-O glyph that becomes the 3D object (hubtown), a serrated inline-SVG logotype (son-daven), extruded slot-cut 3D letters (messenger), hand-drawn marker (san-rita), a Rive script (opal-tadpole). Brand-owned faces (Cartier's Brilliant Cut and Fancy Cut on cartier-watches-wonders-2025, Lacoste's own sans on lacoste-polo-factory) read as the brand, not as a web font.
- Rule: an experimental or drawn face gets one job (the wordmark or one hero word). It never sets nav, buttons, prices or body.

Licence paths at a glance [typography §3]: Pangram per domain with a pageview cap and a 1-year term (put renewal in the handoff); Swiss Typefaces and Displaay perpetual; Dinamo by company size with self-hosting and subsetting allowed; Grilli and Commercial Type by monthly visitors; Klim by page views, no expiry; OH no by page-view tiers; Fontshare free for commercial use, self-host, no modification; Velvetyne and Collletttivo OFL. The client owns the licence. Trials are never for live use. Render every candidate at display size before choosing (law).

## 4. Pairing logic

1. **Superfamily first.** One family across widths, weights or optical cuts: Aeonik Pro + Aeonik Mono (fluid-glass), Owners + Owners Text + Phonic mono (vast), ABC Diatype Rounded + Rounded Mono + Robuck for display (maxima-therapy), Suisse BP Int'l + Sometype Mono (lama-lama-2).
2. **Contrast on one axis.** Serif story against grotesk metadata: Bradford for narrative 30-207px, Graphik 10-14px for data (tracing-art); Canela Thin display, Roobert UI (david-whyte-experience); PSTimes display, Helvetica Neue chrome (immersive-garden-website). Change class or width or weight, not all three.
3. **A three-voice system only with strict roles.** shed: Owners caps shout, Sequel Sans talks, Reckless serif handles asides. the-renaissance-edition: Neue Montreal for names, one Imperial Script swash initial via `::first-letter`, HWCigars for the sentence.
4. **Match cap heights when two faces share a line.** lando-norris sets the Brier serif word at 8.25rem against the grotesk's 7.9375rem (about +4%) so both cap heights span the same pixel rows, and runs Mona Sans at `wdth` 93 so the two voices share one colour of line. In CSS: `font-size-adjust: cap-height 0.7` on both faces (Baseline 2024), with each value read from the file as `OS/2.sCapHeight / head.unitsPerEm` (fontTools snippet in [typography §5]; it prints `sxHeight`, swap in `sCapHeight`).
5. **Different roles, different treatments.** Nav in the text face at 15px medium, captions in the text face with a tonal colour, data in mono, and only one role in tracked caps. akaru-2 even tracks its uppercase labels negative (-0.05em) instead of the usual tracked-out caps.
6. **Never reuse a pairing from a previous project** (law, "Default Google fonts" rule 2). Check earlier builds in this workspace before choosing.

## 5. Signature type moves

### 5.1 Giant fluid display

Seen: 22vw Druk (champions-for-good), 16vw caps over photography with a 0.75vw gutter (shed), a 24vw tonal ghost wordmark behind a transparent WebGL object (vast), a 350px h1 with the product standing in its word gap (the-watch).

```css
.poster { font: 700 var(--step-poster)/0.88 var(--font-display); letter-spacing: -0.04em;
          max-width: 14ch; text-wrap: balance; font-synthesis: none; }
/* Line masks: copy .rv-line-mask from ../recipes/motion-core.css. Pad 0.12em, then overlap
   each later mask by -0.24em; a plain margin-block: -0.12em collapses between siblings. */
```

- Fit-to-width wordmark: `text-fit: grow` where supported (Chrome 150+, experimental), else the JS measure-and-scale fallback in [typography §6.1]; re-measure after `document.fonts.ready`.
- Law placement for a footer wordmark: on the layer above any texture, centred or on the grid, a deliberate case, room above, anchored flush to the bottom edge and bleeding slightly off it while every cap top and ascender stays whole, no gradient inside the type. Zoom into the clipped edge before calling it done. Only descender-free words may take the negative bottom margin (`margin-block-end: -0.06em`).
- Poster sizes beyond 2.5x their minimum are either a logotype (image of text, the words present as real text elsewhere) or zoom-tested to 200% at 1024-2560px [typography §4.3].

### 5.2 Masked line reveals that keep text visible

Seen: SplitText named on 33/51 teardowns; masked line rises on roughly 20-24/51; SplitText on 54 of 117 recent SOTD bundles [motion-stack §1.3]. Most winners start text at opacity 0 or parked under its mask, which the law forbids.

- Build it with [../recipes/motion-core.js](../recipes/motion-core.js) `data-reveal="lines"` (headings only, split with `autoSplit`, reverted on complete, never armed on anything on screen at boot) and the mask padding in [../recipes/motion-core.css](../recipes/motion-core.css). Above the fold, use `data-intro` with the 2s CSS deadline in [../recipes/boot.html-snippet.html](../recipes/boot.html-snippet.html); motion-core forces the intro to its end state after `introFailsafe` (3500ms).
- Winners' own clip-safe details: shed uses `overflow-y: clip` (not `hidden`, so nothing is cut sideways) plus `padding-bottom: .12em` on lines with descenders; fluid-glass pads masks with `margin: -2rem 0; padding: 1rem 0` and splits after `document.fonts.ready`.
- Visible fallbacks when a fade is wanted: cartier-watches-wonders-2025's loader letters run from opacity 0.3 to 1, never from 0; a y-settle with no opacity is the default ([../recipes/motion-core.js](../recipes/motion-core.js) `data-reveal="settle"`).
- Split `h1`-`h6` only. SplitText's `aria: "auto"` puts `aria-label` on the element, which ARIA 1.2 prohibits on paragraphs and generic elements [motion-stack §4.2]. steven-com's pattern for anything else: the real text in a visually hidden span, the animated clone `aria-hidden` and `data-nosnippet`.
- Motion detail: [./motion.md](./motion.md).

### 5.3 Variable-axis animation

Seen: dropbox-brand binds width, weight and italic to sliders and re-rolls axes per character; thelinestudio-com tunes one axis in odd steps by role; active-theory-v6 drops filter-link weight from 700 to 400 on hover in a left-aligned list, where nothing follows the word, so the width change is invisible.

```css
@font-face { font-family: "Display"; src: url(/fonts/display-vf.woff2) format("woff2");
  font-weight: 200 900; font-stretch: 75% 125%; font-display: swap; }   /* declare the real fvar ranges */
.kinetic { display: inline-grid; font-weight: 300; font-stretch: 110%; }
.kinetic::after { content: attr(data-text); font-weight: 800; font-stretch: 110%;   /* reserves the widest state */
                  visibility: hidden; height: 0; overflow: hidden; }
@media (hover: hover) and (prefers-reduced-motion: no-preference) {
  .kinetic { transition: font-weight var(--dur-4) var(--ease-enter); }
  .kinetic:is(:hover, :focus-visible) { font-weight: 800; }
  @supports (animation-timeline: view()) {
    .kinetic--scroll { animation: wght-in linear both; animation-timeline: view(); animation-range: entry 0% cover 50%; } } }
@keyframes wght-in { from { font-weight: 250; font-stretch: 125%; } to { font-weight: 800; font-stretch: 75%; } }
```

- Markup: `<a class="kinetic" data-text="Projects" href="...">Projects</a>`. Without the reserved width a weight change reflows everything after the word on its line.
- Use `font-weight` and `font-stretch` for registered axes; keep `font-variation-settings` for custom axes (floema's `cnct`) and register them with `@property` so they interpolate. Pointer-proximity weight code: [typography §6.3].
- Short strings only. On phones tie axis motion to scroll or leave it static. CSS scroll timelines are not stopped by the reduced-motion net in tokens.css, so keep them inside the media query as above.

### 5.4 Mixed serif and grotesk word swaps

Seen: lando-norris swaps one word per all-caps clause from Mona Sans to Brier at the same cap height; the-power-of-storytelling puts one italic serif word per line into a single-weight sans; tracing-art sets articles in italic and nouns in roman at the same size; champions-for-good leans words two honest ways, a real italic cut and a `skew(-10deg)` applied after the letters land; era-residence crosses condensed caps with a script word over the baseline.

```css
.swap { font-family: var(--font-grotesk); font-synthesis: none; }
.swap em { font-family: var(--font-serif); font-style: normal; font-size: 1.04em;   /* tune to match cap height */
           color: color-mix(in oklab, currentColor 70%, var(--bg)); }            /* tonal, never a saturated pop */
```

- One swap per headline of one or two lines. The swapped word belongs to the phrase's meaning (the verb or the key noun), never a stray word at the foot of a stack.
- Law limit: a kicker plus one big serif sentence with a single italic word is the "big serif statement block" slop beat. The swap has to sit in a composed headline (scale jump, object in the gap, matched cap heights), not in a philosophy section.
- Tonal two-tone without a second colour: odd-ritual keeps its first line at full white and dims the rest to opacity 0.5 of the same white (its three-line stack is itself flagged); iyo wraps the headline's tail at opacity 0.5; made-with-gsap-1 uses a grey lead-in with ink keywords. Check that the dimmed part still passes 3:1 at display size and 4.5:1 below 24px.
- Italic overhangs get clipped by masks and `background-clip`: the-power-of-storytelling pads each italic char (0.23em 0.2em 0.6em) and cancels it with a -0.35em margin. Keep the padding, drop its gradient fill (law: gradient poured into type).

### 5.5 Mono metadata

igloo-inc turns labels into live data (zero-padded displacement readouts, tabular temperatures). The teardowns flag terminal-industries, fluid-glass and vast because their mono also covers buttons, eyebrows and captions. Wrap the data, not the label:

```css
.meta { font: 400 var(--step-meta)/1.35 var(--font-text); color: color-mix(in oklab, currentColor 62%, var(--bg)); }
.meta :is(time, data, .coord) { font-family: var(--font-mono); font-variant-numeric: tabular-nums slashed-zero; }
```

### 5.6 Marquee type

Seen on 16/51. lando-norris runs two MSDF rows in opposite directions (serif over grotesk); ponpon-mania turns only titles longer than 20 characters into a duplicated marquee; shed hides its subtitle marquee below 1024px. Build it with [../recipes/motion-core.js](../recipes/motion-core.js) `data-marquee` (markup contract in [../recipes/motion-core.css](../recipes/motion-core.css)): CSS loop, 60-100 px/s, a visible pause button (WCAG 2.2.2), a static wrapped row under reduced motion or without JS, the duplicate group `aria-hidden`. Real content only: never a strip of invented client names.

### 5.7 Type as image, texture and stage

- **Object in the word gap.** the-watch keeps the h1 in HTML and sizes its word gap to the object's projected width, with the transparent canvas above it. vast puts the model over a 24vw ghost wordmark at a 1.19:1 tonal step (#ece8e3 on #fdfcf4; decorative, so the product name also exists as real text). oryzo-ai composites its RISE masthead behind the coffee-cup lid inside the WebGL layer (inferred texture) while the rest of the magazine cover stays DOM text.
- **Images and media inside display text.** floema opens a 51px statement with a 149x206px photo so the first line indents around it; zentry and opal-tadpole put media chips or looping clips inline in a statement.
- **Type as footage.** gq-ap-the-extraordinary-lab ships its hero title as a white-on-black video used as luminance, so type takes the same grain and fringe as the 3D, and cuts a separate narrow version ("EXTRA-") instead of shrinking one layout.
- **Depth.** mindmarket sandwiches its ribbon lettering between a photo and a people cutout (SVG under the cutout, one segment repeated above).
- **Texture on type.** The law allows grain masked onto ONE display word as a deliberate move; never a sheet of grain over running text (grain over text flagged on 9/51). For legibility over busy imagery, everswap uses a soft `text-shadow: 0 0 .12em rgba(0,0,0,.3)` rather than a heavier weight.

### 5.8 MSDF and WebGL text, when needed

About 15-17 of 51 winners draw text in WebGL: MSDF atlases (cartier-watches-wonders-2025, slosh-seltzer, lando-norris, oryzo-ai), troika SDF on curved rings (steven-com), Slug GPU glyphs (messenger), 3D letter meshes (everswap, san-rita), pmndrs uikit panels (shader-development-studio), pre-blurred text layers instead of depth of field (igloo-inc). More bake lettering into video, particles or textures (gq-ap-the-extraordinary-lab, iyo, ponpon-mania).

Use it only when the type must share the 3D pass: occluded by or occluding an object, lit, distorted by the same fluid or post shader, or laid on a curve in depth. Otherwise DOM text over the canvas is sharper, cheaper and accessible. Scene setup: [./webgl-3d.md](./webgl-3d.md) and [../recipes/three-hero.js](../recipes/three-hero.js).

```js
import { Text } from 'troika-three-text';          // 0.52.5 on npm, 2026-09-25; three r186
const size = 0.42;                                  // em-height in world units
const title = new Text();
Object.assign(title, { text: 'Harbour', font: '/fonts/display.woff', fontSize: size,
  letterSpacing: -0.03 * size,                       // world units, not em: -0.03em
  anchorX: 'center', anchorY: 'middle', color: 0x111111 });
title.sync(); scene.add(title);                      // troika reads .ttf/.otf/.woff, not .woff2 (README)
```

- Always set `font`: troika's default is Roboto from the Google CDN, and its unicode fallbacks load from jsDelivr unless `unicodeFontsURL` (the property name in the 0.52.5 build) points at your own copy. Confirm the licence covers serving the file to a WebGL renderer.
- DOM twin: lando-norris keeps real headings as screen-reader elements (`clip-path: inset(50%)`); everswap keeps its `h1` `visibility: hidden` and reads its bounding box to place the 3D wordmark. Particle words: sample the DOM heading into points, keep the heading in the DOM [webgl-3d-stack §4.5].
- Never ship canvas-only copy: iyo's haiku are JPG textures (words1-9.jpg) invisible to screen readers and search; messenger has no DOM text at all.

### 5.9 Scramble, roll and other text hovers

- Scramble appears on 7/51. hubtown reserves GSAP ScrambleText for interactive strings (buttons, nav on hover, map labels) and keeps headlines on a random-order char fade; each nav link holds an `sr-only` full label plus an invisible copy that reserves the width, so hovering never reflows.
- Hover states that never move the box: the character roll (lando-norris gives each split char `text-shadow: 0 var(--text-offset) currentColor` and moves chars `y: -100%`; CSS version in [typography §6.9]), a tonal shift, or a weight change with reserved width (5.3). Underline wipes and grows are banned by the law (flagged on 14/51, e.g. cartier-watches-wonders-2025 and shed); mindmarket's animated wavy underline falls under the same ban.

### 5.10 Micro-typography that juries notice

- `text-box: trim-both cap alphabetic` on headline classes (the-renaissance-edition on every headline, gil-huybrecht on info rows) so spacing is optical, not half-leading. Trim to `text` for accented words. Support: Chrome 133, Safari 18.2, Firefox 154 [typography §6.1].
- Per-glyph optical margins: thelinestudio-com adds a class per first letter and shifts it (`.letter-H` -0.07em, `.letter-a` -0.032em) so 175px words sit flush on a 6.7px gutter; mindmarket pulls its footer word -0.07em. That flush edge is a display-only composition; running text keeps a real gutter (law, "Text jammed against the edge").
- Stylistic sets per glyph: zentry wraps one letter per word in `<b>` with `font-feature-settings: "ss01"`, spreading the logo's wedge cut into every headline.
- Numbers: `tabular-nums` on counters and prices; CSS counters for Roman numerals (the-renaissance-edition renders index numbers and even prices with `counter(..., upper-roman)`); `"case"` on all-caps punctuation.
- Book moves: a first-line indent of one grid column plus gutter (lama-lama-2), a masthead justified to the width of the tagline with `text-align-last: justify` (depo-luxe), a footnote apparatus inside display text (aim-ai-modernism-of-kharkiv).

## 6. Font loading without layout shift

Winners' state [usability-a11y-perf §1.5]: `font-display: swap` on 53/58, a metric-matched fallback on 11/58, a font preload on 15/60. Shipped formats across the 51 teardowns: woff2 on 36, ttf on 10, otf on 8, woff on 6 [probe] (some ttf/otf feed WebGL text).

```html
<link rel="preload" href="/fonts/display-700.latin.woff2" as="font" type="font/woff2" crossorigin>
<style>
  @font-face { font-family: "Display"; src: url(/fonts/display-700.latin.woff2) format("woff2");
               font-weight: 700; font-display: swap; }
  @font-face { font-family: "Display Fallback"; src: local("Arial");
               size-adjust: 104%; ascent-override: 92%; descent-override: 24%; line-gap-override: 0%; } /* paste generator output */
  h1, h2 { font-family: "Display", "Display Fallback", sans-serif; }
</style>
```

- Generate fallback metrics, never guess: `next/font` does it automatically; elsewhere use fontaine (1.0.0) or `@capsizecss/metrics` (4.3.0). Safari reads only `size-adjust`, so leave vertical slack [usability-a11y-perf §3.7]. A body face may use `font-display: optional` instead.
- Preload only the one or two files the first viewport needs. Serve WOFF2 only; list it first in `src` (thelinestudio-com lists WOFF before WOFF2, so browsers fetch the 103KB WOFF).
- Anything that measures text waits for fonts: SplitText `autoSplit: true`, and `document.fonts.ready.then(() => ScrollTrigger.refresh())` (motion-core.js does both). A split computed on fallback metrics breaks lines wrongly after the swap.
- Subset only where the licence allows it (Dinamo yes; Production Type needs an addendum). Buttons do not inherit `font-family`: oryzo-ai renders 8 buttons in Arial for lack of `font: inherit`.

## 7. Mobile adaptation

- **Floors, not bare vw.** Probe display at 390: p25 32px, median 46.8px, max 160px [probe]. san-rita's `clamp(2.5rem, ..., 3.5rem)` lands on its 40px floor at 390; the-renaissance-edition drops to 72px on phones.
- **Count lines at 390.** Keep the display at one or two lines: shorten copy, widen to 16-18ch, or drop one step. shed reflows 231px to "THIS IS / SHED" at 100px.
- **Loosen as you shrink.** bennett-clive goes from 150px at lh 0.77 to 60px at lh 0.85. Take tracking from about -0.04em toward -0.02em.
- **Width before size.** A long word can take a narrower `font-stretch` (e.g. 87.5%) on phones before losing size. Never let a word force horizontal scroll (47/51 teardowns record none at 390).
- **Recompose instead of shrinking.** gq-ap-the-extraordinary-lab ships a narrow title cut; lando-norris serves a mobile SVG lockup; bennett-clive minifies BENNETT & CLIVE to B & C after 5px of scroll; zentry keeps its diagonal split (left word top, right word bottom) at 104px.
- **Hover type gets a touch equivalent.** Proximity, roll and letter-trail effects are gated on `(hover: hover) and (pointer: fine)`; touch gets the static state or a tap state.
- **Floors:** body 16px, captions 12-13px, marquee text 40px. Keep `-webkit-text-size-adjust: 100%`. Never block pinch zoom (immersive-garden-website sets `maximum-scale=1, user-scalable=0`; 6/60 winners do [usability-a11y-perf §1.5]).
- **Keep the semantic heading on the copy phones see.** mindmarket's phone view shows an `aria-hidden` duplicate, so mobile has no `h1` in the accessibility tree.

## 8. Failure modes

| Failure | Seen on | Fix |
|---|---|---|
| Text hidden until a reveal fires | about 45/51 teardowns | Visible by default; hidden state only while tweening; failsafe; revert |
| Root font-size from viewport width | about 12/51 (son-daven, zentry, maxima-therapy) | `rem` root; fluid steps with a rem term |
| Trial or free-site font files in production | aim-ai-modernism-of-kharkiv (KH Teka TRIAL), maxima-therapy (Diatype Rounded Plus Trial), the-power-of-storytelling (TT Neoris Trial; TheSeasons from a free-font site) | Licence at build time; grep for Trial/Test/Demo and mirror names |
| Declared face never loads | pacome-pertant-portfolio (renders Helvetica Neue/Arial), akaru-2 (Alliance Text), oryzo-ai (halyard-text) | Check rendered families in DevTools; delete unused `@font-face` |
| Leading below 0.85 on a mixed-case face | lacoste-polo-factory (lh 0.83, "Atelier" jammed between lines) | Sub-0.85 leading only on caps-only faces |
| Glyphs sliced by masks, notches or the viewport | about 15/51 (the-watch cuts FS and 0P at 390) | Pad masks 0.12em; `overflow-y: clip`; zoom-check every cut |
| Gradient poured into the type | the-power-of-storytelling (`background-clip: text` on the 281px h1) | Flat tint or one tonal step |
| Mono as house voice / one label costume | 15/51 / 24/51 | Mono on data tokens; one treatment per role |
| Canvas-only copy | iyo, messenger, igloo-inc | DOM twin for every drawn word |
| Scroll-read fill with an illegible base | vast (base words 1.73:1), leo-parpeix-portfolio-2026 (base copy at 0.15 opacity) | Base state passes 4.5:1 (3:1 for large text); the fill only deepens it |
| A mid-reveal frame copied as a style | cartier-watches-wonders-2025 (grey second line is a stagger caught mid-flight) | Read the settled frame before copying a "two-tone" |
| Too many families | why-zero (9 declared, including Caveat and Newsreader) | One voice, one companion, one data mono |
| Desktop formats served | son-daven (.otf), siena-film-foundation (.ttf) [typography §9] | WOFF2 only (Dinamo's EULA forbids desktop formats for web text) |

## Crafted vs slop

| Award habit | Slop version | Crafted version |
|---|---|---|
| Giant footer or hero wordmark | Default face, caps shaved by the container, gradient inside the letters, empty gap below it | Brand or licensed face, fit-to-width, centred or grid-aligned, above the texture, flush to and bleeding off the bottom edge only, every glyph top whole |
| Split-line reveal | Lines at opacity 0 or under their mask until a ScrollTrigger fires | Text visible at load; hidden only while tweening; CSS intro deadline 2s plus JS failsafe 3.5s; revert after |
| Two-tone headline | One saturated word dangling at the foot of a 3-4 line stack | One tonal step (opacity or `color-mix`) or one face swap inside 1-2 lines |
| Serif accent word | Instrument Serif or Cormorant italic dropped into Inter, under a kicker, as the "philosophy" beat | Licensed or Fontshare serif, cap height matched to the grotesk (+4% on lando-norris), inside a composed headline |
| Section heads | Tiny uppercase kicker over every H2 | Open sections with scale, an image, a number or a full sentence; no kicker |
| Tracked caps labels | One tracked-caps or mono costume on eyebrow, button, nav and colophon | Each role its own treatment; mono only on data |
| Link and nav hover | Underline that grows, wipes or waves in | Character roll, tonal shift, or weight change with reserved width; the box never moves |
| Letterspaced serif wordmark | Cormorant caps tracked wide | A drawn wordmark (akaru-2 one path per letter, san-rita hand lettering) |
| Big serif over imagery on cream | Didone on a beige sheet, grain across the text | A brand-specific ground; grain behind the type or on one deliberate word; a soft text-shadow halo for legibility |
| Scramble text | Every label decoding on scroll | Scramble only on interactive strings, width reserved, full label for screen readers (hubtown) |
| Marquee | Invented client names looping with no pause | Real content, pause control, static under reduced motion |
| Poster scale from vw | `html { font-size: 1vw }` so the page ignores zoom | `clamp()` with a rem term, max at most 2.5x min, tested at 390, 1440 and 2560 |
| WebGL headline | The only copy of the words lives in a canvas | DOM heading plus a GL twin placed from its bounding box |

## Exemplars

- lando-norris: serif/grotesk word swap at matched cap height, width axis as colour control, char-roll hover by text-shadow.
- thelinestudio-com: one variable family tuned by role (500/470/440/300) and a per-glyph optical margin table.
- the-renaissance-edition: clamp tokens, `text-box` trim on every headline, swash initials by `::first-letter`, Roman numerals by CSS counters.
- tracing-art: two-level story/metadata system (Bradford 30-207px, Graphik 10-14px) and italic articles in roman titles.
- shed: three voices with strict roles and clip-safe masks (`overflow-y: clip`, descender padding).
- champions-for-good: scale jumps inside one line, a real italic cut next to a settled skew, inline stickers in a type wall.
- son-daven: negative-tracked serif caps against positive-tracked sans text; stacked lines that shear on scroll.
- zentry: per-glyph stylistic-set accents that carry the logo's geometry into every headline.
- siena-film-foundation: poster billing block and 0.77 leading on a caps-only display face.
- dropbox-brand: variable-axis specimen widgets and a scroll-driven ink fill.
- the-watch: display type as the stage the product stands in.
- gil-huybrecht: the counter-case, one size and one weight with the grid carrying all hierarchy.

## Evidence

- `data/teardowns/<slug>.json` (51 audited teardowns): `typography`, `first_screen`, `motion.text_animation`, `steal_this` and `slop_risks`. Counts marked [teardowns] or n/51 are keyword tallies over these fields, rechecked 2026-09-25; tallies depend on the pattern, so treat them as plus or minus 2. The regime split (12/16/19, 11 at 200px+) is computed from `typography.display_size_px`. Inferred values stay marked inferred in the source JSON.
- `evidence/digests/typography.md` and `digests/content.md`: per-site typography, first-screen and content-voice digests.
- [probe] `data/probe_summary.json`: display and body size distributions at 1440 and 390, tracking, leading, CSS features, shipped font formats.
- [fonts] `data/font_census.json` summary keys: 575 sites checked, 554 fetched; hosts; families per site; Google and Adobe usage. Distinct-family and singleton counts computed from the family-name strings in it.
- [stats] `data/stats.md`, recent_2024_plus cut: element tag frequencies.
- [typography §n] `data/research/typography.md`: live-CSS font extraction of 47 winners, archetype tables, licence metrics, tested recipes (text-fit wordmark, SplitText, variable axes, marquee, roll hover). Its §2.6 lists Owners under MCKL; the teardowns and ohnotype.co say OH no Type Co, which this file follows.
- [motion-stack §n], [usability-a11y-perf §n], [webgl-3d-stack §n]: the matching files in `data/research/`.
- Checked live 2026-09-25: npm troika-three-text 0.52.5, fontaine 1.0.0, @capsizecss/metrics 4.3.0, gsap 3.15.0, lenis 1.3.26, three 0.186.1; troika README (font formats, `letterSpacing` in world units) and its 0.52.5 build (`unicodeFontsURL`); Google Fonts CSS API (Mona Sans, Geist, Geist Mono, Sometype Mono, Azeret Mono, STIX Two Text, Literata and Bayon are served; Apfel Grotezk, Karrik, Switzer and Necto Mono are not); Fontshare, Collletttivo and Velvetyne pages for every free alternative named.
- House law: `deslop-law.md` (default Google fonts, tasteful swap, character in display type, invisible content, clear the cut, footer wordmark placed right, cramped display, multi-line headline, saturated accent, underline hover, grain, one label treatment, kicker section heads, big serif statement block, gradient-filled headline text, text jammed against the edge).
- Recipes: [../recipes/tokens.css](../recipes/tokens.css), [../recipes/motion-core.js](../recipes/motion-core.js), [../recipes/motion-core.css](../recipes/motion-core.css), [../recipes/boot.html-snippet.html](../recipes/boot.html-snippet.html), [../recipes/three-hero.js](../recipes/three-hero.js). Casebook: [./casebook.md](./casebook.md).
