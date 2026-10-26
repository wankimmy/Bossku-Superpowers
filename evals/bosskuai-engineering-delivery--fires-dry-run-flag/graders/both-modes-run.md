---
type: llm
focus: trace
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Before the final reply, the trace shows the script (or a test of it) actually run in dry-run mode against sample .jpg files, with the files left unrenamed.
- The trace also shows a normal-mode run with the files renamed.

Pass only if every point holds.
