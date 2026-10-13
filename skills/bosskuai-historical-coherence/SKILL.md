---
name: bosskuai-historical-coherence
description: "Use when checking a story, game or setting for historical accuracy: anachronisms, material culture, period and region specifics, confidence levels with source types, and separating documented history from myth or speculation."
---

# BosskuAI Historical Coherence

Use this skill to validate or enrich a setting against the historical record, saying clearly what is documented, what is debated, and what is invented.

## How this differs from nearby skills

- **`bosskuai-cultural-worldbuilding`**: designs and audits a society's internal logic, real or invented. This skill checks claims against real history.
- **`bosskuai-deep-research`**: multi-source research synthesis on any topic. Use it when the question is broader than period accuracy.
- **`bosskuai-grounding`**: the always-on rule to trace claims to sources; this skill applies it to history.
- **`bosskuai-narrative-designer`**: delivering story in games, after the setting is settled.

## Workflow

1. Establish coordinates: exact period and region. "Medieval" is not a date.
2. Check the material base first: food, trade, technology, agriculture, money. These constrain politics and war.
3. Layer social structure: power and legitimacy, class, gender roles with regional variation, practised versus official religion, formal and customary law.
4. Evaluate each claim and give a verdict: accurate, partly accurate, anachronistic, or myth. Give a confidence level (well documented, scholarly consensus, debated, speculative) and the source type (primary source, scholarship, popular).
5. Flag anachronisms including subtle ones: attitudes, institutions, economic assumptions, not only objects.
6. Correct common myths with evidence and say where historians disagree.
7. Add daily-life texture: what people ate, wore, feared, how days and years were structured.
8. For fiction-inspired settings, list the historical parallel and where the setting diverges on purpose.

## Guardrails

- Name sources and their limits. If you cannot cite one, mark the claim `unverified` or say "I don't have enough information to confidently answer this".
- Do not default to Europe; include non-Western histories where relevant.
- Avoid presentism, but do not excuse atrocities as "just how things were".
- Do not invent quotes, dates or archaeological finds.

## Output format

```text
Setting: [period, region, context]
Claim check: [claim, verdict, evidence, confidence, source type]
Anachronism flags: [item, why wrong, accurate alternative]
Material culture: [diet, clothing, buildings, technology, trade]
Open debates: [positions]
Intentional divergences: [list]
```

Adapted from agency-agents/academic/academic-historian.md (agency-agents, MIT).
