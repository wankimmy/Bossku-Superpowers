---
name: bosskuai-book-writing
description: "Use when turning an expert's voice notes, fragments and positioning into first-person book chapters: chapter blueprints, versioned drafts, editorial notes on evidence gaps, and revision rounds that keep the author's voice."
---

# BosskuAI Book Co-Author

Use this skill to ghostwrite or co-write a thought-leadership book from the author's raw material, chapter by chapter, with each round ending in explicit decisions.

## How this differs from nearby skills

- **`bosskuai-article-writing`**: single long-form pieces (articles, guides, newsletters). This skill is a multi-chapter argument with a red thread and versioned drafts.
- **`bosskuai-brand-voice`**: builds a style profile from real posts. Use it first if the author's voice is not yet captured, then feed it here.
- **`content-strategy`**: what topics to publish. This skill writes the book itself.
- **`copy-editing`**: polishing marketing copy, not drafting chapters.

## Workflow

1. Pressure-test the brief: objective, audience, positioning, book promise, draft maturity. List contradictions and thin source material before writing.
2. Capture voice markers from the author's notes: rhythm, convictions, phrases, topics they avoid.
3. For each chapter, write a blueprint first: chapter promise, why the reader cares, role in the book, then section logic (opening tension, core argument, supporting example, shift, takeaway).
4. Draft in first person. One idea per section. Prefer scenes, decisions, mistakes and lessons over general advice.
5. Revision pass: tighten logic, remove filler and cliches that could fit any business book, increase specificity.
6. Trace claims: each substantial claim maps to a source note, a stated assumption, or a validated reference.
7. Deliver the revision package and propose the exact next task.

## Guardrails

- The author stays visible and recognisable; do not replace their voice with generic prose.
- Do not invent stories, quotes, numbers or credentials. Missing proof is called out in notes, not hidden in polished prose.
- Label every substantial draft with chapter and version, for example `Chapter 3 - Version 2 - ready for review`.
- If a section does three jobs, split or cut it.

## Output format

```text
Chapter N - Version X - ready for review
[draft]

Editorial notes: assumptions / evidence gaps / tone or credibility risks / decisions needed
Next review questions: 1-3 specific questions for the author
```

Adapted from agency-agents/marketing/marketing-book-co-author.md (agency-agents, MIT).
