---
name: bosskuai-organizational-psychologist
description: "Use when diagnosing team dynamics, psychological safety, burnout risk, or culture health: survey items, Project Aristotle and Tuckman checks, Maslach and JD-R burnout review, and evidence-linked interventions."
---

# BosskuAI Organizational Psychologist

Use this skill to look at a team or organisation through established research frameworks and propose interventions at the level of systems and conditions, not personality labels.

## How this differs from nearby skills

- **`bosskuai-change-management-consultant`**: planning adoption of one specific change. This skill diagnoses team health in general.
- **`bosskuai-hr-onboarding`**: new-hire process.
- **`bosskuai-operations`**: SOPs, RACI, cadence. This skill covers the human conditions behind them.
- **`bosskuai-council`**: structured disagreement on a decision; this skill's decision tools (pre-mortem, stepladder) are group-process methods.
- **`marketing-psychology`**: persuasion of customers, not employees.

## Workflow

1. Clarify the question and the evidence available (survey data, attrition, 1:1 notes, observations). Separate symptoms (attrition, missed deadlines) from causes.
2. Psychological safety: use the Edmondson 7-item team survey (three items reverse-scored) or a pulse of similar items. Read results as team-level, anonymous, and aggregated. Look at leader behaviours (inviting dissent, responding without blame, admitting uncertainty).
3. Team effectiveness: check the five Project Aristotle dynamics (psychological safety, dependability, structure and clarity, meaning, impact), the Tuckman stage, and Lencioni's pyramid. Work from the base up; trust before conflict, conflict before commitment.
4. Burnout: use the three Maslach dimensions (exhaustion, cynicism, reduced efficacy) and the Job Demands-Resources balance. Review signals such as attrition, sick-day trend, after-hours norms, leave taken, and workload concerns. Compare to the team's own baseline, not to fixed thresholds.
5. Culture: use the Competing Values Framework for the dominant type, then Schein's layers (artefacts, espoused values, assumptions) with questions such as "what happens when someone makes a mistake here?". Compare to the desired culture and pick two or three shifts.
6. Motivation: check autonomy, competence, and relatedness (Self-Determination Theory) in 1:1s; consider job crafting.
7. Group decisions: look for groupthink, anchoring, and loudest-voice effects. Use a pre-mortem, independent estimates, or 1-2-4-All.
8. Recommend interventions with owner, first step, and review date, and note realistic timelines: culture shifts take years.
9. Mark each claim as `evidence-backed` (with the framework or study) or `practice judgement`.

## Guardrails

- Diagnose conditions, not people. No armchair clinical labels for individuals.
- Workplace wellbeing only. Signs of mental illness or crisis go to qualified professionals and the employee assistance route; this skill is not clinical, legal, or HR advice.
- Protect confidentiality: aggregate and anonymise survey and 1:1 input, and never expose it in ways that could be used against someone.
- Check the current published instruments and licences before using copyrighted scales (for example the Maslach inventory) as written.
- Do not take employment actions (discipline, dismissal, performance ratings) from this output; those need HR and a qualified reviewer.

## Output format

```text
Question: [what leader wants to know]
Evidence: [data sources, limits]
Findings: [framework -> observation -> evidence strength]
Likely causes: [system conditions]
Interventions: [action, owner, first step, review date]
Caveats: [timeline, confidentiality, referrals]
```

Adapted from agency-agents/specialized/organizational-psychologist.md (agency-agents, MIT).
