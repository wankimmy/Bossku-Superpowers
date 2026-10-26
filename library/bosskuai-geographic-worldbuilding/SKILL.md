---
name: bosskuai-geographic-worldbuilding
description: "Use when designing or checking a fictional or real region for physical plausibility: tectonics, climate, rivers, biomes, resources, settlement and trade routes, with a coherence report of problems."
---

# BosskuAI Geographic Worldbuilding

Use this skill to build a map-level world where terrain, climate, water, resources and settlement explain each other, or to audit an existing setting for impossible geography.

## How this differs from nearby skills

- **`bosskuai-narrative-analysis`**: story structure and character arcs. This skill checks the physical setting behind the story.
- **`bosskuai-gis-technical-consultant`** and **`bosskuai-gis-geoai-ml-engineer`**: real spatial data systems and imagery models, not invented or conceptual worlds.
- **`bosskuai-scientific-thinking-literature-review`**: research synthesis. Use it if you need cited climate science rather than design plausibility.

## Workflow

1. Start with tectonics: where are the mountain ranges and coasts? Most later decisions follow from these.
2. Build climate from first principles: latitude, prevailing winds, ocean currents, continental position, elevation, rain shadows.
3. Add hydrology: rivers run downhill, tributaries merge, and basins drain to a sea or lake. Forks are rare special cases such as deltas.
4. Layer biomes from climate, soil and water.
5. Place resources by geological and ecological logic.
6. Place people: water access, defence, farmland, trade. Then trace trade routes along passes, valleys and coasts.
7. Check scale: a small kingdom and a large empire need different communication, supply and governance.
8. List coherence issues and, for each, either a physical fix or a flagged "needs a fantastical explanation".

## Guardrails

- Every feature has a stated cause, or is explicitly marked as magic or other deliberate exception.
- Geography constrains but does not dictate culture. Avoid deterministic claims; similar environments produce different societies.
- Maps are choices. Note what a map leaves out.
- For real regions or scientific claims, check current sources rather than the heuristics here.
- Track established facts across a project and flag new additions that contradict them.

## Output format

```text
GEOGRAPHIC COHERENCE REPORT
Region: [name, scale]
Physical: [terrain origin, climate zone, hydrology, biome, hazards]
Resources: [farmland, minerals, timber, water]
Human: [settlement logic, trade routes, chokepoints, carrying capacity]
Issues: [problem -> why implausible -> fix]
```

Adapted from agency-agents/academic/academic-geographer.md (agency-agents, MIT).
