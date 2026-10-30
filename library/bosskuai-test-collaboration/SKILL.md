---
name: bosskuai-test-collaboration
description: "Use when the task explicitly concerns test collaboration. Inventory and govern a project's test assets. Connect requirements, business rules, risks, bugs, and cross-boundary contracts to stable TEST-IDs and executable evidence in the repository's existing test registry or TESTS.md. Use for test inventory, test gap analysis, unit/integration/contract/E2E/smoke classification, bug-to-test regression protection, consumer/provider contract testing, test-necessity review, and pre-delivery evidence review."
metadata:
  origin: ECC-adaptation
---

# Test Collaboration Governance — portable workflow

Inventory and govern a project's test assets. Connect requirements, business rules, risks, bugs, and cross-boundary contracts to stable TEST-IDs and executable evidence in the repository's existing test registry or TESTS.md. Use for test inventory, test gap analysis, unit/integration/contract/E2E/smoke classification, bug-to-test regression protection, consumer/provider contract testing, test-necessity review, and pre-delivery evidence review.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-module-regression`, `bosskuai-codebase-analysis`, `bosskuai-csharp-testing`, `bosskuai-contract-first`, `bosskuai-documentation-lookup`, `bosskuai-qa-automation-strategy`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Anti-Patterns.
2. Trust Boundary.
3. Goal.
4. Responsibility Boundary.
5. Read Before Starting.
6. 1. Inventory Existing Test Assets.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- The full source bundle is kept, with 1 sidecar file. Its code is reference-only until its dependencies, paths and effects are reviewed; this import did not run it.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Output” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

The shared quality bar: `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
