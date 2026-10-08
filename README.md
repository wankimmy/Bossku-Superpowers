# Bossku Superpower

**Skills and tools that make your AI coding agent do better work.** It helps your agent pick the right skill, run its own code before it says "done", and remember your project's rules from one session to the next. Free and open source ([MIT](LICENSE)).

Works with **Claude Code, Cursor, Codex, OpenCode, and OMP**. *(Formerly BosskuAI. The `bossku` command and the `bosskuai-*` skill names stay the same, so your installed skills, hooks and notes keep working; if you installed the plugin from a marketplace, reinstall it once.)*

![What Bossku Superpower adds around your agent. You ask; your agent picks a skill, does the work, runs it, and gives you a checked result. Behind it: 240+ skills found for you, optional tools, a check that sends the agent back if it never ran its code, and your notes saved in Obsidian.](docs/assets/superpower-overview.svg)

## What is it, in plain words?

Your coding agent is clever, but it forgets your rules and sometimes says "done" without checking. Bossku Superpower is a small layer around it that fixes four everyday problems:

| The problem | What Bossku Superpower does |
|---|---|
| The agent does not know which skill fits your request. | It names the best-fitting skill when the match is strong. There are 240+ skills; about 25 are listed, the rest are one command away, and `bossku skills find` shows a shortlist. |
| The agent writes code and never runs it. | If code changed and nothing ran afterwards, the agent is sent back once to run it. |
| You told the agent a rule yesterday and today it forgot. | Rules and decisions are saved as short notes and shown at the start of the next session, and they sync to your Obsidian vault. |
| Useful tools are scattered and hard to set up. | `bossku tools list` shows what is installed. Nothing installs unless you say yes. |

## How it works

1. **Install once** (two commands, below).
2. **Ask for what you want** in plain words. Bossku Superpower points your agent at the right skill, and the agent does the work.
3. **The agent checks its own work** and **saves what lasts**: your rules, decisions and lessons.

Everything is optional and light: skills load only when needed, tools install only on request, the run-your-code check has an off switch (`BOSSKU_VERIFY_GATE=0`), and `bossku hooks uninstall` removes every helper hook.

## Does it help? We measured it with real agents

We ran a real coding agent (Claude Code) on coding tasks with hidden tests, once **without Bossku Superpower** and once **with Bossku Superpower**, on the same tasks, at the same time. Some tasks have two sessions: the first states a project rule, the second asks for related work that breaks the rule unless it is remembered. Every number and chart below is rebuilt from result files saved in this repository, and a test fails if they ever disagree; the sentences around them are written by hand. How each check works, and what it cannot show, is in the [benchmark notes](docs/benchmarks/README.md).

![How each result was measured: a coding task and a fresh project go to an agent run beside an isolation check; a usage meter and hidden tests feed a comparison of the two setups, which feeds the charts.](docs/assets/benchmark-method.svg)

### In short

In plain words: Bossku Superpower helps a model that skips checking its own work. A model that already checks its work passes about as often with or without it, and uses more tokens. Whether notes help a project keep its rules from one session to the next is shown further down.

<!-- summary-overall:start -->
- **DeepSeek V4.1 Flash showed no clear difference on coding tasks:** 97% without, 97% with.
- **Nemotron 3 Nano 30B finished more coding tasks with Bossku Superpower:** 18% without, 40% with.
- **DeepSeek V4.1 Flash showed no clear difference on harder tasks:** 95% without, 93% with.
- **Gemma 4 31B showed no clear difference on harder tasks:** 57% without, 52% with.
- **DeepSeek V4.1 Flash showed no clear difference on tasks that need a rule from an earlier session:** 87% without, 100% with.
- **The extra checking costs tokens:** tokens per run with Bossku Superpower compared with without: DeepSeek V4.1 Flash 1.1× on coding tasks, Nemotron 3 Nano 30B 5.3× on coding tasks, DeepSeek V4.1 Flash 1.1× on harder tasks, Gemma 4 31B 1.6× on harder tasks, DeepSeek V4.1 Flash 1.2× on two-session tasks.
- **It finds the right skill more often:** 82% first-pick accuracy on new requests, against 56% for keyword search.
- **Its fixed cost is small:** extra tokens on the first call of a session: 1,241 on Claude Haiku 4.5, 2,155 on Claude Sonnet 5.5.
<!-- summary-overall:end -->

