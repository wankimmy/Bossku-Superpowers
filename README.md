# BosskuAI

Open-source AI co-founder toolkit for **Cursor**, **Claude Code**, **Codex**, **OpenCode**, and **OMP**.

One canonical skill library, plan → execute → audit agents, project memory, and the `bossku` CLI — optional one-way Obsidian export for durable memory.

## Quick start

```bash
git clone https://github.com/wankimmy/Bossku-AI bosskuAI
cd bosskuAI
pip install -e .
bossku install --vault "C:/path/to/your/Obsidian/Vault"
cd /path/to/your/project
bossku init .
```

`bossku install` refreshes denser Obsidian auto-sync hooks by default (curated one-way
export only). Codex needs a one-time in-session `/hooks` trust approval. Details:
[docs/memory.md](docs/memory.md).

Open the project in any supported coding agent. Say `bossku` or ask for cofounder mode.

## Plugin / marketplace install

Install BosskuAI as a native plugin on Claude Code, Cursor, and Codex. OpenCode uses skill discovery plus the `.opencode` harness (no marketplace plugin).

### Claude Code

Run inside Claude Code:

```text
/plugin marketplace add wankimmy/Bossku-AI
/plugin install bossku-ai@bosskuai-marketplace
```

Manifests: [`.claude-plugin/`](.claude-plugin/).

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

Restart Cursor after install. Manifests: [`.cursor-plugin/`](.cursor-plugin/).

### Codex

```bash
codex plugin marketplace add wankimmy/Bossku-AI
```

Then restart the ChatGPT desktop app, open **Plugins**, choose the **BosskuAI** marketplace, and install **bossku-ai**. Manifests: [`.codex-plugin/`](.codex-plugin/) and [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json).

### OpenCode

No marketplace plugin. Install skills once per machine, then open this repo (or any `bossku init` project) as the workspace:

```bash
pip install -e /path/to/Bossku-AI
bossku install --profile full
```

OpenCode reads [`.opencode/opencode.jsonc`](.opencode/opencode.jsonc) for `AGENTS.md` and agent references.

### OMP

Install the native Windows binary, then open this repository from OMP:

```powershell
irm https://omp.sh/install.ps1 | iex
omp --cwd C:\path\to\Bossku-AI
```

OMP reads the canonical contract through [`.omp/AGENTS.md`](.omp/AGENTS.md) and discovers the same user-level skills installed for the other tools. The project config uses `tools.approvalMode: write`, so workspace writes can proceed while actions outside the workspace still require approval.

See [`docs/installation.md`](docs/installation.md) for the CLI path and per-project setup.

## Commands

| Command | Purpose |
|---|---|
| `bossku install` | Copy skills to `~/.agents/skills` and `~/.claude/skills` |
| `bossku init <project>` | Add cross-tool adapters + `.bossku/memory/` |
| `bossku init <project> --portable` | Vendor skills into the project |
| `bossku update` | Refresh user-level skills from this repo |
| `bossku remember --project . --kind decision "..."` | Save curated memory |
| `bossku sync --project .` | Export memory to Obsidian |
| `bossku skills find "laravel security"` | Suggest a primary + complementary skill stack |
| `bossku skills audit` | Measure description context cost and skill integrity |
| `bossku doctor` | Install health check |
| `bossku validate --root .` | Repository validation |

## Layout

- [`AGENTS.md`](AGENTS.md) — cross-tool contract
- [`skills/`](skills/) — canonical skill library (~240 skills, including vendored packs)
- [`skills/vendored.json`](skills/vendored.json) — third-party skill provenance
- [`agents/`](agents/) — orchestrator, planner, executor, auditor, final reviewer
- [`.claude-plugin/`](.claude-plugin/) — Claude Code plugin + marketplace manifests
- [`.cursor-plugin/`](.cursor-plugin/) — Cursor plugin + marketplace manifests
- [`.codex-plugin/`](.codex-plugin/) — Codex plugin manifest
- [`.agents/plugins/`](.agents/plugins/) — Codex marketplace catalog
- [`.opencode/`](.opencode/) — OpenCode references harness
- [`.omp/`](.omp/) - OMP project instructions and safe approval defaults
- [`bossku/`](bossku/) — CLI package (stdlib only)
- [`docs/third-party.md`](docs/third-party.md) — MIT attribution for vendored packs

## Vendored skill packs

BosskuAI ships skills from **marketingskills**, **superpowers**, **hallmark**, **taste-skill**, **loop-engineering**, **scroll-world**, **emil-skills**, **i-have-adhd**, a curated **ECC** subset, **browser-use**, **graft**, **graphify**, and a thin **markitdown** wrapper. Use `bossku install --profile full` to install all of them.

Optional CLIs for some packs: see [`requirements-optional.txt`](requirements-optional.txt).

## Archive

The Docker/Laravel/Nuxt product MVP is preserved on branch `archive/product-mvp-2026-07`.

## License

MIT — see [`LICENSE`](LICENSE).

## Claude Code practice review

The [coverage review](docs/claude-practices-review.md) maps the reviewed Claude Code course README to BosskuAI's skill guidance, existing packs, examples, and host-specific features. The [practice playbook](references/playbooks/claude-code-practices-playbook.md) covers skill design, startup context, discovery, invocation, and permissions.

- [`bosskuai-product-verification`](skills/bosskuai-product-verification/SKILL.md) verifies real user paths and CLI behavior with observed evidence.
- [`bosskuai-hindsight-memory`](skills/bosskuai-hindsight-memory/SKILL.md) integrates an approved, configured Hindsight connection with project-scoped memory. Its optional runtime is separate from the BosskuAI skill installation.

`bossku init` repairs instruction adapters even when an existing file mentions the import only in prose or a fenced example, preserving the original instructions.
