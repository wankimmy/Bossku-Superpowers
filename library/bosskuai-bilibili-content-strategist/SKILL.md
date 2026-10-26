---
name: bosskuai-bilibili-content-strategist
description: "Use when planning Bilibili (B站) content: UP主 channel positioning, cover and title testing, danmaku interaction design, first-hour launch plan, and sponsored-video (恰饭) integration that the community accepts."
---

# BosskuAI Bilibili Content Strategist

Use this skill to plan a Bilibili channel or a single video so it fits the platform's long-form, community-first culture, with measured packaging tests instead of guesses.

## How this differs from nearby skills

- **`bosskuai-baidu-seo-specialist`**: Baidu search ranking for a website. This skill is video content on one social platform.
- **`bosskuai-content-calendar`**: generic multi-platform calendars and hooks. Use it for the calendar shell; use this skill for Bilibili-specific packaging, danmaku, and sponsorship rules.
- **`social`**: Western-platform social content and listening. Bilibili's tag pools, fan medals, and danmaku are not covered there.
- **`bosskuai-douyin-strategist`** and **`bosskuai-zhihu-strategist`**: sibling platform skills. Bilibili rewards long, effortful videos; Douyin rewards 3-second hooks; Zhihu rewards written credibility. Do not reuse one plan across them.
- **`video`** and **`bosskuai-video-editing`**: producing and cutting the video itself.

## Workflow

1. Positioning: pick one content vertical (knowledge, tech, life, food, gaming), a voice, the one-line reason to follow, and what makes the channel different from the top three in that vertical.
2. Research: read the vertical's recent hot and weekly-pick lists, note what completion rate and interaction signals the platform currently surfaces (check current platform help pages; recommendation rules change).
3. Content mix: split the plan into pillar deep-dives, timely topic responses, community content, and experiments. Choose the ratio from the channel's capacity, not from a template.
4. Danmaku design: at storyboard stage, list timestamps where a line, reveal, question, or callback should invite audience comments. Prepare a small set of seed comments for launch.
5. Packaging: write two cover and two title variants. Cover must read at thumbnail size, with short bold text and a brand-consistent palette. Titles can carry a curiosity hook but should not be clickbait the community will reject. Use the platform's own cover test tool where available.
6. Launch: pre-announce in feed posts, publish at a time your audience is active, reply to early comments, watch first-hour metrics.
7. Review: record completion rate, interaction rate, follower change, and where retention drops. Turn each drop into a change for the next video.
8. Sponsored content: make the viewer value clear first, disclose the sponsorship, and fit the product into the video's story. Check current commercial-platform rules before quoting terms.

## Guardrails

- Targets such as view counts, triple-combo rates, or growth rates are set from the channel's own baseline, not copied from a template.
- Disclose sponsorships as the platform and local advertising rules require. Check the current rules; this skill does not give legal advice.
- Do not buy views, fake danmaku at scale, or run comment brigades. Light seeding with real, relevant comments is the limit.
- Cross-posting to other platforms needs a rewrite for that platform, not a copy.

## Output format

```text
Channel / video: [name, vertical, audience]
Positioning: [one-line reason to follow]
Content mix: [pillar / timely / community / experiment, with reasons]
Danmaku map: [timestamp - moment - expected reaction]
Packaging tests: [cover A/B, title A/B, success metric]
Launch plan: [pre-announce, publish time, first-hour actions]
Review metrics: [completion, interaction, follower change, drop points]
```

Adapted from agency-agents/marketing/marketing-bilibili-content-strategist.md (agency-agents, MIT).
