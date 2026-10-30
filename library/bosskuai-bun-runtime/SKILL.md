---
name: bosskuai-bun-runtime
description: "Use when the task explicitly concerns bun runtime. Bun as runtime, package manager, bundler, and test runner. When to choose Bun vs Node, migration notes, and Vercel support."
metadata:
  origin: ECC-adaptation
---

# Bun Runtime — portable workflow

Bun as runtime, package manager, bundler, and test runner. When to choose Bun vs Node, migration notes, and Vercel support.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. Run and install.
3. Run a script or file.
4. Scripts and env.
5. Testing.
6. Runtime API.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions first: `bun --version` for the installed Bun, the lockfile (`bun.lock` or `bun.lockb`), and the `@types/bun` version in `package.json`. Check the latest stable Bun release at work time on bun.sh, and use only APIs that exist in the installed version. Node APIs that Bun implements can behave differently, so check each one against the Bun docs for that version. Also check the source prerequisites. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Apply the source “How It Works”, “Run and install” guidance to the concrete request. Return the resulting bun runtime artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Also check before you finish: CI and production run the same Bun version; the build uses `bun install --frozen-lockfile`, so it fails on an out-of-date lockfile instead of changing it; `bun test` runs clean; and each Node API the code uses works on the installed Bun. The full quality bar is in `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
