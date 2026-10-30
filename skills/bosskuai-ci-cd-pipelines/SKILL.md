---
name: bosskuai-ci-cd-pipelines
description: "Use when designing, speeding up, or fixing CI/CD pipelines, including GitHub Actions, GitLab CI, matrices, caching, concurrency, required checks, OIDC, artifact promotion, releases, monorepo filters, secrets, and flaky-check policy; use ci-triage to classify a red run."
---

# CI/CD pipelines

For the pipeline itself: shape, speed, gates, secrets, and promotion to production. Not for classifying one red run (`ci-triage`) or the infra/runtime behind it (`bosskuai-devops-iac`).

1. **Read what exists.** List the workflow files' triggers and jobs, get a timing baseline (`gh run list --json name,startedAt,updatedAt,conclusion`, where duration is roughly `updatedAt` minus `startedAt`, or the Actions usage report). Take runtime versions from the project's own files (for example `node-version-file: .nvmrc` in `actions/setup-node`), not typed into the YAML. At work time, check each action's latest release and the runtime it targets, and read the deprecation warnings in the run log.
2. **Shape stages by trigger.** PR: lint + typecheck + unit + integration + build, parallel, under ~10 minutes. Main: PR jobs, build the artifact once, tag with the SHA, deploy staging, smoke test. Tag: release notes, production behind approval. Nightly: E2E and perf. `workflow_dispatch` for manual ops.
3. **Lock permissions and secrets first**: `permissions: contents: read` at workflow level, write scopes only where needed. Pin third-party actions to a commit SHA, use OIDC not long-lived keys, and never let a secret reach a log, fork build, or artifact. Pin runner images too (`runs-on: ubuntu-<version>`, not `ubuntu-latest`; check the current labels in the actions/runner-images README), because `latest` moves under you.
4. **Add the primitives for speed and safety**: a cache keyed on the lockfile hash, `concurrency` + `cancel-in-progress` on PR workflows only, `timeout-minutes` on every job, a path filter so a monorepo skips unaffected packages. Deploy jobs use a concurrency group per environment with `cancel-in-progress: false`: a deploy cancelled halfway through a migration leaves the database half-changed. Rollbacks use the same group name, so they never run beside a deploy. With the default `queue: single`, a newer run cancels an older pending run in that group, so check that a queued rollback was not cancelled.
5. **Wire the merge gate**: stably named required status checks (a rename silently drops protection), branch protection, a merge queue once merges are frequent. Merge only when the required checks are green on the exact head commit, and check again after every push.
6. **Promote, don't rebuild.** Build once on main, tag with the SHA, redeploy that digest. Gate migrations as their own backward-compatible step. Add a post-deploy smoke check and a rehearsed `workflow_dispatch` rollback. Run the migration on a recent anonymized copy of production data, and compare the results, before the production step. The rollback redeploys a known previous digest and never rebuilds.
7. **Give flakiness a policy**: quarantine with an owner and expiry, count retries as failures, fix the cause instead of sleeps or blanket retries.
8. **Verify.** `actionlint`, then `gh run watch <id> --exit-status`. Confirm no unpinned action, no `pull_request_target` with PR-head checkout, and every deploy has a gate and rollback.

**Local pre-commit hooks** (JavaScript repos) are a fast first gate, not a replacement for CI. Detect the package manager from the lockfile, then run a staged-files formatter (lint-staged with Prettier, using `--ignore-unknown`) first, and the full typecheck and tests after it. Leave out a typecheck or test line if the repo has no such script, and tell the user. Check the installed Husky version for the init command and hook-file format, create a formatter config only if none exists, and verify by running the staged-files step and making a test commit.

If nobody can settle a policy choice, default to the smallest safe rule: required checks on main, no merge queue, zero blanket retries, and say so in one line.

Stack presets, the Actions rules list, secrets detail, and the output template: `reference.md`.

Shared bar for merge gates and release checks: `../../references/checklists/engineering-quality-bar.md`.

Pre-commit hook note adapted in part from misc/setup-pre-commit (skills pack by Matt Pocock, MIT).
