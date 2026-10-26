---
name: bosskuai-master-agreement-generator
description: "Use when the task explicitly concerns master agreement generator. Generate review drafts of counterparty master agreements from one template plus a JSON spec, with role-selected clauses and a Schedule A workflow limited to the executed agreement's notice authority. Use when you need reproducible drafting and separately reviewed execution preparation."
metadata:
  origin: ECC-adaptation
---

# Master Agreement Generator — portable workflow

Generate review drafts of counterparty master agreements from one template plus a JSON spec, with role-selected clauses and a Schedule A workflow limited to the executed agreement's notice authority. Use when you need reproducible drafting and separately reviewed execution preparation.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-rapid-prototype`, `bosskuai-design-systems`, `bosskuai-llm-trading-agent-security`, `bosskuai-esign-field-placement`, `bosskuai-operations`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. Template.
3. Spec.
4. Role table.
5. Build.
6. Signature page geometry.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- The full source bundle is kept, with 3 sidecar files. Its code is reference-only until its dependencies, paths and effects are reviewed; this import did not run it.
- For clinical, compliance, legal, regulatory or financial conclusions, use current authoritative sources and an independent review; treat sample values and rules as examples until checked for the actual jurisdiction or system.

## Done when

Complete the source “Schedule A append workflow” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
