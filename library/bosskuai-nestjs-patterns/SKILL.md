---
name: bosskuai-nestjs-patterns
description: "Use when the task explicitly concerns nestjs patterns. NestJS architecture patterns for modules, controllers, providers, DTO validation, guards, interceptors, config, and production-grade TypeScript backends. Use when building or reviewing a NestJS backend — modules, providers, DTO validation, guards, or interceptors."
metadata:
  origin: ECC-adaptation
---

# NestJS Development Patterns — portable workflow

NestJS architecture patterns for modules, controllers, providers, DTO validation, guards, interceptors, config, and production-grade TypeScript backends. Use when building or reviewing a NestJS backend — modules, providers, DTO validation, guards, or interceptors.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-django-patterns`, `bosskuai-laravel-development`, `bosskuai-dart-flutter-patterns`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Project Structure.
2. Bootstrap and Global Validation.
3. Modules, Controllers, and Providers.
4. DTOs and Validation.
5. Auth, Guards, and Request Context.
6. Exception Filters and Error Shape.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Apply the source “Project Structure”, “Bootstrap and Global Validation” guidance to the concrete request. Return the resulting nestjs development patterns artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
