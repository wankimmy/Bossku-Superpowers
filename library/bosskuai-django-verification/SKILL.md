---
name: bosskuai-django-verification
description: "Use when the task explicitly concerns django verification. Run the full Django verification loop — environment check, mypy/ruff/black linting, migration safety, pytest with coverage targets, pip-audit and bandit security scans, settings and logging review, and diff review — producing a phased pass/fail report before release or PR. Use when preparing a Django pull request, validating migrations or coverage, or running pre-deploy readiness checks."
metadata:
  origin: ECC-adaptation
---

# Django Verification Loop — portable workflow

Run the full Django verification loop — environment check, mypy/ruff/black linting, migration safety, pytest with coverage targets, pip-audit and bandit security scans, settings and logging review, and diff review — producing a phased pass/fail report before release or PR. Use when preparing a Django pull request, validating migrations or coverage, or running pre-deploy readiness checks.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-springboot-verification`, `verification-before-completion`, `bosskuai-laravel-verification`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Phase 1: Environment Check.
2. Verify Python version.
3. Check virtual environment.
4. Verify environment variables.
5. Phase 2: Code Quality & Formatting.
6. Type checking.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions first: `python --version` against `requires-python` in `pyproject.toml`, and the Django, pytest-django and pip-audit versions in the lockfile or `requirements*.txt`. Check the latest stable Django release at work time on djangoproject.com, and use only APIs that exist in the installed versions. Also check the source prerequisites. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Django Verification Loop”, “Verify Python version” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Also check before you finish: `python manage.py makemigrations --check --dry-run` reports no missing migration; each new migration ran against a production data copy (ask the user to prepare one if there is none), and the old code still works on the new schema; `bandit` findings at High severity are fixed, not excepted. `pip-audit` output has no severity, so look up each advisory's severity in its advisory entry and fix every High or Critical one. Do not add an exception for these; and lint and tests run clean with no warnings. The full quality bar is in `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
