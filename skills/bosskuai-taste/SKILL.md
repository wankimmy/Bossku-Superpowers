---
name: bosskuai-taste
description: "Use when building, designing or redesigning any website, landing page, portfolio, homepage or marketing UI: the Awwwards house rule (concept, signature moment, one direction, motion ladder, quality gates, jury score) that keeps it from looking AI-generated."
---

# BosskuAI Taste - the Awwwards house rule

**Awwwards Site of the Day quality is the default style for every web design.** It applies unless the user or the
project's `DESIGN.md` names another style. Scope:
- Websites, landing pages, portfolios, launch, brand and campaign sites, and redesigns get the full rule.
- Dashboards, app screens and product UI get the craft bar in §8 and keep native scroll.

The default look an LLM reaches for is the Tell. The award bar is the way past it: one owned idea, rendered live,
on a tight system, with usability that holds up.

This file is the law and the loop. The depth lives in the vendored packs. Open their files by the path their
`SKILL.md` sits at, or with `bossku skills show <id>`:

| Need | Open |
|---|---|
| Ten directions, signature, measured numbers, crafted-vs-slop crosswalk | `awwwards-web-design`: `references/directions.md`, `typography.md`, `color.md`, `layout.md`, `motion.md`, `interaction.md`, `imagery.md`, `webgl-3d.md`, `content-voice.md`, `quality-gates.md`, `casebook.md` (51 winners) |
| Framework-free tested code: tokens, motion core, page transitions, magnetic hover, WebGL image hover, three.js hero | `awwwards-web-design`: `recipes/` |
| Concepts, the build engine (one GSAP clock, Lenis, OGL), Next.js and Astro adapters, font, photo and OG scripts, ship checklist | `awwwards`: `references/concepts.md`, `art-direction.md`, `engine.md`, `nextjs.md`, `astro.md`, `webgl.md`, `ship.md`; `scripts/` |
| Score a build or a live site like the jury | `jury` |
| One technique (masked reveal, scroll-scrubbed sequence, marquee, progressive blur, shader cursor, globe, mood systems) | the `mengto` library skills: `bossku skills find "<technique>"` |

Load only one full build loop (`awwwards` or `awwwards-web-design`), never both.

## 1. Read the room

- **Design Read.** Write one line before anything else: who it is for, the mood, and the closest real reference.
  Example: *"Independent architecture studio - quiet, material, exact; closest to an editorial catalogue."*
- **Brief from real specifics.** List what the brand really has: an object, a place, footage, a body of work,
  names, numbers, dates. No lorem. A missing fact becomes a labelled placeholder (`[REAL DATA]`), never an invention.
- **One question at most** if the brief is ambiguous. Otherwise decide and say what you assumed.

## 2. Concept and signature (the step that decides the score)

- Write three concepts from different territories: the name, the profession's material, the place or culture, a
  metaphor for how they work, a formal or type system (`awwwards` `references/concepts.md`).
  - Score each 1 to 5 on originality, fit, feasibility and portability. Lower portability is better: it means
    the idea cannot be moved to another brand.
  - Pick one and say why in a line.
- **Concept Card** in `DESIGN.md`: Idea, Metaphor, Signature, Emotion, Motion verb, Screenshot.
- **Signature.** One sentence: the brand's own object, material or process, which the visitor plays.
  - It must survive with motion off.
  - It recurs at 3 or more touchpoints: loader, nav, transition, footer.
  - One signature moment, executed perfectly. Everything around it stays quiet.

## 3. Direction (one primary, at most one secondary layer)

Pick from the ten directions in `awwwards-web-design` `references/directions.md`: Flown world, Playable toy, Object
hero, Reel as interface, Editorial catalogue, Kinetic poster, Illustrated story, Material calm, Process filter,
Archive index.

- Task-first pages (checkout, catalogue, lead form) keep native scroll and DOM content. Use object, calm,
  editorial or index there.
- With no 3D budget (under about 1.5 MB compressed on mobile before first interaction), step down to a 2D direction.
- Write the decision as one line before designing:
  `<Direction> (+ <secondary>) for <brand>: <signature>. Ground <hex>, ink <hex>, accent <hex or none>. Display <face> at <px>. Clock <ease family>, ladder <ms>.`
- Another vocabulary is fine *inside* the direction when the user asks for it: a `hallmark` theme, a `taste-skill`
  aesthetic (`soft-skill`, `minimalist-skill`, `brutalist-skill`), or a real design system (Material 3, Fluent,
  Carbon, HIG, shadcn/ui). Use one system per project and install its official package. Never mix two.

