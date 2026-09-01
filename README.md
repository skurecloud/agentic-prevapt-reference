# Agentic Pre-VAPT Reference Implementation

Reference implementation accompanying the manuscript:

**Agentic AI for Pre-VAPT: Probabilistic Attack-Path Risk Scoring with Cloud-Native Validation**

This repository implements the mathematical core described in the paper:

- Security Knowledge Graph (SKG) representation
- step-level exploitability scoring
- conditional multi-step attack-path probability
- normalized contextual-impact scoring
- normalized system-risk scoring
- Bayesian evidence updates
- optional overlap-aware path-score aggregation with explicit joint-probability inputs
- bounded, deterministic candidate-path enumeration
- reproducible ranking comparison against CVSS-max and impact-only baselines

## Important reproducibility note

Earlier drafts reported aggregate before/after values for three AWS scenarios, but the original records do **not** provide the raw per-run observations, exact randomized variables, or sampling distributions required for independent inference. Version 0.3 does not use those aggregates as effectiveness evidence.

Accordingly:

- `data/paper_reported_results.csv` is retained only as a legacy provenance record.
- `examples/` contains transparent, synthetic reference scenarios that exercise the equations.
- `data/ranking_comparison.csv` is generated from those scenarios by `experiments/ranking_comparison.py`.
- this repository does **not** claim statistical effectiveness or regenerate unavailable experiments.

This separation is intentional and prevents synthetic data from being presented as observed experimental evidence.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -e .
python -m agentic_prevapt.cli examples/scenario_enterprise.json
pytest
```

## Mathematical model

For attack path \(A_i = \{s_1,\ldots,s_k\}\):

```text
R_i = P(A_i) * I(A_i)

P(A_i) = P(s_1) * product(P(s_j | s_(j-1)))

P(s_1) = sigmoid(-4 + 3E + 1.5R + 1A + 0.5D)

For j > 1, P(s_j | s_(j-1)) must be supplied explicitly.

I(A_i) = alpha*Ds + beta*Br + gamma*Oi

R_norm = 100 * (1 - exp(-R_system / tau))
```

Here `A` is attack ease, not attack complexity. All features increase with ease
of exploitation. The configured first-step range is approximately 0.018 to
0.881.

Bayesian evidence update:

```text
P(E) = P(E|A_i)P(A_i) + P(E|not A_i)P(not A_i)
P(A_i | E) = P(E | A_i) * P(A_i) / P(E)
```

The quantity `R_i` is a dimensionless prioritization score because impact is
normalized; it is not an actuarial expected loss or breach probability.

For two overlapping path events, exact joint probabilities may be supplied:

```text
P(A union B) = P(A) + P(B) - P(A intersect B)
```

For multiple paths, the engine optionally applies a documented second-order
pairwise correction.  Each joint term is weighted by the smaller of the two
path impacts.  Without explicit joints, the engine labels its result
`additive_without_overlap_correction`; it never infers joint probabilities from
shared graph nodes.

## Reproducible ranking comparison

```bash
PYTHONPATH=src python experiments/ranking_comparison.py
```

Across the six synthetic paths, Pre-VAPT score has Kendall tau-b = -0.60
against CVSS-max and -0.47 against impact-only ranking. This exposes a length
penalty in the multiplicative path model: longer paths can rank below shorter
paths even when their CVSS and impact are higher. The manuscript reports this
as a diagnostic limitation, not an effectiveness result.

## Repository layout

```text
src/agentic_prevapt/
  graph.py       Security Knowledge Graph
  risk.py        scoring equations
  bayes.py       Bayesian update
  overlap.py     overlap-aware aggregation
  enumeration.py bounded simple-path enumeration
  ranking.py     Kendall tau-b comparison
  engine.py      end-to-end assessment
  cli.py         command-line runner

examples/
  scenario_simple.json
  scenario_microservices.json
  scenario_enterprise.json

data/
  paper_reported_results.csv
  ranking_comparison.csv

experiments/
  ranking_comparison.py

docs/
  REPRODUCIBILITY.md
  METHODOLOGY.md
  SECURITY.md

tests/
  unit tests for equations and aggregation
```

## What should be added before citing this repository as a full artifact

1. Exact AWS/IaC artifacts for each evaluated architecture.
2. Exact attack paths used in each of the 10 runs per scenario.
3. Per-step features and conditional probabilities.
4. Exact randomized variables and sampling distributions.
5. Random seeds for each run.
6. Raw before/after observations used for t-tests and confidence intervals.
7. Manual reviewer protocol and adjudicated ground truth.
8. Model/provider/version identifiers for any LLM-based agents.

## License

Apache-2.0. See `LICENSE`.
