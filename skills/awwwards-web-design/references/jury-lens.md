# The jury lens: what wins and how to self-score

Last updated: 2026-09-25

Use this when: choosing the site's one idea, setting score targets before design starts, or grading your own build before calling it award-ready.

## Rules

1. The published score is `0.4·Design + 0.3·Usability + 0.2·Creativity + 0.1·Content`, taken from a trimmed jury mean (at least 18 jurors, with the 3 scores furthest from the average dropped). It reproduces the published total on 51/51 teardowns and 9/9 annual winners [awwwards-editorial §1.2]. The community score is shown separately and never blended in, so ignore it.
2. Aim at numbers, not a feeling. SOTD needs about 7.4: recent SOTDs have a median of 7.38 and a floor of 7.17 (n=215, 2024+ [stats]). SOTM score pages have a median of 7.73 (range 7.51-8.25, n=28), and only 10% of recent SOTDs (22/215) reach 7.7. Sites of the Year 2023-2025 scored 7.92-8.25 [awwwards-editorial §2.2, §3.1].
3. Build one owned idea, rendered live, that the visitor completes. That means one sentence, one object or world taken from the brand itself, running in real time and changed by the visitor's input. 11 of the 12 highest-scoring teardowns run it as a real-time WebGL layer (10 as a 3D scene; siena-film-foundation shades image planes; mindmarket is 2D Rive).
4. Make the object the grammar. It comes back as the loader, the nav, the transitions, a decorative cursor follower (native cursor kept) and the footer (everswap, hubtown, thelinestudio-com). One idea used everywhere beats five separate effects.
5. Creativity separates the tiers: +0.86 between the top and bottom recent SOTDs. Design earns the most weighted points: 0.28 of the 0.64-point overall gap. Settle both before polishing anything else.
6. Usability is the lowest sub-score on 47/51 teardowns and on 169/215 recent SOTDs. A Usability of 7.5 or more puts a site in the top 7%. You earn it with orientation, legibility, stable frames and a mobile input model of its own.
7. The Developer Award goes to totals above 7. Accessibility, Markup and Semantics carry 45% of the dev weight, and their tier means stay flat at 6.8-7.3 from the <7.3 tier to the ≥7.7 tier (195 recent SOTDs with a dev block). Raising all three to 8.0 adds about +0.37 to the dev total and costs the creative work nothing.
8. Real time, not playback. The dev jury's Animations category counts only scripted real-time motion. Video and image sequences score nothing there [awwwards-editorial §1.4].
9. Content must be real and specific to the brand: a race calendar, a store, a provenance story, game dialogue. Lorem, stock or a template demo loses the points, and Awwwards rejects pre-made templates outright.
10. Keep the palette to one ground, one ink and at most one owned hue, with everything else in tonal steps. Use a saturated hue only when the brand owns it, and then as a field or an object colour.
11. Set the performance budget before you design the signature moment. Motion quality and WPO rise together (r = +0.47 [usability-a11y-perf §1.4]).
12. Jurors see a desktop and a mobile thumbnail side by side, watch element videos and click past the homepage. Design the 390px first screen, the loader, the footer and the 404 as deliberately as the hero.
13. The house law outranks award habit. Where winners use a slop tell, build the crafted version from "Crafted vs slop".
14. Grade the build with the section 7 rubric before shipping. A criterion below its band goes on the fix list. It is not a caveat to mention.

## 1. The scoring math

| Stage | Rule [awwwards-editorial §1.1] |
|---|---|
| Honorable Mention | Jury 6.5 or more AND users 6.5 or more, voted separately. HM jury scores are never published. |
| Site of the Day | Highest jury score of the day. A site stays eligible for 3 months. |
| Developer Award | Every SOTD goes to a separate developer jury. A total above 7 wins. 195/215 recent SOTDs carry the dev block [corpus]. |
| Site of the Month | The 8 top-scoring sites of the month are re-reviewed, and user votes carry extra weight. |
| Site of the Year | All SOTMs plus some favourites go to a plurality vote. Lando Norris won with 43 of 253 jury votes (17%). |

Selectivity: about 1 in 7 nominees becomes SOTD, and 1 in 33 SOTDs becomes SOTM. The outlier trim and the plurality vote both reward broad agreement, not the most polarising site.

```js
// Checked: lando-norris 8.12/7.90/8.71/8.18 -> 8.18; igloo-inc dev (wpo 8.0, rwd 8.4, markup 6.4,
// semantics 6.6, anim 9.6, a11y 6.6) -> 7.66. 51/51 jury totals and 49/49 published dev totals match.
const jury = (D, U, Cr, Co) => +(0.4 * D + 0.3 * U + 0.2 * Cr + 0.1 * Co).toFixed(2);
const dev = ({ wpo, rwd, markup, semantics, anim, a11y }) =>
  +(0.2 * wpo + 0.2 * rwd + 0.15 * markup + 0.2 * semantics + 0.15 * anim + 0.1 * a11y).toFixed(2);
```

To add +0.10 to the total you need +0.25 Design, +0.33 Usability, +0.50 Creativity or +1.00 Content.

