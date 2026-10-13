---
name: bosskuai-ui-personality
description: "Use when adding personality to a product UI: playful microcopy, delightful error, empty and loading states, micro-interactions, Easter eggs and achievements that stay accessible, reduced-motion safe and useful."
---

# BosskuAI UI Personality and Delight

Use this skill to add small moments of character that support the task instead of getting in its way. Every playful element needs a reason, a quiet default, and an accessible fallback.

## How this differs from nearby skills

- **`bosskuai-taste`**: overall design direction for landing pages; this skill adds personality to specific moments in an existing product.
- **`animate`**: how to build one animation correctly (purpose, properties, curve). Use it when implementing a specific motion from this skill's plan.
- **`antislop-copywriting`** and **`copywriting`**: general copy quality and marketing copy. This skill covers in-product microcopy and tone shifts.
- **`accessibility`**: full WCAG audit; this skill only keeps delight accessible.

## Workflow

1. Read the brand guidelines and audience. Decide how much playfulness fits: serious flows (payments, errors with data loss) need little or none.
2. Define a personality spectrum by context: professional, casual, error, success. State the voice for each.
3. Choose where delight goes using a taxonomy: subtle (hover and button feedback), interactive (user-triggered celebration), discovery (hidden shortcuts, Easter eggs), contextual (404, empty states, seasonal theming).
4. Write microcopy for errors, loading, success, empty states and buttons. Errors must still say what went wrong and what to do next.
5. Design micro-interactions with a functional job (confirm, guide, reduce wait anxiety). Keep them short and cheap to render.
6. If using achievements or streaks, avoid nagging, dark patterns, or pressure to return.
7. Accessibility pass: respect `prefers-reduced-motion`, keep content readable by screen readers (decorative emoji hidden or given text alternatives), keep contrast and focus states, do not hide required information behind a surprise.
8. Performance pass: delight must not block rendering or inflate bundles.
9. Cultural check: avoid humour that excludes or confuses users in other regions or languages.
10. Measure with task completion and user feedback; remove anything that slows tasks.

## Guardrails

- No playful tone in destructive confirmations, billing or safety messages.
- Do not claim engagement gains without a test; treat quoted improvements as hypotheses.
- Provide a way to turn off or reduce animation and sound.
- Easter eggs must not be required for any task.

## Output format

```text
Context and tone: [product, audience, allowed playfulness]
Moments to enhance: [place, type, purpose]
Copy: [state, text]
Interaction spec: [trigger, motion, duration, reduced-motion fallback]
Accessibility and performance checks: [results]
Success measure: [metric]
```

Adapted from agency-agents/design/design-whimsy-injector.md (agency-agents, MIT).
