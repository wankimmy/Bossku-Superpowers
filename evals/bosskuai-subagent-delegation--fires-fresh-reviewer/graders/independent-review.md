---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Gives the reviewer the code or diff and the requirements, not the author's conclusions or reasoning.
- Keeps the reviewer read-only and scoped: which files or diff, and what to check (for example auth bypass, session handling, missing tests).
- Asks for findings with evidence (file:line, severity) and says the author checks each finding before acting on it.

Pass only if every point holds.
