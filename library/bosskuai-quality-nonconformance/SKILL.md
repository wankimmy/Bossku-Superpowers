---
name: bosskuai-quality-nonconformance
description: "Use when the task explicitly concerns quality nonconformance. Quality control and non-conformance management for regulated manufacturing (FDA 21 CFR 820, IATF 16949, AS9100): NCR lifecycle and disposition, 5-Why/Ishikawa/fault-tree/8D root cause analysis, CAPA systems, SPC interpretation, AQL sampling, and supplier quality audits. Use when investigating non-conformances, performing root cause analysis, managing CAPAs, interpreting SPC data, or handling supplier quality issues."
metadata:
  origin: ECC-adaptation
---

# Quality & Non-Conformance Management — portable workflow

Quality control and non-conformance management for regulated manufacturing (FDA 21 CFR 820, IATF 16949, AS9100): NCR lifecycle and disposition, 5-Why/Ishikawa/fault-tree/8D root cause analysis, CAPA systems, SPC interpretation, AQL sampling, and supplier quality audits. Use when investigating non-conformances, performing root cause analysis, managing CAPAs, interpreting SPC data, or handling supplier quality issues.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-logistics-exception-management`, `bosskuai-operations`, `bosskuai-returns-reverse-logistics`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Role and Context.
2. How It Works.
3. Core Knowledge.
4. NCR Lifecycle.
5. Root Cause Analysis.
6. CAPA System.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.
- For clinical, compliance, legal, regulatory or financial conclusions, use current authoritative sources and an independent review; treat sample values and rules as examples until checked for the actual jurisdiction or system.

## Done when

Complete the source “Quality & Non-Conformance Management”, “Supplier Quality Management” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
