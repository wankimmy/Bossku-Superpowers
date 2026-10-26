---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- The reply cites the evidence (for example that the 3 tests passed) rather than a bare 'looks good'.
- It names at least one limit of what was checked (for example names in Chinese or Tamil script become 'item', or that nothing was pushed or run in CI).

Pass only if every point holds.
