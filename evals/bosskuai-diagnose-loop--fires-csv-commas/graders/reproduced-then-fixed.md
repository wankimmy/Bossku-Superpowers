---
type: llm
focus: trace
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Before the fix, the agent reproduced the split with a name that contains a comma.
- A test with such a name passed in the final run.

Pass only if every point holds.
