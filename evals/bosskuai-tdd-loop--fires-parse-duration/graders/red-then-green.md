---
type: llm
focus: trace
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- A test run happened before duration.py had a working parse_duration, and it failed on the missing behaviour (an assertion failure, or an import or attribute error for the not-yet-written function), not on a mistake in the test.
- A later run of the tests passed.
- The tests cover the three examples, an empty string and an unknown unit.

Pass only if every point holds.
