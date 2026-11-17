---
name: bosskuai-ui-ux-design-to-code
description: "Use when reviewing or critiquing UI/UX, or turning designs or screenshots into implementation-ready code guidance: design systems thinking, mobile-responsive behavior, and accessibility (WCAG)."
---

# UI/UX and design-to-code

For critiquing a screen or flow and turning it into implementation-ready guidance. Not the design system's own tokens and foundations (`bosskuai-design-systems`) or 3D/WebGL work (`bosskuai-3d-web-development`).

1. **Name the user's goal on this screen** — their goal, not the product's — before judging anything else.
2. **Load the baseline.** Check `.bossku/DESIGN.md` then root `DESIGN.md` and build against its tokens. If none exists, say so and point to `bosskuai-design-systems` instead of inventing a style.
3. **Familiar first.** Name the product type (showcase web, task-first public page, product UI, consumer or mobile app); when it is unclear, say which type you assumed in one line. Reuse the project's component library and existing screens before inventing a pattern. Put navigation, search and filter, settings, forms and back where users expect them. Innovate only where it helps the main task.
4. **Read the existing code first**: where its state lives (store, URL, server cache) and which other screens render the same component (search its imports); name each one in the handoff. Then **break the screen into a component hierarchy** (layout, navigation, content, actions, feedback), then **list every state each key component needs** (the state list below). Design with real-length content: a 200-row table, the longest real name, the largest real amount, error text and translated strings. A design that only shows the happy path is unfinished. Each state's message must match what happened. Where the user can act, error, empty and zero-result messages say what to do next, and a disabled control says why; in a review, a confusing or wrong-for-the-state message is a finding to fix, not a nit (severity per the UI/UX rule in ../bosskuai-rigorous-code-review/reference.md, step 4).
5. **Check responsive behavior mobile-first**: how navigation collapses, whether tables scroll or reflow, 16px minimum body text, and 200% text zoom (WCAG 1.4.4). The width set is named here once: `node <BosskuAI install>/scripts/layout-check.mjs <url> [--widths ...] [--json]` (the session-start line prints the full path) runs at 320, 375, 390, 768, 1024, 1440 and 1920 CSS pixels; 320 also stands for 400% zoom of a 1280 page (WCAG 1.4.10 reflow, no sideways scroll). Take screenshots at 390 and 1440 as a minimum, and at any width the check flags (`shot.mjs --widths 320,768`); name each screenshot you looked at. Exit 0 means no errors (read any warnings), 1 is findings to fix, 2 means the check did not run: report "not verified: <reason>", never a pass. Fix the geometry; never hide it with a global `overflow-x: hidden`. Layout reliability detail: `../../references/checklists/layout-reliability-checklist.md`. Where the repo or the design file asks for other sizes, add those. Also check each screen in the locale formats its markets use: `01/02/2026` is 1 February in Malaysia and 2 January in the US, and some locales write `0,01`.
6. **Check accessibility as correctness, not polish**: contrast per the measurement rules below, computed with the `contrast-check.py` script in the `antislop-human` skill, never by eye; full keyboard reach with visible focus, never hidden behind a sticky header (WCAG 2.4.11); a closed modal returns focus to its opener; semantic HTML first — ARIA only where HTML has no equivalent, never to paper over bad markup; every input labeled, errors wired to `aria-describedby`.
7. **Hold the craft bar for the product type.**
   - Showcase web: the full `bosskuai-taste` house rule and a `jury` score on a public URL or a local production build.
   - Task-first public pages (storefront, checkout, booking, docs, pricing): familiar commerce and form patterns, native scroll, trust and clarity first; house craft for type, spacing and imagery; no intro loader, no scroll theatre.
   - Product UI: the project's design system and component library first; one accent for state and focus, one radius rule, hover that never moves the box, state-change motion of 120 to 300ms; no concept card, no signature moment, no jury, no loader beyond a stable skeleton. The verdict is a task walkthrough of every task in the brief, the state list, the layout check and screenshots.
   - Consumer and mobile apps: platform conventions (native navigation, back behaviour, safe areas, thumb reach, keyboard avoidance), then the product UI rules. Engagement features only as `../../references/checklists/engagement-ethics-checklist.md` allows.

   A redesign follows the type of the thing being redesigned. `DESIGN.md` or the user may name another style. The frequency of an action decides whether it animates at all; reduced motion is always honoured.
8. **Reject generic AI-slop visuals on sight**: gradient hero with glowing blobs, glassmorphism everywhere, generic three-card sections, fake dashboard decoration, robot/sparkle icons as the main idea, over-empty SaaS spacing. Prefer product-specific evidence — real screenshots, CLI output, actual data shapes.
9. **Translate to implementation primitives**: layout approach, component list with props/variants, a state machine, the data shape each component needs, interaction and animation notes.
10. **Flag every ambiguity by name** instead of inventing a silent decision. If nobody can resolve it, pick the simplest state matching the rest of the design system and say so in one line.

Verify with the repo's own lint, typecheck, test and build commands, plus a browser check at each breakpoint. Walk each listed state at 390 and 1440 and at any flagged width, with a failed or slow request mid-flow; a state left unchecked makes the result provisional, not done (shared bar, header).

## State list and measurement rules

These win where a vendored design skill gives a different number.
- **States:** empty; loading (with a slow path: still working after a few seconds, with a way to cancel or retry); error with a way to recover; success; disabled with the reason shown; offline or retry where the screen depends on the network; confirmation before a destructive action, and undo where the action can be undone.
- **Touch targets:** 24 by 24 CSS pixels is the floor (WCAG 2.5.8); 44 by 44 for primary actions and anything used by touch.
- **Contrast:** large text for the 3:1 rule is 24px regular or about 18.66px bold; everything else needs 4.5:1.

The Nielsen heuristics, the full anti-AI checklist, and the output template: `reference.md`. The shared bar: `../../references/checklists/engineering-quality-bar.md`.

## Batch screenshots to Vue 3

For a folder of design exports going into a Vue 3 app (Vant, Element Plus or Ant Design Vue):
- Group screenshots by module and page; treat list, detail, form, loading and empty variants of one page as states of one component, not separate pages.
- Map visual elements to the chosen library's components and keep to that one library. Check the library version in the lockfile first, since component names and props change between major versions. Use asset priority page-level, then module-level, then global. Extract a shared component only when a region repeats.
- Match CSS units to the export baseline (for example a 3x export width) and wire routes in the project's existing router style.
- Design images may contain private data. Do not send customer designs to an external model API or converter without permission. Do not install or run a third-party converter, or put an API key in a committed config, unless the user approves; pin its version if used.
- Treat the output as a first draft: review placeholder copy, mock data and assets, then run the project's formatter, linter, type check and build.

Adapted in part from ECC skills/ui-to-vue (affaan-m/ECC, MIT).
