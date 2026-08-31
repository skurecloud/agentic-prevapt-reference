# Methodology Mapping to the Manuscript

| Manuscript concept | Code |
|---|---|
| SKG: G=(V,E,lambda,rho) | `graph.py` |
| Step exploitability | `RiskModel.step_probability()` |
| Conditional path probability | `RiskModel.path_probability()` |
| Business impact | `RiskModel.impact()` |
| Path prioritization score | `RiskModel.path_score()` |
| Normalized prioritization score | `RiskModel.normalize()` |
| Bayesian evidence update | `bayes.py` |
| Optional overlap correction with explicit joint inputs | `overlap.py`, `AssessmentEngine.assess()` |
| End-to-end scoring | `engine.py` |
| Reproducible scenario I/O | `io.py`, `cli.py` |

## Scope boundary

The reference implementation is deliberately non-exploitative. It does not perform penetration testing, credential abuse, SSRF exploitation, or cloud compromise. Scenario files describe abstract attack steps and model inputs only.

## Coefficient interpretation

Default coefficients are heuristic priors:

- wE = 0.4
- wR = 0.3
- wC = 0.2
- wD = 0.1

They should be calibrated before probabilities are interpreted as empirically meaningful.

## Conditional path model

The logistic model produces the first-step marginal estimate `P(s_1)`. Every
later step must provide `conditional_probability = P(s_j | s_(j-1))`. The
engine rejects a multi-step path when a later conditional is missing; it does
not silently substitute an unconditional step score.

## Score interpretation

Impact inputs are normalized on a 0-10 organizational prioritization scale.
Consequently, `P(A_i) * I(A_i)` and its normalized system-level transform are
dimensionless prioritization scores. They are not expected monetary loss,
incident frequency, or breach probability.

## System aggregation

Paths are ordered by path score, with optional `top_k` truncation. When explicit
pairwise joint probabilities are supplied, the engine uses the second-order
approximation

```text
S = sum_i P(A_i) I(A_i)
    - sum_(i<j) P(A_i intersect A_j) min(I(A_i), I(A_j)).
```

The smaller-impact rule prevents the shared term from exceeding either path's
impact. Higher-order intersections are omitted, so this is an approximation.
When joint inputs are absent, the engine reports an additive score and labels
the aggregation method accordingly; it does not claim overlap correction.

## CVSS treatment

The reference implementation accepts a normalized exploitability-related feature in `[0,1]`. It does not treat the CVSS Base Score as an exploitability probability.
