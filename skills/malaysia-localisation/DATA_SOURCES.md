# Evidence, licences and provenance

Checked 9 October 2026. This package's instructions, scripts, examples and eval
cases were authored for this release. Examples are synthetic, not corpus rows
and not native-speaker-validated gold data. No source code, social posts, model
weights, corpus excerpts or third-party dataset rows are bundled. The package
does not scrape, train or download data when used. Its MIT licence covers its
own contents, not linked sources. It is unaffiliated with ILMU, YTL, DBP,
Mesolitica, NVIDIA, Anthropic, Cursor or OpenAI.

The register and pragmatic approach is an editorial inference from the sources
below, not a reproduction of ILMU's training or a claim of equal performance.

| Source | Evidence and intended role | Licence/reuse status at check |
|---|---|---|
| [ILMU technical report](https://www.ilmu.ai/assets/ilmu-technical-report.pdf) | Reports Malaysia-centric data, several Malay registers and mixed language capabilities; motivates register-sensitive guidance | Report is reference-only here. Training mixture and model size are not fully disclosed; no training-data reuse permission inferred. |
| [ILMU system card](https://www.ilmu.ai/assets/ilmu-system-card.pdf) | Describes Malaysian-context instruction-response post-training | Reference-only. Does not make its underlying examples public. |
| [MalayMMLU](https://github.com/UMxYTL-AI-Labs/MalayMMLU), [licence](https://github.com/UMxYTL-AI-Labs/MalayMMLU/blob/main/LICENSE.txt) | Malaysian knowledge benchmark; potential separate factual evaluation, not a colloquial style source | Repository identifies BSD-3-Clause. No questions copied; preserve upstream notice if later importing permitted material. |
| [MESocSentiment](https://github.com/afifahms/MESocSentiment), [licence](https://github.com/afifahms/MESocSentiment/blob/main/LICENSE) | Public Malay-English social-media sentiment corpus; candidate for separate pattern analysis | Repository identifies CC0-1.0. No posts copied. Platform terms, privacy and rights in underlying posts still deserve dataset-specific review before reuse. |
| [malaysian-manglish-nlp documentation](https://manglish-nlp.readthedocs.io/en/latest/) | Toolkit for normalisation, language and code-switch analysis; candidate research utility | Documentation declares MIT for the project. Repository licence could not be independently fetched in this pass; dataset-specific rights are not assumed from the toolkit licence. No mappings or code copied. |
| [Malaysia-AI / Mesolitica Malaysian dataset](https://github.com/malaysia-ai/malaysian-dataset) | Research leads for mixed language and corpus provenance | README requests contact before redistribution and cautions about commercial use of third-party processed data. Treat each component separately; no blanket permissive licence assumed. |
| [Malay-Dialect-Instructions](https://huggingface.co/datasets/mesolitica/Malay-Dialect-Instructions) | Candidate for dialect-aware research and review | No clear licence declaration found on the inspected page. Do not redistribute or treat as commercial-safe on this evidence. No rows copied. |
| [DBP corpus portal](https://dbp.gov.my/data-korpus/), [PRPM](https://prpm.dbp.gov.my/) | Authoritative standard BM lookup leads | Corpus portal requires agreement to user terms. The EULA could not be fully fetched here, so exact grant/restrictions remain unverified. No corpus material bundled; do not infer open redistribution. |
| [ILMU's Malaysia personas announcement](https://www.ilmu.ai/about/) | Candidate future source for diverse scenario design, not proof of an individual's voice | Inspected primary page labels NVIDIA Nemotron-Personas-Malaysia “Coming Soon”; a dataset card/licence was not retrieved. Earlier CC BY 4.0 claims remain unverified; no profiles bundled. |
| [Discourse Particles in Malaysian English](https://www.sciencedirect.com/org/science/article/pii/S0006229416000010) | Research supports treating particles as contextual stance/interpersonal markers | Reference-only research; no conversations copied. Sample frequencies are not generation quotas or population-wide rules. |
| [UPM particle-use thesis record](https://psasir.upm.edu.my/id/eprint/42806/) | Documents a particular sample, not all Malaysian speakers | Reference-only. Never turn group-level observations into identity inference. |

The 2024 large X-post corpus mentioned in the earlier research conversation was
not independently pinned to a stable dataset licence in this pass. It is not a
dependency and no material is included. This release deliberately avoids
unverified dataset sizes, blanket “safe data” labels and automatic downloads.

## Mesolitica follow-up: 9 October 2026

Inspected the [collections page](https://huggingface.co/mesolitica/collections),
its pretraining, translation and instruction collections, dataset cards and
small public previews. Repository revisions below were observed at inspection;
live viewer previews are not claimed to be immutable snapshots of those commits.
No bulk corpus was downloaded and no third-party rows are included in this skill.

| Dataset and observed revision | Inspected scope and editorial use |
|---|---|
| [Malay-Dialect-Instructions](https://huggingface.co/datasets/mesolitica/Malay-Dialect-Instructions), `17ba33e2371472dcfeb7f77b296f529c90a82fd1` | Card, metadata, viewer and first three API rows in default/train. Parallel original, BM and dialect fields illustrate register differences; one preview translates an executable SQL type. This motivates original code-preservation cases, not dialect imitation. |
| [Malaysian-Translation](https://huggingface.co/datasets/mesolitica/Malaysian-Translation), `fb6c40193900e994164d264cd405de885c64af0f` | Card, metadata and first three API rows in stage1/train. Source/target/prefix pairs map colloquial text to standard BM or English. Use the requested target register rather than automatically normalising casual speech. No claims about later subsets' quality. |
| [chatgpt4-malaysian-general-qa](https://huggingface.co/datasets/mesolitica/chatgpt4-malaysian-general-qa), `9acbb5b0abbcb99b58c326829d377c442e0fbcb0` | Card examples and visible dialect previews. Card identifies synthetic ChatGPT4 QA; Malaysian topics coexist with formal/explanatory language. Local subject matter is not evidence of the requested casual voice. |
| [MaLLaM-2.5-Small-Manglish-QA](https://huggingface.co/datasets/mesolitica/MaLLaM-2.5-Small-Manglish-QA), `e125093aa64b6456f9beb78579e8bbe489464842` | Three card conversations, identified as synthetic. Dense particles and added mathematical guidance motivate original over-localisation and meaning-delta tests. Not a gold standard for natural Manglish. |
| [chatgpt4-code-instruct](https://huggingface.co/datasets/mesolitica/chatgpt4-code-instruct), `9a5b88422c1b3ade367f63da2b62fd559e581de6` | Card loop example and visible preview fields. Card describes ChatGPT4 translation/answers from evol-codealpaca. Original and localised fields plus detection flags do not establish fluency or code correctness. |
| [chatgpt-malay-instructions](https://huggingface.co/datasets/mesolitica/chatgpt-malay-instructions), revision not recovered | Live card examples and market-dialogue preview. Described as synthetic/evolved ChatGPT3.5 instructions. Ordinary contractions can be enough; an evolved code sample also mismatches identifier bindings. Keep code intact and author new illustrations. |
| [fineweb-filter-malaysian-context](https://huggingface.co/datasets/mesolitica/fineweb-filter-malaysian-context), `c8df876812cc99955138c3f3691c2fc3b7933d6c` | Card and metadata only; tagged English. Malaysian-context filtering does not make it a BM/rojak voice corpus. No row-based style inference made. |
| [pretrain-text-dataset](https://huggingface.co/datasets/malaysia-ai/pretrain-text-dataset), `870eb846a8106dc21fb5c8cf54541333beb62983` | Card and metadata only; card describes multilingual web-crawled texts and disables the viewer. No rows inspected and no colloquial-frequency claims made. |

The inspected metadata/cards did not establish an explicit data reuse grant
for these datasets. Visibility, a collection label or a related model's licence
is not a dataset licence. This pass uses observations to design original
guidance and examples; it does not infer permission to redistribute corpus rows.
Small previews cannot establish population-wide preferences or dataset quality.
User-supplied wording corrections motivated the casual result/pakai examples;
the dataset inspection motivates register, meaning and code-preservation checks.
See [dataset patterns](references/dataset-patterns.md) for the resulting guidance.

## Local Malaya follow-up: 9 October 2026

Inspected the user-supplied checkout at
`C:/dev/Tenant-Management-System/skills/malaya`, revision
`d3e6858667cbc96fa79da76a8da2c0960d3ca19f`, origin
[malaysia-ai/malaya](https://github.com/malaysia-ai/malaya). README also cites
Mesolitica's Malaya repository. No library import, installation or model run.

- `malaya/normalizer/rules.py:256-313` has independent normalisation,
  shortform/contraction expansion, translation and language-detection controls.
  Editorial implication: understand shorthand without automatically normalising
  the speaker's final voice.
- `malaya/language_detection.py:37-49` and `malaya/model/rules.py:41-108`
  expose processing labels and configurable dictionary/language checks.
  Editorial implication: a label is not a register, identity or naturalness
  judgement, nor a reason to reject a shared Malay phrase.
- `malaya/augmentation/rules.py:14-38,96-159` describes random synonyms and
  naive typo/slang transformations. Inspected augmentation notebook examples
  show meaning changes. Editorial implication: use augmentation as noisy-input
  test inspiration, not a template for fluent casual prose.

The inspected `LICENSE` grants MIT for the software and documentation, with
notice retention. This is not a blanket grant for linked models or external
datasets. No code, mappings or notebook text are bundled. These are source-led
editorial decisions, not measured claims about Malaya's overall quality.

## Local Malaysian-Dataset follow-up: 9 October 2026

Inspected the user-supplied checkout at
`C:/dev/Tenant-Management-System/skills/malaysian-dataset`, revision
`87c0562cb41966babc62b299cd2812e620d1c23e`, origin
[malaysia-ai/malaysian-dataset](https://github.com/malaysia-ai/malaysian-dataset).
The bounded inspection covered documentation, generation notebooks and two
locally stored synthetic normalisation pairs, not private social posts.

- `README.rst:23-55` separates crawled text, translation, semisupervision and
  LLM generation. `normalization/iium-confession/README.md:3` describes
  backtranslation; normalised targets are not a default speaking voice.
- `normalization/normalize/normalized.json` first two synthetic pairs expand
  a reminder particle as a lexical verb. Their generation template is in
  `normalization/normalize/augmented-normalization.ipynb:112-115`.
  This motivates an original particle-context case, not copied text.
- `docs/dumping.rst:248-262` labels a Manglish section while describing
  Singaporean sites/blogs and a Singlish file. A synthetic word-switching
  notebook also uses random aligned-word substitutions. Inspect geographical
  and generation provenance; do not infer a uniform voice from the heading.
- `sentiment/supervised-twitter/README.md:1-3` describes manual sentiment
  annotation; semisupervised confidence and lexicon-based keyword sets serve
  other tasks. Neither annotation nor confidence certifies natural style.

`README.rst:62` requests contact before redistribution; `:71-77` cautions about
commercial use of third-party processed data. No root data licence was found
in this bounded check. No corpus row, mapping or notebook content is bundled;
the skill adds original guidance and cases from the observed failure patterns.

## Extending with public data later

Pin the exact repository commit/dataset version, inspect its licence and origin,
record the intended use, and distinguish code licensing from data rights. For
each imported item keep provenance, applicable notices and consent/privacy
considerations. Avoid private identifiers and verbatim social posts in examples.
Prefer original scenario-based examples reviewed by fluent target speakers.
Keep imported benchmark questions separate from style examples and publish the
evaluation method. Recheck upstream terms before each redistributed release.

## Installation specifications

The installation guide follows the inspected primary documentation:
[Claude skills](https://code.claude.com/docs/en/skills),
[Claude plugins](https://code.claude.com/docs/en/plugins),
[local marketplace](https://code.claude.com/docs/en/plugin-marketplaces),
[Cursor skills](https://cursor.com/docs/skills), and
[Codex skills](https://learn.chatgpt.com/docs/build-skills).
Client versions can differ; structure validation is not live-client validation.
