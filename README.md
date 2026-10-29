# Bossku Superpowers

**Skills tell your AI coding agent what to do. Bossku checks that it did.**

Free and open source ([MIT](LICENSE)). Works with **Claude Code, Codex, Cursor, OpenCode and OMP**, and is strongest in Claude Code.

**Website:** [wankimmy.github.io/Bossku-Superpowers](https://wankimmy.github.io/Bossku-Superpowers/)

*Formerly BosskuAI. The `bossku` command, the `bosskuai-*` skill names and the `~/.bosskuai` config folder did not change, so your skills, hooks and notes still work. If you installed the plugin from a marketplace, reinstall it once.*

![What Bossku Superpower adds around your agent. You ask; your agent picks a skill, does the work, runs it, and gives you a checked result. Behind it: 670+ skills found for you, optional tools, a check that sends the agent back if it never ran its code, and your notes saved in Obsidian.](docs/assets/superpower-overview.svg)

## What makes it different

1. **It checks, not just advises.** A skill is text the agent may or may not follow. Bossku adds hooks that act at the right moment. In Claude Code, `git reset --hard`, a plain force push and similar commands are refused, a `git push` waits for your yes, and a turn that edited code with no check after it is sent back once.
2. **It remembers.** The agent is told to save the rules and decisions you give as notes. In Claude Code the newest notes show when the next session starts, and every 50 tool calls the agent is asked to turn useful lessons into small skills.
3. **One install for your tools.** `bossku install` makes the same skills available to Claude Code, Codex, Cursor, OpenCode and OMP, and writes seven subagent contracts for Claude Code, Codex, Cursor, OpenCode and Devin.
4. **Measured in public.** Benchmarks with and without Bossku are published with their limits (see [Does it really help?](#does-it-really-help)).

## What it does

| Problem | What Bossku does |
|---|---|
| Agent doesn't know which skill to use | Names up to three fitting skills from 670+ when your request clearly matches |
| Agent writes code but never runs it | Sends the agent back once if it edited code and ran no test, lint, build or run after the last edit |
| Agent runs a command that destroys work | Refuses `git reset --hard`, a plain force push, `rm -rf ~` and similar, and tells the agent to give you the exact command and recovery steps |
| Agent pushes, merges or deploys on its own | Asks you first before `git push`, a PR merge, `npm publish`, `vercel --prod`, `terraform destroy` and similar (`BOSSKU_GUARD_ASK=off` for an approved autonomous loop) |
| You told it a rule yesterday, today it forgot | Asks the agent to save rules and decisions as notes; Claude Code shows the newest notes when the next session starts |
| It relearns the same lesson every week | Auto-learn asks the agent to save useful lessons as small skills. `BOSSKU_AUTO_LEARN=off` turns it off |
| Codex stopped on its usage limit | Open Claude Code in the same folder and say "continue": it loads the task's brief. `bossku resume` shows the brief in a terminal |
| Useful tools are hard to set up | `bossku tools list` shows what's available. Nothing installs unless you say yes |

Hooks are on after `bossku install`. Turn off the run-your-code check with `BOSSKU_STOP_GATE=off` (the default Node stop gate). `BOSSKU_VERIFY_GATE=0` works only when the Python verify gate is the Stop hook, as after `bossku install --no-harness`. Remove the hooks with `bossku hooks uninstall`. The Node hooks and their switches: [`hooks/`](hooks/README.md). Auto-learn and the security gate have their own switches, listed in [AGENTS.md](AGENTS.md).

## What Claude Code already does

Bossku is built on features Claude Code already has. Here is what is native and what Bossku adds.

| Area | Built into Claude Code | What Bossku adds |
|---|---|---|
| Skills | Loads a skill when its description fits | 670+ skills, most vendored or adapted from other open-source packs, plus a hook that names fitting skills when the match is clear |
| Memory | `CLAUDE.md` files and its own auto memory | Notes per project shown at session start, optional Obsidian sync, auto-learn |
| Ask before push | Permission rules can allow, ask or deny a command by its pattern | A ready-made rule set. Cursor and OpenCode 2 ask too; Codex and OpenCode 1 refuse and hand the command to you |
| Run your code | Stop hooks you can write yourself | The check itself: one push back if code changed and no check ran after the last edit |
| Subagents | Supported | Seven written contracts, rewritten for Codex, Cursor, OpenCode and Devin |

Good to know:

- **What is enforced.** In Claude Code, a stop hook sends the agent back once when a turn changed code, a dependency file or infra config and the reply has no `Security gate:` line. It checks that the line is there; it does not run a scanner, and nothing checks the review was real. The three-line answer header is only an instruction.
- **What the guard sees.** It checks the command the agent runs. A push hidden inside a script (`bash push.sh`) is not seen.
- **Other hosts.** The guard runs in Claude Code. The Codex, Cursor and OpenCode versions are unit-tested against each tool's hook format, not yet run inside those apps. OMP gets the skills only.
- **Where the skills come from.** Most come from other packs (Superpowers, ECC, marketingskills, MengTo and more), each [credited with its license](docs/third-party.md).

## Does it really help?

We ran real agents on the same tasks, with and without Bossku.

![With and without Bossku Superpower: the share of two-session tasks passed, where the second session breaks a project rule unless it is remembered](docs/assets/benchmark-memory.svg)

- **Memory gave the clearest gain.** When a rule was set in one session and needed in the next, Claude Haiku 4.5 (48% → 68%), Claude Sonnet 5.5 (64% → 84%) and Gemma 4 31B (39% → 68%) passed 20 to 30 points more tasks. DeepSeek V4.1 Flash (79% → 74%) and Nemotron 3 Nano 30B (6% → 9%) showed no clear difference.
- **Models that skip testing run their code more.** Small Nemotron passed 37 of 40 sampled HumanEval problems with Bossku, against 25 of 40 without (the runs without were on other days).
- **Skill picking.** An acceptable skill ranked first 81% of the time on 158 new requests, against 56% for a keyword baseline that uses only skill names and descriptions. The acceptable skills were labelled by AI models, not people.
- **The catch: tokens.** About 1.0× to 4.7× the tokens per run, highest on models that checked the least before.
- **No clear change in pass rate on coding and harder tasks** for the three open models tested. Claude models were not run on those. Samples are small, so read each result with its interval.

Read the setup before you trust the numbers:

- The "without" runs had no Bossku setup, no `CLAUDE.md` and Claude Code's own auto memory switched off. The Claude runs still used the tester's own Claude Code config, which listed 20 skills and 2 plugins at start. So the memory result shows Bossku against **no memory**, not against Claude Code's own memory or a rule you wrote in `CLAUDE.md`. That was not tested.
- Skill picking was compared with keyword search, not with Claude Code's own skill choice. With a real agent, an acceptable skill was opened for 45% of 60 requests.
- The agent runs used build `b8ccea1`, whose stop check also reminded the agent to save rules. Today's default install uses a simpler check (details: [memory](docs/memory.md#automatic-remembering)). Session costs come from build `02ee2f2` and the live skill-use check from `8279f19`.

Full numbers: [benchmark results](docs/benchmarks/results.md) and the [10 October run](docs/benchmarks/results-2026-10-10.md). How it was tested: [benchmark notes](docs/benchmarks/README.md).

## How does it compare with other skill packs?

On 29 October 2026 we ran Bossku (lean profile, the code of commit `d93b529`), four other packs and Claude Code with nothing added, on the same tasks, the same day, with Claude Haiku 4.5 and Claude Sonnet 5.5.

| Setup | Rule remembered in the next session (44 tasks) | Coding tasks (34) | Cost per run vs no pack |
|---|---|---|---|
| **Bossku** | **33 (75%)** | 32 | +38% to +42% |
| No pack | 23 (52%) | 32 | |
| ECC | 22 (50%) | 31 | +80% to +90% |
| Anthropic skills | 22 (50%) | 32 | +6% |
| Superpowers | 20 (45%) | 31 | +13% to +26% |
| Karpathy guidelines | 20 (45%) | 31 | -3% to +4% |

- **Where Bossku wins: remembering your rules.** Bossku passed more of the two-session tasks than each other setup, a gap unlikely to be luck (exact tests, p 0.04 or lower against each).
- **Where nobody wins: coding.** All six passed 31 or 32 of 34.
- **What it costs.** About 40% more per run than no pack (for the memory tasks, the graded session only). Karpathy's guidelines and Anthropic's skills cost about the same as no pack.

Be fair to the others when you read this. Superpowers, Karpathy's guidelines and Anthropic's skills are not built to carry your rules between sessions. ECC is, but its hooks failed to start on this Windows machine, so its memory never ran. Only Bossku came with instructions (including "save every rule the user states"), so the result is for the whole Bossku bundle. `CLAUDE.md` and Claude Code's own auto memory were off for everyone. The tasks are Bossku's own, and each ran once. Full method and limits: [pack comparison](docs/benchmarks/results-2026-10-29-packs.md).

## Quick start

You need **Python 3.11+** and **Git**. Six steps:

1. **Get it.** `git clone https://github.com/wankimmy/Bossku-Superpowers`, then `cd Bossku-Superpowers` and `pip install -e .` (if `bossku` is not found afterwards, use `python -m bossku`).
2. **Set up your machine.** `bossku install` copies the skills, writes the subagent contracts for every tool you have set up, and turns on the hooks. Want notes in Obsidian? Add `--vault "/path/to/your/Obsidian/Vault" --memory-storage obsidian`.
3. **Set up a project.** `cd /path/to/your/project`, then `bossku init .`. It adds a Bossku block to `AGENTS.md`, a `CLAUDE.md` that imports it, and small `.omp/` and `.bossku/` files.
4. **Check it.** `bossku doctor --project .` prints `doctor: ok`, or the issues found and what to fix.
5. **Use your agent.** Open the project and start your agent as usual. No magic word: the hooks run on their own. Mostly you will not notice anything, until it stops a mistake.
6. **Turn things off.** `bossku install --no-harness` leaves out the command guard, the syntax check, the deny rules and the Node stop gate; the Python verify gate stays (set `BOSSKU_VERIFY_GATE=0` for that, as noted for `--no-harness`). `BOSSKU_STOP_GATE=off` switches off only the run-your-code check. `BOSSKU_RESUME=off` switches off the hooks that read Codex's session files. `bossku hooks uninstall` removes the hooks (also turn off the Bossku plugin if you enabled it in Claude Code). `bossku uninstall --purge` removes Bossku's user-level files and settings; project files and your notes stay.

More choices:

- **Where are my notes?** In `.bossku/memory` inside the project (learned skills too), unless you chose Obsidian storage in step 2.
- **Want all skills listed?** A first install starts at `--profile lean` (28 listed, the rest one command away). Use `--profile core` for a small set, `--profile engineering` for everything except marketing, or `--profile full` for all 258 listable skills. The other 416 stay in a library that `bossku skills find` searches.
- **Claude Code cutting skill descriptions?** On the full profile, `bossku doctor` warns you, and `bossku install --fit-skill-list` fixes it at a context cost ([details](docs/installation.md#skill-list-budget-claude-code)).
- **Other tools?** Setup for [Claude Code](docs/installation.md#claude-code), [Cursor](docs/installation.md#cursor), [Codex](docs/installation.md#codex), [OpenCode](docs/installation.md#opencode), [OMP](docs/installation.md#omp) or [portable mode](docs/installation.md#portable-mode-cloudshared-repos).

## What's inside

| Part | What it is |
|---|---|
| **670+ skills** | Short checklists for engineering, product, design, security, marketing and founder work: 258 listable, 416 in a searchable library |
| **Helper hooks** | Name fitting skills when a prompt clearly matches (Claude Code and Codex), and show a short brief of your saved notes at the start of a Claude Code session |
| **Safety gates** (Claude Code; the command guard also runs in Codex, Cursor and OpenCode) | Refuse destructive commands, ask before a push, merge, publish or deploy, check the syntax of files the agent writes, and send the agent back once if it edited code with no check after. [Details and switches](hooks/README.md). Leave most of them out with `bossku install --no-harness` |
| **Subagents** (Claude Code, Codex, OpenCode, Cursor, Devin) | Seven contracts (orchestrator, researcher, planner, designer, executor, auditor, final-reviewer), each with a model per role. Leave them out with `--no-agents` |
| **Resume** | When Codex stops on its usage limit, Claude Code loads the task's brief in the same folder after you say "continue". Only thread ids and times are kept, in `~/.bosskuai/resume-state.json` |
| **Tools** | Optional programs like Headroom, Moli, e2e, Cypress, Archify, Graft and MarkItDown. Installed only when you ask |
| **Memory** | Your rules, decisions and lessons, one folder per project, optionally in Obsidian |

## Your notes in Obsidian

![Where notes come from and where they go. Saved notes, Claude's own memory and your rules files are copied into one folder per project in your Obsidian vault by an automatic sync after every session; an index links everything, and the newest notes are shown at the start of the next session.](docs/assets/superpower-memory.svg)

The agent is told to save a note when a future session would need it: a decision, a plan, a fact or a lesson. It judges this itself, so a note can be missed. Common secret patterns are blanked out (a pattern list, not a guarantee). Notes are written by the agent, not copied from chat, but auto-learn can keep short quotes from your session as evidence in a learned skill; `BOSSKU_AUTO_LEARN=off` turns that off. After each session the notes sync to your vault. It only **copies**; your originals stay put. With Obsidian storage, if the vault is missing, Bossku tells you the note was not saved.

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
| `bossku tools install <tool>` | Show the plan for a tool. Add `--yes` to run it (pip, npm and agent-skill tools; manual tools are never run) |
| `bossku init <project>` | Set up a project (`--portable` puts the skills inside it) |
| `bossku hooks install` / `uninstall` | Add or remove the helper hooks |
| `bossku install --no-harness` | Leave out the safety gates. `--no-agents` leaves out the subagents, `--no-claude` the skills in `~/.claude/skills` |
| `bossku resume` | Show the brief of a Codex task that stopped on its usage limit |
| `bossku doctor --project .` | Check your setup |
| `bossku update` | Refresh installed skills (run after `git pull`) |

## For contributors

```bash
python -m bossku skills index --root .   # only if a skill or routing input changed (a SKILL.md, aliases.json, vendored.json, curated triggers)
python -m bossku validate --root .
python -m unittest discover -s tests -v
```

The website lives in [`web/`](web/). [`.github/workflows/pages.yml`](.github/workflows/pages.yml) publishes it to GitHub Pages once Pages is turned on for the repo.

## Learn more

- [Skills](skills/) and [shared instructions](AGENTS.md)
- [Benchmark results](docs/benchmarks/results.md), [the pack comparison](docs/benchmarks/results-2026-10-29-packs.md) and [how they were measured](docs/benchmarks/README.md)
- [Third-party packs and credits](docs/third-party.md), plus [optional requirements](requirements-optional.txt)
- [Claude Code practice review](docs/claude-practices-review.md) and [Archify practice review](docs/archify-practices-review.md)

## License

[MIT](LICENSE). Vendored skills keep their own licenses: see [third-party](docs/third-party.md).
