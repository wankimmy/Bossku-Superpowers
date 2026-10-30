---
name: bosskuai-contract-first
description: "Use when the task explicitly concerns contract first. Coordinate frontend/backend or service-to-service work through one authoritative machine-checkable contract (OpenAPI, AsyncAPI, Protocol Buffers, or JSON Schema), with generated consumer types and contract-verified integration. Use when parallel consumer and provider work must evolve an API or event schema without field drift, mock/production shape mismatch, or one side silently redefining the interface."
metadata:
  origin: ECC-adaptation
---

# Contract-First Collaboration — portable workflow

Coordinate frontend/backend or service-to-service work through one authoritative machine-checkable contract (OpenAPI, AsyncAPI, Protocol Buffers, or JSON Schema), with generated consumer types and contract-verified integration. Use when parallel consumer and provider work must evolve an API or event schema without field drift, mock/production shape mismatch, or one side silently redefining the interface.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-subagent-delegation`, `bosskuai-quarkus-patterns`, `bosskuai-rapid-prototype`, `bosskuai-api-design`, `bosskuai-qa-automation-strategy`, `bosskuai-react-development`, `bosskuai-software-architecture`, `bosskuai-tdd-loop`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. The Boundary Artifact.
2. Consumer-First Workflow.
3. 1. Identify Consumers and Owners.
4. 2. Describe Consumer Jobs.
5. 3. Define the Smallest Useful Contract.
6. openapi.yaml.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: read the contract's own version line (`openapi:` in `openapi.yaml`, `asyncapi:` in an AsyncAPI file, or a versioned `package` name, such as `package acme.v1;`, in a `.proto` file), and the generator and validator versions in the lockfile. Check the latest stable spec and tool releases at openapis.org, asyncapi.com or protobuf.dev at work time, and use only APIs present in the installed version. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

The authoritative contract exists, consumers use matching generated/derived types, and a provider verification demonstrates actual responses match the contract.

- Type traps: check the contract against recorded production responses, not only the spec. Look at integers vs numbers, 64-bit IDs sent as strings, nullable vs missing fields, and money as a decimal string.
- Concurrency: a provider and a consumer that release in the same window can disagree. Pin the contract version each side builds against. Release an added field on the provider first only when every consumer is known to ignore unknown fields (check strict decoders, protobuf JSON parsers and schemas that set additionalProperties to false). If a consumer is strict, release that consumer's support for the field first.
- Zero downtime: make schema changes additive (new optional fields, new endpoints) while old clients run, and run a breaking-change check on every change (for example `buf breaking` for `.proto` files).
- Full quality bar: `../../references/checklists/engineering-quality-bar.md`.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
