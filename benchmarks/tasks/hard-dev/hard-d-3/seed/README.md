# url_fetcher

Fetches a resource from a URL, but only if its host is on a configured
allowlist (used by scrapers that pull data from partner sites).

```python
from url_fetcher import fetch

data = fetch("https://partner.example.com/feed.json", allowed_hosts=["partner.example.com"])
```

`opener` defaults to a real HTTP GET (`urllib.request.urlopen`), but every
caller in the test suite passes a fake one instead so nothing ever touches
the real network. An opener is just `opener(url) -> bytes`; it may instead
raise `url_fetcher.Redirect(location)` to signal a 3xx response pointing at
`location`.

Run the visible tests: `python -m unittest discover -s tests`
