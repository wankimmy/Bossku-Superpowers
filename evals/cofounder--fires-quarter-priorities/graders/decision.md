---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Gives one main recommendation for the quarter, not a list of equally weighted options.
- Reasons from the numbers given, for example that 8% monthly churn loses about 3 of the 40 stalls a month, or that revenue is roughly RM1,960 a month against RM60k cash.
- Says what not to do yet (the Go rewrite, the TikTok push, or both) and why.
- Names a concrete metric or check, with a target or a time frame, that would show the bet is working.

Pass only if every point holds.
