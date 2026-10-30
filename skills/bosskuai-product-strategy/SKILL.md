---
name: bosskuai-product-strategy
description: "Use when deciding what to build and why: product strategy, feature shaping, PRD review, scope refinement, prioritization, user-value analysis, and go-to-market implications."
---

# BosskuAI Product Strategy

Use this skill when the task is primarily about **what to build and why**, not how to build it.

## How this differs from nearby skills

- **`bosskuai-planning-execution`**: turns strategy into a roadmap and milestones; load after this skill to sequence delivery.
- **`bosskuai-market-analysis`**: external market reality (competitors, trends, TAM); load alongside when positioning is unclear.
- **`bosskuai-launch-commercialization`**: full launch readiness across engineering, GTM, and sales; load when nearing ship.
- **`bosskuai-business-logic-review`**: correctness of workflow rules; load when an existing feature has wrong logic, not unformed strategy.
- **`bosskuai-analytics-metrics`**: designs the measurement a goal or an ROI review needs; load when the feature has no usable data.
- **`bosskuai-financial-modeling`**: full revenue, runway and unit-economics models; load when the money side needs more than a payback estimate.

## Mindset

- Disaggregate what the user **wants** from what they **need** — surface the real job-to-be-done.
- Challenge scope creep as the default enemy of early delivery.
- Prefer outcomes (behavior change, revenue, retention) over outputs (features shipped).
- Ask "what is the smallest thing that proves the hypothesis?" before defining anything larger.
- Technically possible is never the reason to build. The question is whether it repays the time, and whether something cheaper already gets the goal.

## Workflow

1. **Frame the problem** — Identify the user, the trigger that causes them to seek a solution, the pain, the frequency, and what they currently do instead. Do not accept "users want X" — ask why.

2. **Run a JTBD analysis** — Define the Job-to-be-Done: functional job, emotional job, social job. Separate the core job from ancillary jobs.

3. **Shape the scope** — Apply MoSCoW or NOW/NEXT/LATER to separate must-have from nice-to-have. Challenge every "must have" that lacks a clear failure consequence.

4. **Map assumptions and risks**:
   - What must be true for this to work?
   - Which assumptions are highest risk and lowest validation evidence?
   - What is the riskiest part of this bet?

5. **Define acceptance criteria** — For each must-have scope item, write a testable definition of done from the user's perspective (not the engineering perspective).

6. **Recommend the smallest meaningful delivery slice** — What is the minimum that creates real user value and generates learning? Separate the MVP hypothesis from the full vision.

7. **Surface GTM implications** — Does this change pricing, onboarding, messaging, or sales motion? Call it out even if it is not the user's primary question.

## Worth building? (before anything is built)

Run this for every new requirement, request or idea, and give a verdict before any build plan.

