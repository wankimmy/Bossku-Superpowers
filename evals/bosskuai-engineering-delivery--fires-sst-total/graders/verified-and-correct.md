---
type: llm
focus: trace
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- The tests were run in this session and the final run passed (the trace shows the command and its output).
- The tests cover an empty list, the ValueError for negative input, and half-up rounding on a value that lands exactly on a half cent.
- The implementation avoids binary-float rounding errors (for example Decimal with ROUND_HALF_UP).
- The final reply lists what was run and states anything not verified.

Pass only if every point holds.
