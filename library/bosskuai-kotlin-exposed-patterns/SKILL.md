---
name: bosskuai-kotlin-exposed-patterns
description: "Use when the task explicitly concerns kotlin exposed patterns. JetBrains Exposed ORM patterns including DSL queries, DAO pattern, transactions, HikariCP connection pooling, Flyway migrations, and repository pattern. Use when working with the Exposed ORM — DSL or DAO queries, transactions, pooling, or migrations."
metadata:
  origin: ECC-adaptation
---

# Kotlin Exposed Patterns — portable workflow

JetBrains Exposed ORM patterns including DSL queries, DAO pattern, transactions, HikariCP connection pooling, Flyway migrations, and repository pattern. Use when working with the Exposed ORM — DSL or DAO queries, transactions, pooling, or migrations.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-prisma-patterns`, `bosskuai-tinystruct-patterns`, `bosskuai-vite-patterns`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. DSL Query.
3. DAO Entity Usage.
4. HikariCP Configuration.
5. Database Setup.
6. HikariCP Connection Pooling.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: the Exposed, HikariCP and Flyway versions in `gradle/libs.versions.toml` or `build.gradle.kts`, the Kotlin version, and the database engine version (for example `SELECT version();` on PostgreSQL). Check the latest Exposed release notes on GitHub at work time. Use only APIs present in the installed version. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Apply the source “How It Works”, “DSL Query” guidance to the concrete request. Return the resulting kotlin exposed patterns artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

- Money uses a decimal column with fixed precision and scale, never a double column.
- No entity is read after its transaction ends. A check followed by a write runs in one transaction, with a row lock or a unique constraint.
- Keep the sum of `maximumPoolSize` across every running app instance (old and new instances both count during a rolling deploy), plus other clients such as workers, migrations and admin tools, under the database connection limit (`max_connections` on PostgreSQL or MySQL). Never edit a Flyway migration after it ships.
- Full quality bar, with version and type checks: `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
