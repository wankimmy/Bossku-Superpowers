---
name: bosskuai-qa-automation-strategy
description: Use this for automated testing strategy, Playwright/Cypress, feature tests, integration tests, regression suites, fixtures, CI gates, and release confidence.
---

# QA automation strategy

For deciding what to test, at which level, and what gates a release — not writing one specific test (`bosskuai-tdd-loop`) or driving one browser session (`bosskuai-browser-automation`).

1. **Map risk before coverage.** List the flows where failure is expensive — auth, payments, permissions/tenancy, deletion, anything that sends money or mail — and cover those deepest first. A 90%-covered suite with an untested refund path is still untested.
2. **Push each behaviour to the cheapest level that would still catch the bug.** Unit for pure logic and edge cases. Feature/integration (real database and routing, faked third parties) for most backend invariants — best value per test. Contract tests at an external boundary. End-to-end only for a genuine cross-system journey; keep that set small.
3. **Design for determinism before writing tests**: seeded factories, a controlled clock, isolated per-test data, no order dependence, no live network calls, explicit waits instead of sleeps. A flaky suite is worse than a small one — it trains people to re-run instead of investigate.
4. **Split the CI gate by speed.** Lint, types, unit, feature tests block the PR. Full E2E, cross-browser, and performance suites run on merge or nightly, with a named owner for failures.
5. **Close the loop on every production bug**: add one regression test that would have caught it, or write down why one is not practical — never skip silently.
6. **Quarantine, don't skip.** A flaky test gets an owner and a deadline, never a permanent skip; a gate nobody can fix within a month gets disabled, not ignored forever.
7. **Audit before calling it done**: tests asserting on implementation details that break on every refactor, a test that mocks the thing it claims to verify, test data that depends on shared environment state.

If the right level for a behaviour is genuinely unclear and nobody can answer, write it as a feature/integration test — the safest default.

The full risk-allocation reasoning and the output template: `reference.md`.
