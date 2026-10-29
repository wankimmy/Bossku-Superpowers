# Architecture

```text
Bossku-AI repo (canonical skills + contract)
        │
        ├─ plugin manifests ──► Claude / Cursor / Codex marketplace install
        │
        ├─ bossku install ──► ~/.agents/skills + ~/.claude/skills
        │
        └─ bossku init ──► project AGENTS.md + CLAUDE.md (@AGENTS.md) + .bossku/memory/
                                    │
                                    └─ bossku sync ──► Obsidian/BosskuAI/<project>/
```

## Principles

- **One source of truth** - skills and contract in this repo
- **Thin adapters** - projects keep small instruction blocks, not full copies
- **On-demand depth** - 670+ skills: 258 listable ones in `skills/` and 416 library-only ones in `library/`, which no plugin or profile lists (the `lean` profile, where a first install starts, lists 28); small always-on contract
- **No runtime orchestrator** - agents follow markdown contracts in your editor

## Agents

Seven roles in [`agents/`](../agents/): orchestrator, researcher (read-only mapping of unknown code), planner, designer (UI work only), executor, auditor and final reviewer, in that order of a task.

Specialist behavior lives in skills, not separate agent services.

## Cross-tool adapters

- **Cursor, Codex, OpenCode** load project `AGENTS.md` (OpenCode falls back to `CLAUDE.md` only when `AGENTS.md` is missing).
- **OMP** loads `.omp/AGENTS.md`, which imports the canonical project `AGENTS.md`, and reuses both installed skill directories.
- **Claude Code** loads `CLAUDE.md`; Bossku-AI repos and `bossku init` projects use `@AGENTS.md` so Claude imports the same contract without a second copy.
- **Plugin manifests** at `.claude-plugin/`, `.cursor-plugin/`, `.codex-plugin/`, and `.agents/plugins/` let each host install skills and agents from this repo without copying via the CLI.
- **OpenCode** has no marketplace plugin; `.opencode/opencode.jsonc` is a bare settings stub with no references.
- **Skills** install to `~/.agents/skills/` (Cursor, Codex, OpenCode, OMP) and `~/.claude/skills/` (Claude Code; OpenCode and OMP scan both). No extra OMP copy is needed. `bossku doctor` verifies managed skill counts in both mirrors. See [installation.md](installation.md#tool-compatibility).
