---
name: bosskuai-teach
description: "Use when the user wants to learn a topic over several sessions: set a mission, keep a learning workspace, write short interactive lessons with retrieval practice, and track learning records and references."
---

# BosskuAI Teach

Use this skill for stateful, multi-session teaching in a directory the user owns. The goal is lasting skill, tied to a reason the user cares about.

## How this differs from nearby skills

- **`bosskuai-continuous-learning`**: the agent learns from its own sessions. This skill teaches the user.
- **`bosskuai-handoff`**: carries context between agent sessions, not learner progress.
- **`bosskuai-scientific-thinking-literature-review`**: reviews literature for research; here sources feed lessons.
- **`bosskuai-article-writing`**: produces articles, not an interactive course.
- **`bosskuai-code-tour`**: walks a codebase; use it when the topic is one specific repo.

## Workspace

Treat the current directory as the teaching workspace and keep state in plain files:

- `MISSION.md`: why the user is learning this. If empty or unclear, question the user first.
- `RESOURCES.md`: trusted sources with notes.
- `learning-records/NNNN-name.md`: short records of what was learned and non-obvious insights.
- `lessons/NNNN-name.html`: one self-contained lesson each.
- `reference/*.html`: compressed cheat sheets and glossaries.
- `assets/`: shared stylesheet and reusable components.
- `NOTES.md`: user preferences about how they like to learn.

## Workflow

1. Read `MISSION.md`, the learning records, and `NOTES.md`. Pick the most relevant next skill within the learner's zone of proximal development (challenging but reachable).
2. While resources are thin, find high-quality sources first and record them in `RESOURCES.md`. Do not trust memory for facts; cite what you used.
3. Teach only the knowledge needed for one skill, then practise the skill with a tight feedback loop (quiz, short task, or real-world steps). Prefer effortful recall over re-reading, and space and interleave practice across lessons.
4. Write one short lesson that gives a single tangible win. Reuse components in `assets/`; add a new reusable component rather than inlining code a later lesson would duplicate.
5. Quiz design: answers of equal length, correct answer position varied, no formatting clues.
6. Link to related lessons and references, name one primary source to read or watch, and remind the learner they can ask follow-up questions.
7. Write the reference documents the lesson earns (syntax, glossary, flowchart). Keep one glossary and use its terms consistently.
8. Add a learning record. If the mission changes, confirm with the user before editing `MISSION.md` and record why.
9. For wisdom that needs real practice, suggest a reputable community, unless the user declines.

## Guardrails

- Confirm before creating files outside the current directory or opening a browser.
- Mark claims you could not verify from a source, and do not invent citations.
- Respect stated preferences in `NOTES.md`.

## Output format

```text
Mission: [one line]
Next skill: [target + why it fits now]
Lesson: [file, win, practice task]
Sources: [links]
Record: [what was learned, what to revisit]
```

Adapted from mattpocock/skills/skills/productivity/teach/SKILL.md (mattpocock/skills, MIT).
