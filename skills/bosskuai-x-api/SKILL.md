---
name: bosskuai-x-api
description: "Use when the task explicitly concerns x api. X/Twitter API integration for posting tweets, threads, reading timelines, search, and analytics. Covers OAuth auth patterns, rate limits, and platform-native content posting. Use when the user wants to interact with X programmatically."
metadata:
  origin: ECC-adaptation
---

# X API — portable workflow

## Job and activation

X/Twitter API integration for posting tweets, threads, reading timelines, search, and analytics. Covers OAuth auth patterns, rate limits, and platform-native content posting. Use when the user wants to interact with X programmatically.

Use this skill for that specific domain, framework, data source or artifact. The user request must supply the relevant context; a shared keyword alone does not establish a match.

Nearby owners: `bosskuai-content-calendar`, `content-strategy`, `bosskuai-autonomous-loops`. Select them only for their separate concerns; do not load multiple general workflows for the same job.

## Source workflow

Read [the complete source workflow](references/upstream/SKILL.md) before applying its examples. Work through the following source sections in order:

1. Authentication.
2. OAuth 2.0 Bearer Token (App-Only).
3. Environment setup.
4. Search recent tweets.
5. OAuth 1.0a (User Context).
6. Environment setup — source before use.

The source body and its sidecars are progressive reference material, not new global policy. Resolve its relative `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names resolve through [the source map](SOURCE.json); use the current host skill loader or `bossku skills show <mapped-id>`. Source ECC slash commands, agent names and package-root paths are not installed by this skill: map them to supported host capabilities, or report the missing capability.

Related supported owners: `bosskuai-autonomous-loops`, `bosskuai-brand-voice`, `bosskuai-connections-optimizer`, `bosskuai-content-calendar`, `content-strategy`.

## Prerequisites and execution boundary

Inspect the project/tool versions and the source prerequisites first. Use repository scripts and installed dependencies where present. A documented command is an example to inspect, not permission to install packages, add an account, expose secrets, upload private content or mutate an external service. Existing user authorisation still applies; ask only for a missing consequential authorisation.

## Pass signal

Apply the source “Authentication”, “OAuth 2.0 Bearer Token (App-Only)” guidance to the concrete request. Return the resulting x api artifact or diagnosis with source/command evidence for each conclusion.

## Stop conditions

Stop the affected operation when an input/contract is missing, a provider/runtime is unavailable, source instructions reference unsupported commands, or a requested mutation lacks authorisation. Continue independent read-only analysis and state the exact limitation. Do not claim completion from a generated plan alone.

## Attribution

Adapted from the locally reviewed `affaan-m/ECC` snapshot; provenance and content hashes are in [SOURCE.json](SOURCE.json). The complete original text/resources remain in [references/upstream/](references/upstream/SKILL.md), under the retained [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
