---
name: bosskuai-investment-research
description: "Use when researching a company or asset for an investment view: thesis with bull and bear cases, valuation scenarios, due-diligence checklist, catalysts, and thesis-breaker monitoring from primary sources."
---

# BosskuAI Investment Research

Use this skill to structure research on a listed company, private company, or asset so the thesis is testable, the downside is quantified, and the sources are primary.

## How this differs from nearby skills

- **`bosskuai-capital-allocation`**: an organisation deciding how to spend its own capital. This skill evaluates an outside investment.
- **`bosskuai-deep-research`**: general multi-source research and synthesis. Use it for broad evidence gathering; this skill supplies the investment structure (thesis, valuation, thesis breakers).
- **`bosskuai-financial-modeling`**: forward models for a startup's own finances.
- **`bosskuai-investor-prep`**: raising money from investors; the reverse direction.
- **`bosskuai-prediction-market-risk-review`**: prediction-market positions, a narrower setting.

## Workflow

1. Define the question: asset, investment horizon, and what decision the research supports.
2. Screen: pull the last three years of statements, filings, and call transcripts from primary sources (regulator filings, company reports). Rough valuation range to decide whether a deep dive is worth it.
3. List the three to five questions that decide the outcome.
4. Business and moat: market size built bottom-up, competitive position, switching costs, scale or network effects, management incentives and capital-allocation record.
5. Financial quality: revenue mix and concentration, earnings quality and cash conversion, balance sheet, off-balance-sheet items, working capital, capital intensity.
6. Valuation: scenario DCF (bull, base, bear with stated weights), plus peer multiples as a cross-check. Show which assumptions drive the value.
7. Write the bear case with the same rigor as the bull case, with quantified downside.
8. Define thesis breakers: specific metrics or events that would invalidate the view, and a date or frequency to check them.
9. Due diligence (private or M&A): financial, operational, market, and legal checklists with a red-flag table (finding, severity, impact, action).
10. Update when new facts arrive. Record what changed and why.

## Guardrails

- This is research organisation, not investment advice. Conclusions need current authoritative data and review by a qualified professional. State the confidence level and the evidence quality.
- Cite primary sources. Mark anything from secondary summaries, social media, or unverified data as unverified.
- Do not place orders, move money, or contact third parties (customers, management) on the user's behalf without explicit approval.
- Past performance and model output are not predictions. Show ranges, not a single price target, unless the user asks for one and the assumptions are visible.
- Check data-vendor terms before redistributing licensed data.

## Output format

```text
Asset / horizon / confidence: [..]
Thesis: [2-4 sentences, why now]
Bull drivers: [quantified]   Bear risks: [quantified, mitigations]
Catalysts: [event, timing, probability]
Valuation: [scenarios, weights, key assumptions, comps]
Thesis breakers: [metric/event - threshold]
Red flags: [finding - severity - action]
Sources and unverified items: [..]
```

Adapted from agency-agents/finance/finance-investment-researcher.md (agency-agents, MIT).
