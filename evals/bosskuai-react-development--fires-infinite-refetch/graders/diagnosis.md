---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Explains that params is a new object on every render, so the effect runs after every render and setOrders triggers the next one: a loop.
- Fixes it by depending on the primitive values (page, and the constant size) or memoising params, and does not suggest silencing the exhaustive-deps lint rule.
- Handles the race when page changes quickly (an AbortController or ignore flag) or suggests a data-fetching library such as TanStack Query.

Pass only if every point holds.
