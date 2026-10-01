# Benchmarks

Everything in the main README comes from the checks below. The raw rows are in [`benchmarks/results/raw/`](../../benchmarks/results/raw/), one summary per check is in [`benchmarks/results/`](../../benchmarks/results/), and [`scripts/make_charts.py`](../../scripts/make_charts.py) draws every chart and README table from them, so no number is typed by hand. [`tests/test_results_consistent.py`](../../tests/test_results_consistent.py) recomputes each summary from the raw rows and fails if a summary, a chart, or the README table has drifted from them.

| Check | What it answers | Needs a model? | Saved result |
|---|---|---|---|
| Session overhead | What does BosskuAI add to the first call of every session? | Yes (2 Claude models, a few cents) | `overhead.json` |
| Skill search on new prompts | Does the router find the right skill for requests it was never tuned on? | No | `routing-heldout.json` |
| Live skill use | Does a real agent open a fitting skill? | Yes (Ollama Cloud) | `routing-live.json` |
| Coding tasks | Does the agent finish more tasks, and at what token cost? | Yes (Ollama Cloud) | `coding-test.json` |
| HumanEval | Does anything get worse on a well-known public test? | Yes (Ollama Cloud) | `humaneval.json` |
| Tuned routing regression | Did a router change break the 82 prompts it was tuned on? | No | [`routing.json`](routing.json) |

## What was run

- **Setups.** *Without BosskuAI* has no skills, no hooks, and no instructions. *With BosskuAI* is this release (commit `b167823`, the `lean` profile with the skill hint, verify gate, and project-notes hooks). The previous release (commit `8adea49`, the `full` profile with 234 skills listed, no helper hooks) was run next to them in every test as an internal regression check. Its rows are kept in `benchmarks/results/raw/` but it is not part of the published comparison.
- **Agent.** Claude Code 2.1.284 in headless mode. Claude models use your own login; the other models are reached through Ollama Cloud's Anthropic-compatible API.
- **Models.** Session overhead: Claude Haiku 4.5 and Claude Sonnet 5.5. Coding and live skill use: Nemotron 3 Nano 30B (a small model that often forgets to run its code) and DeepSeek V4.1 Flash (a strong one that already does). HumanEval: the same two.
- **Samples.** 17 test tasks, each run 4 times per setup for Nemotron and 2 times per setup for DeepSeek. 40 HumanEval problems, one run per setup. 73 held-out skill-search requests for the live check.
- **Date.** 1 October 2026.

## How a coding run works

1. A task is a small Python project plus tests the agent never sees. 26 tasks were written for this repository (bug fixes, features, refactors, security, data and CLI work, performance, concurrency, test-writing graded by mutation). Each was validated: its hidden tests fail on the starting files and pass on a reference solution (`benchmark_agent.py validate`). HumanEval adds 164 public problems, sampled with a fixed seed.
2. The tasks are split before any comparison. Nine **dev** tasks were used while the changes were built; 17 **test** tasks were run once the changes were frozen and are what the README reports. The split is recorded in [`benchmarks/tasks/split.json`](../../benchmarks/tasks/split.json).
3. Every run gets a fresh git repository and a throwaway home folder.
4. The setups run on identical tasks, shuffled so no setup always runs first.
5. When the agent stops, the hidden tests are copied in and run. Pass means every test passes. Tokens, turns, and time come from Claude Code's own result report.

## Rules that keep it honest

- **The baseline is checked, not assumed.** Claude Code reads `~/.claude/CLAUDE.md` through the operating system account, whatever home folder a child process is given. In an early run that file carried BosskuAI's own memory block into the "without BosskuAI" arm, and those agents ran `bossku`. Every run now switches all `CLAUDE.md` files off, hands BosskuAI its instructions as a separate file, and starts with a canary: the baseline agent is asked to quote any instruction it was given and must answer `NONE`, or the run stops. Results from before that fix were thrown away.
- **Nothing touches your real setup.** Each run uses a throwaway home, so `bossku remember` inside a benchmark cannot write to your notes. The harness also watches the real vault and stops if a benchmark folder appears. (An early pilot did leave one note there before this guard existed.)
- **Failures are not dropped.** A run that hits a rate limit or an API error is retried and, if it still has no answer, excluded and counted in the report. A run that times out counts as a failure.
- **No made-up dollar cap.** Claude Code prices models it does not know with a rate it invents. A $1 cap on an early Ollama run therefore ended 8 of 17 runs part-way, and the version that used more tokens lost the most runs. Those results were thrown away. Runs on Ollama models now have no cap, the report prints a warning if any run was ended by one, and a test fails if a saved result contains one. Claude models keep a $1 cap per run to protect your account.
- **Dev and test are separate.** Router thresholds, the hint wording, the memory wording, the gate rules, and the lean list were chosen on dev data only. The test split of the 160 held-out prompts and the 17 test tasks were not used for any choice. The code was committed before the test runs started, and the commit is named above.
- **Held-out prompts are blind.** The 160 skill-search prompts and their acceptable skills were written by an author who saw only the skill catalog (names and descriptions), never the router code or its tests. They are split in two by a hash of the prompt id.

## Numbers

