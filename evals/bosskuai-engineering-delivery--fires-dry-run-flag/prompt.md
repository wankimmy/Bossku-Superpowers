---
description: "Add a flag to an existing script without changing its normal behaviour, and prove both modes."
tags: ["lean", "bosskuai-engineering-delivery", "fires", "work"]
max_turns: 30
timeout_seconds: 900
allowed_tools: ["Skill", "Read", "Glob", "Grep", "Write", "Edit", "Bash(python:*)", "Bash(python3:*)", "Bash(py:*)"]
---

Save the script below as `rename_photos.py`, then add a `--dry-run` flag that prints each planned rename without renaming anything. Keep the normal behaviour exactly as it is, and make sure both modes work before you tell me it's done.

```python
import argparse
import os


def plan(folder, prefix):
    names = sorted(n for n in os.listdir(folder) if n.lower().endswith(".jpg"))
    return [(n, f"{prefix}_{i:03d}.jpg") for i, n in enumerate(names, start=1)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    parser.add_argument("--prefix", default="photo")
    args = parser.parse_args()
    for old, new in plan(args.folder, args.prefix):
        os.rename(os.path.join(args.folder, old), os.path.join(args.folder, new))
        print(f"{old} -> {new}")


if __name__ == "__main__":
    main()
```
