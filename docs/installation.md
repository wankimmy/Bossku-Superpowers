# Installation

## Requirements

- Python 3.11+
- Git

## Plugin / marketplace install

BosskuAI ships native plugin manifests for Claude Code, Cursor, and Codex. OpenCode uses skill discovery plus the `.opencode` harness.

### Claude Code

```text
/plugin marketplace add wankimmy/Bossku-AI
/plugin install bossku-ai@bosskuai-marketplace
```

Skills and agents load from this repository via [`.claude-plugin/plugin.json`](../.claude-plugin/plugin.json). Refresh after updates with `/plugin marketplace update` and reinstall if needed.

### Cursor

**Windows (PowerShell):**

```powershell
git clone https://github.com/wankimmy/Bossku-AI $env:USERPROFILE\.cursor\plugins\local\bossku-ai
```

Or link an existing clone:

```powershell
$pluginDir = "$env:USERPROFILE\.cursor\plugins\local\bossku-ai"
New-Item -ItemType Directory -Force -Path (Split-Path $pluginDir) | Out-Null
if (Test-Path $pluginDir) { Remove-Item $pluginDir -Recurse -Force }
New-Item -ItemType Junction -Path $pluginDir -Target "C:\path\to\Bossku-AI"
```

**macOS / Linux:**

```bash
git clone https://github.com/wankimmy/Bossku-AI ~/.cursor/plugins/local/bossku-ai
```

Restart Cursor after install. Cursor reads [`.cursor-plugin/plugin.json`](../.cursor-plugin/plugin.json) and the thin rule in [`.cursor/rules/bosskuai.mdc`](../.cursor/rules/bosskuai.mdc).

For team distribution, point a Cursor marketplace at this repository using [`.cursor-plugin/marketplace.json`](../.cursor-plugin/marketplace.json).

### Codex

```bash
codex plugin marketplace add wankimmy/Bossku-AI
```

Restart the ChatGPT desktop app, open the Plugins Directory, choose the **BosskuAI** marketplace, and install **bossku-ai**. Catalog: [`.agents/plugins/marketplace.json`](../.agents/plugins/marketplace.json).

### OpenCode

OpenCode does not use a Claude-style marketplace plugin. Install skills with the CLI, then open this repo as the workspace:

```bash
pip install -e /path/to/Bossku-AI
bossku install --profile full
```

[`.opencode/opencode.jsonc`](../.opencode/opencode.jsonc) references `AGENTS.md`, `skills/`, and `agents/`.

### OMP

On Windows, install OMP with the upstream PowerShell installer:

```powershell
irm https://omp.sh/install.ps1 | iex
```

OMP discovers BosskuAI's existing `~/.agents/skills/` and `~/.claude/skills/` installs, so `bossku install` does not create a third copy. `bossku init` creates a thin `.omp/AGENTS.md` import and a project-local `.omp/config.yml` with `tools.approvalMode: write`.

## Install the CLI

```bash
pip install -e /path/to/Bossku-AI
```

## User-level skills (once per machine)

```bash
bossku install --profile lean --memory-storage obsidian --vault "/path/to/Obsidian/Vault"
```

Pick how much of the library your agent lists in every session:

| Profile | Lists in the agent | Reach the rest | Best for |
|---|---|---|---|
| `lean` (default) | About 25 everyday engineering and process skills with short descriptions | `bossku skills find` / `bossku skills show`, installed whole in `~/.bosskuai/library` | Most people; the smallest per-session cost |
| `core` | Co-founder essentials plus the **loop-engineering** pack | Not installed | A minimal set |
| `full` | All ~235 skills | Already listed | Hosts with a very large skill budget |

Agents spend a fixed share of their context window on the skill list and cut the rest to bare names, so listing everything makes every session pay for skills it never uses. Measured costs are in the [benchmark](benchmarks/README.md). Switch any time by running `bossku install --profile <name>`; `bossku update` keeps your profile. After pulling Bossku-AI changes, run `bossku update` so installed skills match the repo.

`bossku install` also refreshes the Claude Code, Cursor, Codex, and OpenCode hooks by default:

