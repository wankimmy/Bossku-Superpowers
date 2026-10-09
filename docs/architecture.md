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
- **On-demand depth** - 240+ specialist skills (the `lean` profile, where a first install starts, lists about 25); small always-on contract
- **No runtime orchestrator** - agents follow markdown contracts in your editor

## Agents

Six roles in [`agents/`](../agents/): orchestrator → planner → designer (UI work only) → executor → auditor → final reviewer.

Specialist behavior lives in skills, not separate agent services.

## Cross-tool adapters

- **Cursor, Codex, OpenCode** load project `AGENTS.md` (OpenCode falls back to `CLAUDE.md` only when `AGENTS.md` is missing).
- **OMP** loads `.omp/AGENTS.md`, which imports the canonical project `AGENTS.md`, and reuses both installed skill directories.
- **Claude Code** loads `CLAUDE.md`; Bossku-AI repos and `bossku init` projects use `@AGENTS.md` so Claude imports the same contract without a second copy.
- **Plugin manifests** at `.claude-plugin/`, `.cursor-plugin/`, `.codex-plugin/`, and `.agents/plugins/` let each host install skills and agents from this repo without copying via the CLI.
- **OpenCode** has no marketplace plugin; `.opencode/opencode.jsonc` is a bare settings stub with no references.
- **Skills** install to `~/.agents/skills/` (Cursor, Codex, OpenCode, OMP) and `~/.claude/skills/` (Claude Code; OpenCode and OMP scan both). No extra OMP copy is needed. `bossku doctor` verifies managed skill counts in both mirrors. See [installation.md](installation.md#tool-compatibility).
