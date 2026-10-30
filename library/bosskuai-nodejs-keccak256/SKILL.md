---
name: bosskuai-nodejs-keccak256
description: "Use when the task explicitly concerns nodejs keccak256. Prevent Ethereum hashing bugs in JavaScript and TypeScript. Node's sha3-256 is NIST SHA3, not Ethereum Keccak-256, and silently breaks selectors, signatures, storage slots, and address derivation. Use when hashing for Ethereum in JavaScript or TypeScript, or when a selector, signature, storage slot, or derived address is wrong."
metadata:
  origin: ECC-adaptation
---

# Node.js Keccak-256 — portable workflow

Prevent Ethereum hashing bugs in JavaScript and TypeScript. Node's sha3-256 is NIST SHA3, not Ethereum Keccak-256, and silently breaks selectors, signatures, storage slots, and address derivation. Use when hashing for Ethereum in JavaScript or TypeScript, or when a selector, signature, storage slot, or derived address is wrong.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. ethers v6.
3. viem.
4. web3.js.
5. Common patterns.
6. Address from public key.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the Node.js version (`node -v`, `.nvmrc` or `engines`) and the hashing library in the lockfile (ethers, viem or web3.js), each against its latest stable release, checked live at work time, and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service. If the lockfile pins another major version, use that version's API docs, not the v6 examples.

## Done when

Apply the source “How It Works” guidance and the library section that matches the lockfile pin (ethers, viem or web3.js) to the concrete request, using only that version's API. Return the resulting node.js keccak-256 artifact or diagnosis with source/command evidence for each conclusion.

- Test the helper first against known values. Keccak-256 of an empty input is `c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470`, and the `transfer(address,uint256)` selector is `0xa9059cbb`.
- Use canonical signatures (`uint256`, not `uint`, and no spaces). Check whether a helper reads a hex-looking string such as `0x1234` as bytes or as text.
- Derive an address from the 64-byte public key without the `0x04` prefix, and compare it with a known key and address pair.
- Meet every check in the [shared quality bar](../../references/checklists/engineering-quality-bar.md).

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