| Criterion (weight) | Recent SOTD p25 / p50 / p75 (n=215) | 51 teardowns, mean | Top 12 teardowns (≥7.85), mean | SOTM pages, mean (n=28) |
|---|---|---|---|---|
| Overall | 7.29 / 7.38 / 7.53 | 7.73 | 7.95 | median 7.73 |
| Design .40 | 7.31 / 7.47 / 7.66 | 7.83 | 8.03 | 7.91 |
| Usability .30 | 7.08 / 7.19 / 7.31 | 7.40 | 7.57 | 7.45 |
| Creativity .20 | 7.38 / 7.56 / 7.79 | 7.98 | 8.33 | 8.05 |
| Content .10 | 7.31 / 7.44 / 7.65 | 7.77 | 8.02 | 7.86 |

Where the climb comes from: compare recent SOTDs at 7.7 or above (n=22) with those below 7.3 (n=56). Design is +0.70 (0.28 weighted), Usability +0.41 (0.12), Creativity +0.86 (0.17) and Content +0.63 (0.06). Design and Creativity together deliver 71% of the gap.

The developer side, over 308 Developer-Award SOTDs [usability-a11y-perf §1.3]:

| Category | Mean |
|---|---|
| Accessibility | 6.93 (below 7.0 on 51% of sites) |
| Markup | 7.22 |
| Semantics | 7.27 |
| WPO | 7.54 |
| RWD | 7.60 |
| Animations | 8.10 |

Between the top (≥7.7) and bottom (<7.3) recent SOTD tiers, Animations moves +0.83, WPO +0.46 and RWD +0.37. Semantics moves only +0.11, Accessibility +0.05 and Markup +0.04. Winners do not do those three any better, so doing them well is the cheapest differentiator.

## 2. What each criterion rewards in practice

Awwwards publishes no rubric text for the four criteria. The readings below come from the observed scores [awwwards-editorial §1.3].

**Design (40%): art direction held as one system on every route.**
- Design correlates +0.90 with the overall score on recent SOTDs, and it is never an annual winner's weakest criterion.
- Awwwards records a 1-2 colour palette on every recent page that records one (275/575 [stats]). The field may be capped, so read it as "the identity is two colours", not as a count.
- 397 of the 554 live winners checked ship 1-3 font families, and 46 show none detectable [fonts].
- Measured display sizes are a median of 80px at 1440 (p25 40.8, p75 150) and 46.8px at 390 (p25 32, p75 80). Display tracking has a median of -0.023em (n=27) and line-height a median of 1.0 (p25 0.83) [probe].
- Decisions: derive the ground from the idea's material. Use at most three families, with the display face licensed or custom and not reused from another build in this repo. Set display type at 80-150px on desktop and 47-80px on mobile (the probed median-to-p75 bands), and keep tracking between -0.02em and 0 with no glyphs touching at display size (house law: cramped display type). Use one easing family and one duration scale from `../recipes/tokens.css`. Re-compose the phone layout instead of shrinking the desktop one.

**Usability (30%): can a stranger orient, move and leave, on a laptop and a mid-range phone?**
- Jury Usability tracks the dev Responsive (+0.27) and Animations (+0.20) scores more than Accessibility (+0.18) [usability-a11y-perf §1.4]. Inferred from those correlations: jurors feel smoothness and mobile quality, and do not audit ARIA.
- Highest in the set (akaru-2 and vast also reach 7.61):
  - lando-norris 7.90: fixed corner chrome (wordmark, STORE, menu), with hover turned into tap-to-lock on phones.
  - brunos-portfolio 7.83: a map modal, an "I'm stuck" button, touch controls and an automatic quality tier.
  - siena-film-foundation 7.61: one ticket-style nav card that re-titles itself to the film on screen.
  - fluid-glass 7.60: no blocking loader, and a bottom-centre bar that names the current page.
- Lowest in the set:
  - lacoste-polo-factory 7.09: about 6s of loading, then small copy over moving sprites.
  - iyo 7.11: the manifesto exists only as particles, and the page never scrolls.
  - ponpon-mania 7.12: the comic is canvas-only, with cream nav text on orange at about 1.6:1.
  - cartier-watches-wonders-2025 7.17: no menu, and 11-12px white caps over pale scenes.
- Decisions: see section 5.

**Creativity (20%): an original concept and the interaction that expresses it.**
- Creativity is the top sub-score on 33/51 teardowns.
- It has the widest spread: SD 0.34 on recent SOTDs, against 0.19 for Usability. That spread is the room to pull away.
- The jury scores the idea, not the amount of WebGL. dont-board-me scored Creativity 8.00 (overall 7.83) in flat 2D and won Users' Choice 2024.
- A juror-attributed post says copying the season's trend board, such as the horizontal-scroll gallery, costs points fast [awwwards-editorial §1.3, sec].
- Decisions: see section 3.

**Content (10%): authored, specific words and imagery that serve the concept.**
- Highest in the set:
  - immersive-garden-website 8.34.
  - lando-norris 8.18: a first-person racer voice plus fan-hub utility (results, stats).
  - brunos-portfolio 8.18: first person, crediting collaborators by name.
  - messenger 8.15: quest dialogue.
  - tracing-art 8.09: one plain sentence per scroll beat, each carrying a date, an owner or a city.
- Lowest in the set:
  - everswap 7.10: metaphor fragments and brand puns.
  - lacoste-polo-factory 7.13: prize-draw copy.
  - lama-lama-2 7.39: slogan-only agency voice.
- The submission counts too. Awwwards wants 1600×1200 thumbnails, recommends videos and shows the mobile thumbnail next to the desktop one.
- Decisions: every section carries a fact (a name, date, place, number or material) or a working tool. Microcopy, loader lines and the 404 speak in the headline's voice.

