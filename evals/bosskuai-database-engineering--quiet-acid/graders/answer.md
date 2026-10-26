---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Atomicity, Consistency, Isolation, Durability, each with a correct one-line meaning.
- Stays short and direct: no multi-step process, plan, review template or file changes for this simple question.

Pass only if every point holds.
