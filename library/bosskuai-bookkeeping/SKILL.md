---
name: bosskuai-bookkeeping
description: "Use when running month-end close or bookkeeping controls: close checklist, account reconciliations, journal entry support, flux analysis, and segregation of duties. Organises the work; not accounting advice."
---

# BosskuAI Bookkeeping and Month-End Close

Use this skill to plan and review the routine accounting cycle: keep the ledger reconciled, close on a published calendar, and leave support for every balance.

## How this differs from nearby skills

- **`bosskuai-accounts-payable-agent`**: vendor invoices, PO matching, and payment-run proposals. This skill covers the whole ledger close, of which AP is one reconciliation.
- **`bosskuai-finance-billing-ops`** and **`bosskuai-saas-billing-ops`**: revenue, refunds, and subscription billing truth. They feed this skill's revenue and deferred-revenue reconciliations.
- **`bosskuai-financial-modeling`**: forward projections. This skill is about closed periods and actual balances.
- **`bosskuai-tax-planning`**: tax positions and filings. Close output is an input there.

## Workflow

1. Publish a close calendar with owners, dependencies, and a cut-off date. Confirm bank feeds, AP and AR entries, payroll, and expense reports are in before cut-off.
2. Post recurring entries (depreciation, amortisation, rent, insurance), then accruals and deferrals. Each manual journal needs a real description, support, preparer, and a different approver.
3. Reconcile every balance sheet account to independent support: bank and cards to statements, AR and AP to subledger aging, prepaids and fixed assets to schedules, accruals and deferred revenue to roll-forwards, intercompany to the counterparty.
4. For each reconciliation record GL balance, support balance, reconciling items with age and owner, and the remaining difference. Investigate any unexplained difference; do not net it away.
5. Review the trial balance for unusual balances, then run flux analysis (month over month and against budget) with a written reason for each variance above the agreed threshold.
6. Review, lock the period, archive support, and hold a short retrospective on what slowed the close.
7. Corrections that touch already-reported periods are documented and disclosed to the people who relied on those numbers.

## Guardrails

- This skill organises work and evidence. It is not accounting, audit, or tax advice. The accounting framework, thresholds, and policies that apply need current authoritative sources and a qualified accountant or auditor to review.
- Do not post, approve, pay, file, or change a real ledger, bank, or payroll system without the user's explicit approval.
- Keep initiator, approver, and recorder as different people where staffing allows; where it does not, name the compensating review.
- Do not guess account balances or invent support. Mark missing support as open.
- Never store credentials or bank details in notes.

## Output format

```text
Period / entity: [..]
Close status: [task, owner, due, done]
Reconciliations: [account, GL, support, difference, open items]
Journals needing support or approval: [id, issue]
Flux explanations: [line, change, reason, evidence]
Open risks and who must review: [..]
```

Adapted from agency-agents/finance/finance-bookkeeper-controller.md (agency-agents, MIT).
