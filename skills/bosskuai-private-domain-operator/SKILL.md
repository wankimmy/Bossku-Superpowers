---
name: bosskuai-private-domain-operator
description: "Use when planning WeCom (Enterprise WeChat) private-domain operations: channel codes, tagging, segmented community SOPs, lifecycle flows, Mini Program linkage, funnel metrics, and consent and platform-rule limits."
---

# BosskuAI Private Domain Operator

Use this skill to design the owned-audience system on WeCom and WeChat: how people are added, tagged, grouped, nurtured, and measured. It produces plans, configs, and SOPs; it does not message anyone.

## How this differs from nearby skills

- **`bosskuai-china-ecommerce-operator`**: marketplace stores, ads, and live commerce on Taobao, Tmall, JD, and similar. This skill is the owned WeCom community and CRM layer.
- **`bosskuai-china-market-localization-strategist`**: entering China with trend-led content. This skill covers retention and conversion after contact exists.
- **`bosskuai-wechat-mini-programs`**: building the Mini Program itself. This skill plans how it links to chats and member data.
- **`bosskuai-marketing-growth`** and **`community-marketing`**: general growth and community strategy, not WeCom mechanics.
- **`bosskuai-customer-success-support`**: support SOPs that can be reused for the service side.

## Workflow

1. Audit what exists: contact count, groups and their activity, Mini Program usage, current funnel stages and drop-off, and what the SCRM tool can actually do (automation, tags, analytics).
2. Segmentation: define tag dimensions (source, spend tier, lifecycle stage, interest) and automatic tagging rules with clear triggers.
3. Entry points: channel codes per source (package insert, livestream, store) with staff pools, a welcome message, and source tags, so each channel can be measured.
4. Community tiers: for example welcome, perks, VIP, with entry conditions, capacity, a daily and weekly content calendar, and rules for pruning and upgrading members.
5. Lifecycle flows: new member activation, growth, maturity, dormant reactivation, and a human hand-off at key points rather than pure automation.
6. Data link: join WeCom contact IDs with Mini Program IDs only with a lawful basis and consent, to build one customer view.
7. Metrics by stage: new contacts by channel, first-interaction rate, group activity, click and purchase conversion, repeat purchase, lifetime value, and opt-out or removal rate. Define each metric and its source before reporting.
8. Review loop: daily check on adds and activity, weekly funnel review, monthly SOP and tag clean-up. Test mass messages on a small segment first.

## Guardrails

- Follow the current WeCom and WeChat platform rules, including limits on mass messages, friend-add frequency, and use of unofficial tools. Check the official documentation for current limits.
- Privacy: obtain explicit consent and respect China's Personal Information Protection Law and any sector rules (finance, health, education). This skill is not legal advice; have qualified counsel review data use and content.
- Do not add people to groups, send mass messages, or contact lapsed users without consent. Anyone who leaves or opts out is not contacted again.
- Keep content mostly useful, not promotional, and do not use automation for sensitive one-to-one conversations.
- Do not send, publish, or change a live SCRM setup without the owner's explicit approval.

## Output format

```text
Audit summary: [assets, funnel, tool limits]
Tag system and rules: [dimension, tags, trigger]
Channel codes: [source, staff pool, welcome, tags]
Community SOP: [tier, entry rule, calendar, pruning]
Lifecycle flows: [stage, trigger, steps, human touchpoints]
Metrics and review cadence: [definition, source]
Compliance review items: [..]
```

Adapted from agency-agents/marketing/marketing-private-domain-operator.md (agency-agents, MIT).
