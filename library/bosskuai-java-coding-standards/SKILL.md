---
name: bosskuai-java-coding-standards
description: "Use when the task explicitly concerns java coding standards. Java coding standards for Spring Boot and Quarkus services: naming, immutability, Optional usage, streams, exceptions, generics, CDI, reactive patterns, and project layout. Automatically applies framework-specific conventions. Use when writing or reviewing Java in a Spring Boot or Quarkus service."
metadata:
  origin: ECC-adaptation
---

# Java Coding Standards — portable workflow

Java coding standards for Spring Boot and Quarkus services: naming, immutability, Optional usage, streams, exceptions, generics, CDI, reactive patterns, and project layout. Automatically applies framework-specific conventions. Use when writing or reviewing Java in a Spring Boot or Quarkus service.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-coding-best-practices`, `bosskuai-code-revamp`, `bosskuai-quarkus-patterns`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. Framework Detection.
3. Core Principles.
4. Naming.
5. Immutability.
6. Optional Usage.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: `java -version`, the release target in `maven.compiler.release` or the Gradle toolchain, and the Spring Boot or Quarkus version in `pom.xml`, `build.gradle(.kts)` or `gradle.properties`. Check the latest stable JDK on openjdk.org, and the Spring Boot or Quarkus release and support dates on spring.io or quarkus.io, at work time. Use only APIs present in the installed version. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Apply the source “How It Works”, “Framework Detection” guidance to the concrete request. Return the resulting java coding standards artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

- Money and other decimals: build `BigDecimal` from a string and compare with `compareTo`, since `equals` treats `2.0` and `2.00` as different.
- Shared mutable state is guarded by `synchronized`, a lock or a `java.util.concurrent` type. Use `volatile` only for a single flag or value that is set without reading the old value, because it does not make a check or a read-modify-write atomic. A check and the write after it must be one atomic step, and a test covers the concurrent path.
- Values from other services are checked on purpose: Jackson turns `"0.01"` into a number by default, so decide whether that is allowed.
- Full quality bar, with version and type checks: `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
