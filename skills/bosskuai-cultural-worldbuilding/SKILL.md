---
name: bosskuai-cultural-worldbuilding
description: "Use when designing or checking a fictional or historical society's culture: subsistence, kinship, rituals, belief, exchange and internal tensions, with a coherence check that avoids culture-salad cliches in games, novels and settings."
---

# BosskuAI Cultural Worldbuilding

Use this skill to build cultures that feel lived-in, and to audit existing ones. The question for every practice is what problem it solves for these people.

## How this differs from nearby skills

- **`bosskuai-historical-coherence`**: checks real-period accuracy and anachronisms. This skill designs and audits social and cultural systems, real or invented.
- **`bosskuai-narrative-designer`**: dialogue, branching and lore delivery in games. This skill supplies the culture that lore describes.
- **`bosskuai-brand-discovery`**: brand identity interviews, not societies.

## Workflow

1. Start with subsistence and environment: how do these people eat, and what resources exist and who controls them.
2. Build social organisation: kinship and descent, residence pattern, inheritance, political form.
3. Add exchange: reciprocity, redistribution or market, and who owes what to whom.
4. Layer meaning: cosmology, ritual calendar, taboos, specialists, rites of passage (separation, liminality, incorporation).
5. Define identity and boundaries: how "us" and "them" are drawn, and how status is displayed.
6. Coherence check each element: its function, fit with the rest, contradictions, real-world parallels, then keep, modify or rethink.
7. Stress-test: drought, war, a new technology. How does the culture adapt, and what breaks.
8. List internal tensions. A culture with none is a utopia and reads false.

## Guardrails

- No culture salad: do not mix traits from real cultures without knowing what each means in context and how they interact.
- Function before aesthetics. Ask what a ritual does before asking if it looks good.
- Treat real cultures with care. Check claims about real peoples against current scholarship or sources the user supplies; mark anything else `unverified`.
- Pre-industrial does not mean simple or harmonious.

## Output format

```text
Society: [name]
Subsistence and economy: [mode, exchange, resource control]
Social organisation: [kinship, residence, politics]
Belief and ritual: [cosmology, calendar, taboos, specialists]
Identity and boundaries: [in-group, status markers]
Coherence flags: [element, problem, keep / modify / rethink]
Internal tensions: [list]
```

Adapted from agency-agents/academic/academic-anthropologist.md (agency-agents, MIT).
