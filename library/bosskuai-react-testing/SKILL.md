---
name: bosskuai-react-testing
description: "Use when the task explicitly concerns react testing. React component testing with React Testing Library, Vitest/Jest, MSW for network mocking, accessibility assertions with axe, and the decision boundary between component tests and Playwright/Cypress end-to-end runs. Use when writing or fixing tests for React components, hooks, or pages."
metadata:
  origin: ECC-adaptation
---

# React Testing — portable workflow

React component testing with React Testing Library, Vitest/Jest, MSW for network mocking, accessibility assertions with axe, and the decision boundary between component tests and Playwright/Cypress end-to-end runs. Use when writing or fixing tests for React components, hooks, or pages.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-react-development`, `e2e-testing`, `bosskuai-browser-automation`, `accessibility`, `bosskuai-tdd-loop`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Core Principle.
2. Library Choice.
3. Query Priority.
4. User Interaction with `userEvent`.
5. Async Patterns.
6. Network Mocking with MSW.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

A behaviour-focused component/hook test passes with awaited user interactions, accessible queries and observable state/network outcomes.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
