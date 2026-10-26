---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- A race condition: the result depends on the timing or interleaving of concurrent access to shared state.
- A deadlock: two or more threads each wait for something the other holds, so none can continue.
- Stays short and direct: no multi-step process, plan, review template or file changes for this simple question.

Pass only if every point holds.
