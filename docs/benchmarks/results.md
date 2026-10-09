# Benchmark results

The full results behind the short summary in the [main README](../../README.md). Every number, table and chart in the marked blocks is rebuilt from the saved result files by [`scripts/make_charts.py`](../../scripts/make_charts.py), and [`tests/test_results_consistent.py`](../../tests/test_results_consistent.py) fails if they drift. How each check works is in the [benchmark notes](README.md).

We ran a real coding agent (Claude Code) on coding tasks with hidden tests, once **without Bossku Superpower** and once **with Bossku Superpower**, on the same tasks. Some tasks have two sessions: the first states a project rule, the second asks for related work that breaks the rule unless it is remembered. The sentences around the numbers are written by hand.

![How each result was measured: a coding task and a fresh project go to an agent run beside an isolation check; a usage meter and hidden tests feed a comparison of the two setups, which feeds the charts.](../assets/benchmark-method.svg)

## In short

In plain words: the clearest gain is **memory**. When a rule is stated in one session and needed in the next, Claude Haiku 4.5 (48% to 68%), Claude Sonnet 5.5 (64% to 84%) and Gemma 4 31B (39% to 68%) finished 20 to 30 points more tasks with Bossku Superpower. DeepSeek V4.1 Flash and Nemotron 3 Nano showed no clear difference there. On the coding and harder tasks no model passed clearly more; models that tend to skip running their code (Gemma, Nemotron) ran it far more often, and the small Nemotron model passed more HumanEval problems (62% to 92%). The extra checking costs tokens, from about 1.1 times to 4.7 times as many, and most where the model had done the least checking before. The sample sizes are small, so read each result with its interval.

<!-- summary-overall:start -->
- **DeepSeek V4.1 Flash showed no clear difference on coding tasks:** 97% without, 94% with.
- **Gemma 4 31B showed no clear difference on coding tasks:** 82% without, 82% with.
- **Nemotron 3 Nano 30B showed no clear difference on coding tasks:** 18% without, 29% with.
- **DeepSeek V4.1 Flash showed no clear difference on harder tasks:** 95% without, 93% with.
- **Gemma 4 31B showed no clear difference on harder tasks:** 57% without, 64% with.
- **Nemotron 3 Nano 30B showed no clear difference on harder tasks:** 0% without, 7% with.
- **Claude Haiku 4.5 finished more tasks that need a rule from an earlier session with Bossku Superpower:** 48% without, 68% with.
- **Claude Sonnet 5.5 finished more tasks that need a rule from an earlier session with Bossku Superpower:** 64% without, 84% with.
- **DeepSeek V4.1 Flash showed no clear difference on tasks that need a rule from an earlier session:** 79% without, 74% with.
- **Gemma 4 31B finished more tasks that need a rule from an earlier session with Bossku Superpower:** 39% without, 68% with.
- **Nemotron 3 Nano 30B showed no clear difference on tasks that need a rule from an earlier session:** 6% without, 9% with.
- **The extra checking costs tokens:** tokens per run with Bossku Superpower compared with without: DeepSeek V4.1 Flash 1.1× on coding tasks, Gemma 4 31B 1.4× on coding tasks, Nemotron 3 Nano 30B 4.7× on coding tasks, DeepSeek V4.1 Flash 1.1× on harder tasks, Gemma 4 31B 1.2× on harder tasks, Nemotron 3 Nano 30B 2.9× on harder tasks, Claude Haiku 4.5 1.2× on two-session tasks, Claude Sonnet 5.5 1.1× on two-session tasks, DeepSeek V4.1 Flash 1.0× on two-session tasks, Gemma 4 31B 1.6× on two-session tasks, Nemotron 3 Nano 30B 2.8× on two-session tasks.
- **It finds the right skill more often:** 81% first-pick accuracy on new requests, against 56% for keyword search.
- **Its fixed cost is small:** extra tokens on the first call of a session: 1,241 on Claude Haiku 4.5, 2,155 on Claude Sonnet 5.5.
<!-- summary-overall:end -->

## What it adds to every session

![With and without Bossku Superpower: the input tokens and the cost of the first call of a Claude Code session](../assets/benchmark-session-overhead.svg)

<!-- summary-overhead:start -->
**What this shows:** Bossku Superpower adds a small, fixed amount to the first call of a session: Claude Haiku 4.5 +1,241 tokens (4% more), +$0.0011; Claude Sonnet 5.5 +2,155 tokens (6% more), +$0.0049. That is the skill list and the short instructions. The same text is reused on every later call, so it does not grow with the length of the session.
<!-- summary-overhead:end -->

## Finding the right skill

![With Bossku Superpower and with plain keyword search: how often the right skill is ranked first on requests it was never tuned on](../assets/benchmark-routing.svg)

