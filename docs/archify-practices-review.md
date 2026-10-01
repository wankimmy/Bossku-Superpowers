# Archify practices review

Reviewed on 2026-10-01 from the supplied checkout of [tt-a1i/archify at 9e35d2b0b39b155553ba9fcfe0b4f2a5198dd993](https://github.com/tt-a1i/archify/tree/9e35d2b0b39b155553ba9fcfe0b4f2a5198dd993). The tracked source files below were inspected locally. This review adapts practices to existing BosskuAI skills; it does not vendor Archify's runtime, schemas, viewer, examples, or brand assets.

## Source extracts

1. `archify/references/authoring-contract.md:186`: “Never infer runtime causality from file proximity or naming alone.”
2. The same file, line 191: “Verification reads blobs at that commit, independently of working-tree edits.”
3. `archify/references/delivery-contract.md:33`: “Passing one claim never implies either of the others.” The preceding lines distinguish deterministic artifact checks, browser evidence, and perceptual review.
4. `archify/SKILL.md:87`: “Relationship labels are semantic data.”
5. `archify/SKILL.md:65`: “Scenario proof examples are structural references, not facts to copy.”

These extracts anchor the following changes. Source paths are relative to the pinned Archify checkout, not to a user's workstation.

## Applied practices

| Practice and source | BosskuAI application |
|---|---|
| Inspect entry points, runtime boundaries, storage, transports, and deployment configuration; avoid naming-based causality (`archify/references/authoring-contract.md:181-187`, quote 1) | Codebase analysis requires source evidence for important calls, registrations, dispatch, queries, and transports; architecture applies the same rule to relationships. |
| Bind evidence to the source being inspected (`archify/references/authoring-contract.md:189-199`, quote 2) | Record revision or working-tree state when available, distinguish uncommitted source, refresh citations after edits, and state sampling limits. Non-Git analysis still works. |
| Select architecture, workflow, sequence, dataflow, or lifecycle for the question (`archify/SKILL.md:55-65`) | Architecture chooses a suitable view using text or Mermaid as its portable default. |
| Preserve relationship meaning (`archify/SKILL.md:87`, quote 4) | Maps retain verified direction, action/protocol, synchronous/asynchronous transport, and failure paths. |
| Separate different evidence claims (`archify/references/delivery-contract.md:27-33`, quote 3) | Analysis and architecture distinguish source inspection, automated checks, exercised behavior, and visual review. |
| Read matching references selectively (`archify/SKILL.md:20`, quote 5) | Project understanding retains stratified sampling; its playbook now matches that scope and reports unread areas. |

The project-understanding playbook and checklist also resolve memory through `bossku memory-path --project <project-root>` and save only verified durable facts with `bossku remember`. This repair follows BosskuAI's configured-memory contract; it is not an Archify feature.

## Boundaries and exclusions

- Archify verifies source blob existence and line bounds (`archify/renderers/shared/repository-evidence.mjs:165-217`). That loop traverses component source references, not runtime calls; a valid citation alone is insufficient evidence of a claimed relationship.
- Archify's verifier requires an origin, a full 40-character commit SHA, and committed blobs (`archify/references/authoring-contract.md:189-199`, `:218-219`). BosskuAI does not adopt those requirements because analysis must include local, non-Git, and uncommitted work.
- Archify's web links support GitHub and Gitee, with local-only mode for other hosts (`archify/references/authoring-contract.md:201-243`). BosskuAI keeps source paths portable and does not guess forge URLs.
- Node commands, schemas, diagram geometry, branded assets, exports, and browser viewport receipts remain outside the default skill workflow (`archify/SKILL.md:19-35`, `:75-137`). They are specific to producing Archify artifacts.

## Verification scope

BosskuAI validates the edited skills and their local reference links as part of its standard checks. This review inspected Archify source; it did not execute the Archify renderer, browser checks, or source tests. The transferred instructions improve evidence handling without claiming that source inspection proves runtime correctness or guarantees an optimal architecture.
