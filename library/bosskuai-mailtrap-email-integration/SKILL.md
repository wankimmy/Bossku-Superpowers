---
name: bosskuai-mailtrap-email-integration
description: "Use when the task explicitly concerns mailtrap email integration. Guides agents through integrating transactional email sending via Mailtrap's Email API, including sandbox testing, domain verification, and API authentication. Use when implementing email-sending features, debugging delivery issues, or setting up safe dev/staging email testing."
metadata:
  origin: ECC-adaptation
---

# Mailtrap Email Integration — portable workflow

Guides agents through integrating transactional email sending via Mailtrap's Email API, including sandbox testing, domain verification, and API authentication. Use when implementing email-sending features, debugging delivery issues, or setting up safe dev/staging email testing.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-email-ops`, `bosskuai-browser-automation`, `bosskuai-cybersecurity-risk`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Core Concepts.
2. Anti-Patterns.
3. Best Practices.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the Mailtrap SDK or API version the project pins (lockfile or manifest), its latest stable release notes, and the sending domain's SPF, DKIM and DMARC records, all checked live at work time, and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Apply the source “Core Concepts”, “Anti-Patterns” guidance to the concrete request. Return the resulting mailtrap email integration artifact or diagnosis with source/command evidence for each conclusion.

- Send dev and staging mail only to a Mailtrap sandbox inbox. Keep the live API token in the secrets store, never in dev or staging config, and log each request and response with secrets and personal data masked (the token, recipient addresses, message bodies).
- Set explicit timeouts. Mailtrap's docs describe no idempotency key, so the app must prevent duplicates itself. Before each call, save a unique id for the email in the app's own record. On a success response, save the `message_ids` it returns. Treat a timeout or a 500 as an unknown result, not a failure: do not resend until someone has checked Mailtrap Email Logs for that email, or accepts a possible duplicate. Retry only a clear rejection, such as 429, with capped backoff. Honour `Retry-After` only when the response sends it, since Mailtrap's docs do not describe that header.
- Test with recorded responses that have missing and extra fields. Stop sending to any address that bounced or complained, and check that those events reach your app.
- Meet every check in the [shared quality bar](../../references/checklists/engineering-quality-bar.md).

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
