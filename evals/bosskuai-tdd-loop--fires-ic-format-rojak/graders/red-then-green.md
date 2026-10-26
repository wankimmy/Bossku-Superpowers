---
type: llm
focus: trace
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- A test run happened before ic.py had a working is_valid_ic, and it failed on the missing behaviour (an assertion failure, or an import or attribute error for the not-yet-written function), not on a mistake in the test; a later run passed.
- The tests cover a valid number with dashes, a valid number without dashes, a wrong length, dashes in the wrong places, and an impossible date (for example month 13 or 30 February).

Pass only if every point holds.
