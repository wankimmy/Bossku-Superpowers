---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Gives a sensible starting range (around 2e-5 to 5e-5 with AdamW) and one or two practical tips (warmup, a small sweep).
- Stays short: no learned skill, intent JSON, memory note or file changes for this question.

Pass only if every point holds.
