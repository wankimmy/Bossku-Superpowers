---
type: llm
focus: trace
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- The tests were run in this session and passed (the trace shows the command and its output).

Pass only if every point holds.