- **Memory sync** (all four tools): Cursor `stop`/`sessionEnd`/`afterAgentResponse`, Claude Code `Stop`/`SessionEnd`, Codex `Stop`/`SessionEnd` via a continue-safe wrapper, OpenCode `session.idle`. In Obsidian mode, hooks check vault availability; canonical notes are written directly to the vault. Legacy repo mode retains curated one-way export. See [memory.md](memory.md).
- **Skill hint** (Claude Code `UserPromptSubmit`): matches your prompt against the whole library and adds one short line naming the best one or two skills and how to load them.
- **Verify gate** (Claude Code `Stop`): if the agent edited source files and ran nothing afterwards, it is sent back once to run the tests or a quick check. It does the same when you asked for a change and the agent edited no file but only pasted code into the reply. It stays silent for questions, reviews, and documentation edits. Switch it off with `BOSSKU_VERIFY_GATE=0`.

Re-run `bossku hooks install` anytime; uninstall with `bossku hooks uninstall`. Codex needs a one-time `/hooks` trust approval in-session before hooks fire.

Skills and their shared `references/` sidecars are copied to:

- `~/.agents/skills/` - Cursor, Codex, OpenCode, and OMP (OpenCode and OMP also scan `~/.claude/skills/`)
- `~/.claude/skills/` - Claude Code, OpenCode, and OMP

Bossku does **not** duplicate skills into `~/.cursor/skills/`, `~/.codex/skills/`, or `~/.config/opencode/skills/`; those tools discover the paths above per their upstream docs.

No symlinks. Unrelated skills in those folders are left untouched.

After `bossku install` or `bossku update`, the JSON includes `tools` (per-tool skill paths) and `agents_count` / `claude_count` (must match). Run `bossku doctor` for a human-readable coverage summary; use `bossku doctor --project .` to verify instruction adapters in a repo.

Coding agents pick skills using each skill's `description` and your project `AGENTS.md`. After pulling changes, run `bossku update`. `bossku skills find "<task>"` returns `selection` with a primary, complements, reasons, deferred candidates, and missing named skills. It defaults to the installed profile; `--profile lean|core|full` overrides it. Each selected skill says how to load it: the Skill tool when the agent lists it, or `bossku skills show <id>` when it lives in the library. Read descriptions and check host capabilities before loading. `matches` are search candidates. Use `bossku skills audit` to measure context size and reference integrity.

## Tool compatibility

| Tool | Plugin / marketplace | Project instructions | Skills |
|---|---|---|---|
| Cursor | [`.cursor-plugin/`](../.cursor-plugin/) | `AGENTS.md` | `~/.agents/skills/` or bundled plugin skills |
| Codex | [`.codex-plugin/`](../.codex-plugin/) + [`.agents/plugins/`](../.agents/plugins/) | `AGENTS.md` | `~/.agents/skills/` or bundled plugin skills |
| OpenCode | [`.opencode/`](../.opencode/) references only | `AGENTS.md` (uses `CLAUDE.md` only if `AGENTS.md` is absent) | `~/.agents/skills/` and `~/.claude/skills/` |
| Claude Code | [`.claude-plugin/`](../.claude-plugin/) | `CLAUDE.md` with a bare `@AGENTS.md` line | `~/.claude/skills/` or bundled plugin skills |
| OMP | [`.omp/`](../.omp/) native project adapter | `.omp/AGENTS.md` importing the canonical `AGENTS.md` | `~/.agents/skills/` and `~/.claude/skills/` |

Keep `AGENTS.md` as the canonical contract. `bossku init` adds `CLAUDE.md` containing only `@AGENTS.md` so Claude Code shares the same rules without duplicating them. On Windows, prefer this import over symlinking `CLAUDE.md` to `AGENTS.md`.

## Per-project adapter

```bash
bossku init /path/to/project
```

Creates:

- Managed block in `AGENTS.md`
- `CLAUDE.md` with `@AGENTS.md`
- `.bossku/project.json`
- Memory templates in the directory returned by `bossku memory-path --project /path/to/project`; Obsidian mode keeps them in the vault
- `.omp/AGENTS.md` importing the canonical project contract
- `.omp/config.yml` with project-scoped `tools.approvalMode: write`

## Portable mode (cloud/shared repos)

```bash
bossku init /path/to/project --portable --profile core
```

## Update / uninstall

```bash
bossku update
bossku doctor
bossku doctor --project /path/to/project
bossku uninstall          # removes managed skills only
bossku uninstall --purge  # also removes ~/.bosskuai/config.json and the BosskuAI hooks
```

Uninstall keeps project memory in its configured location.
