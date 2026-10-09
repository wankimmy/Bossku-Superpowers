# Benchmarks

Everything in the [results page](results.md) and the main README summary comes from the checks below. The raw rows are in [`benchmarks/results/raw/`](../../benchmarks/results/raw/), one summary per check is in [`benchmarks/results/`](../../benchmarks/results/), and [`scripts/make_charts.py`](../../scripts/make_charts.py) draws every chart and results table from them, so no number is typed by hand. [`tests/test_results_consistent.py`](../../tests/test_results_consistent.py) recomputes each summary from the raw rows and fails if a summary, a chart, or the results page has drifted from them.

| Check | What it answers | Needs a model? | Saved result |
|---|---|---|---|
| Session overhead | What does Bossku Superpower add to the first call of every session? | Yes (2 Claude models, a few cents) | `overhead.json` |
| Skill search on new prompts | Does the router find the right skill for requests it was never tuned on? 328 requests written by agents that saw only the skill catalog; the router is tuned on one half (by id hash) and reported on the other (158) | No | `routing-heldout.json` |
| Live skill use | Does a real agent open a fitting skill? | Yes (Ollama Cloud) | `routing-live.json` |
| Coding tasks | Does the agent finish more tasks, and at what token cost? | Yes (Ollama Cloud) | `coding-test.json` |
| Harder tasks | The same on longer projects with many rules to follow | Yes (Ollama Cloud) | `hard.json` |
| Remembering a rule | Does a rule stated in one session survive into the next? | Yes (Ollama Cloud) | `memory.json` |
| HumanEval | Does anything get worse on a well-known public test? | Yes (Ollama Cloud) | `humaneval.json` |
| Tuned routing regression | Did a router change break the 84 prompts it was tuned on? | No | [`routing.json`](routing.json) |

## What was run

