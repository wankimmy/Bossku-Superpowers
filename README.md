# BosskuAI

Skills for your coding agent, plus three habits that make its work better: find the right skill, run the code it writes, and remember your project.

Works with **Claude Code, Cursor, Codex, OpenCode, and OMP**. Free and open source ([MIT](LICENSE)).

![From your prompt to a checked result. Your agent reads context, chooses skills, does the work, runs and reviews it, and delivers. BosskuAI adds three helpers: it shows saved notes, names skills for your prompt, and sends the agent back if it never ran its code.](docs/assets/bosskuai-flow.svg)

## What you get

- **The right skill, found for you.** Say what you want in plain words. BosskuAI points your agent to the best skill, and adds a second one only when your request has two separate jobs.
- **Code that gets run.** If your agent changes code and never runs it, or pastes code into the chat instead of writing the file, it is sent back once. (Claude Code.)
- **A project that remembers.** Decisions and lessons are saved as short notes, in Obsidian if you use it. The newest ones appear when the next session starts.
- **Light on your agent's memory.** About 25 skills are listed each session. About 210 more are one command away.

For example:

```text
bossku, review this code for security problems.
```

## Does it help? We measured it with real agents

We ran a real coding agent (Claude Code) on small coding tasks with hidden tests, once **without BosskuAI** and once **with BosskuAI**, on the same tasks. Every number, chart, and explanation below is rebuilt from result files saved in this repository, and a test fails if they ever disagree. How each check works, and what it cannot show, is in the [benchmark notes](docs/benchmarks/README.md).

![How each result was measured: a coding task and a fresh project go to an agent run beside an isolation check; a usage meter and hidden tests feed a comparison of the two setups, which feeds the charts.](docs/assets/benchmark-method.svg)

### In short

<!-- summary-overall:start -->
- **DeepSeek V4.1 Flash gained nothing it could measure:** 91% without, 94% with.
- **Nemotron 3 Nano 30B finished more tasks with BosskuAI:** 22% without, 38% with.
- **It finds the right skill more often:** 75% first-pick accuracy on new requests, against 60% for keyword search.
- **Its fixed cost is small:** extra tokens on the first call of a session: 1,333 on Claude Haiku 4.5, 2,914 on Claude Sonnet 5.5.
<!-- summary-overall:end -->

### What it adds to every session

![With and without BosskuAI: the input tokens and the cost of the first call of a Claude Code session](docs/assets/benchmark-session-overhead.svg)

<!-- summary-overhead:start -->
**What this shows:** BosskuAI adds a small, fixed amount to the first call of a session: Claude Haiku 4.5 +1,333 tokens (4% more), +$0.0012; Claude Sonnet 5.5 +2,914 tokens (9% more), +$0.0078. That is the skill list and the short instructions. The same text is reused on every later call, so it does not grow with the length of the session.
<!-- summary-overhead:end -->

### Finding the right skill

![With BosskuAI and with plain keyword search: how often the right skill is ranked first on requests it was never tuned on](docs/assets/benchmark-routing.svg)

<!-- summary-routing:start -->
**What this shows:** on 73 requests it was never tuned on, BosskuAI ranked an acceptable skill first 75% of the time, against 60% for plain keyword search. For requests with several jobs it found a fitting skill for every part 58% of the time. With a real agent (DeepSeek V4.1 Flash) on the same requests, an acceptable skill was actually opened for 49% of them.
<!-- summary-routing:end -->

### Finishing tasks

![With and without BosskuAI: the share of hidden-test tasks and HumanEval problems passed, per model](docs/assets/benchmark-pass-rates.svg)

<!-- summary-pass:start -->
**Hidden-test coding tasks**
- **DeepSeek V4.1 Flash: no clear difference.** 94% with BosskuAI against 91% without (34 runs each): +3 points over the same tasks, 95% interval 0 to +9. Both setups were already near the ceiling, so there was little room to improve.
- **Nemotron 3 Nano 30B finished more tasks.** 38% with BosskuAI against 22% without (68 runs each): +16 points over the same tasks, 95% interval +6 to +26. 6 of the 68 runs with BosskuAI (0 without) ran out of time and count as failures.