## 3. The SOTY/SOTM pattern: one owned idea, rendered live

| Site (score) | The sentence | Where the object comes from | What the visitor does | Where it recurs |
|---|---|---|---|---|
| lando-norris (SOTY 2025, 8.18) | Put the helmet on the driver | His real race helmet (GLB) over a depth-mapped portrait | A fluid cursor trail paints the helmet on | Livery swaps per season further down; the lime is the livery |
| igloo-inc (SOTY + Dev 2024, 7.92) | The portfolio, frozen in ice | The client's own portfolio companies | Scroll cranes the camera through the world | Intro, crystals, HUD, particle footer |
| messenger (Dev SOTY 2025, 7.92) | A courier on a tiny planet | A playable world | Walk and deliver | Title tiles, HUD and dialogue all drawn in one ink-outline renderer |
| brunos-portfolio (8.11) | Drive through my work | A toy world with physics | Drive and find secrets | The reveal radius is the loader and the intro |
| immersive-garden-website (8.00) | The studio carved in plaster | The studio's own craft, as material | Scroll raises motifs, the cursor presses the surface | The menu floods the same relief |
| oryzo-ai (7.86) | A deadpan AI launch for a cork coaster | One coaster | Scroll hands it between photoreal 3D and 2D drawings | Every section boundary |
| mindmarket (7.85, 2D) | Services as a board-game path | A commissioned illustrated journey | Scroll draws the trail | Cards ride over it |
| cartier-watches-wonders-2025 (7.64) | Each watch lives in a world built from its own geometry | Bracelet links become a wall, the Tank case becomes frames | Scroll flies through into the next world | Every chapter |

Grammar reuse, the move that turns an effect into an identity:
- everswap: the split-diamond mark is the preloader portal, the chapter nav, the copy frame and the closing mask.
- hubtown: the logo's square O is the cube, the preloader, the map pins and the city.
- thelinestudio-com: the loading bar settles into the wordmark's crossbar.
- maxima-therapy: the transition's last frame and the hero are the same drawing.
- active-theory-v6: the logo ring returns upside down in the footer.
- lama-lama-2: the 4×4 logo is the dither primitive that renders every image.

What the numbers say:
- 11 of the 12 teardowns at 7.85 or above run real-time 3D. mindmarket is the exception.
- Across all 51, the 36 sites with a WebGL/3D layer average 7.74 overall and the 15 without average 7.69. Inferred (small, unmatched sample): the medium alone is worth about 0.05, the owned idea is the lever, and 3D is how the top tier renders it.
- Pre-rendered work still wins its lane: terminal-industries' 410-frame scrubbed film (7.68) and opal-tadpole's 321-frame turntable (E-commerce 2024). But every Site of the Year and Developer SOTY since 2023 has been real-time.

The owned-idea worksheet (do this before any layout):
1. List the brand's owned nouns: product geometry, logo parts, founder artefacts, the domain's materials, a place. For example, the arch (era-residence), the film strip (siena-film-foundation), the trail map (san-rita), animation-desk material (thelinestudio-com).
2. Write "[visitor verb] the [owned object] to [brand truth]". Then run the swap test: put a competitor's name in. If the sentence still works, the idea is not owned.
3. Choose the medium the verb needs:
   - an object you turn or enter: real-time 3D (`../recipes/three-hero.js`)
   - a brand built on film or photography: a shader over DOM media (`../recipes/webgl-image-hover.js`)
   - drawn characters: Rive or canvas
   - a logo that morphs: SVG or Lottie
4. Give the object at least 3 system roles: loader, nav or menu, section transition, cursor, footer, 404.
5. Budget it before building. 3D payload before first interaction stays at or under 1.5 MB on mobile and 3 MB on desktop (a house rule, not an observed winner median: messenger loads about 5.7 MB up front). Cap the device pixel ratio at 2, as 4 probed winners do, and at 1.5 for heavy fragment work. Target 60 fps, and degrade quality before dropping below 30 [webgl-3d-stack §6.1]. Show a poster first.
6. Keep everything around it a real website: DOM text, a real nav and a working utility.

## 4. What separates SOTD from Honorable Mention

HM jury scores are never published, so this comparison rests on thresholds, tags and account type. The sample is 117 SOTDs (2026-06-01 to 09-25) against 139 HM-only sites (2026-08-09 to 09-25). Tags are chosen by submitters [awwwards-editorial §3.2].

| Measure | SOTD | HM only |
|---|---|---|
| Jury score | Highest of the day; recent floor 7.17, median 7.38 | 6.5 or more |
| WebGL / 3D / Three.js tags | 42.7% / 40.2% / 29.9% | 16.5% / 23.7% / 18.0% |
| GSAP | 54.7% | 38.1% |
| Promotional (one-idea campaign) | 13.7% | 2.2% |
| Minimal / Parallax | 7.7% / 6.0% | 17.3% / 11.5% |
| Illustration / Graphic design | 3.4% / 6.8% | 10.1% / 14.4% |
| Framer / WordPress / React | 3.4% / 3.4% / 1.7% | 7.9% / 7.9% / 7.9% |
| Webflow | 22.2% | 18.7% |
| "404 pages" tag | 10.3% | 3.6% |
| PRO (paid studio) account | 84% | 39% |

