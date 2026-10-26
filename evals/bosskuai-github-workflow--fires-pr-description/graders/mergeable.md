---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- A short summary in plain terms, and `Closes #212` (or an equivalent link).
- Test evidence: what was run (the session tests, locally), without claiming CI results that were not given.
- Deploy risk: Redis must exist and REDIS_URL be set before deploy, and existing file-based sessions are lost (users logged out) at the switch.
- A rollback plan (for example revert and redeploy, noting sessions created in Redis are lost).

Pass only if every point holds.
