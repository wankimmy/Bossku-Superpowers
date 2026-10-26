---
name: bosskuai-jpa-patterns
description: "Use when the task explicitly concerns jpa patterns. JPA/Hibernate patterns for entity design, relationships, query optimization, transactions, auditing, indexing, pagination, and pooling in Spring Boot. Use when designing JPA entities or relationships, or when a Hibernate query, transaction, or N+1 problem needs fixing."
metadata:
  origin: ECC-adaptation
---

# JPA/Hibernate Patterns — portable workflow

JPA/Hibernate patterns for entity design, relationships, query optimization, transactions, auditing, indexing, pagination, and pooling in Spring Boot. Use when designing JPA entities or relationships, or when a Hibernate query, transaction, or N+1 problem needs fixing.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-mybatis-patterns`, `bosskuai-prisma-patterns`, `bosskuai-postgres-patterns`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Entity Design.
2. Relationships and N+1 Prevention.
3. Repository Patterns.
4. Transactions.
5. Pagination.
6. Indexing and Performance.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Apply the source “Entity Design”, “Relationships and N+1 Prevention” guidance to the concrete request. Return the resulting jpa/hibernate patterns artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
