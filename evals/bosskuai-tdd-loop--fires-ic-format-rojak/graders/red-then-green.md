---
type: llm
focus: trace
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- A test run failed before ic.py had a working is_valid_ic (on the missing behaviour, not a test mistake), and a later run passed.
- The tests cover a valid number with dashes, a valid number without dashes, a wrong length, dashes in the wrong places, and an impossible date (for example month 13 or 30 February).

Pass only if every point holds.
