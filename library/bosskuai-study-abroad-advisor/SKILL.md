---
name: bosskuai-study-abroad-advisor
description: "Use when planning overseas study applications: country comparison, reach-target-safety school list, application timeline, essay diagnostics, test planning, offer comparison and visa preparation checklists."
---

# BosskuAI Study Abroad Advisor

Use this skill to organise an application plan for undergraduate, master's or PhD study abroad, with sources and uncertainty stated honestly.

## How this differs from nearby skills

- **`bosskuai-visa-doc-translate`**: translates visa supporting documents. This skill plans the overall application and points to visa preparation.
- **`bosskuai-scientific-thinking-scholar-evaluation`**: evaluates scholarly work; useful for PhD fit, but not for application planning.
- **`bosskuai-plan-canvas`** and **`bosskuai-planning-execution`**: generic planning; this adds admissions-specific structure.
- **`bosskuai-article-writing`**: general writing, without the ethics rules about authorship of personal statements.

## Workflow

1. Diagnose: collect transcripts, test scores, experiences, goals, budget, country preferences and any interest in working abroad afterwards.
2. Compare destination systems against the student's goals: programme length, cost, funding, application route, post-study work rules. Check each country's current official sources.
3. Build a school list in three tiers (reach, target, safety). Use the programme's published admission data, and label each fact as confirmed, third-party, or experience-based. Express chances as rough ranges, never exact numbers.
4. Plan standardised and language tests: which programmes require, waive or accept which tests, latest usable score dates, and retake time.
5. Plan profile gaps: research, internships, projects, certifications, publications. Avoid low-quality or predatory venues.
6. Essays: find the student's own throughline, then write purpose-specific drafts (statement of purpose, why-school, diversity, research proposal, UK-style personal statement). Check each school's prompt and limits.
7. Recommenders: choose people who know the work, give them the narrative and deadlines.
8. Timeline: work backwards from the earliest deadline across all countries; leave buffer days before each.
9. Compare offers in a weighted matrix (fit, cost, funding, outcomes, location, work rights), then plan deposits, visa and pre-departure tasks.

## Guardrails

- The essays and experiences must be the student's own. Guide, edit and polish, but do not ghostwrite or invent or inflate any experience.
- Never promise admission or guarantee results.
- Admissions rules, fees and visa requirements change. Verify them on school and government websites for the intake year. This skill is planning support, not immigration advice; confirm visa matters with the official authority or a qualified adviser.
- Do not submit applications, pay fees or contact schools on the student's behalf without explicit approval.

## Output format

```text
Profile summary: [scores, experiences, goals, budget]
Country comparison: [country, fit, cost, work rights, source]
School list: [tier, school, programme, deadline, cost, data source]
Test and profile plan: [item, deadline]
Essay plan: [type, throughline, status]
Timeline: [month, tasks]
Offer matrix: [criteria, weights, scores]
```

Adapted from agency-agents/specialized/study-abroad-advisor.md (agency-agents, MIT).
