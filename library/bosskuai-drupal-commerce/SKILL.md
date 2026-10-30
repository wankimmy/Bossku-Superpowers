---
name: bosskuai-drupal-commerce
description: "Use when building or auditing a Drupal Commerce store: product and variation model, price resolvers, checkout panes, payment gateway webhooks, order workflow, tax, promotions and safe deployment."
---

# BosskuAI Drupal Commerce

Use this skill for a Drupal 10/11 storefront where prices must be right, orders must not vanish, and payments must reconcile.

## How this differs from nearby skills

- **`bosskuai-laravel-development`** and other framework skills: different stack; use them for non-Drupal shops.
- **`bosskuai-customer-billing-ops`** and **`bosskuai-saas-billing-ops`**: operating subscriptions and refunds through billing tools, not building a storefront.
- **`bosskuai-web-performance`**: general caching and Core Web Vitals; here caching is only the cart and checkout rule.
- **`bosskuai-cybersecurity-risk`**: wider security review; here security covers secrets, webhook verification and PCI scope.

## Workflow

1. Model the catalog: product types, variation types, attributes, SKUs, single or multi-store. Decide stock tracking and currency/tax inclusion early.
2. Pricing: resolve all prices through the Commerce price resolver chain. Do not compute totals in Twig or cart subscribers. Store money as amount plus currency, never a float. Prices read from the database can come back as strings, and gateways often want minor units (cents), so convert once, at the edge.
3. Checkout: extend Commerce flows and panes. A custom pane validates input, is idempotent, logs failures, and must not block the order for a non-critical error.
4. Payments: test against the gateway sandbox. Support the operations you need (authorize, capture, void, refund). Verify every webhook signature, handle duplicates, and log each event. Never rely on the customer's browser returning to the success URL.
5. Tax and promotions: configure through Commerce so rates and rules are auditable. Document stacking rules and test combined discounts.
6. Orders: define the workflow states to match fulfilment, including failure states. Transition orders and payments; do not delete them.
7. Stock: decrement atomically at the right workflow point (usually payment), not on add-to-cart. Two checkouts can take the last unit, so use one conditional update that changes a row only when enough stock is left (for example `WHERE stock >= :qty`). If no row changes, fail the checkout and void any payment authorization. Never read the stock first and write after. Run this update before the gateway captures the payment.
8. Deploy in sequence (database updates, config import, cache rebuild) with a tested rollback. Read the installed versions with `composer show drupal/core` and `composer show drupal/commerce`, and check the latest Drupal release and support dates at drupal.org at work time. Keep old code working on the new schema until the rollout ends, and test the rollback on a copy of production first.

## Guardrails

- Gateway credentials stay in environment variables or a secrets manager, never committed.
- Test and live mode must be visible and checked on every deploy.
- Cart, checkout and account pages are not publicly cacheable.
- Reconcile orders against gateway settlements; surface mismatches.
- Do not switch a gateway to live mode, capture or refund a real payment, or change production tax or promotion rules without explicit user approval. Confirm tax and PCI obligations with a qualified adviser.
- Full quality bar: `../../references/checklists/engineering-quality-bar.md`.

## Output format

```text
Catalog model: [product types, variations, stock]
Pricing path: [resolvers, currency, tax mode]
Checkout flow: [steps, custom panes]
Payment spec: [gateway, mode, webhook handling, reconciliation]
Order workflow: [states, transitions]
Go-live checklist: [credentials, mode, test capture and refund, deploy order]
```

Adapted from agency-agents/engineering/engineering-drupal-shopping-cart.md (agency-agents, MIT).
