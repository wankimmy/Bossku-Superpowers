---
name: bosskuai-skill-stocktake
description: Use when auditing local skills, commands, and nearby guidance for overlap, stale content, weak triggers, and prompt-weight bloat.
---

# BosskuAI Skill Stocktake

Use this skill when the skill system itself needs maintenance.

## Audit dimensions

For each skill, check:

- trigger clarity
- uniqueness vs overlap
- actionability
- freshness
- token efficiency
- output format quality
- guardrails

## Workflow

1. Inventory skill files and note rough size/verbosity.
2. Check root `AGENTS.md` alignment: missing, stale, or duplicate roster entries.
3. Flag skills that are vague, overlapping, stale, or too heavy for how often they load.
4. Prefer the smallest safe maintenance action: keep, improve, merge, update, retire.
5. Prioritize high-traffic skills and always-loaded rule surfaces first.

## Token-efficiency bias

- Repeated routing tables belong in root `AGENTS.md`, not every tool-specific file.
- Keep skill bodies dense with decisions and guardrails; move long procedures to playbooks/checklists when possible.
- A shorter skill is better only if routing clarity and actionability stay intact.

## Gotchas

- A static audit cannot prove a skill was invoked. Separate available files, host discovery, routing results, and observed usage.
- Classify each skill by its recurring job: API reference, product verification, analysis, business workflow, scaffolding, review, delivery, runbook, or infrastructure operation. Category overlap is a signal to inspect boundaries, not a reason to add nine new duplicates.
- Check trigger-oriented descriptions, specific gotchas, supporting resources, invocation controls, and actual verification evidence. Review host-only fork, hook, and dynamic-context settings only where supported.
- Preserve vendored upstream text; improve routing or add a first-party reference instead of mechanically appending Gotchas to every file.


## Output

Return:

- scope audited
- audit result per skill
- overlap map
- priority maintenance actions
- what not to change yet and why

## References

- `../../references/checklists/skill-health-checklist.md`
- `../../references/playbooks/claude-code-practices-playbook.md`
- `../../references/playbooks/skill-stocktake-playbook.md`
- `../../references/checklists/learning-promotion-checklist.md`

## Verdicts and evidence

- Verdicts: Keep, Improve (name the change), Update (technology outdated; verify with a source), Retire, Merge into X (name the target and what to integrate). Judge holistically on actionability, scope fit, uniqueness and currency; do not use a numeric rubric.
- Every reason stands alone and enables a decision. Never write "unchanged" or "superseded" alone: Retire states the defect and what covers the need; Merge names the target and the content to move; Improve names the section and the target size (for example "section X duplicates Y, delete to reach about 150 lines").
- Usage data is optional. When no usage log exists, mark use as unmeasured, not zero, and never retire a skill on missing usage data.
- For large inventories evaluate in chunks of about 20 skills, keyed by file path (not name) so same-named skills cannot overwrite each other. Keep a results cache with the path, modification time, verdict and reason, and on a quick pass re-evaluate only files whose mtime changed. Skip archived or trash directories.
- Evaluate blind to origin: the same checklist applies to vendored, first-party and auto-extracted skills. Before retiring or merging, list dependents (other skills, memory references, workflows). Deleting or archiving always needs explicit user confirmation.
- Host portability: a skill copied into another host's skills folder should keep only the frontmatter keys that host supports, and bash fences must not rely on Claude-only substitutions (`${CLAUDE_SKILL_DIR}`, `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PROJECT_DIR}`, `$ARGUMENTS`); rewrite them to a resolved path in the copy. A passing frontmatter check does not prove a skill is safe on another host.

Adapted in part from ECC skills/skill-stocktake and skills/skill-host-compat (affaan-m/ECC, MIT).
