---
name: bosskuai-ios-icon-gen
description: "Use when the task explicitly concerns ios icon gen. Generate iOS app icons as PNG imagesets for Xcode asset catalogs from SF Symbols (5000+ Apple-native) or Iconify API (275k+ open source icons from 200+ collections). Use when generating icons, creating icon assets, adding icons to asset catalog, or searching for icons for iOS projects."
metadata:
  origin: ECC-adaptation
---

# iOS Icon Generator — portable workflow

Generate iOS app icons as PNG imagesets for Xcode asset catalogs from SF Symbols (5000+ Apple-native) or Iconify API (275k+ open source icons from 200+ collections). Use when generating icons, creating icon assets, adding icons to asset catalog, or searching for icons for iOS projects.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-codebase-analysis`, `bosskuai-opensource-pipeline`, `content-strategy`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Core Principles.
2. 1. Two Sources, One Output Format.
3. 2. Always Match Existing Style.
4. 3. Output Structure.
5. Step 1: Assess Requirements.
6. Check dimensions of existing icon.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- The full source bundle is kept, with 2 sidecar files. Its code is reference-only until its dependencies, paths and effects are reviewed; this import did not run it.

## Done when

Complete the source “1. Two Sources, One Output Format”, “3. Output Structure” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
