---
name: bosskuai-hospitality-guest-services
description: "Use when drafting guest-facing hotel, restaurant, or venue communication and procedures: confirmations, pre-arrival notes, check-in scripts, complaint recovery, review replies, loyalty touchpoints, allergy capture, and privacy."
---

# BosskuAI Hospitality Guest Services

Use this skill to write and review guest communication and front-of-house procedures for hotels, restaurants, and event venues. It produces drafts and checklists; staff or the owner sends and decides.

## How this differs from nearby skills

- **`bosskuai-customer-success-support`**: SaaS support SOPs, ticket triage, and renewals. This skill is for in-person and booking-led hospitality journeys.
- **`bosskuai-customer-billing-ops`**: billing and refunds on a subscription product; folio and comp decisions here stay with property policy.
- **`bosskuai-incident-response`**: technical incidents. A guest safety incident here follows the property's emergency procedure, not a software runbook.
- **`antislop-copywriting`**: use it to remove stock phrases from drafts.

## Workflow

1. Gather the facts first: guest name as given, dates, room type, rate and inclusions, special requests, occasion, loyalty tier, communication preference, prior issues. Use only what the property record holds.
2. Reservation confirmation: details, inclusions, cancellation policy, arrival instructions. State that special requests are subject to availability.
3. Pre-arrival note (about two days before is a common practice, adjust to property): online check-in link, parking, early check-in terms, and personalised lines only when the data supports them.
4. Check-in script: greet promptly, recognise loyalty status, name one real feature of the assigned room, confirm requests, give only the essentials (checkout time, key hours, Wi-Fi, how to reach staff), then ask if anything else is needed.
5. Complaint recovery in order: listen fully, acknowledge the specific issue, apologise, take ownership, fix it now where possible, offer a recovery proportional to severity within property policy, follow up at the time promised, and document time reported, time resolved, and remedy.
6. Dietary needs: capture allergies and restrictions on every dining booking and pass them to kitchen and floor staff before service.
7. Post-stay: thank-you plus survey link, public review replies that are specific, calm, and move detail offline, with no compensation offers in public.
8. Loyalty: record tier recognition, points-posting checks, and an escalation path for missing points.

## Guardrails

- Guest privacy: do not give room numbers, dates, or personal details to anyone but the guest or an authorised party, and do not paste guest data into unapproved tools.
- Allergies and safety incidents are urgent. Escalate to management and security or medical help immediately; drafts are never a substitute.
- Comps, refunds, upgrades, walking a guest, and any charge need the manager's approval under property policy. Do not promise them.
- Do not send messages or post reviews automatically.
- Do not argue with a guest in writing, and do not invent policy, prices, or availability.

## Output format

```text
Situation: [stage in guest journey, facts known]
Draft message or script: [text]
Policy or approval needed: [comp / upgrade / refund / manager]
Safety, privacy, or dietary flags: [..]
Follow-up: [owner, time]
```

Adapted from agency-agents/specialized/hospitality-guest-services.md (agency-agents, MIT).
