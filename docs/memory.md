# Memory and Obsidian

## Project memory

Curated Markdown only, under `.bossku/memory/`:

| File | Purpose |
|---|---|
| `project.md` | Durable project summary |
| `decisions.md` | Decisions worth keeping |
| `plans.md` | Plans and milestones |
| `learnings.md` | Verified lessons |
| `handoff.md` | Ephemeral continuation (clear when done) |

```bash
bossku remember --project . --kind decision "Use toolkit-only main."
bossku sync --project .
```

## Obsidian export

- **One-way** — repo → vault only
- **Dedicated folder** — `<vault>/BosskuAI/<project>/`
- **No raw prompts or transcripts**
- Vault path stored in `~/.bosskuai/config.json` only

If the vault is offline, local memory still saves; run `bossku sync` later.

If a vault file was edited manually after export, BosskuAI writes a `*.conflict.md` copy instead of overwriting.

## Denser Obsidian auto-sync hooks (default)

`bossku remember` already exports on every call (curated Markdown only — never raw
prompts or transcripts). `bossku install` (and `bossku hooks install`) wires **denser**
auto-sync hooks so `bossku sync-hook` also reruns after agent turns / session ends:

| Tool | Events |
|---|---|
| Cursor | `stop`, `sessionEnd`, `afterAgentResponse` |
| Claude Code | `Stop`, `SessionEnd` |
| Codex | `Stop`, `SessionEnd` via a continue-safe wrapper (`~/.bosskuai/codex-sync-hook.sh or .ps1`) |
| OpenCode | `session.idle` plugin (unchanged) |

This is still a safety net on the same curated one-way export path (repo → vault), not a
new write model. Install is additive and idempotent (`HOOK_MARKER = sync-hook`): only
BosskuAI entries are added or removed; unrelated hooks are preserved. Codex also gets
`[features] hooks = true` in `~/.codex/config.toml` without wiping other config.

```bash
bossku install --vault "/path/to/Obsidian/Vault"   # refreshes denser hooks by default
bossku hooks install                               # all detected tools
bossku hooks install --tools codex                 # one tool: claude_code, cursor, codex, opencode
bossku hooks uninstall                             # remove only BosskuAI-marked entries
```

**Codex trust step:** after install, run Codex once and approve hooks when prompted
(`/hooks` trust gate). Hooks are written immediately but only fire after that one-time
approval. `bossku doctor` reports which tools currently have denser hooks installed.

## Privacy

Secrets are redacted before write. Do not store API keys, passwords, or `.env` contents in memory files.

## Optional Hindsight integration

[`bosskuai-hindsight-memory`](../skills/bosskuai-hindsight-memory/SKILL.md) provides an explicit workflow for an already configured Hindsight CLI or MCP connection. It separates retain (fact extraction), recall (retrieval), and reflect (generated reasoning), checks project-bank isolation and provenance, and falls back to local Markdown when unavailable.

The skill does not install or start Hindsight, change providers, migrate notes, or enable automatic transcript capture. Canonical notes remain in `.bossku/memory/`; only approved redacted notes may be mirrored to an approved bank. Obsidian export is unchanged. See the [integration playbook](../references/playbooks/hindsight-memory-playbook.md) for setup boundaries and readiness checks.
