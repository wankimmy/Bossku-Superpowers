# Posting a review

Only when the user asks you to post (`SKILL.md`, step 6).

## Write it short

- One point per sentence, about 15 words or fewer. Split "and", "which" and "so" chains.
- Lead with what to change, then the place (`file:line`), then one short reason.
- Bullets over paragraphs. Long proof (test output, before and after tables) goes in a `<details>` block.

## Number the findings

- Number them F1, F2... per PR, most severe first.
- Keep the numbers across rounds. New findings carry on after the last number. Each earlier finding is marked Fixed (commit), Still open, or Disputed (quote the reply).
- A review posted without numbers: in its next round, number its findings in the order it gave them and say so once.

## Inline comments

- Every finding with a file:line, nits included (marked "Nit (optional)"), goes as an inline comment on that line. It opens with its number and level (`F1 - P1`), so the author's reply in that thread names it.
- A finding on a line outside the diff cannot go inline: the review body names it.
- The review summary gives the reviewed SHA, lists each finding in one line, and says what you ran.

## Before posting: re-check

- **Head:** if it moved since the pin, the new commits are unreviewed. Read them first.
- **Base:** if it moved, list what landed on the files in scope, rerun `git merge-tree --write-tree <head> <base tip>`, and redo any count taken from code outside the diff.
- **Merge-only commits:** after "Update branch", each new commit must be a merge whose tree equals `git merge-tree --write-tree <c>^1 <c>^2`. Anything of its own is a new round.
- **Mergeable and CI:** check both again (`SKILL.md`, Rules that decide the verdict).

## Submit

- Create a pending review pinned to the reviewed `commit_id`, with the inline comments in it.
- Submit it with the event the user picks, event and body in one call.
- Read it back (the body length and the comment count).
