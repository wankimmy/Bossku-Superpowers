---
name: bosskuai-module-regression
description: "Use when the task explicitly concerns module regression. Govern cross-module regression in large repositories with a REGRESSION.md ledger that records each module's downstream consumers and executable acceptance command. After a change, run the changed module and every affected downstream command, and use observed exit codes as regression evidence under the project's delivery policy. Use for module regression, regression ledgers, impact audits, downstream verification, and changes where modifying A may break B."
metadata:
  origin: ECC-adaptation
---

# Module Regression Ledger — portable workflow

Govern cross-module regression in large repositories with a REGRESSION.md ledger that records each module's downstream consumers and executable acceptance command. After a change, run the changed module and every affected downstream command, and use observed exit codes as regression evidence under the project's delivery policy. Use for module regression, regression ledgers, impact audits, downstream verification, and changes where modifying A may break B.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-codebase-analysis`, `bosskuai-test-collaboration`, `bosskuai-browser-automation`, `bosskuai-contract-first`, `bosskuai-qa-automation-strategy`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Anti-Patterns.
2. Problem.
3. Three Required Fields per Module.
4. Module 03 — Shop Data Cleaning.
5. Connection to TESTS.md.
6. Ledger Discipline.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check each module's language version and test runner version in its manifest or lockfile, and each one's latest stable release, checked live at work time, and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- The full source bundle is kept, with 1 sidecar file. Its code is reference-only until its dependencies, paths and effects are reviewed; this import did not run it.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Apply the source “Anti-Patterns”, “Problem” guidance to the concrete request. Return the resulting module regression ledger artifact or diagnosis with source/command evidence for each conclusion.

- After a change, run the changed module's tests and every downstream command in `REGRESSION.md` that does not install packages, add an account, expose secrets, upload private content or change an external service. Ask first for any other downstream command, and record each exit code and each command not run.
- Check the ledger's consumer list against the code by searching for imports and calls of the module. A consumer missing from the ledger is a regression nobody checks.
- A consumer can break on a changed type or a removed field while the module's own tests pass. Test each consumer's use of the output with a copy of production data, types included.
- Meet every check in the [shared quality bar](../../references/checklists/engineering-quality-bar.md).

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
