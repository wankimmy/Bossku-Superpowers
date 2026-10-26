---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Path traversal or overwrite through the user-controlled filename (for example ../ segments), with the fix (a generated name, or a safe name plus a resolved-path check).
- The MIME type comes from the client and can be faked: check the real content (magic bytes or an image library) and an extension allowlist.
- No size limit: set a maximum upload size.
- Files land in a public static folder, so a malicious file (for example HTML or SVG with script) can be served from the site's origin: store outside the web root or serve with safe headers.

Pass only if every point holds.
