---
name: bosskuai-django-tdd
description: "Use when the task explicitly concerns django tdd. Django testing strategies with pytest-django, TDD methodology, factory_boy, mocking, coverage, and testing Django REST Framework APIs. Use when writing Django or DRF tests with pytest-django, or driving a Django feature test-first."
metadata:
  origin: ECC-adaptation
---

# Django Testing with TDD — portable workflow

Django testing strategies with pytest-django, TDD methodology, factory_boy, mocking, coverage, and testing Django REST Framework APIs. Use when writing Django or DRF tests with pytest-django, or driving a Django feature test-first.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-laravel-tdd`, `bosskuai-perl-testing`, `python-testing`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. TDD Workflow for Django.
2. Red-Green-Refactor Cycle.
3. Step 1: RED - Write failing test.
4. Step 2: GREEN - Make test pass.
5. Create User model or factory.
6. Step 3: REFACTOR - Improve while keeping tests green.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Complete the source “TDD Workflow for Django” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
