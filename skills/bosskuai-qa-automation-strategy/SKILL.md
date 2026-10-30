---
name: bosskuai-qa-automation-strategy
description: "Use when setting automated testing strategy: Playwright/Cypress, feature tests, integration tests, regression suites, fixtures, CI gates, and release confidence."
---

# QA automation strategy

For deciding what to test, at which level, and what gates a release — not writing one specific test (`bosskuai-tdd-loop`) or driving one browser session (`bosskuai-browser-automation`).

1. **Map risk before coverage.** List the flows where failure is expensive — auth, payments, permissions/tenancy, deletion, anything that sends money or mail — and cover those deepest first. A 90%-covered suite with an untested refund path is still untested.
2. **Push each behaviour to the cheapest level that would still catch the bug.** Unit for pure logic and edge cases. Feature/integration (real database and routing, faked third parties) for most backend invariants — best value per test. Contract tests at an external boundary. End-to-end only for a genuine cross-system journey; keep that set small.
3. **Design for determinism before writing tests**: seeded factories that use production's data types and shapes (taken from a production copy, not guessed), a controlled clock, isolated per-test data, no order dependence, no live network calls, explicit waits instead of sleeps. A flaky suite is worse than a small one — it trains people to re-run instead of investigate.
4. **Split the CI gate by speed.** Lint, types, unit, feature tests block the PR. Full E2E, cross-browser, and performance suites run on merge or nightly, with a named owner for failures.
5. **Close the loop on every production bug**: add one regression test that would have caught it, or write down why one is not practical — never skip silently.
6. **Quarantine, don't skip.** A flaky test gets an owner and a deadline, never a permanent skip; a gate nobody can fix within a month gets disabled, not ignored forever.
7. **Audit before calling it done**: tests asserting on implementation details that break on every refactor, a test that mocks the thing it claims to verify, test data that depends on shared environment state.

If the right level for a behaviour is genuinely unclear and nobody can answer, write it as a feature/integration test — the safest default.

The full risk-allocation reasoning and the output template: `reference.md`. The shared quality bar: `../../references/checklists/engineering-quality-bar.md`.

## Regression coverage for AI-assisted changes

When the same model wrote and reviewed a change, it carries its blind spots into both steps, so mechanical tests must come first.

- Run tests and the type-check/build before any code review; a failure there is the top finding and needs no judgement.
- Assert the response contract (a list of required fields) rather than implementation, and name regression tests after the bug they prevent.
- Most common AI-introduced regressions to test for: mock/sandbox path and production path returning different shapes (assert both, or force the mock path in tests); a new field added to the response but not to the query's column list, so it is always undefined; error handling that sets an error but leaves stale data on screen; optimistic updates with no rollback when the request fails; a type cast hiding a null.
- For an external API, test the endpoint down or slow, retries, and a response with extra fields, missing fields or a changed data type. Race conditions on the same row (two users or jobs, double submits) need a real database with two connections, so test them in the feature/integration suite, not here.
- Write the test when the bug is found, ideally before the fix, and add tests where bugs cluster (auth, multi-path logic, state) rather than chasing a coverage percentage. Do not add tests for code that has never failed just to raise the count.
- Keep this suite fast (seconds, no database) so it runs on every bug-check.

Adapted in part from ECC skills/ai-regression-testing (affaan-m/ECC, MIT).
