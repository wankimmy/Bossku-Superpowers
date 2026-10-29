# Bossku against other skill packs: 29 October 2026

This run puts Bossku Superpowers next to four other popular packs for Claude Code, plus Claude Code with no pack at all. All six setups ran the same tasks on the same day, with the same two Claude models. The method and the honesty rules are in the [benchmark notes](README.md). The raw rows are in [`benchmarks/results/raw/2026-10-29-packs/`](../../benchmarks/results/raw/2026-10-29-packs/).

## The short answer

- **Remembering a rule from an earlier session: Bossku passed the most.** Across both models, Bossku passed 33 of 44 two-session tasks (75%). The other packs passed 20 to 22 (45% to 50%), and no pack passed 23 (52%). Compared task by task, Bossku passed 11 tasks that no pack failed and failed 1 that no pack passed (exact test p = 0.006). Against each of the four other packs, the split was 11 to 0, 13 to 0, 13 to 2 and 14 to 1 in Bossku's favour (p from 0.0002 to 0.007). None of the four other packs differed clearly from no pack.
- **Coding tasks: no winner.** Every setup passed 31 or 32 of 34 coding tasks. Bossku and no pack both passed 32. One task of 34 is 3 points, and no difference here is clear.
- **The cost: Bossku costs more per run.** About 40% more per run than no pack (+38% on the memory tasks, +42% on coding). ECC cost the most (+80% to +90%). Karpathy's guidelines and Anthropic's skills cost about the same as no pack.
- **Why the memory gap is not a surprise.** Superpowers, Karpathy's guidelines and Anthropic's skills do not claim to carry rules between sessions. ECC does have session memory, but its hooks failed to start in this setup (see "ECC's hooks did not run"). So this run shows that Bossku's notes help where the others have nothing running. It does not show Bossku beating a working memory feature from another pack, or Claude Code's own memory.

## Results

Each task ran once per setup and model. "Both" adds the two models. The interval is a 95% Wilson interval.

### Remembering a rule from an earlier session (22 tasks per model)

Session 1 asks for a small change and states a project rule. Session 2 is a fresh conversation in the same folder that asks for work which breaks the rule unless it is remembered. Hidden tests check the work and the rule.

| Setup | Claude Haiku 4.5 | Claude Sonnet 5.5 | Both | 95% interval | Bossku-only passes vs this setup's only passes | Exact p |
|---|---|---|---|---|---|---|
| **Bossku** | **14** | **19** | **33 of 44 (75%)** | 61% to 85% | | |
| No pack | 8 | 15 | 23 of 44 (52%) | 38% to 66% | 11 vs 1 | 0.006 |
| ECC | 9 | 13 | 22 of 44 (50%) | 36% to 64% | 11 vs 0 | 0.001 |
| Anthropic skills | 8 | 14 | 22 of 44 (50%) | 36% to 64% | 13 vs 2 | 0.007 |
| Superpowers | 7 | 13 | 20 of 44 (45%) | 32% to 60% | 14 vs 1 | 0.001 |
| Karpathy guidelines | 8 | 12 | 20 of 44 (45%) | 32% to 60% | 13 vs 0 | 0.0002 |

The exact p is a two-sided exact binomial test on the tasks where only one of the two setups passed (McNemar). Five comparisons were made; all five stay under 0.01, which is what a Bonferroni correction for five tests asks for at the usual 0.05 level.

Per model the picture is the same, with smaller samples. Haiku: Bossku 14 of 22 against 8 for no pack (7 vs 1 on split tasks, p = 0.07). Sonnet: Bossku 19 of 22 against 15 (4 vs 0, p = 0.13). With Sonnet, Bossku did not fail a single task that any other setup passed.

How often Bossku's first session saved a note: Haiku in 9 of 22 tasks, Sonnet in 20 of 22. When Haiku saved one it passed 8 of 9; when it did not, 6 of 13.