### What it adds to every session

![With and without Bossku Superpower: the input tokens and the cost of the first call of a Claude Code session](docs/assets/benchmark-session-overhead.svg)

<!-- summary-overhead:start -->
**What this shows:** Bossku Superpower adds a small, fixed amount to the first call of a session: Claude Haiku 4.5 +1,241 tokens (4% more), +$0.0011; Claude Sonnet 5.5 +2,155 tokens (6% more), +$0.0049. That is the skill list and the short instructions. The same text is reused on every later call, so it does not grow with the length of the session.
<!-- summary-overhead:end -->

### Finding the right skill

![With Bossku Superpower and with plain keyword search: how often the right skill is ranked first on requests it was never tuned on](docs/assets/benchmark-routing.svg)

<!-- summary-routing:start -->
**What this shows:** on 158 requests it was never tuned on, Bossku Superpower ranked an acceptable skill first 82% of the time, against 56% for plain keyword search. For requests with several jobs it found a fitting skill for every part 77% of the time. With a real agent (DeepSeek V4.1 Flash) on 73 of those requests, an acceptable skill was actually opened for 55% of them.
<!-- summary-routing:end -->

### Finishing tasks

![With and without Bossku Superpower: the share of hidden-test tasks and HumanEval problems passed, per model](docs/assets/benchmark-pass-rates.svg)

<!-- summary-pass:start -->
**Hidden-test coding tasks**
- **DeepSeek V4.1 Flash: no clear difference.** 97% with Bossku Superpower against 97% without (34 runs each): the same result on every one of the 17 tasks. Both setups were already near the ceiling, so there was little room to improve.
- **Nemotron 3 Nano 30B finished more tasks.** 40% with Bossku Superpower against 18% without (68 runs each): +22 points over the same tasks, 95% interval +12 to +34.

**Harder tasks**
- **DeepSeek V4.1 Flash: no clear difference.** 93% with Bossku Superpower against 95% without (42 runs each): -2 points over the same tasks, 95% interval -7 to 0. Both setups were already near the ceiling, so there was little room to improve.
- **Gemma 4 31B: no clear difference.** 52% with Bossku Superpower against 57% without (42 runs each): -5 points over the same tasks, 95% interval -14 to +7.
- 16 attempts (7 with Bossku Superpower, 9 without) were cut short by a usage limit on the model account. They count as neither passes nor failures; the run counts above are the completed runs.

**HumanEval problems**
- **DeepSeek V4.1 Flash: no clear difference.** 100% with Bossku Superpower against 100% without (40 runs each): the same result on every one of the 40 problems. Both setups were already near the ceiling, so there was little room to improve.
- **Nemotron 3 Nano 30B finished more problems.** 82% with Bossku Superpower against 62% without (40 runs each): +20 points over the same problems, 95% interval +2 to +38.
- 15 attempts (9 with Bossku Superpower, 6 without) were cut short by a usage limit on the model account. They count as neither passes nor failures; the run counts above are the completed runs.
<!-- summary-pass:end -->

### Running the code

![With and without Bossku Superpower: the share of runs that changed code and then ended without running anything](docs/assets/benchmark-checking.svg)

<!-- summary-checking:start -->
**What this shows:** the habit that Bossku Superpower's stop check is built to change. A model that never runs what it wrote cannot find its own mistakes.
- **DeepSeek V4.1 Flash** ended without running its code in 3% of the runs that changed code on its own, and in 0% with Bossku Superpower.
- **Nemotron 3 Nano 30B** ended without running its code in 100% of the runs that changed code on its own, and in 33% with Bossku Superpower.
<!-- summary-checking:end -->

### Remembering a rule from an earlier session

![With and without Bossku Superpower: the share of two-session tasks passed, where the second session breaks a project rule unless it is remembered](docs/assets/benchmark-memory.svg)

