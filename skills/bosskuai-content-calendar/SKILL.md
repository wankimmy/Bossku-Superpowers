---
name: bosskuai-content-calendar
description: "Use when planning or distributing content: calendars, platform-specific posts, hooks, CTAs, content pillars, Malaysian mixed Malay-English tone, repurposing, cross-posting, scheduled publishing, and publishing cadence."
---

# BosskuAI Content Calendar

Use this skill when the output is a content plan, posting calendar, campaign sequence, or social media operating rhythm.

## How this differs from nearby skills

- **`social`**: platform strategy, hook formulas, carousels, short-form scripts, listening; load it for post craft. This skill owns the dated calendar, audience split, per-post CTA and metric, and Malay-English tone.

## Operating principles

- Read `.agents/product-marketing.md` first if it exists, for ICP, positioning, and voice already defined.
- Start from audience, objective, offer, and CTA.
- Separate customer-facing content from vendor/partner-facing content.
- Use content pillars, not random daily topics.
- Keep copy platform-native: Threads, TikTok, Instagram, LinkedIn, blog, and email behave differently.
- For Malaysian audiences, use simple Malay + English only when it improves clarity and relatability.

## Checklist

- Objective: awareness, engagement, lead gen, vendor signup, conversion, retention.
- Audience: customer, vendor, buyer, HR, founder, developer, etc.
- CTA: exact URL or action mapped to each post.
- Pillars: education, proof, pain point, behind-the-scenes, comparison, objection handling, offer.
- Cadence: dates, time slots, topic, hook, post body, CTA, suggested community/hashtag.
- Measurement: saves, replies, clicks, signups, leads, booked calls, conversion rate.

## Guardrails

- Do not create generic motivational filler.
- Do not reuse the same CTA blindly when audience intent differs.
- Do not make unsupported claims; mark proof needed.
- Do not over-polish social copy until it sounds like a corporate AI ad.

## Output format

```text
Campaign goal: [goal]
Audience split: [segments]
Pillars: [list]
Calendar:
  Date | Time | Platform | Audience | Topic | Hook | Post | CTA | Metric
Reuse plan: [how to convert one idea into multiple formats]
```

## Distribute and publish

After the calendar is agreed, two adapted ECC workflows (MIT, provenance in each `SOURCE.json`) cover the last step:

- **Cross-post** one idea natively to X, LinkedIn, Threads and Bluesky, never the same text everywhere: [`references/crosspost/SKILL.md`](references/crosspost/SKILL.md).
- **Schedule and publish** to up to 13 platforms through the SocialClaw service: [`references/social-publisher/SKILL.md`](references/social-publisher/SKILL.md). It needs a SocialClaw account and API key from the user; if either is missing, deliver the calendar and drafts instead of inventing a publishing step.

Publishing is visible to the public: confirm the final copy, accounts and times with the user before the first post goes out.

## References

- `../../references/playbooks/bosskuai-content-calendar-playbook.md`
- `../../references/checklists/content-calendar-checklist.md`
- `../../references/checklists/expert-cofounder-stack-checklist.md`
