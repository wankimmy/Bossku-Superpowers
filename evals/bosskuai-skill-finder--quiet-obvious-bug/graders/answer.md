---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Says it raises ZeroDivisionError when xs is empty.
- Gives a fix (guard the empty case and return a chosen value or raise a clear error).
- Stays short and direct: no multi-step process, plan, review template or file changes for this simple question.

Pass only if every point holds.
