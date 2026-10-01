# static_files

Serves file contents out of a fixed content root for internal tooling (docs
previews, asset bundles, etc).

```python
from static_files import read_file

data = read_file("/srv/content-root", "guides/intro.txt")
```

Run the visible tests: `python -m unittest discover -s tests`
