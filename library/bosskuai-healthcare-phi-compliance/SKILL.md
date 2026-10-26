---
name: bosskuai-healthcare-phi-compliance
description: "Use when the task explicitly concerns healthcare phi compliance. Protected Health Information (PHI) and PII compliance patterns for healthcare applications: data classification, row-level access control, tamper-proof audit trails, schema tagging, and common leak vectors such as logs, URLs, and browser storage. Use when code touches patient or clinician data, when implementing HIPAA or GDPR access controls, or when auditing a healthcare system for data exposure."
metadata:
  origin: ECC-adaptation
---

# Healthcare PHI/PII Compliance Patterns — portable workflow

Protected Health Information (PHI) and PII compliance patterns for healthcare applications: data classification, row-level access control, tamper-proof audit trails, schema tagging, and common leak vectors such as logs, URLs, and browser storage. Use when code touches patient or clinician data, when implementing HIPAA or GDPR access controls, or when auditing a healthcare system for data exposure.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-design-systems`, `bosskuai-healthcare-emr-patterns`, `accessibility`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. Data Classification.
3. Access Control: Row-Level Security.
4. Audit Trail.
5. Common Leak Vectors.
6. Database Schema Tagging.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.
- For clinical, compliance, legal, regulatory or financial conclusions, use current authoritative sources and an independent review; treat sample values and rules as examples until checked for the actual jurisdiction or system.

## Done when

Complete the source “Deployment Checklist” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
