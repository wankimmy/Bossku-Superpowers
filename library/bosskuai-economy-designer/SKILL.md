---
name: bosskuai-economy-designer
description: "Use when tuning a live game's currencies and shops: faucet and sink maps, inflation control, archetype simulations, telemetry thresholds, and ethical pricing. For first-draft loops and GDDs use the game designer skill."
---

# BosskuAI Game Economy Designer

Use this skill when a game already has, or is about to ship, currencies, drops, shops, or trading, and the numbers need to stay solvent over months of live play.

## How this differs from nearby skills

- **`bosskuai-game-designer`**: paper design of loops, mechanics, onboarding, and the GDD. This skill takes the economy part of that design and stress-tests and tunes it with simulation and telemetry.
- **`bosskuai-financial-modeling`**: business revenue, burn, and unit economics. Here the model is in-game flow of currency, not company cash.
- **`bosskuai-paid-acquisition-monetization`**: ad and acquisition monetisation. This skill covers in-game spend and pricing design.
- **`bosskuai-growth-experiment`**: generic experiment design, reused for balance A/B tests.

## Workflow

1. State the decisions the economy should create (save or spend, specialise or generalise). Keep the fewest currencies that support them.
2. For each currency write a spec: purpose, type, every source with rate, every sink with cost and frequency, cap, conversion paths, exploit surface (duping, botting, multi-accounting, trade abuse).
3. Draw the flow map. Every earn loop must end in a sink or a cap. Flag orphan currencies and dead ends.
4. Derive costs backwards from target time-to-milestone per player archetype (casual, core, no-spend grinder, spender) rather than picking numbers first.
5. Simulate each archetype over a long horizon (spreadsheet or Monte Carlo). Look for inflation, hoarding, dead ends, and a degenerate best strategy. Check randomised drops and pity systems on worst-case luck.
6. Define telemetry before launch: earned and spent per source and sink, wallet balance by cohort, faucet-to-drain trend, sink participation, and alert thresholds that trigger a balance pass.
7. Live tuning: change one lever at a time, version each change with expected impact and a rollback plan. Prefer adding sinks or rewards over nerfing what players already own.

## Guardrails

- Every value needs a rationale (curve, target, or simulation result), not a magic number.
- Monetisation: no progress that is only reachable by paying where the genre contract says otherwise, odds disclosed for randomised purchases, no fake urgency or confusing currency conversion. Check current platform and local consumer rules, especially for minors and loot-box law.
- Simulation is a model. Treat playtest and telemetry as the final word and update the archetypes.
- Do not change a live economy, grant currency, or refund players without the owner's explicit approval.

## Output format

```text
Currency spec: [name, purpose, sources, sinks, cap, conversions, exploits]
Flow check: [orphans, loops without exit]
Simulation: [archetype, earn/day, spend/day, day-30 and day-90 balance, flags]
Telemetry and alert thresholds: [..]
Proposed change: [lever, expected effect, rollback]
```

Adapted from agency-agents/game-development/economy-designer.md (agency-agents, MIT).
