---
name: bosskuai-cybersecurity-risk
description: "Use when doing a cybersecurity review or hardening: privacy, abuse-case analysis, auth and authorization concerns, trust boundaries, and operational risk evaluation."
---

# Security: review and hardening

Name the attacker and what they control (input, filenames, URLs, headers, payloads), then what they could reach. Check every place untrusted data enters.

**When you write or fix code that takes untrusted input, check each line that applies:**

- **Paths and files:** reject absolute paths, drive letters, `..` segments (before normalising), backslash separators, NUL and control characters. Confirm the resolved real path is still inside the root (symlinks). For archives, refuse links, devices and odd member types, set limits (count, size, total size, depth), and fail before anything is written.
- **URLs and hosts:** use a real parser. Allowlist the scheme; compare the host exactly (case-insensitive, trailing dot), never by prefix, suffix or substring; ignore `user@host` userinfo; re-check every redirect and cap how many are followed.
- **SQL:** parameterize values; allowlist identifiers (column names, sort direction); escape LIKE wildcards; scope every query to the owner or tenant; check ownership on update and delete, not only on read.
- **Secrets and signatures:** compare with a constant-time function (`hmac.compare_digest`); pin the algorithm so it cannot be downgraded; sign the raw bytes; require a timestamp and reject replays and clock skew; use `secrets`, never `random`.
- **Output:** escape for the sink (HTML, shell, SQL, log lines: strip CR and LF). Keep secrets out of logs, URLs and error messages.
- **Resources:** bound size, depth, count and time, and reject early.
- **Fail closed:** unknown value means reject; an error means deny.
- **Still works:** legitimate input must keep passing (dots inside names, unicode, empty values, an allowed second host).

Write one test per attack input (it is rejected) and one per legitimate edge (it is still accepted).

**For a review:** go through STRIDE for each trust boundary, label every finding confirmed or inferred with a severity, and give the smallest fix. The OWASP list, auth and session checks, supply-chain rules, worked threat models, privacy and what to skip at MVP stage: read `reference.md` in this folder.
