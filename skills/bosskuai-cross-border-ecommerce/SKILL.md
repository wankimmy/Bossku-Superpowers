---
name: bosskuai-cross-border-ecommerce
description: "Use when selling physical products across borders on Amazon, Shopee, Lazada, AliExpress, Temu or TikTok Shop: product selection, landed-cost margin, compliance checklist, logistics, localisation and ads."
---

# BosskuAI Cross-Border E-Commerce

Use this skill to evaluate and launch a product in an overseas marketplace, with margin, compliance and localisation checked before any listing goes live.

## How this differs from nearby skills

- **`bosskuai-china-ecommerce-operator`**: operating inside China's domestic platforms, not exporting.
- **`bosskuai-customs-trade-compliance`**: deep HS classification, duties and entry documents. Use it when customs detail is the main problem; this skill only lists the questions to ask.
- **`bosskuai-inventory-demand-planning`**: forecasting and reorder maths for stock you already carry.
- **`bosskuai-paid-acquisition-monetization`** and **`bosskuai-seo-geo`**: generic ads and search work; this skill covers marketplace-specific structure.

## Workflow

1. Research the market: search volume, competition on page one, price range, seasonality, trend. Use current data from whichever research tools the user has.
2. Score the product on three dimensions: market, margin, compliance. Drop it if any one fails.
3. Build a full landed-cost sheet per SKU: procurement, first-mile freight, storage and fulfilment, platform commission, advertising, returns allowance, payment fees, FX movement.
4. Check compliance for the target market: required product certifications, tax registration and filing, packaging and recycling rules, import duty, trademark and patent risk, prohibited categories on the platform.
5. Choose fulfilment: platform warehouse, third-party overseas warehouse, or merchant-fulfilled, based on speed, cost and returns handling.
6. Localise the listing with native-speaker review. Adapt images, packaging, price and support hours to the market.
7. Phase advertising by launch, growth and mature stages, and set a ceiling so ad cost never exceeds gross margin.
8. Start with a small first shipment, watch results, then widen. Model the startup cost of each new marketplace before entering it.

## Guardrails

- Check current platform rules, tax law and certification requirements with official sources. This skill is a work checklist, not tax, customs or legal advice; a qualified adviser must confirm obligations before listing.
- No fake reviews, review manipulation, linked accounts, counterfeit goods, hijacked listings or unlicensed brand assets.
- Product descriptions must be truthful. Machine translation without native review is a conversion and legal risk.
- Do not register accounts, file taxes, buy inventory or place ads without the user's explicit approval.

## Output format

```text
Product and market: [product, marketplace, evidence]
Scorecard: [market / margin / compliance, each pass or fail]
Landed cost: [per-unit breakdown, net margin]
Compliance list: [item, owner, status]
Fulfilment plan: [route, first batch size]
Launch and ad plan: [phases, ceiling]
```

Adapted from agency-agents/marketing/marketing-cross-border-ecommerce.md (agency-agents, MIT).