### Coding tasks (17 tasks per model)

| Setup | Claude Haiku 4.5 | Claude Sonnet 5.5 | Both |
|---|---|---|---|
| Bossku | 16 | 16 | 32 of 34 (94%) |
| No pack | 16 | 16 | 32 of 34 (94%) |
| Anthropic skills | 16 | 16 | 32 of 34 (94%) |
| Superpowers | 15 | 16 | 31 of 34 (91%) |
| ECC | 16 | 15 | 31 of 34 (91%) |
| Karpathy guidelines | 15 | 16 | 31 of 34 (91%) |

No setup passed a coding task that no pack failed. Both Claude models already pass nearly everything here, so there was little room to gain.

### Cost and tokens per run

Cost is Claude Code's own figure for the session that was graded. For the memory tasks it leaves out session 1, so Bossku's extra cost of saving a note in session 1 is not in these numbers.

| Setup | Memory: $ per run | vs no pack | Coding: $ per run | vs no pack | Tokens per run vs no pack (memory / coding) |
|---|---|---|---|---|---|
| No pack | 0.059 | | 0.062 | | |
| Bossku | 0.082 | +38% | 0.087 | +42% | +30% / +43% |
| Superpowers | 0.067 | +13% | 0.078 | +26% | +1% / +13% |
| ECC | 0.112 | +90% | 0.111 | +80% | +39% / +31% |
| Karpathy guidelines | 0.058 | -3% | 0.064 | +4% | -3% / -1% |
| Anthropic skills | 0.063 | +6% | 0.065 | +6% | -3% / -5% |

The task sessions in this run cost $35.23 in all ($37.47 with the warm-up and self-test calls).

### What each setup loaded

| Setup | Skills at session start | Runs where the agent opened a skill |
|---|---|---|
| No pack | 21 (Claude Code's built-in) | 0 of 78 |
| Bossku | 49 | 21 of 78 (mostly `bosskuai-security-gate`) |
| Superpowers | 36 | 0 of 78 |
| ECC | 335 | 0 of 78 |
| Karpathy guidelines | 22 | 0 of 78 |
| Anthropic skills | 37 | 0 of 78 |

"Opened" means the Skill tool or a read of a `SKILL.md`. Superpowers also puts its `using-superpowers` guide into every session through a start-up hook, which does not count as opening a skill. A spot check (coding task `conc-01`, Haiku) confirmed that hook ran.

## What was run

- **Date and tools.** 29 October 2026, 04:41 to 07:48 UTC. Claude Code 2.1.310 in headless mode on Windows 11, Node.js 26.8.1. Models: Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) and Claude Sonnet 5.5 (`claude-sonnet-5-5`), on the author's own Claude login.
- **Tasks.** The 10 tasks in `benchmarks/tasks/memory`, the 12 in `benchmarks/tasks/memory-rules` and the 17 coding tasks in `benchmarks/tasks/test`. One trial each, 468 graded runs.
- **Setups and versions.**

