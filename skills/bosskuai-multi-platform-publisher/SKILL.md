---
name: bosskuai-multi-platform-publisher
description: "Use when one article must go to several Chinese content platforms (知乎, 小红书, CSDN, B站, 公众号, 掘金): platform-fit check, per-platform rewrite, length limits, rate caps, and draft-only syncing for human review."
---

# BosskuAI Multi-Platform Publisher

Use this skill to turn one source article into platform-native drafts for several Chinese content platforms, stopping at drafts so a human presses publish.

## How this differs from nearby skills

- **`bosskuai-social-publisher`**: scheduling and publishing to Western social platforms through one service. This skill is about Chinese platforms, per-platform rewriting, and draft-only handoff.
- **`bosskuai-content-calendar`**: planning what to post and when. This skill executes one article across channels.
- **`bosskuai-zhihu-strategist`**, **`bosskuai-bilibili-content-strategist`**: platform strategy and voice. Use them to rewrite for those platforms.
- **`bosskuai-article-writing`**: writing the master draft.

## Workflow

1. Collect inputs: topic or source file, target platforms, cover image, tags, category, and whether the piece is original, translated, or reposted.
2. Fit check per platform. Mark each as fit, needs major rewrite, or skip. A deep technical tutorial suits developer platforms; casual experience pieces suit lifestyle platforms; skip platforms where the content type does not belong.
3. Show the parameter table and the fit result to the user and wait for confirmation before any sync.
4. Produce the master draft, then one adapted version per platform (voice, title, length, call to action, cover ratio). Do not paste identical text everywhere.
5. Preflight: check each platform's current title and body limits, image rules, required category or tags, and originality marker in the platform's own documentation. Check tool authentication and installed versions of the sync tool before running anything.
6. Sync as drafts only, with random gaps between posts on the same platform and no same-minute batches.
7. Report a table: platform, status, draft URL, notes. If a sync fails, diagnose first (token, port, expired login, length) and report the cause instead of retrying blindly.
8. Hand control back: the user reviews each draft and publishes manually.

## Guardrails

- Never publish live. Stop at drafts, and say so in the report.
- Do not fabricate tool output. If a tool is not installed, give the install step and stop.
- Credentials, cookies, and tokens stay in the user's environment and are never written to files or logs.
- Respect platform terms: label original, translated, or reposted accurately, credit sources, and do not use stolen content.
- Do not use tricks to evade platform risk control (image hash variation, mass posting). Keep the cadence human.
- Any run against a real account needs the user's explicit approval.

## Output format

```text
Source: [file/topic, original|translation|repost]
Platform fit: [platform - fit/rewrite/skip - reason]
Adaptations: [platform - title, length, CTA, cover]
Preflight: [auth, limits, images]
Result: | Platform | Status | Draft URL | Notes |
Next step: user reviews and publishes manually
```

Adapted from agency-agents/marketing/marketing-multi-platform-publisher.md (agency-agents, MIT).
