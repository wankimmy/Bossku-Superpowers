---
name: bosskuai-stakeholder-questionnaire
description: "Use when you cannot answer a decision alone and need someone else's knowledge: interview yourself about who and what you need, then write a discovery questionnaire in Markdown for them to fill in."
---

# BosskuAI Stakeholder Questionnaire

Use this skill to turn "I need an answer from someone else" into a short Markdown questionnaire the recipient can fill in alone or in a meeting. The questions target the gap between what the recipient knows and what you need, not the topic in general.

## How this differs from nearby skills

- **`bosskuai-customer-discovery`**: a full interview programme with hypotheses, recruiting, and transcript tagging. This skill makes one document for one recipient.
- **`customer-research`**: research with many customers. This is one stakeholder, one decision.
- **`bosskuai-grill-with-docs`**: stress-tests a plan against your own domain docs. Here the knowledge is in someone else's head.
- **`brainstorming`**: explores a design with the user. This skill produces a document to send out.

## Workflow

1. Who is it going to? In one exchange, ask the recipient's role, expertise, and relationship to the user. This sets tone and how much context to include. Done when you know who they are and what they know that the user does not.
2. What do you need back? In one exchange, ask which decisions or facts the user cannot settle alone. Done when there is a concrete list of what the user must be able to decide or do afterwards.
3. Draft the questionnaire from that gap. Order questions most-important-first, since you may get only one pass. Group by theme under `##` headings once there are more than a few.
4. Check coverage: every item from step 2 maps to at least one question. Each question is one idea, not compound.
5. Write it to `to-questionnaire-<slug>.md` in the working directory (or where the user says) and report the path.

## Document template

```markdown
# <Title>

**Purpose:** why this exists and the decision riding on it.
**From:** <user>, **To:** <recipient>, **How your answers will be used:** <where they go>

## Context
One short paragraph for someone who was not in your head.

## How to answer
Deadline and rough effort. Partial answers and "I don't know" are useful.

## <Theme>
### <One question, one idea>
_Why this matters: one line, only where the question could be misread._

>

## Anything else?
Anything we did not ask that we should know?
```

## Guardrails

- Interview the user only about the send (who, what back). Do not quiz them on the subject they admit they cannot answer.
- Do not put secrets, personal data, or confidential figures in the document unless the user confirms the recipient may see them.
- Do not send the questionnaire. Writing the file is the end of this skill.
- Keep it short enough to finish. Cut questions that do not change the decision.

Adapted from mattpocock/skills/skills/productivity/to-questionnaire/SKILL.md (mattpocock/skills, MIT).
