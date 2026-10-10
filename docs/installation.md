# Installation

## Requirements

- Python 3.11+
- Git

## Plugin / marketplace install

Bossku Superpower ships native plugin manifests for Claude Code, Cursor, and Codex. OpenCode uses skill discovery and the root `AGENTS.md`.

### Claude Code

```text
/plugin marketplace add wankimmy/Bossku-Superpowers
/plugin install bossku-superpower@bossku-superpower-marketplace
```

Skills and agents load from this repository via [`.claude-plugin/plugin.json`](../.claude-plugin/plugin.json). Refresh after updates with `/plugin marketplace update` and reinstall if needed.

The plugin lists all 240+ skills and ignores `--profile lean`. It does not add the hooks that `bossku install` sets up (sync, skill hint, verify gate, project notes); its manifest wires only the Node gates in [`hooks/`](../hooks/README.md). Do not run both: their skill lists overlap. A first `bossku install` starts at `--profile lean`; later runs keep your profile (see [User-level skills](#user-level-skills-once-per-machine)).

### Cursor

**Windows (PowerShell):**

```powershell
git clone https://github.com/wankimmy/Bossku-Superpowers $env:USERPROFILE\.cursor\plugins\local\bossku-superpower
```

Or link an existing clone:

```powershell
$pluginDir = "$env:USERPROFILE\.cursor\plugins\local\bossku-superpower"
New-Item -ItemType Directory -Force -Path (Split-Path $pluginDir) | Out-Null
$existing = Get-Item $pluginDir -Force -ErrorAction SilentlyContinue
if ($existing -and $existing.LinkType -ne "Junction") { throw "$pluginDir is a real folder; move it aside first." }
if ($existing) { $existing.Delete() }   # removes the junction only, not the clone it points to
New-Item -ItemType Junction -Path $pluginDir -Target "C:\path\to\Bossku-AI"
```

**macOS / Linux:**

```bash
git clone https://github.com/wankimmy/Bossku-Superpowers ~/.cursor/plugins/local/bossku-superpower
```

Restart Cursor after install. Cursor reads [`.cursor-plugin/plugin.json`](../.cursor-plugin/plugin.json) and the thin rule in [`.cursor/rules/bosskuai.mdc`](../.cursor/rules/bosskuai.mdc).

For team distribution, point a Cursor marketplace at this repository using [`.cursor-plugin/marketplace.json`](../.cursor-plugin/marketplace.json).

The plugin lists all 240+ skills and ignores `--profile lean`. It does not add the hooks that `bossku install` sets up. Do not run both: their skill lists overlap. A first `bossku install` starts at `--profile lean`; later runs keep your profile (see [User-level skills](#user-level-skills-once-per-machine)).

### Codex

```bash
codex plugin marketplace add wankimmy/Bossku-Superpowers
```

Restart the ChatGPT desktop app, open the Plugins Directory, choose the **Bossku Superpower** marketplace, and install **bossku-superpower**. Catalog: [`.agents/plugins/marketplace.json`](../.agents/plugins/marketplace.json).

The plugin lists all 240+ skills and ignores `--profile lean`. It does not add the hooks that `bossku install` sets up. Do not run both: their skill lists overlap. A first `bossku install` starts at `--profile lean`; later runs keep your profile (see [User-level skills](#user-level-skills-once-per-machine)).

### OpenCode

OpenCode does not use a Claude-style marketplace plugin. Install skills with the CLI, then open this repo as the workspace:

```bash
pip install -e /path/to/Bossku-AI
bossku install --profile full
```

OpenCode reads the root `AGENTS.md` and finds skills in `~/.agents/skills/` and `~/.claude/skills/`. [`.opencode/opencode.jsonc`](../.opencode/opencode.jsonc) is a bare settings stub with no references.

### OMP

On Windows, download the upstream PowerShell installer, read it, then run it:

```powershell
irm https://omp.sh/install.ps1 -OutFile "$env:TEMP\omp-install.ps1"
notepad "$env:TEMP\omp-install.ps1"   # read it before you run it
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:TEMP\omp-install.ps1"
```

OMP discovers Bossku Superpower's existing `~/.agents/skills/` and `~/.claude/skills/` installs, so `bossku install` does not create a third copy. `bossku init` creates a thin `.omp/AGENTS.md` import and a project-local `.omp/config.yml` with `tools.approvalMode: write`.

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
| `lean` (default for a first install) | About 25 everyday engineering and process skills with short descriptions | `bossku skills find` / `bossku skills show`, installed whole in `~/.bosskuai/library` | Most people; the smallest per-session cost |
| `core` | Co-founder essentials plus the **loop-engineering** pack | Not installed | A minimal set |
| `engineering` | Every skill except the 47 of the marketingskills pack (about 195) | Already listed | People who build software and do not need the marketing set |
| `full` | All 240+ skills | Already listed | Hosts with a very large skill budget |

Agents spend a fixed share of their context window on the skill list and cut the rest to bare names, so listing everything makes every session pay for skills it never uses. Measured costs are in the [benchmark](benchmarks/README.md). Switch any time by running `bossku install --profile <name>`; `bossku update` and a plain `bossku install` keep your profile (a first install starts at `lean`). After pulling Bossku-AI changes, run `bossku update` so installed skills match the repo.

`bossku install` also refreshes the Claude Code, Cursor, Codex, and OpenCode hooks by default:

- **Memory sync** (all four tools): Cursor `stop`/`sessionEnd`/`afterAgentResponse`, Claude Code `Stop`/`SessionEnd`, Codex `Stop`/`SessionEnd` via a continue-safe wrapper, OpenCode `session.idle`. In Obsidian mode, hooks check vault availability; canonical notes are written directly to the vault. Legacy repo mode retains curated one-way export. See [memory.md](memory.md).
- **Skill hint** (Claude Code and Codex `UserPromptSubmit`, `bossku skill-hint`): matches your prompt against the whole library and adds one short line naming the best one or two skills and how to load them. `hint_mode` in `~/.bosskuai/config.json` picks the policy: `v1` (the default, and what you get when the key is missing) or `v2` (up to three skills, a skill you name by id gets through, under 800 characters). `bossku doctor` prints the mode. `v2` is opt in: in an offline test it was right a little more often when it spoke, but it missed some bars, so `v1` stays the default ([numbers](benchmarks/README.md#skill-hint-v1-against-v2)).
- **Project notes** (Claude Code `SessionStart`, `bossku session-brief`): the newest notes for the folder, at most 1,300 characters. It also adds one line when Codex stopped on its usage limit in this folder, and the skill hint hands over a brief of that Codex task when you then say "continue". That reads Codex's own files read-only and never saves them; see [Resume a Codex task](#resume-a-codex-task-in-claude-code) and `BOSSKU_RESUME=off`.
- **Harness gates** (Claude Code, Node, from a checkout of this repo; described in [`hooks/README.md`](../hooks/README.md)): `PreToolUse` guard that refuses destructive commands (switch `BOSSKU_GUARD=off`), `PostToolUse` syntax and anti-slop check on files the agent writes (`BOSSKU_POST_EDIT=off`, `BOSSKU_SLOP_LINT=off`), `SessionStart` contract (the harness reminder, the `DESIGN.md` pointer), and a `Stop` gate: if the agent edited source files and ran nothing afterwards, it is sent back once to run the tests or a quick check (`BOSSKU_STOP_GATE=off`). The same install adds a short `permissions.deny` list to `~/.claude/settings.json` (`git reset --hard`, `git clean -f`, `git push -f`, `migrate:fresh`, `db:wipe`, `docker compose down`, `docker-compose down`, `docker system prune`), and `bossku hooks uninstall` takes it out again.
- **Verify gate** (Claude Code `Stop`, `bossku verify-gate`, Python): used instead of the Node stop gate when you install with `--no-harness`, or when there is no `node` or no checkout. Besides the run-your-code check it sends the agent back once when you asked for a change and it only pasted code into the reply, and once when your message stated a rule and the turn ended without `bossku remember`. The Node stop gate does not do those two. Switch it off with `BOSSKU_VERIFY_GATE=0`, which does nothing while the Node gate is the one wired.
- **Subagent contracts**: the six files in `agents/` (orchestrator, planner, designer, executor, auditor, final-reviewer) are copied to `~/.claude/agents`.

Install choices: `--no-claude` leaves out the skills in `~/.claude/skills` (for a machine where a Claude Code plugin serves them), `--no-agents` leaves out the subagent contracts, and `--no-harness` leaves out the Node gates and the deny list and takes ours out again. Each flag has a positive form (`--claude`, `--agents`, `--harness`). Left out, `install` and `update` keep the saved choice, and a first install turns all three on.

### Skill list budget (Claude Code)

On the `engineering` and `full` profiles Claude Code may cut the descriptions of your skills, and then picks them worse. What is known (Claude Code 2.1.293, checked 10 October 2026):

- Claude Code shows the model a list of skills with the name, `description` and `when_to_use` of each. The list is capped at `skillListingBudgetFraction` times the context window, a setting in `~/.claude/settings.json` that is `0.01` when missing. That is about 3 characters per token. See [skill descriptions are cut short](https://code.claude.com/docs/en/skills.md#skill-descriptions-are-cut-short) and [`skillListingBudgetFraction`](https://code.claude.com/docs/en/settings-reference.md#skilllistingbudgetfraction).
- Over the budget, it keeps every name and drops descriptions, starting with the skills you use least. `claude --debug` then logs `Skill listing over budget: <N> skills, <C> chars > <B> budget`.
- Measured at `0.01`: 30,000 characters on `claude-opus-5-5` (1M context), 6,000 on `claude-sonnet-5-5` and `claude-haiku-5-5` (200K context). On one machine 267 skills took 98,037 characters, and `0.035` removed the warning on Opus. The `SKILL.md` files on that machine estimate to only 81,157 characters, so the other 16,880 are entries bossku cannot see (most likely Claude Code's bundled skills) and format overhead.
- One skill's `description` plus `when_to_use` is cut at `skillListingMaxDescChars` (1536 by default). Skills with `disable-model-invocation` are not listed.

`bossku doctor` adds a line that estimates this from the `SKILL.md` files in `~/.claude/skills` (`--project` adds the project's `.claude/skills`, and reads the two settings from the project's `.claude/settings.local.json` and `.claude/settings.json` too, because they override the user file; the line names the file when the fraction comes from one). Managed settings and `--settings` rank higher still and `doctor` cannot see them. It also ignores the `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable and `skillOverrides`, which change the list too. It says, for a 1M-context and a 200K-context model, whether the list fits and about how many descriptions would be cut, and which fraction would fit on a 1M-context model (the line is always shown). It is a warning and never makes `doctor` fail. Skills from plugins and Claude Code's own bundled skills count too, so the real list is larger than the estimate. For that reason the 1M-context check and the fraction include 16,880 characters of headroom for them, the gap measured above; the 200K-context line counts the `SKILL.md` files only. The headroom is one measurement on one machine with no plugins, so a machine with plugin skills may need a higher fraction by hand. For this repo the estimate is about 2,600 characters for `lean`, 5,100 for `core`, 48,000 for `engineering` and 81,000 for `full`: the first two fit at the default, the last two do not.

No skill is shortened, hidden or removed to fit; the fix is the setting. It costs context, because the whole list is sent in every session (about 1 token per 3 characters, so 98,037 characters is about 33,000 tokens), so it is opt in:

```bash
bossku install --fit-skill-list     # or: bossku update --fit-skill-list
```

This sets `skillListingBudgetFraction` to the fraction that fits the estimated list plus that headroom on a 1M-context model, rounded up to the next `0.005` (`0.035` for the 81,157-character list above, where the files alone would give `0.03` and still lose descriptions). It sizes from `~/.claude/skills` only, not from a project's `.claude/skills`. If the file is locked or cannot be written (read-only, for example), the install still finishes, the summary says `not changed (failed: ...)`, and no `settings.json.tmp` is left behind. Make the file writable and run the command again. It never lowers a value that is already higher, keeps every other key in `settings.json`, and keeps a `settings.json.bak-<time>` copy before it changes the file. The choice is saved in `~/.bosskuai/config.json`, so a later `bossku update` repeats it after new skills arrive; a default install does not touch the setting. A 200K-context model needs a fraction 5 times higher for the same list, which `--fit-skill-list` does not set.

To undo it, run `bossku install --no-fit-skill-list` (it stops raising the value and leaves the one in `settings.json` as it is), then delete `skillListingBudgetFraction` from `~/.claude/settings.json` or set it lower by hand. A cheaper fix is a smaller profile: `bossku install --profile lean`.

Summary or JSON: `install`, `update`, `init`, `uninstall`, `remember`, `sync`, `hooks install`, `hooks uninstall`, `vault sync` and `vault tidy --apply` print a short summary when stdout is a terminal (what changed, what was skipped and why, and one next step). When stdout is a pipe or a file, which is how scripts and agents usually run them, they print the JSON described on this page, unchanged. An agent that runs commands in a real terminal gets the summary, so anything that parses the output should pass `--json`. In a terminal `--json` gives the JSON too; for `vault tidy` it applies with `--apply` (without it only the plan is printed). Exit codes are the same either way. `memory-path`, `skills find`, `skills index` and the hook commands print what they always did.

Re-run `bossku hooks install` anytime; uninstall with `bossku hooks uninstall`. Codex needs a one-time `/hooks` trust approval in-session before hooks fire.

### Resume a Codex task in Claude Code

When Codex stops on its usage limit, open the same folder in Claude Code and say "continue". The session hook shows a one-line pointer on a new session, and `UserPromptSubmit` then hands Claude a brief of at most 2,000 characters (the request, the plan, the files and the last three commands with common secret shapes blanked out (a pattern list, not a guarantee), and Codex's last message). It is context only: it goes into the chat, never into the vault. `bossku resume` prints the same brief by hand, and `bossku resume --debug` shows the structure of the Codex files without any text. `BOSSKU_RESUME=off` switches both hooks off. See [`SECURITY.md`](../SECURITY.md#hooks) for what is read and written.

Codex also needs `[features] hooks = true` in `~/.codex/config.toml`. Install sets it when `~/.codex` exists, leaves an explicit `hooks = false` alone, and does not edit a config that is not valid TOML. In those two cases the Codex entry in the JSON shows `status` `disabled_by_user` or `skipped_invalid_toml` with a warning, even when it also added entries to `~/.codex/hooks.json` (check its `added` list); set the line by hand. `bossku install`, `bossku update`, `bossku hooks install`, `bossku hooks uninstall` and `bossku uninstall` exit 1 when a hook tool reports `status` `error`.

Skills and their shared `references/` sidecars are copied to:

- `~/.agents/skills/` - Cursor, Codex, OpenCode, and OMP (OpenCode and OMP also scan `~/.claude/skills/`)
- `~/.claude/skills/` - Claude Code, OpenCode, and OMP

Bossku does **not** duplicate skills into `~/.cursor/skills/`, `~/.codex/skills/`, or `~/.config/opencode/skills/`; those tools discover the paths above per their upstream docs.

No symlinks. Unrelated skills in those folders are left untouched.

After `bossku install` or `bossku update`, the JSON includes `tools` (per-tool skill paths) and `agents_count` / `claude_count` (must match). Run `bossku doctor` for a human-readable coverage summary; use `bossku doctor --project .` to verify instruction adapters in a repo. `bossku doctor` prints `doctor: issues found` and exits 1 when an installed skill differs from the repo (run `bossku update`), the install source folder is gone, a hook in `~/.claude/settings.json` runs a program that no longer exists, that file is not valid JSON, or - with `--project` - the project's managed block in `AGENTS.md` is out of date. This repo's own `AGENTS.md` keeps a short stub block on purpose, so doctor does not call it out of date. Missing Claude Code hook pieces (the verify gate, for example) are only named on the `claude_code hooks` line; doctor does not fail on them, because leaving one out can be a choice.

Coding agents pick skills using each skill's `description` and your project `AGENTS.md`. After pulling changes, run `bossku update`. `bossku skills find "<task>"` returns `selection` with a primary, complements, reasons, deferred candidates, and missing named skills. It defaults to the installed profile; `--profile lean|core|engineering|full` overrides it. Each selected skill says how to load it: the Skill tool when the agent lists it, or `bossku skills show <id>` when it lives in the library. Read descriptions and check host capabilities before loading. `matches` are search candidates. Use `bossku skills audit` to measure context size and reference integrity. `bossku skills find "<task>" --brief` prints one line per selected skill (id, score, `SKILL.md` path, what it is for) instead of the JSON.

### Optional tools

`bossku tools list` shows the optional programs the skills use (Headroom, MarkItDown, Graphify, browser-use, OpenDataLoader PDF, Graft, e2e, Cypress, Archify, Moli, Hindsight, dcg) and which are installed. `bossku tools install <tool>` prints the exact commands and any telemetry notice and runs nothing; add `--yes` to run it (pip and npm tools only). Moli, Hindsight and dcg are set up by hand, because their installers are a script piped into a shell or an unsigned binary. `e2e` and `cypress` are per project: they change the project in the current folder (or `--project <folder>`), never the machine. Cypress needs Node 22, 24 or 26 and newer, downloads its binary during install, and sends crash reports to `api.cypress.io` unless `CYPRESS_CRASH_REPORTS=0` is set. Bossku does not log in to Cypress Cloud or set a record key.

## Tool compatibility

| Tool | Plugin / marketplace | Project instructions | Skills |
|---|---|---|---|
| Cursor | [`.cursor-plugin/`](../.cursor-plugin/) | `AGENTS.md` | `~/.agents/skills/`, or the plugin (lists every skill, ignores `--profile`) |
| Codex | [`.codex-plugin/`](../.codex-plugin/) + [`.agents/plugins/`](../.agents/plugins/) | `AGENTS.md` | `~/.agents/skills/`, or the plugin (lists every skill, ignores `--profile`) |
| OpenCode | none ([`.opencode/`](../.opencode/) is a settings stub) | `AGENTS.md` (uses `CLAUDE.md` only if `AGENTS.md` is absent) | `~/.agents/skills/` and `~/.claude/skills/` |
| Claude Code | [`.claude-plugin/`](../.claude-plugin/) | `CLAUDE.md` with a bare `@AGENTS.md` line | `~/.claude/skills/`, or the plugin (lists every skill, ignores `--profile`) |
| OMP | [`.omp/`](../.omp/) native project adapter | `.omp/AGENTS.md` importing the canonical `AGENTS.md` | `~/.agents/skills/` and `~/.claude/skills/` |

Keep `AGENTS.md` as the canonical contract. `bossku init` adds `CLAUDE.md` containing only `@AGENTS.md` so Claude Code shares the same rules without duplicating them. On Windows, prefer this import over symlinking `CLAUDE.md` to `AGENTS.md`. In this repo, `bossku validate` fails when `AGENTS.md` is over 16,000 characters, because every session loads it.

## Per-project adapter

```bash
bossku init /path/to/project
```

Creates:

- Managed block in `AGENTS.md`
- `CLAUDE.md` with `@AGENTS.md`
- `.bossku/project.json`
- `.bossku/DESIGN.md`, a stub for the designer contract to fill in (not written when `DESIGN.md`, `design/DESIGN.md` or `.bossku/DESIGN.md` already exists)
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
bossku uninstall          # removes managed skills, the library and unchanged shared files; the hooks, the config, and the memory and voice blocks in your CLAUDE.md / AGENTS.md stay
bossku uninstall --purge  # also removes ~/.bosskuai/config.json, the Bossku Superpower hooks, and those two blocks from ~/.claude/CLAUDE.md, ~/.codex/AGENTS.md and ~/.config/opencode/AGENTS.md
```

Uninstall keeps project memory in its configured location. It deletes the shared `references/`, `site/` and `docs/memory.md` copies under `~/.agents` and `~/.claude` only when they are unchanged from the repo, so a file you edited stays.
