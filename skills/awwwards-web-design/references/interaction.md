# Interaction, navigation and signature UI elements

Last updated: 2026-09-25

Use this when: you are choosing or building the nav, menu, cursor, hovers, CTAs, loader or gate, galleries, product controls, sound, gestures, toys, 404 or footer of an award-level site.

## Rules

1. Commit to one navigation model: a text row on the grid, a corner HUD, a floating island, a vertical chapter rail, or the world itself. A world-as-nav site ships a DOM mirror of every destination, with real links and visible focus (active-theory-v6, shader-development-studio).
2. Grow the menu out of its own trigger (pill, capsule, dock, ticket) rather than dropping an unrelated sheet (pacome-pertant-portfolio, iyo, why-zero, fluid-glass, siena-film-foundation). Open in 0.6-1.2 s, close at about 0.6x that, close on Esc, return focus, lock scroll.
3. The nav must read on every surface. Use one `mix-blend-mode: difference` layer with un-blended "solver" parts (opal-tadpole), or a per-section theme token (lando-norris). Test every section: akaru-2 and leo-parpeix-portfolio-2026 lose their logo on dark floors.
4. Keep the native cursor: only 2/51 winners hide it [probe]. A follower is decoration that names a target with no text, or shows a mode you cannot otherwise see. It runs on fine pointers with full motion only.
5. Hover is a state change that starts within 200 ms (`--dur-2`) and never moves or resizes the box: a tone step, a fill, an icon slide, a media reveal or sibling dimming. No underline animation (grow, wipe or retract), no lift, no scale of the control. Only an image may scale, 1.03-1.05 inside its own clip.
6. One primary action per view, set as a bare word or a bespoke silhouette. Never the filled-plus-outlined pair, a glow or a gradient pill. Every control works; no prop is dressed as a button.
7. No full-screen preloader unless a real asset needs it. Progress counts real promises, the intro totals 1.5 s or less (`--dur-6` is 1.4 s), repeat visits skip it, and the 2 s CSS deadline in the [boot snippet](../recipes/boot.html-snippet.html) releases the page if JS dies.
8. A gate (click, sound, gesture) is passable in one click or keypress, names its control, renders the page behind it and remembers the choice. Probe screenshots of dont-board-me, siena-film-foundation, brunos-portfolio and why-zero never got past theirs.
9. Sound stays off until the visitor asks for it, through a labelled toggle whose glyph moves only while audio plays. An incidental first click never unmutes.
10. Every drag, hold or draw gesture has a single-pointer or keyboard alternative (WCAG 2.5.7), is taught in place, and gates nothing essential.
11. A toy or game sits beside a conventional route (map, list, "I'm stuck"), is reversible, and never holds the only copy of content.
12. Anything that moves on its own for more than 5 s (auto-advancing slider, drifting carousel, ambient loop beside text) gets a pause control (WCAG 2.2.2).
13. The 404 continues the site's world with one joke and one obvious way home, and returns HTTP 404.
14. The footer is a composition: a wordmark flush to the bottom edge with whole caps, a next-project handoff, or a finale. Never the standard footer (big word, rule, four labelled link columns, rule, copyright row) and never the pre-footer CTA banner above it.

## 1. Navigation bars

| Model | Winners | Fits |
|---|---|---|
| Corner HUD, no bar: 3-5 fixed marks | cartier-watches-wonders-2025, era-residence, immersive-garden-website, igloo-inc, lando-norris, pacome-pertant-portfolio, steven-com, hubtown, why-zero, the-power-of-storytelling | single-scene and immersive sites |
| Floating island or capsule | iyo (375x62 glass capsule, 32px from the top), fluid-glass (248x45 frosted bar, bottom-centre), lama-lama-2, vast (appears after 100px), terminal-industries, mindmarket (two separate bars) | commerce, a cart, many links |
| Text row on the grid | aim-ai-modernism-of-kharkiv, bennett-clive, leo-parpeix-portfolio-2026, depo-luxe, gil-huybrecht, oryzo-ai, thelinestudio-com | portfolios, editorial |
| Vertical rail or chapter index | the-renaissance-edition (I-XII left rail, dotted leader on the active chapter), cartier-watches-wonders-2025 (8-dot pagination, each universe a hash deep link via pushState), tracing-art (active dot stretches into a bar), everswap (split-diamond markers), dropbox-brand (60px rail with a vertical chapter name) | long single-page stories |
| The world is the nav | brunos-portfolio (drive; map modal on M), messenger, steven-com (3D dial), san-rita (map legend, then hotspots), active-theory-v6 (Work and Contact are camera destinations) | games, experiences |

Unusual Navigation is tagged on 15/575 recent winners and Menu - Vertical on 3 [stats]. Most winners treat a normal nav; few invent a new one.

Moves worth taking:
- Live label: the fluid-glass bar names the current page, swapping it with yPercent -100, then 100 -> 0 (.6 s power3 in and out), and marquees titles that overflow at 15px/s (fluid-glass).
- Retracting: son-daven hides the header (yPercent -100, 0.8 s) once you scroll down past 1000px, ignores deltas under 40px, and brings it back on any scroll up or within 160px of the bottom (son-daven). vast hides past one viewport (.7 s power3.in) and returns on scroll up (.7 s power3.out) but leaves a ~25px shadow band on screen: hide the shadow with the bar (vast). odd-ritual slides its bar out in 300 ms once the footer reaches 20% of the viewport (odd-ritual). lando-norris scrubs its corner chrome from scale 1.2 to 1 over the first 10vh (lando-norris).
- Spotlight: hovering the oryzo link group fades a 75% brown blocker over the page in .18 s (oryzo-ai).
- Gauge as nav: the why-zero depth ruler magnifies ticks toward the centre like a dock; on hover the tape swaps for five stage buttons (why-zero).

Active state. The law bans the dot under the active item; use weight, tone or a real sliding indicator. oryzo lerps both edges of one dashed indicator toward the active link (1-exp(-dt*10)), so it slides and resizes (oryzo-ai). gq-ap slides a 2px bar in from 5px (.4 s cubic-bezier(.4,0,.3,1)) (gq-ap-the-extraordinary-lab). active-theory-v6 sets white plus a 10px shift. ponpon-mania draws a 1.5px outline pill. floema's small dot under the label is the tell to skip (floema).

