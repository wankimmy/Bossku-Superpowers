---
name: bosskuai-defi-amm-security
description: "Use when the task explicitly concerns defi amm security. Security checklist for Solidity AMM contracts, liquidity pools, and swap flows. Covers reentrancy, CEI ordering, donation or inflation attacks, oracle manipulation, slippage, admin controls, and integer math. Use when auditing or writing Solidity AMM, liquidity pool, or swap code."
metadata:
  origin: ECC-adaptation
---

# DeFi AMM Security — portable workflow

Security checklist for Solidity AMM contracts, liquidity pools, and swap flows. Covers reentrancy, CEI ordering, donation or inflation attacks, oracle manipulation, slippage, admin controls, and integer math. Use when auditing or writing Solidity AMM, liquidity pool, or swap code.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-cybersecurity-risk`, `bosskuai-flutter-dart-code-review`, `bosskuai-healthcare-phi-compliance`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. Execution Safety.
3. Reentrancy: enforce CEI order.
4. Donation or inflation attacks.
5. Oracle manipulation.
6. Slippage protection.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the Solidity compiler version the contracts pin (`pragma`, `foundry.toml` or the Hardhat config), the OpenZeppelin Contracts version in the lockfile, and the compiler's known-bugs list for that version, all checked live at work time, and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- Research and review do not authorise signing, trading, booking, purchase or wallet access. Keep any transaction behind an exact operation scope and the user's approval, and never copy or expose private keys.

## Done when

Complete the source “Security Checklist” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

- Run swaps and liquidity changes on a fork of the target chain at a recent block (for example with `forge test --fork-url`), using real token decimals and balances.
- Take prices from a time-weighted or external oracle, and reject stale answers by checking `updatedAt`. Never price from one pool's reserves inside a transaction, since a flash loan can move them.
- Test fee-on-transfer tokens, first-deposit (inflation) attacks, and swaps with the user's minimum output and deadline.
- Meet every check in the [shared quality bar](../../references/checklists/engineering-quality-bar.md).

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
