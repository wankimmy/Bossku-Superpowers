---
name: bosskuai-subagent-delegation
description: Use when independent workstreams, context-heavy research, or a separate review benefit from subagents; select supported host tools, bounded tasks, and safe write scopes.
---

# Subagent delegation

Use when splitting work across agents beats running it serially: independent workstreams, context-heavy research, or a review that should test assumptions separately.

1. **Check it's worth it.** Delegate for two or more genuinely independent workstreams, research where only the conclusion needs to return, or a review that benefits from distance — not a single linear task.
2. **Inspect what the host actually supports** — exposed agent tools, concurrency limits, context inheritance — before assuming a field or mode exists. Use the inherited model unless the task clearly justifies an override.
3. **Write each task so the agent never needs to ask back**: a concrete goal, exact paths, read-only or write scope, constraints, the success check, and a bounded turn/time/retry budget.
4. **Give every writer exclusive ownership** of its files or a worktree; serialize anything shared. A worktree does not isolate credentials, databases, or external services — treat those as shared regardless.
5. **Name the skills and files each task needs explicitly** — a child does not inherit the parent's skill selection or context by default.
6. **Run independent tasks in parallel or background; wait for a dependency before starting the step that needs it.** If the host has no delegation support, say so and run the same scoped tasks sequentially instead of silently skipping the split.
7. **Review every returned diff against its own evidence**, not just the subagent's summary, and run the relevant integration check before accepting it.

Check before you finish: no two writers touched the same file concurrently, nothing started before a dependency it needed had returned, and every task had enough context to run with nobody able to answer a follow-up.

Host-specific patterns (Claude Code, Cursor, Codex, OpenCode/OMP) and the delegation-plan template: `reference.md`.

## Lane matrix, context retrieval and merge gates

- Before a large fan-out, write a lane matrix: lane, parallel/sequential/gated, write surface, risk, verification. Run lanes in parallel only when their write surfaces do not collide; if a lane finds a blocker that changes the plan, pause its dependents and update the matrix.
- Never parallelize destructive commands, migrations, writes to the same table, or customer-impacting deploys without an explicit gate. Start long builds and tests as separate sessions and poll them deliberately; nothing should outlive the turn unless the user asked for it.
- When a child cannot know what context it needs, give it a bounded retrieval loop: broad keyword/path search, score each hit for relevance and list missing context, refine terms (the codebase may use different vocabulary, e.g. "throttle" for "rate limit"), and stop after 3 cycles or once a few clearly relevant files are found. A few high-relevance files beat many mediocre ones.
- Treat each agent as a teammate with an owner, a scope (files, branch, forbidden areas), a state (ready, running, review, blocked, merged), evidence (tests, logs, screenshots) and one exact merge gate. Move a card to review only when its handoff artifact and changed files exist.
- Review order before merge: tests, diff review, risk/security check, then polish. One integrator resolves conflicts.
- Failure modes: many agents with no owner or merge gate, useful output that lives only in a chat transcript, a task board whose cards have no acceptance criteria, overlapping writes without worktrees, and reporting "fast" before correctness is proven.
- Finish with a verification table: lanes run and completed, blocked lane with owner and next action, checks run, checks skipped (never hidden behind a success summary).

Adapted in part from ECC skills/iterative-retrieval, skills/parallel-execution-optimizer and skills/team-agent-orchestration (affaan-m/ECC, MIT).
