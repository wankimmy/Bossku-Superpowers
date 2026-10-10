# Bossku Superpowers

**Make your AI coding agent work properly: pick the right skill, run its own code, and remember your project rules.** Free and open source ([MIT](LICENSE)).

Works with **Claude Code, Cursor, Codex, OpenCode and OMP**.

*Formerly BosskuAI. The `bossku` command and `bosskuai-*` skill names are the same, so your skills, hooks and notes still work. If you installed the plugin from a marketplace, reinstall it once.*

![What Bossku Superpower adds around your agent. You ask; your agent picks a skill, does the work, runs it, and gives you a checked result. Behind it: 240+ skills found for you, optional tools, a check that sends the agent back if it never ran its code, and your notes saved in Obsidian.](docs/assets/superpower-overview.svg)

## Why use it?

Your agent is smart, but it forgets your rules and sometimes says "done" without testing anything. Bossku Superpower fixes that.

| Problem | What Bossku Superpower does |
|---|---|
| Agent doesn't know which skill to use | Picks the best skill for your request from 240+ skills |
| Agent writes code but never runs it | Sends the agent back once to run it |
| Agent runs a command that destroys work | Refuses `git reset --hard`, force push, `rm -rf ~` and similar, and tells you how to run it yourself (Claude Code) |
| You told it a rule yesterday, today it forgot | Saves rules and decisions as notes and shows them next session |
| Codex stopped on its usage limit | Claude Code can pick the task up in the same folder with `bossku resume` |
| Useful tools are hard to set up | `bossku tools list` shows what's available. Nothing installs unless you say yes |

Skills load only when needed. Hooks are on after `bossku install`: turn off the run-your-code check with `BOSSKU_STOP_GATE=off` (the Node stop gate, the default), or with `BOSSKU_VERIFY_GATE=0` only if you installed with `--no-harness`. Remove all hooks with `bossku hooks uninstall`. The other Node gates in [`hooks/`](hooks/README.md) have their own switches, listed there.

## Does it really help?

We tested it with real agents on the same tasks, with and without Bossku Superpower.

![With and without Bossku Superpower: the share of two-session tasks passed, where the second session breaks a project rule unless it is remembered](docs/assets/benchmark-memory.svg)

