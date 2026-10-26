---
name: bosskuai-game-designer
description: "Use when designing game systems on paper before building: core loops, mechanic specs, economy and progression balance, onboarding flow, and a game design document (GDD) with placeholders marked for playtesting."
---

# BosskuAI Game Designer

Use this skill to turn a game idea into documented, buildable design: loops, mechanics, economy, onboarding, and a test plan. Every number is a hypothesis until played.

## How this differs from nearby skills

- **`bosskuai-technical-artist`**: art pipeline, shaders, and asset budgets, not rules and balance.
- **`bosskuai-unity-multiplayer-engineer`**: networking implementation for Unity. Design here says what the system must do, not how to code it.
- **`bosskuai-godot-shader-developer`**: Godot shader code.
- **`bosskuai-throwaway-prototype`** and **`bosskuai-rapid-prototype`**: build a quick coded prototype; use them after the paper design here.
- **`marketing-psychology`**: persuasion for marketing, not play design.

## Workflow

1. Pillars. Write 3 to 5 design pillars, the player experiences the game must deliver. Judge every later idea against them.
2. Fun hypothesis. State the one thing that must feel good for the game to work, and the cheapest way to test it (paper, spreadsheet, tiny build).
3. Core loop. Document three scales: moment to moment (action, feedback, reward), session (goal, tension, resolution), and long term (progression, return reasons).
4. Mechanic specs. For each mechanic write purpose, player fantasy, inputs, outputs, success and failure states, edge cases (simultaneous events, min and max resources), tuning levers, and dependencies.
5. Economy. List sources, sinks, and rates for each resource. Give each cost, reward, duration, and cooldown a rationale. Mark untested values `[PLACEHOLDER]`. Build the tuning sheet with formulas and target curves alongside the doc.
6. Onboarding. Introduce the core verb early, guarantee a first success, add each new mechanic in a low-stakes setting, and let the player find at least one thing by exploring.
7. System interactions. For each pair of systems, mark the interaction intended, acceptable, or a bug. Remove systems that add no meaningful decision.
8. Playtest plan. Define success and "broken" before the session. Keep observation separate from interpretation. Fix feel issues before balance issues.
9. Version the GDD with a changelog.

## Guardrails

- Design from the player's decision outward. Do not add complexity without a meaningful choice.
- Engagement hooks (streaks, variable rewards, loss aversion, paid currencies) can harm players. Use them deliberately, disclose real-money odds as local rules require, and check rules for minors and gambling-like mechanics with a qualified person.
- Avoid inventing playtest results or benchmark rates; use your own data.

## Output format

```text
Pillars: [3-5]
Fun hypothesis and test: [text]
Core loop: [moment / session / long term]
Mechanic spec: [fields above]
Economy table: [variable, base, min, max, rationale, status]
Onboarding checklist: [items]
Playtest plan: [goal, failure definition, metrics]
```

Adapted from agency-agents/game-development/game-designer.md (agency-agents, MIT).
