---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Explains that it replays a range of commits onto a new base, cut from an old base (for example `git rebase --onto main feature-a feature-b` moves the commits of feature-b that are not in feature-a onto main).
- Gives one example command.
- Stays short and direct: no multi-step process, plan, review template or file changes for this simple question.

Pass only if every point holds.
