---
name: bosskuai-blender-addon-engineer
description: "Use when building a Blender Python add-on: operators, panels, asset validators, export presets, or batch tools that automate naming, transform, material-slot and glTF/FBX/USD handoff checks."
---

# BosskuAI Blender Add-on Engineer

Use this skill to turn a repetitive Blender asset-prep or export task into a reliable operator, validator or panel that artists can run without help.

## How this differs from nearby skills

- **`bosskuai-blender-motion-state-inspection`**: inspects rigs, poses and animation alignment in a scene. This skill writes the add-on code and validation tooling.
- **`bosskuai-3d-web-development`**: Three.js and WebGL scenes in the browser, not Blender-side tooling.
- **`python-patterns`**: general Python style and structure. This skill covers `bpy` registration, operators, panels and Blender-specific export gates.

## Workflow

1. Map the manual workflow step by step. List the repeated error classes: naming drift, unapplied transforms, wrong collection, broken export settings.
2. Pick the smallest useful wedge: a validator, an exporter, a cleanup operator, or a publish panel. Decide what is validate-only and what may auto-fix.
3. Define property groups and `AddonPreferences` first, so settings that matter between sessions persist.
4. Build operators with clear inputs and explicit results. Use the data API (`bpy.data`, direct property edits) in preference to context-dependent `bpy.ops`; use `bpy.ops` where Blender only exposes an operator (some exporters).
5. Put the panel where artists already work. Prefer a checklist plus one "Fix Selected" button over clever UI.
6. Gate export on validation: the export button runs the same checks as the validate button.
7. Test on dirty real scenes and several collections, then compare the result in the downstream engine or tool.
8. Document every rule the tool enforces and why.

## Checks the validator should cover

- Naming: deterministic, documented, no leading or trailing whitespace, no Blender duplicate suffixes such as `.001`.
- Transforms: check location, rotation and scale separately; "apply all" is not always safe.
- Materials: no empty slots; slot order checked when downstream tools use slot indices.
- Collections: explicit include and exclude rules, no hidden scene heuristics.

## Guardrails

- Never rename, delete, apply transforms or merge data without confirmation or a dry-run mode. Validation reports first, fixes second.
- Operators fail with actionable messages. Never report success while leaving the scene ambiguous.
- Batch tools log exactly what they changed, show progress, and are cancellable where practical.
- Exporters leave the source scene unchanged unless the user opts into destructive cleanup.
- Registration must be clean and reloadable. Check the installed Blender version and current `bpy` docs; the API changes between releases.
- Read the minimum Blender version from `bl_info` (or `blender_manifest.toml` for an extension), and read `bpy.app.version` at runtime. Check Blender's release notes on developer.blender.org before you use an API.
- Test a name close to Blender's length limit, linked library data, an object in two collections, and a file saved by an older Blender.
- Give each operator `bl_options = {'REGISTER', 'UNDO'}` so Ctrl+Z works, and leave the scene as it was if the operator fails halfway.
- Data the add-on stores in a `.blend` file must still load after an update. Test with a file saved by the last release.

Full quality bar (versions, edge cases, data, deploy, proof): `../../references/checklists/engineering-quality-bar.md`.

## Output format

```text
Pipeline problem: [error class, how often, who hits it]
Tool scope: [validator / exporter / cleanup / publish panel]
Rules enforced: [naming, transforms, materials, collections]
Persistence: [preferences / scene props]
Verification: [dirty-scene test, downstream import result]
```

Adapted from agency-agents/game-development/blender/blender-addon-engineer.md (agency-agents, MIT).
