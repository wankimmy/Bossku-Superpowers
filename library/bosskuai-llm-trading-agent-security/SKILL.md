---
name: bosskuai-llm-trading-agent-security
description: "Use when the task explicitly concerns llm trading agent security. Security patterns for autonomous trading agents with wallet or transaction authority. Covers prompt injection, spend limits, pre-send simulation, circuit breakers, MEV protection, and key handling. Use when an autonomous agent holds wallet or transaction authority and its limits, simulation, or key handling need review."
metadata:
  origin: ECC-adaptation
---

# LLM Trading Agent Security — portable workflow

Security patterns for autonomous trading agents with wallet or transaction authority. Covers prompt injection, spend limits, pre-send simulation, circuit breakers, MEV protection, and key handling. Use when an autonomous agent holds wallet or transaction authority and its limits, simulation, or key handling need review.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-cybersecurity-risk`, `error-handling`, `bosskuai-agent-architecture-audit`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. Treat prompt injection as a financial attack.
3. Hard spend limits.
4. Simulate before sending.
5. Circuit breaker.
6. Wallet isolation.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the wallet, exchange and chain SDK versions in the lockfile, and the LLM SDK version, each against its latest stable release, checked live at work time, and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- Research and review do not authorise signing, trading, booking, purchase or wallet access. Keep any transaction behind an exact operation scope and the user's approval, and never copy or expose private keys.

## Done when

Complete the source “Pre-Deploy Checklist” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

- Give the agent only the permissions and funds it needs: no withdrawal rights on an exchange key, and a hard spend cap enforced in code, not in the prompt. Keys never appear in prompts, logs or evidence bundles.
- Simulate each transaction on a fork or with a simulation call, and compare the simulated amount with the cap. Reserve that amount against the cap in one atomic step before you send, using a row lock or a conditional update (for example, update the spend row only when spent plus the amount is at most the cap, and send only if one row changed). Release the reservation only when the send is confirmed to have failed; a timeout or unknown result keeps it reserved, because the transaction may still land. A failed or missing simulation, or a failed reservation, stops the send.
- Test prompt injection with crafted market text, news and token names on a testnet or paper account, and check that no tool call goes outside its allowlist.
- Meet every check in the [shared quality bar](../../references/checklists/engineering-quality-bar.md).

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
