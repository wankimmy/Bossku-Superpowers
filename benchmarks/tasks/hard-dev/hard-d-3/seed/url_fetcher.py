"""Fetch resources from an allowlisted set of hosts."""
import urllib.parse
import urllib.request


class URLSecurityError(Exception):
    """Raised when a URL is not safe to fetch."""


class Redirect(Exception):
    """Raised by an opener to signal that the server redirected to `location`."""

    def __init__(self, location):
        super().__init__(location)
        self.location = location


def _default_opener(url):
    with urllib.request.urlopen(url) as resp:  # pragma: no cover - real network
        return resp.read()


def fetch(url, allowed_hosts, opener=None):
    """Fetch `url` via `opener`, but only if its host is allowlisted."""
    opener = opener or _default_opener
    parsed = urllib.parse.urlsplit(url)
    host = parsed.hostname or ""
    if not any(allowed in host for allowed in allowed_hosts):
        raise URLSecurityError(f"host not allowed: {host}")
    return opener(url)