- **Pass rate** is runs where every hidden test passed. The interval is a 95% Wilson interval.
- **Paired differences** compare the same task and model across setups, with a bootstrap interval over tasks.
- **Tokens** are every input token the model processed across all turns (cached or not) plus output tokens. Ollama Cloud bills by subscription, so tokens are reported instead of dollars; Claude Code's own cost figure is used where the model is a Claude model.
- **Session overhead** is the first call of a session with a one-word prompt, taken after a cache warm-up, median of three.
- **Ended without running its code** counts runs that changed a code file and then never ran anything afterwards. It is read from the tool calls alone, the same way for both setups, so it does not depend on BosskuAI's own hook.

## Check the saved numbers (no model needed)

```bash
python -m unittest tests.test_results_consistent -v                      # summaries, charts and README table match the raw rows
python scripts/benchmark_agent.py report benchmarks/results/raw/coding-*.jsonl           # the coding table, from the raw rows
python scripts/benchmark_agent.py routing-report benchmarks/results/raw/routing.jsonl     # live skill use
python scripts/benchmark_agent.py overhead-report benchmarks/results/raw/overhead.jsonl   # session overhead
python scripts/benchmark_routing_heldout.py --arm before=/path/to/old/checkout --arm after=.   # skill search on new prompts
python scripts/benchmark_agent.py validate --suite benchmarks/tasks/test                  # tasks are fair
python scripts/make_charts.py --readme README.md                                          # redraw charts and the README table
```

## Repeat the runs (spends model usage)

`before` is a checkout of the commit before this release (`git archive 8adea49 | tar -x -C /path/to/old/checkout`). Claude runs use your own login; Ollama runs use your own key, read from a file and never printed or saved.

```bash
python scripts/benchmark_agent.py overhead --arm baseline --arm before=/path/to/old/checkout@full \
    --arm after=.@lean+hint+gate+brief --model claude-sonnet-5-5 --trials 3 --out /tmp/overhead
python scripts/benchmark_agent.py run --provider ollama --ollama-key-file KEYFILE \
    --suite benchmarks/tasks/test --arm baseline --arm before=/path/to/old/checkout@full \
    --arm after=.@lean+hint+gate+brief --model nemotron-3-nano:30b --trials 4 --parallel 6 --out /tmp/coding
python scripts/benchmark_agent.py run --provider ollama --ollama-key-file KEYFILE --suite humaneval:40 \
    --arm baseline --arm before=/path/to/old/checkout@full --arm after=.@lean+hint+gate+brief \
    --model deepseek-v4.1-flash --out /tmp/humaneval
python scripts/benchmark_agent.py routing --provider ollama --ollama-key-file KEYFILE --split test \
    --arm before=/path/to/old/checkout@full --arm after=.@lean+hint+gate+brief --model deepseek-v4.1-flash --out /tmp/routing
python scripts/benchmark_agent.py compact /tmp/coding/runs.jsonl --kind task --kind selftest --out benchmarks/results/raw/coding-MODEL.jsonl
```

An interrupted run resumes where it stopped when you start it again with the same `--out` folder.

## Limits

- The tasks are small, spec-driven Python projects with hidden tests. They say nothing about large repositories, other languages, or open-ended design work.
- Strong agentic models already run their own tests. On those, BosskuAI cannot raise a pass rate that is already near the ceiling; the question there is whether it costs more.
- Two Ollama Cloud models were run on the coding tasks (one small, one strong). Claude models were measured for session overhead only, to avoid spending Claude usage; their coding behavior was not measured here.
- Samples are small. Read overlapping intervals as "no clear difference", not as proof of equality.
- Skills built for a specific stack (Laravel, Nuxt, Docker, marketing, legal) are not exercised by generic coding tasks. Their value is not measured here.
- The held-out skill-search prompts and their acceptable skills are one author's judgment, not ground truth.
- The agent in these runs is Claude Code. The helper hooks only exist for Claude Code, so Cursor, Codex, OpenCode, and OMP got the skills and instructions but not the hooks, and were not benchmarked.

## Tuned routing regression (82 prompts)

The older offline check compares BosskuAI's lexical routing with an ID/description-only keyword baseline on the 82 prompts the router was tuned against. It makes no model calls and needs only Python's standard library. Treat it as a regression test, not as evidence of accuracy on new prompts; the held-out check above is for that.

The [machine-readable snapshot](routing.json) holds every prompt, defensible answer set, predicted ID, ranked score, and pass/fail outcome.

| Method | Top-one hits | Top-three hits |
|---|---|---|
| BosskuAI `find_skill` / `rank_skills` | 82/82 (100%) | 82/82 (100%) |
| ID/description-only keyword baseline | 46/82 (56.10%) | 61/82 (74.39%) |

The automatic selector (`select_skill_stack`) is scored separately under `results.automatic_selection`: 79/79 model-invoked primaries and 3/3 user-only commands correctly deferred.

```console
python scripts/benchmark_routing.py          # regenerate docs/benchmarks/routing.json
python scripts/benchmark_routing.py --check  # compare current inputs and results with the snapshot
python -m unittest discover -s tests -p test_routing_benchmark.py -v
```

The corpus comes from the literal `ROUTING_CASES` and `REVIEW_ROUTING_CASES` assignments in [tests/test_routing.py](../../tests/test_routing.py), read with AST literal evaluation without running the test module. Identical prompts merge into one case with the union of their defensible IDs. The baseline removes the `bosskuai-` prefix from each skill ID, tokenizes the ID and description with the same normalization as the router, and scores each skill by its IDF-weighted share of the query terms; it uses no curated triggers, exclusions, aliases, or body headings. Numeric scores from the two methods use different scales and are not confidence probabilities. A ranking hit does not authorize automatic loading of a user-only skill.
