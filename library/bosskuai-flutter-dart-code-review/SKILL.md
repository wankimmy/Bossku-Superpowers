---
name: bosskuai-flutter-dart-code-review
description: "Use when the task explicitly concerns flutter dart code review. Library-agnostic Flutter/Dart code review checklist covering widget best practices, state management patterns (BLoC, Riverpod, Provider, GetX, MobX, Signals), Dart idioms, performance, accessibility, security, and clean architecture. Use when reviewing Flutter or Dart code, whatever state management library the project uses."
metadata:
  origin: ECC-adaptation
---

# Flutter/Dart Code Review Best Practices — portable workflow

Library-agnostic Flutter/Dart code review checklist covering widget best practices, state management patterns (BLoC, Riverpod, Provider, GetX, MobX, Signals), Dart idioms, performance, accessibility, security, and clean architecture. Use when reviewing Flutter or Dart code, whatever state management library the project uses.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-dart-flutter-patterns`, `bosskuai-swiftui-patterns`, `vue-patterns`, `accessibility`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. 1. General Project Health.
2. 2. Dart Language Pitfalls.
3. 3. Widget Best Practices.
4. Widget decomposition:.
5. Const usage:.
6. Key usage:.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: read the SDK constraint (`environment: sdk`) in `pubspec.yaml`, the resolved versions in `pubspec.lock`, and `flutter --version`. Check the latest stable Flutter release at docs.flutter.dev/release/archive at work time, and use only APIs present in the installed version. Run `flutter analyze` and read its output. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Immutability & value equality (for immutable-state solutions: BLoC, Riverpod, Redux):”, “Widget test quality:” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

- Type traps: a JSON whole number cast with `as double` (it throws on the Dart VM), money held in a `double` (it rounds), and numbers that arrive as text.
- Concurrency: `BuildContext` used after an `await` with no `mounted` check, `setState` after `dispose`, and a late async result that overwrites newer state.
- Zero downtime: a changed API or stored-data format must still read what older app builds wrote.
- Full quality bar: `../../references/checklists/engineering-quality-bar.md`.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
