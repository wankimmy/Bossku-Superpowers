# Typography

Type is most of the Design score. Winning sites are recognisable from a crop of their type.

## Choosing: role first, then voice

Decide roles: **display** (the image-making voice), **text** (reading and UI), optionally
**accent** (one contrasting voice: serif italic, mono for data, script/handwriting for annotations).
One family can do all three; two is the norm; three only when the third is tiny and functional.

Choose the voice from the concept: a frame/museum concept wants museum-label restraint; a
"compile" concept wants mono precision; a field-color brand wants a heavy wide grotesk shouting.

All fonts below are verified downloadable with `scripts/font.mjs` (free for commercial web use
under their licenses: Fontshare FFL, Google OFL). If the user provides licensed fonts (Neue
Montreal, Suisse, Söhne, GT, ABC), use them from their files instead.

### Neo-grotesk / grotesk (the workhorse of winners)
| Font | Source | Character |
|---|---|---|
| Switzer | fontshare `switzer` | neutral Swiss, closest free to Neue Montreal/Suisse; Noho (SOTD) |
| General Sans | fontshare `general-sans` | slightly geometric, friendly-precise |
| Satoshi | fontshare `satoshi` | modernist geometric-grotesk, very popular (use with intent) |
| Supreme | fontshare `supreme` | tall x-height, sharp, tech-leaning |
| Synonym | fontshare `synonym` | quirky grotesk with character in a, g |
| Inter Tight | google `Inter Tight` | display-tight Inter cut; neutral to the point of anonymity |
| Instrument Sans | google `Instrument Sans` | condensed-ish, editorial-tech; has width axis |
| Schibsted Grotesk | google `Schibsted Grotesk` | newspaper grotesk, warm and solid |
| Host Grotesk | google `Host Grotesk` | clean, slightly humanist |
| Hanken Grotesk | google `Hanken Grotesk` | light geometric grotesk |
| Mona Sans / Hubot Sans | google | variable width + weight (Lando Norris SOTY uses Mona Sans) |
| Geist | google `Geist` | Vercel's grotesk; developer-coded |
| Familjen Grotesk | google | Scandinavian, idiosyncratic g and y |

### Display with attitude
| Font | Source | Use |
|---|---|---|
| Clash Display / Clash Grotesk | fontshare | bold contemporary display |
| Cabinet Grotesk | fontshare | chunky, characterful headlines |
| Panchang | fontshare `panchang` | ultra-wide, architectural |
| Tanker | fontshare `tanker` | condensed heavy poster |
| Melodrama | fontshare `melodrama` | high-contrast condensed display |
| Bricolage Grotesque | google | expressive optical-size grotesk |
| Big Shoulders Display | google | condensed industrial, many weights |
| Anton / Six Caps | google | ultra-condensed poster (use huge) |
| Unbounded | google | wide rounded techno |
| Syne | google | wide, quirky, art-school |
| Funnel Display | google | modern display grotesk with character |
| Archivo | google | variable width 62 to 125: one family from condensed to expanded |

### Serif (editorial, luxury, culture: needs a reason)
| Font | Source | Use |
|---|---|---|
| Zodiak | fontshare `zodiak` | sharp contemporary serif, great italics |
| Gambetta | fontshare `gambetta` | classical, refined text and display |
| Erode | fontshare `erode` | soft contemporary serif |
| Sentient | fontshare `sentient` | literary, calm |
| Boska | fontshare `boska` | high-contrast display serif with drama |
| Gambarino | fontshare `gambarino` | single-weight display serif with flair |
| Newsreader | google | optical sizes, editorial text |
| Gloock | google | heavy high-contrast display |
| Young Serif | google | warm old-style display |
| Bodoni Moda | google | fashion contrast (optical sizes) |
| Libre Caslon Display | google | bookish elegance |
| Hedvig Letters Serif | google | contemporary, slightly odd, memorable |
| Italiana | google | thin fashion caps |
Avoid as reflex: Fraunces, Instrument Serif, Playfair (overused by generators).

