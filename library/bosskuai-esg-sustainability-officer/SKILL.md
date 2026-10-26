---
name: bosskuai-esg-sustainability-officer
description: "Use when building an ESG or sustainability programme: double-materiality assessment, GHG Scope 1-2-3 inventory, science-based target path, framework mapping (GRI, TCFD, CSRD), and checking claims for greenwashing."
---

# BosskuAI ESG and Sustainability Officer

Use this skill to organise ESG work so each claim has a method, boundary, and evidence trail, and each target has a funded path.

## How this differs from nearby skills

- **`bosskuai-legal-compliance`**: product privacy and legal readiness. This skill covers sustainability disclosure and climate data.
- **`bosskuai-energy-procurement`**: buying electricity and gas. It can feed Scope 2 data; this skill covers the inventory and reporting.
- **`bosskuai-cost-optimization`**: cloud and vendor cost. Carbon is a different measurement.
- **`bosskuai-deep-research`**: multi-source research for any topic; use it to gather regulation texts.
- **`bosskuai-customs-trade-compliance`**: trade rules, relevant only where carbon border rules touch imports.

## Workflow

1. Scope: legal entities, operating boundary, reporting period, and which regulations or buyers require disclosure. Check current regulation text and deadlines; they change.
2. Materiality: list candidate topics from the chosen framework and sector standard, gather stakeholder input, score financial materiality and impact materiality, plot the matrix, and have governance sign it off.
3. GHG inventory: define the base year; Scope 1 (direct), Scope 2 (location-based and market-based), and screen all Scope 3 categories for relevance, data source, and method. Record emission-factor sources and versions.
4. Targets: set interim milestones and identify funded initiatives (reduce, replace, then remove). Check the current target-setting body's criteria before claiming alignment.
5. Framework mapping: map data points to the required frameworks (for example GRI, TCFD, SASB, CSRD/ESRS, CDP) so one dataset serves several reports.
6. Social and supply chain: workforce metrics, health and safety, human-rights due diligence steps, supplier code and audits, grievance channel.
7. Governance: board oversight, policy suite, whether executive pay links to ESG metrics.
8. Claim review: for each public statement record the method, boundary, data owner, and assurance level. Rewrite or drop claims that cannot be supported.
9. Report cycle: data collection, verification, drafting, legal and finance review, assurance, publication, feedback.

## Guardrails

- This skill organises work and evidence. It is not legal, audit, or assurance advice. Regulatory applicability, thresholds, and dates need current authoritative sources and review by a qualified adviser or assurer.
- No unsupported claims such as "carbon neutral" without defined boundary, method, and verified offsets.
- Do not omit material Scope 3 or bad news to look better.
- Do not submit filings, ratings questionnaires, or public statements without explicit user approval.
- Emission factors and regulatory tables go stale. Cite version and date.

## Output format

```text
Scope and period: [entities, boundary, regulations]
Material topics: [topic - financial / impact score]
Inventory: [scope - method - data source - gaps]
Target path: [target, milestones, initiatives, funding]
Framework map: [data point - framework references]
Claims register: [claim - evidence - status]
Next steps and reviewers: [..]
```

Adapted from agency-agents/specialized/esg-sustainability-officer.md (agency-agents, MIT).
