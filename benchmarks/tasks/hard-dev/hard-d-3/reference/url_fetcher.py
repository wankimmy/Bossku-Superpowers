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


ALLOWED_SCHEMES = ("http", "https")
MAX_REDIRECTS = 3


def _default_opener(url):
    with urllib.request.urlopen(url) as resp:  # pragma: no cover - real network
        return resp.read()


def _validate(url, allowed_hosts):
    parsed = urllib.parse.urlsplit(url)

    scheme = parsed.scheme.lower()
    if scheme not in ALLOWED_SCHEMES:
        raise URLSecurityError(f"scheme not allowed: {parsed.scheme!r}")

    if "@" in parsed.netloc:
        raise URLSecurityError(f"userinfo not allowed in URL: {url!r}")

    host = parsed.hostname
    if not host:
        raise URLSecurityError(f"URL has no host: {url!r}")
    host = host.lower()
    if host.endswith("."):
        host = host[:-1]

    allowed_lower = {h.lower() for h in allowed_hosts}
    if host not in allowed_lower:
        raise URLSecurityError(f"host not allowlisted: {host!r}")


def fetch(url, allowed_hosts, opener=None):
    """Fetch `url` via `opener`, following only allowlisted redirects.

    Every URL actually requested - the original one and any redirect
    target - is validated against `allowed_hosts` before `opener` is
    called with it. Follows at most MAX_REDIRECTS redirects.
    """
    opener = opener or _default_opener
    current = url
    for attempt in range(MAX_REDIRECTS + 1):
        _validate(current, allowed_hosts)
        try:
            return opener(current)
        except Redirect as redirect:
            if attempt == MAX_REDIRECTS:
                raise URLSecurityError("too many redirects") from redirect
            current = redirect.location
    raise URLSecurityError("too many redirects")  # pragma: no cover - unreachable