- **Memory is the biggest win.** When a rule is set in one session and needed in the next, Claude Haiku 4.5 (48% → 68%), Claude Sonnet 5.5 (64% → 84%) and Gemma 4 31B (39% → 68%) passed 20 to 30 points more tasks.
- **Models that skip testing run their code more.** Gemma and Nemotron ran their code far more often. Small Nemotron passed more HumanEval problems (62% → 92%).
- **Better skill picking.** The right skill ranked first 81% of the time, vs 56% for keyword search.
- **The catch: more tokens.** About 1.1× to 4.7× the tokens per run, highest on models that checked the least before.
- **No clear change on coding and harder tasks** for any model. Samples are small, so read each result with its interval.
- **Which setup was measured.** Build `b8ccea1`, whose Stop hook was the Python verify gate. It also sent the agent back to save a rule it was told and to edit a file instead of pasting code. A default install now uses the Node stop gate, which only checks that code was run, so those two Stop reminders are not in it (the rule reminder on your prompt is). `bossku install --no-harness` brings the Python gate back. Details: [memory](docs/memory.md#automatic-remembering).

Full numbers, charts and limits: [benchmark results](docs/benchmarks/results.md) and the [10 October run](docs/benchmarks/results-2026-10-10.md). How it was tested: [benchmark notes](docs/benchmarks/README.md).

## Quick start

Need **Python 3.11+** and **Git**. About five minutes:

1. **Get it.** `git clone https://github.com/wankimmy/Bossku-Superpowers`, then `cd Bossku-Superpowers` and `pip install -e .`
2. **Set up your machine.** `bossku install`. It copies the skills and the six subagents and turns on the hooks. In a terminal it prints a short summary and the next step (`--json` prints JSON instead; piped, it is always JSON). Want notes in Obsidian? Add `--vault "/path/to/your/Obsidian/Vault" --memory-storage obsidian`.
3. **Set up a project.** `cd /path/to/your/project`, then `bossku init .`. It adds a short Bossku block to `AGENTS.md` and a `CLAUDE.md` that imports it.
4. **Check it.** `bossku doctor --project .` prints `doctor: ok`, or `doctor: issues found` and what to fix.
5. **Use your agent.** Open the project in it and say `bossku`. Mostly you will not notice anything. On Claude Code the agent is told which skill fits each request, reads your saved notes at session start, is refused a destructive command such as `git reset --hard`, and is sent back once to run its code if it edited files and ran nothing.
6. **Turn things off.** `bossku install --no-harness` leaves out the safety gates. `BOSSKU_STOP_GATE=off` (set in the shell that starts your agent) switches off only the run-your-code check. `BOSSKU_RESUME=off` switches off the hooks that read Codex's session files. `bossku hooks uninstall` removes every hook, and `bossku uninstall --purge` removes the skills, subagents, config and hooks.

More choices:

- **Where are my notes?** In `.bossku/memory` inside the project, unless you chose Obsidian storage in step 2.
- **Want all skills listed?** A first install starts at `--profile lean` (about 25 listed, the rest one command away); a later `bossku install` keeps your profile. Use `--profile core` for a small set, `--profile engineering` for everything except the marketing skills, or `--profile full` for all 240+.
- **Claude Code cutting skill descriptions?** On the full profile, Claude Code may cut skill descriptions; `bossku doctor` tells you, and `--fit-skill-list` fixes it at a context cost ([details](docs/installation.md#skill-list-budget-claude-code)).
- **Other tools?** See setup for [Claude Code](docs/installation.md#claude-code), [Cursor](docs/installation.md#cursor), [Codex](docs/installation.md#codex), [OpenCode](docs/installation.md#opencode), [OMP](docs/installation.md#omp) or [portable mode](docs/installation.md#portable-mode-cloudshared-repos).

## What's inside

| Part | What it is |
|---|---|
| **240+ skills** | Short checklists for engineering, product, design, security, marketing and founder work |
| **Helper hooks** (Claude Code; Codex gets the skill hint too) | Suggest a skill for your prompt and show your saved notes at session start. `hint_mode` `v2` in `~/.bosskuai/config.json` suggests up to three skills per prompt: it is opt in, because it missed some bars in its [offline test](docs/benchmarks/README.md#skill-hint-v1-against-v2) |
| **Safety gates** (Claude Code) | Refuse destructive commands (`git reset --hard`, `rm -rf ~`), check the syntax of files the agent writes, and send the agent back once if it never ran its code. [Details and switches](hooks/README.md). Leave them out with `bossku install --no-harness` |
| **Subagents** (Claude Code) | Six contracts (orchestrator, planner, designer, executor, auditor, final-reviewer), copied to `~/.claude/agents`. Leave them out with `--no-agents` |
| **Resume** | When Codex stops on its usage limit, Claude Code shows the task's brief in the same folder after you say "continue". Context only: nothing is saved |
| **Tools** | Optional programs like Headroom, Moli, e2e, Cypress, Archify, Graft and MarkItDown. Installed only when you ask. Cypress goes into one project, never global |
| **Memory** | Your rules, decisions and lessons, saved in Obsidian, one folder per project |

## Your notes in Obsidian

![Where notes come from and where they go. Saved notes, Claude's own memory and your rules files are copied into one folder per project in your Obsidian vault by an automatic sync after every session; an index links everything, and the newest notes are shown at the start of the next session.](docs/assets/superpower-memory.svg)

The agent saves a note only when a future session needs it: a decision, a plan, a fact or a lesson. Secrets are blanked out, and prompts or transcripts are never saved. After each session the notes sync to your vault. It only **copies**, your originals stay put. If the vault is missing, it tells you the note was not saved.

```bash
bossku remember --project . --kind decision "Use the existing test runner for this project."
bossku memory-brief --project .       # newest notes
bossku vault sync --project .         # sync to the vault now
bossku vault tidy                     # preview a clean-up (nothing changes)
```

More in [memory and Obsidian](docs/memory.md).

## Common commands

| Command | What it does |
|---|---|
| `bossku skills find "<task>"` | Show which skill fits and why (`--brief`: one line per skill) |
| `bossku skills show <id>` | Print one skill |
| `bossku tools list` | See optional tools and what's installed |
| `bossku tools install <tool>` | Show the plan for a tool. Add `--yes` to run it (pip and npm tools only). `cypress` installs into the current project only |
| `bossku init <project>` | Set up a project (`--portable` puts the skills inside it) |
| `bossku hooks install` / `uninstall` | Add or remove the helper hooks |
| `bossku install --no-harness` | Leave out the safety gates and deny rules. `--no-agents` leaves out the subagents, `--no-claude` the skills in `~/.claude/skills` |
| `bossku resume` | Show the brief of a Codex task that stopped on its usage limit in this folder (nothing is saved) |
| `bossku doctor --project .` | Check your setup |
| `bossku update` | Refresh installed skills (run after `git pull`) |

## For contributors

```bash
python -m bossku skills index --root .   # only if a skill or routing input changed (a SKILL.md, aliases.json, vendored.json, curated triggers)
python -m bossku validate --root .
python -m unittest discover -s tests -v
```

## Learn more

- [Skills](skills/) and [shared instructions](AGENTS.md)
- [Benchmark results](docs/benchmarks/results.md) and [how they were measured](docs/benchmarks/README.md)
- [Third-party packs and credits](docs/third-party.md), plus [optional requirements](requirements-optional.txt)
- [Claude Code practice review](docs/claude-practices-review.md) and [Archify practice review](docs/archify-practices-review.md)

## License

[MIT](LICENSE). Vendored skills keep their own licenses: see [third-party](docs/third-party.md).
