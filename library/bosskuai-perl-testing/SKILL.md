---
name: bosskuai-perl-testing
description: "Use when the task explicitly concerns perl testing. Perl testing patterns using Test2::V0, Test::More, prove runner, mocking, coverage with Devel::Cover, and TDD methodology. Use when writing Perl tests with Test2::V0 or Test::More, or measuring coverage."
metadata:
  origin: ECC-adaptation
---

# Perl Testing Patterns — portable workflow

Perl testing patterns using Test2::V0, Test::More, prove runner, mocking, coverage with Devel::Cover, and TDD methodology. Use when writing Perl tests with Test2::V0 or Test::More, or measuring coverage.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-django-tdd`, `bosskuai-go-development`, `bosskuai-csharp-testing`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. TDD Workflow.
2. Step 1: RED — Write a failing test.
3. t/unit/calculator.t.
4. Step 2: GREEN — Write minimal implementation.
5. lib/Calculator.pm.
6. Step 3: REFACTOR — Improve while tests stay green.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions first: `perl -v`, the `requires 'perl'` line in `cpanfile`, and the Test2::Suite and Devel::Cover versions in `cpanfile.snapshot` or the installed copy. Check the latest stable release of each on metacpan.org at work time, and use only APIs that exist in the installed versions. Also check the source prerequisites. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Complete the source “TDD Workflow”, “Equality” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Also check before you finish:

- The suite runs clean with `prove -lr t` (or the repo's documented command), with no warnings.
- Each fix has a test that fails before the fix and passes after.
- Test data has the types production returns. DBI often returns numbers as strings, so test with "0.01", not 0.01.
- A mock of a database, HTTP or file call matches a real or recorded response in shape and type.

The full quality bar is in `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
