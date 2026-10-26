---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Defines a code smell as a surface sign of a deeper design problem (not a bug in itself).
- Gives one example, such as a very long function or duplicated code.
- Stays short and direct: no multi-step process, plan, review template or file changes for this simple question.

Pass only if every point holds.
