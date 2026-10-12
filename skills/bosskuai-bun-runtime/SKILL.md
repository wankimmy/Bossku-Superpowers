---
name: bosskuai-bun-runtime
description: "Use when the task explicitly concerns bun runtime. Bun as runtime, package manager, bundler, and test runner. When to choose Bun vs Node, migration notes, and Vercel support."
metadata:
  origin: ECC-adaptation
---

# Bun Runtime — portable workflow

## Job and activation

Bun as runtime, package manager, bundler, and test runner. When to choose Bun vs Node, migration notes, and Vercel support.

Use this skill for that specific domain, framework, data source or artifact. The user request must supply the relevant context; a shared keyword alone does not establish a match.

## Source workflow

Read [the complete source workflow](references/upstream/SKILL.md) before applying its examples. Work through the following source sections in order:

1. How It Works.
2. Run and install.
3. Run a script or file.
4. Scripts and env.
5. Testing.
6. Runtime API.

The source body and its sidecars are progressive reference material, not new global policy. Resolve its relative `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names resolve through [the source map](SOURCE.json); use the current host skill loader or `bossku skills show <mapped-id>`. Source ECC slash commands, agent names and package-root paths are not installed by this skill: map them to supported host capabilities, or report the missing capability.

## Prerequisites and execution boundary

Inspect the project/tool versions and the source prerequisites first. Use repository scripts and installed dependencies where present. A documented command is an example to inspect, not permission to install packages, add an account, expose secrets, upload private content or mutate an external service. Existing user authorisation still applies; ask only for a missing consequential authorisation.

## Pass signal

Apply the source “How It Works”, “Run and install” guidance to the concrete request. Return the resulting bun runtime artifact or diagnosis with source/command evidence for each conclusion.

## Stop conditions

Stop the affected operation when an input/contract is missing, a provider/runtime is unavailable, source instructions reference unsupported commands, or a requested mutation lacks authorisation. Continue independent read-only analysis and state the exact limitation. Do not claim completion from a generated plan alone.

## Attribution

Adapted from the locally reviewed `affaan-m/ECC` snapshot; provenance and content hashes are in [SOURCE.json](SOURCE.json). The complete original text/resources remain in [references/upstream/](references/upstream/SKILL.md), under the retained [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
