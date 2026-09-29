---
name: bosskuai-skill-creator
description: Use when creating, improving, evaluating, or benchmarking BosskuAI skills and their triggers, sidecars, or validation prompts.
---

# BosskuAI Skill Creator

Use this skill when the task is to **create or improve BosskuAI skills**: new skill directories, skill rewrites, skill quality audits, validation prompts, or reusable skill benchmarks.

## How this differs from nearby skills

- **`bosskuai-skill-stocktake`**: audits the whole roster for overlap and maintenance quality; this skill builds or revises individual skills.
- **`bosskuai-rules-distill`**: promotes repeated behavior into rules; this skill packages repeatable domain workflows into skill form.
- **`bosskuai-continuous-learning`**: decides where a lesson belongs; this skill applies the decision when the target is a skill.
- **`cofounder`**: routes across the workspace; this skill handles the craft of skill design.

## Mindset

- A skill is not a knowledge dump. It is a compact operating manual for a recurring class of work.
- Frontmatter is the router; the body is the workflow. Make both precise.
- Prefer one sharp skill over several vague ones with overlapping triggers.
- Use progressive disclosure: keep `SKILL.md` lean and point to checklists or playbooks for longer detail.
- Validate skills against realistic prompts, not only against their own wording.

## Canonical structure

Use the local BosskuAI pattern unless an existing nearby skill uses a stronger convention:

1. YAML frontmatter with `name` and a specific `description`.
2. One `# BosskuAI ...` heading.
3. A short "Use this skill when..." orientation.
4. `How this differs from nearby skills`.
5. `Mindset`.
6. `Workflow` or named lenses.
7. `Gotchas` or specific failure-oriented `Guardrails`.
8. `Output format`.
9. `References` with relative links to checklists, playbooks, memory, or scripts.

Target concise skills. Stay under the repo's line-count ceiling and move detail to references if the body starts becoming a handbook.

## Artifact decision guide

Create or update a **skill** when the lesson changes how the assistant should perform a recurring domain task.

Create or update a **checklist** when the lesson is a repeatable verification pass.

Create or update a **playbook** when the lesson is a longer step-by-step operating process that does not always need to be loaded.

Create or update a **rule** when the lesson should apply across many tasks and tools.

Create or update **memory** when the lesson is durable project context but not a reusable operating procedure.

Do nothing when the lesson is a one-off outcome, temporary debug note, or already covered by a stronger artifact.

## Workflow

### Phase 1 - Define the skill boundary

1. Identify the recurring job the skill enables.
2. Name the adjacent skills and write explicit boundaries.
3. Decide if this should be a new skill, an enhancement to an existing skill, a checklist, a playbook, a rule, or a memory note.
4. Reject the new skill if it is only a synonym for an existing one.

### Phase 2 - Write the router

5. Write the frontmatter `description` as: "Use when <trigger situations>." Aim for <=300 chars (validator max 1200).
6. Include exclusions or nearby skill pointers if ambiguity is likely.
7. Keep the description broad enough to trigger naturally but narrow enough to avoid hijacking unrelated tasks.

### Phase 3 - Write the operating body

8. Add a short mindset that changes behavior in useful ways.
9. Write the workflow as steps the next model can execute without chat history.
10. Include tool or MCP guidance only when it materially changes the work.
11. Add guardrails for common failure modes: overbroad scope, stale assumptions, secret leakage, unsupported claims, or irreversible actions.
12. Add an output format that fits the actual work product.

### Phase 4 - Validate and benchmark

13. Run a format pass: frontmatter parses, headings are clear, links are relative, and line count is below the limit.
14. Run an overlap pass against nearby skills.
15. Test with 2-4 realistic prompts: one ideal trigger, one adjacent non-trigger, one ambiguous request, and one high-risk task.
16. If the environment supports subagents and the user wants evaluation, use four perspectives:
    - **designer**: clarity and trigger quality
    - **operator**: whether the workflow is executable
    - **reviewer**: overlap and failure modes
    - **benchmark**: realistic prompt behavior

## Gotchas

- Descriptions should tell the router when to fire, not summarize every section. Put broader phrase coverage in the generated index's curated trigger source.
- Include verified failure points that change the next action. Do not repeat elementary advice or impose one rigid workflow where a goal and constraints suffice.
- Sidecars must survive user-level installation. Reuse an existing script or standard tool; verify relative links, prerequisites, and side effects.
- Claude-only `context: fork`, preloaded subagent skills, invocation controls, scoped hooks, and dynamic `!` shell context are not universal Agent Skills features. Verify the host and Bossku schema before adding them.
- Dynamic shell context runs on invocation; keep it narrowly read-only and free of credentials or automatic installs. Explicit tool calls are the portable default.
- Distinguish a routing check from a behavioral evaluation and actual host usage. `bossku skills audit` measures inventory and context cost, not invocation frequency.


## Guardrails

- Do not add a new skill just to preserve a single idea; use memory or a checklist when that is enough.
- Do not duplicate long reference material inside `SKILL.md`.
- Do not create extra README, changelog, or install docs inside a skill directory unless the repository already requires them.
- Do not claim a skill has been validated unless you actually ran the checks or reviewed realistic prompts.
- Do not hardcode machine-local absolute paths in portable BosskuAI skill references.

## Output format

```text
Skill design summary:
  Target skill: [name]
  Job to be done: [recurring task]
  Adjacent skills: [boundaries]
  Artifact choice: [new skill / existing skill update / checklist / playbook / memory]

Changes:
  Files: [paths]
  Router description: [why it should trigger]
  References: [linked artifacts]

Validation:
  Format: [pass / gap]
  Overlap: [pass / risk]
  Prompt checks: [pass / not run]
  Line count: [count / ceiling]
```

## References

- `../../references/checklists/skill-creator-checklist.md`
- `../../references/playbooks/claude-code-practices-playbook.md`
- `../../references/checklists/learning-promotion-checklist.md`
