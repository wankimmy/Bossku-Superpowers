---
name: bosskuai-douyin-strategist
description: "Use when planning Douyin short videos or livestream commerce: 3-second hook scripts, completion-rate tests, DOU+ audience tests, matrix accounts, livestream product sequencing, and ad-law-safe wording."
---

# BosskuAI Douyin Strategist

Use this skill to plan Douyin short-video scripts, traffic tests, and livestream sales sessions, judged by completion rate and conversion rather than by how the video looks.

## How this differs from nearby skills

- **`bosskuai-bilibili-content-strategist`**: long-form, community-driven video on Bilibili. Douyin is short, vertical, and hook-first.
- **`social`**: Western short-video platforms (TikTok, Reels). Douyin has its own ad tools (DOU+, Qianchuan), commerce rules, and compliance limits.
- **`bosskuai-content-calendar`**: generic content planning. Use it for cadence; use this skill for scripts, boosts, and live sessions.
- **`ads`** and **`ad-creative`**: paid campaigns on global ad platforms. Here paid traffic is a test input to the video plan.
- **`video`**, **`bosskuai-video-editing`**: producing and editing the footage.

## Workflow

1. Diagnose the account: follower mix, which videos got reach, traffic sources, and the monetization path (product sales, leads, brand).
2. Pick a content matrix: educational, story, product review, vlog. Assign a target length by type (check what the account's own data supports).
3. Write each script with a hook in the first 3 seconds (conflict, value, suspense, or relatability), core content (pain point, solution, demo, proof), and a close with one engagement prompt.
4. State a completion-rate hypothesis per video and the one change you will test (hook type, demo position, length).
5. Shooting notes: vertical 9:16, subtitles on, on-camera talent if it tests better, current trending audio checked for commercial-use rights.
6. Traffic test: use DOU+ or similar boosts as small audience-targeting experiments. Compare audience segments before scaling spend.
7. Livestream plan: set a product mix (traffic item, profit item, prestige item, limited deal), a time-boxed segment plan, a script per segment, and a post-stream review of average watch time, conversion, and revenue per thousand views.
8. Review weekly: completion, interaction, follower growth, and what the best and worst videos had in common. Change one variable at a time.

## Guardrails

- Advertising law: no absolute claims ("best", "number one", "100% effective"); food, drug, health, and cosmetic categories have extra rules. Check current regulations and platform ad policy, and use a human reviewer for regulated categories.
- No false urgency, fake scarcity, or invented testimonials in livestreams.
- Follow minor-protection policies. Do not direct viewers off-platform where the platform restricts it.
- Do not treat sample percentages or spend ratios as targets. Set them from the account's own baseline and budget.
- Boost spend and any purchase need explicit user approval.

## Output format

```text
Account diagnosis: [audience, traffic sources, gap]
Video plan: [format, length, hook type, completion hypothesis]
Script: [0-3s hook / core / close]
Test: [one variable, how measured, decision rule]
Livestream plan: [product mix, segment timeline, review metrics]
Compliance check: [claims reviewed, categories, reviewer]
```

Adapted from agency-agents/marketing/marketing-douyin-strategist.md (agency-agents, MIT).
