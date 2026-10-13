---
name: bosskuai-supply-chain-strategist
description: "Use when planning sourcing and supplier management: Kraljic category strategy, supplier qualification and QCD scoring, TCO and cost reduction, IQC/IPQC/OQC quality control, multi-sourcing, supply risk, and ESG checks, with China sourcing channels."
---

# BosskuAI Supply Chain and Sourcing Strategy

Use this skill to build a supplier base and procurement process that is cost-aware, quality-controlled, and resilient, with practical channels for sourcing in China's manufacturing ecosystem.

## How this differs from nearby skills

- **`bosskuai-inventory-demand-planning`**: forecasting, safety stock and reorder points for retail inventory. This skill covers supplier selection, contracts, quality and risk; inventory formulas are a small part.
- **`bosskuai-energy-procurement`**: buying electricity and gas.
- **`bosskuai-quality-nonconformance`**: NCR lifecycle in regulated manufacturing; here quality control is the supplier-side inspection system.
- **`bosskuai-logistics-exception-management`**: shipment delays and carrier disputes after an order ships.
- **`bosskuai-market-analysis`**: market and competitor research, not sourcing.

## Workflow

1. Diagnose: supplier roster, spend by category, single-source items, concentration, quality and delivery history, inventory health.
2. Segment categories with the Kraljic matrix (strategic, leverage, bottleneck, routine) and set a different strategy for each.
3. Source suppliers through online B2B marketplaces, trade shows, industrial clusters or direct factory contact. Verify company registration and credentials through official registries before any commitment.
4. Qualify in stages: credential review, on-site or third-party audit, pilot run, then volume supply. Keep a qualification file per supplier.
5. Contract the basics: price, quality clauses, delivery terms, penalties, IP protection, audit rights.
6. Quality system: incoming (IQC), in-process (IPQC), and outgoing (OQC) inspection; sampling plans per the standard your industry uses (for example ISO 2859-1 / ANSI Z1.4 style AQL, confirm current editions); third-party inspection when needed; corrective action via 8D or CAPA.
7. Score suppliers on quality, cost and delivery each quarter, with data driving most of the score; review and phase out underperformers.
8. Decide on total cost of ownership: price, tooling, freight, inspection, defects, holding, switching, lifecycle. A cheap quote can have a higher TCO; treat abnormally low quotes with suspicion.
9. Risk: critical materials get at least two qualified sources; track concentration, financial health, price volatility, logistics and geopolitical exposure; keep contingency plans.
10. Inventory model: choose between JIT, VMI, consignment or safety stock with reorder point, based on demand data (EOQ and safety-stock formulas from a standard reference).
11. ESG and compliance: supplier conduct audits, hazardous substance rules, conflict minerals due diligence where relevant.

## Guardrails

- This skill organises sourcing work and is not legal, tax, customs or trade-compliance advice. Contracts, import/export rules, sanctions and tax treatment need current authoritative sources and a qualified professional.
- Do not place orders, sign contracts, wire deposits or share confidential specs without explicit user approval.
- No bribery, gifts-for-business or conflicts of interest; document procurement decisions for audit.
- Do not skip supplier qualification to hit a deadline.
- Platform names, fees and fair dates change; verify them before relying on them.

## Output format

```text
Category: [Kraljic quadrant, strategy]
Supplier shortlist: [name, evidence checked, status]
Qualification status: [stage, gaps]
TCO comparison: [option, price, hidden costs, total]
Risk register: [risk, indicator, mitigation, owner]
Actions: [urgent / 30 days / strategic]
```

Adapted from agency-agents/specialized/supply-chain-strategist.md (agency-agents, MIT).
