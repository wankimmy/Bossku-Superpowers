---
name: bosskuai-healthcare-sovereign-health-systems-agent
description: "Use when a health-technology team is planning engagement with a national health ministry or sovereign health programme: mandate alignment brief, MOU path, pilot sequencing alongside a regulated market launch."
---

# BosskuAI Sovereign Health Systems Engagement

Use this skill to plan how a health-technology team approaches government health systems: map to a stated policy mandate, sequence pilots, and keep sovereign and commercial work separate.

## How this differs from nearby skills

- **`bosskuai-healthcare-emr-patterns`** and **`bosskuai-healthcare-cdss-patterns`**: building clinical software. This skill is about engagement strategy with governments.
- **`bosskuai-healthcare-phi-compliance`** and **`bosskuai-hipaa-compliance`**: data protection engineering and a US regime; here data rights appear as a partnership term.
- **`bosskuai-legal-compliance`**: product-level legal readiness, not government partnership design.
- **`bosskuai-sales-strategy`**: commercial selling, which this skill explicitly separates from sovereign engagement.

## How the two tracks differ

| | Sovereign | Commercial |
|---|---|---|
| Entry point | Policy mandate alignment | Product demonstration or pilot |
| Stakeholders | Ministry technical teams, development partners | Hospital or payer buyers |
| Success marker | Framework agreement, pilot authorisation, data MOU | Signed contract |
| Timeline | Follows policy cycles; usually long | Follows procurement cycles |

## Workflow

1. Identify the specific national policy or coverage mandate the technology addresses: coverage extension, financial protection, or quality improvement. If none fits, treat it as a product, not a partnership.
2. Research the ministry's current priorities and active procurements, and the institutional route in (development partners, academic centres, in-country operators).
3. Write a one-page mandate alignment brief: no product pitch, no pricing.
4. First engagement: lead with the brief, ask about infrastructure gaps and data governance, leave with a named technical counterpart and a documented next step. Do not discuss pricing or procurement.
5. Build toward a framework agreement: joint technical working group, contained data pilot, co-authored policy brief, MOU, then pilot authorisation.
6. If also launching in a regulated market, sequence the two so each supports the other, and avoid running both with the same team, materials and timeline.
7. Keep the regulatory analysis separate per jurisdiction, each reviewed by local counsel.
8. Maintain relationships at institutional level with regular updates and a continuity plan for political change.

## Guardrails

- This skill supports planning only. Regulatory, clinical, data-protection and contract conclusions need current authoritative sources, local legal advice and a qualified human reviewer.
- No commitments to a government partner without legal review. No outreach, submission or agreement is sent or signed without the user's explicit approval.
- Do not name individual officials in documents shared externally.
- Do not apply one jurisdiction's regulatory analysis to another.

## Output format

```text
Mandate: [policy, commitment addressed]
Alignment brief: [one-page outline]
Stakeholders: [institutions, technical counterparts]
Sequence: [phase, goal, evidence produced]
Data rights and regulatory notes: [per jurisdiction, reviewer]
Next step: [action, owner, date]
```

Adapted from agency-agents/healthcare/healthcare-sovereign-health-systems-agent.md (agency-agents, MIT).
