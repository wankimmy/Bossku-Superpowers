---
name: bosskuai-healthcare-customer-service
description: "Use when drafting patient-support scripts and workflows for a clinic or hospital: appointment, billing, insurance, and complaint handling, emergency screening, clinical routing, and warm escalation with privacy limits."
---

# BosskuAI Healthcare Customer Service

Use this skill to design or review the non-clinical support side of a healthcare organisation. It organises scripts, routing, and records; it does not give clinical advice.

## How this differs from nearby skills

- **`bosskuai-customer-success-support`**: SaaS support SOPs and SLAs. This skill adds patient-specific safety, privacy, and routing rules.
- **`bosskuai-healthcare-phi-compliance`** and **`bosskuai-hipaa-compliance`**: how software stores and protects health data. This skill is the conversation and escalation workflow.
- **`bosskuai-healthcare-emr-patterns`**: building clinical systems.
- **`bosskuai-medical-billing-coding-specialist`**: claim coding and denials. This skill only explains bills and routes disputes.

## Workflow

1. Greet, ask who is speaking, and screen for an emergency in the first moments. If the person describes an emergency, stop the original task and direct them to local emergency services or a crisis line; confirm help is on the way. Use the correct local numbers for the organisation's country.
2. Verify identity before discussing any account details, with the minimum identifiers the organisation's policy allows. Do not ask for more health information than needed or repeat sensitive details unnecessarily.
3. Listen, reflect back what you heard, and classify: appointment, billing, insurance, complaint, clinical question, or other. Ask one clarifying question at a time.
4. Clinical questions (symptoms, medication, test results) are not answered by support. Route to licensed clinical staff warmly.
5. Complaints: acknowledge, validate, clarify, act and document, then commit to a specific next step with a time. Escalate legal threats, safety incidents, and complaints involving clinical staff to a supervisor and risk management.
6. Billing: explain each charge in plain language, show what insurance paid versus patient responsibility, mention financial-assistance and payment-plan options the organisation actually offers, and hold disputed accounts for review where policy allows.
7. Insurance: state coverage and authorisation status, what the organisation is doing, and what the patient may need to do. For denials, route to the appeals specialist.
8. Escalation tiers: immediate (emergency, self-harm, legal threat, any clinical question), same day (large disputes, distress, imminent-treatment denials), next business day (standard review). Do warm transfers: brief the receiver, stay until connected, and give a direct callback route.
9. Close with a summary, owner, deadline, and a reference number. Record every commitment and keep follow-ups.

## Guardrails

- This skill organises work and wording; it is not clinical, legal, or insurance advice. Rules (privacy law, appeal windows, emergency numbers) depend on country and payer, so confirm against current authoritative sources and have a qualified reviewer approve the scripts.
- Take no action on a real patient account, appointment, claim, or record without explicit approval from the user and the organisation's authorised staff.
- Do not place a distressed caller on hold without asking and giving an estimate. Do not use family members as interpreters for clinical or billing talk.

## Output format

```text
Contact type: [appointment / billing / insurance / complaint / clinical / emergency]
Emergency screen: [clear / escalated]
Resolution or route: [what, who, by when]
Script: [acknowledge -> clarify -> action -> commitment]
Record: [commitments, escalations, follow-up date]
```

Adapted from agency-agents/specialized/healthcare-customer-service.md (agency-agents, MIT).
