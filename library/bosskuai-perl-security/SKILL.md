---
name: bosskuai-perl-security
description: "Use when the task explicitly concerns perl security. Comprehensive Perl security covering taint mode, input validation, safe process execution, DBI parameterized queries, web security (XSS/SQLi/CSRF), and perlcritic security policies. Use when reviewing Perl input handling, process execution, DBI queries, or web-facing code."
metadata:
  origin: ECC-adaptation
---

# Perl Security Patterns — portable workflow

Comprehensive Perl security covering taint mode, input validation, safe process execution, DBI parameterized queries, web security (XSS/SQLi/CSRF), and perlcritic security policies. Use when reviewing Perl input handling, process execution, DBI queries, or web-facing code.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-django-security`, `bosskuai-quarkus-security`, `bosskuai-cybersecurity-risk`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. Taint Mode.
3. Enabling Taint Mode.
4. Tainted: anything from outside the program.
5. Sanitize PATH early (required in taint mode).
6. Untainting Pattern.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Complete the source “Good: Capture output safely with IPC::Run3”, “Good: Encode output for HTML context” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
