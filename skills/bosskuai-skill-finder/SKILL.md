---
name: bosskuai-skill-finder
description: "Use when no listed skill fits (marketing, SEO, ads, legal, finance, design, mobile, DevOps) or the right skill is unclear."
---

# BosskuAI Skill Finder

The skill list shows the most-used skills only. The rest of the library is installed too and is found by search.

1. Run `bossku skills find "<the task, in the user's words>"`. Search for the work, not for a skill: leave out the question about skills ("is there a Bossku skill for", "which skill should I use", "ada skill untuk"). Those words pull the search towards the skills about Bossku itself.
2. Read `selection.selected`. The first entry is the main skill; later entries cover other parts of the request. Skip anything in `selection.deferred` and any skill marked user-only.
3. Load each selected skill. If `access` is `listed`, use the Skill tool. If it is `library`, run `bossku skills show <skill_id>` and follow what it prints.
4. If `confident` is false, read the descriptions and pick the best fit, or carry on without a skill.

Search once per job. Search again only when the task changes.

If the user wants a new skill built, search first: pull 3-5 keywords plus synonyms, check installed skills, then (if remote search is available) at most a few targeted GitHub or web queries. Vet any external skill before adopting it: read it for unexpected shell commands, file writes, network calls, credential handling or installs, and copy it to review the diff instead of editing the original. Rank by name match, description match, then local over remote over web-only mention, show at most 10, and offer use as-is, fork, or create fresh. Create only after the user picks that or nothing close exists; if they say to skip the search, do.

Adapted in part from ECC skills/skill-scout (affaan-m/ECC, MIT).
