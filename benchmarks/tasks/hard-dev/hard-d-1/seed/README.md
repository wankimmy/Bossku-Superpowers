# archive_tool

Unpacks a tar bundle that a user submitted (a project upload) into a scratch
workspace directory so the rest of the pipeline can scan its files.

```python
from archive_tool import extract_archive

written = extract_archive("submission.tar", "/tmp/workspace/abc123")
# written -> sorted list of relative paths that were created under dest_dir
```

Run the visible tests: `python -m unittest discover -s tests`
