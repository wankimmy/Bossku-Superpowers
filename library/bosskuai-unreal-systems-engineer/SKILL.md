---
name: bosskuai-unreal-systems-engineer
description: "Use when architecting Unreal Engine 5 gameplay systems: the C++ and Blueprint boundary, Gameplay Ability System setup and replication, UObject memory safety, Nanite and Lumen constraints, tick costs and module build files."
---

# BosskuAI Unreal Systems Engineering

Use this skill to decide what belongs in C++ versus Blueprint, set up the Gameplay Ability System safely, and avoid common UE5 performance and memory pitfalls.

## How this differs from nearby skills

- **`bosskuai-cpp-coding-standards`**: general C++ Core Guidelines. This skill adds Unreal's reflection, garbage collection and module system.
- **`bosskuai-cpp-testing`**: C++ test frameworks; Unreal automation tests need their own setup.
- **`bosskuai-godot-multiplayer-engineer`**: networking in Godot, a different engine.
- **`bosskuai-performance-profiling`**: general profiling method; here the tools are Unreal Insights and engine stat commands.

## Workflow

1. Define ownership: what engineers implement in C++ versus what designers extend in Blueprint. Document the boundary per system.
2. Put per-frame logic, engine extensions (movement, physics callbacks, collision) and types Blueprint cannot represent in C++. Use Blueprint for flow, UI and prototyping. Expose C++ via `UFUNCTION` specifiers (BlueprintCallable, BlueprintImplementableEvent, BlueprintNativeEvent).
3. Reduce tick cost: avoid tick where a timer or event works, set tick intervals, and store and clear timer handles on end of play.
4. Memory safety: mark UObject pointers with `UPROPERTY()`, use weak object pointers for non-owning references, `IsValid()` for UObject checks, and shared pointers for non-UObject heap data. Null-check actors across frames.
5. Gameplay Ability System: add the required modules to the `.Build.cs`, derive abilities and attribute sets from the engine base classes, use replication notify macros for attributes, use gameplay tags rather than strings, change attributes through gameplay effects, and replicate through the ability system component.
6. Rendering: check Nanite and Lumen support for your engine version in the release notes and the editor visualisation modes before planning content around them; budget instances and verify mesh compatibility early.
7. Build hygiene: keep module dependencies explicit and non-circular, use reflection macros correctly, regenerate project files after changing build or project files.
8. Validate: profile with Unreal Insights before and after content changes; test abilities in play-in-editor with multiple clients and simulated latency; test tags and attributes in a packaged build.

## Guardrails

- Engine APIs, console variables and feature support change between UE5 minor versions. Check the installed version and its docs before relying on any limit or setting.
- Do not mutate replicated attributes directly; go through gameplay effects.
- Do not ship Blueprint tick logic in hot paths; measure before and after moving to C++.
- Do not delete or rewrite project assets or config without explicit user approval.
- Read the exact version from `MajorVersion`, `MinorVersion` and `PatchVersion` in `Engine/Build/Build.version` in the engine folder (the folder that holds `Engine/`). `EngineAssociation` in the `.uproject` may hold only major.minor, a GUID, a relative path, or nothing, so do not use it as the exact version. Then check the release notes before you use an API, a console variable or a limit.
- Renaming a saved property or class needs a core redirect in `DefaultEngine.ini` (`[CoreRedirects]`), or saved data and Blueprint references break. Ask the user to approve that config edit before you make it.
- Build every target you ship (Editor, Game, and Server if the project has one) after each change to a `.Build.cs` file.
- Test abilities with an actor destroyed mid-ability and a level unloaded during an effect.

Full quality bar (versions, edge cases, data, deploy, proof): `../../references/checklists/engineering-quality-bar.md`.

## Output format

```text
System: [feature]
C++/Blueprint split: [engineer-owned, designer-owned]
GAS plan: [attributes, abilities, tags, effects, replication]
Memory and tick risks: [list]
Rendering constraints: [version-checked notes]
Validation: [Insights capture, multi-client test, packaged build test]
```

Adapted from agency-agents/game-development/unreal-engine/unreal-systems-engineer.md (agency-agents, MIT).
