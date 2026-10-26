---
name: bosskuai-hexagonal-architecture
description: "Use when the task explicitly concerns hexagonal architecture. Design, implement, and refactor Ports & Adapters systems with clear domain boundaries, dependency inversion, and testable use-case orchestration across TypeScript, Java, Kotlin, and Go services. Use when introducing or refactoring toward Ports and Adapters, or when domain logic has become entangled with I/O."
metadata:
  origin: ECC-adaptation
---

# Hexagonal Architecture — portable workflow

Design, implement, and refactor Ports & Adapters systems with clear domain boundaries, dependency inversion, and testable use-case orchestration across TypeScript, Java, Kotlin, and Go services. Use when introducing or refactoring toward Ports and Adapters, or when domain logic has become entangled with I/O.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-quarkus-patterns`, `bosskuai-tdd-loop`, `bosskuai-springboot-patterns`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Core Concepts.
2. How It Works.
3. Step 1: Model a use case boundary.
4. Step 2: Define outbound ports first.
5. Step 3: Implement the use case with pure orchestration.
6. Step 4: Build adapters at the edge.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Best Practices Checklist” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
