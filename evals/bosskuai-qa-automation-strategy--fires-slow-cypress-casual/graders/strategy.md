---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Moves most checks down to cheaper levels (unit, API or component tests) and keeps a small end-to-end set for critical journeys.
- Fixes determinism: no fixed sleeps, seeded or isolated test data, no dependence on test order or live third-party services.
- Quarantines flaky tests with an owner and a deadline, and treats re-runs as failures instead of normal.
- Speeds up what remains (parallel runs or sharding, with the full suite on merge or nightly).

Pass only if every point holds.
