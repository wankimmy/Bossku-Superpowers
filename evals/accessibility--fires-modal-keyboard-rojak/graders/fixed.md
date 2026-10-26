---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Gives it dialog semantics: role="dialog" with aria-modal="true" and a name (aria-labelledby the title), or the native `<dialog>` element with showModal().
- Moves focus into the modal when it opens, keeps Tab inside it, closes on Escape, and returns focus to the button that opened it.
- Hides or inerts the page behind the modal from screen readers while it is open.

Pass only if every point holds.
