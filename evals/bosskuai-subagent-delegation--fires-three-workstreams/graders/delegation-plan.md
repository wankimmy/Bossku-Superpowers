---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Runs the three as separate parallel tasks and says which are read-only (the audit, the research) and which write files (the docs update), with each writer owning its own files.
- Each task brief has a concrete goal, a scope or file paths, and a check for when it is done.
- Says how results come back and are checked before being accepted (for example reviewing each report or diff against its evidence).

Pass only if every point holds.