What keeps work at HM [awwwards-editorial §3.3, sec]:
- minimalism or parallax as the whole idea
- a builder or theme structure a juror recognises
- motion with no hierarchy, or dropped frames
- a phone layout that collapses instead of being re-composed
- long progress-bar preloaders
- a custom cursor that hides the native one
- thin or stock content

Decision: if the only honest tags for your concept are "Minimal", "Parallax" or "Clean", you are designing an HM. Add the owned live idea, or accept HM.

## 5. Where points are cheapest

**Jury Usability.** It carries 30% of the weight and it is compressed: 169/215 recent SOTDs score lowest on it, only 15/215 reach 7.5 and 2/215 reach 7.7. Raising it from the SOTD median (7.19) to 7.55 adds +0.11 to the total, as much as +0.54 of Creativity. The failures in the 51 teardowns repeat, so each one is a fix you already know:

| Recurring failure | Seen in | Fix |
|---|---|---|
| No first-party reduced-motion path | 38/51. Only 5 gate their main motion (champions-for-good, shed, thelinestudio-com, the-renaissance-edition, vast) and 8 handle one effect [probe + teardowns] | Designed reduced state (`../recipes/boot.html-snippet.html`, `../recipes/motion-core.js`); vast's single `--motion` multiplier on every CSS duration |
| Text under 12px | lando-norris 8.33px eyebrows ×39; era-residence 8px CTA; hubtown 8-9px; zentry 9px. Probed body median is only 14.4px | Body 16px or more, labels 12px or more, mono only on data |
| Text over moving media with a token scrim | bennett-clive (~1.5:1 over snow), depo-luxe (14% veil), vast (10% overlay), lacoste-polo-factory | Measure the worst frame; scrim behind the text only [imagery §3.1] |
| No DOM heading on the first screen, or the key copy only in canvas | messenger, brunos-portfolio, gq-ap-the-extraordinary-lab, pacome-pertant-portfolio (no `h1`); iyo (a DOM `h1`, but the manifesto lives only in particles) | DOM holds the words, the canvas is `aria-hidden` |
| Long gate before content | era-residence locks scroll ~10.2s; igloo-inc and lacoste-polo-factory ~6s | Content live at first paint; an intro of 2s or less that can be skipped [elements-catalog §1] |
| Consent UI eats the first phone screen | floema (whole screen), vast (~50%), dropbox-brand (~22%), david-whyte-experience | 25% of the screen or less, dismissible, focus never hidden behind it |
| Zoom blocked | active-theory-v6, leo-parpeix-portfolio-2026; 10% of 60 probed winners [usability-a11y-perf §1.5] | Never set `user-scalable=no` or `maximum-scale=1` |

What the top Usability sites share:
- A persistent "you are here" cue with a visible exit at every scroll depth: the ticket card on siena-film-foundation, the named bar on fluid-glass, the I-XII chapter rail on the-renaissance-edition, the chapter pill on tracing-art.
- A mobile input model of its own: tap-to-lock on lando-norris, touch controls on brunos-portfolio, accelerometer tilt on Lusion [awwwards-editorial §2.3].
- A help affordance in any game-like UI.
- Native scroll, with at most one pinned section.

**Developer Award: Accessibility, Markup, Semantics.**
- The math: raise Accessibility from 6.93 to 8.0 (+0.107 to the total), Markup from 7.22 to 8.0 (+0.117) and Semantics from 7.27 to 8.0 (+0.146). That is +0.37.
- Accessibility correlates +0.03 with Animations, so nothing is traded away.
- The best Accessibility score in the 51 is 7.6 (artefakt, fluid-glass, messenger, opal-tadpole), so 8.0 beats every teardown.
- The patterns to copy:
  - lando-norris keeps a real `h1`/`h2` as screen-reader elements and gives each SplitText line a screen-reader clone.
  - the-renaissance-edition ships 9 reduced-motion blocks in CSS plus JS handling.
- The full gate is [usability-a11y-perf §2 A-H]. The recipes pass no-JS, reduced-motion, no-WebGL and CDN-blocked runs (`../recipes/test_recipes.py`).

## 6. 2025-2026 direction: what is rising, what is fading

**Caveat first.** Awwwards changed its tagging in August 2025. Technology tags (GSAP, WebGL, Three.js, Webflow) appear on 0-16% of SOTDs every month through July 2025, then on 94-100% from September 2025, and mean tags per site rose from about 7.8 to 10. Any "GSAP went from 1% to 50%" reading is an artifact. Compare technology tags only within September 2025 to September 2026 (388 SOTDs). Non-technology tags stay comparable across years [awwwards-editorial §4.1].

