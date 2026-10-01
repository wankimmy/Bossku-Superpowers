---
name: bosskuai-subagent-delegation
description: Use when independent workstreams, context-heavy research, or a separate review benefit from subagents; select supported host tools, bounded tasks, and safe write scopes.
---

# BosskuAI Subagent Delegation

Use this skill when a task is large enough, parallel enough, or risky enough that splitting it across multiple agents is more effective than running it serially in the main session.

## How this differs from nearby skills

- **`bosskuai-context-limit-continuation`**: stops and hands off to a new serial session when context is nearly exhausted. This skill delegates parallel work before context runs out.
- **`cofounder`**: orchestrates skill selection within one session. **This skill** extends that orchestration to multi-agent execution.
- **`bosskuai-cross-model-escalation`**: brings in another model when the current workstream is blocked or brittle. **This skill** is for parallelizable workstreams, not a single stuck one.

## Delegation signals

Delegate when the benefit exceeds coordination cost and the host supports it:

| Signal | Threshold | Action |
|--------|-----------|--------|
| Parallel workstreams | Two or more independent tasks | Assign one bounded task per agent, within the host's concurrency limit |
| Context-heavy research | Only the conclusion and evidence need to return | Delegate a read-only investigation |
| Risky scope | A separate review can test assumptions | Delegate investigation or review; keep consequential actions with the coordinator and honor existing user authorization |
| Batch operations | Same small edit across N targets | One subagent with the full list, or inline; one subagent per target only when each needs its own judgment or tests |

## Workflow

1. Inspect exposed tools, agent definitions, permissions, context inheritance, and concurrency limits. Use the configured or inherited model unless the task or user justifies an available override.
2. Assign a concrete goal, exact paths, read-only or write scope, constraints, inputs, success check, and an evidence-bearing output. Give each task a bounded turn/time/retry budget using supported controls or explicit stopping instructions.
3. Name the relevant skills and references. Inspect what context the child receives; supply missing evidence explicitly. Preload only needed skill bodies when supported, otherwise tell the agent which files to read. Do not assume the parent's skill selection transfers.
4. Give each writer exclusive file ownership or supported worktree isolation. Serialize shared files, generated outputs, and operations with ordering dependencies. A worktree does not isolate credentials, databases, or remote services.
5. Run independent tasks in the background when supported; await dependent results before continuing. If delegation is unavailable, execute the same scoped tasks sequentially and report that fallback.
6. Review returned diffs and source evidence, run the relevant integration check, and reconcile disagreements. The coordinator performs consequential actions within the user's authorized scope; request approval only for an unresolved boundary.

## Tool-specific patterns

### Claude Code - Agent tool

Inspect the installed `Agent` tool and available agent definitions before choosing a type. Use tool allow/deny lists, `maxTurns`, `skills`, background execution, and `isolation: worktree` only in the supporting tool or agent configuration; their fields are not interchangeable. Claude's agent `skills` list injects full bodies at startup, so keep it narrow. Prefer model inheritance over fixed role-to-model names.

### Cursor - subagents and parallel agents

Use exposed subagent or parallel-agent tools and inspect their context and isolation contracts. When running separate tabs or worktrees, track the owning agent and paths for each task, then review results before integrating.

### Codex - parallel runs

Use the available collaboration/subagent tools and their actual schemas. Inspect whether agents share the checkout and whether history is forked; assign disjoint write scopes when they share files. Use only exposed or configured roles, then collect results and verify the integrated diff.

### OpenCode and OMP

Discover the installed host's agent tools, configuration, and limitations before delegating. Apply the same task, evidence, budget, and write-ownership contract with supported controls; use the sequential fallback when no suitable tool exists. Do not copy another host's frontmatter or role names into these adapters.

## Delegation output format

When delegating, state the plan before launching:

```
Delegating to subagents:

Subagent 1 - [description] ([verified host tool])
  Goal: [what it will do]
  Scope: [files or domains it touches]
  Type: [read-only | writes to disk | risky/destructive]
  Background: [yes | no]
  Write ownership / isolation: [exclusive paths | worktree | read-only]
  Skills / context: [needed files and what must be supplied]
  Budget / pass signal: [supported limit and check]

Subagent 2 - ...

Synthesis plan: [how results will be combined after all agents complete]
Dependency check: [shared state, write conflicts, or ordering dependencies to watch]
```

## Guardrails

- Do not run overlapping writers or dependent tasks concurrently.
- Await a task whose output is needed before the next step.
- Do not assume a worktree provides permission, secret, or external-service isolation.
- Each task must contain enough context, file paths, goals, and constraints to execute independently.
- If context is already exhausted, use context-limit-continuation first.

## References

- Pair with **`bosskuai-context-limit-continuation`** when context budget is the delegation trigger
- Pair with **`cofounder`** for orchestration and skill routing decisions
- Pair with **`bosskuai-ai-model-selection`** to choose the right model per subagent role
- Pair with **`bosskuai-cross-model-escalation`** when the main workstream is blocked and needs a helper model before or instead of full parallelization
- `../../references/playbooks/claude-code-practices-playbook.md` for host-specific invocation and preloading limits
