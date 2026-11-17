# Full guide

The short version is in SKILL.md. Read this file only when the job needs the detail.


# BosskuAI QA Automation Strategy

Use this skill when deciding **what to test, at which level, and what gates a release** — not when writing one specific test.

## How this differs from nearby skills

- **`test-driven-development` / `bosskuai-tdd-loop`**: drive a single unit of code test-first; this skill designs the suite above them.
- **`bosskuai-integration-testing`**: designs contracts and test doubles at module seams; this skill allocates effort across all levels.
- **`bosskuai-browser-automation`**: drives a browser for a task; this skill decides when a browser test is worth its cost.
- **`bosskuai-laravel-verification`**: Laravel-specific verification commands; this skill is framework-neutral.

## Allocate by risk, not by coverage percentage

Start from the flows where failure is expensive: authentication, payments, permissions and tenancy, data deletion, and anything that sends money or mail. Cover those deeply. Coverage percentage is a weak target; an untested refund path at 90% coverage is still an untested refund path.

## Choose the cheapest level that can catch the bug

- **Unit**: pure logic, calculations, state machines, edge-case branches. Fast, run on every change.
- **Feature/integration**: the level most backend invariants belong at — real database, real routing, faked third parties. Best value per test.
- **Contract**: the boundary with an external service, so an upstream change fails locally rather than in production.
- **End-to-end**: only for genuine cross-page or cross-system journeys. Slowest and most brittle; keep the set small and stable.

Push a test down a level whenever the same bug would be caught there.

## Output format

```text
Risk map: [flow] - [failure cost] - [current coverage]

Recommended allocation:
  Unit: [what belongs here]
  Feature/integration: [what belongs here]
  Contract: [external boundaries]
  E2E: [the short list]

Gaps:
  P0/P1/P2 - [untested risk] - [test to add] - [level]

CI gates: [what blocks PR / what runs nightly]
Flake risks: [sources of nondeterminism found]
Verification: [suite actually run, and result]
```

## References

- `../../references/checklists/qa-automation-strategy-checklist.md`
