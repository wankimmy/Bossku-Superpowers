---
name: bosskuai-roblox-experience-designer
description: "Use when designing a Roblox experience's onboarding, progression, retention, and monetization: Game Passes versus Developer Products, DataStore-safe saves, daily rewards, analytics funnels, and fair, non-predatory pricing."
---

# BosskuAI Roblox Experience Designer

Use this skill for the player-facing systems of a Roblox experience: first minutes, return loops, saved progress, and paid items. The audience includes many minors, so fairness and clarity come first.

## How this differs from nearby skills

- **`bosskuai-game-designer`**: engine-agnostic loops and GDD. This skill is Roblox-specific systems and platform rules.
- **`bosskuai-economy-designer`**: deep currency modelling and simulation. Use it when the soft-currency economy is large; use this skill for pass and product choices.
- **`bosskuai-paid-acquisition-monetization`**: ad monetisation outside the game.
- **`bosskuai-level-designer`**: spatial design of the starter zone and maps.

## Workflow

1. Brief: core fantasy, target age range and genre, and the three things a player would tell a friend about it. Treat title, description, and thumbnail as product decisions because they drive discovery.
2. Engagement ladder: first session, daily return, weekly return. Each tier needs a clear reward at completion and an investment hook (something the player owns or built and wants to keep).
3. Onboarding phases: within the first minute the player performs the core action and succeeds; within about five minutes completes one full loop and earns a first reward; within about fifteen sees progress, a personalisation choice, and a preview of what is locked. Tune these timings by watching where players leave.
4. Persistence first: store progress in DataStores with retry and error handling, version the data schema and migrate rather than overwrite, and use one structure for free and paying players. Handle failed loads without wiping saves.
5. Monetisation: Game Passes for permanent benefits (check ownership server-side, cache with care, invalidate on purchase); Developer Products for consumables. The free path must be complete and fun. Check the current Roblox price tiers, policies, and payments rules in the official docs before pricing.
6. Daily rewards: compute streaks on the server using a trusted time source, handle missed days gracefully, and save claims atomically so they cannot be duplicated.
7. Analytics: log funnel steps (onboarding done, first purchase, session length) with the built-in analytics service, then examine drop-off by step. Compare variants with bucketed A/B tests.
8. Live events: drive timers from one server time source, give limited items a clear earn path, and roll out changes to a portion of servers first.

## Guardrails

- No pressure tactics aimed at children: no fake countdowns, hidden costs, or confusing currency conversion. Mark paid items clearly in the UI. Rewarded ads need explicit consent and an easy skip.
- Follow current Roblox policies on monetisation, minors, and advertising. Policy and API names change; verify them in the current official documentation.
- Never grant items or currency from the client; validate purchases and rewards on the server.
- Do not publish, change prices, or run live-service updates without the owner's explicit approval.
- Retention targets depend on genre; set them from your own data rather than borrowed benchmarks.

## Output format

```text
Brief: [fantasy, audience, genre]
Engagement ladder: [tier, loop, reward, hook]
Onboarding steps and drop-off checks: [..]
Monetisation list: [item, pass/product, benefit, free-path check]
Data safety plan: [schema version, retry, migration]
Analytics events and A/B plan: [..]
```

Adapted from agency-agents/game-development/roblox-studio/roblox-experience-designer.md (agency-agents, MIT).
