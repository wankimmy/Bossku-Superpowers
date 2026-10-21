# Layout, grid and composition

Last updated: 2026-09-25

Use this when: you are deciding page structure before building components: grid tokens, who owns the first screen, section order and scroll budget, pins, indexes, the footer and the phone layout.

## Rules

1. Name the fold owner first: one object, one image or film, or one line of type. On the 51 teardowns 3D leads the first screen on 19, photo/film/illustration on 13, type or logotype on 8 and a composite on 11. Everything else on the first screen is corner furniture.
2. Size the fold type by its owner. When an object leads, use no DOM headline or 12-56px in a corner (11/19 3D heroes), or 180-350px type set into the scene (5/19). Image-led: 32-96px. Type-led: 82-320px. Never put a mid-size headline beside a mid-size object.
3. The first screen is `min-height: 100svh` with a decided bottom edge. Nothing half-peeks unless it is a planned straddle.
4. Grids are tokens chosen from the brief. 12 columns is the default, 14-24 for dense indexes, 9, 4 or thirds for editorial. At 1440 the outer margin has a median of about 36px (middle half 20-48px, about 38 teardowns that state one), and the gutter is 0.5-1x the margin on 14 of the 18 that state both. On phones: 4-6 columns and 15-32px margins.
5. Running text obeys the grid and never sits closer to an edge than `--margin` (20px at 390, 40px at 1440). Only display type and media may break to the viewport edge; the 7-15px margins some winners run (thelinestudio-com, shed, made-with-gsap-1) are for full-bleed media, not paragraphs ("text jammed against the edge" [deslop]).
6. Aim for display:body of 7x or more: winners have a median of 6.9x (p25 4.2x, p75 11.2x, max 29x, n=47 teardowns). Pair one giant thing with small, precise things.
7. Keep the shell airy and the islands dense: `--space-xl` or more between sections, `--space-s` inside an island (R1). 27/51 teardowns class their density as airy, and only one as dense. Alternate loud and quiet every 1-2 screens.
8. Budget scroll in viewport units per scene. A pin over reading content adds at most about 150vh [motion-stack §4.5]. Set-piece pins of 300-900vh are only for scenes where scrolling is the interaction; give them a progress readout and run them on desktop with full motion only.
9. Horizontal sections are an accent (the Horizontal Layout tag is on 5/575 recent winners [stats]). On phones, under reduced motion and without JS they become a vertical stack.
10. Overlap with intent. An object may cover at most about 25% of a word's letters (rec. [imagery §3.2]). Live text stays on the top layer or gets a clear zone.
11. A bleed is either a large, legible share off one edge (at least 15% of the element, or a full gutter past it) or a caps wordmark set flush to the bottom with its empty descender band cut off. It is never a few pixels of glyph. Clear every cut: pad masks and zoom into the clipped edge [deslop].
12. The footer is an idea (a bookend, a hand-off, or a composed wordmark flush to the bottom), or there is no footer. 14/51 ship no conventional footer.
13. Recompose for 390px; do not shrink. Mobile display is about 0.59x its desktop px, yet it takes twice the share of the width (median 46.8px = 12vw vs 80px = 5.6vw) [probe]. Reorder, re-crop, re-author the assets, and drop pins and horizontal tracks.
14. The layout is complete at rest. No section waits at opacity 0 for a reveal. Use native document scroll with sticky stages, not a transform-driven 900px document [usability-a11y-perf §2F].

## 1. Grids observed

| Site | Columns at 1440 | Margin | Gutter | Phone |
|---|---|---|---|---|
| artefakt | 12 (`--margin 2rem`, `--gutter 1rem`, `--column` from `--vw`) | 20px | 10px | WebGL off below 1200px |
| immersive-garden-website | 12, `repeat(12,1fr)`, max 2088px | 16px | 16px | 1/12 stack, 32px |
| lama-lama-2 | 12 | 40px | 24px | 6 cols, 16 / 10px |
| pacome-pertant-portfolio | 12 | 30px | 16px | 6 cols, 20/15 (≤900), 15/10 (≤420) |
| made-with-gsap-1 | 12 | 15px | 15px | carousels go native |
| dropbox-brand | 12, spans as `--body-span-N` tokens | 120px | 24px | 32 / 12px at ≤767 |
| odd-ritual | 12 plus a hard half-axis at x=725 | 20px | 10.4px | 1 col |
| gil-huybrecht | 14, every cell spans 2 (7 visual columns) | 1.4rem | 1.4rem | 4 cols (2-up) |
| oryzo-ai | 16 | 45px (3.125vw) | 24/90 of a column | 4 cols |
| mindmarket | 16 (stats block on 14) | = gutter | = margin | 1 col, 20px insets |
| floema | 24 | 26px (1.8vw) | 20px (1.4vw) | 1 col |
| fluid-glass | 24 | 36px | 18px | 6 cols |
| thelinestudio-com | 9 | 6.67px (.46296vw) | 6.67px | 5 cols |
| bennett-clive | 4 | 112.5px (7.8125vw) | 112.5px | 2 cols, 48px |
| aim-ai-modernism-of-kharkiv | thirds: `1fr 2fr`, `1fr 1fr 1fr` | 14px | 0 in the image mosaic | 1 col |

