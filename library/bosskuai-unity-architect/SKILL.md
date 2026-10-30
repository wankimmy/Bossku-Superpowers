---
name: bosskuai-unity-architect
description: "Use when structuring or refactoring a Unity project: ScriptableObject data and event channels, runtime sets instead of singletons, single-responsibility components, self-contained prefabs, and scene hygiene."
---

# BosskuAI Unity Architect

Use this skill to move a Unity codebase away from God classes and hard references toward small components wired through assets that designers can edit.

## How this differs from nearby skills

- **`bosskuai-software-architecture`**: language-agnostic module boundaries. This skill applies the ideas to Unity assets, prefabs, and scenes.
- **`bosskuai-csharp-testing`** and **`bosskuai-dotnet-patterns`**: C# testing and .NET practice used in the code here.
- **`bosskuai-code-revamp`**: general refactor method; use it to stage large rewrites.
- **`bosskuai-performance-profiling`**: general method; Unity-specific Profiler use is in step 7.
- **`bosskuai-godot-gameplay-scripter`**: the same composition idea for Godot.

## Principles

- Shared game data lives in ScriptableObject assets, not in fields copied between scenes.
- Cross-system messages go through event-channel assets; tracking of active entities goes through runtime-set assets. Avoid global lookups (`Find`-style calls) and singleton managers for cross-system communication.
- Each MonoBehaviour solves one problem. If its description needs "and", split it.
- A prefab must work when dropped into an empty scene.
- Do not store scene-instance references inside ScriptableObjects.

## Workflow

1. Audit: list hard references, singletons, large classes, and where scene objects hold persistent data. Map who reads and writes each piece of shared data.
2. Asset design: create variable assets for shared runtime values, event channel assets for cross-system triggers, and runtime sets for entity groups. Organise by domain under one folder and add create-menu attributes so designers can make new ones.
3. Decompose large behaviours into single-purpose components and wire them in the inspector through those assets.
4. Handle lifecycle: subscribe in the enabling callback, unsubscribe in the disabling callback, and avoid logic in `Update` that could react to an event.
5. Editor tooling: custom inspectors or property drawers for frequently used assets; when scripts modify assets in the editor, mark them dirty so Unity saves the change.
6. Scenes: treat each load as a clean slate, keep scenes lean, and use addressable or asset-based configuration for setup. Replace `Resources` loads with a managed asset loading approach where you need memory control.
7. Verify: open each prefab in an isolated scene, check for compile and console errors, and run play-mode tests for events and runtime sets. Use the Profiler to confirm that event-driven code removed per-frame cost and allocations.
8. Consider the entity component system or the job system only for measured CPU bottlenecks; keep gameplay code in components when editor friendliness matters more.

## Guardrails

- Size limits such as "150 lines" are rules of thumb, not requirements; judge by responsibilities.
- Package names, APIs, and editor menus change between Unity versions. Check the installed version's documentation.
- Do not rewrite serialized assets in bulk without version control and a backup; renamed fields can drop data.
- Read the Unity version from `ProjectSettings/ProjectVersion.txt` and the package versions from `Packages/packages-lock.json`. Check Unity's latest stable release notes before you use an API.
- When you rename a serialized field, add `[FormerlySerializedAs("oldFieldName")]` with the field's old name so saved values carry over. Test with an asset made by the last release.
- Test an event raised before its listener is enabled, a runtime set that still holds destroyed entities, and a scene loaded twice.

Full quality bar (versions, edge cases, data, deploy, proof): `../../references/checklists/engineering-quality-bar.md`.

## Output format

```text
Audit findings: [hard refs, singletons, large classes]
New assets: [type, purpose, location]
Components split: [before -> after]
Lifecycle and editor-tooling changes: [..]
Checks run: [isolated prefab loads, play-mode tests, profiler result]
Risks: [serialization, version]
```

Adapted from agency-agents/game-development/unity/unity-architect.md (agency-agents, MIT).
