---
name: bosskuai-kotlin-coroutines-flows
description: "Use when the task explicitly concerns kotlin coroutines flows. Kotlin Coroutines and Flow patterns for Android and KMP — structured concurrency, Flow operators, StateFlow, error handling, and testing. Use when writing coroutines or Flow code on Android or KMP, or debugging cancellation and concurrency."
metadata:
  origin: ECC-adaptation
---

# Kotlin Coroutines & Flows — portable workflow

Kotlin Coroutines and Flow patterns for Android and KMP — structured concurrency, Flow operators, StateFlow, error handling, and testing. Use when writing coroutines or Flow code on Android or KMP, or debugging cancellation and concurrency.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-dart-flutter-patterns`, `bosskuai-rust-patterns`, `bosskuai-kotlin-patterns`, `bosskuai-android-clean-architecture`, `bosskuai-compose-multiplatform-patterns`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Structured Concurrency.
2. Scope Hierarchy.
3. Parallel Decomposition.
4. SupervisorScope.
5. Flow Patterns.
6. Cold Flow — One-Shot to Stream Conversion.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: the Kotlin and `kotlinx-coroutines` versions in `gradle/libs.versions.toml` or `build.gradle.kts`, and the Android Gradle Plugin version for Android or KMP targets. Check the latest stable Kotlin release on kotlinlang.org and the coroutines releases on GitHub at work time. Use only APIs present in the installed version. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Apply the source “Structured Concurrency”, “Scope Hierarchy” guidance to the concrete request. Return the resulting kotlin coroutines & flows artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

- Never swallow `CancellationException`. A broad `catch (e: Exception)` or `runCatching` catches it, so rethrow it.
- Shared state changes with an atomic update, such as `MutableStateFlow.update { }`, or with a `Mutex`, never with a read followed by a write. Keep the `update` lambda free of side effects, because it can run more than once under contention.
- Test with `runTest` and a test dispatcher, not `Thread.sleep`, and cancel every scope you start.
- Full quality bar, with version and type checks: `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
