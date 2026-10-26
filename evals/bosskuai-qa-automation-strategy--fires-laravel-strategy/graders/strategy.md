---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Prioritises by risk: checkout, payments and refunds (and auth/permissions) covered first and deepest.
- Assigns levels: unit tests for pure logic (prices, discounts, tax), Laravel feature tests with a real database for most backend behaviour, a few end-to-end browser tests (for example Dusk or Playwright) for the critical journeys, and a fake or contract test for the payment gateway.
- Splits the gate: fast tests block every PR; slower end-to-end tests run on merge or nightly with an owner.
- Every production bug gets a regression test, and flaky tests are quarantined with an owner rather than skipped for good.

Pass only if every point holds.
