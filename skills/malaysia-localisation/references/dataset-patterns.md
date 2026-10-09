# Using dataset evidence for voice

Use this when researching corpora or choosing new examples. The inspected
Mesolitica sources and revisions are recorded in [data sources](../DATA_SOURCES.md).
This is editorial guidance from small previews, not a corpus-wide analysis.

- Separate local subject matter from register. A Malaysian QA answer, a Malay
  field or a regional label does not establish a casual Threads voice. Select
  by the requested language, register, audience and task as well as topic.
- In translation pairs, read the target instruction. A colloquial source can
  intentionally map to standard BM; do not learn that as the default direction
  for casual rewriting. The same facts can have several appropriate voices.
- Treat synthetic output as candidate evidence and a source of failure cases.
  Explicit user corrections and relevant fluent review carry more weight for
  the intended voice than a model-generated Manglish or dialect label.
- Compare meaning before adopting style. A rewrite must not add a diagnosis,
  solution hint, insult, emotion, commitment or stronger certainty. Preserve
  questions versus answers, quoted versus speaker claims and both comparison
  groups. Dense particles do not compensate for a changed message.
- Check executable material against the original. Translated prose can coexist
  with damaged code; preserve commands, identifiers, SQL types and error text.
  Language tags and automated detection flags are not correctness judgements.
- Keep regional forms optional and sample-led. A dataset's state label does
  not authorise inventing an accent or assigning a speaker to a region.
- Normalisation and language detection serve text-processing goals, not the
  speaker's chosen voice. Use them to understand shortforms; do not automatically
  expand contractions or translate familiar English words in the final draft.
  A token's language label cannot decide formality or identify its speaker.
- Random synonym, typo and slang augmentation is useful for noisy-input tests,
  not as a template for natural wording. Check that entities and meaning survive;
  no instruction to "sound local" justifies accidental spelling or fact changes.
- Check the origin and annotation task behind a label. A documented Manglish
  section can include Singaporean/Singlish sources or random word-switching.
  Shared forms can still fit, but the label does not establish this speaker's
  voice. Human sentiment labels or confident classifications are not human
  judgements that a sentence is a natural style example.

Author new minimal pairs with the same facts rather than copying dataset rows.
For example, if a test has finished but the cause of failure is unknown:

| Requested voice | Original illustration |
|---|---|
| Standard BM | Ujian telah selesai, tetapi punca kegagalan belum dikenal pasti. |
| Casual BM | Dah habis uji, tapi belum tahu lagi kenapa tak lepas. |
| Malay-led rojak | Dah habis test, tapi tak sure lagi kenapa fail. |
| Casual English | Test is done, but we're still not sure why it failed. |

None adds a suspected cause or a fix. Do not enforce a fixed mixing ratio or
  particle quota. Check provenance and applicable terms before importing any
material; this skill ships original examples, with no third-party rows.
