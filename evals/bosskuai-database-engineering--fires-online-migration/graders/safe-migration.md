---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Expand and contract: add the column as nullable, deploy code that writes tenant_id, backfill existing rows in small batches, then enforce NOT NULL.
- Enforces NOT NULL without a long lock, for example a CHECK (tenant_id IS NOT NULL) NOT VALID constraint, VALIDATE it, then SET NOT NULL.
- Builds any index with CREATE INDEX CONCURRENTLY, and sets a lock_timeout for the DDL.
- States a rollback or back-out path.

Pass only if every point holds.
