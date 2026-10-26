---
name: bosskuai-scientific-db-uspto-database
description: "Use when the task explicitly concerns scientific db uspto database. USPTO patent and trademark data workflow for official record lookup, PatentSearch queries, TSDR checks, assignment data, and reproducible IP research logs. Use when a task needs official United States patent or trademark records from USPTO systems."
metadata:
  origin: ECC-adaptation
---

# USPTO Database — portable workflow

USPTO patent and trademark data workflow for official record lookup, PatentSearch queries, TSDR checks, assignment data, and reproducible IP research logs. Use when a task needs official United States patent or trademark records from USPTO systems.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-scientific-pkg-gget`, `bosskuai-scientific-db-pubmed-database`, `bosskuai-mle-workflow`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Source Selection.
2. Authentication and Secrets.
3. PatentSearch Workflow.
4. Trademark/TSDR Workflow.
5. File Wrapper and Prosecution History.
6. Assignment Workflow.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- For clinical, compliance, legal, regulatory or financial conclusions, use current authoritative sources and an independent review; treat sample values and rules as examples until checked for the actual jurisdiction or system.

## Done when

Return the official patent/trademark record IDs, query/source/date and supported interpretation, separating lookup from legal advice.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
