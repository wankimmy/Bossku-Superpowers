---
name: bosskuai-decision-games
description: "Use when you want to rehearse a negotiation or conflict as a turn-based strategy exercise with a simulated opponent, using game-theory framing and the 36 stratagems, ending in a verdict and a recommendation."
---

# BosskuAI Decision Games

Use this skill to role-play a negotiation or competitive situation round by round, so options and counter-moves are visible before the real conversation.

## How this differs from nearby skills

- **`bosskuai-council`**: four fixed voices argue a go/no-go decision. This skill simulates an opposing party over several rounds.
- **`bosskuai-recursive-decision-ledger`**: records decisions and their rationale over time. This skill explores moves, it does not log them.
- **`bosskuai-sales-strategy`**: real buyer motion and pricing narrative. This skill is a rehearsal game, not a sales plan.
- **`bosskuai-competitor-intelligence`**: scores real competitors on evidence. This skill invents archetype opponents.

## Workflow

1. Gather setup: the situation, the user's role and goal, the opponent type (cooperative, ruthless, cautious, unpredictable), what each side knows, and the number of rounds.
2. Classify the game: one-shot or repeated; zero-sum or positive-sum; simultaneous or sequential; full or hidden information. Name the likely model (for example prisoner's dilemma, chicken, bargaining) and state the assumption.
3. Announce the parameters and a simple scoring rule before round 1 (what a good outcome is for each side).
4. For each round, produce one move per side with: the stratagem used (from the 36 stratagems, by name), the game-theory concept it relies on, the concrete action, a one or two sentence reason, and the score change.
5. Carry the history into each round. Opponent moves must stay consistent with the archetype and what it has seen.
6. After the last round, give a verdict: who gained, what drove it, whether any stable outcome (equilibrium) was reached, and a recommendation the user can apply, such as signalling, commitment, or concession order.
7. Say clearly what was assumed. The opponent is a model, not the real person.

## Guardrails

- This is a thinking aid. Real people will not follow the script; do not present the output as a prediction.
- Do not use it to plan deception that causes real harm, fraud, or illegal coercion; keep stratagems to lawful negotiation and competition.
- Keep reasoning internal; do not depend on any external model or service.
- Check the stratagem names against a reliable source if the user needs accurate classical wording.

## Output format

```text
Setup: [situation, roles, game type, rounds, scoring]
Round N
  User: [stratagem] / [concept] / [move] / [reason] / [score]
  Opponent: [stratagem] / [concept] / [move] / [reason] / [score]
Verdict: [winner or draw, equilibrium check, drivers]
Recommendation: [what to do in the real situation]
```

Adapted from agency-agents/specialized/specialized-strategy-duel-agent.md (agency-agents, MIT).
