---
type: llm
focus: {"source": "file", "path": "tags.py"}
---

Pass criteria:
- The shared mutable default list is gone (for example `tags=None` with a new list per call).
- tag_post returns only the tags passed to it in that call.

Pass only if every point holds.
