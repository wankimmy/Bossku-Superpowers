---
name: bosskuai-autonomous-loops
description: "Use when designing agent loop structure, from sequential pipelines to RFC-driven DAGs: exit conditions, context bridging, merge coordination. Discipline inside an iteration belongs to the loop-family skills."
license: MIT
metadata:
  author: affaan-m/ECC
  source: autonomous-loops
---

# Autonomous Loops Skill

Patterns, architectures, and reference implementations for running coding agents autonomously in loops. Covers everything from simple `claude -p` pipelines to full RFC-driven multi-agent DAG orchestration.

## When to Use

- Setting up autonomous development workflows that run without human intervention
- Choosing the right loop architecture for your problem (simple vs complex)
- Building CI/CD-style continuous development pipelines
- Running parallel agents with merge coordination
- Implementing context persistence across loop iterations
- Adding quality gates and cleanup passes to autonomous workflows

## Loop Pattern Spectrum

From simplest to most sophisticated:

| Pattern | Complexity | Best For |
|---------|-----------|----------|
| [Sequential Pipeline](#1-sequential-pipeline-claude--p) | Low | Daily dev steps, scripted workflows |
| [Infinite Agentic Loop](#3-infinite-agentic-loop) | Medium | Parallel content generation, spec-driven work |
| [Continuous Claude PR Loop](#4-continuous-claude-pr-loop) | Medium | Multi-day iterative projects with CI gates |
| [De-Sloppify Pattern](#5-the-de-sloppify-pattern) | Add-on | Quality cleanup after any Implementer step |
| [Ralphinho / RFC-Driven DAG](#6-ralphinho--rfc-driven-dag-orchestration) | High | Large features, multi-unit parallel work with merge queue |

---

## 1. Sequential Pipeline (`claude -p`)

**The simplest loop.** Break daily development into a sequence of non-interactive `claude -p` calls. Each call is a focused step with a clear prompt.

### Core Insight

> If you can't figure out a loop like this, it means you can't even drive the LLM to fix your code in interactive mode.

The `claude -p` flag runs Claude Code non-interactively with a prompt, exits when done. Chain calls to build a pipeline:

```bash
#!/bin/bash
# daily-dev.sh — Sequential pipeline for a feature branch

set -e

# Step 1: Implement the feature
claude -p "Read the spec in docs/auth-spec.md. Implement OAuth2 login in src/auth/. Write tests first (TDD). Do NOT create any new documentation files."

# Step 2: De-sloppify (cleanup pass)
claude -p "Review all files changed by the previous commit. Remove any unnecessary type tests, overly defensive checks, or testing of language features (e.g., testing that TypeScript generics work). Keep real business logic tests. Run the test suite after cleanup."

# Step 3: Verify
claude -p "Run the full build, lint, type check, and test suite. Fix any failures. Do not add new features."

# Step 4: Commit
claude -p "Create a conventional commit for all staged changes. Use 'feat: add OAuth2 login flow' as the message."
```

### Key Design Principles

1. **Each step is isolated** — A fresh context window per `claude -p` call means no context bleed between steps.
2. **Order matters** — Steps execute sequentially. Each builds on the filesystem state left by the previous.
3. **Negative instructions are dangerous** — Don't say "don't test type systems." Instead, add a separate cleanup step (see [De-Sloppify Pattern](#5-the-de-sloppify-pattern)).
4. **Exit codes propagate** — `set -e` stops the pipeline on failure.

### Variations

**With model routing:**
```bash
# Research with Opus (deep reasoning)
claude -p --model opus "Analyze the codebase architecture and write a plan for adding caching..."

# Implement with Sonnet (fast, capable)
claude -p "Implement the caching layer according to the plan in docs/caching-plan.md..."

# Review with Opus (thorough)
claude -p --model opus "Review all changes for security issues, race conditions, and edge cases..."
```

**With environment context:**
```bash
# Pass context via files, not prompt length
echo "Focus areas: auth module, API rate limiting" > .claude-context.md
claude -p "Read .claude-context.md for priorities. Work through them in order."
rm .claude-context.md
```

**With `--allowedTools` restrictions:**
```bash
# Read-only analysis pass
claude -p --allowedTools "Read,Grep,Glob" "Audit this codebase for security vulnerabilities..."

# Write-only implementation pass
claude -p --allowedTools "Read,Write,Edit,Bash" "Implement the fixes from security-audit.md..."
```

---

## 2. BosskuAI Agent-Contract Loop

**The built-in loop.** BosskuAI 2.x has no runtime service; the loop is the
chain of agent contracts in `agents/*.md`, driven by whichever host is running
the session. The orchestrator scopes the work and hands the executor a *closed*
loop: a pass signal, a loop owner, and a max-iteration budget.

```
orchestrator restates goal, success criteria, out-of-scope
       │
       ▼
planner (strategy, file list, phases) → designer (UI work only)
       │
       ▼
┌─ REVISE LOOP (capped by the budget set up front) ──────────────┐
│ executor implements → auditor reviews                          │
│   ├─ PASS   → de-sloppify → final-reviewer (high-risk only)    │
│   ├─ REVISE → executor retries with the audit feedback         │
│   └─ cap reached → escalate; never report "capped" as "pass"   │
└────────────────────────────────────────────────────────────────┘
       │
       ▼
learning capture is manual: `bossku remember` via `bosskuai-continuous-learning`
```

### Tuning the loop

- **Loop owner by task shape** (from the orchestrator contract): bug →
  `bosskuai-diagnose-loop`; behavior change → `bosskuai-tdd-loop`; PR/review →
  `bosskuai-greptile-review-loop`; performance → `bosskuai-ratchet-loop`.
- **Budget before handoff.** State the pass signal and max iterations in the
  executor brief. One retry is the sane default for attended runs; raise it for
  unattended runs so REVISE verdicts actually loop.
- Each role's persona is the full body of its `agents/*.md` file. Keep them compact — loop depth multiplies persona cost
  (`bosskuai-context-budget` measures it).
- Watch for degraded iterations: a fallback model returning a near-empty
  response can pass as "Completed". Use `bosskuai-agent-introspection` when a
  loop completes suspiciously fast or empty.

### When contract chain vs editor-side loop

| Use Case | Agent-contract chain (in-session) | Editor-side loop (`claude -p`, scripts) |
|----------|-----------------------------------|------------------------------------------|
| Interactive task with a human in the loop | Yes | No |
| Scripted multi-step workflows | No | Yes |
| Custom loop architecture (DAG, waves) | No | Yes |
| Learning capture | Manual (`bossku remember`) | Manual (`bossku remember` as a final step) |

---

## 3. Infinite Agentic Loop

**A two-prompt system** that orchestrates parallel sub-agents for specification-driven generation. Developed by disler (credit: @disler).

### Architecture: Two-Prompt System

```
PROMPT 1 (Orchestrator)              PROMPT 2 (Sub-Agents)
┌─────────────────────┐             ┌──────────────────────┐
│ Parse spec file      │             │ Receive full context  │
│ Scan output dir      │  deploys   │ Read assigned number  │
│ Plan iteration       │────────────│ Follow spec exactly   │
│ Assign creative dirs │  N agents  │ Generate unique output │
│ Manage waves         │             │ Save to output dir    │
└─────────────────────┘             └──────────────────────┘
```

### The Pattern

1. **Spec Analysis** — Orchestrator reads a specification file (Markdown) defining what to generate
2. **Directory Recon** — Scans existing output to find the highest iteration number
3. **Parallel Deployment** — Launches N sub-agents, each with:
   - The full spec
   - A unique creative direction
   - A specific iteration number (no conflicts)
   - A snapshot of existing iterations (for uniqueness)
4. **Wave Management** — For infinite mode, deploys waves of 3-5 agents until context is exhausted

### Implementation via Claude Code Commands

Create `.claude/commands/infinite.md`:

```markdown
Parse the following arguments from $ARGUMENTS:
1. spec_file — path to the specification markdown
2. output_dir — where iterations are saved
3. count — integer 1-N or "infinite"

PHASE 1: Read and deeply understand the specification.
PHASE 2: List output_dir, find highest iteration number. Start at N+1.
PHASE 3: Plan creative directions — each agent gets a DIFFERENT theme/approach.
PHASE 4: Deploy sub-agents in parallel (Task tool). Each receives:
  - Full spec text
  - Current directory snapshot
  - Their assigned iteration number
  - Their unique creative direction
PHASE 5 (infinite mode): Loop in waves of 3-5 until context is low.
```

**Invoke:**
```bash
/infinite specs/component-spec.md src/ 5
/infinite specs/component-spec.md src/ infinite
```

### Batching Strategy

| Count | Strategy |
|-------|----------|
| 1-5 | All agents simultaneously |
| 6-20 | Batches of 5 |
| infinite | Waves of 3-5, progressive sophistication |

### Key Insight: Uniqueness via Assignment

Don't rely on agents to self-differentiate. The orchestrator **assigns** each agent a specific creative direction and iteration number. This prevents duplicate concepts across parallel agents.

---

## 4. Continuous Claude PR Loop

**A production-grade shell script** that runs Claude Code in a continuous loop, creating PRs, waiting for CI, and merging automatically. Created by AnandChowdhary (credit: @AnandChowdhary).

### Core Loop

```
┌─────────────────────────────────────────────────────┐
│  CONTINUOUS CLAUDE ITERATION                        │
│                                                     │
│  1. Create branch (continuous-claude/iteration-N)   │
│  2. Run claude -p with enhanced prompt              │
│  3. (Optional) Reviewer pass — separate claude -p   │
│  4. Commit changes (claude generates message)       │
│  5. Push + create PR (gh pr create)                 │
│  6. Wait for CI checks (poll gh pr checks)          │
│  7. CI failure? → Auto-fix pass (claude -p)         │
│  8. Merge PR (squash/merge/rebase)                  │
│  9. Return to main → repeat                         │
│                                                     │
│  Limit by: --max-runs N | --max-cost $X             │
│            --max-duration 2h | completion signal     │
└─────────────────────────────────────────────────────┘
```

### Installation

> **Warning:** Install continuous-claude from its repository after reviewing the code. Do not pipe external scripts directly to bash.

### Usage

```bash
# Basic: 10 iterations
continuous-claude --prompt "Add unit tests for all untested functions" --max-runs 10

# Cost-limited
continuous-claude --prompt "Fix all linter errors" --max-cost 5.00

# Time-boxed
continuous-claude --prompt "Improve test coverage" --max-duration 8h

# With code review pass
continuous-claude \
  --prompt "Add authentication feature" \
  --max-runs 10 \
  --review-prompt "Run npm test && npm run lint, fix any failures"

# Parallel via worktrees
continuous-claude --prompt "Add tests" --max-runs 5 --worktree tests-worker &
continuous-claude --prompt "Refactor code" --max-runs 5 --worktree refactor-worker &
wait
```

### Cross-Iteration Context: SHARED_TASK_NOTES.md

The critical innovation: a `SHARED_TASK_NOTES.md` file persists across iterations:

```markdown
## Progress
- [x] Added tests for auth module (iteration 1)
- [x] Fixed edge case in token refresh (iteration 2)
- [ ] Still need: rate limiting tests, error boundary tests

## Next Steps
- Focus on rate limiting module next
- The mock setup in tests/helpers.ts can be reused
```

Claude reads this file at iteration start and updates it at iteration end. This bridges the context gap between independent `claude -p` invocations.

### CI Failure Recovery

When PR checks fail, Continuous Claude automatically:
1. Fetches the failed run ID via `gh run list`
2. Spawns a new `claude -p` with CI fix context
3. Claude inspects logs via `gh run view`, fixes code, commits, pushes
4. Re-waits for checks (up to `--ci-retry-max` attempts)

### Completion Signal

Claude can signal "I'm done" by outputting a magic phrase:

```bash
continuous-claude \
  --prompt "Fix all bugs in the issue tracker" \
  --completion-signal "CONTINUOUS_CLAUDE_PROJECT_COMPLETE" \
  --completion-threshold 3  # Stops after 3 consecutive signals
```

Three consecutive iterations signaling completion stops the loop, preventing wasted runs on finished work.

### Key Configuration

| Flag | Purpose |
|------|---------|
| `--max-runs N` | Stop after N successful iterations |
| `--max-cost $X` | Stop after spending $X |
| `--max-duration 2h` | Stop after time elapsed |
| `--merge-strategy squash` | squash, merge, or rebase |
| `--worktree <name>` | Parallel execution via git worktrees |
| `--disable-commits` | Dry-run mode (no git operations) |
| `--review-prompt "..."` | Add reviewer pass per iteration |
| `--ci-retry-max N` | Auto-fix CI failures (default: 1) |

---

## 5. The De-Sloppify Pattern

**An add-on pattern for any loop.** Add a dedicated cleanup/refactor step after each Implementer step.

### The Problem

When you ask an LLM to implement with TDD, it takes "write tests" too literally:
- Tests that verify TypeScript's type system works (testing `typeof x === 'string'`)
- Overly defensive runtime checks for things the type system already guarantees
- Tests for framework behavior rather than business logic
- Excessive error handling that obscures the actual code

### Why Not Negative Instructions?

Adding "don't test type systems" or "don't add unnecessary checks" to the Implementer prompt has downstream effects:
- The model becomes hesitant about ALL testing
- It skips legitimate edge case tests
- Quality degrades unpredictably

### The Solution: Separate Pass

Instead of constraining the Implementer, let it be thorough. Then add a focused cleanup agent:

```bash
# Step 1: Implement (let it be thorough)
claude -p "Implement the feature with full TDD. Be thorough with tests."

# Step 2: De-sloppify (separate context, focused cleanup)
claude -p "Review all changes in the working tree. Remove:
- Tests that verify language/framework behavior rather than business logic
- Redundant type checks that the type system already enforces
- Over-defensive error handling for impossible states
- Console.log statements
- Commented-out code

Keep all business logic tests. Run the test suite after cleanup to ensure nothing breaks."
```

### In a Loop Context

```bash
for feature in "${features[@]}"; do
  # Implement
  claude -p "Implement $feature with TDD."

  # De-sloppify
  claude -p "Cleanup pass: review changes, remove test/code slop, run tests."

  # Verify
  claude -p "Run build + lint + tests. Fix any failures."

  # Commit
  claude -p "Commit with message: feat: add $feature"
done
```

### Key Insight

> Rather than adding negative instructions which have downstream quality effects, add a separate de-sloppify pass. Two focused agents outperform one constrained agent.

---

## 6. Ralphinho / RFC-Driven DAG Orchestration

**The most sophisticated pattern.** An RFC-driven, multi-agent pipeline that decomposes a spec into a dependency DAG, runs each unit through a tiered quality pipeline, and lands them via an agent-driven merge queue. Created by enitrat (credit: @enitrat).

### Architecture Overview

```
RFC/PRD Document
       │
       ▼
  DECOMPOSITION (AI)
  Break RFC into work units with dependency DAG
       │
       ▼
┌──────────────────────────────────────────────────────┐
│  RALPH LOOP (up to 3 passes)                         │
│                                                      │
│  For each DAG layer (sequential, by dependency):     │
│                                                      │
│  ┌── Quality Pipelines (parallel per unit) ───────┐  │
│  │  Each unit in its own worktree:                │  │
│  │  Research → Plan → Implement → Test → Review   │  │
│  │  (depth varies by complexity tier)             │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ┌── Merge Queue ─────────────────────────────────┐  │
│  │  Rebase onto main → Run tests → Land or evict │  │
│  │  Evicted units re-enter with conflict context  │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### RFC Decomposition

AI reads the RFC and produces work units:

```typescript
interface WorkUnit {
  id: string;              // kebab-case identifier
  name: string;            // Human-readable name
  rfcSections: string[];   // Which RFC sections this addresses
  description: string;     // Detailed description
  deps: string[];          // Dependencies (other unit IDs)
  acceptance: string[];    // Concrete acceptance criteria
  tier: "trivial" | "small" | "medium" | "large";
}
```

**Decomposition Rules:**
- Prefer fewer, cohesive units (minimize merge risk)
- Minimize cross-unit file overlap (avoid conflicts)
- Keep tests WITH implementation (never separate "implement X" + "test X")
- Dependencies only where real code dependency exists

The dependency DAG determines execution order:
```
Layer 0: [unit-a, unit-b]     ← no deps, run in parallel
Layer 1: [unit-c]             ← depends on unit-a
Layer 2: [unit-d, unit-e]     ← depend on unit-c
```

### Complexity Tiers

Different tiers get different pipeline depths:

| Tier | Pipeline Stages |
|------|----------------|
| **trivial** | implement → test |
| **small** | implement → test → code-review |
| **medium** | research → plan → implement → test → PRD-review + code-review → review-fix |
| **large** | research → plan → implement → test → PRD-review + code-review → review-fix → final-review |

This prevents expensive operations on simple changes while ensuring architectural changes get thorough scrutiny.

### Separate Context Windows (Author-Bias Elimination)

Each stage runs in its own agent process with its own context window:

| Stage | Model | Purpose |
|-------|-------|---------|
| Research | Sonnet | Read codebase + RFC, produce context doc |
| Plan | Opus | Design implementation steps |
| Implement | Codex | Write code following the plan |
| Test | Sonnet | Run build + test suite |
| PRD Review | Sonnet | Spec compliance check |
| Code Review | Opus | Quality + security check |
| Review Fix | Codex | Address review issues |
| Final Review | Opus | Quality gate (large tier only) |

**Critical design:** The reviewer never wrote the code it reviews. This eliminates author bias — the most common source of missed issues in self-review.

### Merge Queue with Eviction

After quality pipelines complete, units enter the merge queue:

```
Unit branch
    │
    ├─ Rebase onto main
    │   └─ Conflict? → EVICT (capture conflict context)
    │
    ├─ Run build + tests
    │   └─ Fail? → EVICT (capture test output)
    │
    └─ Pass → Fast-forward main, push, delete branch
```

**File Overlap Intelligence:**
- Non-overlapping units land speculatively in parallel
- Overlapping units land one-by-one, rebasing each time

**Eviction Recovery:**
When evicted, full context is captured (conflicting files, diffs, test output) and fed back to the implementer on the next Ralph pass:

```markdown
## MERGE CONFLICT — RESOLVE BEFORE NEXT LANDING

Your previous implementation conflicted with another unit that landed first.
Restructure your changes to avoid the conflicting files/lines below.

{full eviction context with diffs}
```

### Data Flow Between Stages

```
research.contextFilePath ──────────────────→ plan
plan.implementationSteps ──────────────────→ implement
implement.{filesCreated, whatWasDone} ─────→ test, reviews
test.failingSummary ───────────────────────→ reviews, implement (next pass)
reviews.{feedback, issues} ────────────────→ review-fix → implement (next pass)
final-review.reasoning ────────────────────→ implement (next pass)
evictionContext ───────────────────────────→ implement (after merge conflict)
```

### Worktree Isolation

Every unit runs in an isolated worktree (uses jj/Jujutsu, not git):
```
/tmp/workflow-wt-{unit-id}/
```

Pipeline stages for the same unit **share** a worktree, preserving state (context files, plan files, code changes) across research → plan → implement → test → review.

### Key Design Principles

1. **Deterministic execution** — Upfront decomposition locks in parallelism and ordering
2. **Human review at leverage points** — The work plan is the single highest-leverage intervention point
3. **Separate concerns** — Each stage in a separate context window with a separate agent
4. **Conflict recovery with context** — Full eviction context enables intelligent re-runs, not blind retries
5. **Tier-driven depth** — Trivial changes skip research/review; large changes get maximum scrutiny
6. **Resumable workflows** — Full state persisted to SQLite; resume from any point

### When to Use Ralphinho vs Simpler Patterns

| Signal | Use Ralphinho | Use Simpler Pattern |
|--------|--------------|-------------------|
| Multiple interdependent work units | Yes | No |
| Need parallel implementation | Yes | No |
| Merge conflicts likely | Yes | No (sequential is fine) |
| Single-file change | No | Yes (sequential pipeline) |
| Multi-day project | Yes | Maybe (continuous-claude) |
| Spec/RFC already written | Yes | Maybe |
| Quick iteration on one thing | No | Yes (sequential pipeline) |

---

## Choosing the Right Pattern

### Decision Matrix

```
Is the task a single focused change?
├─ Yes → Sequential Pipeline (or just do it interactively)
└─ No → Is there a written spec/RFC?
         ├─ Yes → Do you need parallel implementation?
         │        ├─ Yes → Ralphinho (DAG orchestration)
         │        └─ No → Continuous Claude (iterative PR loop)
         └─ No → Do you need many variations of the same thing?
                  ├─ Yes → Infinite Agentic Loop (spec-driven generation)
                  └─ No → Sequential Pipeline with de-sloppify
```

### Combining Patterns

These patterns compose well:

1. **Sequential Pipeline + De-Sloppify** — The most common combination. Every implement step gets a cleanup pass.

2. **Continuous Claude + De-Sloppify** — Add `--review-prompt` with a de-sloppify directive to each iteration.

3. **Any loop + Verification** — Use the stack's verification gate before commits: `bosskuai-laravel-verification` for Laravel work, or the project's build+lint+test pipeline otherwise.

4. **Ralphinho's tiered approach in simpler loops** — Even in a sequential pipeline, you can route simple tasks to Haiku and complex tasks to Opus:
   ```bash
   # Simple formatting fix
   claude -p --model haiku "Fix the import ordering in src/utils.ts"

   # Complex architectural change
   claude -p --model opus "Refactor the auth module to use the strategy pattern"
   ```

---

## Guardrails for unattended loops

Before a loop runs without a human watching, check each item:

- **Bounds on every external call:** a timeout, a retry cap, and a cheaper or safe fallback. No open-ended retry loop.
- **Spend limit:** a max cost per run, and an estimated cost for the primary and fallback paths when the loop calls a paid model or API.
- **Circuit breaker:** on a traffic spike or a run of 402/429 errors, stop calling that endpoint, switch to the fallback, and alert a human.
- **Score before you shadow-test:** when trying a new model or prompt on real traffic, run it in the background (a small sample) so it cannot affect production, and fix the scoring criteria in numbers first. Do not grade by feel afterwards.
- **Decide whether to automate at all:** weigh time saved per month, how critical the data is, how many external services are in the chain, and whether retries and rate limits still hold at 100x volume. A valid outcome is automate only the safe segments, pilot first, or defer.
- **Reliability baseline:** an explicit error branch, duplicate protection, safe retries with a stop condition, a timeout, an alert, and a manual fallback.
- **Log each run:** workflow name and version, time, source system, affected entity id, success or failure, and error class with a short cause.
- **Test before trusting it:** happy path, invalid input, dependency failure, duplicate event, and recovery.
- **Re-audit** when an API or schema changes, the error rate rises, volume jumps, or the same manual fix keeps recurring. Re-audit does not mean touching production on its own.
- **No change to critical production flows** without explicit approval.

## Designing and reviewing a loop

- **Gate first.** Build a loop only if the task repeats about weekly or more, verification can be automated, the token budget allows it, and the agent has tools that run the code and see the result. Miss one and do it by hand; a repo without tests and a reconciliation baseline only gets its errors amplified.
- **Machine-decidable goal.** Someone outside the domain should be able to run one command and say whether it is done. Write the done-criterion together with a boundary ("must not delete or weaken tests, must not lower coverage"), a retry cap with human escalation, and where possible reconcile against an external fact (golden sample, upstream total, diff under a threshold) instead of "all tests pass".
- **Loop type.** Clear done test: closed loop that stops at the goal. No endpoint, keep a state healthy: a regulator that acts only on change. Watch until a condition: a regulator with an exit. Must happen on time: wrap it in a scheduler.
- **Skeleton.** Maintenance: read a doc on a timer and dispatch only when it changed; humans write the problem column, the loop writes results, state moves one way and stops at "awaiting verification", a human flips "done", and the script's exit code is final. Greenfield: plan (spec plus decidable acceptance), build (may not edit the acceptance), judge (independent and deterministic: tests, diff, type check). Three failed retries means escalate.
- **Land in stages:** run once by hand, then harden into a skill or subagents, then put it on a schedule.
- **Review against five failure modes:** (1) a vague goal spins and burns money; (2) the builder judges its own work and says "looks fine"; (3) a done-criterion with no boundary lets the agent delete the tests; (4) it never asks mid-run, so front-load every clarification before launch; (5) stale instructions and memory make a fast loop err faster.
- **Red lines for automation:** a human owns acceptance and the final switch (open the PR, do not auto-merge); never auto-hand authority for things you cannot afford to get wrong; the more a loop rewrites its own rules, the harder the human gate before the action.
- **Recovery for a stuck loop:** freeze it, cut scope to the failing unit, replay with explicit acceptance criteria. Typical failures: churn with no measurable progress, the same root cause retried, merge queue stalls, cost drift from unbounded escalation.

## Generator and evaluator harness

For quality-critical builds (a full app, a frontend that must not look generic), split generation from evaluation, because an agent grading its own work is too generous.
- Planner expands a short brief into a spec with acceptance criteria; generator builds in sprints and agrees a "sprint contract" with the evaluator first; evaluator tests the running app (browser automation: click, fill forms, hit error states), not only screenshots or code.
- Score a rubric (for example design quality, originality, craft, functionality, each 1-10 with weights) and set a pass threshold and max iterations up front. Pass feedback as `feedback-NNN.md` files the generator reads each round.
- The evaluator only critiques; it never suggests fixes and then grades them. If the first pass scores everything high, the rubric is too lenient. Stop and ask a human if the score plateaus for 3 rounds.
- Every harness part encodes an assumption about what the model cannot do alone; re-test and drop scaffolding (sprints, context resets) as models improve. Expect much higher cost and time than a solo run and use it only where quality justifies that.

## Task-local harnesses and scheduled agents

- Make a task-local harness only when it is cheaper and safer than driving the steps by hand: one-shot tasks stay inline. It needs an objective (what it ships and does not), inputs and credentials policy, outputs, a task-specific pass/fail eval, and a handoff note (status, evidence, next action). Stop on a failed gate, unclear ownership or an unsafe external action.
- Promote it to a shared skill when at least two hold: it recurs across sessions or repos, it needs specific safety sequencing, failures repeat because gates get skipped, it has a stable input and output contract, or it benefits from a team status board. Another person must be able to rerun its eval.
- Cheapest eval by work type: code (focused test, lint, one integration path); UI (browser smoke with screenshot and overflow/error checks); agent workflow (seeded work item with expected routing); research (claim checklist); integration (dry run, config validation, no-secret scan).
- Scheduling and background agents must be explicitly requested and scoped; prefer a dry run and a local queue file first. A `/loop` style prompt lives only as long as its session, so use an OS or CI scheduler for work that must survive. Verify the exact package and version before registering any MCP server (never a guessed name under `npx -y`), and check that each scheduled run actually completed.
- RFC work units also carry `risk_level` and a `rollback_plan`; never merge a unit with unresolved dependency failures, rebase on the latest integration branch, and rerun integration tests after each queued merge.

Adapted in part from ECC skills/autonomous-agent-harness, autonomous-loops, continuous-agent-loop, dynamic-workflow-mode, gan-style-harness, loop-design-check and ralphinho-rfc-pipeline (affaan-m/ECC, MIT).

## Anti-Patterns

### Common Mistakes

1. **Infinite loops without exit conditions** — Always have a max-runs, max-cost, max-duration, or completion signal.

2. **No context bridge between iterations** — Each `claude -p` call starts fresh. Use `SHARED_TASK_NOTES.md` or filesystem state to bridge context.

3. **Retrying the same failure** — If an iteration fails, don't just retry. Capture the error context and feed it to the next attempt.

4. **Negative instructions instead of cleanup passes** — Don't say "don't do X." Add a separate pass that removes X.

5. **All agents in one context window** — For complex workflows, separate concerns into different agent processes. The reviewer should never be the author.

6. **Ignoring file overlap in parallel work** — If two parallel agents might edit the same file, you need a merge strategy (sequential landing, rebase, or conflict resolution).

---

## Related Skills

The loop **architecture** lives here; the discipline **inside** an iteration lives in the loop family:

- `bosskuai-diagnose-loop` — reproduce → hypothesise → instrument → fix for hard bugs
- `bosskuai-tdd-loop` — red → green → refactor per vertical slice
- `bosskuai-ratchet-loop` — metric-driven improvement with a never-regress ratchet
- `bosskuai-greptile-review-loop` / `bosskuai-pr-check` — iterate a PR until review is clean
- `bosskuai-agent-introspection` — when a loop iteration fails, loops on the same tools, or returns empty
- `bosskuai-subagent-delegation` — parallel/worktree execution mechanics for the patterns above
- `bosskuai-handoff` + `bosskuai-context-limit-continuation` — context bridging between sessions (the editor-side equivalent of SHARED_TASK_NOTES.md)

The orchestrator contract (`agents/orchestrator.md`, Autonomous run flow) drives these patterns end-to-end.

## References

| Project | Author | Link |
|---------|--------|------|
| Ralphinho | enitrat | credit: @enitrat |
| Infinite Agentic Loop | disler | credit: @disler |
| Continuous Claude | AnandChowdhary | credit: @AnandChowdhary |
| Autonomous Loops (upstream) | affaan-m/ECC | `skills/autonomous-loops/` |

Unattended-loop guardrails adapted in part from engineering/engineering-autonomous-optimization-architect.md and specialized/automation-governance-architect.md (agency-agents, MIT).
