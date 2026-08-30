# Reproducibility Protocol

## Current artifact status

This repository reproduces the paper's equations and provides transparent synthetic scenarios.

It does **not yet reproduce the reported inferential statistics**, because the manuscript source does not specify:

- the randomized variables used in the 10 runs per scenario;
- their probability distributions;
- raw per-run observations;
- exact random seeds;
- expert-review adjudication data.

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

Do not publish identifying reviewer information without consent.
