---
name: bosskuai-engineering-delivery
description: Use when implementing a software change through planning, tests, review, and observed product verification.
---

# Engineering delivery

Ship the change in this order. Work on your own; ask the user only if the request reads two ways and the code cannot tell you which, or if a step needs an input you do not have (infra details, a production data copy, access).

1. **Orient.** Know the project's current infra architecture before writing code: where each part runs, the web, worker and scheduler processes, data stores, caches and queues, how config reaches each environment, how deploys run, and how many instances run at once (from compose files, IaC, CI/CD and deploy docs; ask the user for the rest). Read the versions it runs on from the manifest, lockfile or runtime, check the latest stable live (shared bar section 2), and use only APIs that exist in the installed version. Read the code, tests and README the change touches. List every entry point that reaches it: other modules, CLI, scripts, README and docs examples. Follow the project's conventions.
2. **List the requirements.** Number every rule in the request and the linked issue (Linear, GitHub) and write the check that will prove each one. If something is ambiguous, take the reading the README, tests or existing code support, and state it in one line.
3. **Test first.** For each requirement add a test, plus the edge cases it implies: empty, one, many, duplicates, boundaries, wrong type, repeated calls, input left unchanged, exact error type, race conditions (two users or jobs at once, double submits), and data in the types production really stores (the number 0.01 in tests can be the string "0.01" in production). Walk each scenario by who, what, when, the record's state and each dependency (shared bar section 3). Run them and see them fail for the right reason.
4. **Make the smallest change that passes.** Update every call site: search for the old name, signature or behaviour across code, scripts and docs. Leave unrelated code alone; remove only what your change orphaned.
5. **Run everything.** Build, type-check, lint and the whole test suite, with no new warnings, then your own checks. Read the output. Fix the code, never the test, until it is green, and CI must be green on the pushed head too.
6. **Check data, users and deploy.** Run the change (migration, queries, new rules) against a masked production data copy (personal data and secrets masked, kept out of git, logs and fixtures), never production itself: the result must match what deploy should give, with no rows missed or broken (nulls, legacy values, duplicates), and data types and structure must match production. Check the effect on day-to-day operations and existing users, and that deploy has zero downtime (old code on the new schema, new code on the old), jobs queued before the deploy still run, changed cache keys or formats are versioned, and new config exists before the code reads it. For an API integration, handle the endpoint down or slow, retries with exponential backoff, jitter, a capped wait and a limit on attempts, only for calls that are safe to repeat (idempotent methods such as GET, PUT and DELETE, or an idempotency key for POST), a delay the caller can afford, logged requests and responses (secrets and personal data masked), and a response with extra fields (ignore them), missing fields or a changed data type (reject loudly, never coerce silently). If you need a production copy or access you do not have, ask the user to prepare it.
7. **Audit.** Re-read the request and the linked issue line by line against your diff, and check the PR description matches it. For each requirement name the code and the run that covers it. Fix any gap and run again. Check that every file in the diff belongs to the change. Plans, work-item notes, handoffs, scratch scripts, logs and local config stay out of the PR unless the repo keeps them on purpose, and any kept file must be current and match the code.
8. **Report** what you ran, what passed, and anything you could not verify. Mark a bar section that cannot apply "not applicable: <reason>"; a missing input makes the result "provisional (missing: <input>)".

Migrations, public APIs, security-sensitive changes, rollback plans, feature flags, ADRs and the long Definition of Done: read `reference.md` in this folder. The full quality bar, with where to read the current and latest version for each language and the types the same value can arrive as: `../../references/checklists/engineering-quality-bar.md`.

## When agents do most of the work

- Define the completion check before executing: one capability check for the new behaviour and one regression check for what must not change. Run both first and keep the failure output as the baseline; rerun and compare after.
- Split work into units that fit about 15 minutes: each independently verifiable, with one dominant risk and a clear done condition.
- Use the cheapest model that fits (narrow edits and boilerplate small, implementation and refactors mid, architecture and root-cause analysis largest). Move up a tier only after a lower tier fails with a clear reasoning gap, not on a hunch.
- Keep the session for tightly coupled units; start fresh after a major phase change; compact after a milestone, not mid-debug.
- Spend review on invariants, edge cases, error boundaries, auth assumptions, hidden coupling and rollout risk. Leave style to the formatter and linter.
- Raise the bar for generated code: regression tests for every touched area, explicit edge-case assertions, and integration checks at interface boundaries.

Adapted in part from ECC skills/agentic-engineering and skills/ai-first-engineering (affaan-m/ECC, MIT).
