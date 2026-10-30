---
name: bosskuai-nextjs-turbopack
description: "Use when the task explicitly concerns nextjs turbopack. Next.js 16+ and Turbopack guidance — incremental Rust bundling, file-system caching, faster dev startup and HMR, Turbopack vs webpack tradeoffs, and the middleware.ts to proxy.ts filename change. Use when developing or debugging Next.js 16+ apps, diagnosing slow dev startup or hot reload, choosing between bundlers, or reviewing middleware/proxy file naming."
metadata:
  origin: ECC-adaptation
---

# Next.js and Turbopack — portable workflow

Next.js 16+ and Turbopack guidance — incremental Rust bundling, file-system caching, faster dev startup and HMR, Turbopack vs webpack tradeoffs, and the middleware.ts to proxy.ts filename change. Use when developing or debugging Next.js 16+ apps, diagnosing slow dev startup or hot reload, choosing between bundlers, or reviewing middleware/proxy file naming.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-django-patterns`, `bosskuai-tinystruct-patterns`, `bosskuai-agent-benchmark-comparison`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. Commands.
3. Usage.
4. Middleware File Naming.
5. Best Practices.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions first: the Node version in `.nvmrc`, `.node-version` or `package.json` `engines`, and the `next` and `react` versions in `package.json` and the lockfile (`npx next --version` prints the installed Next.js). Check the latest stable Next.js release at work time on nextjs.org. Bundler flags and defaults change between major versions, so read the docs for the installed one and use only options that exist in it. Also check the source prerequisites. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Apply the source “How It Works”, “Commands” guidance to the concrete request. Return the resulting next.js and turbopack artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Also check before you finish:

- `next build` passes with no type errors. `typescript.ignoreBuildErrors` is not `true` in the Next config.
- Every Server Action and route handler checks the user's rights itself. Anyone can send a request to it.
- No secret has a `NEXT_PUBLIC_` name. Those values ship in the browser bundle.
- A deploy keeps the previous build's chunks for one release. An open tab then does not fail on a chunk that is gone.

The full quality bar is in `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