On phones keep the same object rather than swapping in a hamburger bar: iyo widens its capsule to the viewport minus 1rem each side, and fluid-glass drops its bar from bottom 4rem to 3rem under 600px.

Build: for recolouring, one `position: fixed; color: #fff; mix-blend-mode: difference` nav, with brand-true parts (a white plate, a yellow hover) kept outside it as solvers (opal-tadpole); blend modes appear on 17/51 [probe]. The alternative is `data-nav-theme` per section, flipped by ScrollTrigger (lando-norris, odd-ritual). Hide and show with transform only.

Guardrails: check logo and link contrast on every floor. akaru's #1A1A1A logo sits at about 1.1:1 on its #0E0E0E sections (akaru-2), and leo-parpeix's name vanishes over dark slides because the token never switches (leo-parpeix-portfolio-2026). A custom scrollbar adds to the native one and never replaces it: oryzo hides the native bar (oryzo-ai); era-residence's rail thumb at least drags. A canvas nav needs a DOM mirror: shader-development-studio draws its focus ring in WebGL from the hidden DOM's focus. Put a skip link first: 59 of 60 winners in the usability probe had none [usability-a11y-perf §1.5, §5]. A glass island needs something to refract: iyo's blur(20px) capsule over #38383899 reads as a flat grey pill on its near-black home field and only works over the pale configurator (iyo slop_risks); fluid-glass sits its frosted bar over footage. Over a flat fill use an opaque tonal plate instead (law: botched glass).

## 2. Menus and overlays

| Site | Form | Open | Close and extras |
|---|---|---|---|
| pacome-pertant-portfolio | "menu •" pill unrolls into a full-height panel | width 0.9 s, height 1 s on a CSS `linear()` spring, radius 24 -> 16 | the trailing dot (scale .125) grows into the 48px close over 0.8 s; page behind #00000080 + blur(1px) |
| iyo | glass capsule morphs into the menu | `grid-template-rows: 0fr -> 1fr`, 0.6 s cubic-bezier(.625,.05,0,1), .125 s delay | the radius waits .45 s on close; Esc and outside click close |
| why-zero | bottom dock track grows into a glass panel | 0.65 s on the same (.625,.05,0,1) curve | burger to X in 0.4 s; links rise yPercent 100, stagger .03 |
| fluid-glass | bottom bar collapses to a 5rem square, panel scales up from its bottom edge | bar .6 s power3.inOut; links yPercent 150 -> 0, .8 s, stagger .02 | links drop on close (power3.out); 40% black page overlay |
| siena-film-foundation | the ticket card expands | grid rows 0fr -> 1fr, .9 s cubic-bezier(.19,1,.22,1) | menu_IN.mp3 plays on open |
| steven-com | right-half panel; the world blurs and greys | x 100% -> 0, 0.85 s power4.out | 0.55 s power3.inOut; MENU rolls letter by letter to CLOSE |
| akaru-2 | full-screen clip-path from the bottom | 1.2 s power4.inOut | close is an apricot circle with × |
| odd-ritual | two stacked 55% panels drop, blue leading, white 0.1 s behind | not timed | Lenis stops, Esc closes; hovered link turns blue, siblings #CCC in 100 ms, thumbnail swaps |
| son-daven | dark modal rises behind a feathered gradient mask | y 200% -> 0, 1.8 s | burger to X .8 s; siblings dim to .2 |
| lando-norris | full-screen overlay | GSAP timeline | close replays it reversed at timeScale 1.5 |

