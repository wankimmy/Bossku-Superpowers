---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Starts from the user's goal (pay quickly and confidently) and reorders around it: the pay action after the summary and fields (for example a sticky bottom button), with the promo field made less prominent.
- Lists the states the screen needs: inline field errors, loading or disabled while paying, payment failure and success.
- Mobile and accessibility basics: body text at least 16px with enough contrast, touch targets around 44px, labelled inputs with the right input types and autocomplete.
- Gives implementation primitives: a component breakdown with key props or state (for example idle → submitting → failed or succeeded).

Pass only if every point holds.
