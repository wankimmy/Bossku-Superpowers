---
name: bosskuai-swift-concurrency-6-2
description: "Use when the task explicitly concerns swift concurrency 6 2. Swift 6.2 Approachable Concurrency — single-threaded by default, @concurrent for explicit background offloading, isolated conformances for main actor types. Use when adopting Swift 6.2 concurrency — offloading with @concurrent or resolving main-actor isolation."
metadata:
  origin: ECC-adaptation
---

# Swift 6.2 Approachable Concurrency — portable workflow

Swift 6.2 Approachable Concurrency — single-threaded by default, @concurrent for explicit background offloading, isolated conformances for main actor types. Use when adopting Swift 6.2 concurrency — offloading with @concurrent or resolving main-actor isolation.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-subagent-delegation`, `bosskuai-swift-actor-persistence`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Core Problem: Implicit Background Offloading.
2. Core Pattern — Isolated Conformances.
3. Core Pattern — Global and Static Variables.
4. MainActor Default Inference Mode.
5. Core Pattern — @concurrent for Background Work.
6. Key Design Decisions.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: read `swift-tools-version` in `Package.swift`, the default actor isolation set on the Xcode target, and run `swift --version`. Check the latest stable Swift release at swift.org/download at work time, and use only APIs present in the installed version. Confirm the toolchain supports `@concurrent` before you use it. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Apply the source “Core Problem: Implicit Background Offloading”, “Core Pattern — Isolated Conformances” guidance to the concrete request. Return the resulting swift 6.2 approachable concurrency artifact or diagnosis with source/command evidence for each conclusion.

- Type traps: a value that is not `Sendable` can race when it crosses into `@concurrent` code. Do not add `@unchecked Sendable` to silence the compiler unless a lock guards every access.
- Concurrency: state can change at each `await`, on the main actor too, so check it again after the `await`. Code moved off the main actor must not touch UI state.
- Zero downtime: a concurrency change must not change the API or the stored data that older app builds use.
- Full quality bar: `../../references/checklists/engineering-quality-bar.md`.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
