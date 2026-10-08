# Memory and Obsidian

## Vault storage

Run `bossku install --vault <existing-vault-path> --memory-storage obsidian`.
The setting lives only in ~/.bosskuai/config.json. Run `bossku memory-path --project <project-root>` to resolve canonical memory.
`remember` appends redacted, UTC-stamped notes directly to `<vault>/Bossku Superpower/<project-name>/`, preserving Obsidian edits. No .bossku/memory or repo sync-state file is created. If the vault is unavailable, the write fails without a repo fallback.

| File | Purpose |
|---|---|
| project.md | Durable project facts |
| decisions.md | Decisions and reasons |
| plans.md | Actionable plans |
| learnings.md | Verified lessons |
| handoff.md | Current unfinished work; clear after completion |

`bossku init` uses the canonical directory for templates. Project adapters and .bossku/project.json remain repo configuration, not memory.

## Project isolation

In Obsidian mode, the first `remember` or memory-template initialization claims the resolved vault directory for its canonical project root. Ownership records live under `~/.bosskuai/memory-project-registry/`, alongside user configuration; they contain project paths, not notes. Exclusive claim creation prevents two different roots from both claiming the same target. `memory-path` and Obsidian sync checks only resolve and inspect ownership; they create no folders or claims.

An unrelated project with the same name, or a name that sanitizes to the same vault folder, fails before reading through the resolver or appending notes. Configured `memory_project_roots` still groups its subrepos intentionally. Different vaults have separate ownership records. Existing folder names and notes are preserved; no migration, deletion, or automatic backfill occurs.

For duplicate names, set an explicit `memory_project_namespaces` mapping in `~/.bosskuai/config.json`, keyed by the resolved grouping root path:

```json
{
  "memory_project_namespaces": {
    "C:/dev/another-workspace/repo": "another-workspace-repo"
  }
}
```

Merge this field with existing configuration. Namespace names use the existing vault-folder sanitization, and ownership checks still reject collisions. A new namespace selects a separate folder; it does not move old notes. An unclaimed pre-existing folder cannot reveal its historical project owner from its name alone: the first authorized write records ownership for future checks. Across different machines or user homes, the local ownership registry is separate; coordinate names explicitly for a shared vault. Malformed ownership records block resolution and writes until their ownership is checked and repaired.

## Automatic remembering

