---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Every input gets a visible label tied to it (label for/id), not just a placeholder.
- The radio buttons are grouped in a fieldset with a legend, each with its own label.
- The clickable div becomes a real `<button type="submit">`, so it works from the keyboard.
- The hint gets enough contrast (#bbb on white fails 4.5:1) and is linked with aria-describedby, and errors are announced (for example role="alert" or aria-live) and not shown by colour alone.

Pass only if every point holds.