<!-- summary-routing:start -->
**What this shows:** on 158 requests it was never tuned on, Bossku Superpower ranked an acceptable skill first 81% of the time, against 56% for plain keyword search. For requests with several jobs it found a fitting skill for every part 75% of the time. With a real agent (DeepSeek V4.1 Flash) on 60 of those requests, an acceptable skill was actually opened for 45% of them.
<!-- summary-routing:end -->

## Finishing tasks

![With and without Bossku Superpower: the share of hidden-test tasks and HumanEval problems passed, per model](../assets/benchmark-pass-rates.svg)

<!-- summary-pass:start -->
**Hidden-test coding tasks**
- **DeepSeek V4.1 Flash: no clear difference.** 94% with Bossku Superpower against 97% without (34 runs each): -3 points over the same tasks, 95% interval -9 to 0. Both setups were already near the ceiling, so there was little room to improve.
- **Gemma 4 31B: no clear difference.** 82% with Bossku Superpower against 82% without (17 runs each): 0 points over the same tasks, 95% interval -18 to +18.
- **Nemotron 3 Nano 30B: no clear difference.** 29% with Bossku Superpower against 18% without (68 runs without, 34 with): +12 points over the same tasks, 95% interval -3 to +28.

**Harder tasks**
- **DeepSeek V4.1 Flash: no clear difference.** 93% with Bossku Superpower against 95% without (42 runs without, 28 with): -2 points over the same tasks, 95% interval -7 to 0. Both setups were already near the ceiling, so there was little room to improve.
- **Gemma 4 31B: no clear difference.** 64% with Bossku Superpower against 57% without (42 runs without, 28 with): +7 points over the same tasks, 95% interval -6 to +20.
- **Nemotron 3 Nano 30B: no clear difference.** 7% with Bossku Superpower against 0% without (14 runs each): +7 points over the same tasks, 95% interval 0 to +21.

**HumanEval problems**
- **DeepSeek V4.1 Flash: no clear difference.** 100% with Bossku Superpower against 100% without (40 runs each): the same result on every one of the 40 problems. Both setups were already near the ceiling, so there was little room to improve.
- **Gemma 4 31B: no clear difference.** 100% with Bossku Superpower against 95% without (20 runs each): +5 points over the same problems, 95% interval 0 to +15. Both setups were already near the ceiling, so there was little room to improve.
- **Nemotron 3 Nano 30B finished more problems.** 92% with Bossku Superpower against 62% without (40 runs each): +30 points over the same problems, 95% interval +15 to +45.
<!-- summary-pass:end -->

## Running the code

![With and without Bossku Superpower: the share of runs that changed code and then ended without running anything](../assets/benchmark-checking.svg)

<!-- summary-checking:start -->
**What this shows:** the habit that Bossku Superpower's stop check is built to change. A model that never runs what it wrote cannot find its own mistakes.
- **DeepSeek V4.1 Flash** ended without running its code in 3% of the runs that changed code on its own, and in 0% with Bossku Superpower.
- **Gemma 4 31B** ended without running its code in 53% of the runs that changed code on its own, and in 0% with Bossku Superpower.
- **Nemotron 3 Nano 30B** ended without running its code in 100% of the runs that changed code on its own, and in 17% with Bossku Superpower.
<!-- summary-checking:end -->

## Remembering a rule from an earlier session

![With and without Bossku Superpower: the share of two-session tasks passed, where the second session breaks a project rule unless it is remembered](../assets/benchmark-memory.svg)

<!-- summary-memory:start -->
**What this shows:** each task states a project rule in a first session (for example "this must run on Python 3.8" or "never use eval") and asks for related work in a second one that would break the rule if forgotten. The agent starts the second session fresh: without Bossku Superpower it has only the files; with Bossku Superpower it also sees the notes it saved.
- **Claude Haiku 4.5 finished more tasks.** 68% with Bossku Superpower against 48% without (44 runs each): +20 points over the same tasks, 95% interval +7 to +34. In the first session, the agent with Bossku Superpower saved the rule as a note 100% of the time.
- **Claude Sonnet 5.5 finished more tasks.** 84% with Bossku Superpower against 64% without (44 runs each): +20 points over the same tasks, 95% interval +7 to +36. In the first session, the agent with Bossku Superpower saved the rule as a note 100% of the time.
- **DeepSeek V4.1 Flash: no clear difference.** 74% with Bossku Superpower against 79% without (66 runs each): -5 points over the same tasks, 95% interval -14 to +3. In the first session, the agent with Bossku Superpower saved the rule as a note 100% of the time.
- **Gemma 4 31B finished more tasks.** 68% with Bossku Superpower against 39% without (44 runs each): +30 points over the same tasks, 95% interval +11 to +48. In the first session, the agent with Bossku Superpower saved the rule as a note 100% of the time.
- **Nemotron 3 Nano 30B: no clear difference.** 9% with Bossku Superpower against 6% without (34 runs each): +7 points over the same tasks, 95% interval -7 to +23. In the first session, the agent with Bossku Superpower saved the rule as a note 76% of the time.
<!-- summary-memory:end -->

