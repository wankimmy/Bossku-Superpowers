---
name: bosskuai-android-clean-architecture
description: "Use when the task explicitly concerns android clean architecture. Clean Architecture patterns for Android and Kotlin Multiplatform projects — module structure, dependency rules, UseCases, Repositories, and data layer patterns. Use when structuring modules, layers, or data flow in an Android or KMP project."
metadata:
  origin: ECC-adaptation
---

# Android Clean Architecture — portable workflow

Clean Architecture patterns for Android and Kotlin Multiplatform projects — module structure, dependency rules, UseCases, Repositories, and data layer patterns. Use when structuring modules, layers, or data flow in an Android or KMP project.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-fastapi-development`, `bosskuai-compose-multiplatform-patterns`, `bosskuai-flutter-dart-code-review`, `bosskuai-design-systems`, `bosskuai-kotlin-coroutines-flows`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Module Structure.
2. Recommended Layout.
3. Dependency Rules.
4. Domain Layer.
5. UseCase Pattern.
6. Domain Models.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: the Android Gradle Plugin, Kotlin and Compose versions in `gradle/libs.versions.toml` or `build.gradle.kts`, the Gradle version in `gradle/wrapper/gradle-wrapper.properties`, and `compileSdk`, `targetSdk` and `minSdk` in the app's `build.gradle.kts`. Check the latest AGP, Compose and API level release notes on developer.android.com at work time. Use only APIs present in the installed version. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Apply the source “Module Structure”, “Recommended Layout” guidance to the concrete request. Return the resulting android clean architecture artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

- A Room schema change ships with a migration from every version already on users' devices, tested with `MigrationTestHelper`. Keep the exported schema files in version control.
- Money is an integer in minor units or a `BigDecimal` built from a string, never a `Float` or `Double`.
- Test an app update over data from the previous release, since users keep their data.
- Full quality bar, with version and type checks: `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
