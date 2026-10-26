---
type: llm
focus: trace
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- A test with a partial last page (for example 5 items with size 2 gives 3 pages, the last being one item) ran and passed.

Pass only if every point holds.