**HumanEval problems**
- **DeepSeek V4.1 Flash: no clear difference.** 100% with BosskuAI against 98% without (40 runs each): +2 points over the same problems, 95% interval 0 to +8. Both setups were already near the ceiling, so there was little room to improve. 0 of the 40 runs with BosskuAI (1 without) ran out of time and count as failures.
- **Nemotron 3 Nano 30B: no clear difference.** 78% with BosskuAI against 80% without (40 runs each): -2 points over the same problems, 95% interval -20 to +15.
<!-- summary-pass:end -->

### Running the code

![With and without BosskuAI: the share of runs that changed code and then ended without running anything](docs/assets/benchmark-checking.svg)

<!-- summary-checking:start -->
**What this shows:** the habit that BosskuAI's stop check is built to change. A model that never runs what it wrote cannot find its own mistakes.
- **DeepSeek V4.1 Flash** ended without running its code in 0% of the runs that changed code on its own, and in 3% with BosskuAI.
- **Nemotron 3 Nano 30B** ended without running its code in 100% of the runs that changed code on its own, and in 48% with BosskuAI.
<!-- summary-checking:end -->

### What it costs in tokens

![With and without BosskuAI: tokens per run and per solved task](docs/assets/benchmark-effort.svg)

<!-- summary-effort:start -->
**What this shows:** BosskuAI makes the agent do more work, and work costs tokens. The extra work is running, checking and fixing. Where that turns failures into passes it is worth it; where the model already passes, it is not.
- **DeepSeek V4.1 Flash** used 1.6× the tokens per run (106k without, 171k with) and 1.6× the tokens per task it actually solved.
- **Nemotron 3 Nano 30B** used 3.9× the tokens per run (57k without, 221k with) and 2.2× the tokens per task it actually solved.
<!-- summary-effort:end -->

### All the numbers

<!-- results:start -->
| First call of a session | Without BosskuAI | With BosskuAI |
|---|---:|---:|
| Claude Haiku 4.5: input tokens | 32,280 | 33,613 |
| Claude Haiku 4.5: cost | $0.0108 | $0.0120 |
| Claude Sonnet 5.5: input tokens | 33,856 | 36,770 |
| Claude Sonnet 5.5: cost | $0.0245 | $0.0323 |

| Finding a skill (73 new requests) | Keyword search only | With BosskuAI |
|---|---:|---:|
| Right skill ranked first | 60% | 75% |
| Right skill in the top three | 77% | 92% |
| Every part of a multi-part request covered | - | 58% |
| A real agent (DeepSeek V4.1 Flash) opens an acceptable skill | - | 49% |

| Hidden-test coding tasks | Without BosskuAI | With BosskuAI |
|---|---:|---:|
| DeepSeek V4.1 Flash: tasks passed (34 runs each) | 91% (31/34) | 94% (32/34) |
| DeepSeek V4.1 Flash: tokens per run | 106k | 171k |
| DeepSeek V4.1 Flash: ended without running its code | 0% | 3% |
| Nemotron 3 Nano 30B: tasks passed (68 runs each) | 22% (15/68) | 38% (26/68) |
| Nemotron 3 Nano 30B: tokens per run | 57k | 221k |
| Nemotron 3 Nano 30B: ended without running its code | 100% | 48% |

| HumanEval problems | Without BosskuAI | With BosskuAI |
|---|---:|---:|
| DeepSeek V4.1 Flash: tasks passed (40 runs each) | 98% (39/40) | 100% (40/40) |
| DeepSeek V4.1 Flash: tokens per run | 74k | 86k |
| Nemotron 3 Nano 30B: tasks passed (40 runs each) | 80% (32/40) | 78% (31/40) |
| Nemotron 3 Nano 30B: tokens per run | 85k | 208k |
<!-- results:end -->

