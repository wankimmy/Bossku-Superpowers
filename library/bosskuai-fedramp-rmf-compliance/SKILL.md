---
name: bosskuai-fedramp-rmf-compliance
description: "Use when preparing a system for FedRAMP or the NIST RMF: FIPS 199 categorisation, authorisation boundary, control implementation statements, POA&M, evidence and continuous monitoring planning."
---

# BosskuAI FedRAMP and RMF Compliance

Use this skill to organise authorisation work: categorise honestly, draw the boundary, write assessable control statements, and keep evidence and findings tied together.

## How this differs from nearby skills

- **`bosskuai-cybersecurity-risk`**: general security review and abuse cases; this skill follows a formal authorisation lifecycle.
- **`bosskuai-legal-compliance`**: product-level privacy and policy readiness, not NIST control documentation.
- **`bosskuai-hipaa-compliance`**: HIPAA-specific work, a different regime.
- **`bosskuai-observability-sre`**: logging and monitoring implementation that can supply evidence.

## Workflow

1. Confirm the pathway and requirements from current official FedRAMP and NIST sources: which authorisation route applies, which control catalogue revision and baseline, and the current packaging format and deadlines. These change; do not rely on memory.
2. Categorise: list information types, rate confidentiality, integrity and availability impact, take the highest as the system level, and record the rationale.
3. Draw the authorisation boundary before writing the plan: components, data stores, data flows, external services, inherited platforms.
4. Select the baseline, then tailor only with written justification and any compensating controls.
5. Map responsibility per control: provider, shared, inherited, customer.
6. Write implementation statements that say how this system meets the control: mechanism, configuration, role, evidence. Restating control text is not a statement.
7. Collect dated, owned evidence as you implement. If you cannot produce evidence, mark the control not yet implemented.
8. Track every finding on the POA&M with risk, milestones, owner and date. Close items only with evidence.
9. Plan continuous monitoring: scan cadence, POA&M updates, significant-change review before deployment, incident reporting.

## Guardrails

- This skill organises work and evidence. It is not compliance, legal or audit advice. Conclusions need current authoritative sources and a qualified human reviewer, and nothing is submitted to an agency, assessor or portal without explicit user approval.
- Do not describe a control you cannot demonstrate. Do not under-categorise to avoid controls.
- Treat the plan, assessment report and POA&M as sensitive documents; limit access.

## Output format

```text
Pathway and baseline: [source checked, date]
Categorisation: [info types, C/I/A, rationale]
Boundary: [inside, outside, interconnections]
Control table: [id, status, responsibility, statement, evidence]
POA&M: [weakness, risk, milestone, owner, date]
ConMon plan: [cadence, change review]
```

Adapted from agency-agents/specialized/specialized-fedramp-rmf-compliance.md (agency-agents, MIT).
