# Does a skill, or the whole pack, help?

This page asks one question of the run rows the repository already has: with the pack, did the agent do better than without it? It uses [`scripts/skill_effectiveness.py`](../../scripts/skill_effectiveness.py), makes no model calls, and adds no new runs. The method and the record format are in [`benchmarks/skill-effectiveness/README.md`](../../benchmarks/skill-effectiveness/README.md). Every number below comes from the command shown above its table, run on the row files named in it.

## What the data can and cannot say

- **No single skill has ever been switched off on its own.** The runs compare "no pack" with "the pack". So there is no measured effect for any one skill. The records for `bosskuai-diagnose-loop`, `bosskuai-tdd-loop`, `bosskuai-engineering-delivery`, `verification-before-completion`, `minimal-fix` and `bosskuai-rigorous-code-review` say `not_tested`, with every measured field empty.
- **Most with-pack runs opened no skill.** The rows do not say which part of the bundle (instructions, hooks, session brief, notes) did the work. A pass in a with-pack run is not evidence that a skill was applied. The rows do not record whether a skill hint was shown, so that column says `not recorded`. Nothing here is taken from what the model said about itself.
- **A small paired sample cannot carry a strong label.** The label rule needs at least 10 paired tasks for "demonstrated". An interval that includes zero is called `promising_insufficient_evidence` or `neutral_or_inconclusive`, never "no difference".
- **Several suites are at the ceiling.** When both arms pass nearly every task, there is no room to show a gain, and the interval is `+0.00 to +0.00`. That is labelled `neutral_or_inconclusive`: it means the test could not tell, not that the pack changes nothing. At the ceiling: both Claude Haiku 4.5 and Claude Sonnet 5.5 on the coding tasks in the 29 October set (94% each), Claude Haiku 5.5 and Claude Opus 5.5 on HumanEval (98% to 100%) and on the coding tasks in the 10 October set (94% to 100%), and DeepSeek V4.1 Flash on HumanEval.
- **Arms did not always have equal runs, or run on the same day.** The "Days" column lists the dates (from each row's timestamp) the without and with rows were run. In the 1 to 8 October set, many without rows come from 1 October and the with rows from 8 October (the reused baselines in the [benchmark notes](README.md)), and some pairs have more without runs than with runs. In the 10 October set the improved build (`ship2`) ran the day after its baseline. Rows with different dates can differ for reasons that have nothing to do with the pack (service load, the Claude Code version).
- **Unpaired cells are marked.** In the 10 October set, GLM 5.3, GLM 5.3 Flash and Kimi K3 did not finish the same tasks in both arms (a usage limit stopped some runs). Those cells are compared on the tasks both arms completed, marked `(unpaired)`, and written to no record. DeepSeek V4.1 Flash has only a with-pack arm in that set, so it has no comparison.
- **A "demonstrated" label needs the exact sign test too.** With only a few tasks that differ, the bootstrap interval can exclude zero by luck. So both "demonstrated" labels also need a sign test p of 0.05 or less. Claude Haiku 5.5 and Claude Haiku 4.5 on `memory-rules` (4 tasks better, none worse, p = 0.125) are therefore `promising_insufficient_evidence`.
- **Tokens and cost.** Token overhead is the mean input plus output tokens per run with the pack, over the same for without. Cost per passed task is left out (`-`) wherever a row has no cost; the Ollama Cloud rows have none.

## Did an agent open a skill?

`python scripts/skill_effectiveness.py activation --table ROWS...` counts, per model and arm, runs where a skill hint was shown, runs where at least one skill was opened (from `skills_loaded` or `skills_invoked`), and, where a row names the acceptable skills for the request (only the live routing rows do), runs where an acceptable skill was opened and runs where only other skills were opened. Three separate facts: hinted, opened, passed. "Passed" counts runs.

### 1 to 8 October set

Rows: `benchmarks/results/raw/{coding,hard,humaneval,memory}-*.jsonl` and `routing.jsonl`. The arm is `after`.

| Model | Arm | Kind | Runs | Hint shown | Opened a skill | Acceptable skill opened | Only other skills opened | Passed |
|---|---|---|---|---|---|---|---|---|
| claude-haiku-4-5-20251001 | after | task | 44 | not recorded | 0 | n/a | n/a | 30 |
| claude-haiku-4-5-20251001 | baseline | task | 44 | not recorded | 0 | n/a | n/a | 21 |
| claude-sonnet-5-5 | after | task | 44 | not recorded | 0 | n/a | n/a | 37 |
| claude-sonnet-5-5 | baseline | task | 44 | not recorded | 0 | n/a | n/a | 28 |
| deepseek-v4.1-flash | after | routing | 60 | not recorded | 34 | 27 | 7 | n/a |
| deepseek-v4.1-flash | after | task | 168 | not recorded | 4 | n/a | n/a | 147 |
| deepseek-v4.1-flash | baseline | task | 182 | not recorded | 0 | n/a | n/a | 165 |
| gemma4:31b | after | task | 109 | not recorded | 0 | n/a | n/a | 82 |
| gemma4:31b | baseline | task | 123 | not recorded | 0 | n/a | n/a | 74 |
| nemotron-3-nano:30b | after | task | 122 | not recorded | 0 | n/a | n/a | 51 |
| nemotron-3-nano:30b | baseline | task | 156 | not recorded | 0 | n/a | n/a | 39 |

On the live routing rows (60 requests), the agent opened an acceptable skill in 27 runs and only other skills in 7.

### 10 October set

Rows: `benchmarks/results/raw/2026-10-10/*.jsonl`. The arms are `ship` (v2.2.0) and `ship2` (the improved build).

| Model | Arm | Kind | Runs | Hint shown | Opened a skill | Acceptable skill opened | Only other skills opened | Passed |
|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | baseline | task | 79 | not recorded | 0 | n/a | n/a | 66 |
| claude-haiku-5-5 | ship | task | 79 | not recorded | 0 | n/a | n/a | 71 |
| claude-haiku-5-5 | ship2 | task | 79 | not recorded | 1 | n/a | n/a | 71 |
| claude-opus-5-5 | baseline | task | 79 | not recorded | 0 | n/a | n/a | 72 |
| claude-opus-5-5 | ship | task | 79 | not recorded | 0 | n/a | n/a | 73 |
| claude-opus-5-5 | ship2 | task | 79 | not recorded | 0 | n/a | n/a | 72 |
| deepseek-v4.1-flash | ship | task | 22 | not recorded | 0 | n/a | n/a | 18 |
| glm-5.3 | baseline | task | 20 | not recorded | 0 | n/a | n/a | 13 |
| glm-5.3 | ship | task | 20 | not recorded | 4 | n/a | n/a | 16 |
| glm-5.3-flash | baseline | task | 6 | not recorded | 0 | n/a | n/a | 5 |
| glm-5.3-flash | ship | task | 8 | not recorded | 0 | n/a | n/a | 7 |
| kimi-k3 | baseline | task | 14 | not recorded | 0 | n/a | n/a | 9 |
| kimi-k3 | ship | task | 17 | not recorded | 0 | n/a | n/a | 13 |

### 29 October set (packs)

Rows: `benchmarks/results/raw/2026-10-29-packs/*.jsonl`. The arm is `bossku`; the other packs are listed for the opening counts only.

| Model | Arm | Kind | Runs | Hint shown | Opened a skill | Acceptable skill opened | Only other skills opened | Passed |
|---|---|---|---|---|---|---|---|---|
| claude-haiku-4-5-20251001 | anthropic | task | 39 | not recorded | 0 | n/a | n/a | 24 |
| claude-haiku-4-5-20251001 | baseline | task | 39 | not recorded | 0 | n/a | n/a | 24 |
| claude-haiku-4-5-20251001 | bossku | task | 39 | not recorded | 21 | n/a | n/a | 30 |
| claude-haiku-4-5-20251001 | ecc | task | 39 | not recorded | 0 | n/a | n/a | 25 |
| claude-haiku-4-5-20251001 | karpathy | task | 39 | not recorded | 0 | n/a | n/a | 23 |
| claude-haiku-4-5-20251001 | superpowers | task | 39 | not recorded | 0 | n/a | n/a | 22 |
| claude-sonnet-5-5 | anthropic | task | 39 | not recorded | 0 | n/a | n/a | 30 |
| claude-sonnet-5-5 | baseline | task | 39 | not recorded | 0 | n/a | n/a | 31 |
| claude-sonnet-5-5 | bossku | task | 39 | not recorded | 0 | n/a | n/a | 35 |
| claude-sonnet-5-5 | ecc | task | 39 | not recorded | 0 | n/a | n/a | 28 |
| claude-sonnet-5-5 | karpathy | task | 39 | not recorded | 0 | n/a | n/a | 28 |
| claude-sonnet-5-5 | superpowers | task | 39 | not recorded | 0 | n/a | n/a | 29 |

## With the pack against without

`python scripts/skill_effectiveness.py compare --table --baseline baseline --arm ARM ROWS...`, paired by task: for each task the pass rate in each arm (several trials are averaged), then the mean of the per-task differences. The interval is a bootstrap of those differences (fixed seed). The sign test p is the exact two-sided test on the tasks that differ. Pass rates are over runs. The labels come from `classify` and the rule in the [README](../../benchmarks/skill-effectiveness/README.md).

### 1 to 8 October set, arm `after`

Command: `python scripts/skill_effectiveness.py compare --allow-unpaired --baseline baseline --arm after benchmarks/results/raw/{coding,hard,humaneval,memory}-*.jsonl` (no cell was actually unpaired; the flag is there so a cell cannot be dropped silently).

| Model | Suite | Arm | Paired tasks | Without: pass (runs) | With: pass (runs) | Difference | 95% interval | Sign test p | Token overhead | Label | Days without / with |
|---|---|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-4-5-20251001 | memory | after | 22 | 48% (44) | 68% (44) | +0.20 | +0.07 to +0.34 | 0.021 | +23% | demonstrated_improvement | 10-05 / 10-05 |
| claude-sonnet-5-5 | memory | after | 22 | 64% (44) | 84% (44) | +0.20 | +0.07 to +0.36 | 0.031 | +5% | demonstrated_improvement | 10-05 / 10-05 |
| deepseek-v4.1-flash | coding | after | 17 | 97% (34) | 94% (34) | -0.03 | -0.09 to +0.00 | 1.000 | +12% | neutral_or_inconclusive | 10-01 / 10-08 |
| deepseek-v4.1-flash | hard | after | 14 | 95% (42) | 93% (28) | -0.02 | -0.07 to +0.00 | 1.000 | +5% | neutral_or_inconclusive | 10-01 / 10-08 |
| deepseek-v4.1-flash | humaneval | after | 40 | 100% (40) | 100% (40) | +0.00 | +0.00 to +0.00 | - | +26% | neutral_or_inconclusive | 10-01 / 10-08 |
| deepseek-v4.1-flash | memory | after | 22 | 79% (66) | 74% (66) | -0.05 | -0.14 to +0.03 | 0.688 | +0% | neutral_or_inconclusive | 10-01, 10-05 / 10-05, 10-08 |
| gemma4:31b | coding | after | 17 | 82% (17) | 82% (17) | +0.00 | -0.18 to +0.18 | 1.000 | +41% | neutral_or_inconclusive | 10-08 / 10-08 |
| gemma4:31b | hard | after | 14 | 57% (42) | 64% (28) | +0.07 | -0.06 to +0.20 | 0.375 | +20% | promising_insufficient_evidence | 10-01 / 10-08 |
| gemma4:31b | humaneval | after | 20 | 95% (20) | 100% (20) | +0.05 | +0.00 to +0.15 | 1.000 | +37% | promising_insufficient_evidence | 10-08 / 10-08 |
| gemma4:31b | memory | after | 22 | 39% (44) | 68% (44) | +0.30 | +0.11 to +0.48 | 0.021 | +59% | demonstrated_improvement | 10-05, 10-08 / 10-05, 10-08 |
| nemotron-3-nano:30b | coding | after | 17 | 18% (68) | 29% (34) | +0.12 | -0.03 to +0.28 | 0.289 | +369% | promising_insufficient_evidence | 10-01 / 10-08 |
| nemotron-3-nano:30b | hard | after | 14 | 0% (14) | 7% (14) | +0.07 | +0.00 to +0.21 | 1.000 | +189% | promising_insufficient_evidence | 10-08 / 10-08 |
| nemotron-3-nano:30b | humaneval | after | 40 | 62% (40) | 92% (40) | +0.30 | +0.15 to +0.45 | 0.002 | +217% | demonstrated_improvement | 10-01 / 10-05, 10-08 |
| nemotron-3-nano:30b | memory | after | 22 | 6% (34) | 9% (34) | +0.07 | -0.07 to +0.23 | 1.000 | +180% | promising_insufficient_evidence | 10-05, 10-08 / 10-05, 10-08 |

### 10 October set, arms `ship` and `ship2`

Command: `python scripts/skill_effectiveness.py compare --allow-unpaired --baseline baseline --arm ship --arm ship2 benchmarks/results/raw/2026-10-10/*.jsonl`

| Model | Suite | Arm | Paired tasks | Without: pass (runs) | With: pass (runs) | Difference | 95% interval | Sign test p | Token overhead | Label | Days without / with |
|---|---|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | humaneval | ship | 40 | 100% (40) | 98% (40) | -0.03 | -0.07 to +0.00 | 1.000 | +46% | neutral_or_inconclusive | 10-09 / 10-09 |
| claude-haiku-5-5 | memory | ship | 10 | 50% (10) | 70% (10) | +0.20 | +0.00 to +0.50 | 0.500 | 0% | promising_insufficient_evidence | 10-09 / 10-09 |
| claude-haiku-5-5 | memory-rules | ship | 12 | 42% (12) | 75% (12) | +0.33 | +0.08 to +0.58 | 0.125 | -28% | promising_insufficient_evidence | 10-09 / 10-09 |
| claude-haiku-5-5 | test | ship | 17 | 94% (17) | 94% (17) | +0.00 | +0.00 to +0.00 | - | +13% | neutral_or_inconclusive | 10-09 / 10-09 |
| claude-opus-5-5 | humaneval | ship | 40 | 100% (40) | 100% (40) | +0.00 | +0.00 to +0.00 | - | -5% | neutral_or_inconclusive | 10-09 / 10-09 |
| claude-opus-5-5 | memory | ship | 10 | 80% (10) | 90% (10) | +0.10 | +0.00 to +0.30 | 1.000 | -23% | promising_insufficient_evidence | 10-09 / 10-09 |
| claude-opus-5-5 | memory-rules | ship | 12 | 58% (12) | 67% (12) | +0.08 | -0.17 to +0.33 | 1.000 | -23% | promising_insufficient_evidence | 10-09 / 10-09 |
| claude-opus-5-5 | test | ship | 17 | 100% (17) | 94% (17) | -0.06 | -0.18 to +0.00 | 1.000 | +17% | neutral_or_inconclusive | 10-09 / 10-09 |
| glm-5.3 | memory | ship | 7 (unpaired) | 88% (8) | 88% (8) | +0.00 | +0.00 to +0.00 | - | +14% | neutral_or_inconclusive | 10-09 / 10-09 |
| glm-5.3 | memory-rules | ship | 12 | 50% (12) | 75% (12) | +0.25 | +0.00 to +0.50 | 0.250 | 0% | promising_insufficient_evidence | 10-10 / 10-10 |
| glm-5.3-flash | memory | ship | 5 (unpaired) | 83% (6) | 88% (8) | +0.00 | +0.00 to +0.00 | - | -42% | neutral_or_inconclusive | 10-09 / 10-09 |
| kimi-k3 | memory | ship | 6 (unpaired) | 57% (7) | 75% (8) | +0.33 | +0.00 to +0.67 | 0.500 | +13% | promising_insufficient_evidence | 10-09 / 10-09 |
| kimi-k3 | memory-rules | ship | 5 (unpaired) | 71% (7) | 78% (9) | +0.20 | +0.00 to +0.60 | 1.000 | -10% | promising_insufficient_evidence | 10-10 / 10-10 |
| claude-haiku-5-5 | humaneval | ship2 | 40 | 100% (40) | 100% (40) | +0.00 | +0.00 to +0.00 | - | -1% | neutral_or_inconclusive | 10-09 / 10-10 |
| claude-haiku-5-5 | memory | ship2 | 10 | 50% (10) | 70% (10) | +0.20 | +0.00 to +0.50 | 0.500 | -8% | promising_insufficient_evidence | 10-09 / 10-10 |
| claude-haiku-5-5 | memory-rules | ship2 | 12 | 42% (12) | 67% (12) | +0.25 | -0.08 to +0.58 | 0.375 | -33% | promising_insufficient_evidence | 10-09 / 10-10 |
| claude-haiku-5-5 | test | ship2 | 17 | 94% (17) | 94% (17) | +0.00 | +0.00 to +0.00 | - | -12% | neutral_or_inconclusive | 10-09 / 10-10 |
| claude-opus-5-5 | humaneval | ship2 | 40 | 100% (40) | 100% (40) | +0.00 | +0.00 to +0.00 | - | -6% | neutral_or_inconclusive | 10-09 / 10-10 |
| claude-opus-5-5 | memory | ship2 | 10 | 80% (10) | 80% (10) | +0.00 | +0.00 to +0.00 | - | -25% | neutral_or_inconclusive | 10-09 / 10-10 |
| claude-opus-5-5 | memory-rules | ship2 | 12 | 58% (12) | 67% (12) | +0.08 | -0.17 to +0.33 | 1.000 | -7% | promising_insufficient_evidence | 10-09 / 10-10 |
| claude-opus-5-5 | test | ship2 | 17 | 100% (17) | 94% (17) | -0.06 | -0.18 to +0.00 | 1.000 | +3% | neutral_or_inconclusive | 10-09 / 10-10 |

### 29 October set, arm `bossku`

Command: `python scripts/skill_effectiveness.py compare --baseline baseline --arm bossku benchmarks/results/raw/2026-10-29-packs/*.jsonl`

| Model | Suite | Arm | Paired tasks | Without: pass (runs) | With: pass (runs) | Difference | 95% interval | Sign test p | Token overhead | Label | Days without / with |
|---|---|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-4-5-20251001 | coding | bossku | 17 | 94% (17) | 94% (17) | +0.00 | +0.00 to +0.00 | - | +54% | neutral_or_inconclusive | 10-29 / 10-29 |
| claude-haiku-4-5-20251001 | memory | bossku | 10 | 50% (10) | 70% (10) | +0.20 | -0.20 to +0.60 | 0.625 | +76% | promising_insufficient_evidence | 10-29 / 10-29 |
| claude-haiku-4-5-20251001 | memory-rules | bossku | 12 | 25% (12) | 58% (12) | +0.33 | +0.08 to +0.58 | 0.125 | +28% | promising_insufficient_evidence | 10-29 / 10-29 |
| claude-sonnet-5-5 | coding | bossku | 17 | 94% (17) | 94% (17) | +0.00 | +0.00 to +0.00 | - | +21% | neutral_or_inconclusive | 10-29 / 10-29 |
| claude-sonnet-5-5 | memory | bossku | 10 | 90% (10) | 100% (10) | +0.10 | +0.00 to +0.30 | 1.000 | +5% | promising_insufficient_evidence | 10-29 / 10-29 |
| claude-sonnet-5-5 | memory-rules | bossku | 12 | 50% (12) | 75% (12) | +0.25 | +0.00 to +0.50 | 0.250 | -3% | promising_insufficient_evidence | 10-29 / 10-29 |

## Reading the tables

- Of the 41 cells, 4 got `demonstrated_improvement`, 19 `promising_insufficient_evidence`, 18 `neutral_or_inconclusive`, and none `demonstrated_regression`.
- All the `demonstrated_improvement` cells are in the memory tasks (a rule stated in one session, needed in the next), and for Nemotron 3 Nano on HumanEval. The coding tasks show no demonstrated change for any model with enough room to show one.
- No cell shows a demonstrated drop in pass rate. Several cells have a small negative point estimate whose interval includes zero; that is not evidence of a drop or of none.
- Token overhead is large for the small models (Nemotron and Gemma: +20% to +369%) and mixed for the Claude models (from -33% to +76%). The table gives each value.

## Records

[`benchmarks/skill-effectiveness/records/`](../../benchmarks/skill-effectiveness/records/) holds one JSON record for each paired cell above (written with `record`, status taken from `classify`, `last_evaluated` 2026-11-17) and six `not_tested` records for single skills. Cells where the arms ran different tasks are skipped by `record` (it prints a line for each), so they have no record. The pack records use the skill id `pack:bossku` and have no skill version. Their arm names tell which build was run (`after`, `ship`, `ship2`, `bossku`); the arms are different builds of the pack, so do not read them as one result.
