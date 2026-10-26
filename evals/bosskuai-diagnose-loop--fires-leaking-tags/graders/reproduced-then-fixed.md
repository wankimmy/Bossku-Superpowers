---
type: llm
focus: trace
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Before changing tags.py, the agent ran code (a script or a failing test) showing tags from one call appearing in a later call.
- A regression test that calls tag_post (or add_tag) twice and checks the second result has no tags from the first was added and passed in the final run.

Pass only if every point holds.
