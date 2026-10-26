---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Recommends a composite index with the equality column first and the range/sort column second: (status, created_at).
- Says to confirm with EXPLAIN before and after.
- Mentions a cost or caveat worth checking (extra write cost, low selectivity of status, or SELECT * versus the columns actually needed).

Pass only if every point holds.
