---
name: bosskuai-evm-token-decimals
description: "Use when the task explicitly concerns evm token decimals. Prevent silent decimal mismatch bugs across EVM chains. Covers runtime decimal lookup, chain-aware caching, bridged-token precision drift, and safe normalization for bots, dashboards, and DeFi tools. Use when handling token amounts across EVM chains, or when a balance, price, or transfer amount is off by orders of magnitude."
metadata:
  origin: ECC-adaptation
---

# EVM Token Decimals — portable workflow

Prevent silent decimal mismatch bugs across EVM chains. Covers runtime decimal lookup, chain-aware caching, bridged-token precision drift, and safe normalization for bots, dashboards, and DeFi tools. Use when handling token amounts across EVM chains, or when a balance, price, or transfer amount is off by orders of magnitude.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-cost-optimization`, `error-handling`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. Query decimals at runtime.
3. Cache by chain and token.
4. Handle odd tokens defensively.
5. Normalize to 18-decimal WAD in Solidity.
6. TypeScript with ethers.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the EVM client library in the lockfile (ethers, viem or web3.js) and the Solidity compiler version in `foundry.toml` or the Hardhat config. Compare each with its latest stable release, looked up live at work time and never from memory. Check the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- Research and review do not authorise signing, trading, booking, purchase or wallet access. Keep any transaction behind an exact operation scope and the user's approval, and never copy or expose private keys.

## Done when

Apply the source “How It Works”, “Query decimals at runtime” guidance to the concrete request. Return the resulting evm token decimals artifact or diagnosis with source/command evidence for each conclusion.

- Read `decimals()` on-chain for each token on each chain, and cache by chain ID and token address. Never copy decimals from a symbol: USDT has 6 decimals on Ethereum and 18 on BNB Chain.
- If `decimals()` reverts, or returns anything other than a whole number from 0 to 255, stop with an error. This overrides the source's 18-decimal fallback in 'Handle odd tokens defensively', even when the fallback is logged.
- Do amount math in integers: BigInt, or the `parseUnits` and `formatUnits` helpers of ethers or viem. Test with string amounts such as "0.01" and with values above 2^53, the types production sends.
- Meet every check in the [shared quality bar](../../references/checklists/engineering-quality-bar.md).

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
