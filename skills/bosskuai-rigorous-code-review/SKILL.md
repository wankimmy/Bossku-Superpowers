---
name: bosskuai-rigorous-code-review
description: "Use when doing PR or pre-merge review, adversarial review, or challenging an implementation, a docs or rules change, or a plan: skeptical expert review of correctness, intended outcome and downstream impact that prefers minimal fixes."
---

# Rigorous code review

Assume the change is wrong until the code, tests and callers show otherwise. Review the change, do not rewrite the system. A review request allows analysis only: do not edit files, post comments or submit a review unless asked, and keep any reproduction in a scratch copy (no installers or machine-wide changes).

1. **State the intended outcome** from the request or PR description, and what is deliberately deferred. If intent is unclear, label your assumption and carry on.
2. **Read the evidence, not just the diff:** the callers, the tests, the types or schemas, and the config or infra it touches.
3. **Go through each category** and skip one only when it clearly does not apply:
   - correctness: edge and boundary values, empty and null, ordering, concurrency, idempotency, partial failure, retries
   - security: validation at every trust boundary, injection, authorization on every path, secrets, error leaks
   - performance: queries in loops, unbounded growth, blocking calls on hot paths, missing indexes
   - tests: the new behaviour, the failure paths and the bug path are covered, and the tests exercise real behaviour
   - compatibility: existing callers, schema and API changes, deprecations
   - operations: logs and metrics that help, migrations and rollback
4. **Check the outcome and who is affected** (a short pass, sized to the risk): does the change provide the mechanism for the result it promises, or only describe it? Who or what has to use it: callers, existing data and roles, an agent that must load a rule or doc? How could it pass every check and still miss its purpose? Green CI shows the behaviour the checks cover, not adoption.
5. **Report only what you can point to.** Every finding has a file:line, the evidence, a severity (P0 blocks, P1 must fix, P2 should fix, P3 nit), how you verified it (ran it, traced it, inferred it) and the smallest fix. Keep confirmed defects and unmet explicit requirements apart from optional improvements. Drop findings you cannot support; do not pad, and do not invent a recommendation quota.
6. **Escalate scope** (a larger refactor) only when a small fix cannot work, and say why.

Verdict first: approve, approve with nits, request changes, or block. Then the outcome and impact in a line, the findings most severe first, any material recommendation (smallest change, how to check it, this PR or a follow-up), and the checks you ran, with your local runs kept apart from external CI. If the diff is clean, say so briefly and still say what the evidence does not show. The full checklists, confidence scoring and optional tool integrations: `reference.md`.
