# Code Review Checklist

> Label assumptions and carry on. Ask the user only when a missing input blocks the verdict (then the result is "provisional (missing: <input>)"), with numbered yes/no or A/B questions.

Use alongside `bosskuai-rigorous-code-review`. Work through every section; none is skipped (a section that cannot apply is marked "not applicable: <reason>"). The full bar (requirements, versions, scenarios, production data, API integrations, deploy, proof) is [engineering-quality-bar.md](engineering-quality-bar.md); run it too.

## Graph-aware preflight

- [ ] If `code-review-graph` MCP tools are available, start with `get_minimal_context_tool(task="review changes", base=<base>)`.
- [ ] If graph state is missing or stale, run `build_or_update_graph_tool(postprocess="minimal")` before relying on impact data.
- [ ] Use `detect_changes_tool(detail_level="minimal")` to identify risk, blast radius, and test gaps before broad file reads.
- [ ] For high-risk functions or shared modules, query callers, tests, importers, and affected flows.
- [ ] Confirm every blocking finding by reading the actual source and tests; do not treat graph inference as proof.

## Intended outcome and impact

- [ ] Is the intended outcome stated (request, PR description), with anything deliberately deferred set aside?
- [ ] Does the change provide the mechanism for that outcome, or only describe it?
- [ ] Are the consumers checked: callers, existing data and roles, the agent or person who must load or follow a doc or rule?
- [ ] Could it pass every existing check and still miss its purpose (rule never loaded, grant only on a fresh database, partial deploy)? Only report a path you can support.
- [ ] Is each finding marked reproduced, traced or inferred, and CI results kept apart from checks you ran yourself?

## Correctness

- [ ] Does the change do what it claims in the PR description?
- [ ] Are edge cases handled: null/undefined/empty, zero, negative, max values?
- [ ] Are concurrency risks addressed: race conditions, shared mutable state, ordering?
- [ ] Is partial failure handled correctly — no silent data corruption on error?
- [ ] Is idempotency preserved where expected (retries won't cause duplicates)?
- [ ] Are all return paths and error branches reachable and correct?

## Security

- [ ] Is all input validated and sanitized at every trust boundary?
- [ ] Are there injection risks: SQL, shell, LDAP, template, path traversal, deserialization?
- [ ] Are authentication and authorization checks in place and enforced consistently?
- [ ] Are secrets and credentials free from hardcoding, logging, and error-response leakage?
- [ ] Is cryptography using current recommended algorithms and key sizes?
- [ ] Are web surfaces protected from CSRF, XSS, and open redirects?
- [ ] Is there appropriate rate limiting on abuse-prone endpoints?
- [ ] Are sensitive operations logged (without leaking PII or secrets)?

## Performance & resources

- [ ] Are there N+1 queries or unbounded API calls inside loops?
- [ ] Are memory allocations bounded under load?
- [ ] Is blocking I/O kept off hot or latency-sensitive paths?
- [ ] Are DB queries using appropriate indexes (no full-table scans on large datasets)?
- [ ] Are caching assumptions validated — does cache invalidation hold?
- [ ] Are there potential lock contention or deadlock paths?

## Test coverage

- [ ] Does the change include tests for new behavior?
- [ ] Are failure paths and edge cases covered by tests?
- [ ] Do tests exercise the real code path, not mocked-away behavior that masks real bugs?
- [ ] Are existing tests still meaningful after this change (not accidentally passing)?
- [ ] Are integration or E2E tests needed given the risk level of this change?

## API contracts & backwards compatibility

- [ ] Does this change break any existing callers (internal or external)?
- [ ] Are schema changes additive-only, or do they remove/rename fields?
- [ ] Is versioning required for public or third-party-consumed contracts?
- [ ] Are deprecations communicated through code, docs, or migration guides?
- [ ] Are response shapes and status codes consistent with the existing API surface?

## Operational concerns

- [ ] Is logging useful, structured, and free from sensitive data?
- [ ] Are metrics or traces emitted so on-call can observe this in production?
- [ ] Is the migration path safe: DB migrations backwards-compatible, rollback tested?
- [ ] Is a feature flag or gradual rollout strategy in place for high-risk changes?
- [ ] Is the deployment order correct (avoid DB column removal before code removal)?

## Maintainability

- [ ] Does the change fit the existing module structure and naming patterns?
- [ ] Are responsibilities in the right layer (no logic leaking into the wrong layer)?
- [ ] Is the change the smallest safe fix, or is it larger than necessary?
- [ ] Are abstractions stable and non-accidental?
- [ ] Are error messages and logs actionable for future developers?

## AI/LLM-generated code markers

- [ ] Are all library methods and APIs real (not hallucinated)?
- [ ] Is error handling specific and actionable, not generic catch-all swallowing?
- [ ] Does validation match the actual domain logic, not generic placeholder checks?
- [ ] Does the naming and style match the project's conventions consistently?
- [ ] Is the logic proportionate to the problem, or is it over-engineered boilerplate?

## Business logic, data and deploy

- [ ] Do the new rules clash with existing flows, roles or data, and was every scenario walked by who, what, when, the record's state and each dependency? (bar section 3)
- [ ] Was the change run on a masked production data copy, with production data types, and do counts and results match what deploy should give? (bar section 4)
- [ ] Does it deploy with zero downtime, with queued jobs, cache formats and config ready, and is the rollback safe for data written after deploy? (bar section 6)

## UI/UX and PR scope

- [ ] Was every screenshot and template read state by state as a user would (empty, loading, error, success, disabled)?
- [ ] Is any message, warning or label wrong for its state, contradicting the result, or leaving the user unsure what happened? That is a finding to fix, not a nit (severity per the UI/UX rule in skills/bosskuai-rigorous-code-review/reference.md, step 4).
- [ ] Does each disabled control say why, and does the same thing use the same words everywhere?
- [ ] Does every file in the diff belong to the change? Agent working files (superpowers plans, `docs/work-items` notes, handoffs, scratch scripts, logs, local config) are a finding unless the repo keeps them on purpose, and then they must be current.
