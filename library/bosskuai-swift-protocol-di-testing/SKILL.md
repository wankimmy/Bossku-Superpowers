---
name: bosskuai-swift-protocol-di-testing
description: "Use when the task explicitly concerns swift protocol di testing. Protocol-based dependency injection for testable Swift code — mock file system, network, and external APIs using focused protocols and Swift Testing. Use when Swift code needs testing and file system, network, or external APIs must be mocked."
metadata:
  origin: ECC-adaptation
---

# Swift Protocol-Based Dependency Injection for Testing — portable workflow

Protocol-based dependency injection for testable Swift code — mock file system, network, and external APIs using focused protocols and Swift Testing. Use when Swift code needs testing and file system, network, or external APIs must be mocked.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-agent-architecture-audit`, `bosskuai-angular-developer`, `bosskuai-story-lifecycle`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Core Pattern.
2. 1. Define Small, Focused Protocols.
3. 2. Create Default (Production) Implementations.
4. 3. Create Mock Implementations for Testing.
5. 4. Inject Dependencies with Default Parameters.
6. 5. Write Tests with Swift Testing.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Apply the source “Core Pattern”, “1. Define Small, Focused Protocols” guidance to the concrete request. Return the resulting swift protocol-based dependency injection for testing artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
