# Skill effectiveness records

A light way to say whether a skill, or the whole pack, helps, using only the run rows already in [`benchmarks/results/raw/`](../results/raw/). No model calls. The tool is [`scripts/skill_effectiveness.py`](../../scripts/skill_effectiveness.py); the tables it produced are on the [results page](../../docs/benchmarks/skill-effectiveness.md).

## What a record is

One JSON file in [`records/`](records/) says what was measured for one skill (or `pack:bossku` for the whole pack) on one model and suite. Fields:

| Field | Meaning |
|---|---|
| `skill_id`, `skill_version` | The skill, and the git blob hash of its `SKILL.md` (`git hash-object`, taken from the working tree on the day). `null` for the pack. |
| `model`, `host`, `task_category`, `suite` | Where it ran. `host` is `claude-code` when the rows carry a Claude Code version. `task_category` is set only when the rows name one category. The suite is the file prefix (`coding`, `memory`, ...), with the set folder in front for a dated set. |
| `baseline_arm`, `arm` | The two setups compared, as named in the rows. |
| `sample_size` | Paired tasks (tasks both arms ran). |
| `baseline_pass_rate`, `skill_pass_rate` | Share of runs that passed. |
| `paired_difference`, `confidence_interval` | Mean of per-task (arm minus baseline) pass differences, and its 95% bootstrap interval (4000 resamples, fixed seed). |
| `token_overhead` | Mean input plus output tokens per run of the arm over the baseline, minus 1. |
| `cost_per_success` | Total cost of the arm's runs over its passed runs. `null` when any run has no cost. |
| `evaluation_status` | A label from `classify`, or `required_safety_control` when the caller passed `--required`. |
| `last_evaluated` | Passed in with `--date`; the code never reads the clock. |
| `source_rows` | The row files read. |

A value that was not measured is `null`. The script never fills a number it did not compute. Individual skills have never been switched off on their own, so every single-skill record here is `not_tested` with empty measurements. The records for `pack:bossku` compare "no pack" with "a build of the pack"; the arm name (`after`, `ship`, `ship2`, `bossku`) says which build.

## Reproduce each number

Row files are JSONL. Arms: `baseline` is no pack; the pack is `after` (1 to 8 October), `ship` and `ship2` (10 October) or `bossku` (29 October).

| Command | Gives |
|---|---|
| `python scripts/skill_effectiveness.py activation --table ROWS...` | Per model and arm: runs, runs with a skill hint shown (`not recorded` when the rows do not say), runs that opened at least one skill, runs that opened an acceptable skill, runs that opened only other skills, runs passed. Three separate facts: hinted, opened, passed. A skill counts as opened only when the row lists it in `skills_loaded` or `skills_invoked`; nothing is taken from the model's own words. Only the live routing rows name acceptable skills. |
| `python scripts/skill_effectiveness.py compare --baseline baseline --arm bossku ROWS...` | Per model and suite, paired by task: pass rate of each arm with a 95% Wilson interval, the paired difference with its bootstrap interval and an exact sign test, mean tokens and cost, token overhead, cost per passed task. Stops with an error if the arms ran different tasks; `--allow-unpaired` compares the shared tasks and marks the cell `unpaired` with the task names that differ. `--arm` can repeat. |
| `python scripts/skill_effectiveness.py classify --baseline baseline --arm bossku ROWS...` | The label for each cell. |
| `python scripts/skill_effectiveness.py record --date 2026-11-17 --skill pack:bossku --baseline baseline --arm bossku ROWS...` | One record file per cell. Cells where the arms ran different tasks are skipped, with one line on stderr each. `--required` sets the status to `required_safety_control`, with or without row files. |
| `python scripts/skill_effectiveness.py record --date 2026-11-17 --skill minimal-fix` | A `not_tested` record with every measurement empty. |

Add `--table` to `activation`, `compare` and `classify` for a plain table. Rows from a harness error or an infrastructure failure are left out, as in `benchmark_agent.py`. The exact commands and row files for the published tables are on the [results page](../../docs/benchmarks/skill-effectiveness.md).

## Classification rule

`classify` reads one compare cell. At least 10 paired tasks and a sign test p of 0.05 or less are needed for either "demonstrated" label (`MIN_PAIRED_TASKS` in the script, tested).

| Label | When |
|---|---|
| `demonstrated_improvement` | 10 or more paired tasks, the whole interval is above zero, and the exact sign test p is 0.05 or less. |
| `demonstrated_regression` | 10 or more paired tasks, the whole interval is below zero, and the exact sign test p is 0.05 or less. |
| `promising_insufficient_evidence` | The point estimate is positive but the interval includes zero, or the interval is above zero but there are fewer than 10 paired tasks or the sign test p is above 0.05. |
| `neutral_or_inconclusive` | Anything else, including a zero difference and a negative estimate with an interval that includes zero. |
| `not_tested` | No paired rows. |

An interval that includes zero is never reported as "no difference".

## What the data cannot show

- Whether any one skill helps: no run switched a single skill off. Doing so needs an arm that installs the pack minus one skill; the arm set in `scripts/benchmark_agent.py` has no such option today.
- That a skill was applied. Rows say which skills were opened, not whether the work followed them. Most Claude runs with the pack opened no skill at all, and the rows do not say which part of the bundle (instructions, hooks, session brief, notes) did the work.
- Anything at the ceiling. When both arms pass nearly everything, the interval is zero-width and the label is `neutral_or_inconclusive`.
- Fair timing. Some baselines were run on other days than their with-pack rows, and some arms have unequal runs (the results page lists the dates); a difference can come from the day.
- A tight interval on few differing tasks. The bootstrap interval of per-task differences can exclude zero when only 4 tasks differ, where the exact sign test (also reported) does not. The labels therefore also require the sign test; the p value is in `compare` output but not in the record file.
- Tasks outside the suites: the tasks are small Python projects, HumanEval problems and two-session rule-keeping tasks.
