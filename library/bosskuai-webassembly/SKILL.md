---
name: bosskuai-webassembly
description: "Use when deciding whether to use WebAssembly and how: compile Rust or C++ to Wasm, design the JS boundary, manage linear memory, shrink and stream modules, and sandbox untrusted plugins with WASI runtimes."
---

# BosskuAI WebAssembly

Use this skill to decide whether Wasm fits a workload, then build it so the speedup survives the JS boundary, load time and memory limits. Most "Wasm is slow" cases are too many boundary crossings.

## How this differs from nearby skills

- **`bosskuai-rust-patterns`**: idiomatic Rust itself. This skill is about targeting Wasm and its boundary.
- **`bosskuai-cpp-coding-standards`**: C++ code quality; Emscripten and boundary design come from here.
- **`bosskuai-web-performance`**: general bundle and load performance; a Wasm module size budget belongs in that budget.
- **`bosskuai-performance-profiling`**: general profiling and benchmarking method.

## Workflow

1. Fit check: compute-bound work with small data crossing the boundary (codecs, parsing large buffers, simulation, crypto, numeric kernels) often wins. DOM glue and chatty logic usually loses. Untrusted plugins can justify Wasm for isolation alone.
2. Baseline the current JS or native version on representative data, so "faster" has a number to beat.
3. Design the boundary first: what crosses, in what format, who owns the memory. Pass large typed buffers or handles, loop inside the module, avoid per-element calls and rich object graphs. In JavaScript, 64-bit integers cross as `BigInt`, and a JS `Number` loses precision above 2^53 - 1.
4. Choose the toolchain by its costs: Rust with wasm-bindgen, C/C++ with Emscripten, or standalone WASI. Languages with a runtime or garbage collector add size and startup cost.
5. Manage linear memory deliberately: it grows and does not shrink in a running instance, so bound it, reuse buffers, and consider arena allocation for churn. After `memory.grow`, JavaScript views on the old buffer are detached, so recreate them after any call that can grow memory.
6. Optimise only measured hotspots. Use SIMD or threads when benchmarks justify them, with feature detection and a working fallback (threads need shared memory and cross-origin isolation in browsers).
7. Ship small and early: optimise with wasm-opt and release-profile flags, strip debug info, use streaming instantiation, lazy-load, and track module size in CI.
8. Server side: run modules on Wasmtime or Wasmer, grant only the WASI capabilities required (specific directories, no ambient network), define interfaces with the component model where tooling supports it, and test that the module cannot exceed its grant, such as a file outside the granted directory or a denied socket.
9. Re-benchmark end to end, including instantiation and marshalling.

## Guardrails

- Check installed toolchain versions (`rustc --version`, `wasm-bindgen --version`, `emcc --version`, `wasmtime --version`) and current docs at work time. Wasm proposals, WASI previews and component model tooling are changing, so use only APIs present in the installed version.
- Do not claim speedups without a benchmark against the real baseline.
- Do not run untrusted modules with broad filesystem, network or environment access.
- Provide a fallback for runtimes missing SIMD, threads or component support.

## Output format

```text
Workload and fit: [verdict, reason]
Baseline: [implementation, timing on real data]
Boundary design: [data crossing, ownership, batching]
Toolchain: [language, tool versions, size/startup cost]
Memory and security: [limits, WASI grants]
Results: [timing, module size, fallback path]
```

Also check the shared quality bar: `../../references/checklists/engineering-quality-bar.md`.

Adapted from agency-agents/engineering/engineering-webassembly-engineer.md (agency-agents, MIT).
