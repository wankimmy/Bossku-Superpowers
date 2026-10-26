---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Identifies an uptime-monitoring service: an Express API that schedules repeating checks on a BullMQ (Redis) queue, and a separate worker that fetches each URL every 60 seconds and stores the status and time in Postgres.
- Says it needs two processes (`npm start` and `npm run worker`) plus Redis (REDIS_HOST) and Postgres.
- Notes gaps or risks visible in what is shown (for example no schema or migration for the results table, no URL validation, no way to list or delete monitors) without inventing files that were not shown.

Pass only if every point holds.
