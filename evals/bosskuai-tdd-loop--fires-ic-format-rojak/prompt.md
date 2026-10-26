---
description: "Rojak red-green-refactor request: validate the Malaysian IC number format."
tags: ["lean", "bosskuai-tdd-loop", "fires", "work"]
max_turns: 30
timeout_seconds: 900
allowed_tools: ["Skill", "Read", "Glob", "Grep", "Write", "Edit", "Bash(python:*)", "Bash(python3:*)", "Bash(py:*)"]
---

buat TDD style ya, red-green-refactor. nak function `is_valid_ic(ic)` dalam `ic.py` untuk check format IC Malaysia: 12 digit, boleh ada dash ikut format YYMMDD-PB-#### atau tanpa dash langsung, dan 6 digit pertama mesti tarikh yang wujud. return True/False je. guna unittest, takyah library lain.
