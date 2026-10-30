---
name: bosskuai-unity-editor-tool-developer
description: "Use when automating the Unity Editor: custom EditorWindows, PropertyDrawers, AssetPostprocessors for import rules, menu items, and pre-build validators that fail the build on bad assets."
---

# BosskuAI Unity Editor Tool Developer

Use this skill to build Unity Editor tooling that catches asset and setup mistakes automatically and saves repeated manual review.

## How this differs from nearby skills

- **`bosskuai-csharp-testing`**: tests for C# code. This skill builds the Editor tools and import/build gates themselves.
- **`bosskuai-dotnet-patterns`**: general .NET application patterns, not Unity APIs.
- **`bosskuai-godot-multiplayer-engineer`**: another engine, runtime networking.
- **`bosskuai-ci-cd-pipelines`**: pipeline design; Unity batch mode validation fits there.
- **`bosskuai-game-audio-engineer`**: audio middleware budgets.

## Workflow

1. Specify the tool from real pain: ask "what do you do by hand more than once a week?" and write a success measure before building.
2. Choose the right Editor mechanism: EditorWindow (project insight), PropertyDrawer or CustomEditor (inspector safety), AssetPostprocessor (import rules), MenuItem or ContextMenu (shortcuts), build preprocessor (gate).
3. Keep Editor code out of runtime: put it in an `Editor` folder or an assembly definition restricted to the Editor, or guard with `#if UNITY_EDITOR`.
4. Build a prototype with the actual user and note where they get confused before adding polish.
5. EditorWindow standards: persist state across domain reloads, bracket edits with change checks, call `Undo.RecordObject` before modifying objects, and show a progress bar for work that takes more than a moment.
6. PropertyDrawer standards: use `BeginProperty`/`EndProperty` so prefab overrides work, return a height from `GetPropertyHeight` that matches what `OnGUI` draws, and tolerate null references.
7. AssetPostprocessor standards: put import enforcement here, not in ad hoc scripts; make it idempotent; log a clear warning whenever it overrides an artist's setting.
8. Wire critical rules into a pre-build step that throws a build failure, not just a log line.
9. Document inside the tool (help text, tooltips, a menu link) and keep a changelog comment.
10. For CI, run validators in headless batch mode with an execute-method entry and export a report. Check the installed Unity version's docs for flags and API names.

## Guardrails

- Unity Editor APIs and UI Toolkit versus IMGUI guidance change by version; verify against the installed version.
- Mass-changing import settings can modify thousands of assets; run on a branch with version control and review the diff before committing.
- Tools should not delete or overwrite assets without a confirmation and undo path.
- Read the Unity version from `ProjectSettings/ProjectVersion.txt`, and check the latest stable release notes before you use an Editor API.
- Stop when a scene the tool will touch has unsaved changes. Run a dry run that lists the assets it would change before the real run.
- Test on a project with broken references, prefab variants, and an empty or missing target folder. The tool must stop with a clear message, not write half the changes.

Full quality bar (versions, edge cases, data, deploy, proof): `../../references/checklists/engineering-quality-bar.md`.

## Output format

```text
Pain point: [manual task, frequency]
Mechanism: [window / drawer / postprocessor / build gate]
Rules enforced: [rule, severity, auto-fix or fail]
Undo/progress: [yes/no per operation]
Validation: [how tested, CI hook]
```

Adapted from agency-agents/game-development/unity/unity-editor-tool-developer.md (agency-agents, MIT).
