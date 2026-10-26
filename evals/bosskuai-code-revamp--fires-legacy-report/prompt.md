---
description: "Refactor a messy legacy function without changing behaviour: pin it with tests first."
tags: ["lean", "bosskuai-code-revamp", "fires", "work"]
max_turns: 30
timeout_seconds: 900
allowed_tools: ["Skill", "Read", "Glob", "Grep", "Write", "Edit", "Bash(python:*)", "Bash(python3:*)", "Bash(py:*)"]
---

This legacy module works but it's a mess. Refactor it for readability without changing behaviour. Save it as `report.py` first, and keep the function name and signature the same.

```python
def build_report(orders):
    out = []
    t = 0
    for o in orders:
        if o['status'] == 'paid':
            if o['currency'] == 'MYR':
                amt = o['amount']
            else:
                if o['currency'] == 'SGD':
                    amt = o['amount'] * 3.4
                else:
                    if o['currency'] == 'USD':
                        amt = o['amount'] * 4.4
                    else:
                        amt = 0
            t = t + amt
            out.append(o['id'] + ': ' + str(round(amt, 2)))
        else:
            if o['status'] == 'refunded':
                if o['currency'] == 'MYR':
                    amt = o['amount']
                else:
                    if o['currency'] == 'SGD':
                        amt = o['amount'] * 3.4
                    else:
                        if o['currency'] == 'USD':
                            amt = o['amount'] * 4.4
                        else:
                            amt = 0
                t = t - amt
                out.append(o['id'] + ': -' + str(round(amt, 2)))
    out.append('TOTAL: ' + str(round(t, 2)))
    return '\n'.join(out)
```
