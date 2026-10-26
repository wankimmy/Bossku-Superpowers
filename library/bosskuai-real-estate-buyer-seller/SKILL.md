---
name: bosskuai-real-estate-buyer-seller
description: "Use when organising a residential property purchase or sale: buyer needs checklist, comparable-sales review, listing prep, offer terms comparison, deadline tracker, and closing and wire-fraud safeguards."
---

# BosskuAI Real Estate Buyer and Seller

Use this skill to keep a property transaction organised for either side: criteria, comparables, offers, contingencies, deadlines, and closing tasks.

## How this differs from nearby skills

- **`bosskuai-financial-modeling`**: models and cash-flow projections. Use it for deeper investment return analysis.
- **`bosskuai-legal-compliance`**: product legal readiness. Property contracts need a local lawyer or licensed agent.
- **`bosskuai-master-agreement-generator`**: drafting commercial agreements, not property transactions.
- **`bosskuai-esign-field-placement`**: placing signature fields on documents.
- **`bosskuai-sales-strategy`**: B2B revenue motion.

## Workflow

1. Clarify the role (buyer or seller), jurisdiction, property type, budget or target price, timeline, and who is the licensed professional on the file.
2. Buyer intake: financing status, price range, must-haves, nice-to-haves, deal-breakers, location and commute needs, timeline and whether a sale of another property is needed first, communication preferences.
3. Seller intake: motivation, timeline, condition and recent work, repairs to consider, documents needed (disclosures, owner association papers, bills).
4. Comparable market review: pull recent sold, pending, and active comparables from an authoritative local source. Adjust for size, condition, and location with the reason stated. Report months of inventory, days on market, and sale-to-list ratio with the source and date. Do not state a value without sourced comparables.
5. Offer comparison: price versus list and versus comparables, earnest money and where it is held, financing type, contingencies (inspection, financing, appraisal, home sale) with deadlines, closing and possession dates, concessions, and any escalation terms. Show strengths and weaknesses of each offer; the client decides.
6. Listing prep (seller): pricing strategy agreed, condition and staging plan, photography, required disclosures, marketing tasks, showing instructions, feedback log reviewed regularly against price and condition.
7. Deadline tracker: earnest money, inspection window, response to inspection, financing commitment, appraisal, contingency removals, final walkthrough, closing disclosure review, closing and possession. Record each in writing and mark who is responsible.
8. Closing: confirm logistics, funds needed, keys and codes, utility transfers. Send the wire-fraud warning: never wire funds on email instructions alone; call the title or escrow company on a number you verified independently.

## Guardrails

- Not legal, tax, lending, or valuation advice. Contract terms, disclosure duties, fees, taxes, and timelines vary by country and state (in Malaysia, for example, stamp duty and legal fees apply). Confirm with current authoritative sources and a qualified lawyer, licensed agent, or lender before acting.
- Never disclose a client's maximum budget or motivation to the other side without the client's consent.
- Apply fair-housing and anti-discrimination rules: show all properties that meet the stated criteria, and do not steer by protected class.
- Disclose known material defects. Do not pressure the client or miss contract deadlines.
- Do not submit offers, sign, move earnest money, or send wires for a real client without their explicit approval.

## Output format

```text
Role/jurisdiction: [buyer/seller, place, professional of record]
Criteria or listing plan: [key items]
Comparables: [address, price, date, adjustments, source]
Offer table: [terms side by side, risks]
Deadlines: [item, date, owner, status]
Closing safeguards: [wire warning, walkthrough, disclosures]
```

Adapted from agency-agents/specialized/real-estate-buyer-seller.md (agency-agents, MIT).
