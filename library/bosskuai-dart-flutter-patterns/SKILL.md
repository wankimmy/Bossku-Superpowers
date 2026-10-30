---
name: bosskuai-dart-flutter-patterns
description: "Use when the task explicitly concerns dart flutter patterns. Production-ready Dart and Flutter patterns covering null safety, immutable state with Freezed, async composition, widget architecture, state management (BLoC, Riverpod, Provider), GoRouter navigation with auth guards, Dio networking, error handling, and testing. Use when writing or reviewing Dart and Flutter code — state, widgets, navigation, networking, or architecture."
metadata:
  origin: ECC-adaptation
---

# Dart/Flutter Patterns — portable workflow

Production-ready Dart and Flutter patterns covering null safety, immutable state with Freezed, async composition, widget architecture, state management (BLoC, Riverpod, Provider), GoRouter navigation with auth guards, Dio networking, error handling, and testing. Use when writing or reviewing Dart and Flutter code — state, widgets, navigation, networking, or architecture.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-flutter-dart-code-review`, `bosskuai-swiftui-patterns`, `vue-patterns`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. 1. Null Safety Fundamentals.
3. Prefer Patterns Over Bang Operator.
4. Avoid `late` Overuse.
5. 2. Immutable State.
6. Sealed Classes for State Hierarchies.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: read the SDK constraint (`environment: sdk`) in `pubspec.yaml`, the resolved versions in `pubspec.lock`, and the installed toolchain from `flutter --version`. Check the latest stable Flutter release and its release date at docs.flutter.dev/install/archive at work time, and use only APIs present in the installed version. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Apply the source “How It Works”, “1. Null Safety Fundamentals” guidance to the concrete request. Return the resulting dart/flutter patterns artifact or diagnosis with source/command evidence for each conclusion.

- Type traps: `jsonDecode` returns an int for `1` and a double for `1.5`, and a String for `"1"`. Read numbers as `num`, and keep money in integer minor units, never `double`.
- Concurrency: after an `await`, check `context.mounted` before you use a `BuildContext`, and drop a late result when a newer request has started.
- Zero downtime: old app builds stay installed after a release, so keep the API and local data format they read working until those builds are no longer in use.
- Full quality bar: `../../references/checklists/engineering-quality-bar.md`.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
