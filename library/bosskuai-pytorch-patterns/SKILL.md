---
name: bosskuai-pytorch-patterns
description: "Use when the task explicitly concerns pytorch patterns. PyTorch deep learning patterns and best practices for building robust, efficient, and reproducible training pipelines, model architectures, and data loading. Use when writing or reviewing PyTorch training loops, model architectures, or data loading, or when a run will not reproduce."
metadata:
  origin: ECC-adaptation
---

# PyTorch Development Patterns — portable workflow

PyTorch deep learning patterns and best practices for building robust, efficient, and reproducible training pipelines, model architectures, and data loading. Use when writing or reviewing PyTorch training loops, model architectures, or data loading, or when a run will not reproduce.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-go-development`, `bosskuai-kotlin-patterns`, `python-patterns`, `bosskuai-performance-profiling`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Core Principles.
2. 1. Device-Agnostic Code.
3. Good: Device-agnostic.
4. Bad: Hardcoded device.
5. 2. Reproducibility First.
6. Good: Full reproducibility setup.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions first: `python --version`, the PyTorch version in the lockfile or `requirements*.txt`, and the installed build with `python -c "import torch; print(torch.__version__, torch.version.cuda)"`. Check the latest stable PyTorch release at work time on pytorch.org, and use only APIs that exist in the installed version. Also check the source prerequisites. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Apply the source “Core Principles”, “1. Device-Agnostic Code” guidance to the concrete request. Return the resulting pytorch development patterns artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Also check before you finish:

- The input dtype and scale match production. uint8 images from 0 to 255 are not float images from 0 to 1.
- The run uses the same dtype and device.
- `torch.load` uses `weights_only=True` for any checkpoint you did not make. A pickled file can run code.
- Inference runs under `model.eval()` and `torch.inference_mode()`.
- A resumed run restores the optimizer and RNG state, not only the weights.

The full quality bar is in `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
