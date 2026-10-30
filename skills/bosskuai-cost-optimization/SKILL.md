---
name: bosskuai-cost-optimization
description: "Use when controlling cloud/server/API/model cost: token budgets, queue sizing, storage costs, vendor spend, and unit economics."
---

# BosskuAI Cost Optimization

Use this skill when spend is the problem: infrastructure, vendor APIs, model tokens, storage, or the unit economics underneath them.

## How this differs from nearby skills

- **`bosskuai-performance-profiling`**: makes something faster; this skill makes it cheaper, which is sometimes the opposite decision.
- **`bosskuai-financial-modeling`**: models company-level revenue and runway; this skill attacks the cost line items feeding it.
- **`bosskuai-token-saver`**: reduces context cost inside an agent session; this skill covers total product spend including models.
- **`bosskuai-ai-model-selection`**: picks a model for capability; this skill sets the cost envelope it must fit.

## Measure before optimizing

Name the cost driver with a number before changing anything. Request volume, tokens per call, queue duration, database load, egress, storage growth, vendor call counts. Optimizing an unmeasured cost usually moves work rather than removing it, and the savings claim cannot be checked afterwards. Price each unit at the provider's live price for the model id the project runs (read from config), and write down the date you checked.

## Where SaaS spend actually concentrates

- **Model/API calls**: prompt size, retries, context re-sent per turn, and calls made on paths users never see.
- **Egress and bandwidth**: often invisible until the bill; check media and export paths.
- **Storage growth**: logs, backups, uploaded media, soft-deleted rows, and old analytics events.
- **Always-on compute**: idle instances, oversized workers, and environments nobody uses.
- **Queue and retry loops**: failed jobs retrying forever cost real money.
- **Per-seat vendor tools**: seats provisioned and never reclaimed.

## Tiering, not blanket downgrades

Separate quality modes rather than degrading everything: a cheap default path, escalation to a stronger model or larger instance only when the task warrants it, and batch/offline processing for work with no latency requirement. This preserves quality where users notice and cuts cost where they do not.

## Caching rules

Cache only what is safe, scoped, and invalidatable. Every cache needs a key that includes tenant and permission scope, an explicit TTL or invalidation event, and a decision about what a stale read would cost. Caching authorization-dependent data on a shared key is a security bug wearing a performance costume.

## Unit economics

Track cost per active user, per job, per lead, or per successful transaction. Absolute spend rising is not automatically bad; cost per successful outcome rising is.

## Order of work

1. **Allocate**: tag every resource by team, service, environment and cost center; deny provisioning without tags. Spend you cannot attribute cannot be owned.
2. **Remove waste**: idle, orphaned and forgotten dev environments.
3. **Rightsize**, then **commit**: buy reserved or committed capacity only for a steady baseline, never for a workload about to be refactored or retired.
4. Give each saving an owner (the team that controls the resource) and watch daily spend with anomaly alerts, so a runaway job shows up in hours, not at month end.
5. Trace the data path for egress: cross-AZ and cross-region traffic and NAT processing hide in line items.

## Guardrails

- Never reduce cost by weakening security, audit trails, tenant isolation, or backup integrity.
- Do not cut observability to the point where the next incident goes undetected. That trade shows up later at a higher price.
- Do not claim a saving without a before and after number.
- Watch for cost shifted rather than removed: moving work to a queue still burns compute.
- Check whether committed-use or reserved pricing beats optimization effort before rewriting code.

## Output format

```text
Measured baseline:
  [cost driver] - [current number] - [source of measurement]

Biggest levers:
  1. [change] - [estimated saving] - [risk] - [effort]

Unit economics: [cost per user / job / transaction, before -> after]
Quality tiers: [cheap default / escalation / batch]
Guardrails preserved: [security, audit, observability untouched]
Verification: [how the saving will be confirmed]
```

## References

- `../../references/checklists/cost-optimization-checklist.md`
- `../../references/checklists/engineering-quality-bar.md`

Adapted from engineering/engineering-finops-engineer.md (agency-agents, MIT).

## LLM pipeline and prompt caching checks

- Route by task complexity (input size, item count) with a cheap default and a `force_model` override; keep model names in config, not scattered in code; log each routing decision so thresholds can be tuned from real data.
- Set a budget limit before a batch and fail early when it is exceeded. When runs can overlap, reserve the spend in one atomic step, or two runs can both pass the check.
- Keep cost records append-only, one per call, with no prompt text or personal data. Sum money as decimals or integer units, never floats, so totals can be audited.
- Retry only transient errors (connection, rate limit, 5xx) with backoff and a cap, and set a timeout on every paid call; fail fast on auth and validation errors.
- Prompt caching: keep tools, instructions and stable examples first and unchanged (a changed prefix breaks reuse from that point); put the question, timestamps and retrieved results after it. Confirm the provider's minimum prefix length, TTL and write price from current docs, since a short prefix yields zero cache hits and a write can cost more than plain input. Caching does not shrink the context window.
- A one-off call or a prefix that keeps expiring can cost more with caching. Count warmup, miss, refresh and retry requests in the measured period.
- Measure with provider usage counters (ordinary input, cache write, cache read, output). Do not double count the same tokens, never apply a cache discount to output tokens, and report token hit rate (cache reads / total input) separately from request hit rate. With no measured traffic, label hit rate and savings `unmeasured`.
- Cache keys and cached handles are scoped to tenant, permission and content revision; a cache key is not an authorization check.
- Usage logs that store cumulative per-session snapshots must be reduced to the latest row per session before summing, and a recorded cost field beats recomputing from token counts.
- Any cost change that alters output (a cheaper model, a shorter prompt, a new cache) changes what existing users get. Check quality on an eval set first, roll it out behind a flag, and keep the old path to switch back to.
- Set the cost budget and the latency ceiling together. A cheaper path that breaks the latency ceiling is not a saving.

Adapted in part from ECC skills/cost-aware-llm-pipeline, skills/cost-tracking and skills/prompt-caching-strategy (affaan-m/ECC, MIT).
