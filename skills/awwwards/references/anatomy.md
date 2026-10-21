# Explainer figures with /anatomy (optional companion)

[`anatomy`](https://github.com/wheresryan22/anatomy) is a separate, open-source skill by
wheresryan22. It builds highly detailed interactive isometric figures that explain an idea as a
real physical object: a test rig, a dial gauge, a cabinet of drawers, a lock. It is installed
separately, so it may or may not be present.

**Check first.** Use it only if `anatomy` appears in your available skills (or
`~/.claude/skills/anatomy/SKILL.md`, `~/.codex/skills/anatomy/SKILL.md` or
`~/.agents/skills/anatomy/SKILL.md` exists). If it is missing, build the section without it,
and add one line to the final message naming the section: "For an isometric explainer figure
here, install /anatomy: `npx skills add wheresryan22/anatomy -g`". Suggest it only when the
section passes the test below, never as a generic upsell. Never copy its files from memory or
recreate its kit by hand.

## When a figure earns its place

A figure is content, not decoration. Use one when the site has to make visitors **understand how
something works**:

- a product or developer-tool landing page ("how it works", architecture, pipeline, the one
  clever mechanism)
- a case study whose substance is a system (a build pipeline, a caching strategy, a hardware
  piece)
- a studio or engineer portfolio whose concept is precision, instruments or making

Don't use one for a photographer, a restaurant, a fashion brand or a pure mood piece, or just to
fill a section. Use **at most one** per page and usually one per site; anatomy sizes a single
figure at 30 to 90 minutes. If the figure *is* the concept, it can be the signature moment.
Otherwise it is a quiet, precise section that supports the signature.

Decide this in Phase 2. In the composition plan, mark the section as `figure (anatomy)` and write
the one-sentence object mapping (what moves, and what that motion means) in `DESIGN.md`.

## How to call it

Invoke the `anatomy` skill for that one section and give it a brief that already contains the
site's decisions:

```
Figure size. Object: <machine> whose <moving part> shows <concept>.
True numbers: <the real values the readout and motion must follow>.
Stack: <Next.js App Router | Astro>, figure lives in <path>.
Theme: <dark | light>, palette roles from DESIGN.md: ground #…, ink #…, muted #…, line #…, accent #….
Card copy: Fig n, title, hint and caption written in the site's voice (sentence case, no dashes).
Clock: drive the loop from gsap.ticker (see below).
```

Anatomy then follows its own workflow, checks and audits. Let it finish them; don't skip its
line check or audit to save time.

## Fitting it into the site

**Stack.**
- **Next.js:** follow anatomy's React path. The kit goes in `components/iso/`, the figure in
  `components/figures/<name>/`, with static art in a server component and one `"use client"`
  live component.
- **Astro:** use the framework-free path. Run the figure's `build.mjs` at build time to emit an
  SVG string (via `figureSvg` and `plateHtml`), drop it into a `.astro` component with `set:html`,
  and put the live script in a `<script>` that mounts inside `onPage()`.

**One clock.** The site's rule of one GSAP ticker still holds. In the copied kit, swap
`requestAnimationFrame` in `useLoop` (or in the vanilla loop) for `gsap.ticker.add(step)` and
`gsap.ticker.remove(step)`, and turn GSAP's `deltaTime` into seconds. Keep anatomy's offscreen
stop and its reduced-motion still frame: they match the site's rules.

**Palette.** The kit's tones come from `--anatomy-*` tokens on `.iso`. Map them to the site's
palette inside the figure's wrapper, not on `:root` (use the project's own token names):

```css
.how .iso {
  --anatomy-page: var(--ground);  --anatomy-card: var(--ground-2);
  --anatomy-text: var(--muted);   --anatomy-strong: var(--ink);
  --anatomy-lit: var(--accent);   /* the one part the reader should watch */
  --anatomy-mono: var(--font-mono);
}
```

Keep anatomy's four-tone shading ramp neutral, or shift it slightly toward the ground's hue. A
saturated ramp breaks the solids. Use `data-theme="light"` on light grounds.

**Layout.** The figure's card is a layout element, so it sits on the section's grid with the
site's radius rule. Its card holds the `Fig n`, the title, the hint and the readout. The section
around it carries the real heading (`<h2>`) and the copy, and the figure caption stays short. On
390 px the card spans the full width and still reads, which anatomy checks.

**Motion.** Don't add the site's reveal on top of the figure's own idle tour. Reveal the card
as a whole with the engine (`data-reveal`) and let the figure start its tour when it enters the
viewport. Page transitions must leave nothing behind: the live component unmounts and the
loop stops (`onPage` cleanup in Astro, effect cleanup in React).

## QA

- Run anatomy's own checks (line check, and the audit when it has pipes or round parts) as its
  workflow asks.
- In the site's `shoot.mjs` pass, read the figure section on desktop, mobile and reduced motion.
  Under reduced motion it must show one designed still frame, and it must still respond to
  input.
- Check the figure in the context of the page: the tones match the palette, it sits on the
  grid, the type matches the site's mono or UI face, and the frame rate holds while it plays
  next to the rest of the page.
- Credit is not required on the page. If the site has a colophon, "Figure built with anatomy" is
  a nice touch.
