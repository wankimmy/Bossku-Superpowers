---
type: llm
focus: trace
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass if either holds:
- A: the agent ran a skill search (for example `bossku skills find`) before answering, and the reply names a library skill for small-business bookkeeping (such as bosskuai-bookkeeping) that appears in the search output.
- B: the search command was unavailable or failed, and the reply says so plainly instead of guessing.

Fail in either case if the reply presents a skill name that never appeared in any tool output.