**Dials** (they gate layout, motion and density). The Awwwards baseline is `9 / 8 / 3`. Override it from the read,
never by asking the user to edit a file.
- `DESIGN_VARIANCE` runs from 1 (symmetry) to 10 (art-directed asymmetry).
- `MOTION_INTENSITY` runs from 1 (static) to 10 (cinematic).
- `VISUAL_DENSITY` runs from 1 (airy) to 10 (packed).

| Read | Dials |
|---|---|
| Material calm or editorial | `6 / 4 / 2` |
| Premium consumer | `8 / 7 / 3` |
| Flown world or playable toy | `10 / 10 / 3` |
| Trust-first or regulated | `5 / 3 / 4`, still with a signature and the full craft bar |
| Redesign, preserve | Match the existing site |
| Redesign, overhaul | +2 / +2 / match |

## 4. System

- **Type.**
  - One distinctive display face plus a truly neutral body face, at most 2 families. Only fonts you can load:
    Fontshare, Google Fonts, Fontsource, or the brand's licensed files. Self-host them with `awwwards`
    `scripts/font.mjs`.
  - Not as the brand face: Inter, Space Grotesk, Syne, Fraunces, Instrument Serif.
  - Display type is measured, with negative tracking set per size. Winners have a median of 80px at 1440 and
    about 47px at 390 (`awwwards-web-design` numbers card).
  - Body text is 16 to 18px with 1.45 to 1.6 leading.
  - Italic words with descenders get extra leading.
- **Colour.**
  - One ground, one ink, and at most one owned hue: either 5% of the area or less, or a whole field or the
    object's own material. Everything else is a tonal step.
  - No pure `#000`. No AI-purple gradients. No neon chips. No cream plus terracotta serif. No acid green on black.
  - If a background changes by chapter, all text colour follows through one variable on `<html>`. Check contrast
    in every state.
- **Layout.**
  - Every static frame is a poster.
  - Use a visible or implied grid, with a section rhythm that varies: at least 4 layout families across 8
    sections, and no two neighbours the same. No three equal feature cards.
  - Compose the 390px first screen, loader, footer and 404 as deliberately as the hero.
- **Shape and material.** One radius rule. Use inner borders or tinted shadows over neon glows. Use spacing
  before cards. Grain or dither goes on the substrate or inside one display word, never over body text.
- **Motion.**
  - One ease family (expo-out or cubic-out) and one duration ladder: hover about 200ms, menus and cards about
    600ms, a reveal about 1000ms, the hero intro 1400ms or less.
  - Stagger 20 to 80ms in reading order, with a total spread of 0.6s or less. Big things move slower than
    small things.
  - The world or object moves first, type second, chrome last.
  - Page choreography follows this ladder. Component micro-interactions follow `animate` (or `animate-expo`),
    with the same ease family.
- **Images.**
  - Real images, never `<div>` fake screenshots.
  - Priority order: the user's assets, then generated images, then `awwwards` `scripts/photos.mjs` or
    `https://picsum.photos/seed/{word}/{w}/{h}` with credits.
  - Logo walls only for customers the user confirmed, with real SVG marks (Simple Icons, devicon).
- **Icons.** Phosphor, HugeIcons, Radix, Tabler, or Solar through Iconify. No hand-rolled SVG paths, and no
  model-drawn illustration.
- **Stack.**
  - Use the project's stack first.
  - On a new build: Next.js App Router by default, or Astro for an animation-heavy static showcase.
  - GSAP with ScrollTrigger, Lenis, and OGL. Use three.js or R3F only for real 3D (`bosskuai-3d-web-development`).
  - Use exactly one smooth-scroll engine.

## 5. Build laws (a failure blocks shipping)

1. **Content is visible by default.**
   - No text, image or control waits on JS, a CDN, WebGL or a scroll trigger.
   - Hidden start states are set by JS in the frame their tween starts.
   - No sections authored at `opacity: 0`.
2. **One clock.**
   - Everything runs on GSAP's ticker. Never use `addEventListener('scroll')` or `requestAnimationFrame` loops of
     your own.
   - Animate `transform`, `opacity`, `clip-path` and shader uniforms, never layout properties.
3. **Hover never moves the box and never wipes an underline.**
   - States are tonal or typographic, or happen inside a static box.
   - Every control has hover, `:focus-visible` and active states from the system.
   - Inline body links keep an underline at rest.
