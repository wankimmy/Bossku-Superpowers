---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Classifies it as flaky (intermittent) because the same commit both passed and failed, while noting that the changing total points to real nondeterminism to find (for example dates or time zones, ordering, randomness or shared test data).
- Does not jump to changing the checkout code; recommends finding the nondeterminism and tracking or quarantining the test with an owner, rather than re-running until green.

Pass only if every point holds.
