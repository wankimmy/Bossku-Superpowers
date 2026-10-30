---
name: bosskuai-solidity
description: "Use when writing, testing, or reviewing Solidity contracts: checks-effects-interactions, access control, upgradeable proxies, gas patterns, Foundry unit, fuzz, and invariant tests, and audit-ready deployment checklists."
---

# BosskuAI Solidity Engineering

Use this skill to build EVM contracts that hold value. Assume a determined adversary reads the source. Contracts are hard to change after deployment, so review and tests come before any live transaction.

## How this differs from nearby skills

- **`bosskuai-defi-amm-security`**: security checklist for AMM and swap contracts (donation attacks, oracle use). This skill covers general contract design, testing, and deployment; run that one too for AMM code.
- **`bosskuai-llm-trading-agent-security`**: wallet and key risks in AI trading agents.
- **`bosskuai-cybersecurity-risk`**: general threat modelling beyond contracts.
- **`bosskuai-tdd-loop`**: the same red-green habit applies to Foundry tests.

## Workflow

1. Threat model: who holds authority (admin keys, roles), what can be upgraded, which external contracts and oracles are trusted, and what invariants must always hold (for example total deposits equal the sum of user balances). Map flash-loan, price-manipulation, governance, and frontrunning risks.
2. Design: define interfaces and events first. Pick the upgrade approach (none, transparent proxy, UUPS, beacon) with its trade-offs; plan storage layout so slots are never reordered or removed across versions. Compare the layout before and after each upgrade with `forge inspect <Contract> storage-layout`.
3. Implement with audited base libraries such as OpenZeppelin (check the installed major version, because APIs change between versions). Follow checks-effects-interactions, use reentrancy guards where external calls exist, prefer pull over push payments, and avoid `tx.origin` for authorisation. Never change a non-zero token allowance straight to another non-zero value (the ERC-20 approve race).
4. Safety features: role-based access, pause or circuit breaker, timelock on privileged changes, and events for every state change. Avoid unbounded loops over user-growable arrays.
5. Gas: minimise storage reads and writes, pack structs deliberately, use calldata for read-only arguments, immutable or constant for fixed values, and custom errors. Measure with gas snapshots rather than guessing, and do not hand-optimise what the compiler already does.
6. Tests with Foundry or equivalent: unit tests for every branch, fuzz tests for arithmetic and state transitions, invariant tests across random call sequences, upgrade tests that preserve state, and fork tests against real chain state where integrations exist. Rehearse each upgrade on a fork of the live chain (`forge script` with `--fork-url`) and compare balances and totals before and after with the numbers you expect.
7. Static analysis (for example Slither): fix each finding or write down why it is a false positive.
8. Audit preparation: architecture notes, trust assumptions, known risks, a deployment checklist (constructor args, proxy admin, role grants, timelocks), and a testnet rehearsal. Keep off-chain readers (indexers, front ends) working with both the old and the new ABI until the switch is done.

## Guardrails

- Contracts handle money. This skill organises engineering work; it is not a security guarantee, audit, or legal or financial advice. Get an independent professional audit before mainnet and a qualified review of regulatory exposure.
- Never deploy, sign, send, or fund anything on a real network, and never handle private keys or seed phrases, without the user's explicit approval. Use testnets and local forks by default.
- Chain behaviour (timestamps, gas, precompiles, opcodes) and compiler versions differ; check the target chain's and compiler's current documentation.
- Treat all external contracts and token behaviours (fees, callbacks, odd return values) as untrusted.
- Versions: read the pinned compiler from the `solidity` setting in `hardhat.config.*` or the `solc` key in `foundry.toml` (a strict version, not a range). A `pragma solidity` line such as `^0.8.20` is only a version range and does not name the compiler. If nothing is pinned, say so and do not guess a version. Confirm it in the build files, not the tool version: for Hardhat, `solcVersion` in `artifacts/build-info/*.json` after a compile; for Foundry, an exact `solc` set in `foundry.toml` (`forge --version` shows only the Foundry release). Check the latest stable release at soliditylang.org at work time, and use only APIs present in the installed version. Check that the target chain supports the EVM version the build targets.
- Token amounts are integers in the token's smallest unit. Tokens do not all use 18 decimals, so read `decimals()` from the token, multiply before you divide (integer division rounds down), and test with production decimals.
- Full quality bar: `../../references/checklists/engineering-quality-bar.md`.

## Output format

```text
Contract scope and trust assumptions: [..]
Invariants: [list]
Design choices: [upgrade pattern, roles, pause]
Findings or changes: [issue, severity, fix]
Test summary: [unit, fuzz, invariant, upgrade, fork; command and result]
Analysis tool results and open items: [..]
Deployment checklist status: [..]
```

Adapted from agency-agents/engineering/engineering-solidity-smart-contract-engineer.md (agency-agents, MIT).