4. **The native cursor is always visible.** A follower is allowed only on fine pointers with full motion, and only
   as a label. On touch, nothing depends on hover.
5. **Loader only for real loading.** It shows honest progress on real promises, ends within 1.5s, can be skipped,
   and runs once per session. No timed 0 to 100 counters.
6. **3D only when it carries the subject.**
   - Budget it first: DPR at 2 or below, init after LCP, pause offscreen, a poster fallback.
   - The canvas is `aria-hidden` and the DOM owns every word.
7. **Reduced motion is a designed state.**
   - No smooth scroll, no GL, no scrub, no loader theatrics, all content visible.
   - The OS setting can flip live.
   - Anything that moves on its own for more than 5s gets a pause control.
8. **Dead is a fail too.** Every page ships a hero intro, one signature moment that answers scroll, pointer or
   state, a nav that enters and responds, and crafted hovers.
9. **Award conventions must carry real information:** corner nav, index lists, vertical labels, coordinates.
   No decoration eyebrows (`V0.6`, `00 / INDEX`), no decorative 01/02/03, no fake version footers or status dots,
   no decorative text strips, no scroll-jacking that fights the user.

## 6. Content honesty (applies to all generated copy)

- No invented people, companies, numbers, reviews, awards, client logos or dates. Use what the user supplied, or an
  honest placeholder. A more believable invention (47.2% instead of a round number) is still fabrication.
- No startup-slop brands (Acme, Nexus, SmartFlow). Use the real name or `[BRAND]`.
- No filler verbs (elevate, seamless, unleash, next-gen, cutting-edge, revolutionize). Do not write "passionate
  about crafting digital experiences".
- Never repeat a sentence across sections. Write copy that fits the device ("hover" is wrong on touch).
- **Zero em or en dashes** in visible text, alt text and buttons. Use a hyphen or rewrite the sentence.
- Use initials or a labelled slot until real photos exist. No SVG "egg" avatars.

## 7. Quality gates and the jury score (before calling it done)

- **Accessibility.**
  - A skip link comes first, and focus is visible (2px, 3:1) and never under a sticky header.
  - One `<h1>`, landmarks and `lang`.
  - Text contrast is 4.5:1 (3:1 at 24px and up), measured on the worst frame behind the text. Compute it with
    `skills/antislop-human/contrast-check.py`, never by eye.
  - Targets are at least 24px, and primary targets at least 44px.
  - 0 serious or critical axe violations.
- **Performance at mobile p75:**
  - LCP is 2.5s or less, on real text or an `<img>`.
  - CLS is under 0.05.
  - INP is 200ms or less.
  - First-route JS is 350KB compressed or less.
  - Fonts: at most 2 preloads, and 200KB of WOFF2 or less.
- **Scenarios.** Every route still shows all of its text, images and links with no JS, with no WebGL, and with
  the CDN blocked. The reduced-motion version is composed, not broken.
- **SEO and meta.** Each route gets a unique title and description, an OG image, canonical, sitemap, robots and
  a 404. No console errors, debug GUIs or localhost URLs.
- **Eyes on it.**
  - Screenshot at 390 and 1440 plus reduced motion. Use `scripts/shot.mjs` from the BosskuAI install, or the
    `jury` and `awwwards` shoot scripts.
  - View every screenshot on its own.
- **Score.** Run `jury`. It sends the evidence to a fresh critic that never sees the code.
  - If Playwright is missing, self-score with the rubric in `awwwards-web-design` `references/jury-lens.md`.
  - Ship target: a jury estimate in the Site of the Day band (7.2 and up), zero build-law failures, and a
    signature that survives with motion off.
  - Anything lower goes back to the build as a ranked fix list.

## 8. Product UI: the craft bar (dashboards, app screens, admin, forms)

The same quality, tuned for a task. Usability is 30% of the jury score, and here it is most of the job.
- **Keep:**
  - the type system: a distinctive display face for headings, a neutral body face, tabular numerals for data;
  - one accent kept for state, progress and focus;
  - the tonal palette;
  - one radius rule;
  - hover that never moves the box, with full hover, focus, active, disabled, loading, empty and error states;
  - the contrast, target and keyboard gates;
  - the performance budgets;
  - honest content.
- **Motion:**
  - micro 120 to 200ms, panels and menus 200 to 300ms, one ease family, through `animate`;
  - no scroll reveals on data;
  - no smooth-scroll engine, no loader beyond a stable skeleton, no WebGL unless the data itself is 3D or spatial.
