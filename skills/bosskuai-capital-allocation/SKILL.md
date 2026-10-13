---
name: bosskuai-capital-allocation
description: "Use when ranking investments or capex against a hurdle rate, stress-testing a budget or forecast, checking covenant and cash headroom, or preparing a board finance pack: NPV/IRR, WACC, downside cases."
---

# BosskuAI Capital Allocation

Use this skill to compare capital decisions on risk-adjusted return and liquidity, and to prepare a finance pack the numbers of which can be traced and defended.

## How this differs from nearby skills

- **`bosskuai-financial-modeling`**: startup revenue, runway, and unit-economics models. This skill is the decision layer above: which investments to fund, against what hurdle, with what cash headroom.
- **`bosskuai-investor-prep`**: fundraising materials. This skill is about deploying capital, not raising it.
- **`bosskuai-investment-research`**: researching an outside company or asset. Here the money is the organisation's own projects, capex, or M&A.
- **`bosskuai-cost-optimization`**: cutting cloud and vendor spend.
- **`bosskuai-finance-billing-ops`**: revenue and billing operations, not capital decisions.

## Workflow

1. State the decision, the options (including do nothing), the horizon, and the owner.
2. Liquidity first: current cash, 13-week cash view, debt covenants and headroom. A decision that breaches covenants or near-term runway fails before returns are discussed.
3. Classify each option: maintain the core, grow the core, extend the core, or transform. Maintenance and compliance spend is not discretionary.
4. Build base, downside, and upside cases with the assumptions written down. A single-point forecast is not enough.
5. Compute NPV, IRR, and payback. Choose the discount rate from the organisation's cost of capital plus a risk premium that you justify. Show the WACC inputs (cost of equity, after-tax cost of debt, target weights) and their sources.
6. Compare against the hurdle for that class of project and against alternative uses of the same money. Run sensitivity on the two or three assumptions that move the answer most.
7. For M&A, add: strategic fit, valuation cross-checks (DCF and comparables), diligence workstreams (financial, tax, legal, commercial, operations, people), and the bridge from enterprise value to equity value.
8. Prepare the pack: headline, key numbers versus budget and prior period, cash and leverage, outlook, top risks with mitigants. Every figure reconciles to a source.

## Guardrails

- This skill organises analysis and evidence. It is not financial, tax, accounting, audit, or legal advice. Conclusions need current authoritative sources and review by a qualified finance professional, auditor, tax adviser, or counsel.
- No action on a real account, transaction, filing, or disclosure without explicit user approval.
- Hurdle rates, leverage limits, and benchmarks differ by sector and lender. Take them from the organisation's policy and facility documents, not from this skill.
- Do not shape figures to hit a target (pulling revenue forward, selective disclosure). Surface the problem instead.

## Output format

```text
Decision: [options, horizon, owner]
Liquidity check: [cash, covenants, headroom]
Cases: [base / downside / upside, key assumptions]
Returns: [NPV, IRR, payback, discount rate and why]
Sensitivity: [assumption - effect on NPV]
Recommendation: [choice, what we give up, review date]
Open items: [data to verify, reviewer]
```

Adapted from agency-agents/specialized/chief-financial-officer.md (agency-agents, MIT).