| Setup | In the rows | What was loaded |
|---|---|---|
| No pack | `baseline` | Claude Code as installed, nothing added. |
| Bossku | `bossku` | Commit `d93b529`, `lean` profile with the skill hint, the session brief and the Node hooks (`.@lean+hint+brief+harness`). Auto-learn's 50-call reminder was not part of this setup. |
| Superpowers | `superpowers` | [obra/superpowers](https://github.com/obra/superpowers) at `2ce8aa1` (v7.0.1), as shipped. |
| ECC | `ecc` | [affaan-m/ECC](https://github.com/affaan-m/ECC) at `25278e7` (v2.2.3), with the sandbox change below. |
| Karpathy guidelines | `karpathy` | [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) at `2c60614`, as a plugin skill. |
| Anthropic skills | `anthropic` | [anthropics/skills](https://github.com/anthropics/skills) at `ca45fc4`: the `document-skills` and `example-skills` plugins from its marketplace file, with one change below. |

The four other packs were loaded with `claude --plugin-dir`, the same files a `/plugin install` would add (`NAME=pack:DIR` in [`scripts/benchmark_agent.py`](../../scripts/benchmark_agent.py)). Their hooks were read before the run and ran as shipped, apart from the two changes listed next.

## Read this before you trust the numbers

- **Built-in memory was off for every setup.** Every run switches off all `CLAUDE.md` files and Claude Code's own auto memory, so no setup could pass by writing a `CLAUDE.md`. That keeps the comparison clean, but it also means Claude Code's own memory was not tested, and nor was Karpathy's main install path, which is a `CLAUDE.md` file. A rule you write in `CLAUDE.md` yourself may do as well as Bossku's notes. That was not measured.
- **ECC's hooks did not run.** In every ECC session, each hook stopped at once with a Node.js syntax error, before doing anything. The same command copied unchanged from ECC's `hooks/hooks.json` fails the same way inside Claude Code on this machine, so the benchmark's change did not cause it. The hook scripts also need ECC's npm packages (`js-yaml` and others), which a plugin install does not add. ECC's own README lists native Windows as "Supported with limitations". So the ECC column measures ECC's skills, agents and commands without its hooks, and without its session memory. On Linux or macOS ECC's hooks may well run and its memory result may differ.
- **The tasks are Bossku's own.** They live in this repository and were written for Bossku's benchmarks, by AI assistants that were told not to open Bossku's skills, code or documents. They test the kind of help Bossku was built for. They are not a neutral, general score for any pack.
- **Small samples.** One trial per task, 22 memory tasks and 17 coding tasks per model. One memory task is 2 to 5 points. The pooled memory result is clear (p ≤ 0.007 against every other setup); the per-model results are not on their own.
- **One machine, one operating system.** Windows only. Packs whose hooks need Bash or Linux tools are at a disadvantage here, as the ECC result shows.

### Sandbox changes to the other packs

- **ECC.** Its hooks read and write the real `~/.claude` folder (session files, metrics) and one of them can start a nested `claude -p` call. Each hook command was wrapped with a small Node preload that points `CLAUDE_CONFIG_DIR`, `HOME` and `USERPROFILE` at a throwaway folder per run and sets `ECC_SKIP_LLM_SUMMARY=1`. The two sessions of a memory task shared that folder. ECC only calls its summary model when context is under 20% or every 50 messages, which these short sessions never reach. As it turned out the hooks did not start at all (see above).
- **Anthropic skills.** `skill-creator/scripts/` was removed, because its scripts start nested `claude -p` runs on the real login.
- **Isolation check.** Before each suite a canary run confirmed the no-pack setup saw no instructions. Afterwards, the real `~/.claude` folder had no new files except Claude Code's own session records and two empty folders Claude Code made for the plugins (`plugins/data/ecc-inline`, `plugins/data/superpowers-inline`).

## Recompute it

```bash
python scripts/benchmark_agent.py report benchmarks/results/raw/2026-10-29-packs/memory-claude-*.jsonl benchmarks/results/raw/2026-10-29-packs/memory-rules-*.jsonl
python scripts/benchmark_agent.py report benchmarks/results/raw/2026-10-29-packs/coding-*.jsonl
```

The harness command that produced the rows, once per model and suite:

```bash
python scripts/benchmark_agent.py run --suite benchmarks/tasks/memory --model claude-sonnet-5-5 \
  --arm baseline --arm "bossku=.@lean+hint+brief+harness" \
  --arm "superpowers=pack:PACKS/superpowers" --arm "ecc=pack:PACKS/ecc-bench" --arm "karpathy=pack:PACKS/karpathy" \
  --arm "anthropic=pack:PACKS/anthropic-plugins/document-skills,PACKS/anthropic-plugins/example-skills" \
  --parallel 4 --out OUT
```
