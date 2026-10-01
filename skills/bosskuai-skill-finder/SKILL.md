---
name: bosskuai-skill-finder
description: "Use when no listed skill fits (marketing, SEO, ads, legal, finance, design, mobile, DevOps) or the right skill is unclear."
---

# BosskuAI Skill Finder

The skill list shows the most-used skills only. The rest of the library is installed too and is found by search.

1. Run `bossku skills find "<the request, in the user's words>"`.
2. Read `selection.selected`. The first entry is the main skill; later entries cover other parts of the request. Skip anything in `selection.deferred` and any skill marked user-only.
3. Load each selected skill. If `access` is `listed`, use the Skill tool. If it is `library`, run `bossku skills show <skill_id>` and follow what it prints.
4. If `confident` is false, read the descriptions and pick the best fit, or carry on without a skill.

Search once per job. Search again only when the task changes.
