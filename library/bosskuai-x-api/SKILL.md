---
name: bosskuai-x-api
description: "Use when the task explicitly concerns x api. X/Twitter API integration for posting tweets, threads, reading timelines, search, and analytics. Covers OAuth auth patterns, rate limits, and platform-native content posting. Use when the user wants to interact with X programmatically."
metadata:
  origin: ECC-adaptation
---

# X API — portable workflow

X/Twitter API integration for posting tweets, threads, reading timelines, search, and analytics. Covers OAuth auth patterns, rate limits, and platform-native content posting. Use when the user wants to interact with X programmatically.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-content-calendar`, `content-strategy`, `bosskuai-autonomous-loops`, `bosskuai-brand-voice`, `bosskuai-connections-optimizer`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Authentication.
2. OAuth 2.0 Bearer Token (App-Only).
3. Environment setup.
4. Search recent tweets.
5. OAuth 1.0a (User Context).
6. Environment setup — source before use.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check these first, live at work time. Your X app's access and billing setup can limit which endpoints you can call and how often. Check the API version the code calls, and X's developer changelog for deprecations. Then check the source prerequisites. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Apply the source “Authentication”, “OAuth 2.0 Bearer Token (App-Only)” guidance to the concrete request. Return the resulting x api artifact or diagnosis with source/command evidence for each conclusion.

- Set explicit connect and read timeouts. On a 429, wait until the `x-rate-limit-reset` time before you retry. If the API stays down or slow, return a clear error to the caller.
- Follow `meta.next_token` to the last page. Keep tweet and user IDs as strings, because a JavaScript number loses digits above 2^53. Validate the fields you read, and ignore extra ones.
- Before you retry a post, check whether the first one went through, because a retry can publish the same post twice. Log each request and response with the bearer token masked.
- Meet every check in the [shared quality bar](../../references/checklists/engineering-quality-bar.md).

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
