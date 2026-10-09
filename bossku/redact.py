from __future__ import annotations

import re

SENSITIVE_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|password|bearer)\s*[:=]\s*\S+"),
    re.compile(r"(?i)[\"'](api[_-]?key|secret|token|password)[\"']\s*:\s*[\"'][^\"']+[\"']"),
    re.compile(r"(?i)\bBearer\s+(?=[A-Za-z0-9._~+/=-]*\d)[A-Za-z0-9._~+/=-]{8,}"),     # needs a digit: "Bearer authentication" stays
    # A PEM key: header to END line, or the header plus the base64 lines of a cut-off one. A bare header still matches,
    # and nothing past it is taken unless it looks like key lines. A "-" is skipped in the body only when it is single,
    # so "Proc-Type:" lines stay inside the block while the next "-----" ends the scan (no quadratic run on many headers).
    re.compile(r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY(?: BLOCK)?-----"
               r"(?:(?:[^-]|-(?!--)){0,16384}?-----END (?:[A-Z0-9]+ )*PRIVATE KEY(?: BLOCK)?-----"
               r"|(?:\s+[A-Za-z0-9+/=]{20,}){1,200})?"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    # Vendor prefixes. Each starts on a fixed prefix, so ordinary words do not match.
    re.compile(r"\bxox[abposr]-[A-Za-z0-9-]{10,}"),                                    # Slack
    re.compile(r"\bAIza[0-9A-Za-z_-]{35}"),                                            # Google API key
    re.compile(r"\b(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{10,}"),                         # Stripe
    re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}"),                                         # GitLab
    re.compile(r"\bhf_[A-Za-z0-9]{30,}"),                                              # Hugging Face
    re.compile(r"\bnpm_[A-Za-z0-9]{36}\b"),                                            # npm
    # JWT. The lookbehind (not \b) keeps a long run of "eyJ-eyJ-" linear, because "-" is also inside the class.
    re.compile(r"(?<![A-Za-z0-9_-])eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"),
    re.compile(r"(?i)\bAuthorization:\s*Basic\s+[A-Za-z0-9+/]{8,}={0,2}"),
    # user:password in a URL. The lookbehind and lookahead leave the scheme, the host and the "@".
    re.compile(r"(?<=://)[^\s/:@]*:[^\s/@]+(?=@)"),
    # AWS_SECRET_ACCESS_KEY=..., STRIPE_SECRET_KEY=...: a name that ends in a secret word. "max_tokens=4096" stays (the
    # word must sit right before "="), but a code line such as "cache_key = x" is redacted too.
    re.compile(r"(?i)\b[A-Z0-9_]*(?:SECRET|PASSWORD|PASSWD|TOKEN|CREDENTIALS?|_KEY)\s*=\s*\S+"),
]


def redact(text: str) -> str:
    out = text
    for pattern in SENSITIVE_PATTERNS:
        out = pattern.sub("[REDACTED]", out)
    return out


# A shell command carries secrets that notes do not: flag values, short options, a password on a login line. Each
# entry is (pattern, replacement) and keeps the program and the flag, so the brief still shows what ran.
COMMAND_PATTERNS = [
    # --password x, --db-pass=x, --api-key x, --client-secret=x. The flag must end in the word: --password-stdin and
    # --bypass take no secret.
    (re.compile(r"(?i)(--(?:[a-z0-9]+-)*(?:password|passwd|pass|token|secret|api-?key|access-?key|auth|credentials?)(?:=|\s+))(?!-)\S+"),
     r"\1[REDACTED]"),
    # gh secret set NAME --body VALUE (or -b)
    (re.compile(r"(?i)(\bsecrets?\s+set\b[^\n|;&]*?\s(?:--body|-b)(?:=|\s+))\S+"), r"\1[REDACTED]"),
    # curl -u user:pass, -fsSLu user:pass, --user user:pass
    (re.compile(r"(?i)(\bcurl\b[^\n|;&]*?\s(?:-[a-zA-Z]*u|--user)(?:=|\s*))\S+"), r"\1[REDACTED]"),
    # docker login -u bob -p secret
    (re.compile(r"(?i)(\b(?:docker|podman|nerdctl)\s+login\b[^\n|;&]*?\s-p(?:=|\s*))\S+"), r"\1[REDACTED]"),
    # mysql -pSecret: only when attached (a bare -p asks for it, and mkdir -p stays); -P is the port, so case matters
    (re.compile(r"(\b(?i:mysql|mysqldump|mysqladmin|mariadb|mariadb-dump)\b[^\n|;&]*?\s-p)(?=\S)\S+"), r"\1[REDACTED]"),
    # DB_PASS=..., MYSQL_PWD=...: a name that ends in PASS or PWD. A bare PWD is the working folder, so it needs a prefix.
    (re.compile(r"(?i)\b(?:(?:[a-z0-9]+_)+(?:pass(?:phrase)?|pwd)|pass(?:phrase)?)\s*=\s*\S+"), "[REDACTED]"),
]


def redact_command(text: str) -> str:
    """`redact` plus the command-line forms above, for text that is a shell command."""
    out = text
    for pattern, replacement in COMMAND_PATTERNS:
        out = pattern.sub(replacement, out)
    return redact(out)
