---
name: bosskuai-healthcare-marketing-compliance
description: "Use when reviewing China healthcare marketing before publishing: drug, device, medical-aesthetics, health-supplement, and internet-healthcare content, ad claims, patient privacy, academic detailing, and platform rules."
---

# BosskuAI Healthcare Marketing Compliance (China)

Use this skill to run a structured pre-publication review of healthcare marketing content in China and to organise the evidence a qualified reviewer needs.

## How this differs from nearby skills

- **`bosskuai-hipaa-compliance`** and **`bosskuai-healthcare-phi-compliance`**: US health-data privacy and software controls. This skill covers Chinese advertising, product-category, and platform rules for marketing.
- **`bosskuai-legal-compliance`**: product privacy and legal readiness in general. Use it for the privacy side of non-health products.
- **`ads`** and **`ad-creative`**: writing and running ad campaigns. This skill is the compliance gate before they go out.
- **`bosskuai-douyin-strategist`**: platform growth tactics; use this skill to check the wording that strategy produces.
- **`bosskuai-healthcare-cdss-patterns`**, **`bosskuai-healthcare-emr-patterns`**: clinical software, not marketing.

## Workflow

1. Classify the content: advertisement, health education, patient education, academic promotion, or brand publicity. Classify the product: drug (prescription or OTC), device (class), medical-aesthetics procedure, health supplement, or medical service.
2. Qualification check: advertising approval or review number valid and unexpired, publisher's licences present, platform industry certification done, physician credentials verified if a clinician appears.
3. Claim check: absolute claims, guarantees, efficacy rates without cited source, comparisons with other products or institutions, patient or celebrity endorsement, fear or urgency language, and "appearance anxiety" wording for aesthetics.
4. Scope match: indications, intended use, model, and function claims must match the approved label, registration certificate, or filing exactly. No off-label or unregistered-product promotion.
5. Category rules: prescription products are limited to professional channels; supplements must keep required declaration text and stay within registered functions; aesthetics content has extra limits (for example on before-and-after material). Confirm each against the current regulation text.
6. Privacy: patient information, consent, de-identification, minimum necessary collection, health data in CRM, cross-border transfer. Check current personal-information and data-security rules.
7. Academic and rep activity: sponsorship written agreements, speaker fees, gifts and travel within the company's and industry codes, representative duties.
8. Platform check: confirm each platform's current healthcare rules for ads, livestreams, doctor accounts, and commercial labels.
9. Record the review: findings, required changes, approver, date. Define takedown and response steps for a discovered violation.

## Guardrails

- This skill organises review work and evidence. It is not legal or regulatory advice. Laws, approval rules, penalties, and platform policies change; verify against current official text, and have a qualified compliance professional or counsel make the final decision.
- Do not publish, submit approvals, or contact regulators or platforms without explicit user approval.
- Do not suggest ways to evade advertising review, disguise advertising as education, or collect patient data without consent.
- Treat fine amounts and examples in any source as unverified until checked against the current law.

## Output format

```text
Content / channel / product category: [..]
Qualification check: [item - status]
Findings: | Text | Issue | Risk level | Suggested compliant wording |
Privacy check: [consent, de-identification, data use]
Platform check: [platform - rule source - result]
Decision: approve / approve with changes / reject
Reviewer and date: [qualified human required]
```

Adapted from agency-agents/specialized/healthcare-marketing-compliance.md (agency-agents, MIT).
