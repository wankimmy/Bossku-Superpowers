---
name: bosskuai-story-lifecycle
description: "Use when the task explicitly concerns story lifecycle. Manage a file-based epic → story → sprint development loop without requiring an external project management tool. Creates and tracks epics, breaks them into user stories, assigns them to sprints, and drives implementation story by story. Use when starting a new feature initiative or when the team has no Jira/Linear/Taiga but needs structured delivery tracking."
metadata:
  origin: ECC-adaptation
---

# Story Lifecycle — portable workflow

Manage a file-based epic → story → sprint development loop without requiring an external project management tool. Creates and tracks epics, breaks them into user stories, assigns them to sprints, and drives implementation story by story. Use when starting a new feature initiative or when the team has no Jira/Linear/Taiga but needs structured delivery tracking.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-flox-environments`, `bosskuai-agent-architecture-audit`, `bosskuai-continuous-learning`, `bosskuai-council`, `bosskuai-project-flow-ops`, `bosskuai-tdd-loop`, `verification-before-completion`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Authority.
2. Boundary with GitHub-backed coordination.
3. Directory Layout.
4. Naming and path contract.
5. Writes go through the ledger helper.
6. Commands.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- The full source bundle is kept, with 1 sidecar file. Its code is reference-only until its dependencies, paths and effects are reviewed; this import did not run it.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Workflow” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
