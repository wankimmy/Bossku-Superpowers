---
name: bosskuai-level-designer
description: "Use when designing or reviewing a game level: layout and flow, pacing arc, encounter design, readability of the critical path, environmental storytelling, grey-box playtests, and a handoff spec for art."
---

# BosskuAI Level Designer

Use this skill to plan and critique game spaces so players know where to go, fights are fair and readable, and the space itself tells the story.

## How this differs from nearby skills

- **`bosskuai-game-designer`**: core loops, mechanics, economy, and the GDD. This skill takes one level and its layout, pacing, and encounters.
- **`bosskuai-economy-designer`**: currencies and rewards; level rewards should be priced there.
- **`bosskuai-character-psychology`** and **`bosskuai-cultural-worldbuilding`**: story and world texture that environmental storytelling can draw on.
- **`bosskuai-game-audio-engineer`**: sound support for pacing, done after layout locks.

## Workflow

1. Intent: write the emotional arc in one paragraph and name the one moment the player should remember. Note any mechanic the level introduces and how space teaches it.
2. Paper layout: sketch the flow top-down with entry, encounters, junctions, optional branches, rewards, and exit. Identify the critical path and every branch before building.
3. Pacing chart: sequence activity types (explore, combat, reward, rest) with a rough tension level and time estimate.
4. Readability rules for the critical path: lighting, colour, and geometry lead the eye; exits and objectives contrast with surroundings; every junction has a clear main route and an optional reward route; dead ends do not look like exits.
5. Encounters: give each an entry read time, at least two viable tactics, a fallback position, and enemies visible before they can hurt the player unless an ambush is deliberately telegraphed. Use position and layout for difficulty before stat inflation.
6. Grey box: build untextured geometry and playtest immediately. If it is not readable in grey box, art will not fix it. Lock layout decisions here.
7. Tune encounters in isolation, measure time to completion, tactics used, and confusion points, then connect them.
8. Art handoff: annotate gameplay-critical geometry versus dressable areas, intended lighting direction, and the story beat per zone.
9. Polish playtest with fresh players and compare actual timing to the pacing chart.
10. Check for unintended sequence breaks; decide which are intended shortcuts and which are exploits. For multiplayer maps, review sight lines, choke points, flanks, and spectator readability.

## Guardrails

- Evidence is playtest observation, not designer opinion. Record what testers did, not what they said they would do.
- Do not art-dress a layout that has not been playtested as a grey box.
- Procedural levels still need anchors and validation (reachability, key and door solvability, encounter spread).

## Output format

```text
Level intent and arc: [..]
Layout: [shape, critical path, optional branches]
Encounter table: [id, type, count, tactics, fallback]
Pacing chart: [time, activity, tension]
Playtest findings: [observation, count of testers, change made]
Art handoff notes: [..]
```

Adapted from agency-agents/game-development/level-designer.md (agency-agents, MIT).
