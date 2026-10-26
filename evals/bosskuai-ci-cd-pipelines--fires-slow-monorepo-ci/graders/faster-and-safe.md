---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Caches dependencies keyed on the lockfile (for example setup-node `cache: npm`) and uses `npm ci` instead of `npm install`.
- Splits lint, test and build into parallel jobs or a matrix, and runs only the packages affected by the change (path filters or an affected-packages tool).
- Adds `concurrency` with `cancel-in-progress` for PR runs, and `timeout-minutes` on jobs.
- Mentions at least one safety point: least-privilege `permissions`, pinning third-party actions, or keeping required status check names stable.

Pass only if every point holds.