### What these results do not show

- **Small Python tasks only.** Nothing here covers large repositories, other languages, or open-ended design work.
- **Two open models, not Claude.** The coding runs used one small and one strong open model through Ollama Cloud, driven by Claude Code. Claude models were measured only for the cost of a session's first call, so no dollar cost per coding task is reported; tokens are the unit.
- **Small samples.** Overlapping intervals mean "no clear difference", not "equal".
- **One author's judgment.** The skill-search requests and the skills accepted for them were written by one person who had not seen the router.
- **Claude Code only.** The helper hooks exist for Claude Code. Cursor, Codex, OpenCode, and OMP get the skills and instructions but were not benchmarked.

## Install and start

Needs **Python 3.11+** and **Git**.

```bash
git clone https://github.com/wankimmy/Bossku-AI bosskuAI
cd bosskuAI
pip install -e .
bossku install --vault "/path/to/your/Obsidian/Vault" --memory-storage obsidian
cd /path/to/your/project
bossku init .
bossku doctor --project .
```

Open that project in your coding agent and say `bossku`.

- **No Obsidian?** Leave out `--vault` and `--memory-storage`. Notes then stay in `.bossku/memory` inside the project.
- **Want every skill listed?** The default is `--profile lean` (about 25 listed, the rest one command away). `--profile core` is a small set, and `--profile full` lists all ~235. See [installation](docs/installation.md#user-level-skills-once-per-machine).
- **Helper hooks.** Installing also adds small hooks for Claude Code: one names skills for your prompt, one makes the agent run its code, and one shows saved notes at the start. Turn off the run-your-code check with `BOSSKU_VERIFY_GATE=0`. Remove every hook with `bossku hooks uninstall`. Codex asks you to approve hooks once.
- **Another tool?** Follow the [Claude Code](docs/installation.md#claude-code), [Cursor](docs/installation.md#cursor), or [Codex](docs/installation.md#codex) steps. [OpenCode](docs/installation.md#opencode) and [OMP](docs/installation.md#omp) use skills and project files. For shared or cloud workspaces, see [portable mode](docs/installation.md#portable-mode-cloudshared-repos).

## See why a skill was chosen

```bash
bossku skills find "Review this code for security problems"
```

The answer names the main skill and any extra skills, says when a match is weak, and shows what was left out and why. Some skills can only be started by you (for example `/prototype`); BosskuAI says so instead of loading them.

## Keep project notes in one place

The agent saves a note when it learns something a future session needs: a decision and why, a plan, a fact, a lesson. Small fixes usually save nothing. The agent is told never to save secrets, prompts, or transcripts, and obvious secrets are blanked out before anything is written.

```bash
bossku memory-brief --project .       # the newest notes
bossku remember --project . --kind decision "Use the existing test runner for this project."
```

With Obsidian, the vault is the one place notes live. If the vault is missing, BosskuAI tells you the note was not saved; it does not quietly write into your repository. See [memory and Obsidian](docs/memory.md).

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
| `bossku hooks install` / `uninstall` | Add or remove the helper hooks |
| `bossku doctor --project .` | Check installed skills and project files |

## Explore the library

- [Skills](skills/) cover engineering, product, design, security, marketing, and founder work.
- [Shared instructions](AGENTS.md) keep the workflow the same across coding tools.
- [Benchmarks](docs/benchmarks/README.md) explain how every number above was measured and how to repeat it.
- [Third-party packs and credits](docs/third-party.md) list the vendored sources. [Optional requirements](requirements-optional.txt) cover separate tools.
- [Claude Code practice review](docs/claude-practices-review.md) and [Archify practice review](docs/archify-practices-review.md) explain how their advice was applied.

## License

[MIT](LICENSE).
