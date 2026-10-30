---
name: bosskuai-lsp-index-engineer
description: "Use when building a code-intelligence service on Language Server Protocol clients: multi-language orchestration, a symbol and reference graph, a navigation index, incremental updates and cache design."
---

# BosskuAI LSP Index Engineer

Use this skill to design a service that runs several language servers and turns their answers into one consistent symbol graph and navigation index.

## How this differs from nearby skills

- **`graft`**: use it when a graft index already exists and you only need to query code. This skill is for building the indexing service itself.
- **`bosskuai-codebase-analysis`** and **`bosskuai-project-understanding`**: read and explain an existing repo; they do not build indexers.
- **`bosskuai-software-architecture`**: general design tradeoffs; this skill is specific to LSP orchestration and graph consistency.
- **`bosskuai-performance-profiling`**: use it to find the actual bottleneck once the service runs.

## Workflow

1. Choose the first languages and their servers. Check each server's installed version and its reported capabilities rather than assuming features. Compare the installed version with the server's latest stable release, checked live at work time.
2. Run each client through the full lifecycle: initialise, initialised, requests, shutdown, exit. Negotiate capabilities and handle server crashes and restarts.
3. Define the graph schema: file and symbol nodes, edges for contains, imports, extends, implements, calls and references.
4. Pick a stable symbol identity based on definition location (file, position, name). Use the same id in the graph, the navigation records, the references and the hover data. Names alone repeat across files and scopes.
5. Build in phases: collect files, create file nodes, extract symbols, resolve references and calls.
6. Enforce consistency: one definition per symbol, every edge points to an existing node, file nodes exist before the symbols they contain, import edges resolve to real files, references point to definitions.
7. Write the navigation index as line-delimited records (definition, references, hover), one complete record per line.
8. Update incrementally from file watchers and commits. Apply diffs atomically so the graph is never half updated. Build a new index beside the old one, and switch only after it passes the consistency checks, so queries keep working during a rebuild.
9. Add a persistent cache for fast start-up, and invalidate precisely. Batch requests to cut round trips. Version the index format and cache keys, so an upgrade ignores old caches instead of reading them.
10. Set latency and memory targets from measurement on a real repo, then profile.

## Guardrails

- Follow the protocol version your servers support; read its specification for details.
- Never assume a capability; check the server's response.
- Serve stale-but-consistent data in preference to an inconsistent graph during updates.
- Respect repo size and ignore rules (build output, dependencies) when walking files.
- LSP positions are zero-based and count UTF-16 code units, unless the client and server agree on another encoding. Test with non-ASCII files: a column counted in bytes points at the wrong text.
- Test with messy input: syntax errors, a file deleted mid-index, a symlink loop and CRLF line endings.
- Compare symbol and reference counts with the language server's own output, on a copy of a real, large repo.

## Output format

```text
Languages and servers: [server, version, capabilities used]
Graph schema: [node kinds, edge types, id format]
Pipeline: [collect, extract, resolve, persist]
Consistency checks: [rules, how verified]
Update path: [watcher, diff, atomic apply]
Targets and measurements: [latency, memory, symbol count]
```

The shared quality bar: `../../references/checklists/engineering-quality-bar.md`.

Adapted from agency-agents/specialized/lsp-index-engineer.md (agency-agents, MIT).
