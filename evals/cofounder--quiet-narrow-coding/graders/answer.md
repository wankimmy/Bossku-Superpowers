---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Gives a correct one-liner such as `new Map(users.map(u => [u.id, u]))` or an equivalent.
- No business, product or strategy discussion.
- Stays short and direct: no multi-step process, plan, review template or file changes for this simple question.

Pass only if every point holds.
