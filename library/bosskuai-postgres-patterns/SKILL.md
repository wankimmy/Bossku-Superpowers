---
name: bosskuai-postgres-patterns
description: "Use when the task explicitly concerns postgres patterns. PostgreSQL database patterns for query optimization, schema design, indexing, and security. Based on Supabase best practices. Use when designing PostgreSQL schemas, indexes, or RLS policies, or when a query is too slow."
metadata:
  origin: ECC-adaptation
---

# PostgreSQL Patterns — portable workflow

PostgreSQL database patterns for query optimization, schema design, indexing, and security. Based on Supabase best practices. Use when designing PostgreSQL schemas, indexes, or RLS policies, or when a query is too slow.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-clickhouse-io`, `mysql-patterns`, `bosskuai-jpa-patterns`, `bosskuai-software-architecture`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Quick Reference.
2. Index Cheat Sheet.
3. Data Type Quick Reference.
4. Common Patterns.
5. Anti-Pattern Detection.
6. Configuration Template.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: run `SELECT version();` on the target database (not only on a local copy), and read the driver version from the lockfile. Check the latest supported PostgreSQL release and its end-of-life dates at postgresql.org/support/versioning at work time, and use only APIs present in the installed version (for example, `MERGE` needs PostgreSQL 15 or later). A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Apply the source “Quick Reference”, “Index Cheat Sheet” guidance to the concrete request. Return the resulting postgresql patterns artifact or diagnosis with source/command evidence for each conclusion.

- Type traps: money in `numeric`, never `real` or `double precision`. Ids in `bigint`, because an `integer` runs out at 2,147,483,647. Send ids above 2^53 − 1 to JavaScript clients as strings.
- Concurrency: guard check-then-act with `SELECT ... FOR UPDATE`, an atomic `UPDATE ... WHERE`, or a unique constraint, and retry the whole transaction on SQLSTATE `40001` and `40P01`, with a capped number of attempts. Keep payment, email and queue calls out of the transaction body, because a retry runs them again: write a row for each one in the same transaction, and let a worker send it after the commit.
- Zero downtime: `CREATE INDEX CONCURRENTLY` (not inside a transaction; after a failure, find the INVALID index with `SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;`, check that no build of it is still running in `pg_stat_progress_create_index` (PostgreSQL 12 or later), then drop it with `DROP INDEX CONCURRENTLY` before you retry, because `IF NOT EXISTS` skips the retry and keeps the INVALID index), `ADD CONSTRAINT ... NOT VALID` then `VALIDATE CONSTRAINT`, and `SET lock_timeout` before any DDL.
- Full quality bar: `../../references/checklists/engineering-quality-bar.md`.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