| Rising | Evidence | Build decision |
|---|---|---|
| Real-time 3D as the dividing line | WebGL tag 28.3% (Sep 2025-Feb 2026), then 39.4% (Mar-Sep 2026); all three recent SOTYs; `webgl2` context on 41/51, GLB on 19/51, KTX2 on 14/51 [probe] | Plan a live object; ship GPU-compressed textures |
| Worlds and games as websites | messenger, brunos-portfolio; the Games & Entertainment category fell 9.3%→4.9% as mechanics moved into brand and portfolio sites | Game mechanics in service of a brand, with help and exits |
| WebGPU at the very top | 2/51 (brunos-portfolio, shader-development-studio) [probe]; no Awwwards tag exists | WebGL2 by default; WebGPU through TSL only with a fallback |
| Serious and B2B brands going expressive | Business & Corporate 20.2%→24.3%; Technology 17.2%→21-26%; terminal-industries, oryzo-ai, dropbox-brand, floema | A dry brief is the opening, not the excuse |
| Luxury real-time cinema | Luxury tag 3.0% (2024) → 11.6% (2026); cartier-watches-wonders-2025, gq-ap-the-extraordinary-lab | One continuous timeline; sound as an opt-in layer |
| Storytelling structure | 16.4% (2024) → 23.2% (2026) | One narrative axis mapped to scroll |
| Modern CSS as the craft baseline | `:has()` 17/51, `text-wrap` 13/51, oklch/color-mix 10/51, view transitions 4/51, scroll-driven animations 4/51 [probe] | Use them; progressive, never load-bearing |
| Specificity over polish | A 2026 young-jury member reports that clean work has become the norm and that the standouts are specific, opinionated and rooted in a place [sec] | The swap test in section 3 |
| Sound at the top tier | Howler.js on 7 of 30 SOTY 2025 nominees [sec], while the Sound-Audio tag stays at 5-8% of all SOTDs | Authored sound as an opt-in layer behind a visible toggle, never autoplay |
| Free GSAP plugins | GSAP is free for all users, SplitText and MorphSVG included (gsap.com/pricing, read 2026-09-24); SOTY 2025 shipped on Webflow | Split headings only, with SplitText `aria: 'auto'` and a revert on complete, as `../recipes/motion-core.js` does |

| Fading as a winning default | Evidence |
|---|---|
| Typography-only minimalism | Typography tag 27.3% (2023) → 18.7% (2026); Minimal 13.4% → 10.1% |
| Parallax or big-image hero as the main idea | Parallax 9.8% → 7.1%; Big Background Images 10.4% → 6.4% |
| Flat illustration by default | 6.0% in 2026, down from 8.5-11.8%; it still wins when authored (mindmarket) |
| Page-transition showcases | Transitions 26.8-28.3% → 15-20% (possibly a taxonomy effect) |
| Horizontal-scroll galleries | 2-4% every year; named by a juror as the stock derivative move [sec] |
| The clean, safe B2B page | "Promotional" fell to 11.6% in 2026 while corporate and technology categories rose; Razorpay's case study argues against the product-in-the-hero formula |

## 7. Pre-ship self-score rubric

### 7.1 Evidence pack (collect before scoring)

