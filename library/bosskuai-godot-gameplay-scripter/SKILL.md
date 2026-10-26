---
name: bosskuai-godot-gameplay-scripter
description: "Use when writing or reviewing Godot 4 gameplay code: typed GDScript, signal design, node composition, autoload and event bus use, scene lifecycle, resources for data, and GDScript versus C# boundaries."
---

# BosskuAI Godot Gameplay Scripter

Use this skill for Godot 4 gameplay systems built from scenes, nodes, signals, and resources, with static typing turned on.

## How this differs from nearby skills

- **`bosskuai-game-designer`**: what the game should do on paper. This skill is how to implement it in Godot code.
- **`bosskuai-game-audio-engineer`**: audio middleware and mixing; here only the gameplay scripting side.
- **`bosskuai-csharp-testing`** and **`bosskuai-dotnet-patterns`**: general C# practice, used when a Godot project mixes C#.
- **`bosskuai-tdd-loop`**: red-green loop, reusable for isolated scene tests.

## Principles

- Compose behaviour from small child nodes (a health component, a movement component) instead of deep inheritance.
- Every scene should run alone (play the scene directly) without assuming a parent or sibling.
- Components talk upward with signals and downward with direct calls. Avoid reaching into parents or `owner`.
- Type everything: variables, parameters, returns, typed arrays, typed exports, typed signal parameters. Raise typing warnings to errors in project settings if the team agrees.
- Autoloads hold true global state only (settings, save data, event bus). Gameplay logic does not belong in them, and they cannot be tested in isolation.
- Use custom `Resource` classes for static data such as enemy stats so designers edit assets, not code.

## Workflow

1. Decide which scenes are self-contained units and which signals cross scene boundaries. Put only genuine cross-scene events on an event-bus autoload.
2. Declare signals first with typed parameters and doc comments; treat them like a public API.
3. Split monolithic character scripts into components, each with one concern and its own exports.
4. Acquire node references with typed `@onready` variables or exported node paths, not scattered runtime path lookups.
5. Lifecycle: set up in `_ready`, not `_init`; disconnect or use one-shot connections where lifetimes differ; free nodes with `queue_free`.
6. Replace per-frame polling with signals when state changes are rare.
7. Run each scene standalone and fix errors before integration. Use assertions for development invariants.
8. When moving to C#, remember signal naming and connection syntax differ between languages; check the engine documentation for the installed 4.x version.

## Guardrails

- Names, annotations, and APIs change between Godot 4.x minor releases. Verify against the installed version's docs.
- Profile before moving code to C# or a native extension; justify with data.
- Do not edit project settings or export presets without saying so.

## Output format

```text
Scene tree and component split: [..]
Signals: [name, typed params, emitter, listeners]
Autoloads and why each is global: [..]
Typing and lifecycle issues fixed: [..]
Standalone scene test result: [..]
```

Adapted from agency-agents/game-development/godot/godot-gameplay-scripter.md (agency-agents, MIT).
