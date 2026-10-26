---
name: bosskuai-returns-reverse-logistics
description: "Use when the task explicitly concerns returns reverse logistics. Codified expertise for returns authorization, receipt and inspection, disposition decisions, refund processing, fraud detection, and warranty claims management. Informed by returns operations managers with 15+ years experience. Includes grading frameworks, disposition economics, fraud pattern recognition, and vendor recovery processes. Use when handling product returns, reverse logistics, refund decisions, return fraud detection, or warranty claims."
metadata:
  origin: ECC-adaptation
---

# Returns & Reverse Logistics — portable workflow

Codified expertise for returns authorization, receipt and inspection, disposition decisions, refund processing, fraud detection, and warranty claims management. Informed by returns operations managers with 15+ years experience. Includes grading frameworks, disposition economics, fraud pattern recognition, and vendor recovery processes. Use when handling product returns, reverse logistics, refund decisions, return fraud detection, or warranty claims.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-logistics-exception-management`, `bosskuai-production-scheduling`, `architecture-decision-records`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Role and Context.
2. How It Works.
3. Core Knowledge.
4. Returns Policy Logic.
5. Inspection and Grading.
6. Disposition Decision Trees.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- For clinical, compliance, legal, regulatory or financial conclusions, use current authoritative sources and an independent review; treat sample values and rules as examples until checked for the actual jurisdiction or system.

## Done when

Apply the source “Role and Context”, “How It Works” guidance to the concrete request. Return the resulting returns & reverse logistics artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