Decisions:
- **DOM pages use CSS grid; stages do not.** 19/51 winners ship zero grid containers [probe]. Most are canvas worlds with absolutely placed chrome (messenger, igloo-inc, the-power-of-storytelling). A few are DOM pages laid out in flex or absolute positions: akaru-2 runs a 25,053px page with no grid, and its section heads start at four different x values (113/160/235/520). Any page with running content gets a real grid.
- **Expose the grid as tokens.** Examples: artefakt's `--margin/--gutter/--column`, dropbox-brand's `--body-col-N-left` and `--body-span-N`, era-residence's cell units (122.4 x 86.4px) that set the vertical rhythm. Compute widths from a width without the scrollbar. Artefakt derives columns from a `--vw` token, because `100vw` includes the classic scrollbar.
- **A second axis beats more columns.** odd-ritual hangs its hamburger, manifesto and footer column on x=725. aim-ai-modernism-of-kharkiv splits the hero with a rule at one third. depo-luxe hangs everything on x=720. bennett-clive runs its whole page on a horizontal axis at 50vh.
- **Hang the heads.** gil-huybrecht sets list heads one gutter left (`-ml-14`), so the items sit exactly on the column.
- **Build a grid overlay for yourself.** gil-huybrecht toggles one with Shift+G and fluid-glass with Ctrl/Cmd+G. Never ship it visible: a faint grid background is slop [deslop].
- **Seat type on the rows, not just the columns.** The-renaissance-edition sets `text-box: trim-both cap alphabetic` on every headline and gil-huybrecht on its info rows, so a head's cap height sits on a grid line with no half-leading. Trim to `text` for accented words; support is Chrome 133, Safari 18.2 and Firefox 154 [typography §6.1].

**Recipe R1: grid and spacing tokens.** Type steps live in [tokens.css](../recipes/tokens.css). These are the layout tokens it deliberately leaves out. Values are linear between 390px and 1440px, with the same formula as tokens.css.

```css
:root {
  --cols: 12;
  --margin: clamp(1.25rem, 0.786rem + 1.905vw, 2.5rem);   /* 20 -> 40 */
  --gutter: clamp(0.75rem, 0.564rem + 0.762vw, 1.25rem);  /* 12 -> 20 */
  --space-s:  clamp(1rem, 0.814rem + 0.762vw, 1.5rem);    /* 16 -> 24   inside components */
  --space-m:  clamp(1.5rem, 1.129rem + 1.524vw, 2.5rem);  /* 24 -> 40   between blocks */
  --space-l:  clamp(2.5rem, 1.757rem + 3.048vw, 4.5rem);  /* 40 -> 72   index row gaps (gil: 72) */
  --space-xl: clamp(4rem, 2.7rem + 5.333vw, 7.5rem);      /* 64 -> 120  section padding */
  --space-2xl: clamp(6rem, 4.05rem + 8vw, 11.25rem);      /* 96 -> 180  air around a one-idea screen */
  --space-void: clamp(9.75rem, 1.3rem + 34.667vw, 32.5rem); /* 156 -> 520 immersive-garden's project gap */
}
@media (width < 48em) { :root { --cols: 6; } }
.grid {
  display: grid;
  grid-template-columns: repeat(var(--cols), minmax(0, 1fr));
  column-gap: var(--gutter);
  padding-inline: var(--margin);
}
.grid > * { grid-column: 1 / -1; }      /* full width by default; place every block on purpose */
.bleed { margin-inline: calc(-1 * var(--margin)); }   /* media escapes the margin, text never does */
```

## 2. First screen: who owns it and how the bottom edge is controlled

