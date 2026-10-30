---
name: bosskuai-ml-engineering
description: "Use when building an AI-powered product feature: choosing model and serving pattern (real-time, batch, streaming, edge), bias and privacy checks, A/B testing, drift monitoring, and cost control in production."
---

# BosskuAI ML Engineering

Use this skill when a team must put a machine-learning or LLM-powered feature into a product and keep it healthy: pick the approach, serve it, test it fairly, monitor it, and control cost and harm.

## How this differs from nearby skills

- **`bosskuai-mle-workflow`**: the data-contract, reproducible-training, and rollback discipline for ML systems. Use it for the training pipeline; use this skill for product-level choices and serving.
- **`bosskuai-ml-adoption-playbook`**: adding a first ML capability to a codebase that has none. This skill covers the wider lifecycle after that.
- **`bosskuai-ai-model-selection`**: picks which model or provider fits a task.
- **`bosskuai-rag-pipelines`**: retrieval for LLM context specifically.
- **`bosskuai-llm-post-training`**: tuning model weights, with release gates.

## Workflow

1. Requirements and data. State the user problem, the success metric, the cost of a wrong answer, and what data exists. Check whether a simple rule or baseline already meets the need.
2. Choose the approach: classical model, fine-tuned model, hosted API, or retrieval-augmented LLM. Justify against latency, cost, privacy, and accuracy needs.
3. Develop. Data preparation and validation, feature engineering, cross-validation or held-out evaluation, hyperparameter search, and interpretability checks. Report confidence intervals, not single scores. Build the training set from a copy of production data made after a privacy decision, with personal data masked or removed and each field keeping its production type, and compare its types, nulls, value ranges and categories with live traffic first.
4. Fairness and safety. Test performance across relevant groups, check for leakage of personal data, add content-safety and misuse limits, and keep human oversight where errors matter.
5. Pick a serving pattern: synchronous API for interactive use, batch for large offline jobs, streaming for continuous events, edge or on-device for privacy or latency, or a hybrid. Set authentication, rate limits, timeouts, and fallbacks. Check that the serving library and runtime versions match the ones training used.
6. Version models and data (for example with MLflow or an equivalent). Keep a rollback path and canary releases. Record the framework, CUDA and GPU driver versions and the random seeds with each model.
7. Validate online with an A/B test that has a pre-set metric and sample size before declaring a win.
8. Monitor: input drift, prediction drift, data quality, latency, error rate, and cost per request. Define retraining triggers and who approves them.
9. Document model purpose, limits, data sources, and known failure modes.

## Guardrails

- Targets such as accuracy or latency come from your requirements, not from rules of thumb. Do not copy a number from another project.
- Verify framework and cloud service features against installed versions and current docs.
- Face-recognition, hiring, lending, medical, and other high-stakes decisions need legal and domain review and human oversight. This skill organises the work; it is not professional advice.
- Do not send personal or customer data to a third-party API without a privacy decision.
- Do not deploy, retrain on live data, or change production traffic without explicit user approval.
- Check each framework and driver version against its latest stable release, live at work time. `nvidia-smi` shows the GPU driver, and the lockfile shows the framework version.
- A hosted model API call needs a timeout, and retries with capped exponential backoff and jitter for 429 rate-limit and 5xx responses, honoring Retry-After. Retry only calls that are safe to repeat, and never retry a 429 caused by a spend cap or quota. Mask personal data in its request and response logs.
- Deploys keep the current model serving until the new one passes its canary, and the rollback is tested before release.

## Output format

```text
Problem and metric: [text, cost of error]
Approach and baseline: [choice, reason]
Evaluation: [held-out results, group breakdown, intervals]
Serving design: [pattern, auth, limits, fallback]
Rollout: [canary, A/B plan, rollback]
Monitoring: [drift, latency, cost, retrain trigger]
Risks: [fairness, privacy, safety]
Versions and data: [framework, CUDA and driver, data copy used]
```

The shared quality bar: `../../references/checklists/engineering-quality-bar.md`.

Adapted from agency-agents/engineering/engineering-ai-engineer.md (agency-agents, MIT).
