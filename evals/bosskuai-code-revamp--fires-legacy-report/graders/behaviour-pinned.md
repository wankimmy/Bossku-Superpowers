---
type: llm
focus: trace
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Before report.py was refactored, tests capturing its current output were written and run (paid and refunded orders, an order with another status, and each currency including an unknown one).
- The same tests passed after the refactor.

Pass only if every point holds.
