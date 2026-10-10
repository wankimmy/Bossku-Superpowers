---
name: bosskuai-ui-ux-design-to-code
description: "Use when reviewing or critiquing UI/UX, or turning designs or screenshots into implementation-ready code guidance: design systems thinking, mobile-responsive behavior, and accessibility (WCAG)."
---

# UI/UX and design-to-code

For critiquing a screen or flow and turning it into implementation-ready guidance. Not the design system's own tokens and foundations (`bosskuai-design-systems`) or 3D/WebGL work (`bosskuai-3d-web-development`).

1. **Name the user's goal on this screen** — their goal, not the product's — before judging anything else.
2. **Load the baseline.** Check `.bossku/DESIGN.md` then root `DESIGN.md` and build against its tokens. If none exists, say so and point to `bosskuai-design-systems` instead of inventing a style.
3. **Break the screen into a component hierarchy** (layout, navigation, content, actions, feedback), then **list every state each key component needs**: empty, loading, error, success, disabled, and edges like long text or zero results. A design that only shows the happy path is unfinished.
4. **Check responsive behavior mobile-first**: 320/375/768/1024/1440px, how navigation collapses, whether tables scroll or reflow, 44×44px touch targets, 16px minimum body text.
5. **Check accessibility as correctness, not polish**: 4.5:1 text contrast (3:1 large text/UI) computed with `skills/antislop-human/contrast-check.py`, never by eye; full keyboard reach with visible focus; semantic HTML first — ARIA only where HTML has no equivalent, never to paper over bad markup; every input labeled, errors wired to `aria-describedby`.
6. **Reject generic AI-slop visuals on sight**: gradient hero with glowing blobs, glassmorphism everywhere, generic three-card sections, fake dashboard decoration, robot/sparkle icons as the main idea, over-empty SaaS spacing. Prefer product-specific evidence — real screenshots, CLI output, actual data shapes.
7. **Translate to implementation primitives**: layout approach, component list with props/variants, a state machine, the data shape each component needs, interaction and animation notes.
8. **Flag every ambiguity by name** instead of inventing a silent decision. If nobody can resolve it, pick the simplest state matching the rest of the design system and say so in one line.

Verify with `pnpm lint && pnpm typecheck && pnpm test && pnpm build`, plus a browser check at each breakpoint.

The Nielsen heuristics, the full anti-AI checklist, and the output template: `reference.md`.
