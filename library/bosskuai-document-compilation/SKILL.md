---
name: bosskuai-document-compilation
description: "Use when generating PDFs from HTML or structured data: deterministic page sizes, no blank trailing pages, Playwright browser pools, tagged accessible PDFs, and schema-agnostic YAML/JSON to paged-document layouts."
---

# BosskuAI Document Compilation

Use this skill to build or debug a pipeline that turns a web preview or arbitrary YAML/JSON data into print-ready, paged documents (invoices, reports, CVs, proposals) with predictable layout.

## How this differs from nearby skills

- **`odl-pdf`**: extracting structured text, tables, and OCR from existing PDFs. This skill creates PDFs.
- **`markitdown`**: converting Office/PDF/HTML into Markdown, the reverse direction.
- **`accessibility`**: WCAG for web UI; here only the PDF tagging and metadata part.
- **`e2e-testing`**: Playwright test suites; this skill uses Playwright only as a PDF renderer.

## Part A: HTML to PDF

1. One template. Render the PDF from a snapshot of the same hydrated UI the user previews, not from a second backend template that can drift.
2. Set page size explicitly with `@page { size; margin }`. Check the installed browser's support: CSS variables inside `@page` have not worked in Chromium, so inject concrete values from a runtime style element.
3. Compute sizes in one place (mm, pt, px at 96 DPI) and keep a small table for A4, Letter, Legal, and custom sizes. Validate custom sizes are finite and positive.
4. Avoid blank trailing pages: sub-pixel rounding can push content a fraction over the page. Test with a small height buffer on the page container and check the page count on long and short inputs.
5. Keep text and shapes as vectors. In print CSS, avoid `filter`, `backdrop-filter`, and heavy effects that can make the engine rasterise; verify by inspecting the output.
6. Wait for fonts and images before printing (for example `document.fonts.ready`). Use the headless renderer's PDF call, not `window.print()`.
7. Editor preview: keep the sheet at fixed physical size and zoom with a transform so line breaks match the PDF.
8. Throughput: reuse a warm browser and isolated contexts, cap concurrency, recycle after a job count, and drain in-flight jobs before shutdown. Measure your own latency; do not trust quoted numbers.
9. Accessibility: emit a tagged PDF, use real headings, lists, table headers, and image alt text. If PDF/A or PDF/UA is required, post-process metadata and validate with a dedicated checker.
10. Audit the output: page count, selectable text, font ToUnicode maps, no full-page raster images.

## Part B: schema-agnostic data to layout

1. Parse YAML with a library that keeps source positions and comments; do not round-trip with a plain dump.
2. Never drop unknown keys. Render them with a generic block layout.
3. Infer a layout per node from its shape (list of similar records, key-value map, short tags, long prose, dated items). Make inference a replaceable function with an explicit override.
4. Store view settings (colours, ordering, hidden flags) in a separate sidecar file keyed by stable paths, not inside the user's data.
5. Two-way editing: tag each edit with its origin to avoid update loops, and mutate the syntax tree in place to preserve comments.
6. Paged rules: headings `break-after: avoid`, cards and rows `break-inside: avoid`, and a fallback page break when a block exceeds a page.

## Guardrails

- Sanitise snapshots: strip scripts, iframes, and inline event handlers. When inlining assets, allow only https and a domain allow-list to prevent SSRF.
- Bound iterative solvers (max iterations) to avoid denial of service.
- Browser flags like `--no-sandbox` reduce isolation; use only where the container requires it.
- Check current Playwright, Chromium, and PDF-library docs for option names.
- Compliance claims (PDF/UA, PDF/A, Section 508) need a validator run and human review; documents with legal or clinical content need their own review.

## Output format

```text
Input and target: [source, page size, accessibility level]
Pipeline: [snapshot, render, post-process, audit]
Layout rules: [page geometry, break rules, fallbacks]
Throughput and limits: [pool size, recycle, timeouts]
Verification: [page count, text selectable, validator result]
Open risks: [list]
```

The shared quality bar: `../../references/checklists/engineering-quality-bar.md`.

Adapted from agency-agents/engineering/engineering-pdf-engine-architect.md and engineering-universal-document-compiler.md (agency-agents, MIT).
