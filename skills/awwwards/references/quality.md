# Quality: the developer checklist (and the Usability 30%)

These are the six developer criteria: **Semantics/SEO, Animations/Transitions, Accessibility,
WPO, Responsive Design, Markup/Meta-data.** Recent award winners score about 8 on animations
but only 6.4 to 7 on accessibility, so accessibility and performance are where you beat the
field.

## Semantics / SEO / Markup
- `<html lang>`, one `<h1>`, ordered headings, landmarks (`header`, `nav`, `main`, `footer`),
  lists as lists, buttons for actions, links for navigation.
- Unique `<title>` (≤ 70 chars) and meta description per page; canonical; OG title/description/
  image (1200x630); Twitter card; JSON-LD (`Person` for portfolios, `Organization` for studios,
  `CreativeWork` on case studies if useful); sitemap; robots.txt; favicon (SVG + 32 px PNG + apple-touch-icon).
- Images: `width`/`height` attributes (or aspect-ratio boxes), `loading="lazy"` below the fold,
  `fetchpriority="high"` on the hero image, `decoding="async"`, modern formats (`next/image`, Astro `<Image>`).
- All content is in server-rendered HTML (both stacks do this by default). No content exists only in a canvas.

## Accessibility (where most award sites lose points)
- Contrast AA: body 4.5:1, large text 3:1, including text over images and over animated backgrounds.
- Visible `:focus-visible` everywhere in the system's style; skip link (in the layout contract).
- Keyboard: every interaction reachable and operable; hover-only content also on focus; menus
  trap focus, close on Escape, restore focus.
- Reduced motion: no smooth scroll, GL, scrub, parallax, or loader theatrics (engine); verify the
  `r-*` screenshots show complete, visible content.
- Text stays text (SplitText keeps it readable; never bake headlines into images or canvas only).
- Native cursor visible; touch targets ≥ 24 px (44 px primary); no hover traps on touch.
- Route changes are announced: both Next's router and Astro's ClientRouter announce the new
  title. With a custom router, move focus to `main` after navigation.
- `aria-hidden` on decorative duplicates (marquee copies, GL canvas, cursor follower).

## WPO (performance)
| Metric | Award target |
|---|---|
| LCP | < 1.5 to 2.5 s (hero text or image is the LCP; never the canvas) |
| CLS | < 0.05 |
| INP | < 100 to 200 ms |
| Total weight | < 3 MB (images dominate: compress) |
| JS | < 300 KB gzipped per page (`audit.mjs` reports it). Baselines: Astro + full engine ~75 KB, Next + full engine ~250 KB. Lazy-load Three/models |
| Fonts | ≤ 4 files preloaded at most 2; woff2 only; subset latin |
| Frame rate | 60 fps scroll on mid-range hardware |

- Self-host fonts (`scripts/font.mjs`), `font-display: swap`, matching fallback metrics if CLS appears.
- Images: `next/image` or Astro `<Image>`/`<Picture>` with AVIF/WebP, `sizes`; the hero eager with `fetchpriority="high"`.
- Video: muted, playsinline, poster, < 4 MB, lazy for below the fold, `preload="none"` off-screen.
- Optional: run Lighthouse (`npx lighthouse <url> --only-categories=performance,accessibility,seo,best-practices --view`) when network access allows.

## Responsive
- Designed at 390, 768, 1024, 1440, 1920. Check 1920 wide (large monitors are common among designers):
  cap measure, scale display type with `clamp` maxima, avoid sparse emptiness.
- `100svh`/`100dvh` for full-height sections; safe-area insets on fixed UI for notched phones.

## Animations / transitions
- No jank on enter/leave, no flash of unstyled or unrevealed content, no double animations after
  navigation (engine cleans up; your `onPage` code must return cleanups for window listeners).
- Interruptible: navigating mid-animation must not break state.
- Scroll restoration on back navigation is acceptable at top; never land mid-animation broken.

## Bugs found in real test builds (check each one explicitly)

