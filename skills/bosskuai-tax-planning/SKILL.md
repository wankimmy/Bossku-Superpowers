---
name: bosskuai-tax-planning
description: "Use when structuring a tax planning memo: facts and issues, authority and position strength, effective tax rate bridge, entity or cross-border options, documentation, deadlines. Organises analysis; not tax advice."
---

# BosskuAI Tax Planning

Use this skill to organise a tax question into a reviewable memo: facts, issues, applicable law, analysis, risk, and documentation. The output is a draft for a qualified tax professional, not a conclusion.

## How this differs from nearby skills

- **`bosskuai-bookkeeping`**: closed-period accounting and reconciliations; their output feeds the facts here.
- **`bosskuai-saas-billing-ops`** and **`bosskuai-finance-billing-ops`**: tax and receipt flows inside billing systems, not planning.
- **`bosskuai-financial-modeling`**: projections and scenarios; after-tax scenario inputs from this skill can go into it.
- **`bosskuai-legal-compliance`**: product legal readiness; tax law questions here need a qualified tax adviser.
- **`bosskuai-customs-trade-compliance`**: duties and trade classification, which is a different regime.

## Workflow

1. Facts: entities, ownership, jurisdictions, transactions, dates, amounts, and business purpose. Mark each fact as confirmed or assumed.
2. Issues: write each tax question as one sentence.
3. Authority: list statutes, regulations, treaties, rulings, and cases that may apply, with the jurisdiction and the date you checked. Pull them from current official sources. If you cannot verify a citation, mark it unverified instead of filling the gap.
4. Analysis: apply the law to the facts per issue. Show alternatives, including doing nothing, and the after-tax effect of each on cash, not only the rate.
5. Position strength: for each position state the authority level and confidence standard that applies in that jurisdiction, the exposure if challenged (tax, interest, penalties), and any disclosure that is available or required.
6. Effective tax rate bridge when relevant: pre-tax income, statutory rate, state or local, foreign rate difference, credits, permanent differences, with year-over-year change and driver.
7. Cross-border and transfer pricing: check each jurisdiction's filing and nexus rules, treaty relief, and whether arm's-length pricing is supported by a current benchmarking study.
8. Recommendation and plan: implementation steps with owners and dates, economic substance and business purpose, and monitoring for law changes.
9. Documentation list and calendar of deadlines for elections, returns, estimates, and studies.

## Guardrails

- This skill organises analysis and evidence. It is not tax, legal, or accounting advice. Tax rules differ by place and change often, so every conclusion needs current authoritative sources and review by a qualified tax professional or lawyer.
- Do not file, elect, pay, amend, contact a tax authority, restructure an entity, or change a real account without explicit user approval.
- Do not recommend positions you would not be prepared to disclose or defend, and do not propose arrangements without business substance.
- Do not invent rates, thresholds, or deadlines; look them up for the specific tax year and jurisdiction.
- Do not trade away liquidity for a tax deferral without showing the cash impact.

## Output format

```text
Facts (confirmed / assumed): [..]
Issues: [..]
Authority checked: [source, jurisdiction, date, status]
Options and after-tax impact: [option, cash effect, risk]
Position strength: [position, standard, exposure, disclosure]
Documentation and deadlines: [item, owner, date]
Questions for the qualified reviewer: [..]
```

Adapted from agency-agents/finance/finance-tax-strategist.md (agency-agents, MIT).
