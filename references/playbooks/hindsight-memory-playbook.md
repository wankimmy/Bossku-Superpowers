# Hindsight with BosskuAI

This is a Bossku-authored integration contract informed by [Hindsight](https://github.com/vectorize-io/hindsight), reviewed at commit `ccfe85b4851957ac2adf88b4a9ddf9668b2882f1` on 2026-10-01. Runtime examples must be checked against the installed CLI or MCP schema before use.

## Architecture and boundary

The upstream service provides retain (fact extraction), recall (retrieval), and reflect (reasoning). It also consolidates observations and mental models. BosskuAI keeps dependency-free Markdown memory in the directory returned by `bossku memory-path --project <project-root>`; Hindsight is an optional, explicitly configured secondary layer. Obsidian mode writes canonical notes directly to the vault; legacy repo mode retains one-way export.

| Concern | BosskuAI contract |
|---|---|
| Durable canonical evidence | Configured memory directory, source files, commands, and commits |
| Optional retrieval | Hindsight recall in the selected project bank |
| Synthesis | Hindsight reflect; verify sources before acting |
| Ingestion | Redacted approved notes, not prompts, logs, or transcripts |
| Isolation | A project/audience-specific bank; tags only classify within it |
| Runtime missing or offline | Use configured Markdown, report Hindsight unavailable |
| Canonical vault unavailable | Report memory unsaved; never fall back to repo storage |
| Obsidian | Direct canonical writes, or legacy export according to configuration |

Installing this skill does not install a database, daemon, model, CLI, or MCP server and does not change credentials or host configuration. Upstream provider installation and automatic capture hooks are separate integrations, not enabled by BosskuAI.

## Review before configuring

1. Identify the use case that plain Markdown cannot serve, such as repeated retrieval across many verified project decisions.
2. Choose an existing approved deployment and model provider. Check whether extraction, embeddings, and reflection leave the machine, even when the service URL is local.
3. Choose a bank whose access matches the intended project and audience. Verify deployment authentication, network exposure, and tenant authorization separately: selecting a bank does not prove access isolation. The reviewed MCP defaults to unauthenticated access; its basic API-key extension authenticates callers into one shared schema.
4. Inspect the installed tool schema and effective CLI/MCP endpoint. Do not print credential files, put keys in committed examples, or infer health from an existing config. Treat bank creation, mission/configuration changes, ingestion, and mental-model creation/refresh as service writes requiring authorization.
5. Test using a synthetic, non-sensitive note only after the endpoint and write are authorized. Wait for supported operation completion, recall it with the intended scope, and verify source evidence. Confirm an unrelated scope cannot retrieve it; obtain authorization before removing the exact test record with a supported deletion tool.

## CLI and MCP use

The inspected upstream CLI documents these command shapes:

```bash
hindsight --help
hindsight memory recall --help
hindsight memory recall <selected-project-bank> "past decisions about this component"
hindsight memory reflect <selected-project-bank> "what changed across those decisions?"
```

Run recall and reflect only on an approved bank. These operations can invoke configured model providers. If an MCP is available, inspect its actual retain/recall/reflect schemas instead of assuming CLI argument names map to tool fields.

In the reviewed MCP, bank selection follows URL path, then `X-Bank-Id`, then configured/default bank. A single-bank connection scopes tools implicitly; multi-bank tools expose a bank parameter. Verify the effective bank before a call. In the reviewed CLI, environment URL/key values override named profiles and shared config; inspect overrides without logging secrets. These details describe the reviewed version, not every installed interface.

For an approved write, first save a verified canonical note using `bossku remember --project <project-root> --kind decision|plan|learning|project`. Then submit the curated note with the installed Hindsight retain interface. Include a stable source identifier and update semantics only if the chosen interface documents them. The reviewed `document_id` upsert defaults to deleting the previous document and its memories before reprocessing; use a separate ID for each independent decision, and a complete approved replacement for an evolving document. Append has its own semantics. Never replay an incomplete excerpt over a complete document or assume a retry is idempotent without checking the schema.

## Capability checklist

Apply only fields supported by the installed interface. Keep extraction context in approved notes: named entities, dates, cause, outcome, rationale, and evidence references. Curating a note can remove useful structure; preserve relevant verified relationships rather than uploading raw conversations to recover them.

| Capability | Practice |
|---|---|
| Bank missions | When configuration is authorized, define desired verified facts, excluded material, durable patterns/contradictions, and evidence-based reflection; inspect existing missions first |
| Retain `context` / `timestamp` | Describe the note's source and purpose; use actual event time when known, and an explicit timeless value only if supported |
| Metadata / tags | Use metadata for source/commit links and tags for retrieval filters; neither replaces bank/tenant authorization |
| Recall budget / token caps | Choose the smallest effort and returned context that answer the question; narrow the query before increasing either. Inspect actual payload size: the reviewed fact budget excludes metadata and can return an over-budget top fact |
| Recall tags / types / include | Check whether the match includes untagged data; use supported strict matching when it must be excluded. Prefer source facts and chunks for citations; inspect truncation and missing source entries before auditing observations |
| Reflect sources / schema | Request `include.facts` or equivalent provenance; verify returned `based_on` evidence. Use supported structured output for consumers that need a schema, then validate it |

The reviewed `any`/`all` tag modes include untagged records, while `any_strict`/`all_strict` exclude them. Broad filters may be valid for approved shared knowledge; audience-sensitive filters must match the authorized scope. Reflection traces can contain model inputs and outputs: request them only for authorized debugging and avoid indiscriminate logging.

## Retrieval and synthesis quality

- Select a narrow query and bounded output. Ask for the source facts/chunks when supported and needed for evidence.
- Compare timestamps and source/commit identifiers with the current repo. A relevant old decision can still be wrong today.
- Treat generated observations and mental models as derived knowledge. Their provenance must support the conclusion.
- Use recall for evidence the assistant will reason over; use reflect when synthesis across multiple memories is useful.
- Record a correction when new verified evidence supersedes an old note. Keep the reason and source so another tool can inspect it.
- Only consider precomputed mental models for repeated queries where refresh and freshness can be verified. Use one narrow knowledge dimension per model. Review bank, audience tags, source filters, and refresh policy together; untagged or broadly filtered models can synthesize wider data.
- Mental-model creation returns a pending operation in the reviewed API, and automatic refresh is off by default. Verify completion, last refresh, and supporting source changes; refresh or bypass stale models using an authorized operation rather than assuming they update after retain.

## Readiness and failure states

| Observation | Report |
|---|---|
| Skill exists, service not checked | Integration instructions available; runtime unverified |
| CLI exists, connection fails | Hindsight unavailable; use local notes |
| Canonical note saved, mirror fails | Canonical memory saved; Hindsight mirror failed |
| Canonical vault unavailable | Memory not saved; no repo fallback |
| Retain returns an operation ID | Accepted/pending; do not claim searchable |
| Mental model created or refresh queued | Pending until completion and scoped content are verified |
| Scoped recall returns verified source evidence | Retrieval verified for that query and bank |
| Reflect lacks supporting sources | Generated analysis unverified; do not promote as fact |

## Evaluation

After an authorized synthetic smoke, assess representative project queries with expected sources: exact decision lookup, superseded decision, evidence-backed synthesis, and audience separation. Check provenance and freshness as well as relevance; record actual latency and returned context instead of copying upstream performance claims. Bound retries and preserve the canonical note when the mirror fails. Static skill validation establishes guidance consistency, not live Hindsight behavior.

## Sources

- [Upstream memory skill](https://github.com/vectorize-io/hindsight/blob/ccfe85b4851957ac2adf88b4a9ddf9668b2882f1/skills/hindsight-local/SKILL.md): setup and retain/recall/reflect workflow.
- [Best practices](https://github.com/vectorize-io/hindsight/blob/ccfe85b4851957ac2adf88b4a9ddf9668b2882f1/skills/hindsight-docs/references/best-practices.md): bank isolation, missions, filtering, provenance, and recall versus reflect.
- [CLI reference](https://github.com/vectorize-io/hindsight/blob/ccfe85b4851957ac2adf88b4a9ddf9668b2882f1/skills/hindsight-docs/references/sdks/cli.md): configuration and command shapes.
- [MCP reference](https://github.com/vectorize-io/hindsight/blob/ccfe85b4851957ac2adf88b4a9ddf9668b2882f1/skills/hindsight-docs/references/developer/mcp-server.md): authentication, effective bank selection, and connected schemas.
- [Extension reference](https://github.com/vectorize-io/hindsight/blob/ccfe85b4851957ac2adf88b4a9ddf9668b2882f1/skills/hindsight-docs/references/developer/extensions.md): authentication versus tenant isolation.
- [Retain API](https://github.com/vectorize-io/hindsight/blob/ccfe85b4851957ac2adf88b4a9ddf9668b2882f1/skills/hindsight-docs/references/developer/api/retain.md), [reflect API](https://github.com/vectorize-io/hindsight/blob/ccfe85b4851957ac2adf88b4a9ddf9668b2882f1/skills/hindsight-docs/references/developer/api/reflect.md), and [mental-model API](https://github.com/vectorize-io/hindsight/blob/ccfe85b4851957ac2adf88b4a9ddf9668b2882f1/skills/hindsight-docs/references/developer/api/mental-models.md): context, update semantics, provenance, and refresh completion.
- [Recall API](https://github.com/vectorize-io/hindsight/blob/ccfe85b4851957ac2adf88b4a9ddf9668b2882f1/skills/hindsight-docs/references/developer/api/recall.md): fact budgets, source chunks, and truncated provenance.
- [Claude Code plugin](https://github.com/vectorize-io/hindsight/blob/ccfe85b4851957ac2adf88b4a9ddf9668b2882f1/hindsight-integrations/claude-code/README.md): automatic transcript capture and recall hooks, intentionally separate from BosskuAI.
