---
name: bosskuai-product-verification
description: "Use when verifying real user journeys, signup/checkout flows, CLI smoke checks, or a launch and verification recipe."
---

# BosskuAI Product Verification

Verify what a user can actually do in the running product. A passing test suite is useful evidence, but does not demonstrate a browser journey, CLI invocation, or integration that was never exercised.

## How this differs from nearby skills

- `bosskuai-engineering-delivery` owns implementation and the delivery gate; this skill supplies observed product evidence.
- `e2e-testing` authors automated browser tests; this skill runs the relevant user path using available tooling.
- `bosskuai-browser-automation` drives a browser; this skill also covers CLI and service behavior.
- `bosskuai-tdd-loop` owns failing-test-first development, not release smoke checks.

## Workflow

1. Identify the changed user path and an observable success condition. Read the repo's launch/test commands, configuration requirements, and existing verification recipe.
2. Confirm the environment and test data. Use a disposable account, temporary home, or test database when the path writes state. Respect existing authorization for actions.
3. Choose the lightest real check: invoke the CLI as a user would, exercise the service boundary, or walk the browser journey. Use an installed browser tool; do not assume a tool, server, or credential exists.
4. When diagnosing a regression, capture the original failure or baseline before the fix. Record the command, inputs, expected result, and observed result.
5. Run the changed path and one adjacent path that could regress. Check relevant failure states such as invalid input, an unavailable service, or a denied permission.
6. Record exit codes, returned values, persisted effects, or screenshots when useful. Redact secrets and personal data from evidence.
7. Turn repeated checks into a project-specific recipe or automated test only when it saves recurring work. Include prerequisites, launch command, readiness signal, test inputs, cleanup, and evidence.
8. Report `passed`, `failed`, or `blocked` for each acceptance criterion. Name checks that could not run; do not substitute a unit-test pass for missing product evidence.

## Gotchas

- A healthy server or HTTP 200 does not prove the intended state change occurred; check the response and resulting state.
- A CLI smoke check using the real home can alter live agent settings. Give installers an isolated temporary home.
- Browser actions such as checkout, invitation, and deletion may have external effects. Use a test path within the authorized scope.
- A launch command copied from another project is not a verification recipe. Discover the actual repo's commands first.
- Stop or clean up only resources created for this verification; preserve the user's existing processes and data.

## Output

| Criterion | Check / environment | Expected | Observed evidence | Status |
|---|---|---|---|---|
| CLI accepts valid input | Actual CLI in a temporary home | Successful result | Exit code and resulting files | passed / failed / blocked |

State any remaining gap and the cleanup performed. Never claim product verification when only static review or unit tests ran.

## References

- `../../references/playbooks/claude-code-practices-playbook.md`
- `../../references/checklists/engineering-delivery-checklist.md`
