---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Gives a verdict that does not approve (request changes or block).
- Flags the SQL injection from the f-string and gives the parameterised fix.
- Flags that any logged-in user can read any order (no ownership check against the current user).
- Flags the crash or 500 when no row is found (dict(None)) and says it should return 404.

Pass only if every point holds.
