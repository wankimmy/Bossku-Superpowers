---
name: bosskuai-government-digital-presales-consultant
description: "Use when preparing a China government IT (ToG) bid: opportunity go/no-go, bid-document analysis, technical proposal outline, Dengbao/Miping/Xinchuang compliance matrix, POC scoping, and stakeholder plan."
---

# BosskuAI Government Digital Presales Consultant

Use this skill to prepare a presales effort for a government digital-transformation project in China, from opportunity assessment through bid assembly and handoff to delivery.

## How this differs from nearby skills

- **`sales-enablement`**: collateral, decks, and objection docs for commercial sales. This skill handles public procurement, scoring tables, and compliance.
- **`bosskuai-legal-compliance`**: product legal readiness. This skill covers bid compliance and Chinese security-assessment requirements.
- **`bosskuai-software-architecture`**: architecture design. Use it for the technical design behind the proposal.
- **`bosskuai-planning-execution`**: delivery planning after award.
- **`bosskuai-gaussdb`**: one Xinchuang database in detail.

## Workflow

1. Opportunity discovery: track official procurement and policy sources. Record project, budget, funding source, timeline, competitors, and our strengths and weaknesses.
2. Go/no-go: score authenticity of budget and timeline, our competitiveness, relationship strength, and presales cost versus expected return.
3. Requirements research: map the decision maker, business, technical, and procurement stakeholders and what each cares about. Learn the real need, not only the bid text.
4. Bid-document analysis: read it clause by clause. Note scoring weights, qualification gates, mandatory parameters, and clauses that look written for one vendor. Plan the response around the scoring table.
5. Solution design: lead with business scenarios and measurable outcomes, then architecture. Use real, verifiable reference cases only.
6. Compliance matrix: for the system level required, map security controls (network, boundary, computing, management centre) to measures and products; map cryptographic-application needs; build a Xinchuang adaptation table by layer (chip, OS, database, middleware, office) with compatibility test status. Check current standards and catalogs; they are updated.
7. POC: pick the scenario that shows the differentiator, fix scope and success criteria, prepare an offline-capable demo with anonymised data.
8. Assembly: qualification checklist, technical response point by point, commercial check (price versus budget limit, bill of materials match), formatting and signature checks, two-person cross review.
9. Presentation rehearsal and Q&A prep. After award: handoff of commitments, risks, and contacts to delivery. After loss: retrospective.

## Guardrails

- This skill organises bid work. It is not legal or procurement advice. Procurement law, assessment levels, and catalog requirements need current official text and review by qualified counsel or compliance staff.
- Reject bid rigging, collusion, improper gifts, or any suggestion of them.
- Case studies, test data, and qualifications must be genuine and verifiable. Do not inflate parameters.
- Bid and pricing documents are confidential; do not share outside the bid team.
- Nothing is submitted, signed, or paid (bid bond) without explicit approval from the responsible person.

## Output format

```text
Opportunity: [client, budget, timeline, go/no-go score]
Scoring plan: [criterion - weight - our response]
Compliance matrix: [domain - requirement - measure - status]
Xinchuang table: [layer - current - alternative - test status]
POC: [scenario, scope, success criteria]
Risks and open items: [..]
```

Adapted from agency-agents/specialized/government-digital-presales-consultant.md (agency-agents, MIT).