<!-- summary-memory:start -->
**What this shows:** each task states a project rule in a first session (for example "this must run on Python 3.8" or "never use eval") and asks for related work in a second one that would break the rule if forgotten. The agent starts the second session fresh: without Bossku Superpower it has only the files; with Bossku Superpower it also sees the notes it saved.
- **DeepSeek V4.1 Flash: no clear difference.** 100% with Bossku Superpower against 87% without (30 runs each): +13 points over the same tasks, 95% interval 0 to +33. In the first session, the agent with Bossku Superpower saved the rule as a note 100% of the time.
- 11 attempts (5 with Bossku Superpower, 6 without) were cut short by a usage limit on the model account. They count as neither passes nor failures; the run counts above are the completed runs.
<!-- summary-memory:end -->

### What it costs in tokens

![With and without Bossku Superpower: tokens per run and per solved task](docs/assets/benchmark-effort.svg)

<!-- summary-effort:start -->
**What this shows:** Bossku Superpower makes the agent do more work, and work costs tokens. The extra work is running, checking and fixing. Where that turns failures into passes it is worth it; where the model already passes, it is not.
- **DeepSeek V4.1 Flash, coding tasks:** 1.1× the tokens per run (107k without, 113k with) and 1.1× the tokens per task it actually solved. It ran shell commands 3.0 times per run instead of 2.4.
- **Nemotron 3 Nano 30B, coding tasks:** 5.3× the tokens per run (52k without, 276k with) and 2.4× the tokens per task it actually solved. It ran shell commands 3.6 times per run instead of 0.1.
- **DeepSeek V4.1 Flash, harder tasks:** 1.1× the tokens per run (294k without, 329k with) and 1.1× the tokens per task it actually solved. It ran shell commands 5.3 times per run instead of 5.3.
- **Gemma 4 31B, harder tasks:** 1.6× the tokens per run (195k without, 313k with) and 1.7× the tokens per task it actually solved. It ran shell commands 6.2 times per run instead of 3.0.
- **DeepSeek V4.1 Flash, two-session tasks:** 1.2× the tokens per run (97k without, 115k with) and about the same tokens per task it actually solved. It ran shell commands 1.9 times per run instead of 1.6.
<!-- summary-effort:end -->

### All the numbers

<!-- results:start -->
| First call of a session | Without Bossku Superpower | With Bossku Superpower |
|---|---:|---:|
| Claude Haiku 4.5: input tokens | 33,413 | 34,654 |
| Claude Haiku 4.5: cost | $0.0109 | $0.0120 |
| Claude Sonnet 5.5: input tokens | 35,403 | 37,558 |
| Claude Sonnet 5.5: cost | $0.0247 | $0.0297 |

| Finding a skill (158 new requests) | Keyword search only | With Bossku Superpower |
|---|---:|---:|
| Right skill ranked first | 56% | 82% |
| Right skill in the top three | 73% | 95% |
| Every part of a multi-part request covered | - | 77% |
| A real agent (DeepSeek V4.1 Flash) opens an acceptable skill | - | 55% |

| Hidden-test coding tasks | Without Bossku Superpower | With Bossku Superpower |
|---|---:|---:|
| DeepSeek V4.1 Flash: tasks passed (34 runs each) | 97% (33/34) | 97% (33/34) |
| DeepSeek V4.1 Flash: tokens per run | 107k | 113k |
| DeepSeek V4.1 Flash: ended without running its code | 3% | 0% |
| Nemotron 3 Nano 30B: tasks passed (68 runs each) | 18% (12/68) | 40% (27/68) |
| Nemotron 3 Nano 30B: tokens per run | 52k | 276k |
| Nemotron 3 Nano 30B: ended without running its code | 100% | 33% |

| Harder tasks | Without Bossku Superpower | With Bossku Superpower |
|---|---:|---:|
| DeepSeek V4.1 Flash: tasks passed (42 runs each) | 95% (40/42) | 93% (39/42) |
| DeepSeek V4.1 Flash: tokens per run | 294k | 329k |
| Gemma 4 31B: tasks passed (42 runs each) | 57% (24/42) | 52% (22/42) |
| Gemma 4 31B: tokens per run | 195k | 313k |

