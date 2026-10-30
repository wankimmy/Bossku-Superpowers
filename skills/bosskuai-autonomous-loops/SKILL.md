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
| [BosskuAI Agent-Contract Loop](#2-bosskuai-agent-contract-loop) | Low | The default: the planner, executor and auditor contracts in any host |
| [Sequential Pipeline](reference.md#1-sequential-pipeline-claude--p) | Low | Daily dev steps, scripted workflows |
| [Infinite Agentic Loop](reference.md#3-infinite-agentic-loop) | Medium | Parallel content generation, spec-driven work |
| [Continuous Claude PR Loop](reference.md#4-continuous-claude-pr-loop) | Medium | Multi-day iterative projects with CI gates |
| [De-Sloppify Pattern](reference.md#5-the-de-sloppify-pattern) | Add-on | Quality cleanup after any Implementer step |
| [Ralphinho / RFC-Driven DAG](reference.md#6-ralphinho--rfc-driven-dag-orchestration) | High | Large features, multi-unit parallel work with merge queue |

Pattern 2 is below. The other five, with their scripts, configuration and design principles, are in [`reference.md`](reference.md): open only the pattern you chose.

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

- **Bounds on every external call:** a timeout, a retry cap, and a cheaper or safe fallback. No open-ended retry loop. Retry only a call that is safe to repeat, such as a read or a write with an idempotency key.
- **Spend limit:** a max cost per run, and an estimated cost for the primary and fallback paths when the loop calls a paid model or API.
- **Circuit breaker:** on a traffic spike or a run of 402/429 errors, stop calling that endpoint, switch to the fallback, and alert a human.
- **Score before you shadow-test:** when trying a new model or prompt on real traffic, run it in the background (a small sample) so it cannot affect production, and fix the scoring criteria in numbers first. Do not grade by feel afterwards.
- **Decide whether to automate at all:** weigh time saved per month, how critical the data is, how many external services are in the chain, and whether retries and rate limits still hold at 100x volume. A valid outcome is automate only the safe segments, pilot first, or defer.
- **Reliability baseline:** an explicit error branch, duplicate protection, safe retries with a stop condition, a timeout, an alert, and a manual fallback.
- **Log each run:** workflow name and version, time, source system, affected entity id, success or failure, and error class with a short cause. Mask personal data in any logged prompt or response.
- **Test before trusting it:** happy path, invalid input, dependency failure, duplicate event, and recovery.
- **Re-audit** when an API or schema changes, the error rate rises, volume jumps, or the same manual fix keeps recurring. Re-audit does not mean touching production on its own.
- **No change to critical production flows** without explicit approval.
- **Versions:** read the model id and the CLI or SDK version the loop runs from its config and lockfile. Re-check the provider's live model list before each scheduled run, since a retired id stops the run.
- **No overlapping runs:** a run still going when the next one fires must not start a second copy on the same item. Take a lock or check the item's state first.
- **Data writes:** test a loop that changes data on a production data copy first, and compare its counts with the expected result. Write in small batches. Each batch runs in one transaction (START TRANSACTION ... COMMIT), so a stop halfway leaves no half-written batch. Batches that already committed stay applied, so a rerun must skip them: record which items are done in the same transaction as their change, or make each batch safe to run again.

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
- `../../references/checklists/engineering-quality-bar.md` — the shared bar that loops and their runs are checked against.

The orchestrator contract (`agents/orchestrator.md`, Autonomous run flow) drives these patterns end-to-end.

## References

| Project | Author | Link |
|---------|--------|------|
| Ralphinho | enitrat | credit: @enitrat |
| Infinite Agentic Loop | disler | credit: @disler |
| Continuous Claude | AnandChowdhary | credit: @AnandChowdhary |
| Autonomous Loops (upstream) | affaan-m/ECC | `skills/autonomous-loops/` |

Unattended-loop guardrails adapted in part from engineering/engineering-autonomous-optimization-architect.md and specialized/automation-governance-architect.md (agency-agents, MIT).
