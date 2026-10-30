---
name: bosskuai-kotlin-ktor-patterns
description: "Use when the task explicitly concerns kotlin ktor patterns. Ktor server patterns including routing DSL, plugins, authentication, Koin DI, kotlinx.serialization, WebSockets, and testApplication testing. Use when building a Ktor server — routing, plugins, auth, DI, serialization, or tests."
metadata:
  origin: ECC-adaptation
---

# Ktor Server Patterns — portable workflow

Ktor server patterns including routing DSL, plugins, authentication, Koin DI, kotlinx.serialization, WebSockets, and testApplication testing. Use when building a Ktor server — routing, plugins, auth, DI, serialization, or tests.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-fastapi-development`, `bosskuai-go-development`, `bosskuai-kotlin-testing`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Application Structure.
2. Standard Ktor Project Layout.
3. Application Entry Point.
4. Routing DSL.
5. Basic Routes.
6. Route Organization with Authenticated Routes.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: the Ktor version and the `io.ktor.plugin` Gradle plugin in `gradle/libs.versions.toml` or `build.gradle.kts`, the Kotlin version, and what the build resolves (`./gradlew dependencies --configuration runtimeClasspath`). Check the latest Ktor release on ktor.io at work time. Use only APIs present in the installed version. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Apply the source “Application Structure”, “Standard Ktor Project Layout” guidance to the concrete request. Return the resulting ktor server patterns artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

- Every outbound call sets timeouts (`HttpTimeout`), and retries (`HttpRequestRetry`) only for requests that are safe to repeat.
- Decide `ignoreUnknownKeys` on purpose. When it is `true`, extra fields are ignored. It is `false` by default, so an extra field fails. Missing required fields fail. Wrong-type fields fail. With `coerceInputValues` on, only two cases change: a `null` for a non-nullable field, and an unknown enum value. Each one uses the field's default, if it has one.
- Test each route with `testApplication`, including anonymous, malformed and wrong-type requests.
- Full quality bar, with version and type checks: `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
