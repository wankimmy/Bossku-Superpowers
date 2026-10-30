---
name: bosskuai-prisma-patterns
description: "Use when the task explicitly concerns prisma patterns. Prisma ORM patterns for TypeScript backends — schema design, query optimization, transactions, pagination, and critical traps like updateMany returning count not records, $transaction timeouts, migrate dev resetting the DB, @updatedAt skipped on bulk writes, and serverless connection exhaustion. Use when writing a Prisma schema or query, or debugging transactions, migrations, or serverless connection limits."
metadata:
  origin: ECC-adaptation
---

# Prisma Patterns — portable workflow

Prisma ORM patterns for TypeScript backends — schema design, query optimization, transactions, pagination, and critical traps like updateMany returning count not records, $transaction timeouts, migrate dev resetting the DB, @updatedAt skipped on bulk writes, and serverless connection exhaustion. Use when writing a Prisma schema or query, or debugging transactions, migrations, or serverless connection limits.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-jpa-patterns`, `database-migrations`, `mysql-patterns`, `bosskuai-nestjs-patterns`, `bosskuai-performance-profiling`, `bosskuai-postgres-patterns`, `bosskuai-software-architecture`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Core Concepts.
2. ID Strategy.
3. Schema Defaults.
4. `include` vs `select`.
5. Transaction Form Selection.
6. PrismaClient Singleton.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions first: `npx prisma -v` for the installed Prisma CLI and engines, and the `prisma` and `@prisma/client` versions in `package.json` and the lockfile. The `provider` in `schema.prisma` names the database. Check the latest stable Prisma release at work time on prisma.io, and use only APIs that exist in the installed version. Also check the source prerequisites. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Apply the source “Core Concepts”, “ID Strategy” guidance to the concrete request. Return the resulting prisma patterns artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Also check before you finish:

- `Decimal` values are compared with their own methods, not `===`.
- A `BigInt` must become a string before `JSON.stringify`, because `JSON.stringify` throws on a `BigInt`.
- Run the migration with `prisma migrate deploy` on a production data copy. Never use `migrate dev`, which can reset a database.
- A write that depends on a read needs one of these: a conditional `updateMany` (check `count`), a unique constraint, or a `Serializable` transaction that retries on `P2034` (a retry runs the callback again, so keep payment, email and queue calls outside it).
- The old app still runs on the new schema during deploy.
- Full quality bar, with version and type checks: `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