| HumanEval problems | Without Bossku Superpower | With Bossku Superpower |
|---|---:|---:|
| DeepSeek V4.1 Flash: tasks passed (40 runs each) | 100% (40/40) | 100% (40/40) |
| DeepSeek V4.1 Flash: tokens per run | 63k | 90k |
| Nemotron 3 Nano 30B: tasks passed (40 runs each) | 62% (25/40) | 82% (33/40) |
| Nemotron 3 Nano 30B: tokens per run | 89k | 219k |

| Remembering a rule from an earlier session | Without Bossku Superpower | With Bossku Superpower |
|---|---:|---:|
| DeepSeek V4.1 Flash: tasks passed (30 runs each) | 87% (26/30) | 100% (30/30) |
| DeepSeek V4.1 Flash: tokens per run | 97k | 115k |
<!-- results:end -->

### What these results do not show

- **Python projects of a few dozen to a few hundred lines.** Nothing here covers large repositories, other languages, or open-ended design work.
- **Three open models, not Claude.** Through Ollama Cloud, driven by Claude Code: a small model (Nemotron 3 Nano 30B) and a strong one (DeepSeek V4.1 Flash) on the coding tasks and HumanEval, a mid-size one (Gemma 4 31B) and the strong one on the harder tasks, and the strong one alone on the two-session tasks. Claude models were measured only for the cost of a session's first call, so no dollar cost per coding task is reported; tokens are the unit.
- **One build was measured.** The agent runs used commit `02ee2f2` (1 October 2026). Since then the router learned how people phrase requests (measured offline on the 158 requests above, not with an agent) and the rule reminder was added (measured on 200 labelled messages, not in an agent run). The live-agent skill-use figure also comes from the older router. None of these later changes has an end-to-end agent run yet.
- **Tasks written by assistants.** The harder and two-session tasks were written by AI assistants told not to read Bossku Superpower. Each was checked against a reference solution, and a few over-strict checks were fixed for both setups after a trial run. The [benchmark notes](docs/benchmarks/README.md) list what changed.
- **Small samples.** Overlapping intervals mean "no clear difference", not "equal".
- **AI judgment.** The 328 skill-search requests and the skills accepted for them were written by AI agents that saw only the skill catalog, never the router (160 first, 168 later), so they are not ground truth.
- **Claude Code only.** The helper hooks exist for Claude Code. Cursor, Codex, OpenCode, and OMP get the skills and instructions but were not benchmarked.

## What is inside

| Part | What it is |
|---|---|
| **240+ skills** | Short checklists for engineering, product, design, security, marketing and founder work. About 25 are always listed; the rest are found for you or opened with `bossku skills show <id>`. |
| **Helpers** (Claude Code) | Three small hooks: names skills for your prompt when the match is strong, sends the agent back to run its code, and shows your saved notes when a session starts. `BOSSKU_VERIFY_GATE=0` turns the second one off; `bossku hooks uninstall` removes all three. |
| **Tools** | `bossku tools list` shows optional programs the skills can use, such as Headroom (shrinks bulky tool output), Moli (fetches web pages without Chrome), e2e (AI-driven end-to-end tests), Archify (interactive diagrams), Graft, MarkItDown, and more. They install only when you ask. |
| **Memory** | Notes, learnings and rules saved in your Obsidian vault, one folder per project, with an index. |

```bash
bossku tools list                    # what is installed and what is not
bossku tools install headroom        # shows the exact commands; add --yes to run them
```

Moli, Hindsight and dcg are installed by hand: Moli and dcg ship installers that are scripts piped into a shell, and Hindsight has none here, so Bossku Superpower never runs them for you; it shows where to get them.

## Your notes live in Obsidian

