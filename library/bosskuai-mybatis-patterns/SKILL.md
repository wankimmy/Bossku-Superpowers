---
name: bosskuai-mybatis-patterns
description: "Use when the task explicitly concerns mybatis patterns. MyBatis and MyBatis-Spring patterns for mapper design, XML and annotation SQL, result mapping, dynamic SQL safety, transactions, batching, pagination, and query performance. Use when building or reviewing Java persistence code with MyBatis, Spring Boot, MyBatis-Spring, or MyBatis-based legacy applications."
metadata:
  origin: ECC-adaptation
---

# MyBatis Patterns — portable workflow

MyBatis and MyBatis-Spring patterns for mapper design, XML and annotation SQL, result mapping, dynamic SQL safety, transactions, batching, pagination, and query performance. Use when building or reviewing Java persistence code with MyBatis, Spring Boot, MyBatis-Spring, or MyBatis-based legacy applications.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-jpa-patterns`, `bosskuai-kotlin-patterns`, `bosskuai-springboot-patterns`, `bosskuai-cybersecurity-risk`, `bosskuai-postgres-patterns`, `database-migrations`, `mysql-patterns`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. Parameter Binding and SQL Safety.
3. XML, Result Types, and Result Maps.
4. Dynamic SQL.
5. Transactions and Sessions.
6. Pagination and Large Reads.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: the Java version (`java.version` or `maven.compiler.release` in `pom.xml`, the Gradle toolchain in `build.gradle(.kts)`, and `java -version`), the MyBatis, MyBatis-Spring and Spring Boot versions in `pom.xml` or `build.gradle(.kts)`, and what the build resolves (`mvn dependency:tree` or `./gradlew dependencies --configuration runtimeClasspath`). Check the latest MyBatis release notes on mybatis.org at work time. Use only APIs present in the installed version. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Complete the source “Review Checklist” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

- User input reaches SQL only through `#{}`. `${}` is allowed only for a fixed allow-list, such as a sort column.
- A test covers an empty `<foreach>` list, so no invalid `IN ()` reaches the database.
- DECIMAL columns map to `BigDecimal` with the production scale, and tests use the production column type.
- Full quality bar, with version and type checks: `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