1. **Objective.** The business problem in one sentence: who has it, how often, and the evidence (tickets, logs, usage data, a production data copy, the user's own words). What happens if nothing is built?
2. **Goal.** One measurable outcome: the metric, today's baseline, the target and the date (for example, manual invoice fixes from 40 a week to under 5 within a month of launch). No baseline means measure first.
3. **Options, cheapest first.** Do nothing; change a process or train staff; use or configure what already exists; buy or integrate a tool; build a small slice; build the full thing. Rank them by cost; step 4 picks the one to recommend.
4. **Pick the simplest sound solution.** The recommended option is the simplest one that meets the goal, follows best practice for the stack, and stays efficient at real data sizes and traffic. Reject clever designs, new dependencies and extra moving parts the goal does not need, and say why each rejected option lost.
5. **Short term and long term.** Give both: a short-term solution that relieves the problem now with little effort (a config change, a process step, a small fix, a manual workaround with an owner), and a long-term solution that removes the cause. Say whether the short-term one is a step toward the long-term one or gets thrown away, what it costs to live with, and the trigger or date to move to the long-term one.
6. **Value per year.** People affected × how often × time or money saved per use, plus revenue gained or errors, risk and support load avoided. Write each assumption next to its number.
7. **Cost.** Build effort as a range (code, review, tests, rollout, docs, training), the yearly running cost (hosting, support, upkeep, upgrades), and the opportunity cost: what the team will not build meanwhile.
8. **Verdict.** Build, build smaller, buy or configure, don't build, or get data first. Give the payback period in months: build cost ÷ ((value per year − running cost per year) ÷ 12), your confidence, the riskiest assumption, and the cheapest test that would change the answer.

## ROI review (after it ships)

Run this when asked what a shipped feature returned, and before building more on it.

1. **Goal vs actual.** Read the real numbers for the same metric and period as the goal: usage and adoption by role, task time, error and ticket counts, revenue. Use the production data copy or analytics, not impressions. If the feature was never measured, say so and set up measurement first.
2. **Full cost to date.** Build time, fixes since launch, running cost, and the support load it added.
3. **ROI.** (Value delivered − cost) ÷ cost over a stated period, plus the payback month, with the assumptions and a low and high range.
4. **Improve.** Where users drop off or fall back to the old workaround, the parts nobody uses (candidates to remove), and the top three changes ranked by value ÷ effort, each with the number that would show it worked. Use the same rules as Worth building? steps 4 and 5: the simplest sound fix first, with a short-term and a long-term option where they differ.
5. **Decide.** Keep and improve, simplify, or retire, and the date of the next review.

## Guardrails

- Do not define the solution before the problem is properly framed.
- Do not skip ICP — "everyone" is not a user.
- Do not optimize for feature quantity over outcome quality.
- If the brief is vague, ask clarifying questions rather than fabricating context.
- Do not assume the stated problem is the real problem — probe for the trigger and the workaround.
- Every number comes from data or is labelled an estimate. Ask the user for inputs only they have (staff cost per hour, volumes, contract values) instead of inventing them.

## Output format

```
Problem statement: [one sentence — user, trigger, pain]
JTBD: [functional job / emotional job / social job]
Scope (MoSCoW):
  Must: [list]
  Should: [list]
  Won't (this slice): [list]
Key assumptions: [ranked by risk]
Acceptance criteria: [one per must-have]
Recommended first slice: [what + why it's minimum]
GTM implications: [if any]
Worth it? (new requirement)
  Objective: [problem, who, how often, evidence]
  Goal: [metric: baseline -> target, by date]
  Options considered: [cheapest first; why each rejected one lost]
  Recommended: [simplest option that meets the goal, best practice, efficient]
  Short term: [quick relief, effort, cost to live with] -> Long term: [removes the cause]; switch when: [trigger or date]
  Value per year: [number + assumptions]
  Cost: [build range; running per year; opportunity cost]
  Payback: [build cost / ((value per year - running cost per year) / 12) months]; confidence: [low | medium | high]
  Verdict: [build | build smaller | buy or configure | don't build | get data first] + cheapest test that would change it
ROI review (shipped feature)
  Goal vs actual: [metric, period]
  Cost to date: [build + fixes + running + support]
  ROI over [period]: [(value - cost) / cost, low-high]
  Improve next: [top 3 by value / effort, each with its success number]
  Decision: [keep and improve | simplify | retire]; next review: [date]
```

## References

- `../../references/playbooks/bosskuai-product-strategy-playbook.md`
- `../../references/checklists/product-spec-checklist.md`

## Extra diagnostics
- **Pressure-test questions** to add to step 1: why now (what changed), the 10-star version, the anti-goal (what you are explicitly not building), and the metric that shows it works (a number, not a feeling). End with a go/no-go and the next step.
- **Founder review** of an existing project: read README, instructions, manifest and recent commits; infer what it is trying to be; score usage growth, retention, revenue signals and moat; name the one thing that would 10x it and the things being built that do not matter.
- **Journey audit:** go through the product as a new user, time each step, list friction, and measure time to first win. Recommend the top 3 onboarding fixes.
- **Choosing among many ideas:** score impact x confidence / effort (each 1-5), rank, then apply real constraints (runway, team size, dependencies). Treat the score as a tiebreaker, not a verdict.
- **Acceptance criteria quality:** each one has a starting condition, one trigger, an observable result, a "must not" side effect, a verification method and a priority. Words like "correctly", "secure", "fast" need observable evidence or a marked human judgment.
- **Business rules are not discoverable from code.** Pricing, tier limits, compliance, SLAs, retention and priorities come from the user or a product document. List them as assumptions to confirm, never as discovered facts.
- Ask for confirmation before work only when an open decision risks security exposure, data loss, an irreversible migration, a breaking contract or real cost. Otherwise record assumptions and proceed. If a criterion proves unachievable mid-build, mark it revised with the constraint and re-present only the changed criteria.

Adapted in part from ECC skills/intent-driven-development and product-lens (affaan-m/ECC, MIT).
