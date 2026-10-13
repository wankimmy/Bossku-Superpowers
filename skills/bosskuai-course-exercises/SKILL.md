---
name: bosskuai-course-exercises
description: "Use when scaffolding a course repo: numbered section and exercise folders with problem, solution, and explainer variants, stub readmes, a lint run, and git-mv renumbering that keeps history."
---

# BosskuAI Course Exercises

Use this skill to create or reorganise the directory skeleton of a course or workshop repository from a written outline, and to get it past the repo's own lint before anyone fills in content.

## How this differs from nearby skills

- **`bosskuai-article-writing`**: writing the lesson prose itself. This skill only builds the folder structure and stubs.
- **`writing-plans`**: implementation plans for software changes, not course layouts.
- **`bosskuai-ui-demo`**: recording demo videos, a different course asset.
- **`bosskuai-continuous-learning`**: capturing engineering lessons, not building curriculum.

## Conventions (confirm against the repo first)

These come from one course repo's linter. Read the target repo's README, lint config, or an existing section before applying them.

- Sections: `XX-section-name/` under `exercises/`. Exercises: `XX.YY-exercise-name/` inside a section. Names are lowercase dash-case, numbers keep the order.
- Each exercise has at least one variant folder: `problem/` (student workspace with TODOs), `solution/` (reference), or `explainer/` (concept material, no TODOs). Default to `explainer/` when the plan does not say.
- Each variant folder has a non-empty `readme.md` with no broken links. A folder with code also needs the entry file the linter expects; a readme-only stub is acceptable.
- Disallowed files in that linter: `.gitkeep`, `speaker-notes.md`; also no run-command snippets in readmes. Check your repo's list.

## Workflow

1. Parse the outline into sections, exercises, and variant types.
2. Check the numbering is unique and ordered, and names are dash-case.
3. Create folders with `mkdir -p`.
4. Write one stub `readme.md` per variant: a title line and a one-line description.
5. Run the repo's lint command (look in `package.json` scripts or the README). Read each error, fix one cause at a time, re-run until green.
6. For renumbering or moves, use `git mv` so history follows, update the numeric prefixes, and re-run lint.
7. Report created paths and the lint result.

## Guardrails

- Do not guess the lint command; find it in the repo. If none exists, say so and check the structure by hand.
- Do not overwrite existing readmes or solution code. Stub only missing items.
- Do not commit or push unless the user asks.
- Do not add placeholder files only to satisfy the linter if the rule asks for real content; ask the user for the content instead.

## Output format

```text
Outline parsed: [sections, exercises, variants]
Created: [paths]
Moved: [old -> new]
Lint: [command, result, fixes made]
Left for author: [folders needing real content]
```

Adapted from mattpocock/skills/skills/misc/scaffold-exercises/SKILL.md (mattpocock/skills, MIT).
