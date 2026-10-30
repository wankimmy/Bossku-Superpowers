---
name: bosskuai-ui-ux-design-to-code
description: "Use when reviewing or critiquing UI/UX, or turning designs or screenshots into implementation-ready code guidance: design systems thinking, mobile-responsive behavior, and accessibility (WCAG)."
---

# UI/UX and design-to-code

For critiquing a screen or flow and turning it into implementation-ready guidance. Not the design system's own tokens and foundations (`bosskuai-design-systems`) or 3D/WebGL work (`bosskuai-3d-web-development`).

1. **Name the user's goal on this screen** — their goal, not the product's — before judging anything else.
2. **Load the baseline.** Check `.bossku/DESIGN.md` then root `DESIGN.md` and build against its tokens. If none exists, say so and point to `bosskuai-design-systems` instead of inventing a style.
3. **Break the screen into a component hierarchy** (layout, navigation, content, actions, feedback), then **list every state each key component needs**: empty, loading, error, success, disabled, slow (still working after a few seconds, with a way to cancel or retry), and edges like long text or zero results. Design with real-length content: a 200-row table, the longest real name, the largest real amount. A design that only shows the happy path is unfinished. Each state's message must match what happened. Where the user can act, error, empty and zero-result messages say what to do next, and a disabled control says why; in a review, a confusing or wrong-for-the-state message is a finding to fix, not a nit (severity per the UI/UX rule in ../bosskuai-rigorous-code-review/reference.md, step 4).
4. **Check responsive behavior mobile-first**: 320/375/768/1024/1440px, how navigation collapses, whether tables scroll or reflow, 44×44px touch targets, 16px minimum body text. Where the repo or the design file asks for other sizes, use those, and check each screenshot against the design. Also check each screen in the locale formats its markets use: `01/02/2026` is 1 February in Malaysia and 2 January in the US, and some locales write `0,01`.
5. **Check accessibility as correctness, not polish**: 4.5:1 text contrast (3:1 large text/UI) computed with `skills/antislop-human/contrast-check.py`, never by eye; full keyboard reach with visible focus; semantic HTML first — ARIA only where HTML has no equivalent, never to paper over bad markup; every input labeled, errors wired to `aria-describedby`.
6. **Hold the Awwwards craft bar, the default style** (`bosskuai-taste` §8), unless `DESIGN.md` or the user names another:
   - a distinctive heading face with a neutral body face and tabular numerals;
   - one accent for state and focus;
   - one radius rule;
   - hover that never moves the box;
   - motion of 120 to 300ms in one ease family;
   - one small signature detail.

   Keep native scroll, with no loader beyond a stable skeleton and no WebGL unless the data is spatial.
7. **Reject generic AI-slop visuals on sight**: gradient hero with glowing blobs, glassmorphism everywhere, generic three-card sections, fake dashboard decoration, robot/sparkle icons as the main idea, over-empty SaaS spacing. Prefer product-specific evidence — real screenshots, CLI output, actual data shapes.
8. **Translate to implementation primitives**: layout approach, component list with props/variants, a state machine, the data shape each component needs, interaction and animation notes.
9. **Flag every ambiguity by name** instead of inventing a silent decision. If nobody can resolve it, pick the simplest state matching the rest of the design system and say so in one line.

Verify with `pnpm lint && pnpm typecheck && pnpm test && pnpm build`, plus a browser check at each breakpoint.

The Nielsen heuristics, the full anti-AI checklist, and the output template: `reference.md`. The shared bar: `../../references/checklists/engineering-quality-bar.md`.

## Batch screenshots to Vue 3

For a folder of design exports going into a Vue 3 app (Vant, Element Plus or Ant Design Vue):
- Group screenshots by module and page; treat list, detail, form, loading and empty variants of one page as states of one component, not separate pages.
- Map visual elements to the chosen library's components and keep to that one library. Check the library version in the lockfile first, since component names and props change between major versions. Use asset priority page-level, then module-level, then global. Extract a shared component only when a region repeats.
- Match CSS units to the export baseline (for example a 3x export width) and wire routes in the project's existing router style.
- Design images may contain private data. Do not send customer designs to an external model API or converter without permission. Do not install or run a third-party converter, or put an API key in a committed config, unless the user approves; pin its version if used.
- Treat the output as a first draft: review placeholder copy, mock data and assets, then run the project's formatter, linter, type check and build.

Adapted in part from ECC skills/ui-to-vue (affaan-m/ECC, MIT).
