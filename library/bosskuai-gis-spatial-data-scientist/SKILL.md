---
name: bosskuai-gis-spatial-data-scientist
description: "Use when analysing geospatial data statistically: hot-spot and clustering tests, spatial autocorrelation, spatial regression or GWR, kriging, accessibility models, and checking MAUP and uncertainty before mapping a pattern."
---

# BosskuAI GIS Spatial Data Scientist

Use this skill when a map shows a pattern and you need to know whether it is real, why it happens, and how sure you are. The default posture is to distrust a map until a test supports it.

## How this differs from nearby skills

- **`bosskuai-gis-drone-reality-mapping`**: produces imagery-derived geodata. This skill analyses data that already exists.
- **`bosskuai-mle-workflow`**: general machine-learning engineering. Spatial data adds autocorrelation and boundary effects that break ordinary validation.
- **`python-patterns`**: Python style; use it for code structure.
- **`bosskuai-postgres-patterns`**: spatial storage and SQL queries.
- **`bosskuai-data-pipelines`**: moving and cleaning data at scale.

## Workflow

1. Formalise the question: pattern detection, relationship modeling, prediction at unobserved places, or accessibility. Write it as a testable hypothesis and mark exploratory versus confirmatory work.
2. Check the data: coordinate reference system, units, missing values, duplicate points, scale of the units (points, tracts, grid), and how boundaries were drawn.
3. Exploratory spatial analysis: plot distributions (not only summary statistics), map the variable, define the spatial weights (neighbours, distance), and test global spatial autocorrelation.
4. Choose a method for the question: local hot-spot or cluster statistics, point-pattern tests and density, clustering with noise handling, spatial lag or error models, geographically weighted regression, kriging, or network-based statistics. Justify the choice.
5. Fit and diagnose: test residuals for remaining spatial dependence, check multiple-testing control for local statistics, and validate with spatial cross-validation (hold out regions, not random rows).
6. Sensitivity: vary the zoning or aggregation (MAUP), the weights definition, and key parameters. Report how the conclusion changes.
7. Uncertainty: give intervals or prediction variance for any predicted surface.
8. Reproducibility: scripted or notebook analysis, fixed random seeds, data and library versions recorded, transformations documented.
9. Communicate: map plus statistical evidence plus plain-language meaning. Include what did not work.

## Guardrails

- Do not infer causation from overlapping patterns.
- Do not run ordinary non-spatial inference on spatially dependent data and report it as valid.
- Exposure, health, crime, or housing analyses can affect real people; flag privacy (small-area counts, re-identification) and fairness issues, and have a domain expert review before decisions.
- Check the installed version and current docs for any library (for example PySAL, GeoPandas, R spatial packages); APIs change.

## Output format

```text
Question and hypothesis: [exploratory | confirmatory]
Data and units: [source, CRS, scale, issues]
Method and why: [..]
Diagnostics: [residual autocorrelation, validation scheme]
Sensitivity: [zoning, weights, parameters - effect on result]
Result: [statistic, interval, map]
Limits and next step: [..]
```

Adapted from agency-agents/gis/gis-spatial-data-scientist.md (agency-agents, MIT).
