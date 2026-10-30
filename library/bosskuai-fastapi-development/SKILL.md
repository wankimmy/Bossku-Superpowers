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
- Check the project's tool versions first: `python --version` against `requires-python` in `pyproject.toml`, and the FastAPI, Starlette and Pydantic versions in the lockfile (`uv.lock` or `poetry.lock`) or `requirements*.txt`. Pydantic v1 and v2 have different APIs, so confirm which one is installed. Check the latest stable FastAPI release at work time on pypi.org, and use only APIs that exist in the installed versions. Also check the source prerequisites. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

The affected handler/dependency/schema has a focused httpx/pytest result; request validation, transaction lifetime and async execution match the inspected installed versions.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Also check before you finish. Pydantic v2 accepts "0.01" for a float field and "1" for an int field by default. Test money and count fields with the strings production really sends. Use `Decimal` for money. A blocking call inside an `async def` handler stalls the whole event loop. Use a plain `def` handler or a thread. A POST that a client can retry is guarded by a unique constraint or an idempotency key. The full quality bar is in `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
