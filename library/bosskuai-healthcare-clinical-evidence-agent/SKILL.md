---
name: bosskuai-healthcare-clinical-evidence-agent
description: "Use when writing or auditing clinical claims for decks, grants, papers, or product copy: classify each claim as validated, directional, or unvalidated, add sources, and keep decision support from sounding like diagnosis."
---

# BosskuAI Clinical Evidence Agent

Use this skill to keep outward-facing healthcare writing honest: every clinical claim has a source or a flag, and the product is never framed as making diagnoses.

## How this differs from nearby skills

- **`bosskuai-healthcare-cdss-patterns`**: how to build decision-support software (interaction checks, scoring). This skill covers how to describe and evidence its claims.
- **`bosskuai-healthcare-eval-harness`**: automated patient-safety tests for an app. Here the artefact is a document, not a test suite.
- **`bosskuai-healthcare-phi-compliance`** and **`bosskuai-hipaa-compliance`**: privacy and health-data handling.
- **`bosskuai-legal-compliance`**: general legal readiness; regulatory claims review still needs counsel.
- **`bosskuai-grounding`** (always on): general source discipline; this skill adds clinical categories.

## Claim classes

- **Validated**: from a peer-reviewed study, a prospective dataset with documented methods, official labelling or a systematic review, or confirmed in writing by a named licensed physician reviewer. Cite it.
- **Directional**: from internal data not peer reviewed, a small or limited pilot, or extrapolation from adjacent research. Say so in the sentence ("our operational data suggests ...").
- **Unvalidated**: model output without clinical review, extrapolation beyond the data, or analogies from other markets. Keep out of external documents; label as assumptions internally.

## Workflow

1. For a new claim: state it in one sentence, find the source, classify it, then cite, qualify, or flag it. If unsure, ask.
2. For an existing document: read it all first, mark every clinical claim, classify each, list unvalidated ones for the clinical lead, add qualifiers to directional ones, confirm citations on validated ones, and return the clean text plus a flag list.
3. Write for the strictest audience first (peer review), then adapt wording per audience: reviewers (method, confidence intervals), investors (sourced outcomes), regulators (scope and limits), physicians (workflow value), patients (plain language). Keep the evidence identical across versions; do not mix framings in one document.
4. Decision-support framing: say what the tool surfaces and who decides. Avoid phrases that imply autonomous diagnosis, treatment recommendation, or prescribing.
5. Put forward-looking projections in a separate section; never in the same sentence as a validated finding.

## Guardrails

- This skill organises evidence and wording. It is not medical advice and does not decide clinical questions. Conclusions need current authoritative sources and review by a licensed clinician; regulatory positioning needs qualified legal or regulatory review.
- Do not submit, publish, or send any filing, deck, or manuscript on a user's behalf without explicit approval.
- Never invent a citation, statistic, or study. If a source cannot be found, mark the claim unvalidated.
- Follow the user's or organisation's preferred terminology for clinicians; do not force one term.

## Output format

```text
Claim: [text]  Class: validated | directional | unvalidated
Source: [citation or "none found"]
Action: [keep / qualify / remove / needs physician review]
Audience version: [peer review | investor | regulator | physician | patient]
Flag list for clinical lead: [..]
```

Adapted from agency-agents/healthcare/healthcare-clinical-evidence-agent.md (agency-agents, MIT).
