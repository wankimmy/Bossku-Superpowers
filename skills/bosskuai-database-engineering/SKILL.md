---
name: bosskuai-database-engineering
description: "Use when SQL or NoSQL database design affects correctness or scale (MariaDB, MySQL, PostgreSQL, SQLite, MongoDB): indexing, query plans, transactions and locking, safe online migrations, constraints, multi-tenant schemas, connection pooling, backups."
---

# Database engineering

Use when schema, indexes, query plans, locking, or a migration affects correctness or scale.

1. **Orient before changing anything**: engine and version — confirm tests run on the *same* engine, not SQLite standing in for MySQL/PostgreSQL — the live schema and migration history, existing indexes and their usage stats, and the top queries by total time.
2. **Name the invariant you're protecting** and encode it in the database as a unique or check constraint, not only in application code.
3. **Get the plan before touching an index.** `EXPLAIN`/`EXPLAIN ANALYZE` first; a query is not "fast" or "slow" without one, before or after.
4. **Design composite indexes equality columns first, then the range column, then `ORDER BY`**; lead every tenant-scoped index with `tenant_id`; check selectivity before adding; remove unused and duplicate indexes.
5. **Never run a whole-table `UPDATE` or a locking DDL directly against a production-sized table.** Use expand → chunked backfill → non-locking constraint → switch reads → contract, and state each step's lock impact and rollback.
6. **Scope every tenant query and composite index by `tenant_id`**, and check ownership on update/delete, not only on read.
7. **Re-run the plan after the change** and compare before/after; confirm backups and the restore path still work if schema changed.

Check before you finish: tests ran on the production engine or the gap is stated, every new foreign key on PostgreSQL has an explicit index, no invariant lives only in app code, and no migration shipped without a stated rollback.

Index and plan-reading detail, the full online-migration ladder, multi-tenancy shapes, and the operational baseline: `reference.md`.
