---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Names the failing step (npm ci, the dependency install) and classifies it as an environment or network problem (a registry timeout), not a code regression.
- Says no code change is needed: re-run the job, and if it repeats check the registry status or runner network, or escalate.
- Does not propose editing application code or tests.

Pass only if every point holds.