| Bug | How it showed up | Prevention |
|---|---|---|
| Dark text on a background that turned dark | case page end state and 404 at "night" were unreadable; only the header flipped | one global ink variable on `<html>` drives all text; shoot every page to its end |
| First frame weak | scroll-driven system started at its least flattering state (pre-dawn, low contrast) | pick the initial state for the hero screenshot |
| Heading text doubled | decorative shadow copy inside `<h1>` → "NAME NAME" in SEO/AT | duplicates outside headings (audit FAILs this) |
| Zig-zag paragraph | `text-indent` applied to every SplitText line | engine CSS keeps indent on the first line only |
| Short pages jump to the end state | smooth-scroll lib reports progress 1 when a page cannot scroll | engine normalizes to 0; pin pages that need a fixed state |
| Fixed UI over content | bottom-corner clock/email over case meta; top-left name over section labels | safe zones + frame steps aside on scroll down |
| Copy repeated | hero statement sentence reused as the about heading | audit WARNs repeated sentences |
| Touch copy | "Hover a day to open it" on phones | device-neutral copy |
| Tiny targets | footer social links 18 px tall | shoot report lists small targets by name |
| Loader over budget | 1.3 s exit on top of 1.7 s progress = 3 s | `loaderMs` in shoot report ≤ 2600 |
| GL images render as empty boxes | an opaque CSS background on the `<figure>` painted over the canvas below | engine forces `background: none` on `[data-gl]`; shoot reports `glHidden` |
| Site felt static | primary hovers were color swaps; the concept froze when scrolling stopped | one treatment per role from the verb, and an idle input on the driver (motion.md, patterns.md); shoot reports `hover.colorOnly` and `idleMotion` |
| Cursor preview stuck on screen | `pointerleave` never fires when the page scrolls under a still pointer | check `elementFromPoint` on scroll (recipe fixed in motion.md) |
| Header invisible over a light photo | white UI over a full-bleed print | `mix-blend-mode: difference` on fixed UI, scrims under titles |
| Page weight looked like 5 MB | audit summed every responsive variant in the build | audit now estimates per page from referenced `src` |
| Mobile hero hole | desktop `1fr` grid row stretched on a tall phone | explicit mobile rows |
| Mobile display word breaks mid-word | a 4-letter display word at 26vw wrapped mid-word | `white-space: nowrap` + size from `cqi`/`vw` checked at 390 px |

## QA checklist (tick with evidence)
- [ ] audit.mjs: 0 FAIL; WARNs reviewed and fixed or justified
- [ ] shoot.mjs `--crawl` on every page: 0 console errors, 0 failed requests, no overflow (desktop + mobile), reduced `hiddenText` = 0, FPS ≥ 55
- [ ] Throttled mobile: `mobile.vitals.lcpMs` < 2500, `cls` < 0.05, `mobile.loaderMs` reviewed (a loader that is fine on desktop can run 4 s on a phone)
- [ ] `a11y`: 0 serious or critical axe violations; every `contrastNeedsReview` node checked by eye in the screenshots (text over images and canvas)
- [ ] `keyboard`: skip link first, `noVisibleFocus` and `invisibleFocus` empty, not `stuck`; `k-*` frames show a ring in the system's style
- [ ] `hover`: `noHoverChange` empty; every `h-NN-rest` / `h-NN-hover` pair read; each `colorOnly`, `pixels` and `masked` target judged by eye (a full fill or inversion passes, a text-color swap on a primary link does not); `covered` targets checked by hand
- [ ] `desktop.idleMotion` true, or the still page written down as a decision in `DESIGN.md`
- [ ] Every screenshot read; hero frame works as a poster; mobile frames composed
- [ ] Navigation transition frames reviewed; menu opens, traps focus and closes on Escape (try it by hand)
- [ ] Critic subagent's scores all ≥ 8, and its one-line reading of the idea matches the Concept Card
- [ ] Copy pass: no dashes, no banned words, no placeholder left unmarked
