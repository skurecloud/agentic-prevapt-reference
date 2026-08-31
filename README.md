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
- reproducible scenario execution with deterministic seeds

## Important reproducibility note

The paper reports aggregate before/after values for three AWS scenarios. The original manuscript does **not** provide the raw per-run observations, exact randomized variables, or sampling distributions required to independently reproduce its reported p-values/confidence intervals.

Accordingly:

- `data/paper_reported_results.csv` preserves the values reported in the manuscript.
- `examples/` contains transparent, synthetic reference scenarios that exercise the equations.
- this repository does **not** claim to regenerate the paper's statistical significance results until the raw experiment protocol/data are added.

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

P(s_1) = sigmoid(b + wE*E + wR*R + wC*C + wD*D)

For j > 1, P(s_j | s_(j-1)) must be supplied explicitly.

I(A_i) = alpha*Ds + beta*Br + gamma*Oi

R_norm = 100 * (1 - exp(-R_system / tau))
```

Bayesian evidence update:

```text
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

The corrected paper value for mean scenario-specific modeled-score reduction is
79.7%, reported as 80%.  This is the arithmetic mean of the three unrounded
scenario reductions, not a breach-probability estimate and not a value computed
from the rounded mean scores.

## Repository layout

```text
src/agentic_prevapt/
  graph.py       Security Knowledge Graph
  risk.py        scoring equations
  bayes.py       Bayesian update
  overlap.py     overlap-aware aggregation
  engine.py      end-to-end assessment
  cli.py         command-line runner

examples/
  scenario_simple.json
  scenario_microservices.json
  scenario_enterprise.json

data/
  paper_reported_results.csv

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
