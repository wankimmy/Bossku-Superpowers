---
name: bosskuai-codebase-analysis
description: "Use when explaining runtime behavior by tracing execution paths, call chains, module boundaries and side effects. Run bosskuai-project-understanding first if the stack is unknown."
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

**When several sessions or tools have edited the same code, also look for drift:**

- Read history in chunks as rough eras, and compare the same kind of file (route handlers, forms, data access) across eras.
- Look for parallel implementations of one responsibility, and ask whether they are meant to agree before calling it duplication. If intent is unclear, say "possible duplication, intent unclear".
- Check fallback chains (`??`, `||`, defaults) to see which side is meant to be the fallback; a reversed order can pass a null or zero into a critical field silently.
- For each event, webhook, or job handler, list the state it reads but did not create, and what guarantees the creator ran first (an existence check, an upsert, queue ordering, a transaction). "It usually happens in this order" is not a guarantee. Record handlers you checked and found safe.
- For money, quantity, and time values, note the unit where it is created (integer cents, UTC date, 0 to 1 fraction) and check every downstream read, even under a different variable name.
- Grade findings: breaks data or money, breaks under specific conditions, or cosmetic. If you cannot confirm the runtime impact, say so instead of guessing a severity.
- Keep findings in a registry with status; never delete one, and mark "won't fix" with a reason. After each fix, check it reached every side of the mismatch.

Full phase-by-phase workflow and output template: `reference.md`.

Drift checks adapted in part from specialized/specialized-codebase-archaeologist.md (agency-agents, MIT).
