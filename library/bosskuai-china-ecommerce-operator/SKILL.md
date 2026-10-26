---
name: bosskuai-china-ecommerce-operator
description: "Use when planning or reviewing store operations on Taobao, Tmall, Pinduoduo, JD or Douyin Shop: listings, ad structure, live commerce, and 618 or Double 11 campaign plans with margin checks."
---

# BosskuAI China E-Commerce Operator

Use this skill to plan listings, advertising, live commerce and campaign calendars for Chinese marketplaces, with unit economics checked before volume is chased.

## How this differs from nearby skills

- **`bosskuai-cross-border-ecommerce`**: selling from one country into overseas marketplaces (Amazon, Shopee, Lazada). This skill is for operating inside China's domestic platforms.
- **`bosskuai-marketing-growth`**: generic go-to-market and growth loops, not platform-specific store mechanics.
- **`bosskuai-inventory-demand-planning`**: forecasting and safety stock in depth; here inventory only appears as a campaign constraint.
- **`bosskuai-returns-reverse-logistics`**: returns handling after the sale.

## Workflow

1. Assess the platform and category: market size, competition, price distribution, platform fee structure. Do this per platform, not once.
2. Set store architecture: category navigation and the flagship products.
3. Build listings per platform. Titles, image slots and detail-page order differ by platform; check each platform's current character limits and rules before writing.
4. Set pricing from a per-SKU margin waterfall: cost, platform fees, advertising, logistics, returns.
5. Plan traffic: organic search work first, then paid tools sized to a target return per keyword group. Verify current ad product names and options in each platform's console.
6. Plan live commerce: host, script, product sequence, schedule, and how it feeds the campaign calendar.
7. Run campaigns backwards from a date: planning, creative and ad setup, warm-up, burst day, post-campaign review. Confirm the real campaign calendar and mechanics (presale, deposits, cross-store thresholds) on the platform.
8. After the campaign, report traffic source, conversion and ROI by channel, then feed repeat customers into retention.

## Guardrails

- Do not copy one platform's strategy to another. Algorithms, buyers and rules differ.
- Every operational change is backed by data. Do not chase GMV at negative unit margin.
- Respect listing, claim and promotion rules. Violations cause store penalties; check current platform policy and e-commerce law.
- Inventory accuracy and customer-service capacity are campaign constraints. Overselling hurts store ratings.
- Do not place ad spend, change prices or publish listings on a real store without the user's explicit approval.

## Output format

```text
Platforms and goal: [which, target]
Listing plan: [title formula, image slots, detail page order per platform]
Margin check: [per-SKU waterfall result]
Traffic plan: [organic, paid, live, content]
Campaign timeline: [phases with owners and dates]
Review metrics: [conversion, ROI, return rate, inventory]
```

Adapted from agency-agents/marketing/marketing-china-ecommerce-operator.md (agency-agents, MIT).