- **Setups.** *Without Bossku Superpower* has no skills, no hooks, and no instructions. *With Bossku Superpower* is commit `b8ccea1` (5 October 2026): the `lean` profile with the skill hint, run-your-code check, project-notes hooks and the stated-rule reminder. The session-cost rows come from the earlier build `02ee2f2`; the previous release (commit `8adea49`, the `full` profile with 234 skills listed and no helper hooks) was run for that check only, and its rows stay in `benchmarks/results/raw/overhead.jsonl` but are not part of the published comparison. Runs were shuffled so no setup always ran first.
- **Reused baselines.** The *without* setup does not depend on the build, so for seven sets of runs it was not run again: Nemotron and DeepSeek coding, DeepSeek and Gemma harder tasks, Nemotron and DeepSeek HumanEval, and DeepSeek on the ten original two-session tasks use the *without* runs of 1 to 2 October (committed unchanged in the same raw files). Everything else, including every Claude run, ran both setups in the same session of work. The cost is a confound: the reused runs are from other days and from Claude Code 2.1.284, the new ones from 2.1.293 (every row records its version), and the model service may have changed in between. That is why some lanes show more runs *without* than *with*, and why the [earlier run](#the-earlier-run) is reported too.
- **Agent.** Claude Code 2.1.284 (reused rows) and 2.1.293 (new rows), in headless mode. Claude models use your own login; the other models are reached through Ollama Cloud's Anthropic-compatible API.
- **Models.** Session overhead: Claude Haiku 4.5 and Claude Sonnet 5.5. Coding tasks, harder tasks and HumanEval: Nemotron 3 Nano 30B (a small model that often forgets to run its code), Gemma 4 31B (mid-size) and DeepSeek V4.1 Flash (a strong one that already does). Remembering a rule: those three plus Claude Haiku 4.5 and Claude Sonnet 5.5. Live skill use: DeepSeek V4.1 Flash. The coding, harder-task and HumanEval runs for the two Claude models were started but did not finish (the Claude login expired), so they are not published.
- **Samples.** 17 coding test tasks (Nemotron: 4 runs per task for the reused *without*, 2 for *with*; DeepSeek 2 each; Gemma 1 each). 14 harder test tasks (3 runs *without* and 2 *with* for DeepSeek and Gemma, 1 each for Nemotron). 22 two-session tasks (10 original, 12 added), 1 to 3 runs each. HumanEval: 40 problems once per setup for Nemotron and DeepSeek, the first 20 for Gemma. 60 held-out skill-search requests for the live check.
- **Dates.** 1 to 8 October 2026.

## How a coding run works

1. A task is a small Python project plus tests the agent never sees. 26 tasks were written for this repository (bug fixes, features, refactors, security, data and CLI work, performance, concurrency, test-writing graded by mutation). 31 harder tasks followed: projects of several hundred lines whose rules sit in a README and in the docstrings of the code around the new feature, so a model has to read before it writes. Every task was validated: its hidden tests fail on the starting files and pass on a reference solution (`benchmark_agent.py validate`). HumanEval adds 164 public problems, sampled with a fixed seed.
2. The harder tasks and the memory tasks were written by AI assistants that were told not to open Bossku Superpower's skills, code, or documentation, and that saw only one example task and the prompts of the others.
3. The tasks are split before any comparison. Nine **dev** coding tasks and 17 **dev** harder tasks were used while the changes were built; 17 coding **test** tasks and 14 harder **test** tasks were run once the changes were frozen and are what the README reports. The splits are recorded in [`benchmarks/tasks/split.json`](../../benchmarks/tasks/split.json) and [`benchmarks/tasks/hard-split.json`](../../benchmarks/tasks/hard-split.json).
4. Every run gets a fresh git repository and a throwaway home folder.
5. The setups run on identical tasks, shuffled so no setup always runs first.
6. When the agent stops, the hidden tests are copied in and run. Pass means every test passes. Tokens, turns, and time come from Claude Code's own result report.

### Remembering a rule from an earlier session

Twenty-two tasks have two sessions: ten original ones, and twelve more in `benchmarks/tasks/memory-rules/` of the same kind. The first session asks for a small change and states a project rule ("this must run on Python 3.8", "money is integer cents", "never use eval", "services go in `services/`, one class per file"). The second is a fresh conversation in the same project folder that asks for related work which would break the rule unless it is remembered; nothing in its prompt mentions the rule. Without Bossku Superpower the agent has only the files the first session left behind. With Bossku Superpower it also sees the notes the first session saved, which appear when the second session starts. The hidden tests check the work and the rule itself.

## Rules that keep it honest

- **The baseline is checked, not assumed.** Claude Code reads `~/.claude/CLAUDE.md` through the operating system account, whatever home folder a child process is given. In an early run that file carried Bossku Superpower's own memory block into the "without Bossku Superpower" arm, and those agents ran `bossku`. Every run now switches all `CLAUDE.md` files off, hands Bossku Superpower its instructions as a separate file, and starts with a canary: the baseline agent is asked to quote any instruction it was given and must answer `NONE`, or the run stops. Results from before that fix were thrown away.
- **Nothing touches your real setup.** Each run uses a throwaway home, so `bossku remember` inside a benchmark cannot write to your notes. The harness also watches the real vault and stops if a benchmark folder appears. (An early pilot did leave one note there before this guard existed.)
- **Failures are not dropped.** A run that ends with a rate limit or an API error is retried and, if it still cannot finish, excluded and counted in the report. A run that reaches the time limit is run once more with a longer limit, and a second timeout counts as a failure.
- **No made-up dollar cap.** Claude Code prices models it does not know with a rate it invents. A $1 cap on an early Ollama run therefore ended 8 of 17 runs part-way, and the version that used more tokens lost the most runs. Those results were thrown away. Runs on Ollama models now have no cap, the report prints a warning if any run was ended by one, and a test fails if a saved result contains one. Claude models keep a $1 cap per run to protect your account.
- **Dev and test are separate, with one caveat.** Router thresholds, the hint wording, the memory wording, the gate rules, the lean list, and the compact skills were chosen on dev data only. The 17 coding test tasks had already been run once on an earlier build of this release; the result (a strong model used far more tokens for no more passes) is why instructions were shortened and skills compacted, but no change was tuned to a test task. The 14 harder test tasks had never been run with Bossku Superpower before the build was frozen, so they are the cleanest evidence. The 10 memory tasks were run once before the freeze, which is how their over-strict checks were found; no instruction or hook was changed because of that run. The code was committed before the final runs started, and the commit is named above.
- **Unfair tests were fixed for both setups, not for one.** After a trial run, four checks in two memory tasks were relaxed because they marked correct work as wrong (one hidden test forbade `/` even in exact `Fraction` arithmetic; three expected an error from `value_of` and failed an agent that rejected the bad formula earlier, in `set_formula`). One harder task whose prompt did not state a requirement its tests checked was dropped. Every final run uses the corrected tests, for both setups.
- **Slow runs get one longer try.** The model service slowed down in the evening, and the runs that take more turns were the ones to reach the 25-minute limit. Four runs did (all with BosskuAI: three Nemotron, one DeepSeek). Each was run again with a 60-minute limit and the rerun is the one counted: one passed, three failed. That was in the earlier run; its first tries are kept in `raw/earlier/timeouts-first-attempt.jsonl`. In the later run no published run ended on the time limit.
- **A usage limit on the model account is not a coding failure.** Late in the final runs the Ollama Cloud account reached its usage limit and refused requests (HTTP 429). The harness first called a run an infrastructure failure only when the model had produced no output at all, so a limit that arrived part-way left a half-finished run that was graded as a failed task. That was a bug: any run that ends with an API error is now an infrastructure failure, excluded from every summary, listed in the report, and run again when the limit allows. Runs that could not be run again are counted under the chart text on the results page, because the long runs are the ones a limit is most likely to cut short.
- **An option was removed rather than shipped untested.** A requirement checklist and a second-pass audit were tried; on a strong model the checklist cost 55% more tokens for no extra passes, and no clean run showed a gain on a small model, so both were deleted.
- **Held-out prompts are blind.** The 328 skill-search prompts (160 written first, 168 later) and their acceptable skills were written by agents that saw only the skill catalog (names and descriptions), never the router code or its tests; a second agent then added any other skills it judged equally acceptable. They are split in two by a hash of the prompt id.

## The earlier run

An earlier run of the coding, harder-task, HumanEval and ten-task memory suites measured commit `02ee2f2` (1 to 2 October 2026), with both setups run at the same time. Its raw rows are kept in [`benchmarks/results/raw/earlier/`](../../benchmarks/results/raw/earlier/) (recompute with `python scripts/benchmark_agent.py report benchmarks/results/raw/earlier/coding-*.jsonl`, and the same for `hard-*`, `humaneval-*` and `memory-*`). Next to the later run on `b8ccea1`, with its reused *without* runs:

| Suite and model | Earlier run (`02ee2f2`), without / with | Later run (`b8ccea1`), without / with |
|---|---|---|
| Coding, Nemotron 3 Nano 30B | 18% (12/68) / 40% (27/68) | 18% (12/68) / 29% (10/34) |
| Coding, DeepSeek V4.1 Flash | 97% (33/34) / 97% (33/34) | 97% (33/34) / 94% (32/34) |
| Harder, DeepSeek V4.1 Flash | 95% (40/42) / 93% (39/42) | 95% (40/42) / 93% (26/28) |
| Harder, Gemma 4 31B | 57% (24/42) / 52% (22/42) | 57% (24/42) / 64% (18/28) |
| HumanEval, Nemotron 3 Nano 30B | 62% (25/40) / 82% (33/40) | 62% (25/40) / 92% (37/40) |
| HumanEval, DeepSeek V4.1 Flash | 100% (40/40) / 100% (40/40) | 100% (40/40) / 100% (40/40) |
| Ten original two-session tasks, DeepSeek V4.1 Flash | 87% (26/30) / 100% (30/30) | 87% (26/30) / 90% (27/30) |

The direction held for Nemotron on HumanEval and the other suites show no clear difference in either run. Nemotron's coding gain was smaller the second time (+22 points, interval +12 to +34, then +12 points, interval -3 to +28), and DeepSeek's memory gain disappeared (+13 points, then +3; on the twelve added two-session tasks it passed 22 of 36 with and 26 of 36 without). Differences of ten to twenty points between two runs of the same setup are within what these sample sizes produce; they are also what the changes between the two builds (a shorter reminder, the stated-rule reminder) could cause, and these runs cannot tell the two apart.

## Numbers

- **Pass rate** is runs where every hidden test passed. The interval is a 95% Wilson interval.
- **Paired differences** compare the same task and model across setups, with a bootstrap interval over tasks.
- **Tokens** are every input token the model processed across all turns (cached or not) plus output tokens. Ollama Cloud bills by subscription, so tokens are reported instead of dollars; Claude Code's own cost figure is used where the model is a Claude model.
- **Session overhead** is the first call of a session with a one-word prompt, taken after a cache warm-up, median of three.
- **Saved a note** (memory tasks) counts runs whose first session called `bossku remember`.
- **Ended without running its code** counts runs that changed a code file and then never ran anything afterwards. It is read from the tool calls alone, the same way for both setups, so it does not depend on Bossku Superpower's own hook.

## Check the saved numbers (no model needed)

```bash
python -m unittest tests.test_results_consistent -v                      # summaries, charts and results page match the raw rows
python scripts/benchmark_agent.py report benchmarks/results/raw/coding-*.jsonl           # the coding table, from the raw rows
python scripts/benchmark_agent.py report benchmarks/results/raw/hard-*.jsonl             # harder tasks
python scripts/benchmark_agent.py report benchmarks/results/raw/memory-*.jsonl           # remembering a rule
python scripts/benchmark_agent.py routing-report benchmarks/results/raw/routing.jsonl     # live skill use
python scripts/benchmark_agent.py overhead-report benchmarks/results/raw/overhead.jsonl   # session overhead
python scripts/benchmark_routing_heldout.py --arm after=.                                 # skill search on new prompts
python scripts/benchmark_agent.py validate --suite benchmarks/tasks/hard-test             # tasks are fair (also: test, memory, memory-rules)
python scripts/make_charts.py --readme docs/benchmarks/results.md                         # redraw charts and results page
```

## Repeat the runs (spends model usage)

Claude runs use your own login; Ollama runs use your own key, read from a file and never printed or saved. To compare with an older build, check it out in another folder and add `--arm old=/path/to/old/checkout@full`.

```bash
python scripts/benchmark_agent.py overhead --arm baseline --arm after=.@lean+hint+gate+brief \
    --model claude-sonnet-5-5 --trials 3 --out /tmp/overhead
python scripts/benchmark_agent.py run --provider ollama --ollama-key-file KEYFILE \
    --suite benchmarks/tasks/test --arm baseline --arm after=.@lean+hint+gate+brief \
    --model nemotron-3-nano:30b --trials 4 --parallel 6 --out /tmp/coding
python scripts/benchmark_agent.py run --provider ollama --ollama-key-file KEYFILE \
    --suite benchmarks/tasks/hard-test --arm baseline --arm after=.@lean+hint+gate+brief \
    --model gemma4:31b --trials 3 --parallel 6 --out /tmp/hard
python scripts/benchmark_agent.py run --provider ollama --ollama-key-file KEYFILE \
    --suite benchmarks/tasks/memory --arm baseline --arm after=.@lean+hint+gate+brief \
    --model deepseek-v4.1-flash --trials 3 --parallel 6 --out /tmp/memory
python scripts/benchmark_agent.py run --provider ollama --ollama-key-file KEYFILE \
    --suite benchmarks/tasks/memory-rules --arm baseline --arm after=.@lean+hint+gate+brief \
    --model deepseek-v4.1-flash --trials 3 --parallel 6 --out /tmp/memory-rules
python scripts/benchmark_agent.py run --provider ollama --ollama-key-file KEYFILE --suite humaneval:40 \
    --arm baseline --arm after=.@lean+hint+gate+brief --model deepseek-v4.1-flash --out /tmp/humaneval
python scripts/benchmark_agent.py routing --provider ollama --ollama-key-file KEYFILE --split test --limit 60 \
    --arm after=.@lean+hint+gate+brief --model deepseek-v4.1-flash --out /tmp/routing
python scripts/benchmark_agent.py compact /tmp/coding/runs.jsonl --kind task --kind selftest \
    --out benchmarks/results/raw/coding-MODEL.jsonl
```

An interrupted run resumes where it stopped when you start it again with the same `--out` folder. `compact` also replaces account and folder names in the free text with placeholders before anything is committed.

## Limits

- The tasks are Python projects with hidden tests, from a few dozen lines to a few hundred. They say nothing about large repositories, other languages, or open-ended design work.
- Strong agentic models already run their own tests. On those, Bossku Superpower cannot raise a pass rate that is already near the ceiling; the question there is whether it costs more.
- Three Ollama Cloud models ran the coding, harder-task and HumanEval suites, and those three plus Claude Haiku 4.5 and Claude Sonnet 5.5 ran the two-session memory tasks. Claude coding, harder-task and HumanEval runs did not finish (the login expired), so their cells are empty rather than estimated.
- The agent runs measured commit `b8ccea1`. The router's learned vocabulary (`7aaa1ff`) came after it and was measured offline, and the live skill-use check ran on the router at `8279f19`; no agent run has measured the finished release as a whole.
- Samples are small. Read overlapping intervals as "no clear difference", not as proof of equality.
- Skills built for a specific stack (Laravel, Nuxt, Docker, marketing, legal) are not exercised by generic coding tasks. Their value is not measured here.
- The held-out skill-search prompts and their acceptable skills are the judgment of AI agents, not ground truth.
- The memory tasks measure whether a stated rule is remembered, not whether notes help with open questions such as "why did we choose this design?".
- The agent in these runs is Claude Code. The helper hooks only exist for Claude Code, so Cursor, Codex, OpenCode, and OMP got the skills and instructions but not the hooks, and were not benchmarked.

## Skill search on new prompts (328 requests)

Two sets of requests were written by agents that saw only the skill catalog (each skill's id and description), never the router code or its tests, and each request lists the skills a sensible expert would accept for each of its parts (a second agent then added any other skills it judged equally acceptable). The older set has 160 requests, the newer one 168 and was written after the older half had been used for tuning. Each set is split in two by a hash of the request id; the router is tuned on one half and the numbers reported are for the other. The reported result is on 158 requests.

The vocabulary of requests was generated the same way, from each `SKILL.md` alone and without seeing any of these requests: one small model per skill wrote about 30 messages (241 skills, 7,240 messages in all) "that real users would type when this skill is the right first skill" (12 detailed, 6 short, 6 messy, 4 mixed Malay-English, 2 indirect), described in terms of symptoms, tools, error strings and goals rather than the skill's own words. The weight and the cutoffs were chosen on the tuning halves and the curated regression cases (`tests/test_routing.py`) and reported on the test halves. The previous router scored 66% first-pick accuracy on those 158 requests, the current one 81%, plain keyword search 56%.

Two things this does not show. First, the 81% is for requests the router was not tuned on; the 84 regression prompts below it score 100% only because it was tuned on them, so that number is not worth quoting as accuracy. Second, better ranking does not by itself change what an agent does. In the live check (DeepSeek V4.1 Flash on 60 of the test requests, with the router at commit `8279f19`) an acceptable skill was opened for 45% of them (27 of 60) and no skill at all for 43% (26 of 60); the earlier check on 73 requests with the older router gave 55% and 27%. In the coding, harder-task, HumanEval and memory runs, skills were almost never opened: 4 of 487 completed runs with Bossku Superpower opened one (`minimal-fix`, `bosskuai-tdd-loop` or `bosskuai-qa-automation-strategy`; count them with `python scripts/skill_use_count.py`). What the hint says, and when, matters more than the ranking.

## Tuned routing regression (84 prompts)

The older offline check compares Bossku Superpower's lexical routing with an ID/description-only keyword baseline on the 84 prompts the router was tuned against. It makes no model calls and needs only Python's standard library. Treat it as a regression test, not as evidence of accuracy on new prompts; the held-out check above is for that.

The [machine-readable snapshot](routing.json) holds every prompt, defensible answer set, predicted ID, ranked score, and pass/fail outcome.

| Method | Top-one hits | Top-three hits |
|---|---|---|
| Bossku Superpower `find_skill` / `rank_skills` | 84/84 (100%) | 84/84 (100%) |
| ID/description-only keyword baseline | 46/84 (54.76%) | 62/84 (73.81%) |

The automatic selector (`select_skill_stack`) is scored separately under `results.automatic_selection`: 79/79 model-invoked primaries and 3/3 user-only commands correctly deferred.

```console
python scripts/benchmark_routing.py          # regenerate docs/benchmarks/routing.json
python scripts/benchmark_routing.py --check  # compare current inputs and results with the snapshot
python -m unittest discover -s tests -p test_routing_benchmark.py -v
```

The corpus comes from the literal `ROUTING_CASES` and `REVIEW_ROUTING_CASES` assignments in [tests/test_routing.py](../../tests/test_routing.py), read with AST literal evaluation without running the test module. Identical prompts merge into one case with the union of their defensible IDs. The baseline removes the `bosskuai-` prefix from each skill ID, tokenizes the ID and description with the same normalization as the router, and scores each skill by its IDF-weighted share of the query terms; it uses no curated triggers, exclusions, aliases, or body headings. Numeric scores from the two methods use different scales and are not confidence probabilities. A ranking hit does not authorize automatic loading of a user-only skill.
