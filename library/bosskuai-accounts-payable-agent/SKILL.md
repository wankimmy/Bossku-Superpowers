---
name: bosskuai-accounts-payable-agent
description: "Use when preparing vendor invoice and bill payments for approval: duplicate checks, invoice-to-PO matching, approval thresholds, payment-run proposals, an audit trail, and AP summaries. Prepares the run; a human releases the money."
---

# BosskuAI Accounts Payable Preparation

Use this skill to get invoices ready to pay: verified, de-duplicated, matched, logged, and queued for a human to approve. It never sends money itself.

## How this differs from nearby skills

- **`bosskuai-finance-billing-ops`**: revenue side (sales snapshots, refunds, duplicate charges to customers). This skill is the payables side, money going out to vendors.
- **`bosskuai-legal-compliance`**: product legal and privacy readiness. Contract terms in a vendor agreement go to a lawyer, not here.
- **`bosskuai-energy-procurement`**: buying energy and supplier RFPs. This skill starts after the purchase, at the invoice.

## Workflow

1. Intake each invoice: vendor, invoice number, date, currency, amount, PO or contract reference, payment instructions.
2. Duplicate check: look up the invoice reference (and vendor + amount + date) in payment history before anything else. If it was paid or is queued, stop and report.
3. Vendor check: the vendor is in the approved registry and the bank or wallet details match the registry. A changed account is a hold, confirmed through a known contact, not through the invoice email.
4. Match: invoice against PO and receipt or milestone approval. Any amount, quantity or tax mismatch is flagged and held, not auto-approved.
5. Validate the amount: finite, positive, correct currency. Never add amounts across currencies.
6. Apply approval thresholds set by the user or company policy; anything above them goes to a named approver.
7. Choose the payment method from what the vendor and company already use. Settlement times and fees vary by provider; check the provider's current docs.
8. Produce the payment-run proposal and wait for explicit approval.
9. After a human releases payments, record the result with the reference, amount, method, timestamp and status. Failed payments are held and reported, never dropped.

## Guardrails

- This skill organises work and evidence and is not accounting, tax or legal advice. Conclusions need current authoritative sources and a qualified human reviewer.
- No payment, transfer or bank detail change on a real account without explicit user approval, every time.
- Make payment requests idempotent: one invoice reference, one payment.
- Do not store full bank numbers or secrets in notes or logs.
- Pending and failed items are not paid; report them separately.

## Output format

```text
Run: [date, currency]
Ready for approval: [vendor, invoice ref, amount, method, match status]
Held: [invoice ref, reason: duplicate / unapproved vendor / mismatch / over limit]
Needs approver: [item, threshold, approver]
Audit trail: [reference, status, timestamp for each released item]
```

Adapted from agency-agents/specialized/accounts-payable-agent.md (agency-agents, MIT).
