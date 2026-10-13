---
name: bosskuai-narrative-designer
description: "Use when designing game story systems: branching dialogue with consequences, character voice pillars, tiered lore and a world bible, environmental storytelling beats, and story-to-gameplay alignment in Ink, Yarn or similar."
---

# BosskuAI Narrative Designer

Use this skill to design story as a system players live inside: choices with consequences, voices that stay consistent, lore that is optional but coherent, and story beats tied to gameplay.

## How this differs from nearby skills

- **`bosskuai-cultural-worldbuilding`**: builds the society behind the lore. This skill delivers story through dialogue, branches and spaces.
- **`bosskuai-historical-coherence`**: checks period accuracy for historical settings.
- **`bosskuai-article-writing`**: prose for articles and guides, not interactive narrative.
- **`bosskuai-godot-multiplayer-engineer`**: engine networking; this skill stays on narrative content and structure.

## Workflow

1. Frame the narrative: the central question the game asks, the player's emotional arc, and how story pillars support gameplay pillars.
2. Structure before lines: acts and turning points, then a node map of every branch, convergence and consequence. Never write dialogue into structural dead ends.
3. Character voice pillars for each speaking character: role, want versus need, vocabulary, sentence rhythm, topics avoided, verbal tics, three lines they would never say, and reference lines used to judge new dialogue.
4. Write dialogue in the engine-ready format (Ink, Yarn Spinner, or the project's own) from the start. Pass one for function, pass two for voice, pass three for brevity.
5. Make choices differ in kind, not just degree. Each branch converges without feeling forced, and its consequence is felt within a stated number of scenes.
6. Lore tiers: surface (critical path, everyone), engaged (explorers), deep (hunters). The critical path must be understandable without optional lore. Keep a world bible with timeline, factions, rules of the world, and facts that cannot be retconned.
7. Environmental beats: what happened here, what the player should infer, what stays mysterious, props and placement, light and sound.
8. Align story beats with gameplay consequences in a matrix.
9. Test: read with audio off, walk every branch for dead ends, playtest whether players infer each space's story.

## Guardrails

- No "as you know" exposition between characters who already know it.
- Do not give narrative choices in a game with no mechanical choices unless a fake choice is deliberate and justified.
- Track promises made to the player (foreshadowing, open threads) until each is resolved or retired.
- Plan for localisation: externalised strings and cultural notes.
- Target numbers (percent of players who infer something) are playtest goals, not guarantees.

## Output format

```text
Narrative question and arc: [text]
Node map: [scene, choices, convergence, consequence]
Voice pillars: [character, vocabulary, rhythm, avoids, reference lines]
Lore tiers: [surface / engaged / deep items]
Beat-to-gameplay matrix: [story beat, gameplay consequence, intended feeling]
Open risks: [dead ends, contradictions, unresolved threads]
```

Adapted from agency-agents/game-development/narrative-designer.md (agency-agents, MIT).
