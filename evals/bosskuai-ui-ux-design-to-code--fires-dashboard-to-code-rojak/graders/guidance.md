---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Breaks it into components (header with the export action, KPI card, sales chart, recent orders table, status pill) with the data each needs.
- Lists the states for the data-driven parts: loading (skeleton), empty (no orders or sales yet), error with retry, and export in progress.
- Says how it adapts on a phone: KPI cards stack or go two per row, the table becomes cards or scrolls sideways, and the chart stays readable.

Pass only if every point holds.
