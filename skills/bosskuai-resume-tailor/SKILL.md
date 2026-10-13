---
name: bosskuai-resume-tailor
description: "Use when tailoring a resume to a specific job description: requirement extraction, evidence mapping, truthful ATS keyword alignment, achievement-style bullet rewrites, gap notes, and a change log."
---

# BosskuAI Resume Tailor

Use this skill to adapt a candidate's real resume to one job posting, matching true experience to stated requirements without inventing anything.

## How this differs from nearby skills

- **`bosskuai-article-writing`**: long-form writing for publication. A resume is short, structured, and evidence-bound.
- **`bosskuai-brand-discovery`**: brand identity interviews for businesses, not personal job applications.
- **`bosskuai-personal-growth-mentor`**: long-term goals and habits. This skill is one application document.
- **`customer-research`**: research on customers. Use only for researching a target employer's market if needed.

## Workflow

1. Intake: the current resume text and the full job description are the minimum. Also ask target company, level, location limits, and concerns (career change, gap, short tenure).
2. Requirement extraction: split must-haves, nice-to-haves, tools, seniority signals, and repeated terms. Rank by likely importance.
3. Evidence mapping: for each requirement mark the resume evidence as strong, partial, unsupported, or irrelevant.
4. Rewrite: lead with the strongest relevant evidence. Convert duty bullets into action, scope, result, and context. Use the job's exact terms only where the candidate's background supports them.
5. Metrics: add numbers the candidate provided or that follow directly from their facts. For unknown numbers, write a question for the candidate, not a guess.
6. Format for parsing: standard section headings, clear dates, simple layout, spelled-out acronyms, no tables or graphics in the body.
7. Gap handling: list missing requirements with truthful options (adjacent experience, project, course, portfolio, cover-letter framing), and say when the role is a stretch.
8. Review: check each claim against the candidate's own material; the candidate must be able to explain every line in an interview.
9. Deliver: fit table, keyword map (supported, to strengthen, not yet claimable), tailored draft, change log, open questions.

## Guardrails

- Do not invent jobs, dates, degrees, employers, tools, metrics, certifications, or responsibilities. Unsupported items go in "do not claim yet".
- Do not keyword-stuff or imply expertise from a single exposure.
- Do not promise interviews, offers, ATS results, or visa outcomes. Immigration and legal questions go to a qualified professional.
- Candidate documents contain personal data; keep them out of shared logs and do not send them anywhere without the candidate's consent.
- Do not submit any application on the candidate's behalf without explicit approval.

## Output format

```text
Target role: [title, company, level]
Fit table: | Requirement | Resume evidence | Gap / action |
Keyword map: supported / to strengthen / do not claim yet
Rewrites: | Original | Tailored | Why |
Tailored resume: [sections]
Change log and open questions: [..]
```

Adapted from agency-agents/specialized/resume-tailor.md (agency-agents, MIT).
