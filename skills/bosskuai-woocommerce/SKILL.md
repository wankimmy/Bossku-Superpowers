---
name: bosskuai-woocommerce
description: "Use when building or fixing a WooCommerce store: product and variation setup, checkout customisation via hooks or blocks, payment gateway and webhook handling, tax and coupon rules, order statuses, cart caching."
---

# BosskuAI WooCommerce

Use this skill to customise WooCommerce so checkout stays correct, payments reconcile, and updates do not undo the work.

## How this differs from nearby skills

- **`bosskuai-product-verification`**: proving a signup or checkout journey works. Use it for the final test; this skill is how to build and fix the store.
- **`bosskuai-cybersecurity-risk`**: security review in general. Secrets and payment-mode rules here are the commerce subset.
- **`bosskuai-web-performance`**: Core Web Vitals and caching in general; here the cache rules protect cart and checkout pages.
- **`bosskuai-database-engineering`**: database design; WooCommerce stores data through its own APIs and order storage.
- **`bosskuai-social-publisher`**, **`ads`**: marketing channels that bring traffic, not store mechanics.

## Workflow

1. Discover: WordPress, WooCommerce, and PHP versions; theme and plugins touching cart, checkout, or payment; checkout type (block or classic); order-storage mode; tax mode (prices entered with or without tax); gateways and whether each is in test or live mode.
2. Product model: choose product type per item, define attributes before generating variations, decide stock management and when stock reduces.
3. Customise through hooks, filters, or the block checkout's documented extension points, in a child theme or a small plugin. Do not edit core or parent theme, and override templates only when markup must change (and note the override).
4. Money: use WooCommerce price and total functions, and respect the store's currency and decimals. Do not do raw float arithmetic on prices.
5. Payments: develop with the real gateway's sandbox. Cover authorize, capture, void, and full and partial refund as the gateway supports. Verify webhook signatures, deduplicate events, log them, and never rely only on the customer returning to the thank-you page.
6. Secrets: keep keys in configuration constants or environment variables, never in committed code or exported settings. Make test versus live mode visible.
7. Tax and coupons: configure rates in WooCommerce settings. Document coupon stacking and test combinations with sale prices, tax, shipping, and refunds.
8. Orders: change state by status transitions and refunds, not deletion. Map custom statuses to fulfillment steps and the hooks they fire.
9. Caching: exclude cart, checkout, and account pages from page and CDN caching. Verify on the live edge.
10. Test the full path on a phone: add to cart, coupon, shipping, tax, pay, email, admin order totals. Reconcile first live orders to the gateway's payout report.

## Guardrails

- Check the installed WordPress and WooCommerce versions and the current developer docs. Hook names and checkout internals change between releases.
- Payment handling touches PCI scope; prefer hosted fields or redirects, and never store card numbers. Have a qualified person confirm compliance obligations.
- Do not run live charges, refunds, or changes on a production store without explicit user approval. Back up before updates.
- A custom field that fails must not block order completion silently.

## Output format

```text
Store facts: [versions, checkout type, tax mode, gateways + mode]
Change: [hook/block/plugin, files]
Payment handling: [operations, webhook verification, logging]
Money and stock checks: [totals, tax, coupon, stock timing]
Cache rules: [excluded pages, verified where]
Test and reconcile: [devices, test charge/refund, payout match]
Rollback: [..]
```

Adapted from agency-agents/engineering/engineering-wordpress-shopping-cart.md (agency-agents, MIT).
