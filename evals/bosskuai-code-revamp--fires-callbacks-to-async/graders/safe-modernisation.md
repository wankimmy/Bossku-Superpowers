---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Uses async/await with fs.promises (or util.promisify) inside.
- Keeps readConfig and loadPort exported under the same names, and deals with existing callback callers: either still accepts an optional callback, or clearly flags that returning promises breaks callers and shows how to migrate them.
- Keeps behaviour: the 'Invalid config: ' error wrapping and the 3000 default port.
- Says how to check it (for example tests for a missing file, invalid JSON and a missing port).

Pass only if every point holds.
