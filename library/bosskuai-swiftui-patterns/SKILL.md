---
name: bosskuai-swiftui-patterns
description: "Use when the task explicitly concerns swiftui patterns. SwiftUI architecture patterns, state management with @Observable, view composition, navigation, performance optimization, and modern iOS/macOS UI best practices. Use when building or reviewing SwiftUI views, @Observable state, navigation, or render performance."
metadata:
  origin: ECC-adaptation
---

# SwiftUI Patterns — portable workflow

SwiftUI architecture patterns, state management with @Observable, view composition, navigation, performance optimization, and modern iOS/macOS UI best practices. Use when building or reviewing SwiftUI views, @Observable state, navigation, or render performance.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-react-development`, `vue-patterns`, `bosskuai-dart-flutter-patterns`, `bosskuai-swift-actor-persistence`, `bosskuai-swift-protocol-di-testing`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. State Management.
2. Property Wrapper Selection.
3. @Observable ViewModel.
4. View Consuming the ViewModel.
5. Environment Injection.
6. View Composition.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: read the deployment target (`IPHONEOS_DEPLOYMENT_TARGET`, or `MACOSX_DEPLOYMENT_TARGET` on macOS) in the Xcode project, and run `xcodebuild -version`. Check the latest Xcode release notes on developer.apple.com at work time, and use only APIs present in the installed version. Gate newer SwiftUI APIs with `#available`. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Apply the source “State Management”, “Property Wrapper Selection” guidance to the concrete request. Return the resulting swiftui patterns artifact or diagnosis with source/command evidence for each conclusion.

- Type traps: money in `Decimal`, and dates decoded with the same date strategy the API uses (`JSONDecoder.dateDecodingStrategy`).
- Concurrency: keep UI-facing `@Observable` state on the main actor. Use `.task` for async work, since it cancels when the view goes away, and check the state again before a late result writes to it.
- Zero downtime: old app builds stay in use after a release, so the API and stored data they read must stay compatible until those builds are gone.
- Full quality bar: `../../references/checklists/engineering-quality-bar.md`.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
