---
name: bosskuai-spanish-english-translation
description: "Use when translating between Spanish and English with the right register and region: usted or tu, Mexican versus Castilian wording, phonetic guides, false cognates, and flags for medical or legal text."
---

# BosskuAI Spanish-English Translation

Use this skill for meaning-first translation between English and Spanish, with context, register, and pronunciation help for real conversations and messages.

## How this differs from nearby skills

- **`bosskuai-visa-doc-translate`**: OCR and bilingual output for visa document images. This skill is for everyday, business, travel, and written messages.
- **`bosskuai-i18n-l10n`**: localising a product (strings, formats, RTL). This skill translates a given text or phrase set.
- **`bosskuai-article-writing`**: writing long-form pieces in a voice, not translation.
- **`bosskuai-bengali-nlp`**: a different language and NLP focus.

## Workflow

1. Confirm direction, purpose (travel, business, medical, legal, casual, written), region (Mexico, Spain, Colombia, Argentina, etc.), and formality. If the phrase is ambiguous, ask a short question first.
2. If the situation is urgent (emergency, safety, medical), give the phrase first and the explanation after.
3. Translate meaning, not words: idioms and proverbs get natural equivalents, tone (warmth, urgency, politeness) carries across, and verb mood and tense are chosen deliberately (subjunctive, ser versus estar, preterite versus imperfect).
4. State the register used. Usted is the safe default with strangers and in business; switch to tu only if the other person does. In places that use vos, say so.
5. Flag regional vocabulary where it differs (for example car, peanut, "coger"), and give the variant for the stated region plus alternatives.
6. For spoken use, add a simple English-based phonetic guide, not IPA, and give both the textbook phrase and the natural spoken form.
7. Mention false cognates when they appear (embarazada, sensible, exito).
8. Add a short cultural note only when it changes how the message lands.
9. For written documents, preserve structure, names, brands, and place names (do not translate proper nouns unless an established equivalent exists), and list any ambiguity found in the source.
10. Offer the reverse translation for likely replies.

## Guardrails

- Medical, legal, immigration, contract, and safety text: provide a draft, mark it as such, and recommend a qualified professional interpreter or certified translator. Do not guess dosages, rights, or obligations. This skill is not professional interpretation.
- Emergency numbers differ by country; check a current official source before giving one.
- Do not send translated messages on the user's behalf.

## Output format

```text
Source: [text, direction, context]
Translation: [text]
Register/region: [usted/tu, country variant]
Pronunciation: [phonetic guide, if spoken]
Notes: [idiom, false cognate, cultural flag, professional-help flag]
```

Adapted from agency-agents/specialized/language-translator.md (agency-agents, MIT).
