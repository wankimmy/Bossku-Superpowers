# Hindsight practice review

Reviewed on 2026-10-01 against the supplied `C:\dev\Tenant-Management-System\skills\hindsight` checkout at commit `ccfe85b4851957ac2adf88b4a9ddf9668b2882f1`. This review applies source guidance to Bossku Superpower's optional integration; it does not establish live backend behavior. Source paths below are relative to that checkout.

## Evidence extracts

1. `skills/hindsight-docs/references/developer/mcp-server.md:30`: "By default, the MCP endpoint is **open** (no authentication required)."
2. The same file, lines 84–86: bank selection is "URL path", "X-Bank-Id header", then "Default". Lines 103–108 distinguish implicit single-bank and explicit multi-bank tool schemas.
3. `skills/hindsight-docs/references/developer/extensions.md:15`: the basic API-key extension "uses the `public` schema for all authenticated requests."
4. `skills/hindsight-docs/references/best-practices.md:279`: metadata is "Not filterable"; lines 349–352 show that `any`/`all` include untagged records and strict modes exclude them.
5. `skills/hindsight-docs/references/developer/api/retain.md:155–169`: timestamps represent actual event time; `context` describes the source or situation. Lines 227–240 document replacement, duplicate ingestion, and append semantics.
6. `skills/hindsight-docs/references/developer/api/reflect.md:341`: `include.facts` exposes a `based_on` object listing the sources used. Lines 400–402 describe traces that include model inputs and outputs.
7. `skills/hindsight-docs/references/best-practices.md:523`: mental-model tags filter both source memories and visibility. `skills/hindsight-docs/references/developer/api/mental-models.md:18–19,198–201` documents pending creation and refresh defaults.
8. `skills/hindsight-docs/references/developer/api/recall.md:250–254`: "Only the `text` field of each fact is counted" and an oversized top fact can be returned "whole and over budget". Lines 331–338 describe truncated chunks and source-fact omissions.
9. `skills/hindsight-docs/references/best-practices.md:68,84,99`: missions steer fact extraction, durable observations, and reflection. `skills/hindsight-docs/references/sdks/cli.md:63–70` documents environment overrides of profiles and shared configuration.

## Applied guidance

| Finding | Bossku Superpower change |
|---|---|
| Bank scope and endpoint access are separate (1–3, 9) | Verify effective endpoint, authentication, audience, and bank; inspect connected schemas and CLI overrides |
| Filtering and provenance need explicit semantics (4, 6, 8) | Capability checklist distinguishes metadata, strict tags, source facts/chunks, and reflection evidence; check payload/truncation rather than assuming a strict full-response token cap |
| Replacement can remove previous evidence (5) | Inspect update semantics; separate independent decision IDs and retain complete approved replacements |
| Derived knowledge needs scope and freshness checks (7) | Authorize mental-model writes, review source/visibility scope, and verify refresh completion |
| Canonical memory changed in Bossku Superpower | Resolve `bossku memory-path`; direct vault mode and legacy export have distinct outcomes, with no repo fallback for unavailable canonical vaults |

The last row follows Bossku Superpower `bossku/memory.py` (`memory_directory`, `remember`, `sync_project`) and `docs/memory.md`. Upstream guidance about rich content is adapted by preserving verified entities, dates, rationale, outcomes, and evidence in curated notes (`best-practices.md:178–192`). Runtime installation, provider changes, transcript ingestion, and automatic capture hooks remain outside this change.

## Verification limits

Repository validation and routing checks can verify portable guidance and selection behavior. An authorized runtime evaluation must separately check known-source retrieval, superseded decisions, grounded synthesis, audience separation, operation completion, and observed latency. No backend deployment, uploads, destructive memory operations, or provider configuration were performed for this review.
