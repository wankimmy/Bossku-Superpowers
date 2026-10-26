---
name: bosskuai-recsys-pipeline-architect
description: "Use when the task explicitly concerns recsys pipeline architect. Design composable recommendation, ranking, and feed pipelines using the six-stage Source→Hydrator→Filter→Scorer→Selector→SideEffect framework popularized by xAI's open-sourced For You algorithm. Use this skill whenever the user is building any system that picks \"the top K items for a (user, context)\" — social feeds, content CMSs, RAG rerankers, task prioritizers, notification triage, search reranking, ad ranking."
metadata:
  origin: ECC-adaptation
---

# recsys-pipeline-architect — portable workflow

Design composable recommendation, ranking, and feed pipelines using the six-stage Source→Hydrator→Filter→Scorer→Selector→SideEffect framework popularized by xAI's open-sourced For You algorithm. Use this skill whenever the user is building any system that picks "the top K items for a (user, context)" — social feeds, content CMSs, RAG rerankers, task prioritizers, notification triage, search reranking, ad ranking.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-brand-voice`, `bosskuai-github-workflow`, `bosskuai-regex-vs-llm-structured-text`, `bosskuai-performance-profiling`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. The six-stage framework.
2. Why this exact order.
3. Workflow when invoked.
4. Key trade-offs to surface (don't default silently).
5. 1. Single score vs multi-action prediction.
6. 2. Candidate isolation in scoring.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Workflow when invoked” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
