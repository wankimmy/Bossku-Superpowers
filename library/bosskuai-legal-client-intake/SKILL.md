---
name: bosskuai-legal-client-intake
description: "Use when designing or running a law firm's new-client intake: urgency screen, practice-area qualification, conflict check data, case information form, referral-out script and an attorney-ready intake summary."
---

# BosskuAI Legal Client Intake

Use this skill to structure the first contact between a law firm and a prospective client so that urgent deadlines are caught, conflicts are screened, and the attorney gets a clear brief.

## How this differs from nearby skills

- **`bosskuai-legal-compliance`**: product-facing legal readiness (privacy, consent, retention). This skill is a firm's intake process.
- **`bosskuai-master-agreement-generator`**: drafting agreements, not intake.
- **`bosskuai-customer-success-support`** and **`bosskuai-lead-intelligence`**: general support and lead research; intake adds conflict screening and privilege sensitivity.
- **`bosskuai-malaysia-pdpa-privacy`**: personal data obligations for how intake data is stored.

## Workflow

1. Greet, take the name, and screen for urgency early: court dates, filing deadlines, safety concerns. Escalate urgent items to an attorney immediately.
2. Let the prospect describe the situation before structured questions. Ask one question at a time, in plain language.
3. Qualify: does the firm handle this matter type, in this jurisdiction, at this size? If not, refer out gracefully with specific options.
4. Conflict data: full name and aliases, business entities, every adverse party, prior dealings with the firm. Record status as pending, cleared, potential, or conflict. Do not schedule until the responsible attorney or supervisor clears it.
5. Collect facts: who, what, when, where, key dates, any filed action, opposing counsel, available documents, the prospect's goals, and fee-structure questions.
6. Time limits: flag any matter where a limitation period may apply and have the attorney confirm the actual rule for the jurisdiction. Do not quote limits from memory.
7. Schedule with the right attorney, confirm format and what to bring, and send a confirmation.
8. Deliver the intake summary to the attorney before the consultation. End every contact with a confirmed next step.

## Guardrails

- This skill organises intake. It is not legal advice. Never tell a prospect whether they have a case, what the law says, or what to do; the attorney decides, and a qualified human reviews every urgency and conflict call.
- Never promise outcomes.
- Treat everything shared as confidential from first contact, and store it under the firm's data-protection rules.
- Do not send messages, book appointments or record a conflict as cleared on a real matter without explicit user approval.
- Apply the same process to every prospect.

## Output format

```text
INTAKE SUMMARY
Prospect and contact: [name, method, referral source]
Conflict status: [pending / cleared / potential / conflict]
Matter: [area, summary in the prospect's words, key dates]
Urgency flags: [deadline, hearing, safety, other]
Parties: [client role, adverse parties, counsel]
Documents and goals: [list]
Fee discussion: [done or not, questions]
Next steps: [attorney action, follow-up]
```

Adapted from agency-agents/specialized/legal-client-intake.md (agency-agents, MIT).
