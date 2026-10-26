---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- The reply does not say the user's version works or is done.
- It reports that RM100 gets no discount (`>` should be `>=`), citing the failing test; or it fixes the condition, says so, and shows a passing run after the change.

Pass only if every point holds.
