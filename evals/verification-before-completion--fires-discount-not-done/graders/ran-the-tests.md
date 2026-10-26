---
type: llm
focus: trace
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- The agent ran the tests in this session, and the output showed test_at_threshold failing.

Pass only if every point holds.
