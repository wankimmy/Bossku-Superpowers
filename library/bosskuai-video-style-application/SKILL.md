---
name: bosskuai-video-style-application
description: "Use when the task explicitly concerns video style application. Generate new video against a distilled style pack and cut it into a finished piece - plan takes from the reference's cut rhythm, generate on fal, grade with the pack's measured LUT, cut at the measured cadence, weave in existing footage, composite overlay plates, mint 3D props, and verify the result numerically. Use when the user wants to make a video in a captured style, supplement existing footage, or assemble generated clips into a real edit."
metadata:
  origin: ECC-adaptation
---

# Taste Application — portable workflow

Generate new video against a distilled style pack and cut it into a finished piece - plan takes from the reference's cut rhythm, generate on fal, grade with the pack's measured LUT, cut at the measured cadence, weave in existing footage, composite overlay plates, mint 3D props, and verify the result numerically. Use when the user wants to make a video in a captured style, supplement existing footage, or assemble generated clips into a real edit.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-video-style-distillation`, `bosskuai-video-editing`, `bosskuai-performance-profiling`, `bosskuai-video-creative-direction`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Execution and Delivery Contract.
2. Division of Labour.
3. Generate TAKES, Not Shots.
4. Cutting Rules.
5. Grading Rules.
6. Recovered fal Platform Behavior.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- The full source bundle is kept, with 80 sidecar files. Its code is reference-only until its dependencies, paths and effects are reviewed; this import did not run it.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Validate generated file manifests, timeline references/durations and exported deliverables with the source verification procedure; provider costs need scoped approval.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
