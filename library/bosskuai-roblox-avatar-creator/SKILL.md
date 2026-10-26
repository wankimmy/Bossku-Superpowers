---
name: bosskuai-roblox-avatar-creator
description: "Use when making Roblox avatar items: UGC accessories and layered clothing, mesh and texture limits, attachments and cages, HumanoidDescription outfit code, and a pre-submission checklist for the Creator Marketplace."
---

# BosskuAI Roblox Avatar Creator

Use this skill to build avatar items that pass Roblox validation and moderation, and to implement in-experience outfit customisation.

## How this differs from nearby skills

- **`bosskuai-blender-motion-state-inspection`**: inspecting Blender motion and state, not Roblox item specs.
- **`bosskuai-game-audio-engineer`**: game sound; this skill is avatar assets and Luau avatar code.
- **`bosskuai-3d-web-development`**: web 3D, not Roblox Studio.
- **`bosskuai-narrative-designer`**: story content for games; separate from item pipelines.

## Workflow

1. Look up the current Roblox UGC requirements for the item type first. Limits for triangles, texture size, naming, attachments and eligibility change; do not rely on remembered numbers.
2. Model within the triangle limit from the start, leaving headroom for exporter overhead. Use a single mesh, a clean UV layout in range with padding between islands, transforms applied, and the pivot at the attachment point.
3. Textures: sized and formatted to the current spec, with transparency in the alpha channel, and no real-world brands, logos or other people's content.
4. Attachments: the attachment object name must match Roblox's standard names for the item slot. Test on the supported body types and scales.
5. Layered clothing: rig to the official reference rig, give every vertex valid bone weights, and author the required inner and outer cage meshes per current docs.
6. Test in Studio through the avatar import flow across all body presets and through idle, walk, run, jump and sit animations, checking for clipping.
7. Outfit code: use `HumanoidDescription` (get the applied description, set fields, apply) and persist saved outfits on the server. Verify purchases on the server, not from client-side callbacks alone.
8. Submission package: accurate name and description, category, price researched from comparable items, thumbnail that clearly shows the item, asset files.
9. Moderation pre-check: text on the item, brand references, face coverings, weapon-like shapes. If rejected, read the stated reason before changing anything.

## Guardrails

- Do not submit, publish or price an item on the user's Roblox account without explicit approval.
- Never use copyrighted or branded content without a licence.
- Review times and moderation outcomes vary; do not promise approval.
- Keep marketplace pricing claims as research notes, not guarantees.

## Output format

```text
Item: [type, slot]
Spec check: [tris, UV, textures, attachment, versions checked]
Rig and cages: [bones, inner/outer cage status]
Tests: [body types, animations, clipping notes]
Submission package: [name, description, category, price note, files]
Moderation risks: [list]
```

Adapted from agency-agents/game-development/roblox-studio/roblox-avatar-creator.md (agency-agents, MIT).
