---
name: bosskuai-feishu-integration
description: "Use when building on the Feishu (Lark) Open Platform: bots, interactive message cards, event subscriptions, approval workflows, Bitable sync and OAuth login, with token caching, signature checks and idempotent handlers."
---

# BosskuAI Feishu / Lark Integration

Use this skill to design and review integrations with the Feishu Open Platform (Lark internationally): bots, cards, approvals, Bitable and SSO.

## How this differs from nearby skills

- **`bosskuai-contract-first`**: authoritative API contracts between your own services. Here the contract belongs to Feishu; check its docs.
- **`bosskuai-integration-testing`**: how to test integrations. Use it for the test plan; this skill covers the Feishu specifics.
- **`bosskuai-mailtrap-email-integration`**: email delivery, a different channel.
- **`bosskuai-laravel-security`**: framework hardening; this skill covers webhook and token handling for Feishu.

## Workflow

1. Map the business scenarios and pick the capabilities needed (bot, cards, approval, Bitable, SSO). Choose app type (self-built enterprise app or ISV app).
2. List required permission scopes and request the minimum. Some scopes need admin approval in the admin console.
3. Auth: know when an endpoint needs a tenant access token versus a user access token. Prefer the official SDK for your language, which handles token caching; if you cache manually, expire early and never fetch per request.
4. Secrets: app secret, encrypt key and verification token live in environment variables or a secrets manager, never in source or frontend code.
5. Events: expose an HTTPS endpoint, verify the verification token or decrypt with the encrypt key, return quickly, and process asynchronously. Feishu retries on slow responses, so handlers must be idempotent (dedupe by event id).
6. Cards: build and preview in the Card Builder or validate JSON locally before sending. Handle card action callbacks; update sent cards by message id.
7. Approvals: create instances, subscribe to status events, drive downstream actions only from verified events.
8. Bitable and sync: respect per-request record limits and rate limits, batch writes, add backoff on HTTP 429 and transient errors, and check the `code` field on every response.
9. SSO: authorization code flow with a random `state` bound to the session and consumed once; verify it on callback before exchanging the code.
10. Test duplicate, out-of-order and delayed events; remove unused scopes; add alerts for token failures and API errors.

## Guardrails

- Check the current official Feishu/Lark docs and SDK version for endpoints, limits and event names before coding.
- Never call Feishu APIs with the app secret from a browser; proxy through your backend after authenticating the user.
- Do not send messages or approvals to real users or groups during testing without explicit user approval.
- Return friendly errors to users on API failure instead of failing silently.

## Output format

```text
Scenario: [bot / card / approval / bitable / sso]
Scopes and tokens: [scopes, token type]
Security: [verification, secrets, state]
Handler design: [sync response, async work, idempotency key]
Failure handling: [retry, backoff, alerts]
Tests: [duplicate, ordering, rate limit]
```

Adapted from agency-agents/engineering/engineering-feishu-integration-developer.md (agency-agents, MIT).
