---
name: bosskuai-fastapi-development
description: "Use when the task explicitly concerns fastapi development. FastAPI best practices covering project structure, Pydantic v2 schemas, dependency injection, async handlers, authentication, authorization, transactional service layers, and testing with httpx and pytest. Use when building or reviewing FastAPI apps — Pydantic schemas, dependencies, async handlers, auth, or tests."
metadata:
  origin: ECC-adaptation
---

# FastAPI Patterns — portable workflow

FastAPI best practices covering project structure, Pydantic v2 schemas, dependency injection, async handlers, authentication, authorization, transactional service layers, and testing with httpx and pytest. Use when building or reviewing FastAPI apps — Pydantic schemas, dependencies, async handlers, auth, or tests.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-csharp-testing`, `bosskuai-dotnet-patterns`, `bosskuai-dart-flutter-patterns`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Project Structure.
2. App Factory and Lifespan.
3. app/main.py.
4. Configuration with pydantic-settings.
5. app/config.py.
6. Pydantic Schemas (v2).

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

The affected handler/dependency/schema has a focused httpx/pytest result; request validation, transaction lifetime and async execution match the inspected installed versions.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
