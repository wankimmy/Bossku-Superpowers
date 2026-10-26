---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Identifies the N+1 query: o.customer runs one extra query per order (up to 500).
- Fixes it with select_related('customer') (or fetching only the needed fields) in one query.
- Proves it with a before-and-after measurement: the query count (for example django-debug-toolbar, assertNumQueries or connection.queries) and the response time on the same data.

Pass only if every point holds.