Agents read relevant notes first, then automatically save verified decisions, plans, facts, and lessons with bossku remember before their final response, without waiting for the user to ask. Skip routine work, duplicates, trivial chatter, secrets, raw prompts, transcripts, and logs. A small fix usually has nothing a future session needs, so it saves nothing.
`bossku remember` answers with `"saved": true` and a sentence saying where the note went. Agents that only saw a vault status of `skipped` (no vault configured) took a saved note for a failure and retried, so the saved flag comes first.
`bossku memory-brief --project .` prints the newest notes (at most 1,000 characters, newest first). The `session-brief` hook below runs it for Claude Code at session start, so the agent does not have to look for the files.
`bossku install` maintains separate marked memory-policy blocks in detected Codex ~/.codex/AGENTS.md, Claude Code ~/.claude/CLAUDE.md, and OpenCode ~/.config/opencode/AGENTS.md, preserving unrelated user instructions. New project adapters carry the policy for other hosts.
A rule the user states ("this must run on Python 3.8") counts as something a future session needs, so it is saved with its reason. How well that works is measured with two-session tasks in the [benchmark notes](benchmarks/README.md#remembering-a-rule-from-an-earlier-session).
Models differ a lot in whether they save a rule on their own, so Bossku Superpower helps for Claude Code: when a message states a rule ("from now on...", "our team rule is...", "we decided..."; see [`bossku/rules.py`](../bossku/rules.py)), the prompt hook points it out, and if the turn ends without a `bossku remember` call the stop hook sends the agent back once with the exact command. `BOSSKU_VERIFY_GATE=0` turns off the stop hook's reminders, this one included. The wording check is a proxy, not a judge. On 199 new messages written and labelled blind by other agents, the first version caught 47% of the stated rules and wrongly flagged 13% of tricky non-rules. It was then widened using those misses and tightened again after a code review found cues that were too broad ("Content Security Policy", "across the repo"); the current version reaches 58% on the same messages (13% of the tricky non-rules flagged, 0 of 57 ordinary coding prompts), which is optimistic because it was tuned on them. On a further set of 200 messages that nothing was tuned on (194 kept after blind labelling; committed in [`benchmarks/rules-eval/`](../benchmarks/rules-eval/), rerun with `python scripts/benchmark_rules.py score`) it caught **33 of 99** stated rules (95% interval 25-43%): 22 of 50 rules phrased as rules and 11 of 49 durable constraints or tech choices ("we're stuck on Node 16 until Q1"), and wrongly flagged 4 of 95 non-rules. An earlier set of the same kind, whose data was lost, gave 38 of 100 and 1 of 94. So the reminder fires for roughly one in three of the rules people state in their own words and stays quiet on ordinary requests; the other two in three depend on the agent following the standing instruction to save what the user states. It does not fire on every prompt on purpose: unneeded reminders made weaker models save junk notes and use more tokens. Both reminders say "if", and the agent may finish when no rule was stated. The stop hook ignores lines the app writes as user turns (compact summaries, task and CI notices), counts a message typed while the agent was working, and still sends the rule reminder after an unmet verify reminder.
This is agent-driven curation, not a background transcript summarizer. Hosts must load the instructions and permit vault access. Blocked writes are reported and never redirected into repos.

## Vault sync and tidy

Everything an agent learns can end up in one place. `bossku vault sync` (also run by the end-of-session hooks, at most once a minute) copies into `<vault>/BosskuAI/`:

| Source | Copied to |
|---|---|
| Claude Code's own auto-memory for the project, its sub-repos and its worktrees (`~/.claude/projects/<project>/memory/*.md`) | `<project>/claude-memory/<repo>/` |
| Global rules (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `~/.config/opencode/AGENTS.md`) | `_global/rules/` |
| A project's `CLAUDE.md`, `AGENTS.md` and `.claude/rules/*.md` | `<project>/rules/` |
| Legacy `.bossku/memory` notes inside a repository | `<project>/imported/repo-memory/` |

Copies start with a short header that names the source, have obvious secrets blanked out, and are rewritten only when the source changes. The originals are never modified or moved. `Index.md` at the top of `BosskuAI/` links every note and is regenerated by the same sync.

Earlier versions created one vault folder per working directory, so a project with several repos or worktrees ended up scattered across folders (`backend`, `tms-owner-web`, hash-named leftovers, empty folders). Set `memory_project_roots` in `~/.bosskuai/config.json` so that new notes go to the project's own folder, then tidy the old ones:

```bash
bossku vault tidy            # prints the plan; changes nothing
bossku vault tidy --apply    # zip backup first (~/.bosskuai/backups), then carry it out
```

The plan merges the notes of each sub-repo folder into `<project>/repos/<name>/` (entries from both files are kept, none twice, oldest first), moves `.conflict.md` backups, leaked benchmark notes and hash-named leftovers to `_archive/`, files generated or very short folder names under `_unsorted/` for you to place, imports notes found in a repository's `.bossku/memory` (the original stays), and removes only folders with no file inside them. No note is deleted.

## Session hooks

Existing sync hooks remain safety nets. In Obsidian mode they verify vault availability without overwriting vault notes from legacy copies or recreating local memory.
| Host | Events |
|---|---|
| Cursor | stop, sessionEnd, afterAgentResponse |
| Claude Code | Stop, SessionEnd |
| Codex | Stop, SessionEnd via a continue-safe wrapper |
| OpenCode | session.idle |

Claude Code also gets three small helper hooks: `SessionStart` runs `bossku session-brief` (the newest project notes), `UserPromptSubmit` runs `bossku skill-hint` (names the one or two skills that fit the prompt), and `Stop` runs `bossku verify-gate` (sends the agent back once if it changed code and never ran it; `BOSSKU_VERIFY_GATE=0` turns it off). The hint and the gate read your prompt or the session transcript only to decide what to say; nothing from them is saved.

`bossku hooks install` manages hooks separately. Codex's normal one-time hook trust approval still applies. Direct remember calls do not depend on hooks.

## Legacy repository storage

`memory_storage: "repo"`, or an unset storage field, retains repository-primary storage for compatibility. Notes are exported one way to Obsidian. Unavailable vault exports are pending; missing vault configuration skips exports. Changed vault copies are backed up to .conflict.md before legacy exports replace them.
Switching storage alone does not migrate or delete existing files. Preserve complete legacy files in the vault, verify their content, then remove repo copies. Preserve unrelated vault notes and conflict copies.
Optional Hindsight integrations must respect the configured canonical directory and must not introduce repo storage or transcript capture without the user's request.
