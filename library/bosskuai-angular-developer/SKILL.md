---
name: bosskuai-angular-developer
description: "Use when the task explicitly concerns angular developer. Generates Angular code and provides architectural guidance. Trigger when creating projects, components, or services, or for best practices on reactivity (signals, linkedSignal, resource), forms, dependency injection, routing, SSR, accessibility (ARIA), animations, styling (component styles, Tailwind CSS), testing, or CLI tooling."
metadata:
  origin: ECC-adaptation
---

# Angular Developer Guidelines — portable workflow

Generates Angular code and provides architectural guidance. Trigger when creating projects, components, or services, or for best practices on reactivity (signals, linkedSignal, resource), forms, dependency injection, routing, SSR, accessibility (ARIA), animations, styling (component styles, Tailwind CSS), testing, or CLI tooling.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `vue-patterns`, `bosskuai-dotnet-patterns`, `bosskuai-fastapi-development`, `accessibility`, `bosskuai-cybersecurity-risk`, `bosskuai-react-development`, `bosskuai-tdd-loop`, `e2e-testing`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Creating New Projects.
2. Components.
3. Reactivity and Data Management.
4. Forms.
5. Dependency Injection.
6. Angular Aria.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions first: the `@angular/core` version in `package.json` and the lockfile, the Node version in `.nvmrc` or `package.json` `engines`, and `ng version` for the installed CLI. Check the latest stable Angular release and its support dates at work time on angular.dev, and use only APIs that exist in the installed version. Also check the source prerequisites. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- The full source bundle is kept, with 35 sidecar files. Its code is reference-only until its dependencies, paths and effects are reviewed; this import did not run it.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Apply the source “Creating New Projects”, “Components” guidance to the concrete request. Return the resulting angular developer guidelines artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Also check before you finish: a money value is sent as the type the API contract says, never a float by accident; a double click cannot submit twice (disable the button while the request is open); `HttpClient` calls have a timeout, and only safe calls (GET) are retried; and `ng build` and `ng test` run clean. The full quality bar is in `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