![Where notes come from and where they go. Saved notes, Claude's own memory and your rules files are copied into one folder per project in your Obsidian vault by an automatic sync after every session; an index links everything, and the newest notes are shown at the start of the next session.](docs/assets/superpower-memory.svg)

The agent saves a note when it learns something a future session needs: a decision and why, a plan, a fact, a lesson. Small fixes usually save nothing. Obvious secrets are blanked out before anything is written, and the agent is told never to save secrets, prompts or transcripts.

```bash
bossku remember --project . --kind decision "Use the existing test runner for this project."
bossku memory-brief --project .       # the newest notes
bossku vault sync --project .         # copy Claude's auto-memory and your rules files into the vault now
bossku vault tidy                     # show what a clean-up of old clutter would do (nothing changes)
bossku vault tidy --apply             # do it: a zip backup first, nothing deleted, empty folders removed
```

In Obsidian mode (`--memory-storage obsidian`) the sync runs by itself at the end of each session, through the same hooks that already check your vault. It **copies**: your originals stay where they are. If the vault is missing, Bossku Superpower tells you the note was not saved; it does not quietly write into your repository. More in [memory and Obsidian](docs/memory.md).

## Install and start

Needs **Python 3.11+** and **Git**.

```bash
git clone https://github.com/wankimmy/bossku-superpower
cd bossku-superpower
pip install -e .
bossku install --vault "/path/to/your/Obsidian/Vault" --memory-storage obsidian
cd /path/to/your/project
bossku init .
bossku doctor --project .
```

Open that project in your coding agent and say `bossku`.

- **No Obsidian?** Leave out `--vault` and `--memory-storage`. Notes then stay in `.bossku/memory` inside the project.
- **Want every skill listed?** The default is `--profile lean` (about 25 listed, the rest one command away). `--profile core` is a small set, and `--profile full` lists all 240+. See [installation](docs/installation.md#user-level-skills-once-per-machine).
- **Helper hooks.** Installing also adds small hooks for Claude Code. Turn off the run-your-code check with `BOSSKU_VERIFY_GATE=0`. Remove every hook with `bossku hooks uninstall`. Codex asks you to approve hooks once.
- **Another tool?** Follow the [Claude Code](docs/installation.md#claude-code), [Cursor](docs/installation.md#cursor), or [Codex](docs/installation.md#codex) steps. [OpenCode](docs/installation.md#opencode) and [OMP](docs/installation.md#omp) use skills and project files. For shared or cloud workspaces, see [portable mode](docs/installation.md#portable-mode-cloudshared-repos).

## See why a skill was chosen

```bash
bossku skills find "Review this code for security problems"
```

The answer names the main skill and any extra skills, says when a match is weak, and shows what was left out and why. Some skills can only be started by you (for example `/prototype`); Bossku Superpower says so instead of loading them.

## Update

```bash
git pull
bossku update
bossku doctor
```

`bossku update` refreshes the installed skills and keeps your profile and your other skills.

## Check the repository

```bash
python -m bossku validate --root .
python -m unittest discover -s tests -v
```

After you change a skill description, rebuild the index first: `python -m bossku skills index --root .`

## More commands

| Command | What it does |
|---|---|
| `bossku init <project>` | Add project instructions and set up notes |
| `bossku init <project> --portable` | Put the skills inside the project |
| `bossku skills show <id>` | Print one skill (works for skills not in the agent's list) |
| `bossku skills audit` | Check skill size, descriptions, and links |
| `bossku tools list` | See optional tools and whether they are installed |
| `bossku vault sync` / `tidy` | Mirror memory and rules into Obsidian, or tidy old clutter |
| `bossku hooks install` / `uninstall` | Add or remove the helper hooks |
| `bossku doctor --project .` | Check installed skills and project files |

## Explore the library

- [Skills](skills/) cover engineering, product, design, security, marketing, and founder work.
- [Shared instructions](AGENTS.md) keep the workflow the same across coding tools.
- [Benchmarks](docs/benchmarks/README.md) explain how every number above was measured and how to repeat it.
- [Third-party packs and credits](docs/third-party.md) list the vendored sources and the tools that inspired this one (moli, e2e, headroom, archify, hindsight and more), with their licenses. [Optional requirements](requirements-optional.txt) cover separate tools.
- [Claude Code practice review](docs/claude-practices-review.md) and [Archify practice review](docs/archify-practices-review.md) explain how their advice was applied.

## License

[MIT](LICENSE). Vendored skills keep their own licenses: see [third-party](docs/third-party.md).
