---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Says what is done and what is not, with the file paths.
- Keeps the date-fns decision and its reason.
- Gives ordered steps with concrete targets: add from/to to /api/reports/sales, wire the picker into src/app/reports/page.tsx, test the empty range.
- Flags the empty-range case as not yet tested.

Pass only if every point holds.
