# Reproducibility Protocol

## Current artifact status

This repository reproduces the paper's equations and provides transparent synthetic scenarios.

It does **not yet reproduce the reported inferential statistics**, because the manuscript source does not specify:

- the randomized variables used in the 10 runs per scenario;
- their probability distributions;
- raw per-run observations;
- exact random seeds;
- expert-review adjudication data.

The revised manuscript therefore treats the three scenario results as
descriptive case-study outputs and the expert-review percentages as unverified
legacy aggregates. It does not report a p-value or confidence interval.

## Aggregate calculation

For the published rounded scenario scores, reductions are calculated per
scenario before aggregation:

```text
Simple Web App: (12.4 - 2.1) / 12.4 = 83.0645%
Microservices:  (24.8 - 6.3) / 24.8 = 74.5968%
Enterprise:     (17.1 - 3.2) / 17.1 = 81.2865%
Arithmetic mean                         = 79.6493% ~= 80%
```

The mean is not computed from the rounded average baseline and remediated
scores, and it must not be interpreted as reduced incident probability.

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