| Owner | Sites | Type on the fold |
|---|---|---|
| 3D, 19 | 11 with no DOM headline or a small one: artefakt (12px h1 in the corner), leo-parpeix-portfolio-2026 24, immersive-garden-website 28, hubtown 30, david-whyte-experience 30, steven-com 51, san-rita 56; none on active-theory-v6, brunos-portfolio, igloo-inc, messenger. The other 3 sit between (gq-ap-the-extraordinary-lab and shader-development-studio at 108, why-zero's 150px loader counter) | tiny corner copy |
| | 5 with giant type set into the scene: everswap 189 (the peak pierces the letters), the-power-of-storytelling 281, the-watch 350 (the watch fills the gap in 'FS 60P'), oryzo-ai 180 wordmark, cartier-watches-wonders-2025 (world-space, inferred ~210-230) | type as scenery |
| Photo, film, illustration, 13 | the-renaissance-edition 32, ponpon-mania 35, depo-luxe 39.6, odd-ritual 42, lacoste-polo-factory 48, made-with-gsap-1 48, opal-tadpole 48.9, fluid-glass 57.6, maxima-therapy 62, vast 76, terminal-industries 82.5, son-daven 95; era-residence 172.8 is the outlier, because its wordmark sits in open sky | 32-96px, edge-anchored |
| Type or logotype, 8 | aim 81.9, dont-board-me 126, mindmarket 139.7, siena-film-foundation 196 (logotype), slosh-seltzer 207, champions-for-good 316.8, akaru-2 318 (SVG); dropbox-brand's 36px intro card is the exception | the type is the picture |
| Composite, 11 | for example shed 231.3 over a photo, thelinestudio-com 263 wordmark over the reel, zentry 180 on a diagonal around an object, gil-huybrecht 16.32 over the work grid | varies |

How the bottom edge is controlled:
- **No second section at all.** 22/51 report a 900px document [probe]. Some are single-viewport apps (iyo, steven-com, ponpon-mania, lacoste-polo-factory); others are virtual scrollers on a fixed stage (everswap, igloo-inc, depo-luxe). For content sites, get the same frame with a sticky stage over native scroll (R4).
- **Type seated on the edge.** The-power-of-storytelling's 281px h1 ends with its descenders about 22px above the fold, not cut. Thelinestudio-com's wordmark sits 18px (1.27315vw) off the left, right and bottom edges, whole. Vast, odd-ritual, iyo and steven-com anchor the headline bottom-left at the margin.
- **A planned straddle.** Mindmarket's runners rise from the bottom edge and cross the seam into the next section. Dont-board-me's leash crosses into the next section's copy: the Lottie layer is oversized (1800px, `pointer-events: none`, z-index 1).
- **A lifted sheet.** Opal-tadpole gives its hero `margin-bottom: -100vh; z-index: 4`, so the pinned statement already sits underneath and the hero slides off it with a hard edge. Thelinestudio-com's hero is 200svh with a 100lvh sticky reel.
- **A frame.** Hubtown draws a bevelled frame inset 30px. San-rita's map sits in a frame beside a 350px rail, `grid-template-columns: calc(350px - var(--scroll-normalized)*350px) 1fr`, and the frame goes full-bleed on scroll.
- **Failures to avoid.** Gil-huybrecht leaves about 280px of dead black, and the fold cuts its second row of labels (flagged). Vast's h1 wraps to four lines at 1440 under `max-width: 67rem`, and the consent banner covers it.

Chrome placement:
- **Four-corner HUD.** Artefakt, hubtown, igloo-inc, steven-com, san-rita and pacome-pertant-portfolio pin logo, menu, headline and utility to the corners, and the centre belongs to the object.
- **Corners carry state, not decoration.** Examples: a live clock (steven-com, lama-lama-2, san-rita), a chapter rail (hubtown, everswap) and sound. Give corner strings two type roles, not one costume ("one label treatment" [deslop]).
- **The nav as a detached object.** Terminal-industries uses an island inset 139px from each side. Lama-lama-2 uses a centred 438x50 pill, iyo a 375x62 capsule, and mindmarket two separate floating bars. Fluid-glass docks a 248x45 bar at bottom-centre, 36px up.
- **Plan where the consent card lands.** The probes caught consent UI over the fold: a bottom-right card on era-residence, steven-com, depo-luxe and fluid-glass, a banner over the bottom 20% on vast, and a centred modal on floema. Keep the CTA out of that zone. Era-residence repeats its chamfered frame inside the card.

**Recipe R2: four-corner first screen.**

```css
.fold {
  position: relative; isolation: isolate; box-sizing: border-box;  /* padding inside the 100svh */
  min-height: 100svh;                       /* stable first frame while the URL bar moves */
  display: grid; gap: var(--space-s);
  grid-template: "tl tc tr" auto ". mid ." 1fr "bl bc br" auto / 1fr auto 1fr;
  padding: var(--margin);
}
.fold__stage { position: absolute; inset: 0; z-index: -1; }   /* canvas, film or image: the owner */
.fold__title { grid-area: bl; align-self: end; max-width: 14ch; text-wrap: balance; } /* 1-2 lines */
.fold__meta  { grid-area: br; align-self: end; justify-self: end; }
.fold__nav   { grid-area: tr; justify-self: end; }
```

## 3. Scale contrast

- **The ratios.** Display:body across 47 teardowns: p25 4.2x, median 6.9x, p75 11.2x. At the top: the-watch 350/12 (29x), vast 345.6/14, dont-board-me 293/14 and champions-for-good 316.8/16. Maxima-therapy drops from 575px letters to 19px body within two screens. Akaru-2 sets 96px heads over 10px data rows.
- **Size against the image, not only against the text.** Era-residence pairs viewport-wide display type with a 372x187 carousel, about 20:1 in width [imagery §3.2].
- **Flat scale only when the content is the scale.** Gil-huybrecht uses one 16.32px size everywhere (1.0x), and it works only because the grid of captures carries the page.
- **Decision.** Use one display step per page (`--step-display`, `--step-hero` or `--step-poster` in [tokens.css](../recipes/tokens.css)) and body at 16-18px (winners run 14.4px median [probe]; floor it at 16). Jump at least three steps between display and the next size, so the page lands near the winners' 6.9x median rather than at a timid 2-3x. See [typography](./typography.md) for faces and tracking.

## 4. Density and white space

- **Measured air.** Fluid-glass gives one sentence per screen with 150-200px above and below. Odd-ritual leaves about 250px around its manifesto and a 450px empty band in the footer. Immersive-garden-website puts `margin-top: 36.11vw` between projects (520px at 1440, 156px on mobile). Thelinestudio-com leaves a 200px void under its giant section word.
- **Dense islands as resets.** Gil-huybrecht's 7-column contact sheet, lama-lama-2's 7-row work index, akaru-2's 10px award tables and leo-parpeix-portfolio-2026's 24-row archive each sit between empty, one-idea screens.
- **Scales in use.** pacome-pertant-portfolio uses 10/15/30/60/90/120/180 px, son-daven 2-136 plus an 88px cell, and vast `.4-6.4rem`. Steps grow about 1.5-2x. R1's `--space-*` follows that curve.
- **Decision.** Section padding is `--space-xl`. A statement screen gets `--space-2xl` above and below. Dense blocks tighten to `--space-s` inside and keep the full `--space-xl` outside, so the island reads as one object.

## 5. Section rhythm across a page

- **Length.** Among the 29 documents that scroll natively [probe]: 2,700px (dropbox-brand) to 81,450px (tracing-art), median 13,579px (about 15 screens at 900px), middle half roughly 8,000-25,000px.
- **Alternation is the rhythm.** Examples: floema goes quiet ivory, then a loud 900vh photo run, then quiet type. Odd-ritual follows every loud image section with a near-empty white one. Terminal-industries alternates dark and white every 1-2 sections. Lando-norris switches dense/airy and light/dark "on nearly every step". Shed swings from huge to mid scale every section.
- **Scene budgets in vh.** Examples:
  - everswap: each chapter's `padding-bottom` is its dwell, about 2,075vh in total.
  - hubtown: 400/400/1000/1000vh over a sticky 100vh stage.
  - the-power-of-storytelling: 20 sections, each one second of a 20s Blender timeline, so a section's vh sets how long you dwell.
  - cartier-watches-wonders-2025: 8 stops whose timelines overlap by half, so the next world already sits inside the current one.
- **Vary how sections open.** A kicker over a heading is slop [deslop]. Winners open with a giant word (thelinestudio-com), a live effect number (made-with-gsap-1's "ON SCREEN 090" chip), an image, or a camera move.
- **Hand the surface off.** Options:
  - A rounded sheet overlapping the previous section: mindmarket (radius 50px) or made-with-gsap-1 (inset 5px, radius 20-25px).
  - A seam that doubles as a ground line: champions-for-good's golfer stands on the footer edge.
  - A tone handoff between sections.
  Keep hard colour seams for a floor change [deslop].

**Decision: write a beat sheet before any markup.** One row per beat, with columns for owner, density, surface, vh and mobile form. Example: `hero | object | airy | dark | 100svh | reframed` → `statement | type | void | same | 100vh | 1 col` → `proof index | list | dense | light sheet | auto | 1 col` → `set piece | pinned scene | airy | dark | 250vh | stacked` → `reset | giant word | void | light | 100vh | same` → `footer | hand-off | - | floor | 100svh | same`. If two adjacent rows match on owner and density, change one of them. If three rows in a row share one flat surface after the hero, that is "a flat fill under everything after the hero" [deslop]: carry imagery, a toned or textured ground, or the stage down into one of them.

## 6. Index, list and archive patterns

- **Contact sheet** (gil-huybrecht): captures at their true aspect ratio in 2-column cells on a 14-column grid, wrapping like text. Row bottoms are ragged on purpose, and row gaps are 72px. The header facts sit on the same grid.
- **Ruled rows** (lama-lama-2): 168px full-width rows under a 1px rule. Client 20px at x=40, tags at x=271, toggle at x=617, and a thumbnail strip bleeding off the right edge. Lama-lama-2 sets its tags as black mono chips; set them as plain type in a second role instead ("tinted pill chips everywhere" [deslop]). leo-parpeix-portfolio-2026 uses 45px rows with 10%-alpha rules; a row opens into a poster, then a looping mp4 (1.4s `cubic-bezier(.16,1,.1,1)`).
- **A list that parts** (depo-luxe archive): numerals right-aligned and clients left-aligned about a gutter on x=720. The list opens a 0.35-0.4 viewport window where the title sits, and rows entering it spread toward the edges.
- **Halving squares** (depo-luxe featured index): the focused square is `max(.3*innerWidth, .35*innerHeight)` in the bottom-left corner. Earlier items stack above it at half size each, and later ones run along the bottom at half size.
- **Asymmetric pairs** (immersive-garden-website): a landscape card at about 48% width on the left, then a portrait card at 31-33% on the right. Fluid-glass scatters four portrait cards at three sizes and four x positions. Lando-norris offsets alternate columns of its 4-up helmet grid by about 52px.
- **Zig-zag tables** (akaru-2): 930px-wide 3-column award rows, alternating right (x 480-1410) and left (x 30-960).
- **Index as menu** (dropbox-brand): a pinwheel mosaic of eight chapter tiles around the logo button, with only the outer corners rounded. The-renaissance-edition runs a fixed left rail of 12 chapters that doubles as progress.
- **Decisions.** Use one column template for every row, so parallel parts align ("misaligned parallel columns" [deslop]). Hover changes content in place, not position: odd-ritual swaps the packshot for an on-model photo and shows a spec card inset 10px, with no card lift [deslop]. Rules separate rows at 10-15% alpha. Draw each rule as a 2px line with round caps (R3) rather than a square-cut border, or drop it and let `--space-s` do the separating ("unrounded hairline rules" [deslop]). Never put a lone rule beside a label.

**Recipe R3: contact sheet and ruled archive.**

```css
.sheet-index { display: grid; grid-template-columns: repeat(14, minmax(0, 1fr));
  column-gap: var(--gutter); row-gap: var(--space-l); padding-inline: var(--margin); align-items: start; }
.sheet-index > figure { grid-column: span 2; margin: 0; }
.sheet-index img { display: block; width: 100%; height: auto; } /* width/height attrs in HTML: no CLS */
@media (width < 48em) { .sheet-index { grid-template-columns: repeat(4, minmax(0, 1fr)); } }

.archive { padding-inline: var(--margin); container: archive / inline-size; }
.archive summary {                     /* <li><details><summary>idx, name, type, year</summary>media</details></li> */
  display: grid; grid-template-columns: 3rem minmax(0, 3fr) minmax(0, 2fr) 5rem; /* one template, every row */
  column-gap: var(--gutter); align-items: center; min-height: 3.25rem; cursor: pointer;
  position: relative; list-style: none; }
.archive summary::before {             /* the row rule: 2px, round caps, 12% ink */
  content: ""; position: absolute; inset: 0 0 auto; height: 2px; border-radius: 1px;
  background: color-mix(in oklab, currentColor 12%, transparent); }
.archive summary::-webkit-details-marker { display: none; }
/* R6: the row recomposes by its own width (a split column, a phone), not the viewport */
@container archive (width < 40rem) {
  .archive summary { grid-template-columns: 2.5rem minmax(0, 1fr) auto; row-gap: 0.25rem; padding-block: var(--space-s); }
  .archive summary > :nth-child(3) { grid-column: 2; grid-row: 2; }   /* type drops under the name; year stays right */
}
```

Container queries are on 5/51 winners (gq-ap-the-extraordinary-lab, lama-lama-2, mindmarket, odd-ritual, terminal-industries) and subgrid on 4/51 (mindmarket, odd-ritual, san-rita, terminal-industries) [probe]. Use a container query when one component lives at two widths on the same page, for example the archive inside a sticky split and at full width.

## 7. Sticky and pinned structures

- **Usage.** `position: sticky` appears on 20/51 [probe]. The patterns:
  - **Sticky split index** (aim-ai-modernism-of-kharkiv): a 100vh sticky wrapper with the heading on the left, a counter and names in the middle, and a right-third column where each next artwork slides up one viewport.
  - **Sticky stats** (mindmarket): copy sticky in grid columns 1-9, and a stack of sticky stat cards in columns 10-15 of 14.
  - **Sticky full-bleed cases** (artefakt): one screen each, with a HUD row of label, counter and title. On mobile the next case slides over the previous one.
  - **A deal over a track** (dont-board-me): a 100vh sticky table over a 400vh track of four spacers, where cards travel from `top: 100%` to rest positions at small tilts.
  - **A fixed axis** (bennett-clive): the wordmark row stays fixed at 50vh, and the inset reel is sticky at `100dvh` and 80% height.
- **The budget.** Winners run set pieces long: made-with-gsap-1 pins for 700vh, 400vh and 300vh, floema's slider for 900vh, and pacome-pertant-portfolio's about page for 500vh. Scroll research caps pins over reading content at about 1.5 viewports of extra travel [motion-stack §4.5, §6.1]. So a long pin is allowed only when scrolling scrubs a scene or object, never a paragraph, and it shows where you are (floema's track fill, hubtown's bottom-bar segment).
- **Stacking cards.** Use `data-stack` in [motion-core.js](../recipes/motion-core.js). CSS does the stacking, and JS only adds the covered card's recede.
- **Gotchas.**
  - An ancestor with `overflow: hidden` becomes the scroller and breaks sticky; use `overflow: clip`.
  - `transform`, `filter`, `backdrop-filter` and `contain: layout|paint` on an ancestor capture fixed chrome and pins [motion-stack §6.5]. A `container-type: inline-size` ancestor did not capture a fixed child in the Chromium test of these recipes.
  - Give fixed chrome its own lane. Floema's header has no background, and the 51px statement scrolls straight under the wordmark (flagged).

**Recipe R4: sticky split with subgrid, and a sheet that covers a held hero.**

```css
.split { display: grid; grid-template-columns: subgrid; grid-column: 1 / -1; align-items: start; }
.split__head { grid-column: 1 / span 5; position: sticky; top: calc(var(--header-h, 0px) + var(--margin)); }
.split__body { grid-column: 7 / -1; }
@media (width < 48em) { .split__head { position: static; } .split__head, .split__body { grid-column: 1 / -1; } }

.lift { height: 200svh; }                                        /* 1 screen of hold, 1 of cover */
.lift__stage { position: sticky; top: 0; height: 100lvh; overflow: clip; }  /* lvh: no gap when the URL bar hides */
.lift + .sheet { position: relative; z-index: 1; margin-top: -100svh; background: var(--surface);
  border-radius: var(--sheet-r, 0); }    /* the moving edge must never park on a line of text */
```

## 8. Horizontal sections

- **Who uses them.** 6/51 teardowns: lando-norris (pinned photo track), akaru-2 (overlapping colour panels), era-residence (location track), son-daven (scrubbed gallery), fluid-glass (process strip) and made-with-gsap-1 (250px type). Five of the six are verified to drop or restack the track on mobile. Lando-norris's mobile track is unverified.
- **Size panels in vh, not px.** Lando-norris's large frame is 65.48vh x 59.48vh and the small ones 20.96-29.3vh. Each image is `calc(100% + 4rem)` inside an `overflow: clip` frame, so the 4rem drift never shows an edge.
- **Composition inside the track.** era-residence: stepped title, then a portrait image, then a text column, then a circular CTA. son-daven: each card enters rotated 5-10deg and leaves mirrored.
- **Build it** with `data-pin="horizontal"` from [motion-core.js](../recipes/motion-core.js). The containerAnimation is linear, the pin is desktop-only (60em), and it warns past 150vh. Under reduced motion, below 60em and without JS the panels stay a vertical stack, because motion-core.css only lays out the row once JS adds `.is-pinned`. If you want a native scroll-snap row as the fallback instead, use the variant in [motion-stack §4.5].
- **The cheaper horizontal is a native carousel with a peek.** Examples: leo-parpeix-portfolio-2026 (177px peeks), vast (the next slide 16px away), odd-ritual (running off both edges). Add buttons for the drag (SC 2.5.7 [usability-a11y-perf §2E]).

## 9. Overlap and layering

- **Object in front of type.** The-watch's watch fills the gap in 'FS 60P' and overlaps the '6'. Slosh-seltzer's can interrupts the wordmark. Zentry puts a character in front of its '500K+' numerals, inside the card edge. Oryzo-ai's foil coaster interrupts 'wearable'. Keep occlusion under about 25% of a word's letters (rec. [imagery §3.2]). When the object is shot or rendered, leave a clean zone of at least 35% of the frame where the type will go (rec. [imagery §3.2]).
- **Planes behind type, with a clear zone.** Floema's product planes pass behind the h1 letters. Tracing-art keeps a repel point around the headline and dims the centre column's planes toward 50% white. That is the crafted way to run imagery past live text.
- **Depth sandwich.** Mindmarket stacks photo, back ribbon, cutout, then front ribbon. The house law asks for three reads: foreground copy, a midground object and a background scene, with one element crossing a layer boundary [deslop signature §3].
- **Sheets as layers.**
  - thelinestudio-com's project sheets are 95% opaque, so the frame below ghosts through like a light table.
  - made-with-gsap-1's light sheets slide over a black page.
  - opal-tadpole's statement clips pop to 1.7x over the neighbouring lines.
- **Rules.**
  - An oversized overlap layer gets `pointer-events: none` (dont-board-me).
  - Legibility scrims sit only behind the text and fade out before any section edge [deslop "hard image seams"]. Oryzo-ai blurs a soft SDF patch of the desk under its paragraph instead of laying a box on top.
  - DOM text stays the source of truth, with WebGL drawn around it [awwwards-editorial §3.4].

## 10. Edge-bleed done right: clear the cut

- **Crafted.**
  - akaru-2's footer wordmark runs the full 1380px between the 30px margins and bleeds off the bottom only.
  - bennett-clive's wordmark grows full-bleed, flush to the bottom edge.
  - floema's footer glyph is whole, flush to the 32px margin and about 90px clear of the footer's top.
  - Carousel peeks run off the side edges (odd-ritual, leo-parpeix-portfolio-2026).
  - champions-for-good crops its giant pictograms by an edge, and the cropped piece is the whole point (the bow off the top, the target off the right).
- **Failures in winners.**
  - akaru-2's line masks shave descenders at rest: 'jamais' reads 'iamais'.
  - aim-ai-modernism-of-kharkiv's fixed meta bar shaves the ascenders of lines scrolling under it.
  - cartier-watches-wonders-2025's world-space '& WONDERS' is cut on narrow viewports because it cannot reflow.
  - everswap's reveal masks caught 'O|ol' mid-slice.
  - the-watch's mobile copy sits under the watch (mobile_01): covered rather than cut, the same failure.
- **Rules.**
  - A deliberate bleed removes a large, legible share (rec.: at least 15% of the element, or a full gutter past the edge) and stays whole and centred on the other edges. A cut of a few pixels of glyph reads as an accident.
  - The one small bleed the law asks for is a footer wordmark "bleeding slightly off the bottom" [deslop]. Set it in caps, or in a word with no descenders, and pull it down only into its empty descender band (`margin-block-end: -0.06em` [typography §6.1]), so no letterform is cut.
  - Pad line masks for ascenders and descenders and cancel the padding with negative margins: `.rv-line-mask` in [motion-core.css](../recipes/motion-core.css) uses `padding-block: 0.12em`. Display leading of 0.78-0.95 needs it [typography §0].
  - Never let a section edge, `overflow: hidden` or a fixed height crop live text.
  - Zoom into every clipped corner at 1440 and 390 [deslop].
  - Words with descenders never take a negative bottom margin [typography §6.1].

## 11. Footers

- **No footer, the experience ends** (14/51): brunos-portfolio, cartier-watches-wonders-2025, dropbox-brand, gq-ap-the-extraordinary-lab, hubtown, lacoste-polo-factory, messenger, pacome-pertant-portfolio, ponpon-mania, siena-film-foundation, slosh-seltzer, steven-com, why-zero and the-renaissance-edition (legal links in its rail).
- **Bookend.** The last screen answers the first:
  - active-theory-v6 re-uses the logo ring upside down.
  - artefakt reforms its ASCII logo.
  - aim-ai-modernism-of-kharkiv rebuilds the wordmark from eight slabs.
  - bennett-clive's 50vh row slides down and scales up into the full-bleed wordmark.
- **Hand-off.**
  - pacome-pertant-portfolio ends each case in a sticky 100vh "next up" zone.
  - san-rita puts four corner words around a feathered window of the next project, and clicking scales it into that project's hero.
  - shed sets 'SEE WORK' at about 186px, an inline project thumbnail on column 4 and an arrow on one baseline, about 10px above the bottom edge.
- **Floor reveal.** Thelinestudio-com's footer is a sticky red floor at 100dvh, and its `:before` extends 10vh upward to cover overscroll. A #f8f8f8 sheet carrying the wordmark tilts away above it. The-power-of-storytelling ends on a fixed full-screen contact finale.
- **Island.** Maxima-therapy's footer is a white island inset 48px; lando-norris's is an inset card cut with the site's one tab silhouette. Law: an island is premium, but the default closing "enquire island with a form" is slop [deslop].
- **Rules.**
  - The standard footer is slop: wordmark, rule, four mono-labelled link columns, rule, sign-off [deslop].
  - A giant wordmark is fit-to-width, whole on three edges and flush to the bottom edge. Only the bottom may bleed, it sits above the texture, and it has no gradient inside the type. The fitting code is in [typography §6.1](../data/research/typography.md).
  - Put link columns on the page grid, as gil-huybrecht does (columns 1/5/8/11), not flung to the far edges.
  - Jurors do look at footers. The Footer Design tag is on 21/575 recent winners, and among the element sections submitted for recent winners, footer (75) is level with scroll (77) and loading (75) [stats].

## 12. Mobile re-composition (measured at 390)

- **Numbers** [probe]:
  - Display at 390: p25 32px, median 46.8px, p75 80px, max 160px (the-watch).
  - Type-led phone heroes run 97-160px (25-41vw): maxima-therapy 156, made-with-gsap-1 120, dont-board-me 113, mindmarket 105, zentry 104, shed 100.
  - Body floor 16px [typography §7].
  - 0/51 sites have horizontal overflow at 390.
- **Phone grids.**
  - Columns: 4 (oryzo-ai, gil-huybrecht), 5 (thelinestudio-com), 6 (fluid-glass, lama-lama-2, pacome-pertant-portfolio), 2 (bennett-clive).
  - Margins: 15-20px (pacome-pertant-portfolio), 16px (lama-lama-2), about 17px (dont-board-me), 20px (mindmarket), 25px (igloo-inc), 32px (dropbox-brand, immersive-garden-website).
- **Recompose moves.**
  - **Reframe the camera.** igloo-inc sets `camera.zoom = min(1, aspect*1.25)`, so the igloo keeps its width. steven-com raises the camera and pulls it back (y .2, z 7.75), which makes the dial read as a tilted gyroscope. the-power-of-storytelling ships a separate `cam-mob.glb`.
  - **Re-author the art.** champions-for-good ships portrait Lotties (`archer_mobile.json`). mindmarket draws a separate 847.9x4471 trail at 214% of the column. Opal-tadpole ships a 1280x2310 portrait hero video (inferred from archived code). Lando-norris ships a separate helmet mask SVG below 479px.
  - **Re-scale the stage.** maxima-therapy's wheel goes from `calc(3352/982*100svh)` to `calc(3352/982*70svh)` and its hills from 58 to 50 degrees. ponpon-mania scales its mask 1.5x, so the outline leaves the screen.
  - **Reorder and restack.** depo-luxe moves the client above the title. akaru-2's horizontal rail becomes stacked cards. odd-ritual's carousel becomes one full-width card. iyo turns its tile into an auto-advancing snap carousel above the bottom edge.
  - **Swap the input.** dont-board-me's sticky card deal becomes a slider below 1024px. lando-norris adds a 'TAP TO LOCK' switch where desktop used hover. steven-com replaces hovering the dial with a draggable pill slider.
  - **Gate set pieces.** son-daven returns early from 7 of its 16 scene initialisers below 992px. made-with-gsap-1 drops its pinned type. fluid-glass skips its horizontal track. era-residence keeps its track desktop-only. artefakt never initialises WebGL below 1200px.
- **Rules.**
  - Compose for the phone [usability-a11y-perf §4].
  - Use `svh` for the first frame and `lvh` for media held by CSS `position: sticky`, so no gap shows when the URL bar hides. A GSAP-pinned stage stays in `svh`, with `ScrollTrigger.config({ ignoreMobileResize: true })` [motion-stack §6.5].
  - Gate hover effects behind `(hover: hover) and (pointer: fine)`.
  - Count display lines at 390: shorten the copy, or change the width axis before the size.
  - Never let a pinned or oversized object sit on copy. the-watch's mobile overlap is the failure.

**Recipe R5: recompose, don't stack.** This is a case row, not a hero: on the fold, a text column beside a media panel is the slop split hero [deslop], so use R2 there. The media goes first and full-bleed on the phone, and the title moves over its lower third.

```css
.case { display: grid; grid-template-columns: subgrid; grid-column: 1 / -1; row-gap: var(--space-m); }
.case__title { grid-column: 1 / span 5; grid-row: 1; align-self: end; }
.case__media { grid-column: 7 / -1; grid-row: 1 / span 2; }
.case__meta  { grid-column: 1 / span 4; grid-row: 2; align-self: end; }
@media (width < 48em) {
  .case__media { grid-column: 1 / -1; grid-row: 1; margin-inline: calc(-1 * var(--margin)); aspect-ratio: 4 / 5; }
  .case__title { grid-column: 1 / -1; grid-row: 1; align-self: end; padding: var(--space-s); z-index: 1; } /* over the lower third; z-index or the later media paints over it */
  .case__meta  { grid-column: 1 / -1; grid-row: 2; }
}
```

The CSS these winners use [probe]: `clip-path` 29/51, `position: sticky` 20/51, `clamp()` 18/51, `:has()` 17/51, `mix-blend-mode` 17/51, `backdrop-filter` 16/51, `text-wrap` 13/51, dynamic viewport units 8/51, container queries 5/51, subgrid 4/51 (san-rita's CSS uses subgrid, `:has()` and `clamp()`). The-renaissance-edition places its floating app cards in `cqi` inside a `container-type: inline-size` wrapper, so the cloud scales with its box, not the viewport.

## Crafted vs slop

| Award habit | Slop version | Crafted version |
|---|---|---|
| Centred hero column | Eyebrow, headline, subline and two buttons down the middle [deslop "default hero stack"] | The owner fills the frame; a 1-2 line title at bottom-left, one action, state in the corners (steven-com, vast) |
| Four-corner HUD | 8-9px tracked caps in every corner, one costume, inactive rail items at about 30% opacity (hubtown flagged) | Corners carry live state in two type roles at ≥12px and ≥4.5:1 |
| Fixed full-viewport canvas | A fixed background trailing under every section, including the FAQ (david-whyte-experience flagged) | The stage changes state per section (the-power-of-storytelling), or is scoped in a sticky wrapper that ends (R4) |
| Webflow-style entrance states | Sections at opacity 0 until IX2 or a ScrollTrigger fires (aim-ai-modernism-of-kharkiv, akaru-2 flagged) | Complete at rest; motion on transform and clip of visible media via `data-reveal` in [motion-core.js](../recipes/motion-core.js) |
| Line masks | Descenders shaved at rest (akaru-2) | Masks padded 0.12em with the padding cancelled by negative margins (motion-core.css), and a zoom check at 1440 and 390 |
| Ruled index | Square-cut 1px borders on every row, tags as tinted chips (lama-lama-2) | One column template, 2px round-capped rules at 12% ink, tags as plain type in a second role (R3) |
| Cream ground under everything | Oat-milk sheet behind boxes (aim-ai-modernism-of-kharkiv, akaru-2, fluid-glass, floema flagged) | A ground sampled from the brand's image or material: era-residence's powder sky, son-daven's sand [imagery §3.2] |
| Duotone section bands | Hard seams stacked like templates (fluid-glass flagged) | The seam is a ground line (champions-for-good), or an overlapping sheet with one radius |
| Giant footer wordmark | Pasted text with its cap tops shaved, off-centre, a gradient inside | Fit-to-width, whole on three edges, flush to the bottom, above the texture (bennett-clive, akaru-2) |
| Four-column footer | The standard footer [deslop] | A bookend, a hand-off or a composed line (shed, pacome-pertant-portfolio, san-rita) |
| Label over heading | A kicker opening every section (era-residence, immersive-garden-website flagged) | Open with a giant word, a live number, an image or a camera move |
| Numeral rail down the left | Numbered steps beside a vertical line [deslop] | The rail is progress: depo-luxe's line runs one viewport per project with a travelling gap at the numeral |
| Pieces at both far edges | Content flung to the rims with a dead middle [deslop] | Axis logic: the far pieces share a baseline with a centred anchor (depo-luxe's title line, bennett-clive's 50vh row) |
| 3-4 line display stacks | A tall wrapped staircase with a dangling accent word (immersive-garden-website, vast flagged) | 1-2 lines with `max-width` in ch (12-18ch) and `text-wrap: balance`; stepped indents only as a composed arrangement |
| Card grids with hover | Lift, shadow and boop on every card [deslop] | Content changes in place: odd-ritual's on-model swap plus an inset spec card |
| Long pins | 700-900vh of hijacked reading | One scene per pin, a visible progress readout, desktop only, reading content ≤150vh |

## Exemplars

- **gil-huybrecht**: a 14-column contact sheet, header facts on the same grid, hanging heads. Also study its dead-black fold gap as the thing to fix.
- **artefakt**: a 12-column token grid, a four-corner frame, and case HUDs over sticky full-bleed film.
- **aim-ai-modernism-of-kharkiv**: a thirds system with 1px rules, a pinned split index, and a footer that rebuilds the hero wordmark.
- **bennett-clive**: a 4-column 7.8125vw grid and a whole page on one 50vh axis, which ends as a flush full-bleed wordmark.
- **thelinestudio-com**: a 9-column grid, a 200svh hero with a sticky reel, onion-skin sheets and a sticky floor footer.
- **lando-norris**: a horizontal track sized in vh, offset helmet columns, and one tab silhouette re-used as a layout system.
- **mindmarket**: sticky stat stacks on 14 columns, an oversized trail with its own phone asset, and 50px-radius sheets.
- **depo-luxe**: axial composition on x=720, halving-square index, and an archive that parts around the centre.
- **tracing-art**: a fixed stage with a clear zone and centre dimming that let imagery run past live text.
- **the-watch**: an object occluding display type, an exploded view on one axis; its mobile overlap is the warning.
- **san-rita**: a grid track that animates from a framed map sheet to full-bleed, with subgrid and chamfer geometry.
- **odd-ritual**: a half-axis at x=725, an unequal three-up, and strict loud/quiet alternation.

Full entries are in the [casebook](./casebook.md). Motion for pins, stacks and reveals is in [motion](./motion.md). Image crops and scrims are in [imagery](./imagery.md).

## Evidence

- `data/teardowns/<slug>.json`: `layout`, `first_screen`, `typography`, `navigation_interaction.footer` and `slop_risks` for all 51 sites. Counts in this file were tallied from those fields. Items marked inferred in a teardown stay inferred here (cartier-watches-wonders-2025's type size, opal-tadpole's portrait video). Lando-norris's mobile track is unverified.
- `evidence/digests/layout.md`: the per-site layout digest, read in full.
- `data/probe_summary.json` [probe]: display and body size distributions, CSS feature and usage counts. Per-site `evidence/probes/<slug>/probe.json` supplied doc heights, grid-container counts, largest text at 1440 and 390, and `overflow_x`.
- `data/stats.md` [stats], recent_2024_plus cut (575 sites): tag counts for Horizontal Layout and Footer Design.
- `data/research/`: motion-stack §4.5, §6.1 and §6.5; typography §0, §4.3, §6.1 and §7; imagery §3.2 (both 25% occlusion and the 35% clean zone are marked rec. there); usability-a11y-perf §2 and §4; awwwards-editorial §3.4.
- `deslop-law.md` [deslop]: the house law. It overrides award habit everywhere above.
- Recipes R1-R5 were extracted from this file and run together in headless Chromium (Playwright) at 1440, 390 and 320 on 2026-09-25. Results: token values exact at both anchors, no horizontal overflow, the fold equal to the viewport, the sticky head held at the margin, the sheet covering the held stage, archive columns aligned across rows, and the mobile case title hit-tested above its media. After the audit changes, R3's round-capped rule and the R6 container query were re-run at 1440 and 390 in Chromium: rules render 2px, radius 1px, 12% ink; the archive goes 4-column at full width and 3-column (type under the name) in a 590px split column and on phones, with columns aligned across rows and no horizontal overflow. Firefox and WebKit were not run. Nothing in this file duplicates code in `../recipes/`.
- Audit 2026-09-25: the margin median and gutter ratio were recounted from the teardowns' `layout.grid` fields; the display:body ratios (median 6.9x, n=47), fold-owner counts (19/13/8/11), doc heights (29 native documents, median 13,579px) and zero-grid count (19) were recomputed from the teardown and probe JSON.
