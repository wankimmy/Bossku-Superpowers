---
name: bosskuai-django-celery
description: "Use when the task explicitly concerns django celery. Django + Celery async task patterns — configuration, task design, beat scheduling, retries, canvas workflows, monitoring, and testing. Use when adding background jobs, scheduled tasks, or async processing to a Django app."
metadata:
  origin: ECC-adaptation
---

# Django + Celery Async Task Patterns — portable workflow

Django + Celery async task patterns — configuration, task design, beat scheduling, retries, canvas workflows, monitoring, and testing. Use when adding background jobs, scheduled tasks, or async processing to a Django app.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-qa-automation-strategy`, `bosskuai-quarkus-patterns`, `bosskuai-springboot-patterns`, `bosskuai-django-patterns`, `bosskuai-django-tdd`, `python-testing`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Project Setup.
2. `celery.py` — App Entrypoint.
3. config/celery.py.
4. config/__init__.py.
5. Django Settings.
6. config/settings/base.py.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions first: `python --version` against `requires-python` in `pyproject.toml`, and the Django and Celery versions in the lockfile (`uv.lock` or `poetry.lock`) or `requirements*.txt`. Check the latest stable release at work time on djangoproject.com and docs.celeryq.dev, and use only APIs that exist in the installed versions. Also check the source prerequisites. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Production Checklist” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Also check before you finish. Task arguments are plain ids and values that survive serialization. Never pass a model object. A retry or a duplicate run must not repeat a side effect. Inside `transaction.atomic()`, lock the row with `select_for_update()`, check the stored status after the lock, and return early when the work is done. Save the new status in that same transaction, because the lock alone does not stop a later run. For an external call such as a charge or an email, also send an idempotency key where the provider supports one. A task sent from inside a transaction goes out through `transaction.on_commit`, so the worker never reads data that is not committed yet. Renaming a task or changing its arguments breaks messages already queued. Keep the old form until the queue is empty. The full quality bar is in `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
