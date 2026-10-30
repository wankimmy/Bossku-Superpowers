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

1. Identify the changed user path and an observable success condition. Read the repo's launch/test commands, configuration requirements, and existing verification recipe. Record which build you tested (commit SHA or version string), so the evidence matches what ships.
2. Confirm the environment and test data. Use a disposable account, temporary home, or test database when the path writes state. Respect existing authorization for actions. For a path that reads or writes real records, use a copy of production data. Ask the user to prepare one if none exists. Before you run anything, check that personal data is masked and that email, SMS, payment and webhook calls are switched off. Delete the copy when the test ends. Clean temporary data hides nulls and legacy rows.
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
- A double submit or a retry after a timeout must make exactly one result. On a test path within the authorized scope, send the action twice, then check that only one result exists.
- After a deploy, confirm the live build is the one you tested (version string, commit SHA or a build field in the API) before you call it verified.

## Output

| Criterion | Check / environment | Expected | Observed evidence | Status |
|---|---|---|---|---|
| CLI accepts valid input | Actual CLI in a temporary home | Successful result | Exit code and resulting files | passed / failed / blocked |

State any remaining gap and the cleanup performed. Never claim product verification when only static review or unit tests ran.

## References

- `../../references/playbooks/claude-code-practices-playbook.md`
- `../../references/checklists/engineering-delivery-checklist.md`
- `../../references/checklists/engineering-quality-bar.md`

## Production readiness pass ("what breaks in prod?")

Use when asked whether something is ready to ship. Green CI is not readiness. Build it from local, user-authorized evidence only: do not upload repo contents to an outside service or run unpinned remote scanners unless the user approves that tool and data flow. This is engineering triage, not a compliance certification.

- Gather evidence first: branch state and recent log, diff against the base branch, CI workflows and release scripts, deploy files, routes/webhooks/auth middleware, workers and cron, migrations, env documentation and startup checks, health checks and error reporting, rollback/backfill notes, E2E coverage of the launch-critical paths.
- Look through these lenses: server-side auth and public/admin route separation; secrets kept out of client bundles and logs; rate limits, CSRF, CORS, upload validation; migrations that run forward cleanly with a rollback plan; idempotent retries for writes, jobs and webhooks; webhook signatures verified before trusting the payload, with replay, duplicate and out-of-order delivery handled; test and live credentials separated; clean-checkout startup with fail-fast env validation; a health check that proves dependencies are reachable; mobile and loading/empty/error/denied states on critical paths.
- Treat as ship blockers: missing auth on sensitive data, non-idempotent payment or fulfillment webhooks, migrations that cannot run safely, exposed secrets, no rollback path for a high-impact release. A red CI or an untested launch-critical path caps the verdict at "ship with caveats".
- Report one lead sentence with the verdict and the top two risks, then: blockers, next fixes, evidence checked, evidence missing, and one concrete next action. Never give a verdict without naming the evidence behind it.

Adapted in part from ECC skills/production-audit (affaan-m/ECC, MIT).
