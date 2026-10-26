---
type: llm
focus: {"source": "file", "path": "names.py"}
---

Pass criteria:
- normalize_name returns '' for None.
- Nothing else changed: greet is untouched (string concatenation kept), and there are no new functions, renames, type hints or other rewrites.

Pass only if every point holds.
