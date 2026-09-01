# Reproducibility Protocol

## Current artifact status

This repository reproduces the paper's equations and provides transparent synthetic scenarios.

It does **not yet reproduce the reported inferential statistics**, because the manuscript source does not specify:

- the randomized variables used in the 10 runs per scenario;
- their probability distributions;
- raw per-run observations;
- exact random seeds;
- expert-review adjudication data.

The revised manuscript treats the old before/after values as legacy provenance,
not as a result. It does not report the unauditable expert-review percentages,
a p-value, or a confidence interval.

## Ranking comparison

`experiments/generate_synthetic_dataset.py` deterministically creates 30 paths
in three equal path-length strata. `data/synthetic_paths_30.json` records every
input. `experiments/ranking_comparison.py` generates the result CSV and reports
unadjusted, within-length, and length-normalized Kendall comparisons with
p-values. Because all paths and CVSS v3.1-style values are synthetic, the
comparison diagnoses model behavior rather than operational effectiveness.

The fixed design intentionally couples CVSS to path length and reuses ten
profiles across three length strata; it is a constructed Simpson's-paradox
illustration, not evidence about real architectures.

## Randomized replication

`experiments/randomized_replication.py` runs 1,000 deterministic seeded
replications. Each run generates 30 independent paths, balanced across lengths
2, 3, and 4. Features, impact components, conditional probabilities, and CVSS
are sampled independently; CVSS is Uniform(4, 9) without reference to length.
The committed outputs report pooled and within-length tau-b distributions,
95% simulation intervals, and pooled/stratified sign disagreement.

## Required experiment record

Every experiment should write one record containing:

```json
{
  "scenario_id": "...",
  "git_commit": "...",
  "seed": 0,
  "model_parameters": {},
  "input_artifact_hashes": {},
  "attack_paths": [],
  "baseline": {},
  "remediated": {},
  "agent_model": {
    "provider": "...",
    "model": "...",
    "temperature": 0
  }
}
```

## Statistical reporting

Before reintroducing the paper's `p < 0.001` claim:

1. publish all per-run baseline and remediated values;
2. justify why runs are statistically independent;
3. state the randomization mechanism;
4. verify assumptions for a paired t-test;
5. consider a non-parametric paired test when assumptions are not satisfied;
6. report effect sizes in addition to p-values;
7. define how confidence intervals were calculated.

## Manual expert review

Record:

- reviewer experience band;
- whether assessment was independent;
- whether reviewers were blinded to agent outputs;
- matching criteria for findings;
- adjudication procedure;
- handling of partially overlapping attack paths.

Also publish the total framework findings, total expert findings, matched
findings, false positives, false negatives, and the precise denominator for
each reported rate. Until these counts and rules are available, the 94%, 6%,
and 8% figures are not independently auditable.

Do not publish identifying reviewer information without consent.
