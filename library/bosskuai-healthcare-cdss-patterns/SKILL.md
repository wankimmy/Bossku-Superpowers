---
name: bosskuai-healthcare-cdss-patterns
description: "Use when the task explicitly concerns healthcare cdss patterns. Clinical Decision Support System (CDSS) development patterns. Drug interaction checking, dose validation, clinical scoring (NEWS2, qSOFA), alert severity classification, and integration into EMR workflows. Use when building clinical decision support — drug interaction checks, dose validation, clinical scoring, or alert severity."
metadata:
  origin: ECC-adaptation
---

# Healthcare CDSS Development Patterns — portable workflow

Clinical Decision Support System (CDSS) development patterns. Drug interaction checking, dose validation, clinical scoring (NEWS2, qSOFA), alert severity classification, and integration into EMR workflows. Use when building clinical decision support — drug interaction checks, dose validation, clinical scoring, or alert severity.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-healthcare-emr-patterns`, `bosskuai-devops-iac`, `bosskuai-healthcare-eval-harness`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. Drug Interaction Checking.
3. Dose Validation.
4. Clinical Scoring: NEWS2.
5. Alert Severity and UI Behavior.
6. Testing CDSS (Zero Tolerance for False Negatives).

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- For clinical, compliance, legal, regulatory or financial conclusions, use current authoritative sources and an independent review; treat sample values and rules as examples until checked for the actual jurisdiction or system.

## Done when

Apply the source “How It Works”, “Drug Interaction Checking” guidance to the concrete request. Return the resulting healthcare cdss development patterns artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

The shared quality bar: `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
