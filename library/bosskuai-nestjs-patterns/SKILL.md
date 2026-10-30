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
- Check the project's tool versions first: the Node version in `.nvmrc`, `.node-version` or `package.json` `engines`, and the `@nestjs/core` version in the lockfile (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock` or `bun.lock`). Check the latest stable NestJS release at work time on docs.nestjs.com, and use only APIs that exist in the installed version. Also check the source prerequisites. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Apply the source “Project Structure”, “Bootstrap and Global Validation” guidance to the concrete request. Return the resulting nestjs development patterns artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Also check before you finish:

- Check that the global `ValidationPipe` sets `whitelist: true` and `forbidNonWhitelisted: true`. Then unknown top-level fields are rejected.
- A nested object is validated, and its unknown fields rejected, only when its property has `@ValidateNested()` and `@Type()`.
- Check that each DTO accepts only the types production sends. Money is a string or a decimal, never a plain number by accident.
- Check that a retried or double-submitted write is guarded by a unique constraint or an idempotency key.
- Check that `app.enableShutdownHooks()` is set. Without it, shutdown hooks do not run on SIGTERM.

The full quality bar is in `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
