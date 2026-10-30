---
name: bosskuai-perl-patterns
description: "Use when the task explicitly concerns perl patterns. Modern Perl 5.36+ idioms, best practices, and conventions for building robust, maintainable Perl applications. Use when writing or reviewing modern Perl 5.36+ code."
metadata:
  origin: ECC-adaptation
---

# Modern Perl Development Patterns — portable workflow

Modern Perl 5.36+ idioms, best practices, and conventions for building robust, maintainable Perl applications. Use when writing or reviewing modern Perl 5.36+ code.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-dotnet-patterns`, `bosskuai-go-development`, `bosskuai-kotlin-patterns`, `bosskuai-perl-security`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. Core Principles.
3. 1. Use `v5.36` Pragma.
4. Good: Modern preamble.
5. Bad: Legacy boilerplate.
6. 2. Subroutine Signatures.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions first: `perl -v` for the installed Perl, and the `requires 'perl'` line in `cpanfile`. If the project uses Carton, read the module versions from `cpanfile.snapshot`. Check the latest stable Perl release and its support dates at work time on perl.org, and use only features that exist in the installed version. Also check the source prerequisites. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Apply the source “How It Works”, “Core Principles” guidance to the concrete request. Return the resulting modern perl development patterns artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Also check before you finish:

- Keep money as integer cents or in `Math::BigFloat`, never as a float. `0.1 + 0.2 == 0.3` is false. `print` rounds its output, so `print 0.1 + 0.2` shows `0.3`.
- Start every file with `use v5.36;` (or a later version), or with `use strict;` and `use warnings;`, so mistakes fail loudly.
- Decode text from a file, a form or a database at the boundary, and check its type before use.

The full quality bar is in `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
