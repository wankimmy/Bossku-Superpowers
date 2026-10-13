---
name: bosskuai-wechat-mini-programs
description: "Use when building a WeChat Mini Program: project structure, request wrapper and login, server-side WeChat Pay flow, subscription messages, setData and package-size performance, domain whitelist, privacy, and review readiness."
---

# BosskuAI WeChat Mini Programs

Use this skill to build and review Mini Programs (小程序) that run inside WeChat. They use a dual-thread model, a platform review process, and strict network and privacy rules.

## How this differs from nearby skills

- **`bosskuai-private-domain-operator`**: WeCom community and CRM operations. This skill is the Mini Program code and release path.
- **`bosskuai-china-ecommerce-operator`**: marketplace stores and campaigns, not app code.
- **`bosskuai-china-market-localization-strategist`**: go-to-market strategy for China.
- **`bosskuai-saas-billing-ops`**: generic subscription billing; WeChat Pay specifics are here.
- **`bosskuai-tdd-loop`**: test-first loop for the plain JavaScript logic you extract.

## Workflow

1. Configuration: define pages, tab bar, window, and permission declarations. Plan the main package and subpackages by user journey priority.
2. Network: every API, socket, upload, and download domain must be registered in the Mini Program console, and requests must use HTTPS with a valid certificate. Keep dev, staging, and production environments separate.
3. Request layer: wrap callback-based `wx` APIs in promises; centralise auth headers, token refresh, and error handling. Handle error bodies that are empty, plain text, or gateway HTML without leaving a promise pending.
4. Login: obtain the temporary code on the client, exchange it on your server, and keep session secrets on the server. Never ship app secrets or merchant keys in the package.
5. Payments: create the order on the server, return the signed parameters, and invoke the payment API on the client. Confirm payment status from the server-side notification, not from the client success callback. Distinguish a user cancel from a failure. Check the current WeChat Pay docs for signing and refund requirements.
6. Subscription messages: request authorisation at a moment that has user value (for example after an order), and handle accept, reject, and ban results.
7. Performance: reduce `setData` frequency and payload (send only changed fields), defer non-critical start-up work, lazy-load images, use virtual lists for long lists, and check package size against the current platform limits.
8. Privacy and content: follow current WeChat privacy-API rules, ask authorisation before sensitive data, show a visible reason for permissions, and use content-security APIs for user-generated content where required. Consider China's Personal Information Protection Law and have counsel review.
9. Test on real iOS and Android devices and different base library versions, then prepare review materials and the common rejection causes (permission without visible use, missing policy, content problems).

## Guardrails

- Platform limits, API names, review policy, and base library behaviour change often. Check the current official WeChat documentation and developer tools before relying on any number or API here.
- Never expose merchant keys, signing keys, or user tokens in client code or logs.
- Do not submit for review, publish a version, issue refunds, or call live payment APIs without the owner's explicit approval; use the sandbox where available.
- Treat performance targets as measurements from your own devices.

## Output format

```text
Structure: [pages, subpackages, size per package]
Domains to register: [list]
Auth and payment flow: [client step, server step, verification]
setData and loading findings: [..]
Privacy and permission review: [..]
Device test matrix and result: [..]
Review risks: [..]
```

Adapted from agency-agents/engineering/engineering-wechat-mini-program-developer.md (agency-agents, MIT).
