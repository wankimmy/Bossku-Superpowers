---
name: bosskuai-character-psychology
description: "Use when writing fiction, games, or role-play and you need characters whose behaviour is psychologically credible: motivation, attachment, trauma responses, defences, and relationship dynamics grounded in named frameworks."
---

# BosskuAI Character Psychology

Use this skill to check or design how a character thinks, reacts, and relates, using named psychological frameworks and honest limits. It is a craft tool for fictional people.

## How this differs from nearby skills

- **`bosskuai-story-lifecycle`**: story structure and stages. This skill is about the inner life and relationships of characters inside a story.
- **`bosskuai-article-writing`**: non-fiction long-form writing.
- **`bosskuai-openclaw-persona-forge`**: building an AI agent persona, not a fictional human.
- **`marketing-psychology`**: persuasion and buyer behaviour, not character depth.

## Workflow

1. Observe before labelling. List what the character actually does and says, with scenes as evidence.
2. Pick one primary lens and one or two secondary lenses (for example Big Five traits, attachment style, cognitive distortions, defence mechanisms). Name the lens in the notes.
3. Build the profile: traits with behavioural examples, attachment pattern and what triggers it, usual defences and what happens under stress, the formative experience behind the pattern, coping style (adaptive and maladaptive), and a blind spot.
4. Check for cliche: is this a real pattern or shorthand ("sad backstory means broken")? Trauma responses vary: hypervigilance, people-pleasing, compartmentalising, withdrawal, high functioning.
5. Map each key relationship: power balance, communication pattern, unspoken contract, trigger points, and what a healthier version would look like.
6. Project forward: given this psychology, what would they plausibly do in the scene? Flag any action that contradicts the profile without a story reason.
7. Note cultural context. Many models come from Western, individualist research; other settings may define healthy patterns differently.

## Guardrails

- Describe traits and patterns, not diagnoses. Do not label a character with a clinical disorder as a verdict.
- Separate research-backed ideas from popular self-help. State that some findings are contested or have replication problems.
- This is storytelling craft, not clinical advice. Do not use it to assess a real person; refer real concerns to a qualified professional.
- Handle self-harm, abuse, and trauma themes with care and keep depictions non-instructional.

## Output format

```text
Character: [name]
Lens: [primary framework, secondary]
Traits and evidence: [trait: scene behaviour]
Attachment and triggers: [pattern, triggers]
Defences: [usual, under stress]
Formative experience / blind spot: [text]
Relationship map: [pair: power, pattern, contract, trigger]
Consistency flags: [action vs profile]
Limits: [what the framework cannot say]
```

Adapted from agency-agents/academic/academic-psychologist.md (agency-agents, MIT).
