---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Gives three sensible tips (for example a short imperative subject line, a body that explains why, one logical change per commit).
- Stays short and direct: no multi-step process, plan, review template or file changes for this simple question.

Pass only if every point holds.
