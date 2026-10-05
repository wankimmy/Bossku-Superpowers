---
name: bosskuai-rigorous-code-review
description: "Use for PR or pre-merge review, adversarial review, or challenging an implementation. A skeptical expert review that maps changes to repo structure, applies strict engineering standards and prefers minimal fixes."
---

# Rigorous code review

Assume the change is wrong until the code, tests and callers show otherwise. Review the change, do not rewrite the system.

1. **Read the evidence, not just the diff:** the callers, the tests, the types or schemas, and the config or infra it touches.
2. **Go through each category** and skip one only when it clearly does not apply:
   - correctness: edge and boundary values, empty and null, ordering, concurrency, idempotency, partial failure, retries
   - security: validation at every trust boundary, injection, authorization on every path, secrets, error leaks
   - performance: queries in loops, unbounded growth, blocking calls on hot paths, missing indexes
   - tests: the new behaviour, the failure paths and the bug path are covered, and the tests exercise real behaviour
   - compatibility: existing callers, schema and API changes, deprecations
   - operations: logs and metrics that help, migrations and rollback
3. **Report only what you can point to.** Every finding has a file:line, the evidence, a severity (P0 blocks, P1 must fix, P2 should fix, P3 nit) and the smallest fix. Drop findings you cannot support; do not pad.
4. **Escalate scope** (a larger refactor) only when a small fix cannot work, and say why.

Verdict first: approve, request changes, or block. Then the findings, most severe first. If the diff is clean, say so in one line. The full checklists, confidence scoring and optional tool integrations: `reference.md`.
