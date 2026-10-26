---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- git revert adds a new commit that undoes earlier changes (safe on shared history).
- git reset moves the branch pointer back (rewrites history; --hard also discards local changes).
- Stays short and direct: no multi-step process, plan, review template or file changes for this simple question.

Pass only if every point holds.
