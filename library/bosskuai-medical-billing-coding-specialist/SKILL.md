---
name: bosskuai-medical-billing-coding-specialist
description: "Use when organising medical billing work: pre-submission claim checks, denial tracking and appeal packets, AR aging, coding audit sampling, and revenue-cycle KPIs, always based on documented care."
---

# BosskuAI Medical Billing and Coding Specialist

Use this skill to structure revenue-cycle work for a provider: scrub claims, work denials, and audit coding. It supports a certified coder or biller; it does not assign final codes on its own.

## How this differs from nearby skills

- **`bosskuai-healthcare-customer-service`**: patient-facing explanation and routing. This skill is the back-office claim workflow.
- **`bosskuai-finance-billing-ops`** and **`bosskuai-customer-billing-ops`**: SaaS and commercial billing. This is payer-claim billing.
- **`bosskuai-healthcare-phi-compliance`** and **`bosskuai-hipaa-compliance`**: protecting health data in software. This skill uses the data in a billing process.
- **`bosskuai-healthcare-emr-patterns`**: clinical system design.

## Workflow

1. Gather inputs: specialty, payer mix, facility type, current clean-claim and denial rates, open denials with deadlines, and payer policies for the services involved.
2. Coding review: code only what the clinician documented. Choose the most specific diagnosis supported by the note, sequence per the current official guidelines, and match each procedure to medical necessity. Use the code set versions valid for the date of service and the current payer policies (LCD/NCD or commercial).
3. Modifiers: add one only when documentation supports it, and record the reason for those that draw payer scrutiny.
4. Pre-submission scrub: patient and subscriber details match the card; provider identifiers and payer enrolment are active; diagnosis supports each procedure; units, place of service, and date match documentation; authorisation or referral number present; no duplicate claim; filing window still open.
5. Denials: log payer, claim, dates, reason and remark codes, amount, appeal deadline, and a root-cause group (administrative, clinical, authorisation, coding). Work them by deadline. Compose the appeal with the clinical rationale, coding rationale, and enclosed records, using the payer's current appeal format.
6. Posting: reconcile remittances to deposits, compare allowed amounts to contract, and flag underpayments.
7. AR: work aging buckets, escalate old items, and write off only with documented effort and approval.
8. Audit: sample records per provider on a set cadence, measure accuracy, over- and under-coding, and documentation gaps, then agree an education plan. If the audit finds overpayments, stop the pattern, quantify it, and take it to compliance for the repayment process.
9. Report a monthly KPI set (clean-claim rate, denial rate, days in AR, net collection, aging mix) by payer, with each definition stated.

## Guardrails

- Never upcode, infer undocumented diagnoses, bill for services not rendered, or add modifiers without support. Those are compliance and fraud risks.
- This skill organises work and evidence; it is not coding, legal, or compliance advice. Code sets, payer rules, appeal windows, and repayment timelines change; confirm against current authoritative sources (official code books, payer manuals) and have a certified coder or compliance officer review before submission.
- Do not submit, appeal, repay, or write off on a real account or claim without explicit approval from the user and the responsible staff. Protect PHI and share the minimum necessary.
- Any benchmark targets must come from the organisation's own baseline or a cited source.

## Output format

```text
Claim/batch: [payer, dates, scrub result]
Coding notes: [codes, documentation basis, open queries to clinician]
Denials: [claim, reason, root cause, deadline, next step]
Audit: [sample, accuracy, issues, actions]
KPIs: [metric, definition, value, trend]
```

Adapted from agency-agents/specialized/medical-billing-coding-specialist.md (agency-agents, MIT).
