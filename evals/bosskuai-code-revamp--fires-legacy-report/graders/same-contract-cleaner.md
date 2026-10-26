---
type: llm
focus: {"source": "file", "path": "report.py"}
---

Pass criteria:
- build_report(orders) keeps its name and signature.
- The duplicated currency conversion now lives in one place (a helper or a lookup table).
- The output format is unchanged: an unknown currency still counts as 0, refunds keep the '-' prefix, and the TOTAL line is still last.

Pass only if every point holds.
