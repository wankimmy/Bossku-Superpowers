---
name: bosskuai-dotnet-patterns
description: "Use when the task explicitly concerns dotnet patterns. Idiomatic C# and .NET patterns, conventions, dependency injection, async/await, and best practices for building robust, maintainable .NET applications. Use when writing or reviewing C# / .NET code — DI, async, or general conventions."
metadata:
  origin: ECC-adaptation
---

# .NET Development Patterns — portable workflow

Idiomatic C# and .NET patterns, conventions, dependency injection, async/await, and best practices for building robust, maintainable .NET applications. Use when writing or reviewing C# / .NET code — DI, async, or general conventions.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-go-development`, `bosskuai-kotlin-patterns`, `bosskuai-perl-patterns`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Core Principles.
2. 1. Prefer Immutability.
3. 2. Explicit Over Implicit.
4. 3. Depend on Abstractions.
5. Async/Await Patterns.
6. Proper Async Usage.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Apply the source “Core Principles”, “1. Prefer Immutability” guidance to the concrete request. Return the resulting .net development patterns artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