### Mono and accents
| Font | Source | Use |
|---|---|---|
| JetBrains Mono, DM Mono, IBM Plex Mono, Geist Mono | google | data, code, timecode |
| Fragment Mono, Martian Mono, Space Mono | google | characterful mono |
| Azeret Mono | fontshare `azeret-mono` | precise geometric mono |
| Caveat, Nothing You Could Do, Reenie Beanie | google | handwritten annotations (Maria Vasilyeva's scribbles) |
| Pinyon Script, Mrs Saint Delafield | google | formal script accent (LxL Creative "Real people.") |

## Pairings that work

- Switzer (all) + Zodiak italic (one voice for pull quotes, case-study titles).
- Archivo expanded 800 (display) + Archivo 400 normal width (text): one family, two personalities.
- Big Shoulders Display (display, uppercase, huge) + Host Grotesk (text).
- Supreme (all) + Martian Mono (meta, timecode).
- Bodoni Moda (display, optical size large) + Instrument Sans (text and UI).
- Panchang (wordmark, short headings) + General Sans (text).
- Any grotesk + a handwritten accent used ONLY for annotations that carry real information.

## Setting display type (where sites win)

```css
.display {
  font-family: var(--f-display);
  font-size: var(--t-mega);          /* clamp(4rem, 1.2rem + 14vw, 16rem) style */
  line-height: 0.85;                  /* 0.82 to 0.95 for caps/heavy; 0.95 to 1.05 with descenders */
  letter-spacing: -0.045em;           /* more negative as size grows; per-family, check visually */
  font-feature-settings: 'ss01', 'kern'; /* enable stylistic sets the family offers */
  text-wrap: balance;
  margin-left: -0.06em;               /* optical alignment: large glyph side-bearings */
}
```
- Size type to the **container**, not the viewport, when it must fill a width:
  `font-size: clamp(3rem, 18cqi, 20rem)` with `container-type: inline-size` on the parent.
- Mask reveals need descender room: the engine adds `padding-bottom: 0.08em` to split lines.
  With line-height under 0.9, check that descenders (g, j, p, q, y) are not clipped.
- Hanging punctuation for quotes: `hanging-punctuation: first;` (Safari) or a negative
  `text-indent` on the opening quote.
- Numbers: `font-variant-numeric: tabular-nums` for counters, years, indexes.
- Use real typographic characters: ’ “ ” × … and non-breaking spaces (`&nbsp;`) where a line
  must not break (between a number and its unit, at the end of display lines to avoid widows).

## Scale

Fluid, defined once in tokens, with large jumps between display and text (award sites use
contrast, not a gentle modular scale):
```css
--t-mega: clamp(4rem, 1.2rem + 14vw, 16rem);
--t-xl:   clamp(2.5rem, 1.4rem + 4.8vw, 6rem);
--t-l:    clamp(1.75rem, 1.3rem + 1.9vw, 3rem);
--t-m:    clamp(1.25rem, 1.1rem + 0.6vw, 1.625rem);
--t-body: clamp(1rem, 0.95rem + 0.2vw, 1.125rem);
--t-s:    0.875rem;  --t-xs: 0.75rem;
```
Body copy 16 to 18 px, measure 45 to 70 characters (`max-width: 38rem` or `60ch`).
UI text (nav, captions, meta) 12 to 14 px with AA contrast. Uppercase only when the family's caps
are designed for it, tracked +0.02 to +0.06em at small sizes.

## Kinetic type ideas (see motion.md for code)

- Line mask reveals (engine `data-split="lines"`): the baseline; do not make it the only idea.
- Character cascade with rotation on the hero name (`data-split="chars"`), once.
- Variable-font axis animation (weight/width) driven by scroll or pointer: Archivo width,
  Mona Sans width, Bricolage optical size. Animate `font-variation-settings` on few characters.
- Scroll-scrubbed horizontal type that runs past at a different speed than the page.
- Letters as masks for imagery or GL (`background-clip: text` or GL text texture).
- Text scramble/decode for tech concepts (keep the final text accessible in the DOM).
