---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Names at least one existing Python library for natural-language date parsing (for example dateparser or parsedatetime), or explains what the standard library does not cover.
- Says what to check before adopting (recent maintenance, adoption, license, open security issues), and does not claim it checked anything it could not check here.
- Gives a clear recommendation (adopt, wrap or build) and a small next step.

Pass only if every point holds.
