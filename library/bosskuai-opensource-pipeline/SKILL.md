---
name: bosskuai-opensource-pipeline
description: "Use when the task explicitly concerns opensource pipeline. Open-source pipeline: fork, sanitize, and package private projects for safe public release. Chains 3 agents (forker, sanitizer, packager). Triggers: '/opensource', 'open source this', 'make this public', 'prepare for open source'. Use when a private project must be forked, stripped of secrets, and packaged for public release."
metadata:
  origin: ECC-adaptation
---

# Open-Source Pipeline Skill — portable workflow

Open-source pipeline: fork, sanitize, and package private projects for safe public release. Chains 3 agents (forker, sanitizer, packager). Triggers: '/opensource', 'open source this', 'make this public', 'prepare for open source'. Use when a private project must be forked, stripped of secrets, and packaged for public release.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-codebase-analysis`, `bosskuai-ios-icon-gen`, `bosskuai-permanent-memory-orchestration`, `bosskuai-cybersecurity-risk`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Commands.
2. Protocol.
3. /opensource fork PROJECT.
4. /opensource verify PROJECT.
5. /opensource package PROJECT.
6. /opensource list.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the git version, and the version and latest rule update of the secret-detection patterns the pipeline's Secrets scan uses (see `bosskuai-cybersecurity-risk`), checked live at work time, and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Complete the source “/opensource verify PROJECT” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

- Scan every branch, tag and past commit, not only the current files (`git log --all` lists the commits). Deleting a secret from the files does not remove it from history, so tell the user every real key the scan finds, and do not publish until the user confirms each one is rotated.
- Replace real personal or customer data in fixtures and sample logs with fake data of the same shape. Then run the tests and the build on the public copy, not only the private one.
- Check the licence of every dependency, and get the user's go-ahead before the first push to a public remote.
- Meet every check in the [shared quality bar](../../references/checklists/engineering-quality-bar.md).

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
