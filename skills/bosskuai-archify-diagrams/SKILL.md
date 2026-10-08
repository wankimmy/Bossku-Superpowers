---
name: bosskuai-archify-diagrams
description: "Use when the user wants an architecture, workflow, sequence, data-flow or lifecycle diagram as an interactive standalone HTML page, or wants a Mermaid diagram turned into one. Needs the separate Archify skill (tt-a1i/archify); this skill sets the guard rails."
---

# Diagrams with Archify

Archify turns a small typed JSON description into a self-contained, explorable HTML diagram (inline SVG, light and dark themes). It is a separate MIT project that is not bundled here.

1. **Check it is installed.** Look for an `archify` skill in the agent's skills folder. If it is missing, tell the user it comes from `tt-a1i/archify` (`npx skills add tt-a1i/archify -g`) and install it only after they say yes. Then follow that skill's own `SKILL.md`; it is the source of truth for the schemas and commands.
2. **Pick the type from the question:** `architecture` (components and boundaries), `workflow` (processes, approvals, CI/CD), `sequence` (request chains and returns), `dataflow` (pipelines, lineage), `lifecycle` (states and transitions).
3. **Author fresh JSON.** Use one matching schema and one matching example as a shape only; write new ids, wording and layout from the user's facts. For Mermaid input read the topology and meaning, then author new JSON instead of converting styling.
4. **Draw only what you know.** Components, arrows and labels must come from the code, the docs or what the user said. Mark anything you inferred as an assumption in the diagram's notes.
5. **Validate before you deliver.** Run the Archify validator after every edit and its `deliver` command for the final file. A non-zero exit is a failure: say so and fix the spec, never describe it as done.
6. **Skip the update check.** Archify's skill asks the agent to contact a GitHub Pages URL to look for a newer version; do that only if the user asks.
7. **Hand over** the HTML path, the validator result and the list of assumptions.

Static output is the default; add motion only when the user asks for a presentation. Existing code maps belong to `graft` and `graphify`; this skill is for diagrams a person will read.
