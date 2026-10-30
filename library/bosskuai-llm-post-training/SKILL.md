---
name: bosskuai-llm-post-training
description: "Use when running or debugging LLM post-training (SFT, DPO, GRPO/RLVR, RLHF, MoE): gated experiments, label-mask and reward checks, checkpoint integrity, stalled-run diagnosis, and release evidence."
---

# BosskuAI LLM Post-Training

Use this skill to treat every post-training run as a controlled behaviour change. Loss, reward, throughput, an exit code, or a checkpoint directory is never enough evidence by itself.

## How this differs from nearby skills

- **`bosskuai-mle-workflow`**: general production ML (data contracts, reproducible training, deployment). This skill is specific to tuning language models and their release gates.
- **`bosskuai-ml-engineering`**: shipping ML features and serving; no RL or preference-tuning diagnostics.
- **`bosskuai-eval-driven-agent-improvement`**: evals for agents and prompts, not weight updates.
- **`bosskuai-ai-model-selection`**: choosing a model, not changing its weights.

## Workflow

1. Freeze the decision contract: behaviour target and non-goals, baseline checkpoint digest, data and tokenizer revision, decoding settings, evaluator version, and compute budget. Compare runs only under the same contract. Add the trainer, framework, CUDA and driver versions to the contract.
2. Advance through gates, each with an artifact and a stop condition: preflight (data, template, config checks), smoke (tiny run that produces the promised evidence), signal (the metric moves for the right reason), controlled (matched baseline, held-out evaluation). Run preflight on a copy of production data only after a privacy decision on that copy. Mask or pseudonymise personal fields, keep each field's type and rough length so token counts, truncation and label checks still match production, and keep any key apart from the copy. Delete the copy after preflight. If none exists, ask the user to prepare one.
3. Pick the weakest sufficient method. SFT for trusted targets; preference optimisation only when pair integrity is proven; RL only with a validated, non-degenerate reward tied to held-out quality. Improve data or evaluation before adding compute.
4. Change one variable after an unexplained failure. Classify the failure first (data, objective, reward, rollout, runtime, integrity, or quality) and run the smallest test that separates the explanations.
5. Write an incident report with these headings: Status (PASS, WARN, FAIL, UNVERIFIED), Observed Evidence, Failure Classification, Next Minimal Test, Stop Condition, Artifacts to Preserve, Risks and Limitations.
6. Record a checkpoint release: expected shard inventory, config and tokenizer, rank-local save evidence, hash manifest, and a clean-load probe. Do not register, resume from, or publish a checkpoint that fails any of these. Keep the current checkpoint serving until the new one passes, and keep the previous checkpoint and its manifest for rollback.
7. Preserve hashes, resolved config, sanitised samples, and terminal output before cleanup or retry.

## Known signatures to check first

| Symptom | Check |
|---|---|
| SFT loss falls, held-out behaviour flat | rendered chat template, token IDs, labels, assistant span, ignore index, truncation order, train/eval contamination |
| DPO loss finite, preference accuracy near random | chosen and rejected become identical after truncation (pair collapse) |
| GRPO learning stalls, hardware busy | zero reward variance inside groups means no advantage signal even though execution works |
| RLVR reward up, responses longer, exact match flat | possible reward exploitation; watch KL and clip fraction |
| MoE routing shifts | aggregate expert counts do not prove a quality regression; compare weights, tokenizer, config, and routing settings |
| Task running, no resource activity | UNVERIFIED; take two liveness samples (log size, process state, telemetry) over a fixed interval |

## Guardrails

- Do not scale a run whose smoke or signal gate has not produced evidence.
- Do not diagnose from one scalar. Do not claim correlation or a reward increase proves quality or causality.
- Keep credentials, private examples, and raw environment dumps out of evidence bundles.
- Library flags and trainer behaviour vary by version; check the installed framework docs, and the latest stable release notes, checked live at work time.
- Do not launch paid cluster jobs or publish a model without explicit user approval.
- A new checkpoint changes what users get. Gate it behind a canary, and tell the user what behaviour changes before it ships.

## Output format

```text
Behavior target / non-goals: [text]
Comparator contract: [baseline digest, data, tokenizer, evaluator]
Gate: [preflight | smoke | signal | controlled] and result
Single change under test: [text]
Evidence: [metrics, held-out results, integrity checks]
Decision: [promote | stop | diagnose] and stop condition
```

The shared quality bar: `../../references/checklists/engineering-quality-bar.md`.

Adapted from agency-agents/engineering/engineering-llm-post-training-engineer.md (agency-agents, MIT).
