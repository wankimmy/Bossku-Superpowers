---
name: bosskuai-orgscript
description: "Use when turning SOPs and tribal-knowledge processes into OrgScript (.orgs) files, or changing the OrgScript parser and CLI: process, stateflow, rule and policy blocks, validation, diagnostics, and Mermaid/JSON export."
---

# BosskuAI OrgScript

Use this skill when business logic written as plain-language procedures must become strict, machine-readable OrgScript, or when you change the OrgScript toolchain (parser, AST validator, linter, exporters). OrgScript is a description language, not a general programming language.

## How this differs from nearby skills

- **`bosskuai-business-logic-review`**: reviews existing code for business-rule bugs, not authoring a process DSL.
- **`bosskuai-data-architecture`**: data and system structure, not workflow descriptions.
- **`bosskuai-orch-pipeline`**: orchestrating agent steps in a pipeline, not modelling an organisation's process.
- **`bosskuai-story-lifecycle`**: story and ticket lifecycle, not a formal process language.

## Workflow: modelling a process

1. Read the plain-text SOP or requirement. List triggers, conditions, state changes, roles, notifications, and stop conditions.
2. Read the installed OrgScript language spec and grammar (the repository's `spec/language-spec.md` and `grammar.ebnf` if present). They are the source of truth for supported blocks and statements; the set can change between versions, so do not rely on memory.
3. Draft the `.orgs` file using only supported blocks (for the v0.1 spec: process, stateflow, rule, role, policy, metric, event) and statements (when, if, else, then, assign, transition, notify, create, update, require, stop). Keep it text-first, diff-friendly, and in plain English.
4. Run the CLI in order: format, validate, check (use the `--json` form in automation). Fix every diagnostic; exit code 0 means clean.
5. Export Mermaid or Markdown to review the flow with the process owner, and embed the diagram in docs.
6. Confirm with the owner that the model matches what the business really does, including edge cases the SOP omitted.

Shape example (check the spec for exact syntax):

```text
process LeadRouting
  when lead.created
  if lead.estimated_value < 1000 then
    transition lead.status to "disqualified"
    stop
  transition lead.status to "qualified"
```

## Workflow: changing the toolchain

1. Treat the grammar as the single source for syntax. Update tokenizer, AST nodes, validator, and exporters together.
2. Keep diagnostic codes stable and attach them to exact lines; messages must be readable by people and by AI tools.
3. Keep CI-friendly exit codes (0 clean, 1 errors).
4. Back changes with snapshot tests on canonical JSON and run the full pipeline: parse, AST, canonical model, validate, lint, export.

## Guardrails

- Do not treat OrgScript as Turing-complete or add general-programming constructs to a process file.
- Do not invent statements or blocks outside the spec; ask whether the grammar should change.
- Processes touching payroll, hiring, finance, or legal obligations need review by the process owner and a qualified person before automation relies on them.
- Do not wire a model to automation that sends messages or changes real records without explicit user approval.

## Output format

```text
Source SOP: [reference]
Triggers / roles / states: [lists]
OrgScript file: [path]
CLI results: [format, validate, check exit codes]
Exports: [mermaid / markdown / json paths]
Open questions for the process owner: [list]
```

Adapted from agency-agents/engineering/engineering-orgscript-engineer.md (agency-agents, MIT).
