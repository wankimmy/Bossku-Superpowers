---
type: llm
focus: {"source": "file", "path": "export.py"}
---

Pass criteria:
- Fields are written with correct CSV quoting (for example the csv module), so commas, quotes and newlines inside a field are handled; commas are not just stripped or replaced.
- The header row is unchanged.

Pass only if every point holds.
