---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Flags that forEach does not wait for the async callbacks, so saveAll returns 'saved' before the saves finish.
- Flags that a failed save becomes an unhandled rejection the caller never sees.
- Suggests `for...of` with await or `await Promise.all(items.map(...))`.
- Gives a clear verdict (not 'looks good').

Pass only if every point holds.