- **Signature:** one small owned detail, such as an empty state, an onboarding moment or one key transition.
  It is never decoration on every row.
- Build with `bosskuai-ui-ux-design-to-code`. Tokens and components come from `bosskuai-design-systems`.

## 9. Pre-flight (tick every box; an honest fail means not done)

- [ ] Design Read, Concept Card, the direction line and the dials are written in `DESIGN.md`, reasoned from the brief.
- [ ] One direction, one system, one accent, one radius rule, one page theme, one ease family, one smooth-scroll engine.
- [ ] Display face is not Inter, Space Grotesk, Syne, Fraunces or Instrument Serif. At most 2 families, self-hosted.
- [ ] Signature recurs at 3 or more touchpoints and survives with motion off. Nothing on the page is dead.
- [ ] Content visible with no JS, no WebGL and no CDN. Reduced motion is designed. Loader is 1.5s or less, or absent.
- [ ] No 3 equal cards. At least 4 layout families. 390 first screen, footer and 404 designed.
- [ ] Real images, real logos only when confirmed, no fake screenshots, no invented people, numbers or awards.
- [ ] Zero em or en dashes. No filler verbs. Every visible string re-read.
- [ ] AA contrast on the worst frame, visible focus, a skip link, 24 and 44px targets, 0 serious axe issues.
- [ ] Mobile LCP 2.5s or less, CLS under 0.05, INP 200ms or less, no console errors.
- [ ] Screenshots at 390, 1440 and reduced motion viewed, and the `jury` score is in the Site of the Day band.

## 10. Stack and precedence

- **Precedence:**
  1. the user's explicit instruction;
  2. the project's `DESIGN.md`;
  3. the honesty, accessibility, contrast and reduced-motion gates (`antislop` + `antislop-ui`);
  4. this house rule;
  5. a named vocabulary (`hallmark`, `taste-skill`, a design system);
  6. agent defaults.
- **One direction skill at a time.** This file replaces `taste-skill`, `hallmark` and the single-aesthetic skills
  unless one of them is asked for by name. When it is, this file still supplies the laws and gates.
- **Not this skill:**
  - `DESIGN.md` and tokens: `bosskuai-design-systems`;
  - a screenshot or mockup to code: `bosskuai-ui-ux-design-to-code`;
  - WCAG audits: `accessibility`;
  - motion craft: `animate`;
  - GSAP and Lenis detail: `bosskuai-gsap-animation`, `bosskuai-lenis-smooth-scroll`;
  - scroll fly-throughs: `scroll-world`;
  - how-it-works figures: `anatomy`;
  - marks: `logo-design`.
- **The gate after the build:** `antislop` + `antislop-ui` (+ `antislop-layoutmobile`, `antislop-human`). State
  its dials when it runs:
  - VARIANCE maps to RHYTHM and MOTION_INTENSITY maps to MOTION;
  - ENERGY is the higher of the two;
  - a value of 1-3 becomes 1, 4-7 becomes 2, and 8-10 becomes 3.

The point is intent, not decoration. If the reason for a flourish is "to look designed", delete it.

## Evidence contract and rendered finish gate

- **Before building,** write down the product surface, the user's job, the primary action, the hierarchy, the
  target viewports (390x844 and 1440x900), and the reference observation behind each major choice. A palette
  alone is not evidence.
- **For each content state,** record the trigger, the visible feedback and a safe next action:
  - loading: a stable structure;
  - empty: explain, and offer a next step;
  - error: the specific cause, plus recovery;
  - partial: show what exists, and mark what is missing;
  - success: confirm, and show the next step or undo;
  - permission: explain the boundary, and offer a safe path.

  If a state does not apply, write the reason. A state you could not test is untested, not "not applicable".
- **Reuse before you add.** Use existing project components, tokens and icon libraries before a new visual
  system. Fixed-format elements keep stable dimensions when labels or hover states change. Long labels wrap or
  resize, never overflow.
- **Finish gate.**
  - Inspect the rendered result at every target viewport, not just the source.
  - Check the keyboard path, focus, labels, contrast, reduced motion, touch targets, long content, and each
    applicable state.
  - Keep screenshots in the workspace, fix failures, and repeat the affected checks after structural changes.
  - Report untested items instead of claiming a pass.

Adapted in part from ECC skills/frontend-design-direction (affaan-m/ECC, MIT), owenisas/awwwards-web-design (MIT),
juliobsz/skills awwwards and jury (MIT), and MengTo/Skills (MIT).
