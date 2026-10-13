---
name: bosskuai-french-consulting
description: "Use when pricing and contracting as an independent IT consultant in France: ESN margin chain, daily rate (TJM) gross versus net, portage vs micro-entreprise vs SASU math, platform choice, payment delays, contract review."
---

# BosskuAI French Consulting Market

Use this skill to reason about how freelance IT consultants are sold through ESNs (IT services firms) and platforms in France, and what a quoted daily rate really leaves after charges.

## How this differs from nearby skills

- **`pricing`**: product and SaaS pricing strategy. This skill is about a person's day rate and the French intermediary chain.
- **`bosskuai-financial-modeling`**: company projections and runway. Here the unit is one consultant's net daily rate and cash timing.
- **`bosskuai-legal-compliance`**: product legal readiness. Contract clauses and status choices here need a French professional.
- **`bosskuai-china-market-localization-strategist`**: another market-entry skill, for a different country.

## Workflow

1. Situation: billing structure now (portage salarial, micro-entreprise, SASU or EURL, employee), specialisation, seniority, location, savings runway, current pipeline.
2. Rate maths: always show three numbers for any offer: gross daily rate (TJM), net after all charges and tax for each structure, and effective rate after unpaid days. Compute from the user's own inputs and the current official rate tables; do not reuse remembered percentages.
3. Margin chain: sell rate to the end client, ESN margin, buy rate to the consultant. Treat any margin or rate figure as an estimate and ask the user for the real numbers where possible. Larger firms usually leave less room than smaller specialists or direct clients.
4. Positioning: lead with the niche specialism rather than the generic platform title. Platform profile rates are visible to clients, so set them deliberately.
5. Floor and negotiation: compute a minimum viable rate from monthly costs, target savings, and billable days. Quote above target, and trade rate only for concrete returns (duration, remote days, renewal terms, expenses).
6. Cash timing: model real payment delay through the chain, not just the contract term, and keep a buffer.
7. Contract review checklist: non-compete scope, payment terms and late penalties, renewal and rate adjustment, termination notice, client concentration risk.
8. Remote or abroad: disclose location early, and check which entity can legally invoice and how tax residency applies.

## Guardrails

- This skill organises options and arithmetic. It is not legal, tax, or social-security advice. Current French rules, rates, and thresholds need authoritative sources (official sites) and a qualified accountant or lawyer.
- Do not sign, invoice, register a company, or contact an ESN or platform on the user's behalf without explicit approval.
- Do not advise hiding real location or status from a client.
- Never present portage as equal to an employment contract; the consultant still carries the commercial risk.

## Output format

```text
Offer: [client, ESN, gross TJM, duration]
Net comparison: [structure, assumptions, net per day, source of rates]
Cash timeline: [invoice date, expected payment]
Leverage points and floor: [..]
Contract flags: [clause, risk]
Questions for accountant or lawyer: [..]
```

Adapted from agency-agents/specialized/specialized-french-consulting-market.md (agency-agents, MIT).