## What it costs in tokens

![With and without Bossku Superpower: tokens per run and per solved task](../assets/benchmark-effort.svg)

<!-- summary-effort:start -->
**What this shows:** Bossku Superpower makes the agent do more work, and work costs tokens. The extra work is running, checking and fixing. Where that turns failures into passes it is worth it; where the model already passes, it is not.
- **DeepSeek V4.1 Flash, coding tasks:** 1.1× the tokens per run (107k without, 119k with) and 1.2× the tokens per task it actually solved. It ran shell commands 2.7 times per run instead of 2.4.
- **Gemma 4 31B, coding tasks:** 1.4× the tokens per run (67k without, 95k with) and 1.4× the tokens per task it actually solved. It ran shell commands 2.4 times per run instead of 1.3.
- **Nemotron 3 Nano 30B, coding tasks:** 4.7× the tokens per run (52k without, 244k with) and 2.8× the tokens per task it actually solved. It ran shell commands 4.1 times per run instead of 0.1.
- **DeepSeek V4.1 Flash, harder tasks:** 1.1× the tokens per run (294k without, 310k with) and 1.1× the tokens per task it actually solved. It ran shell commands 5.2 times per run instead of 5.3.
- **Gemma 4 31B, harder tasks:** 1.2× the tokens per run (195k without, 235k with) and 1.1× the tokens per task it actually solved. It ran shell commands 4.6 times per run instead of 3.0.
- **Nemotron 3 Nano 30B, harder tasks:** 2.9× the tokens per run (135k without, 391k with). It ran shell commands 3.9 times per run instead of 1.1.
- **Claude Haiku 4.5, two-session tasks:** 1.2× the tokens per run (252k without, 311k with) and 0.9× the tokens per task it actually solved. It ran shell commands 2.3 times per run instead of 1.9.
- **Claude Sonnet 5.5, two-session tasks:** 1.1× the tokens per run (139k without, 147k with) and 0.8× the tokens per task it actually solved. It ran shell commands 2.0 times per run instead of 1.7.
- **DeepSeek V4.1 Flash, two-session tasks:** about the same tokens per run (118k without, 118k with) and 1.1× the tokens per task it actually solved. It ran shell commands 2.1 times per run instead of 2.1.
- **Gemma 4 31B, two-session tasks:** 1.6× the tokens per run (62k without, 98k with) and 0.9× the tokens per task it actually solved. It ran shell commands 1.8 times per run instead of 0.5.
- **Nemotron 3 Nano 30B, two-session tasks:** 2.8× the tokens per run (78k without, 219k with) and 1.9× the tokens per task it actually solved. It ran shell commands 3.9 times per run instead of 0.2.
<!-- summary-effort:end -->

## All the numbers

<!-- results:start -->
| First call of a session | Without Bossku Superpower | With Bossku Superpower |
|---|---:|---:|
| Claude Haiku 4.5: input tokens | 33,413 | 34,654 |
| Claude Haiku 4.5: cost | $0.0109 | $0.0120 |
| Claude Sonnet 5.5: input tokens | 35,403 | 37,558 |
| Claude Sonnet 5.5: cost | $0.0247 | $0.0297 |

| Finding a skill (158 new requests) | Keyword search only | With Bossku Superpower |
|---|---:|---:|
| Right skill ranked first | 56% | 81% |
| Right skill in the top three | 73% | 94% |
| Every part of a multi-part request covered | - | 75% |
| A real agent (DeepSeek V4.1 Flash) opens an acceptable skill | - | 45% |

| Hidden-test coding tasks | Without Bossku Superpower | With Bossku Superpower |
|---|---:|---:|
| DeepSeek V4.1 Flash: tasks passed (34 runs each) | 97% (33/34) | 94% (32/34) |
| DeepSeek V4.1 Flash: tokens per run | 107k | 119k |
| DeepSeek V4.1 Flash: ended without running its code | 3% | 0% |
| Gemma 4 31B: tasks passed (17 runs each) | 82% (14/17) | 82% (14/17) |
| Gemma 4 31B: tokens per run | 67k | 95k |
| Gemma 4 31B: ended without running its code | 53% | 0% |
| Nemotron 3 Nano 30B: tasks passed (68 runs without, 34 with) | 18% (12/68) | 29% (10/34) |
| Nemotron 3 Nano 30B: tokens per run | 52k | 244k |
| Nemotron 3 Nano 30B: ended without running its code | 100% | 17% |

