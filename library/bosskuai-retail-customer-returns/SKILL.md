---
name: bosskuai-retail-customer-returns
description: "Use when handling retail counter or online customer returns: eligibility check against policy, item inspection, refund method, exchange, exception logging, fraud red flags with escalation, and reason-code analytics."
---

# BosskuAI Retail Customer Returns

Use this skill for the front-line side of returns: deciding eligibility, processing a refund or exchange fairly, escalating suspicious cases, and recording reason codes that feed product and vendor decisions.

## How this differs from nearby skills

- **`bosskuai-returns-reverse-logistics`**: warehouse-side authorisation, disposition, warranty and vendor claims. This skill centres on the customer interaction and policy decision.
- **`bosskuai-customer-billing-ops`**: refunds and plan changes through subscription billing tools.
- **`bosskuai-customer-success-support`**: general support handling; this adds inspection, refund-method and fraud-escalation rules.
- **`bosskuai-logistics-exception-management`**: shipment exceptions, not store returns.

## Workflow

1. Greet and acknowledge before asking questions. Identify the item and transaction by receipt, order lookup or account.
2. Check eligibility against the store's written policy: window, condition, category restrictions (final sale, opened hygiene or personal-care items, custom items, hazardous goods), proof of purchase.
3. Inspect the item before refunding: condition, all parts and packaging, serial or tag match, signs of tampering.
4. Decide the outcome: full refund, partial refund (state the deduction and reason), exchange, store credit, or decline with at least one alternative offered, such as a manufacturer warranty or manager review.
5. Refund to the original payment method by default. Use store credit or another method only where the policy says so or a manager approves.
6. Record an accurate reason code. Product issues, customer preference and operational errors should be distinguishable in the data.
7. Disposition the item: restock, open-box, vendor return, salvage, destroy where safety requires, or hold for loss-prevention review.
8. Offer an exchange or help finding a better fit where it is relevant, and close politely.
9. Analyse reason codes by product, category and channel; look for description, size-guide or packaging problems and for vendor defects.

## Fraud and exceptions

- Red flags are signals for internal escalation, not accusations: altered receipts, tag or serial mismatch, resealed packaging, repeated returns of the same item, refusal of inspection.
- If suspected, do not accuse or process. Ask a manager or loss prevention to take over, document the reason, and let the customer leave if they become hostile.
- Document every exception with reason and approver. Apply the policy the same way to every customer.
- Never confiscate a declined item.

## Guardrails

- Follow the store's actual policy and local consumer law, which varies. This skill supports process design and training and is not legal advice.
- Do not issue a real refund, change a customer record or flag a person to loss prevention without the user's or manager's explicit approval.

## Output format

```text
Eligibility: [window, condition, category, proof]
Inspection result: [grade, notes]
Outcome: [refund / partial / exchange / credit / decline, amount, method]
Reason code and exception log: [code, approver]
Disposition: [route]
Escalation: [yes or no, to whom, why]
```

Adapted from agency-agents/specialized/retail-customer-returns.md (agency-agents, MIT).
