---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Describes the call stack as the stack of active function calls (frames), pushed on call and popped on return.
- Stays short and direct: no multi-step process, plan, review template or file changes for this simple question.

Pass only if every point holds.
