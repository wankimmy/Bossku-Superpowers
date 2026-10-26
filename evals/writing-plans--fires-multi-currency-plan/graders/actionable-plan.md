---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Breaks the work into ordered, small tasks, each naming the files it touches (from the list, plus new ones such as a migration or the rate model).
- Includes a data migration that sets currency to MYR for existing invoices, and states the default for new ones.
- Each task, or nearly each, says how it is tested or verified, with tests written before or with the code.
- Covers converting report totals to MYR with the daily rates, including what happens when a rate is missing for a date.

Pass only if every point holds.
