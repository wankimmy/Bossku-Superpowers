---
name: bosskuai-compose-multiplatform-patterns
description: "Use when the task explicitly concerns compose multiplatform patterns. Compose Multiplatform and Jetpack Compose patterns for KMP projects — state management, navigation, theming, performance, and platform-specific UI. Use when building Compose or Jetpack Compose UI, state, navigation, or theming in a KMP project."
metadata:
  origin: ECC-adaptation
---

# Compose Multiplatform Patterns — portable workflow

Compose Multiplatform and Jetpack Compose patterns for KMP projects — state management, navigation, theming, performance, and platform-specific UI. Use when building Compose or Jetpack Compose UI, state, navigation, or theming in a KMP project.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-swiftui-patterns`, `vue-patterns`, `bosskuai-flutter-dart-code-review`, `bosskuai-android-clean-architecture`, `bosskuai-kotlin-coroutines-flows`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. State Management.
2. ViewModel + Single State Object.
3. Collecting State in Compose.
4. Event Sink Pattern.
5. Navigation.
6. Type-Safe Navigation (Compose Navigation 2.8+).

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: the Compose Multiplatform and Kotlin versions in `gradle/libs.versions.toml` or `build.gradle.kts`, and the Android Gradle Plugin version when an Android target is built. Compose Multiplatform needs a matching Kotlin version, so check its release notes on jetbrains.com at work time. Use only APIs present in the installed version. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Apply the source “State Management”, “ViewModel + Single State Object” guidance to the concrete request. Return the resulting compose multiplatform patterns artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

- Each screen has one immutable state object. State that must survive rotation or process death is saved, not only held in memory.
- Flows are collected with a lifecycle-aware collector, so a stopped screen stops collecting.
- Each `expect` and `actual` pair is tested on every target the app ships to.
- Full quality bar, with version and type checks: `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
