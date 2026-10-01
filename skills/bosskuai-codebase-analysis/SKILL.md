---
name: bosskuai-codebase-analysis
description: "Trace execution paths, call chains, module boundaries, and side effects to explain runtime behavior. Run bosskuai-project-understanding first if the stack is still unknown."
---

# Codebase analysis

Use to explain how code actually runs before changing it. If the project's purpose or stack is still unknown, run `bosskuai-project-understanding` first.

1. **Find the entry points** — HTTP server, CLI, main function, event listener, cron job — then read top-level structure, major modules, config, and test layout, and identify the stack and build system.
2. **Trace the real execution path** for the behavior in question: entry → auth/middleware → routing → handler → business logic → data access → response. Note what transforms at each step.
3. **Back every important call, dispatch, or transport with `file:line` evidence.** Proximity, naming, or an import alone do not prove execution order — find the actual call.
4. **Surface non-obvious side effects**: cache writes, events emitted, background jobs triggered, external calls — and whether each is sync or async, with its failure/retry path.
5. **Map ownership**: which module owns which domain entity, where the boundaries sit, and the architectural style (monolith, layered, hexagonal, microservices, event-driven).
6. **Flag tech-debt and dead-code candidates** (deep nesting, duplicated logic, functions with no internal callers) — but check for public APIs, plugins, registration, and dynamic dispatch before calling anything dead. These are candidates, not verdicts.
7. **Name extension points and high-risk areas**: where the codebase expects new behavior, and where a change is likely to regress something.
8. **Separate confirmed from inferred in the summary**, and list what remains unread rather than rounding up to certainty.

Full phase-by-phase workflow and output template: `reference.md`.
