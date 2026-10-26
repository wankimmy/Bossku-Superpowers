---
name: bosskuai-mailtrap-email-integration
description: "Use when the task explicitly concerns mailtrap email integration. Guides agents through integrating transactional email sending via Mailtrap's Email API, including sandbox testing, domain verification, and API authentication. Use when implementing email-sending features, debugging delivery issues, or setting up safe dev/staging email testing."
metadata:
  origin: ECC-adaptation
---

# Mailtrap Email Integration — portable workflow

Guides agents through integrating transactional email sending via Mailtrap's Email API, including sandbox testing, domain verification, and API authentication. Use when implementing email-sending features, debugging delivery issues, or setting up safe dev/staging email testing.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-email-ops`, `bosskuai-browser-automation`, `bosskuai-cybersecurity-risk`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Core Concepts.
2. Anti-Patterns.
3. Best Practices.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Apply the source “Core Concepts”, “Anti-Patterns” guidance to the concrete request. Return the resulting mailtrap email integration artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
