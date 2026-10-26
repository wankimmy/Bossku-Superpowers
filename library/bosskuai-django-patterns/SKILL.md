---
name: bosskuai-django-patterns
description: "Use when the task explicitly concerns django patterns. Django architecture patterns, REST API design with DRF, ORM best practices, caching, signals, middleware, and production-grade Django apps. Use when building or reviewing Django apps, DRF APIs, ORM queries, or caching."
metadata:
  origin: ECC-adaptation
---

# Django Development Patterns — portable workflow

Django architecture patterns, REST API design with DRF, ORM best practices, caching, signals, middleware, and production-grade Django apps. Use when building or reviewing Django apps, DRF APIs, ORM queries, or caching.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-fastapi-development`, `bosskuai-laravel-development`, `bosskuai-software-architecture`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Project Structure.
2. Recommended Layout.
3. Split Settings Pattern.
4. config/settings/base.py.
5. config/settings/development.py.
6. config/settings/production.py.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Apply the source “Project Structure”, “Recommended Layout” guidance to the concrete request. Return the resulting django development patterns artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
