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
