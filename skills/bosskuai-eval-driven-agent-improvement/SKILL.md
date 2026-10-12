---
name: bosskuai-eval-driven-agent-improvement
description: Use when you need agent eval design, routing tests, retrieval tests, LLM quality cases, regression harnesses, scorecards, and continuous agent improvement.
---

# BosskuAI Eval-Driven Agent Improvement

Use this skill to make agent quality **measurable**, so changes to prompts, tools, or models can be judged instead of guessed at.

## How this differs from nearby skills

- **`bosskuai-agent-architecture-audit`**: inspects agent structure for design faults; this skill measures behavior empirically.
- **`bosskuai-agent-introspection`**: debugs one failing run; this skill turns that failure into a permanent test case.
- **`bosskuai-prompt-optimizer`**: improves a prompt; this skill tells you whether the improvement was real.
- **`bosskuai-qa-automation-strategy`**: tests deterministic software; this skill handles nondeterministic output.

## Build the eval set from real failures

The highest-value cases come from runs that actually went wrong. Each recurring failure becomes a small, named case with a fixed input and a checkable expectation. An eval suite written from imagination tests what you already knew.

## Separate eval types

Aggregating everything into one score hides which layer broke.

- **Routing**: did the right skill, tool, or agent get selected?
- **Retrieval**: were the right documents or context fetched, and was anything critical missed?
- **Workflow**: did the multi-step sequence complete, and did it stop when it should?
- **Quality**: is the final output correct and useful?
- **Token/cost**: did it stay in budget?
- **Safety**: did it refuse, confirm, or escalate where required, including injection resistance?

## Grade with the cheapest sufficient method

Prefer deterministic checks: exact match, schema validity, regex, tool-call assertions, file state. Use an LLM judge only for genuinely open-ended quality, and when you do, give it a rubric and validate the judge against human labels on a sample. An unvalidated judge is an opinion with a number attached.

## Track false confidence

Pass rate alone is misleading. Watch how often the agent is confidently wrong, since that is the failure mode users trust and act on. Record both correctness and calibration, and treat a confident wrong answer as more severe than an admitted uncertainty.

## Guard against overfitting

Tuning prompts against a fixed set produces agents that pass the set and fail reality. Keep a held-out set the prompt author does not read, add fresh generalization cases regularly, and avoid encoding exact phrases from eval cases into prompts.

## Independent review of a model or scorer

When judging a statistical or ML model rather than an agent:

- The reviewer must not have built the model. Record every deviation from the documented method.
- Make the analysis reproducible from raw data: versioned, self-contained scripts, pinned library versions, no manual steps. Replication produces a script plus a delta report against the original.
- Compare against an independently built challenger as a benchmark.
- Check input stability (for example a population stability index per feature) and calibration, not only the headline score. Treat thresholds as monitoring heuristics, not proof of validity.
- Each finding has an observation, evidence, impact, and recommendation, with severity from unsound to informational. Do not say "the model is wrong" without quantifying the impact.

## Guardrails

- Never tune on the held-out set.
- Do not delete a failing case because it is inconvenient; mark it known-failing with an owner.
- Run evals on a fixed model version; a model upgrade is a change to measure, not a confound.
- Report per-category results, not just an aggregate.
- Small suites that run on every change beat large suites nobody runs.

## Output format

```text
Failure being addressed: [observed behavior]

Eval set:
  [case id] - [category] - [input] - [expectation] - [grader: exact/schema/judge]

Baseline: [pass rate per category]
After change: [pass rate per category]
Held-out result: [pass rate, confirming no overfit]

False confidence: [rate of confident-wrong]
Cost per run: [tokens / spend]
Decision: [ship / iterate / revert] - [why]
```

## References

- `../../references/checklists/eval-driven-agent-improvement-checklist.md`

Model review section adapted in part from specialized/specialized-model-qa.md (agency-agents, MIT).
