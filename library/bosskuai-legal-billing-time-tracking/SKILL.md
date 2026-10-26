---
name: bosskuai-legal-billing-time-tracking
description: "Use when a law firm needs time capture, billing narratives, invoice review, collections follow-up, trust-account reconciliation, or realization and WIP/AR reports for hourly, flat-fee, or contingency matters."
---

# BosskuAI Legal Billing and Time Tracking

Use this skill to organise law-firm billing work: clean time entries, defensible narratives, reviewed invoices, a polite collections sequence, and trust-account records that reconcile.

## How this differs from nearby skills

- **`bosskuai-finance-billing-ops`**: revenue, pricing, and refund truth for a software or product business. This skill is law-firm time, narratives, and trust accounts.
- **`bosskuai-customer-billing-ops`**: subscriptions and refunds through billing tools. Law-firm matters have ethics rules and client trust funds.
- **`bosskuai-legal-compliance`**: product-facing privacy and policy readiness, not firm billing.
- **`bosskuai-financial-modeling`**: forward-looking company models, not matter-level billing analysis.

## Workflow

1. Confirm the fee arrangement per matter (hourly, flat, contingency, hybrid) and any client billing guidelines (increment size, block-billing ban, task codes).
2. Time capture: entries recorded as work happens or as soon after as possible, in the firm's minimum increment. Flag gaps in the day.
3. Narrative check: each entry says what was done, on what matter, and why, in words a client understands. Flag vague entries ("review file", "phone call") for revision. Where block billing is allowed, list each task with its time.
4. Pre-bill review: pull unbilled WIP, check narratives and guideline compliance, remove non-billable time, mark write-down candidates for the responsible lawyer.
5. Invoice review checklist: client and matter details, rates match the agreement, no duplicates, expenses billable and supported, totals add up, trust credits applied, adjustments labelled. The responsible lawyer approves before delivery.
6. Collections: reminder sequence by invoice age (invoice, friendly reminder, past-due notice, final notice, escalation to the responsible lawyer). Keep tone firm and courteous. Log every contact. Payment plans and write-offs are lawyer decisions.
7. Trust accounting: record deposits and disbursements with client, matter, source or payee, date, and authorization. Reconcile bank balance, sum of client ledgers, and trust journal each month. Any mismatch, negative client balance, or missing document goes to the supervising lawyer at once.
8. Reporting: realization, collection rate, WIP and AR aging, hours worked versus billed, write-down reasons, matter profitability.

## Guardrails

- This skill organises billing work. It is not legal-ethics advice. Fee, trust-account, and billing rules differ by jurisdiction and bar; confirm the current rules and have a qualified lawyer or accountant review.
- Bill only actual time worked and billable work. Do not pad, estimate, or bill overhead.
- Client funds are never mixed with operating funds; do not move trust money without authorization and documentation.
- No invoice is sent, write-off posted, trust transfer made, or collections notice sent without the responsible lawyer's explicit approval.
- Contingency terms are confirmed against the signed fee agreement, not from memory.
- Billing disputes go to the responsible lawyer; do not adjust unilaterally.

## Output format

```text
Matter / arrangement: [..]
Entries flagged: [entry - problem - suggested rewrite]
Invoice review: [checklist results, blockers]
Collections: [invoice - age - next step - owner]
Trust reconciliation: [bank - ledgers - journal - difference]
Metrics: [realization, collection, WIP aging, AR aging]
Approvals needed: [who, what]
```

Adapted from agency-agents/specialized/legal-billing-time-tracking.md (agency-agents, MIT).