| Harder tasks | Without Bossku Superpower | With Bossku Superpower |
|---|---:|---:|
| DeepSeek V4.1 Flash: tasks passed (42 runs without, 28 with) | 95% (40/42) | 93% (26/28) |
| DeepSeek V4.1 Flash: tokens per run | 294k | 310k |
| Gemma 4 31B: tasks passed (42 runs without, 28 with) | 57% (24/42) | 64% (18/28) |
| Gemma 4 31B: tokens per run | 195k | 235k |
| Nemotron 3 Nano 30B: tasks passed (14 runs each) | 0% (0/14) | 7% (1/14) |
| Nemotron 3 Nano 30B: tokens per run | 135k | 391k |

| HumanEval problems | Without Bossku Superpower | With Bossku Superpower |
|---|---:|---:|
| DeepSeek V4.1 Flash: tasks passed (40 runs each) | 100% (40/40) | 100% (40/40) |
| DeepSeek V4.1 Flash: tokens per run | 63k | 79k |
| Gemma 4 31B: tasks passed (20 runs each) | 95% (19/20) | 100% (20/20) |
| Gemma 4 31B: tokens per run | 54k | 74k |
| Nemotron 3 Nano 30B: tasks passed (40 runs each) | 62% (25/40) | 92% (37/40) |
| Nemotron 3 Nano 30B: tokens per run | 89k | 282k |

| Remembering a rule from an earlier session | Without Bossku Superpower | With Bossku Superpower |
|---|---:|---:|
| Claude Haiku 4.5: tasks passed (44 runs each) | 48% (21/44) | 68% (30/44) |
| Claude Haiku 4.5: tokens per run | 252k | 311k |
| Claude Sonnet 5.5: tasks passed (44 runs each) | 64% (28/44) | 84% (37/44) |
| Claude Sonnet 5.5: tokens per run | 139k | 147k |
| DeepSeek V4.1 Flash: tasks passed (66 runs each) | 79% (52/66) | 74% (49/66) |
| DeepSeek V4.1 Flash: tokens per run | 118k | 118k |
| Gemma 4 31B: tasks passed (44 runs each) | 39% (17/44) | 68% (30/44) |
| Gemma 4 31B: tokens per run | 62k | 98k |
| Nemotron 3 Nano 30B: tasks passed (34 runs each) | 6% (2/34) | 9% (3/34) |
| Nemotron 3 Nano 30B: tokens per run | 78k | 219k |
<!-- results:end -->

## What these results do not show

- **Python projects of a few dozen to a few hundred lines.** Nothing here covers large repositories, other languages, or open-ended design work.
- **Mostly open models.** Through Ollama Cloud, driven by Claude Code: Nemotron 3 Nano 30B (small), Gemma 4 31B (mid-size) and DeepSeek V4.1 Flash (strong) on the coding tasks, the harder tasks and HumanEval. Claude Haiku 4.5 and Claude Sonnet 5.5 were run on the two-session memory tasks and for the cost of a session's first call; their coding, harder-task and HumanEval runs did not finish because the Claude login expired, so those cells are empty. No dollar cost per coding task is reported; tokens are the unit.
- **Which build, and reused baselines.** The agent runs used commit `b8ccea1` (5 October 2026). The session-cost figures come from `02ee2f2` (1 October), the live skill-use figure from the router at `8279f19`, and the router's later vocabulary and the stated-rule detector were measured offline, not with an agent. For seven sets of runs (coding for Nemotron and DeepSeek, harder tasks for DeepSeek and Gemma, HumanEval for Nemotron and DeepSeek, and DeepSeek on the ten original two-session tasks) the *without* runs are from the earlier run of 1 to 2 October, which is why some lanes show more runs without than with; the setup without Bossku Superpower does not depend on the build, but the days and the Claude Code version (2.1.284 against 2.1.293) differ. An earlier run of the same tasks on `02ee2f2`, with both setups at the same time, gave Nemotron coding 18% to 40% (the later run: 18% to 29%) and Nemotron HumanEval 62% to 82% (later: 92%), so a few points either way is noise; see the [benchmark notes](README.md#the-earlier-run).
- **Tasks written by assistants.** The harder and two-session tasks were written by AI assistants told not to read Bossku Superpower. Each was checked against a reference solution, and a few over-strict checks were fixed for both setups after a trial run. The [benchmark notes](README.md) list what changed.
- **Small samples.** Overlapping intervals mean "no clear difference", not "equal".
- **AI judgment.** The 328 skill-search requests and the skills accepted for them were written by AI agents that saw only the skill catalog, never the router (160 first, 168 later), so they are not ground truth.
- **Claude Code only.** The helper hooks exist for Claude Code. Cursor, Codex, OpenCode, and OMP get the skills and instructions but were not benchmarked.
