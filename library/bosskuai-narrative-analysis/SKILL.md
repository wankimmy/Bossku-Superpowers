---
name: bosskuai-narrative-analysis
description: "Use when analysing a story's structure, character arcs, pacing or coherence with named narrative frameworks (Propp, Campbell, Todorov, Genette, McKee) and proposing fixes to a draft, game script or plot."
---

# BosskuAI Narrative Analysis

Use this skill to diagnose a story at the right level and propose specific, framework-grounded fixes instead of vague notes like "make the character more relatable".

## How this differs from nearby skills

- **`bosskuai-geographic-worldbuilding`**: checks physical plausibility of a setting; this skill checks the story told in it.
- **`bosskuai-article-writing`**: voice and long-form nonfiction drafting, not story structure.
- **`antislop-copywriting`**: removes AI-sounding prose; this skill is about structure and arcs.
- **`bosskuai-brand-voice`**: marketing voice rules rather than narrative theory.

## Workflow

1. Name the level of analysis: plot structure, character, theme, narration technique, or genre.
2. Separate story (events in chronological order) from narrative (how they are told). Most problems sit in the telling.
3. State the controlling idea: what the story argues beneath the plot.
4. Pick fitting frameworks and say why they fit: Propp for quest and fairy-tale functions, Campbell and Vogler for hero journeys, Todorov for disruption of equilibrium, Genette for voice, focalisation and time, three-act or five-act or kishotenketsu for structure, Barthes for meaning codes.
5. Map structure: setup, confrontation, resolution, tension peaks and valleys, and what the reader knows versus what characters know.
6. Check narrative debts: promises made to the reader and whether they pay off.
7. Assess each major character: arc type, want versus need, false belief, transformation checkpoints.
8. Respect genre conventions before proposing a subversion, and check the subversion is earned.
9. Diagnose before prescribing. Give two or three alternative fixes with trade-offs and existing works as precedent.

## Guardrails

- Every recommendation cites at least one named framework and explains why it applies.
- Psychological models are lenses, not prescriptions; characters are not case studies.
- Attribute theory accurately; if unsure of a source, say so and check it.
- Track setups and payoffs across a long project and flag contradictions.

## Output format

```text
Controlling idea: [statement]
Structure model: [framework, why]
Act breakdown: [setup / confrontation / resolution]
Tension and information: [peaks, valleys, asymmetries]
Narrative debts: [promise -> status]
Character arcs: [name, type, want/need/belief, checkpoints]
Issues and fixes: [problem -> framework reasoning -> options with trade-offs]
```

Adapted from agency-agents/academic/academic-narratologist.md (agency-agents, MIT).