| ID | Evidence | How |
|---|---|---|
| E1 | 1440×900 screenshots at every 100vh on home, one inner page, contact/about and the 404 | Playwright wheel-scroll, settle ≥1s per step |
| E2 | The same at 390×844 | Mobile context with touch |
| E3 | 10-20s recordings of the signature moment, loader, menu open, one transition and the footer (the jury's element videos) | Playwright `recordVideo` |
| E4 | No-JS and reduced-motion screenshots | `../recipes/test_recipes.py` scenarios, or [usability-a11y-perf §7.1-7.2] |
| E5 | Probe JSON at 1440 and 390, captured while the signature moment plays | Snippet below |
| E6 | LCP, CLS and INP | Lighthouse mobile plus the LCP observer [usability-a11y-perf §7.7-7.8] |
| E7 | Keyboard tab-through, one screenshot per focus stop | Manual or `page.keyboard.press('Tab')` |
| E8 | Contrast: an axe sweep plus manual worst-frame samples for text over media | [usability-a11y-perf §7.6] |
| E9 | Text dump of every UI string, plus each route's `<head>` | `document.body.innerText` and the `<head>` HTML |
| E10 | Submission thumbnails: desktop 1600×1200 and mobile | Composed, not cropped screenshots |

```js
// page.evaluate(probe) at 1440 and 390. Tested 2026-09-25 in headless Chromium on ../recipes/demo/*.html served
// over http (file:// blocks their module imports): all clean; a broken fixture fired every check. Review flags by hand.
const probe = async () => {
  const q = (s) => document.querySelector(s);
  const skip = (el) => el.closest('[aria-hidden="true"],[inert],[hidden],dialog:not([open]),template,noscript,script,style');
  const shown = (el) => el.checkVisibility ? el.checkVisibility({ opacityProperty: true, visibilityProperty: true })
    : getComputedStyle(el).opacity !== '0';
  const texty = [...document.body.querySelectorAll('*')].filter((el) => !skip(el) &&
    [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 1));
  const boxed = texty.filter((el) => { const r = el.getBoundingClientRect(); return r.width && r.height; });
  const px = boxed.filter(shown).map((el) => parseFloat(getComputedStyle(el).fontSize));
  const targets = [...document.querySelectorAll('a[href],button,[role=button],input,select,summary')]
    .filter((el) => !skip(el) && shown(el) && !el.closest('p,li'))
    .map((el) => el.getBoundingClientRect()).filter((r) => r.width && r.height);
  const vp = q('meta[name=viewport]')?.content || '';
  const first = q('a[href],button,input,[tabindex]:not([tabindex="-1"])');
  const frames = await new Promise((res) => { let n = 0, worst = 0; const t0 = performance.now(); let last = t0;
    const tick = (t) => { n++; worst = Math.max(worst, t - last); last = t;
      t - t0 < 3000 ? requestAnimationFrame(tick) : res({ fps: Math.round(n * 1000 / (t - t0)), worstFrameMs: Math.round(worst) }); };
    requestAnimationFrame(tick); });
  return {
    lang: document.documentElement.lang || null, title: document.title,
    description: q('meta[name=description]')?.content || null, ogImage: q('meta[property="og:image"]')?.content || null,
    h1: document.querySelectorAll('h1').length, main: !!q('main'),
    skipLink: !!first && /^#/.test(first.getAttribute('href') || ''),
    zoomBlocked: /user-scalable\s*=\s*(no|0)|maximum-scale\s*=\s*1(\.0+)?(?![\d.])/i.test(vp),
    overflowX: document.documentElement.scrollWidth > innerWidth,
    textHiddenNow: boxed.filter((el) => !shown(el)).length,   // each one needs a reason (closed menu, inert)
    minTextPx: Math.min(...px), textUnder12px: px.filter((s) => s < 12).length,
    targetsUnder24px: targets.filter((r) => r.width < 24 || r.height < 24).length,
    canvases: [...document.querySelectorAll('canvas')].map((c) => c.getAttribute('aria-hidden') === 'true' ? 'hidden' : 'EXPOSED'),
    nativeCursorHidden: [document.documentElement, document.body, q('main')].some((el) => el && getComputedStyle(el).cursor === 'none'), ...frames,
  };
};
```

### 7.2 The checks

Each check is yes or no. A "yes" counts only when its evidence is on disk.

| ID | Design (8) | Evidence |
|---|---|---|
| D1 | The first 1440×900 frame is one composition owned by the signature; no unplanned sliver of the next section shows | E1 frame 0 |
| D2 | One ground, one ink and at most one owned hue, used as a field or object, never sprayed on labels, dots or buttons; everything else is tonal steps | E1, plus the distinct computed `color` and `background-color` values: one saturated hue family at most |
| D3 | At most 3 families; the display face is licensed, custom or drawn, never the Google rotation, and not reused from another build here; display 80-150px at 1440 and 47-80px at 390; tracking -0.02em to 0 with no touching glyphs at display size | `document.fonts`, the `h1` style, a zoomed E1 crop |
| D4 | The signature recurs in at least 3 of: loader, nav or menu, transition, decorative cursor follower, footer, 404 | E1, E3 |
| D5 | Inner pages and the 404 hold the same system as home | E1 routes |
| D6 | The 390px first screen is re-composed, not shrunk; `overflowX` is false | E2, E5 |
| D7 | Motion has hierarchy: one element leads, the rest follow; one easing family; durations from one scale | E3, `../recipes/tokens.css` |
| D8 | No row of "Crafted vs slop" below appears in its slop form | E1-E3 walked against the table |

| ID | Usability (10) | Evidence |
|---|---|---|
| U1 | At 0/25/50/75/100% scroll, a current-location cue and a way out (menu) are visible | E1, E2 |
| U2 | Headline and nav are readable at first paint; mobile LCP ≤ 2.5s; no full-screen gate over 2s; any intro can be skipped | E6, E3 |
| U3 | `textUnder12px` = 0, body ≥ 16px, and contrast ≥ 4.5:1 (3:1 at 24px and up) against the worst frame behind | E5, E8 |
| U4 | During the signature, ≥ 55 fps at 1440 and ≥ 30 fps on a mid phone; `worstFrameMs` < 50 | E5 |
| U5 | Scroll stays native: find-in-page lands on deep text, End/Space/scrollbar work, at most one pinned section and only on desktop | Manual |
| U6 | Hover becomes tap, scroll or tilt on touch; primary targets 44px; `targetsUnder24px` reviewed to 0; `zoomBlocked` false | E2, E5 |
| U7 | `skipLink` true; every control reachable with a visible focus ring; Esc closes overlays and returns focus | E7 |
| U8 | Reduced motion is a designed state: no transforms animate, smooth scroll is off, WebGL shows a still, video is paused, and the page still looks composed | E4 |
| U9 | `textHiddenNow` = 0 (or only closed menus and dialogs); the no-JS pass shows every text and link | E4, E5 |
| U10 | Consent UI covers ≤ 25% of the first phone screen; sound is opt-in behind a visible toggle; `nativeCursorHidden` is false | E2, E5 |

| ID | Creativity (6) | Evidence |
|---|---|---|
| C1 | The idea fits one sentence and fails the swap test | The written sentence |
| C2 | The signature renders live and answers input (cursor, scroll, drag, time, tilt), not a looped video | E3 |
| C3 | The visitor's action changes the object (paint, drive, pour, draw, assemble) | E3 |
| C4 | The main idea is not a trend-board move: horizontal gallery, parallax stack, generic particle sphere, blob or a plain split-text reveal | Section 6 fading list |
| C5 | Section changes happen inside the concept (a camera move, a material wipe, the object's own geometry), not generic fades (igloo-inc, oryzo-ai, cartier-watches-wonders-2025) | E3 |
| C6 | A second-layer discovery rewards a return visit: gil-huybrecht's hidden mode, the-watch showing the visitor's local time, son-daven's night set between midnight and 7am | List it |

| ID | Content (6) | Evidence |
|---|---|---|
| K1 | Every section carries a concrete fact written for this brand; a grep for lorem, placeholder and generic claims comes back empty | E9 |
| K2 | At least one working utility or complete narrative sits behind the showpiece (store, calendar, case studies with outcomes, booking, archive) | Route list |
| K3 | Imagery is commissioned or generated for this art direction and graded as one family, with no stock tells | E1 contact sheet |
| K4 | Microcopy, loader lines, buttons and the 404 share the headline voice | E9 |
| K5 | Sound and video are authored; speech has captions | E3, markup |
| K6 | The submission pack is composed: 1600×1200 desktop and mobile thumbnails, plus element videos of the signature, loader, menu, transition, footer and 404 | E10, E3 |

### 7.3 From yes-counts to a score, then targets

| Yes count | Design (of 8) | Usability (of 10) | Creativity (of 6) | Content (of 6) |
|---|---|---|---|---|
| All | 7.9-8.1 | 7.5-7.7 | 8.1-8.4 | 7.9-8.2 |
| All but 1-2 | 7.6-7.8 | 7.3-7.4 | 7.8-8.0 | 7.6-7.8 |
| All but 3-4 | 7.3-7.5 | 7.1-7.2 | 7.4-7.7 | 7.3-7.5 |
| Fewer | below 7.3 | below 7.1 | below 7.4 | below 7.3 |

Hard caps: a failure on C1 or C2 caps Creativity at 7.6, because the idea is the lever. A failure on U9 or D8 is a house-law failure: fix it before scoring at all.

The bands are a heuristic anchored to the observed ranges (Usability 7.09-7.90, Creativity 7.27-8.71 across the 51), not a fitted model. Use them to rank fixes, not to predict the jury.

| Target | Design | Usability | Creativity | Content | `jury()` |
|---|---|---|---|---|---|
| SOTD, safe margin | ≥ 7.6 | ≥ 7.3 | ≥ 7.8 | ≥ 7.6 | ≥ 7.55 |
| SOTM contention | ≥ 7.9 | ≥ 7.5 | ≥ 8.1 | ≥ 7.9 | ≥ 7.82 |

Fix order: sort the failing checks by weight × band step. One Design band step (+0.3 D, so +0.12 total) outranks one Content step (+0.03 total). Usability failures are the fastest to clear.

### 7.4 Developer self-score

| Category (weight) | Measured check | Target | 51-site mean |
|---|---|---|---|
| WPO (.20) | Mobile LCP ≤ 2.5s, CLS ≤ 0.1, INP ≤ 200ms; 3D before first interaction ≤ 1.5 MB mobile / 3 MB desktop; KTX2 textures; one `fetchpriority="high"`; 0 console errors | ≥ 8.0 | 7.78 |
| RWD (.20) | No `overflowX` at 320 and 390; re-composed phone layout; targets ≥ 24px (44px primary); `svh` hero; DPR cap | ≥ 8.0 | 7.66 |
| Markup (.15) | 0 validator errors; landmarks; `img` width, height and alt; OG and Schema.org; favicon set | ≥ 7.8 | 7.25 |
| Semantics (.20) | One `h1` in server HTML; ordered headings; unique title, description and canonical per route; sitemap; `<a href>` navigation | ≥ 7.8 | 7.27 |
| Animations (.15) | Real-time signature at the U4 frame rates; one easing family; transitions keep history and focus | ≥ 8.6 | 8.42 |
| Accessibility (.10) | U7, U8 and U3 pass; a pause control on anything moving over 5s; canvases `aria-hidden` with DOM mirrors | ≥ 7.8 | 6.88 |

These targets give `dev()` = 8.00. The best teardown is messenger at 8.21.

Ship gate for an award attempt: `jury()` ≥ 7.55 with no criterion under its SOTD band, `dev()` ≥ 7.9 with no category under 7.5, and zero house-law failures.

## Crafted vs slop

| Award habit | Slop version | Crafted version |
|---|---|---|
| Scroll reveals (keyword hit in about 45/51 audits' `slop_risks`) | Copy starts at `opacity: 0` and waits for a trigger; blank when JS stalls | Visible by default; settle the transform only; masked line rise on the hero only, behind a CSS deadline (`../recipes/motion-core.js`, `../recipes/boot.html-snippet.html`) |
| Letter-roll or growing-underline link hovers (lando-norris) | Underline wipes in; every link rolls its letters | Static underline in body copy; hover is a tonal colour shift (a weight shift reflows the line), or an icon sliding inside a fixed box, in `--dur-2` (200ms) from `../recipes/tokens.css` |
| Magnetic buttons, hover lift | The button box jumps or scales toward the cursor | The box never moves; the hover state is a tonal fill change; at most the label drifts ≤ 6px inside the static hit area, off on touch and under reduced motion (`../recipes/magnetic.js`) |
| Poster-bright accent (lando-norris #D2FF00) | A neon hue on labels, dots and buttons | Tonal accents; a saturated hue only when the brand owns it, as a field or object colour (the lime is the helmet livery) |
| Cream or bone ground (keyword hit in about 20/51) | A #F9F4EB sheet as the safe premium ground | A ground from the idea's material, like igloo-inc's rendered fog or immersive-garden-website's plaster, or a chosen brand ground (a green-black, warm charcoal or oxblood-black), never the default blue-charcoal or the gray-100 UI-kit neutral |
| Grain or chromatic post over the frame (keyword hit in 10/51) | Grain and aberration split the UI text (shader-development-studio, siena-film-foundation) | Grain on the substrate below content; at most one masked display word; never on UI text |
| Fixed background field | One fixed sheet trailing behind everything, the nav included | The background is the scene and reacts to scroll (immersive-garden-website's relief), or there is none |
| Giant footer wordmark | Clipped caps pasted at the bottom | Composed, centred, uncut and derived from the page axis (bennett-clive's row that slides down and scales up), or skipped |
| Free-shelf display face (Inter on 60/525 sites [fonts]) | Inter, Instrument Serif or IBM Plex Mono carrying the brand | A licensed or custom display face used with conviction; free faces only as quiet body text |
| Violet, periwinkle or lilac UI (flagged in 12/51) | A purple accent or a lilac gradient on chrome | Colour taken from the object's material; an owned violet stays inside the world's lighting, not the UI |
| Percentage preloader | A full-screen counter to 100; era-residence locks scroll ~10.2s | DOM content live at first paint; a scene-scoped, honest loader; intro ≤ 2s, skippable, once per session |
| Custom cursor (`cursor: none` on 10/58 probed winners) | The native cursor is hidden behind a DOM ring | Native cursor kept; any follower is decorative, `aria-hidden`, and off on touch and under reduced motion |
| UI text drawn in WebGL (igloo-inc, messenger) | The canvas holds the only copy of the words | DOM text is the source; the canvas draws the effect on top and stays `aria-hidden` |
| Tiny mono meta labels | 8-10px caps over imagery (lando-norris, san-rita, hubtown), one tracked-caps costume on nav, buttons and captions alike | Labels ≥ 12px; mono only on data; nav, buttons and captions each get their own treatment; contrast measured on the worst frame |

## Exemplars

Full entries are in [the casebook](./casebook.md).

- **lando-norris**: an owned object made touchable, with the best Usability in the set (7.90): corner chrome, tap-to-lock on phones and screen-reader heading clones.
- **igloo-inc**: the client's content becomes the object, and the 3D stays legible on scroll. Also shows what WebGL-only UI text costs: Semantics 6.6, Markup 6.4, Accessibility 6.6.
- **messenger**: performance as the design constraint (WPO 8.8, dev 8.21, the best in the set). Study the budget, not the canvas-only UI.
- **brunos-portfolio**: a game that still scores Usability 7.83, thanks to the map modal, the help button, touch controls and an automatic quality tier. Built on WebGPU through TSL.
- **immersive-garden-website**: a material substrate instead of a background colour; Content 8.34, the highest in the set.
- **siena-film-foundation**: the metaphor taken from the domain (a projector strip), plus a one-card nav that always says where you are.
- **oryzo-ai**: a deadpan concept scored as Creativity (8.35); one object handed between 3D and 2D drawing at every section boundary.
- **mindmarket**: SOTM level without 3D, turning a dry B2B services list into an illustrated path.
- **the-renaissance-edition**: product chapters as live dioramas, with a real reduced-motion path in CSS and JS (dev 8.05).
- **fluid-glass**: no blocking loader and a nav bar that names the current page. Dev 8.00 and Accessibility 7.6 without 3D.
- **vast**: one `--motion` token switches every CSS duration off under reduced motion; Usability 7.61.

## Evidence

- `data/teardowns/*.json`, `scores` blocks (51 sites). The jury and dev formulas were recomputed on 2026-09-25: 51/51 jury totals match, and 49/49 published dev totals match (2 sites show sub-scores without a total). This is also the source for the tier means, the top-12 set, the 3D vs non-3D split (36 vs 15) and the lowest and highest criterion counts. The `performance_accessibility`, `navigation_interaction`, `motion` and `content_voice` fields give the per-site failures and patterns quoted in sections 2 and 5. `slop_risks` gives the audit flag counts, recounted 2026-09-25 as case-insensitive keyword hits (`reveal|invisible content|opacity 0`, `cream|bone|warm white`, `grain|chromatic aberration`, `violet|purple|lilac|periwinkle|lavender`), so treat them as approximate.
- `data/corpus.jsonl`: 215 SOTDs with award year 2024 or later and published jury scores (195 carry a dev block). Quantiles, the ≥7.7 vs <7.3 tier splits, lowest-criterion counts and correlations were computed 2026-09-25.
- [stats]: `data/stats.md`, recent_2024_plus cut (palette sizes, tags). [fonts]: `data/font_census.json` summary (525 sites with families, 58 on Google Fonts, 37 on Adobe Fonts). [probe]: `data/probe_summary.json` (canvas contexts, 3D asset types, CSS features, type sizes; reduced-motion rules on 11/51 before audit correction).
- [awwwards-editorial §1-4]: pipeline, annual-winner scores, SOTM score anatomy (n=28), SOTD vs HM tags (117 vs 139), tag trends over 1,426 SOTDs, the August 2025 tagging change. [usability-a11y-perf §1.3-1.5, §2, §7]: the dev distribution (n=308), correlations, the 60-site static probe, the gate and the verification protocol. [webgl-3d-stack §6.1]: 3D budgets. [elements-catalog §1]: intro durations. [imagery §3.1]: legibility over images.
- `evidence/digests/signatures.md`: all 51 signatures, read in full for section 3.
- The probe snippet was re-run on 2026-09-25 (after the cursor check was widened to `html`, `body` and `main`) with Playwright and Chromium against `../recipes/demo/index.html`, `about.html` and `webgl.html`, served over a local http server, at 1440, 390 and reduced motion (all clean), and against a broken fixture (every check fired). `fps` reads 120 in headless Chromium, so take U4 frame rates from a real device.
- Gaps:
  - HM jury scores are never published, so SOTD vs HM rests on tags and PRO status.
  - The rubric bands are heuristic, not fitted.
  - Dev scores exist only for Developer Award winners.
  - Tags are chosen by submitters.
  - Juror commentary marked [sec] comes from secondary posts whose juror status is unverified.
