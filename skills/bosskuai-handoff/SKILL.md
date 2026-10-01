---
name: bosskuai-handoff
description: "Use when the user asks to hand off, wrap up for another agent or session, or write a continuation document — compacts the conversation into <memory-dir>/handoff.md so a fresh agent in any tool can continue. Context-pressure handoffs belong to bosskuai-context-limit-continuation."
argument-hint: "What will the next session be used for?"
---

# Handoff

For compacting the current conversation into a document a fresh agent, in any tool or model, can continue from. A handoff forced by context or token pressure instead uses `bosskuai-context-limit-continuation`.

1. **Resolve where it goes first.** Run `bossku memory-path --project <project-root>` for `<memory-dir>` — a vault path when `memory_storage` is obsidian, or `.bossku/` in the repo under legacy mode. Follow whichever it returns; never assume `.bossku/`. If no memory location is configured and the user does not want one set up, write to the OS temp directory and print the path instead.
2. **Write to `<memory-dir>/handoff.md`**, creating the directory if missing. Under legacy repo mode, add `.bossku/` to `.gitignore` if it is not already ignored.
3. **Overwrite the whole file; never append.** It holds only the current unfinished work, not a history. Tell the user to clear it once the work is done.
4. **Fill every section from `references/session-handoff-template.md`**: goal and status (done / not done / blocked); key decisions already made, with the reason, so the next agent does not reopen them; files and artifacts touched, linked by path or URL rather than pasted in full; verification performed *and* verification not performed; open risks and follow-ups; suggested next skills by id; a `FOR_NEXT_MODEL` paste block of ordered next steps with concrete paths or commands.
5. **Redact by hand before saving**: API keys, passwords, tokens, personal data. The handoff file is ephemeral and does not go through `bossku remember`.
6. **Route durable lessons elsewhere.** Anything worth keeping beyond this one task goes through `bosskuai-continuous-learning`, not into `handoff.md`.
7. **Don't duplicate** content that already lives in a PRD, plan, ADR, issue, or commit — link it instead of copying it in.

If the user passed arguments, treat them as the next session's focus and write the document around that.

The full template and the memory-first handoff protocol: `reference.md`.
