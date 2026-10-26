---
name: bosskuai-gaussdb
description: "Use when designing or tuning Huawei GaussDB OLTP (not DWS, not GaussDB for MySQL or openGauss): distribution keys, co-located joins, UStore vs AStore, partitioning, EXPLAIN streaming operators, safe migrations."
---

# BosskuAI GaussDB

Use this skill for schema design and query tuning on GaussDB OLTP, distributed or centralized edition. Confirm the exact product first; sibling products behave differently.

## How this differs from nearby skills

- **`bosskuai-database-engineering`**: engine-neutral design, indexes, transactions, and online migrations. Use it for the general rules; this skill adds GaussDB distribution and streaming concerns.
- **`bosskuai-postgres-patterns`**: PostgreSQL patterns. GaussDB has PostgreSQL lineage but its own syntax and distributed behaviour, so verify against Huawei's docs.
- **`mysql-patterns`**: MySQL and MariaDB. GaussDB for MySQL is a different product and out of scope here.
- **`bosskuai-data-architecture`**: modeling and ownership across systems.
- **`bosskuai-government-digital-presales-consultant`**: where GaussDB appears as a domestic-database option in bids.

## Step 0: identify the product

- Is it GaussDB (own kernel) in the distributed edition (coordinator, data nodes, transaction manager) or the centralized primary-standby edition? Is it instead GaussDB(DWS), GaussDB for MySQL, or openGauss? If unclear, ask before answering.
- Record the version. Syntax, defaults (including the default storage engine), and feature limits vary. Check the current official documentation for that version.

## Workflow

1. Distribution (distributed edition): pick a distribution key with high cardinality and few NULLs, shared by tables that join often, to allow co-located joins. Small, frequently joined dimension tables may suit replication. Avoid keys that cause skew.
2. Storage engine: choose between in-place-update and append-style engines based on update versus insert-heavy workload. Confirm syntax and defaults for your version.
3. Partitioning: align the partition key with the distribution design so pruning and local execution both apply. Check supported partition types in your version.
4. Indexes: index foreign keys and common filter/sort columns; check what global versus local indexes mean in your edition.
5. Query plans: run EXPLAIN ANALYZE and read the streaming operators (broadcast, redistribute, none). Heavy broadcast of large tables is a red flag; co-located joins need no streaming. Compare estimated and actual rows, and refresh statistics after big data changes.
6. Application side: use connection pooling to the coordinator nodes, avoid N+1 round trips, fetch only needed columns.
7. Migrations: DDL on distributed tables touches all nodes. Test on a copy, plan a maintenance window for large tables, check which concurrent-index options your edition supports, and write a rollback.
8. Monitoring: use the version's documented system views for session and statement statistics.

## Guardrails

- Do not apply generic PostgreSQL advice without checking GaussDB documentation for the version in use.
- Do not run DDL, data changes, or parameter changes on a production cluster without explicit user approval and a rollback.
- Size thresholds (for example which tables count as "small") depend on the cluster; measure instead of copying numbers.
- Treat availability and recovery claims (RPO/RTO) as deployment facts to confirm, not defaults.

## Output format

```text
Product / edition / version: [..]
Workload: [read/write mix, joins, growth]
Design: [distribution key, engine, partitioning, indexes - reasons]
Plan findings: [streaming operators, scans, row-estimate gaps]
Change and rollback: [DDL, window, undo]
Verification: [EXPLAIN before/after, latency]
```

Adapted from agency-agents/engineering/engineering-gaussdb-expert.md (agency-agents, MIT).
