---
name: bosskuai-recsys-pipeline-architect
description: "Use when the task explicitly concerns recsys pipeline architect. Design composable recommendation, ranking, and feed pipelines using the six-stage Source→Hydrator→Filter→Scorer→Selector→SideEffect framework popularized by xAI's open-sourced For You algorithm. Use this skill whenever the user is building any system that picks \"the top K items for a (user, context)\" — social feeds, content CMSs, RAG rerankers, task prioritizers, notification triage, search reranking, ad ranking."
metadata:
  origin: ECC-adaptation
---

# recsys-pipeline-architect — portable workflow

## Job and activation

Design composable recommendation, ranking, and feed pipelines using the six-stage Source→Hydrator→Filter→Scorer→Selector→SideEffect framework popularized by xAI's open-sourced For You algorithm. Use this skill whenever the user is building any system that picks "the top K items for a (user, context)" — social feeds, content CMSs, RAG rerankers, task prioritizers, notification triage, search reranking, ad ranking.

Use this skill for that specific domain, framework, data source or artifact. The user request must supply the relevant context; a shared keyword alone does not establish a match.

Nearby owners: `bosskuai-brand-voice`, `bosskuai-github-workflow`, `bosskuai-regex-vs-llm-structured-text`. Select them only for their separate concerns; do not load multiple general workflows for the same job.

## Source workflow

Read [the complete source workflow](references/upstream/SKILL.md) before applying its examples. Work through the following source sections in order:

1. The six-stage framework.
2. Why this exact order.
3. Workflow when invoked.
4. Key trade-offs to surface (don't default silently).
5. 1. Single score vs multi-action prediction.
6. 2. Candidate isolation in scoring.

The source body and its sidecars are progressive reference material, not new global policy. Resolve its relative `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names resolve through [the source map](SOURCE.json); use the current host skill loader or `bossku skills show <mapped-id>`. Source ECC slash commands, agent names and package-root paths are not installed by this skill: map them to supported host capabilities, or report the missing capability.

Related supported owners: `bosskuai-brand-voice`, `bosskuai-github-workflow`, `bosskuai-performance-profiling`, `bosskuai-regex-vs-llm-structured-text`.

## Prerequisites and execution boundary

Inspect the project/tool versions and the source prerequisites first. Use repository scripts and installed dependencies where present. A documented command is an example to inspect, not permission to install packages, add an account, expose secrets, upload private content or mutate an external service. Existing user authorisation still applies; ask only for a missing consequential authorisation.

This domain can require a named provider/MCP/API. Discover available tools, verify the documented surface and scope, and report unavailable capabilities. Do not replace a missing provider with invented output.

## Pass signal

Complete the source “Workflow when invoked” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

## Stop conditions

Stop the affected operation when an input/contract is missing, a provider/runtime is unavailable, source instructions reference unsupported commands, or a requested mutation lacks authorisation. Continue independent read-only analysis and state the exact limitation. Do not claim completion from a generated plan alone.

## Attribution

Adapted from the locally reviewed `affaan-m/ECC` snapshot; provenance and content hashes are in [SOURCE.json](SOURCE.json). The complete original text/resources remain in [references/upstream/](references/upstream/SKILL.md), under the retained [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
