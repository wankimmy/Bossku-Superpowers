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

## Extra checks by theme

Use the themes that match the system; skip the rest.

**AI-generated and web/serverless code**
- A secret behind a client-exposed prefix (`NEXT_PUBLIC_`, `VITE_`, `EXPO_PUBLIC_`) or compiled into the bundle is leaked. A designed-public key (publishable, anon) is not a finding.
- "RLS enabled" is a claim to verify: RLS on with no policy denies all; `USING (true)` allows all. Public buckets and tables without RLS count too.
- Authorize on server-only identity (`app_metadata`), never on client-editable fields (`user_metadata`, a role in the body or header).
- Untrusted input in the system prompt, or in a call that also has tools, is high severity. Untrusted text in its own user message with no tools is the safe pattern; do not flag it. Label this check heuristic.

**Secrets**
- A leaked secret is burned from commit time. Order: rotate at the provider, swap the code to a secret-store reference, purge git history (coordinate the rewrite), audit use during the exposure window, then fix why the scanner missed it.
- Prefer short-lived, least-privilege credentials (OIDC in CI, workload identity) over static keys. Never print a secret value in a report; give type, location, redacted preview.

**Cloud and infrastructure**
- No root account for daily work; MFA for humans; no wildcard IAM in production; disable dormant accounts.
- No `0.0.0.0/0` to management ports; workloads in private subnets; default-deny network policy between pods or services.
- Storage encrypted, public access blocked, audit logs sent to separate immutable storage; alert on IAM and security-group changes.
- Containers: scanned image, non-root. On AWS use IMDSv2 so SSRF cannot steal instance credentials.

**Incident and detection**
- Order: triage and open a timeline, preserve volatile evidence before containing, contain, scope from logs, rebuild from known-good, reset credentials and sessions, post-mortem with owners and dates.
- A detection rule needs a test against a known sample, a false-positive review, and a link to the behaviour it covers. A rule that fires constantly gets ignored.

**Compliance and scope**
- Evidence must show a control worked over the whole period, not only today. Every gap names the control, current state, target state, fix, effort. Never report "compliant" or "% secure" from a code scan.
- Smart contracts: tools are a first pass only; check reentrancy, access control, oracle and flash-loan paths, and that audited code matches deployed bytecode.
- Pen tests and attacker emulation run only inside written scope and rules of engagement.

Adapted from agency-agents/security/ (AI-generated-code auditor, secrets, cloud architect, incident responder, threat detection, blockchain auditor, compliance auditor, pen tester) (agency-agents, MIT).

## More checks

**Uploads and sessions**
- Validate uploads on the server by size, extension allowlist and sniffed content, not the client-sent MIME type alone; store outside the web root under a generated name.
- Keep session tokens in `HttpOnly; Secure; SameSite` cookies, not `localStorage`. Cookie auth on state-changing routes also needs a CSRF token or a strict SameSite policy. Rate-limit harder on expensive and search endpoints than on plain reads.

**Reportable-vulnerability triage (bounty or disclosure work)**
- Read the program scope, `SECURITY.md` and exclusions first. Look for remotely reachable, user-controlled paths: SSRF, auth bypass in guards, upload or deserialization to code execution, SQL and command injection in handlers, path traversal, auto-triggered XSS.
- Drop local-only `pickle`/`torch.load`, `eval` in CLI tools, `shell=True` on hardcoded commands, missing headers alone, generic rate-limit complaints, self-XSS, and demo or test code. Static scanner output is triage input only; read the path end to end.
- Before reporting: the input is truly user-controlled, the sink is exploitable, a minimal safe PoC works, it is not a known advisory or open ticket, and the target is in scope. Report: description, vulnerable file and lines, PoC, impact, affected version.

**Agent configuration (`CLAUDE.md`, settings, MCP, hooks, agent files)**
- Critical: secrets in config, `Bash(*)` or other wildcard allow rules, hooks that interpolate file names or input into shell strings, MCP servers that run shells.
- High: instructions that tell the agent to auto-run commands (prompt-injection vector), no deny list, agents with Bash they do not need.
- Medium: hooks that swallow errors (`2>/dev/null`, `|| true`), unpinned `npx -y` MCP servers. Do not apply auto-fixes or install a scanner without the user's say-so.

Adapted in part from ECC skills/security-bounty-hunter, skills/security-review and skills/security-scan (affaan-m/ECC, MIT).