Numbers: open in 0.6-1.2 s (median about 0.85 s across these; son-daven's 1.8 s mask is the outlier), close at 0.55-0.67x of open (steven-com 0.55/0.85, lando-norris timeScale 1.5). The house tokens are `--dur-4` 600 ms and `--ease-move` in [tokens.css](../recipes/tokens.css). Page transitions live in [motion](./motion.md).

Menu content worth taking: items that complete their own sentence on hover (immersive-garden-website inserts grey words around the hovered item); a tilted photo per hovered link (maxima-therapy); outline-to-fill on stacked display words [elements-catalog §2.2 M3]; the current page shrinking to a thumbnail so you see where it went [elements-catalog §2.2 M1]; a transcript that doubles as the menu, where scroll distance equals narration time (gq-ap-the-extraordinary-lab).

Build: `<dialog>` with `showModal()`, or `inert` on the page, or the Popover API. Animate the open state with CSS transitions plus `@starting-style`, so the links rest visible even if a tween never runs [elements-catalog §5]. Stop smooth scroll while open with `lenis.stop()` and resume with `lenis.start()` on close (odd-ritual stops Lenis), and return focus to the trigger. Morph the trigger through `grid-template-rows` or `clip-path`, never by animating `height`.

Guardrails: dont-board-me's menu links start at opacity 0 and are faded in by JS (dont-board-me); if the tween stalls, the open menu is empty. Links are real `<a href>`; primary targets are 44px [usability-a11y-perf §2 E].

## 3. Cursors

About 22/51 add a DOM follower (teardown cursor fields). Others express the pointer inside WebGL instead: fluid trails, lenses, torches. Only 2/51 set `cursor: none` [probe]: why-zero globally, and oryzo-ai only inside its fullscreen video overlay.

A follower earns its place in three cases:
1. It names a target with no text. fluid-glass's blurred 10rem chip says VIEW, Play or SCROLL (fluid-glass). odd-ritual turns the left and right halves of a full-bleed gallery into PREV and NEXT (odd-ritual). siena's thin ring reads SCROLL and becomes prev/next arrows over hitboxes (siena-film-foundation). gil-huybrecht reads the nearest `[data-cursor]` (Focus, Close, Back).
2. It shows a mode you cannot otherwise see. cartier's ring halves on press and draws a 220px progress ring during a long press (cartier-watches-wonders-2025). iyo's 48px ring slides out drag chevrons over the configurator (iyo). immersive-garden's three dots spread with scroll speed and become a dotted scrollbar during a flick (immersive-garden-website).
3. It is the brand's input. lando-norris paints the helmet with a fluid trail. san-rita draws its lens on the terrain, so it foreshortens over ridges. the-power-of-storytelling refracts the page through an SVG `feDisplacementMap` backdrop filter (Chromium only). hubtown's torch lights the map roads.
A chip that repeats the button's own label is noise: drop it [elements-catalog §2.4 H2].

Build: the follower is `aria-hidden`, `pointer-events: none`, fixed at body level outside any transformed container. Follow with `gsap.quickTo` on x and y (0.35 s power3), a lerp of 0.1 per frame (immersive-garden-website, fluid-glass, thelinestudio-com), or frame-rate-independent damping 1-exp(-12*dt) (leo-parpeix-portfolio-2026). Show it on the first move and hide it when the pointer leaves the document (siena-film-foundation). Run it only under `(hover: hover) and (pointer: fine)`, full motion and no `forced-colors`. Code: [motion-stack §4.10], [usability-a11y-perf §3.9], the blend-mode dot [elements-catalog R4]. The label gets its own type role, not the tracked caps every other label wears (law: one label treatment everywhere).

Guardrails: never `cursor: none`; why-zero's sprite cursor adds a frame of lag and dies with the script (why-zero). Custom image cursors (`cursor: url()`, maxima-therapy) override the OS cursor size that low-vision users rely on [usability-a11y-perf §3.9]. Drag zones use native `grab`/`grabbing` (vast, son-daven). The chip scaling in with an elastic ease (leo-parpeix-portfolio-2026, .65 s) is bounce: use expo.out.

## 4. Hover states

200 ms and 300 ms are the most common CSS durations, each on 34/51 [probe]. Hover starts responding within 200 ms; a lagged follower may settle over 0.35-0.5 s [motion-stack §2.3].

| Crafted hover | Winners and numbers | Build |
|---|---|---|
| Tone or weight step | active-theory-v6: weight 700 -> 400 plus white, .4 s. aim-ai-modernism-of-kharkiv: opacity, .2 s. immersive-garden-website: tone only, every action a word. shader-development-studio: over-unity brightness | transition `color` or `font-variation-settings`, 150-250 ms |
| Frosted plate behind the label | gil-huybrecht: ::before inset -.4rem -.8rem, #ffffff26 + blur(16px), in .3 s cubic-bezier(.19,1,.22,1), out .15 s; the active route keeps its plate | the plate is larger than the label; no layout change |
| Fill that passes through | akaru-2: fill scaleY up from the bottom in .5 s (.165,.84,.44,1), leaves through the top in .5 s (.77,0,.175,1). lacoste-polo-factory: the arrow pill scales x10 to flood the card, the label turns after .2 s. siena-film-foundation: rows fill from the bottom in 1.1 s | pseudo-element `scale` with `transform-origin` swapped between in and out, clipped by the button's radius so the caps never change shape (law: botched fill) |
| Icon slide | thelinestudio-com: the arrow leaves right while a clone arrives at the label's left. aim-ai-modernism-of-kharkiv: → exits +150% as a clone enters from -150%, 400 ms. opal-tadpole: the newsletter arrow slides from the right edge to the centre. leo-parpeix-portfolio-2026: ↗ swaps inside a 7px overflow box | two icon copies in an `overflow: clip` slot |
| Media reveal | odd-ritual: the menu thumbnail swaps per link; the footer table's thumbnail clips open (.6 s expo.inOut) and follows the cursor's Y, clamped. mindmarket: a tilted thumbnail anchored to the row, not the cursor. shed: the sticky preview swaps even while the list scrolls under a still cursor. tracing-art: the hovered artwork regains colour and a provenance toast swaps | anchor the preview to the row or a fixed slot; for GL distortion use [webgl-image-hover.js](../recipes/webgl-image-hover.js) |
| Sibling dim | gil-huybrecht: others to .2 in .25 s. iyo: .2, with the hovered image at 1.04. son-daven: .2 over .8 s. fluid-glass: 40% color-mix. pacome-pertant-portfolio: `:has()`, .4 | `.list:has(a:hover) a:not(:hover)` [elements-catalog §2.2 M2]; dimmed text stays at 3:1 |
| The element acts out its subject | dropbox-brand: each tile inverts, then its icon performs its chapter (swatches swap, the easing curve reshapes, the sun sets) | one subject-specific move per tile |
| Label roll or scramble | at least 15/51, e.g. lando-norris, made-with-gsap-1, shed, zentry, oryzo-ai, odd-ritual, champions-for-good, hubtown, era-residence, everswap | roll a `text-shadow` copy instead of a duplicate node (lando-norris, odd-ritual); stagger from the side the pointer entered (oryzo-ai); slow in (.8 s), fast out (.4 s) (shed); reserve the width so nothing reflows (hubtown, pacome-pertant-portfolio); keep a stable accessible name [elements-catalog R8] |

The label roll is the commonest award hover, which makes it close to a default. Pick one hover vocabulary per site and give it a reason.

Never animate underlines. Winners grow them from the centre (cartier-watches-wonders-2025, 45% -> 100%), wipe them (leo-parpeix-portfolio-2026, pacome-pertant-portfolio, era-residence, dont-board-me), grow a gradient bar (the-power-of-storytelling) or retract them (bennett-clive, thelinestudio-com). Keep a static underline on body links and change its colour or thickness in place [usability-a11y-perf §6]. Never the boop: maxima-therapy scales pills to 1.1 with an elastic wobble, champions-for-good grows the plate about 7-10% and squashes it on press, zentry tilts pills back in 3D, lando-norris lifts a fanned card 2.5rem at scale 1.08. Press feedback is a darker tonal step [motion-stack §7]. A card hover is an image scale of 1.03-1.05 inside its clip, or the 2D accordion [elements-catalog §2.4 H6, R5].

Guardrails: gate hovers with `(hover: hover) and (pointer: fine)` (champions-for-good, pacome-pertant-portfolio) and show hover-revealed content at rest on touch [usability-a11y-perf §4].

## 5. Buttons and CTAs

- Bare word: immersive-garden-website has no boxed button anywhere. aim-ai-modernism-of-kharkiv sets a label on a 1px rule with → or ↗. odd-ritual wraps CTAs in thin brackets. thelinestudio-com sets type and an arrow on a full-width rule with a bracketed count ("The Work [85]"). When you copy the rule, make it the control's own edge and hit area, not an ornament beside the label, and round its caps (`border-radius: 1px` on a 2px bar, or `stroke-linecap: round`); keep the drawn ↗, never the stock → (law: unrounded hairline rules; the arrow is a tell).
- Bespoke silhouette tied to the brand: siena-film-foundation's ENTER is a cinema ticket (label cell, dashed perforation, arrow stub), and its nav ticket is cut by an SVG clipPath. hubtown bevels one or two corners by 15-30px. floema fuses a label pill to a blank tile with a live SVG metaball bridge and no blur filter. lacoste-polo-factory floods a card from its arrow pill. dont-board-me hangs BOOK NOW as a tab from the top edge. fluid-glass uses square-cornered blocks with a "↳" hook glyph.
- Glass, only over imagery worth refracting: why-zero stacks seven layers with em-based inset highlights, but ships the blur only as `-webkit-backdrop-filter`, so Chromium shows no blur on the pills: ship both properties (why-zero). the-power-of-storytelling mirrors its rim highlight to the opposite side on hover. Keep the gloss and drop the halo (law: liquid-glass recipe).
- Hit area larger than the ink: cartier sets `::after { inset: -10px }` (cartier-watches-wonders-2025). leo-parpeix pads 15px and cancels it with a -15px margin, so the target grows without moving layout (leo-parpeix-portfolio-2026). why-zero's hold disc has a hit area 30px larger all round.
- Magnetic: era-residence and son-daven move the whole button (strength 25, power4.out 1.6 s, elastic release). The crafted version keeps the box still and lets only the label drift 6px at most: [magnetic.js](../recipes/magnetic.js).
- The arrow is a tell: draw one diagonal ↗ or hook and reuse it across nav, CTA and footer (law).

Guardrails: one primary per view. iyo pairs an outlined LEARN MORE with a filled SHOP NOW, and hubtown splits a pair only by value; both are the law's stock pair (iyo, hubtown). A saturated brand fill (lando-norris #d2ff00, maxima-therapy #FD4401) is the law's saturated-accent tell by default. The one defensible case is when the colour is the product: lando's lime is the helmet livery ([casebook](./casebook.md)), and even there it fills one control (STORE), not the eyebrows, dots and headline words too. Otherwise use a tonal step off ink or surface. No dead controls: everswap's Launch App has no href and `cursor: default`; made-with-gsap-1's ON SCREEN chip is a 182x50 button-shaped pill that is a plain status div: link it to the effect it names, or drop the button shape. No timed pop-ups: odd-ritual opens a signup modal 10 s after the first load.

## 6. Preloaders and intro gates

About 44/51 ship some loader or intro cover (teardown preloader fields). Seven showed none in the captures: champions-for-good, dropbox-brand, iyo, made-with-gsap-1 and fluid-glass ship none, while floema and depo-luxe carry preloader markup that never appeared. First-visit time to a usable page, where measured: mindmarket ~1.25 s, akaru-2 ~2.1 s, opal-tadpole ~2.9 s, maxima-therapy and thelinestudio-com ~3.3 s, aim-ai-modernism-of-kharkiv 3.9 s (Lottie), shed ~4.4 s, lama-lama-2 ~4.5 s, igloo-inc ~6 s of near-blank grey before its intro, son-daven ~7.5 s, era-residence ~10.2 s. The best Elements intros finish in about 1.9 s and 3.5 s is the upper limit [elements-catalog §1]. The house cap is 1.5 s [usability-a11y-perf §3.6].

Loader forms worth taking:
- The loader becomes the hero. thelinestudio-com's progress bar thickens into its wordmark's crossbar, and the loader logo is moved into the hero. son-daven hands its wordmark to the hero with GSAP Flip (1.8 s). bennett-clive scales the big wordmark into the header slots.
- The mark is the progress bar. steven-com draws a red marker stroke with dashoffset = L*(1-p), with p damped toward real WebGL progress. the-renaissance-edition draws its line drawing to 80% while assets stream and completes it on ready. hubtown assembles its square-glyph wordmark from 13 squares.
- A portal onto the live scene. everswap punches a diamond into a 2D canvas that grows with real load, so the running scene shows through (everswap). brunos-portfolio fills a ring inside the world, which then collapses into the reveal.
- Themed status copy instead of a percentage [elements-catalog §2.1 P6].

Honest progress counts real promises: everswap reports real asset progress with a 1 s minimum; shader-development-studio weights 0.8 content + 0.2 video; cartier-watches-wonders-2025 waits for shader precompile. A 0 -> 100 tween on a timer is fake (dont-board-me's phone counter runs 0 -> 100 over 3 s, ease none; era-residence runs its bar for a fixed 4 s on a stuttering CustomEase with plateaus, then locks scroll for about 10.2 s in total). Every loader also needs a timeout exit: the-power-of-storytelling lifts its panel only on `setSceneLoaded`, so if WebGL never loads the page stays on the panel (the-power-of-storytelling). Recipes: [motion-stack §4.12], the progressive curtain [elements-catalog R1].

Repeat visits: era-residence (short version with no text or bar), son-daven (skips the sheep film) and odd-ritual (first visit per session only) key off `sessionStorage`. mindmarket skips its loader entirely on touch and small screens.

| Gate | What the visitor does | Way through | Observed cost |
|---|---|---|---|
| dont-board-me | bounce a ball; a hole punches open from the click point (r 0 -> 1800, 1.3 s) and the page intro starts 400 ms into it | one click; phones get an automatic 3 s counter | 16 desktop probe screenshots never passed it; the only focusable element is an unlabelled button |
| pacome-pertant-portfolio | choose "enter with sound" or "enter without sound" after a 2.68 s Lottie | either; without-sound stores the choice and starts the bed muted | the buttons appear only once assets load |
| siena-film-foundation | watch the logo film, press an ENTER ticket that also unlocks audio | one click; tutorial hints, then a 48 h cookie hides them | 8 probe frames identical: logo and ENTER only |
| gq-ap-the-extraordinary-lab | click anywhere (headphones glyph) | one click; Skip Intro appears later | the only control is a 10px label that dims to ~3.7:1 |
| brunos-portfolio | click the sphere | click, Enter, W, D, arrows or gamepad; the label redraws for the active input device; a `#skip` hash skips the gate | 7 identical probe frames; no DOM text on the first screen |
| why-zero | draw a zero; a demo comet loops the path | the gesture only | all 8 probe wheel steps returned the gate |

slosh-seltzer (age gate) and messenger (a WebGL BEGIN block with no focusable element) complete the 8 gated teardowns. The jury does not punish gates: those 8 average usability 7.47 and creativity 8.21, against 7.38 and 7.94 for the other 43 (teardown scores). The cost falls on crawlers, link previews, keyboard users and anyone impatient.

The crafted gate: server HTML renders the page behind it (siena should at least show its first film frame); the control is a labelled `<button>` reachable by keyboard; sound gets two explicit choices (pacome-pertant-portfolio); any input device works (brunos-portfolio); shared links can skip it (brunos-portfolio `#skip`); the choice persists; phones and reduced motion pass straight through (dont-board-me on phones). The gate can itself be the signature, as dont-board-me's hole-punch reveal is.

Build: the [boot snippet](../recipes/boot.html-snippet.html) sets `data-motion` and arms the intro under a 2 s CSS deadline; [motion-core.js](../recipes/motion-core.js) has `introFailsafe` (3500 ms) and `introMaxStart` (800 ms), so a late module shows the intro at rest.

## 7. Galleries, sliders and indexes

- Index as navigation: gil-huybrecht's grid/gallery switch flips WebGL planes to their new rects, and hovering a project dims the rest to .2 and fades the header (gil-huybrecht). shed lights the row under the pointer and swaps a sticky preview, with a floating FEATURED | INDEX switch (shed). thelinestudio-com swaps a giant filter word with a bracketed count ("All [67]" -> "Branded. [51]") next to GRID / LIST pills. akaru-2 sets filter counts as superscripts.
- Speed-aware lists: a fast flick turns immersive-garden's project cards into a thumbnail index and fades the chrome (.5 s); slowing down lands on a full card (immersive-garden-website). depo-luxe moves a focus lens through 80+ archive rows, splits the focused row to the viewport edges while its film plays behind, and starts thumbnail video only once scrolling slows (depo-luxe).
- Strips: siena-film-foundation's film strip is hold-and-drag (sensitivity .005), with top and bottom hitboxes as prev and next. odd-ritual's carousel drifts ~50px/s on the GSAP ticker, drags through Observer and follows with quickTo x (.5 s). made-with-gsap-1 collapses its hero into a scrubbable filmstrip of every effect while pressed and snaps to the nearest one on release.
- Selectors: zentry's product overlay is scroll-to-select: index = floor(progress x n), 12rem names, 5 cards on a ring damped toward 2π·i/5, a UI tick per step (zentry). ponpon-mania is a coverflow of record sleeves with padlocks on locked chapters. aim-ai-modernism-of-kharkiv's gallery overlay counts "n of 18".
- From the Elements sample: a scroll fisheye column, an infinite drag canvas (inertia about 1.3 s, velocity decay .92 per frame) and an editor-timeline ruler with a playhead [elements-catalog §2.5 G1-G2, §2.3 T6].

Build: a DOM list first, with WebGL planes over it. Anchor previews to the row (mindmarket) or tilt them by pointer x within ±10° (thelinestudio-com). A list view doubles as the reduced-motion fallback (pacome-pertant-portfolio's "spiral • list" switch).

Guardrails: buttons and arrow keys for every strip (WCAG 2.5.7). A pause for anything that advances by itself past 5 s: made-with-gsap-1 advances every 2.5 s, odd-ritual drifts constantly, maxima-therapy's wheel auto-advances after 10 s idle. An infinite loop still needs reachable legal links (depo-luxe puts them in its Contact view).

## 8. Product interactions

- Colourway toggles: opal-tadpole re-themes the whole page. The render fades out (.48 s), sections flip between #fff and #0a0a0a, and the render returns in the same pose. Its swatches are bare 40px circles with an inset 2px ring on hover, focus and active, and sr-only names. iyo spreads a new finish across the product face as a ripple (1.2 s power2.out). the-watch rings its 4 colourways around the watch (1 s material transition), and its hands show the visitor's real local time. era-residence crossfades identical-camera day and dusk renders from a labelled BY DAY / BY NIGHT text toggle, with the inactive label at 40% white.
- Explode and annotate: iyo grows the hovered part to 1.085-1.3 and turns it to a showcase angle while the others shrink to .8 (2.5 s expo.out), with a glass spec card at the pointer. vast opens 30px hotspot squares into labels with clip-path and offers interior/exterior and 360 views. floema pairs a draggable PBR model with orthographic dimension drawings and runs a scroll-ring material configurator.
- Compare: opal-tadpole pins a drag-handle video comparison against a menu of six rival cameras.
- Commerce inside the story: the-renaissance-edition sells a real beanie in its checkout chapter, with a Roman-numeral quantity stepper. made-with-gsap-1 turns Quarterly/Annual prices on a 3D drum (code). terminal-industries' ROI calculator rolls its result on an odometer.

Build: swap the finish while the surface is invisible, behind a fade or at the edge-on angle [elements-catalog R9]. Keep one camera for every finish. Use `grab`/`grabbing` over anything rotatable. For a 3D hero over a poster, use [three-hero.js](../recipes/three-hero.js).

Guardrails: swatches are `<button aria-pressed>` with names; price and spec text update in the DOM; drag-rotate also has buttons. A theme switch is never the sun-and-moon pill (law); era-residence's labelled text toggle is the model.

## 9. Sound and mute controls

21/51 teardowns ship audio, 8 of them through Howler.js (brunos-portfolio, depo-luxe, immersive-garden-website, leo-parpeix-portfolio-2026, pacome-pertant-portfolio, siena-film-foundation, why-zero, zentry). Sound-Audio is tagged on 13/575 recent winners [stats].

Default state, three camps:
- Off until asked: active-theory-v6, champions-for-good, igloo-inc, immersive-garden-website ("Click to enable sound"), son-daven, hubtown.
- A choice at a gate: pacome-pertant-portfolio, siena-film-foundation, gq-ap-the-extraordinary-lab, brunos-portfolio.
- The first click anywhere unlocks and unmutes: cartier-watches-wonders-2025, david-whyte-experience, leo-parpeix-portfolio-2026, why-zero, the-power-of-storytelling. Avoid this: a click meant for a link starts audio.

Levels seen: an ambient bed at .25-.55 with 0.5-1.5 s fades (son-daven .25 over .8 s; the-power-of-storytelling .4; hubtown .5 over .5 s; why-zero .55 with a 1.5 s fade in). UI one-shots at .1-.5 (hubtown .15; depo-luxe .4 on each project change; siena-film-foundation .5 on hover). Rate-limit hovers: champions-for-good plays at most once per 40 ms, the-power-of-storytelling caps each clip at 5 plays per second. Vary repeats: messenger detunes and shifts playbackRate; why-zero's hold sound speeds up as you hold; champions-for-good fades footsteps up as the pointer nears the logo.

Mixing: duck under video and modals. pacome-pertant-portfolio ducks to 0 over 500 ms under its showreel. hubtown ducks the bed to .15 and sweeps a low-pass from 20 kHz to 200 Hz on modals and route changes. active-theory-v6 muffles the world while a project is open. Pause on a hidden tab (cartier-watches-wonders-2025, david-whyte-experience, the-power-of-storytelling). Use per-state stems rather than per-page loops (cartier-watches-wonders-2025: intro, low, full, transition, discover, single).

Toggle glyphs that show state: active-theory's nav divider becomes a waveform (500 ms) and is exposed as "Toggle Audio" (active-theory-v6). leo-parpeix's four bars shrink to dots when muted (leo-parpeix-portfolio-2026). the-power-of-storytelling's five bars pulse only while on. immersive-garden's ring turns once every 35 s while playing (immersive-garden-website). david-whyte-experience shows a flat line or a sine wave. cartier strikes through SON when muted (cartier-watches-wonders-2025). why-zero flattens its wave when muted or under reduced motion.

Build: create the AudioContext inside the click handler; the toggle is a `<button aria-pressed>` with a text label; persist the choice (gil-huybrecht uses localStorage; champions-for-good does not persist it). Load nothing until opt-in (son-daven sets preload none; champions-for-good preloads all 15 files while off). Compress to ogg or m4a (hubtown declares 38.4 MB of .wav). On phones, champions-for-good forces sound off under 992px, siena-film-foundation plays nothing, and messenger swaps in a lighter music file on low-memory devices.

Guardrails: audio that starts by itself for more than 3 s needs a stop control (WCAG 1.4.2). A story told by voice needs DOM captions (gq-ap-the-extraordinary-lab's subtitles and transcript menu). A keyboard shortcut is a bonus (brunos-portfolio mutes on L).

## 10. Gestures and drag

- Hold: cartier fills a progress ring during press-and-hold, and turns one hold into a release-timing game with a 0.9-1 win window (cartier-watches-wonders-2025). immersive-garden-website opens projects with click-and-hold. the-watch waits 500 ms before a 2 s hold ramp. why-zero asks for a 3 s hold, then 1.5 s.
- Drag along a path: son-daven's season knob slides on a dotted SVG arc (nearest of 101 `getPointAtLength` samples) and snaps on release in 0.8 s; clicking either end node works too (son-daven). maxima-therapy maps a drag to ±5° of wheel rotation and advances past 2.5°.
- Drag to explore: made-with-gsap-1 (press anywhere for the filmstrip), lacoste-polo-factory (spin the machine and the polos swing out), opal-tadpole (comparison handle), everswap (drag-to-scroll with momentum on desktop), era-residence (draggable scroll thumb with a 3.2 s glide).
- Draw or swipe: why-zero's DRAW A ZERO, with a demo comet looping the path (2 s sweep, 2 s rest). messenger's title tiles flip in the swipe's direction. champions-for-good's phone photo stack flicks with elastic.out(1,1), 0.6 s.
- Touch conflict: lando-norris adds a TAP TO LOCK switch so a drag paints the helmet instead of scrolling.

Build: teach in place with a looped demo (why-zero), a cursor cue (iyo's chevrons) or a verb label ("DRAG" in leo-parpeix-portfolio-2026). A hold shows progress from its first frame (cartier-watches-wonders-2025) and ignores the first ~500 ms (the-watch). Snap on release.

Guardrails: a single-pointer alternative for every drag (WCAG 2.5.7), such as son-daven's end nodes or odd-ritual's prev/next halves. Holds of 3 s or less. A gesture never gates essential content; why-zero fails this. Never take over touch scrolling without an explicit switch (lando-norris).

## 11. Games and toys as navigation

Games & Entertainment is tagged on 16/575 recent winners and Gestures / Interaction on 22 [stats].

- The site is the game: brunos-portfolio (drive to each project; a map modal on M; a fixed "I'm stuck" respawn; achievements; a daily race with a leaderboard; controls tabs for mouse and keyboard, touch and gamepad). messenger (a walkable planet with NPCs; Esc closes panels). why-zero (XP = 100 x stages entered for the first time, on an odometer with a sound; the depth gauge jumps between stages; the stage-5 map takes a joystick, arrow keys, drag and pinch).
- A toy inside a normal site: leo-parpeix-portfolio-2026 (carry a fruit to feed the bee, with gravity, squash, sound and a real shadow). champions-for-good (a click stamps a sticker that flips out after 3 s). shader-development-studio (push the shredded newspaper). oryzo-ai (type into a field and flip the coaster to "encrypt" it; a hidden tardigrade on shake). the-renaissance-edition (a real popup window acts as an X-ray lens, synced over BroadcastChannel). the-power-of-storytelling ("Reimagine Phoenix" re-rolls the glass shader on springs). pacome-pertant-portfolio (the logo cycles four faces, each with its own sound).
- From the Elements sample: the breakable footer wordmark with a Repair action [elements-catalog §2.6 F1, R10].

Build and guardrails: the toy is reversible (repair, respawn, reset; the matter.js breakable wordmark with Repair is [elements-catalog R10]); a conventional route sits next to it (brunos-portfolio's map and "I'm stuck"; hubtown's OPEN PROJECT LIST beside its map); everything drawn in canvas has a DOM mirror (active-theory-v6's clipped mirror links; shader-development-studio's hidden DOM with WebGL focus rings); controls are listed per input device. brunos-portfolio has no DOM text on its first screen and scores 6.6 on accessibility; messenger's BEGIN is a WebGL mesh with no focusable element.

## 12. 404 pages

404 pages is tagged on 16/575 recent winners, and 404_page is an Elements section on 39 [stats].

- shader-development-studio: the 404 is a bank-vault set with a "line busy" gag.
- dont-board-me: a punchline pile. The jury video shows shapes raining and piling up behind the headline in a ~7 s loop; the live page is 7 static rotated SVGs.
- iyo: kinetic radial SVG lines, six groups rotating at speeds from 0.49 down to 0.098 in alternating directions (bundle).
- son-daven: an idle scene breathing on a 4 s loop.
- Listed as Awwwards elements, not observed: the-power-of-storytelling (ice shader), maxima-therapy (interactive), the-renaissance-edition (art piece).

Build: reuse one asset from the site's world at a fraction of the home page's weight. One joke. The way home is the primary control, with the index or search next to it. Real HTTP 404. Loop under 5 s or add a pause; static under reduced motion.

Guardrails: the headline and the way home are DOM text, visible at first paint; the scene is decoration behind them, never a gate. A lost visitor who then waits on a scene is lost twice.

## 13. Footers

Footer Design is tagged on 21/575 recent winners, and footer and loading are each Elements sections on 75 [stats].

- Wordmark flush to the bottom: bennett-clive runs its wordmark 100vw, flush to the bottom edge. akaru-2 runs a 1380px SVG wordmark between 30px margins, bleeding off the bottom after a stretched-flight entrance (1.5 s, stagger .05). thelinestudio-com sets its wordmark on a sheet above a sticky red floor and scrubs it to -6° by the end of the page.
- Wordmark as a lens: fluid-glass masks a second copy of the footer footage with its letterforms and scales it 1 -> 1.1 as the footer scrolls in, so the letters read as thick glass, whole and uncropped (fluid-glass).
- Letters as controls: shed's SEE WORK line advances an inline thumbnail to the next case study for each hovered letter (shed). A colour wake in the product's own colourways [elements-catalog §2.6 F2].
- The next project as the footer: pacome-pertant-portfolio ends each case in a sticky "next up" zone where wheeling fills a 6px rail and auto-loads the next project; release for 150 ms and it drains. san-rita's next-trail window scales into the next hero. fluid-glass opens its menu over the footer at the end of the page and turns the bar into back-to-top.
- Finale scene: igloo-inc re-forms 150k particles into a 3D volume per social link. artefakt re-forms the hero's ASCII logo, so the page loops. active-theory-v6 reuses its ring upside down.
- Island: maxima-therapy floats a white island 48px inset, with characters sitting on the wordmark. made-with-gsap-1 raises a white rounded sheet over the black showcase.
- Live details: bennett-clive's city clocks blink their colon (1 s step-start). thelinestudio-com shows real studio open or closed status, and its SITE CREDITS button tilts the red floor away to reveal a credits sheet that any scroll closes.

Build: set the wordmark as an inline SVG whose viewBox is trimmed to the cap height and baseline, sized to the grid's content width (akaru-2: 1380px between 30px margins), as the footer's last child with no bottom padding. To bleed it, translate it down a few percent inside `overflow: clip` so only the bottom edge crops, never the cap tops. A scrub on it (thelinestudio-com's -6°) runs on an element that is already fully visible. A next-project handoff is a sticky 100vh zone: at the page bottom add each positive wheel `deltaY` to an accumulator capped at 1000, fill a 6px rail with `scaleY(acc/1000)` (lerp .1 filling, .05 draining), reset after 150 ms without wheel input, and navigate 300 ms after it reaches 1 (pacome-pertant-portfolio). Make the next project's title a real `<a>` as well: pacome hides the rail at 900px and below, and keyboard and touch users never wheel.

Guardrails (law): the wordmark is centred or on the grid, with whole caps, flush to the bottom with no gap beneath, above any texture, and bleeds only off the bottom edge. No standard four-column footer with a big word and a copyright row; gil-huybrecht's five link groups placed on its 14-column grid are the quiet alternative. Copy bennett-clive and akaru-2 for the wordmark only: both sit it under a four-column info row (akaru's is a 10px-caps colophon with a copyright), which is most of the standard footer, and bennett's footer links retract a 2px underline on hover (bennett-clive slop_risks). What saves bennett's row is live content, the city clocks; give any column row a job like that or cut it. No pre-footer CTA banner (a wide rounded slab with a headline and two buttons) between the last section and the footer; the last section's own single action is enough. No email pill plus pill button for the newsletter (made-with-gsap-1's footer ends on exactly that). Footer items are visible without a scrub: the-power-of-storytelling's footer items sit at opacity 0 until its scrub runs. Footerless sites keep legal links reachable (steven-com and lacoste-polo-factory put them in the menu; ponpon-mania pins 9px legal text bottom-right).

## Crafted vs slop

| Award habit | Slop version | Crafted version |
|---|---|---|
| Hamburger to full-screen overlay | a black sheet with centred links fading up from 0 | the trigger grows into the panel (pacome-pertant-portfolio, iyo); links rest visible; Esc closes |
| Active nav marker | a dot under the current link (floema) | a weight or tone step, or one indicator that slides and resizes (oryzo-ai) |
| Nav over mixed sections | a fixed colour that vanishes on dark floors (akaru-2) | a difference layer with solver parts (opal-tadpole), or section theme tokens |
| Custom cursor | `cursor: none` plus a laggy blob | the native pointer plus a chip that names a target with no text (fluid-glass) |
| Link hover | an underline that grows, wipes or retracts (cartier-watches-wonders-2025, bennett-clive) | a tone or weight step; a static underline in body copy |
| Button hover | a lift or elastic scale (maxima-therapy) | a fill or tone change, an icon sliding inside the box, the label drifting 6px at most ([magnetic.js](../recipes/magnetic.js)) |
| Card hover | a lift and a shadow bloom (lando-norris card fan) | an image scale inside the clip, the 2D accordion, sibling dimming (gil-huybrecht) |
| CTA pair | filled plus outlined buttons (iyo) | one action, as a bare word or a brand silhouette (siena-film-foundation ticket) |
| Accent CTA | a poster-bright fill with no reason | a tonal step off ink or surface; saturated only when it is the product's colour (lando-norris livery) |
| Preloader | a 0-100 timer counter over a blank screen | honest progress, a loader that becomes the hero (thelinestudio-com), 1.5 s at most with a 2 s CSS deadline, skipped on repeat visits |
| Click-to-enter | an unlabelled button with nothing behind it | a labelled choice, the page rendered behind, a skip parameter, automatic pass on phones |
| Sound | the first click anywhere unmutes | an explicit opt-in toggle with a state glyph, ducking and a pause on hidden tabs |
| Footer wordmark | a big word with shaved cap tops, floating above a gap | whole caps flush to the bottom edge, on the grid, above the texture (bennett-clive) |
| Footer body | four labelled link columns, rules, copyright row, often a CTA banner above | links placed on the page grid in the body type (gil-huybrecht), live details (bennett-clive clocks), or a next-project handoff (pacome-pertant-portfolio) |
| Glass nav | blur over a flat dark field, reading as a grey pill (iyo home) | frosted only over footage or imagery (fluid-glass), otherwise an opaque tonal plate |
| Toy | physics that leaves the brand broken | a reversible toy with Repair, plus a conventional route beside it |

## Exemplars

- pacome-pertant-portfolio: the menu pill that unrolls into the panel, the two-choice sound gate, per-cue volumes.
- iyo: the capsule nav growing into the menu through grid rows (the cart state is inferred); the ripple colourway swap; part annotation. Not its glass over the dark home field.
- fluid-glass: the bottom frosted nav with a live page label, the context cursor chip, the refracting footer wordmark.
- opal-tadpole: the difference-blended nav with solver elements; the colourway toggle that re-themes the page.
- immersive-garden-website: every action a word; the speed-aware index; the word cursor; the sentence-completing menu.
- gil-huybrecht: the index as nav, sibling isolation, the frosted hover plate, cursor verbs from data attributes.
- odd-ritual: the stacked-panel menu with sibling dimming, bracket CTAs, gallery halves as prev and next.
- thelinestudio-com: the loader that becomes the wordmark, the relocating arrow, the sticky footer floor with its credits reveal.
- hubtown: Web Audio mixing (ducking, a low-pass on modals), bevelled buttons, the map torch with a list fallback.
- brunos-portfolio: a game as navigation with a map, a respawn, per-device control labels and a skip hash.
- lando-norris: theme-flipping corner chrome, the text-shadow label roll, the cursor-painted hero, the touch scroll lock.
- siena-film-foundation: the ticket-shaped nav and CTA, the strip with hitbox prev/next, and what a hard gate costs.

## Evidence

- Teardowns: `data/teardowns/<slug>.json` for all 51 slugs cited, fields `navigation_interaction.*`, `motion.preloader`, `motion.intro_sequence`, `motion.hover_micro`, `motion.cursor`, `steal_this`, `slop_risks`, `performance_accessibility` and `scores`. Cross-site digest: `evidence/digests/interaction.md`.
- [probe] `data/probe_summary.json`: cursor_none 2/51, mix_blend_mode 17/51, clip_path 29/51, `:has()` 17/51, reduced-motion rules 11/51, CSS durations 200 ms and 300 ms each on 34/51.
- [stats] `data/stats.md`, recent_2024_plus cut (575 sites): tags Unusual Navigation 15, Menu - Vertical 3, Gestures / Interaction 22, Games & Entertainment 16, Sound-Audio 13, Footer Design 21, 404 pages 16; Elements sections footer 75, loading 75, 404_page 39, menu 51.
- Research: [elements-catalog](../data/research/elements-catalog.md) §1, §2.1-§2.6, §4, §5, R1, R4, R5, R8, R9, R10; [motion-stack](../data/research/motion-stack.md) §2.3, §4.9, §4.10, §4.12, §7; [usability-a11y-perf](../data/research/usability-a11y-perf.md) §2, §3.6, §3.9, §4, §5, §6.
- Recipes: [magnetic.js](../recipes/magnetic.js), [boot.html-snippet.html](../recipes/boot.html-snippet.html), [motion-core.js](../recipes/motion-core.js) (intro failsafe, motion toggle, marquee pause), [tokens.css](../recipes/tokens.css), [page-transitions.js](../recipes/page-transitions.js), [webgl-image-hover.js](../recipes/webgl-image-hover.js), [three-hero.js](../recipes/three-hero.js).
- Computed for this file: gated versus other score means (8 against 43) from teardown `scores`; the audio count (21/51), DOM-follower count (about 22/51), loader count (about 44/51) and label-roll count (at least 15/51) from teardown fields; the menu timing median from the table in §2.
- Audit 2026-09-25: 50+ claims re-checked against teardown fields, probe_summary.json, stats.md (recent_2024_plus), the research files and the recipes (tokens `--dur-2`/`--dur-4`/`--dur-6`, `introFailsafe` 3500, `introMaxStart` 800, the 2 s `--intro-deadline`, magnetic `max` 6). All 51 slugs resolve to teardowns and every relative link resolves.
- Inferred or unobserved, kept marked: iyo's menu-to-cart morph (Awwwards element title; the CSS mechanics are verified); the 404s of the-power-of-storytelling, maxima-therapy and the-renaissance-edition (element titles only); made-with-gsap-1's price drum (code only); some label rolls (lama-lama-2, fluid-glass buttons) inferred from doubled label text in the probe.
