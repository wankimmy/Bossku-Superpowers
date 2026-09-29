# CLAUDE.md Management Checklist

> If the request is general, ambiguous, or touches many files, ask clarifying yes/no questions before acting.

- Is the canonical rule owner clear: root `AGENTS.md`, `CLAUDE.md`, `.claude/rules/`, command, skill, reference, or memory?
- Are Claude-specific mirrors short, intentional, and consistent with shared BosskuAI rules?
- Are stale model names, commands, paths, or tool assumptions removed or updated?
- Are vague instructions rewritten into concrete actions or guardrails?
- Are durable session learnings routed through shared memory before Claude-only surfaces?
- Are secrets, private details, and untrusted-content assumptions excluded?
- Are links and referenced files still valid after the edit?

- Does startup-context review include imported files and unconditional rules rather than only the entry stub?
- Are nested and ancestor instructions scoped correctly for the actual working directory?
- Are real imports distinguished from code examples, and repeated corrections promoted only when verified?
- Are prose guidance and harness-enforced settings clearly distinguished?
