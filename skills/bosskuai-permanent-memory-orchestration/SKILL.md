---
name: bosskuai-permanent-memory-orchestration
description: "Use when the task touches BosskuAI memory, automatic remembering, bossku remember, Obsidian storage, cross-tool recall, memory hygiene, or durable decisions and plans."
---

# BosskuAI Permanent Memory Orchestration

Automatically save useful verified decisions, plans, project facts, and lessons as meaningful work proceeds and before the final response. Do not wait for the user to request remembering.

## Resolve storage first

Run `bossku memory-path --project <actual-project-root>` and read relevant kind files from the returned `memory_dir`. Start with a non-empty handoff.md when continuing unfinished work.
Storage comes from ~/.bosskuai/config.json:
- `memory_storage: "obsidian"`: canonical notes live directly under `<obsidian_vault>/BosskuAI/<project-name>/`. No memory or sync state is written inside the repo. Obsidian edits are authoritative.
- `memory_storage: "repo"` (legacy default when unset): repo Markdown is exported one way to the vault.
Configure vault storage with `bossku install --vault <existing-vault-path> --memory-storage obsidian`.
The vault must exist outside the code repo. If unavailable, report the failed save; never fall back to repo storage.

## Automatic workflow

1. Retrieve relevant notes before decisions, debugging, or continuation.
2. Save an actionable multi-phase plan with --kind plan when useful to future sessions.
3. Do the requested work and verify outcomes.
4. Automatically call `bossku remember --project <project-root> --kind decision|plan|learning|project "<concise verified note>"` before replying.
5. Inspect the returned file and vault.status; never claim a save that failed.

| Kind | File | Content |
|---|---|---|
| project | project.md | Stack, constraints, source-of-truth files |
| decision | decisions.md | Verified choices and reasons |
| plan | plans.md | Compact actionable plans |
| learning | learnings.md | Verified lessons and outcomes |
| manual | handoff.md | Current unfinished work; clear when completed |

Resolve handoffs in the same canonical directory. User storage preferences override older skills naming .bossku/memory. Redact manual handoffs; durable notes use remember.

## Hooks and limits

Installation adds standing automatic-memory instructions for detected Codex, Claude Code, and OpenCode hosts. New project adapters instruct other agents to remember automatically. Agents curate and call the CLI; sync hooks do not generate notes or read transcripts. In Obsidian mode, hooks only check vault availability and never recreate repo memory.
Codex hooks still require the host's normal one-time interactive trust approval. Direct remember calls do not depend on hooks.

## Hygiene

- Save only verified facts and explicit user decisions; skip trivial chatter and duplicates.
- Never store secrets, customer data, raw prompts, transcripts, logs, or speculation as fact.
- Link source files instead of copying them. Append dated corrections to stale notes.
- Preserve existing vault content. Legacy notes require an explicit lossless migration; ordinary sync must not overwrite vault notes with repo copies.
- Optional Hindsight integrations must respect the configured canonical directory.
- Report actual save status when the task concerns memory; avoid memory-status noise on other tasks.

## References

- `../../docs/memory.md`
- `../../references/memory-first-handoff-protocol.md`
