---
name: bosskuai-saas-billing-ops
description: Use when handling SaaS subscription lifecycle, invoices, failed payments, dunning, tax/receipt flows, plan changes, entitlement gating, and billing operations.
---

# BosskuAI SaaS Billing Ops

Use this skill when **money state and access state can disagree**: subscriptions, invoices, dunning, plan changes, refunds, and entitlement gating.

## How this differs from nearby skills

- **`pricing`**: decides what to charge; this skill makes the charging mechanism correct.
- **`bosskuai-paid-acquisition-monetization`**: plans monetization strategy; this skill runs the billing system behind it.
- **`churn-prevention`**: cancel flows, save offers, and dunning strategy (retry cadence, email copy, recovery benchmarks); this skill makes the billing state machine, webhooks, and entitlement changes behind them correct.
- **`bosskuai-business-logic-review`**: general workflow review; this skill covers billing-specific state machines.

## Separate payment state from entitlement state

This is the decision most billing bugs trace back to. Payment status is what the processor says; entitlement is what the product grants. Model them as two fields with an explicit mapping, so a webhook delay never silently revokes a paying customer's access, and a refund never leaves access on.

## Lifecycle to model explicitly

Keep two state lists. Processor states come from the processor, spelled exactly as its API spells them (Stripe `subscription.status`: `trialing`, `active`, `incomplete`, `incomplete_expired`, `past_due`, `unpaid`, `paused`, `canceled` with one "l"). Entitlement states are yours, for example `full`, `grace`, `read_only`, `none`; refunds and disputes are events, not statuses. For each transition define: what triggers it, what entitlement results, what the customer is told, and whether it is reversible, plus reactivation.

## Edge cases that break in production

- **Proration on plan change**: upgrade mid-cycle, downgrade mid-cycle, and downgrade that must take effect at period end.
- **Failed payment**: retry schedule, dunning messaging, when access degrades, and when data is retained but locked. (Stripe Smart Retries' recommended default is 8 tries within 2 weeks; the state after the last retry is a setting: `canceled`, `unpaid`, or stay `past_due`)
- **Webhook delivery**: out-of-order events, duplicates, and events for objects the app has not created yet. Do not assume events arrive in order, and do not use `created` to order them (snapshot events record it in seconds, so events can share a timestamp). Dedupe on the event id. Then, in one transaction, lock the local subscription row, fetch the current subscription from the API, and apply the change. Set a short timeout on the API call so the lock is held only briefly.
- **Delayed-confirmation payment methods** (for example ACH Direct Debit): the subscription can be `active` before funds settle, and a later failure voids the invoice while the subscription stays `active`; never read `active` as paid.
- **Refunds and chargebacks**: partial refunds, and whether a chargeback revokes access immediately.
- **Trial abuse**: repeated trials per card, email, or tenant.
- **Currency and tax**: rounding, tax-inclusive vs exclusive display, and invoice fields required for the jurisdiction.
- **Cancellation timing**: immediate vs end-of-period, and what happens to seats and data.

## Guardrails

- Every webhook handler is **idempotent**, keyed on the processor's event id. Assume at-least-once delivery.
- Verify the processor's webhook signature before processing any event; reject events that fail verification.
- The processor is the source of truth for payment state. Reconcile rather than infer.
- Never grant entitlement from a client-side success callback. Wait for the server-side event.
- Treat a webhook as a hint. Fetch the current object from the processor's API before you change access, because the event can be older than the object.
- Log the payment, invoice, subscription, and refund ids on every billing action for support recovery.
- Provide a manual support path to fix a stuck account without direct database editing.
- Do not test billing changes only on the happy path. Also test a masked copy of production subscriptions: old plans, legacy currencies and `past_due` accounts.

## Payment integration checks

- Money is an integer in minor units plus a currency code, never a float. Zero-decimal currencies (for example JPY) change the factor. Three-decimal currencies (for example KWD) change it too.
- Every money mutation (charge, refund, plan change) carries an idempotency key derived from the business operation (order id plus attempt), not a random id per HTTP call. Keys expire on the processor's side, so a retry days later is a new request and can charge twice. Store each key with its operation.
- Card numbers never reach your server; use hosted fields or SDK tokenization to stay in the smallest PCI scope.
- Store the verified webhook event before acknowledging it, and mark it done only after processing succeeds, so a crash replays safely.
- Reconcile processor payouts against the internal ledger daily and alert on drift. Test with the processor's failure cards (decline, 3DS challenge, dispute), not only the success card.
- Pin the processor's API version in code for API calls (Stripe: the SDK's pinned version or the `Stripe-Version` header). Webhook event structure follows the API version of its event destination, or the account's API version, not the pin used for API calls, so check each webhook field against that version before you read it.

## Output format

```text
Processor: [Stripe / other, and API version if it matters]
State model:
  Payment states: [list]
  Entitlement states: [list]
  Mapping: [payment -> entitlement]

Findings:
  P0/P1/P2 - [flow] - [failure] - [fix]

Webhook handling: [events consumed, idempotency key, retry behavior]
Reconciliation: [how drift is detected and corrected]
Support recovery: [how a human fixes a stuck account]
Verification: [tests run; on Stripe, a sandbox test-clock simulation through trial end, renewal, a failed payment, and a mid-cycle plan change, with each webhook handled exactly once]
```

## References

- `../../references/checklists/saas-billing-ops-checklist.md`
- `../../references/checklists/engineering-quality-bar.md`

Adapted from engineering/engineering-payments-billing-engineer.md (agency-agents, MIT).
