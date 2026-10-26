---
type: llm
focus: {"source": "file", "path": "rename_photos.py"}
---

Pass criteria:
- There is a `--dry-run` option; in dry-run mode no os.rename call runs.
- Dry-run mode prints each planned rename.
- Without the flag the script still renames and prints exactly as before.

Pass only if every point holds.
