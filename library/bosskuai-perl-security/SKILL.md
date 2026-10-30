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
- Check the project's tool versions first: `perl -v`, the `requires 'perl'` line in `cpanfile`, and the module versions in `cpanfile.snapshot` if the project uses Carton. Check the latest stable Perl release on perl.org at work time. Check each CPAN module's `Changes` file or its MetaCPAN page for security fixes in the version you run, and use only APIs that exist in those versions. Also check the source prerequisites. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Complete the source “Good: Capture output safely with IPC::Run3”, “Good: Encode output for HTML context” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Also check before you finish. Data from outside the program is tainted. Run CGI and other untrusted-input code with `-T`. Untaint data only with a pattern that matches the exact expected format. Never use a catch-all pattern such as `/(.*)/`. Pass shell commands as a list to `system` or `IPC::Run3`, never a string built from input. Use three-argument `open` with a literal mode. Use `DBI` placeholders for every SQL value. A table name, column name or sort direction cannot be a placeholder, so check it against an allowlist first. Fix a High or Critical finding; do not except it. The full quality bar is in `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
