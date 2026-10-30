---
name: bosskuai-gis-geoai-ml-engineer
description: "Use when building models that extract buildings, roads, vehicles or land cover from satellite or aerial imagery: tiling, training, per-class evaluation, ONNX export, and GIS integration of the output."
---

# BosskuAI GIS GeoAI/ML Engineer

Use this skill to take a feature-extraction or land-cover task from imagery assessment to a deployed inference pipeline whose output lands in GIS layers.

## How this differs from nearby skills

- **`bosskuai-pytorch-patterns`**: general PyTorch training and data loading. This skill adds geospatial tiling, geography-aware validation and raster-to-vector output.
- **`bosskuai-mle-workflow`**: generic ML delivery (data contracts, monitoring, rollback). Use it alongside this one for the production loop.
- **`bosskuai-gis-technical-consultant`**: strategy, platform choice and roadmaps rather than building a model.
- **`bosskuai-eval-driven-agent-improvement`**: evals for LLM agents, not image models.

## Workflow

1. Define what is extracted and at what accuracy. Assess the imagery: resolution, bands, coverage, recency, licensing.
2. Check for existing labelled datasets and pre-trained models before training a custom one. Confirm their licences and coverage.
3. Prepare data: tile (start with moderately sized tiles with overlap and tune), augment, and split train, validation and test by geography, not randomly, to avoid leakage between neighbouring tiles.
4. Pick the architecture for the task: segmentation, detection, or a promptable foundation model for few-shot work. Check the installed library versions.
5. Train with experiment tracking. Evaluate IoU, F1, precision and recall per class, with a confusion matrix and a map of where errors fall.
6. Test on geography the model has not seen: a model trained on one region may fail on another. Spot-check predictions visually.
7. Document failure modes: cloud cover, shadows, seasonal change, unusual roof colours, sensor changes.
8. Export for deployment (for example ONNX), then build tile, predict, merge, simplify. Post-process: remove slivers, smooth boundaries, apply minimum-area thresholds.
9. Integrate with GIS: vectorise, attribute and publish. Monitor drift over time and place.

## Guardrails

- A single accuracy number is not evidence. Report per-class metrics and spatial error distribution.
- Respect imagery and dataset licences, and privacy rules for imagery of people or property.
- Use the neighbouring skills for simple overlay or statistical spatial work; do not train a model where a buffer or join will do.

## Output format

```text
Task and target quality: [feature, metric, threshold]
Data: [imagery, labels, split by geography]
Model: [architecture, weights source, version]
Results: [per-class metrics, unseen-region result]
Failure modes: [conditions, examples]
Deployment: [export format, pipeline, GIS output, monitoring]
```

The shared quality bar: `../../references/checklists/engineering-quality-bar.md`.

Adapted from agency-agents/gis/gis-geoai-ml-engineer.md (agency-agents, MIT).
