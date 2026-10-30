---
name: bosskuai-django-security
description: "Use when the task explicitly concerns django security. Django security best practices, authentication, authorization, CSRF protection, SQL injection prevention, XSS prevention, and secure deployment configurations. Use when reviewing Django authentication, authorization, input handling, or deployment settings."
metadata:
  origin: ECC-adaptation
---

# Django Security Best Practices — portable workflow

Django security best practices, authentication, authorization, CSRF protection, SQL injection prevention, XSS prevention, and secure deployment configurations. Use when reviewing Django authentication, authorization, input handling, or deployment settings.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-laravel-security`, `bosskuai-fastapi-development`, `bosskuai-perl-security`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Core Security Settings.
2. Production Settings Configuration.
3. settings/production.py.
4. Security headers.
5. HTTPS and Cookies.
6. Secret key (must be set via environment variable).

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions first: `python --version`, and the Django version in the lockfile (`uv.lock` or `poetry.lock`) or `requirements*.txt`. Check the latest stable release at work time on djangoproject.com, and which versions still get security fixes there. A version without security fixes is a finding. Use only settings and APIs that exist in the installed version. Also check the source prerequisites. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Complete the source “Quick Security Checklist” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Also check before you finish: every view and query limits objects to what the signed-in user may see or change, not only the login check; model forms and serializers list their fields and never use `__all__`, so a client cannot set `is_staff` or a price; raw SQL, `raw()` and `extra()` take parameters, never formatted strings; and `python manage.py check --deploy` runs clean with the production settings. Fix a High or Critical finding; do not except it. The full quality bar is in `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
