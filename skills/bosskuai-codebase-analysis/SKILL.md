---
name: bosskuai-codebase-analysis
description: "Use when explaining runtime behavior by tracing execution paths, call chains, module boundaries and side effects. Run bosskuai-project-understanding first if the stack is unknown."
---

# Codebase analysis

Use to explain how code actually runs before changing it. If the project's purpose or stack is still unknown, run `bosskuai-project-understanding` first.

1. **Find the entry points** — HTTP server, CLI, main function, event listener, cron job — then read top-level structure, major modules, config, and test layout, and identify the stack and build system. Record the runtime and framework versions from the manifests and lockfiles, so each finding names the version it applies to. Start from the current infra map (which processes run where, and how many instances run at once), not from an assumed single server.
2. **Trace the real execution path** for the behavior in question: entry → auth/middleware → routing → handler → business logic → data access → response. Note what transforms at each step. For a reported problem, trace every entry point under the area the user named (each route, screen, tab and job), not only the first one, and say which you did not trace.
3. **Back every important call, dispatch, or transport with `file:line` evidence.** Proximity, naming, or an import alone do not prove execution order — find the actual call. For each write to shared state on the path, name its guard (a transaction, a row lock, a unique key or an idempotency key), or mark it `unguarded`.
4. **Surface non-obvious side effects**: cache writes, events emitted, background jobs triggered, external calls — and whether each is sync or async, with its failure/retry path. For each outbound call, note the timeout and whether a retry is safe to repeat, or mark it unknown.
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

Shared bar for the blast-radius and release checks: `../../references/checklists/engineering-quality-bar.md`.

Drift checks adapted in part from specialized/specialized-codebase-archaeologist.md (agency-agents, MIT).

**Before a cross-module or high-risk change (blast radius), answer in order, with evidence from real imports, calls, routes, schemas, `git grep`, `git diff`, or tests, never directory names; mark gaps `unverified`:**

1. Code: entry points, direct callers, downstream consumers, generated artifacts, compatibility layers.
2. Data: schemas, migrations, historical data, serialization, caches, idempotency keys. Sample real value types and nulls from a production data copy for any stored data this change touches. If there is no copy, ask the user to prepare one, and mark this check `unverified` in the result until it arrives. The code does not show what is stored.
3. Interfaces: APIs, messages, file formats, CLIs, and who consumes and provides them.
4. Tests: which success criteria and regression commands prove the change.
5. Docs: which ADRs, contracts, specs, or status docs go stale.
6. Release: deploy order, compatibility window, data recovery, rollback command, irreversible effects. Name the users, scheduled jobs and reports that see the change, and what old and new code do side by side during the roll. For migrations, auth, breaking interfaces, and production releases, a missing rollback or recovery step is a blocker.

**After implementation**, compare the actual diff with the plan: does it solve the original problem, did it exceed the declared scope (and was that approved), does the evidence cover the success criteria rather than just show a command ran, are docs synced, and is any temporary code or follow-up left.

**Inventorying an unfamiliar or legacy repo**: tag each file as own code, embedded third-party code (find it by directory names, headers, license files, version markers), or build artifact; note committed artifacts and duplicated wrappers or outdated vendored copies. Label each module core, extract/merge, rebuild, or deprecate. Start with 1-2 files per module on huge repos, then go deeper only on modules flagged for refactoring.

Adapted in part from ECC skills/change-impact and skills/repo-scan (affaan-m/ECC, MIT). The repo-scan ECC skill is only an installer pointer for an external tool; nothing from it is installed here.
