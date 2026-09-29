# Skill Creator Checklist

> If the request is general, ambiguous, or touches many files, ask clarifying yes/no questions before acting.

- Is the recurring job-to-be-done distinct from existing skills?
- Does frontmatter include precise `name` and trigger-oriented `description`?
- Does the skill explain nearby-skill boundaries and exclusions?
- Is `SKILL.md` concise, with longer material moved to references?
- Are guardrails specific to common failure modes for this skill?
- Are output expectations concrete enough for the next model to execute?
- Do referenced files exist and use portable relative paths?
- Was the skill checked against realistic trigger, adjacent non-trigger, ambiguous, and high-risk prompts?
- If output quality depends on format, does the skill show at least one input/output example rather than only describing the format?

- Does the skill capture specific gotchas or failure-oriented guardrails rather than obvious advice?
- Are goals and constraints clear without imposing needless implementation steps?
- Do helper scripts and sidecars survive installation with documented prerequisites and side effects?
- Are host-only fork, invocation, hook, and dynamic-context features verified rather than assumed portable?
- Are static routing checks, behavioral evaluation, and usage measurement reported separately?
