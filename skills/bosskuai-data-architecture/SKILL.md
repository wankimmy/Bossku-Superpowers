---
name: bosskuai-data-architecture
description: Use when you need data modeling, schema boundaries, migrations, warehouses, analytics pipelines, entity ownership, retention, and correctness tradeoffs in data-intensive systems.
---

# BosskuAI Data / Schema Architecture

Use this skill when the main question is **how data should be shaped, owned, migrated, or analyzed** across the system.

## How this differs from nearby skills

- **`bosskuai-software-architecture`**: decides broader component and service boundaries; this skill focuses on the structure and lifecycle of the data itself.
- **`bosskuai-business-logic-review`**: checks whether rules are correct; this skill checks whether schemas and pipelines support those rules safely.
- **`bosskuai-engineering-delivery`**: implements migrations or models; this skill decides the right data direction first.
- **`bosskuai-database-engineering`**: indexes, plans, locking, and online-migration mechanics; this skill decides ownership, lifecycle, and pipelines.

## Mindset

- Schema changes are product changes with operational consequences.
- Data ownership must be explicit or consistency drifts silently.
- Additive migration paths beat big-bang rewrites.
- Analytics pipelines are production systems too, not harmless reporting glue.

## Data lenses

**Entity ownership**
- Which system owns each entity and field?
- Are there overlapping writers?
- Which fields are source of truth versus derived?

**Model shape**
- Is normalization helping or hurting the current workflows?
- Are invariants encoded in schema, app logic, or both?
- Are soft deletes, status flags, and historical records modeled intentionally?

**Migration safety**
- Can the change roll out additively?
- What is the backfill strategy?
- What happens during mixed-version deployments?

**Operational performance**
- Are hot queries and indexes aligned with access patterns?
- Are partitioning, archival, or denormalization required?
- Does the design create hidden N+1 or scan-heavy behavior?

**Analytics and pipeline correctness**
- Is event or metric grain explicit?
- Are transformations reproducible and idempotent?
- Are late-arriving events, replays, and backfills handled safely?

**Privacy and retention**
- What data is sensitive or regulated?
- What should expire, archive, or remain immutable?
- Can deletion and subject-access flows be honored?

## Workflow

1. **Read the current data surface** — schema files, migrations, models, ORM code, warehouses, event specs, and high-signal queries or tests. Read the engine version from the live database (`SELECT VERSION();`), not from the docs, and the migration tool's version from its lockfile.
2. **Map entity ownership and lifecycle** — source of truth, derived copies, historical records, deletion behavior, and downstream consumers.
3. **Design for migration safety** — additive changes, backfills, feature flags, dual reads/writes, and rollback path.
4. **Review access patterns** — read/write hotspots, indexes, partitions, fan-out, and reporting needs.
5. **Review pipeline semantics** — event grain, dedupe, idempotency, reprocessing, and data freshness expectations.
6. **Review retention/privacy obligations** — PII, redaction, archival, and deletion obligations.
7. **Recommend the smallest safe data evolution path** — what to migrate now, what to defer, and what to protect with verification.

## Guardrails

- Do not treat analytics tables as a free dumping ground with no ownership.
- Do not recommend destructive schema changes without an additive transition path.
- Do not mix transactional source-of-truth needs with reporting convenience blindly.
- Do not ignore privacy and retention implications when copying data to new systems.
- In tenant-owned tables, do not write a unique key without `tenant_id`, or one tenant blocks another's value. Keep a key global only when the value must be unique across all tenants. On a table with soft deletes, a plain unique key on `email` also blocks a new row after a delete. Use a partial unique index instead (PostgreSQL: `WHERE deleted_at IS NULL`). MySQL has no partial index, so add a stored generated column that keeps the value only while the row is live, `email_live AS (CASE WHEN deleted_at IS NULL THEN email END) STORED`, and make the unique key `(tenant_id, email_live)`. MySQL lets a unique key hold many NULLs, so deleted rows do not block a new row.
- Do not add an enum or status value in the same release that writes it. Readers that do not know the value fail first, so ship the readers first.
- Do not store dates past 2038 in MySQL `TIMESTAMP`, which stops there. Use `DATETIME` in UTC by convention, or `timestamptz` in PostgreSQL.
- Do not copy production data for testing or analytics without masking personal fields, and keep the copy off public hosts.

## Output format

```text
Data summary:
  Core entities: [list]
  Ownership: [who owns what]
  Current storage/pipeline shape: [summary]
  Engine and version: [from the live database, date checked]

Schema and pipeline risks:
  Modeling: [findings]
  Migrations: [findings]
  Performance: [findings]
  Analytics pipelines: [findings]
  Privacy/retention: [findings]

Recommended evolution path:
  [change] — [why] — [rollout / backfill / rollback]

Open invariants to protect:
  [invariant] — [where to enforce]
```

## References

- `../../references/checklists/data-architecture-checklist.md`
- `../../references/checklists/engineering-quality-bar.md`
