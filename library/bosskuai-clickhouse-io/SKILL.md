---
name: bosskuai-clickhouse-io
description: "Use when the task explicitly concerns clickhouse io. ClickHouse database patterns, query optimization, analytics, and data engineering best practices for high-performance analytical workloads. Use when writing ClickHouse schemas or queries, or when an analytical query is too slow."
metadata:
  origin: ECC-adaptation
---

# ClickHouse Analytics Patterns — portable workflow

ClickHouse database patterns, query optimization, analytics, and data engineering best practices for high-performance analytical workloads. Use when writing ClickHouse schemas or queries, or when an analytical query is too slow.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-postgres-patterns`, `bosskuai-web-performance`, `bosskuai-software-architecture`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Overview.
2. Table Design Patterns.
3. MergeTree Engine (Most Common).
4. ReplacingMergeTree (Deduplication).
5. AggregatingMergeTree (Pre-aggregation).
6. Query Optimization Patterns.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: run `SELECT version()` on the target server, and read the client library version from its lockfile. Check the latest stable release and its changelog at clickhouse.com at work time, and use only APIs present in the installed version. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Apply the source “Overview”, “Table Design Patterns” guidance to the concrete request. Return the resulting clickhouse analytics patterns artifact or diagnosis with source/command evidence for each conclusion.

- Type traps: money in `Decimal`, never `Float64`, even where a source example uses `Float64` for a column that holds money. ClickHouse JSON output quotes 64-bit integers as strings by default, so check how the client parses them.
- Concurrency and duplicates: `ReplacingMergeTree` removes duplicates only when parts merge. Use `FINAL` or `argMax` where a duplicate would change the answer, and never assume a row is unique right after an insert.
- Zero downtime: `ALTER TABLE ... UPDATE` and `ALTER TABLE ... DELETE` run as background mutations, so watch `system.mutations` until they finish. For a new sort key, build a new table, backfill in chunks, and switch reads.
- Full quality bar: `../../references/checklists/engineering-quality-bar.md`.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
