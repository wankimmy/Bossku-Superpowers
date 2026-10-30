---
name: bosskuai-kotlin-testing
description: "Use when the task explicitly concerns kotlin testing. Kotlin testing patterns with Kotest, MockK, coroutine testing, property-based testing, and Kover coverage. Follows TDD methodology with idiomatic Kotlin practices. Use when writing Kotlin tests with Kotest or MockK, or testing coroutines and checking coverage."
metadata:
  origin: ECC-adaptation
---

# Kotlin Testing Patterns — portable workflow

Kotlin testing patterns with Kotest, MockK, coroutine testing, property-based testing, and Kover coverage. Follows TDD methodology with idiomatic Kotlin practices. Use when writing Kotlin tests with Kotest or MockK, or testing coroutines and checking coverage.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-go-development`, `bosskuai-rust-testing`, `bosskuai-fsharp-testing`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. Quick Reference.
3. TDD Workflow for Kotlin.
4. Kotest Spec Styles.
5. Kotest Matchers.
6. MockK.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: the Kotest, MockK and Kover versions, and the Kotlin version, in `gradle/libs.versions.toml` or `build.gradle.kts`. Check the latest stable Kotlin release on kotlinlang.org, and the GitHub release pages of each tool, at work time. Use only APIs present in the installed version. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “TDD Workflow for Kotlin”, “Verify coverage thresholds” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

- Test data uses production types: parse money from the string production sends (`"0.01"`) into `BigDecimal`, not a `Double` literal.
- Coroutine tests use `runTest`, never `Thread.sleep`.
- Database tests run on the production engine and version through Testcontainers, not a mock that hides the SQL.
- Full quality bar, with version and type checks: `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
