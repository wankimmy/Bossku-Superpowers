# Hindsight with BosskuAI

This is a Bossku-authored integration contract informed by [Hindsight](https://github.com/vectorize-io/hindsight), reviewed at commit `ccfe85b4851957ac2adf88b4a9ddf9668b2882f1` on 2026-09-29. Runtime examples must be checked against the installed CLI or MCP schema before use.

## Architecture and boundary

The upstream service provides retain (fact extraction), recall (retrieval), and reflect (reasoning). It also consolidates observations and mental models. BosskuAI keeps its dependency-free Markdown memory and one-way Obsidian export; Hindsight is an optional, explicitly configured secondary layer.

| Concern | BosskuAI contract |
|---|---|
| Durable canonical evidence | `.bossku/memory/`, source files, commands, and commits |
| Optional retrieval | Hindsight recall in the selected project bank |
| Synthesis | Hindsight reflect; verify sources before acting |
| Ingestion | Redacted approved notes, not prompts, logs, or transcripts |
| Isolation | A project/audience-specific bank; tags only classify within it |
| Runtime missing or offline | Use local memory, report Hindsight unavailable |
| Obsidian | Existing `bossku remember` / `bossku sync` behavior |

Installing this skill does not install a database, daemon, model, CLI, or MCP server and does not change credentials or host configuration. Upstream provider installation and automatic capture hooks are separate integrations, not enabled by BosskuAI.

## Review before configuring

1. Identify the use case that plain Markdown cannot serve, such as repeated retrieval across many verified project decisions.
2. Choose an existing approved deployment and model provider. Check whether extraction, embeddings, and reflection leave the machine, even when the service URL is local.
3. Choose a bank whose access matches the intended project and audience. Treat any bank creation, configuration, or note ingestion as a write to that service.
4. Inspect the installed tool schema and account/service access. Do not print credential files, put keys in committed examples, or infer health from an existing config.
5. Test using a synthetic, non-sensitive note only after the endpoint and write are authorized. Recall it and verify source evidence; remove only the test record using supported tools.

## CLI and MCP use

The inspected upstream CLI documents these command shapes:

```bash
hindsight --help
hindsight memory recall --help
hindsight memory recall <selected-project-bank> "past decisions about this component"
hindsight memory reflect <selected-project-bank> "what changed across those decisions?"
```

Run recall and reflect only on an approved bank. These operations can invoke configured model providers. If an MCP is available, inspect its actual retain/recall/reflect schemas instead of assuming CLI argument names map to tool fields.

For an approved write, first save a verified canonical note using `bossku remember --project . --kind decision|learning|project`. Then submit the curated note with the installed Hindsight retain interface. Include a stable source identifier and update semantics only if the chosen interface documents them. Do not assume retries are idempotent or that every retain API supports `document_id`.

## Retrieval and synthesis quality

- Select a narrow query and bounded output. Ask for the source facts/chunks when supported and needed for evidence.
- Compare timestamps and source/commit identifiers with the current repo. A relevant old decision can still be wrong today.
- Treat generated observations and mental models as derived knowledge. Their provenance must support the conclusion.
- Use recall for evidence the assistant will reason over; use reflect when synthesis across multiple memories is useful.
- Record a correction when new verified evidence supersedes an old note. Keep the reason and source so another tool can inspect it.
- Only consider precomputed mental models for repeated queries where refresh and freshness can be verified.

## Readiness and failure states

| Observation | Report |
|---|---|
| Skill exists, service not checked | Integration instructions available; runtime unverified |
| CLI exists, connection fails | Hindsight unavailable; use local notes |
| Local note saved, mirror fails | Canonical memory saved; Hindsight mirror failed |
| Retain returns an operation ID | Accepted/pending; do not claim searchable |
| Scoped recall returns verified source evidence | Retrieval verified for that query and bank |
| Reflect lacks supporting sources | Generated analysis unverified; do not promote as fact |

## Sources

- [Upstream memory skill](https://github.com/vectorize-io/hindsight/blob/ccfe85b4851957ac2adf88b4a9ddf9668b2882f1/skills/hindsight-local/SKILL.md): setup and retain/recall/reflect workflow.
- [Best practices](https://github.com/vectorize-io/hindsight/blob/ccfe85b4851957ac2adf88b4a9ddf9668b2882f1/skills/hindsight-docs/references/best-practices.md): bank isolation, missions, filtering, provenance, and recall versus reflect.
- [CLI reference](https://github.com/vectorize-io/hindsight/blob/ccfe85b4851957ac2adf88b4a9ddf9668b2882f1/skills/hindsight-docs/references/sdks/cli.md): configuration and command shapes.
- [Claude Code plugin](https://github.com/vectorize-io/hindsight/blob/ccfe85b4851957ac2adf88b4a9ddf9668b2882f1/hindsight-integrations/claude-code/README.md): automatic transcript capture and recall hooks, intentionally separate from BosskuAI.
