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
| Bounded path enumeration | `enumeration.py` |
| Ranking comparison | `ranking.py`, `experiments/ranking_comparison.py` |

## Scope boundary

The reference implementation is deliberately non-exploitative. It does not perform penetration testing, credential abuse, SSRF exploitation, or cloud compromise. Scenario files describe abstract attack steps and model inputs only.

## Coefficient interpretation

Version 0.3 uses an explicitly heuristic mapping:

- intercept = -4.0
- exploitability = +3.0
- privilege/precondition ease = +1.5
- attack ease = +1.0
- detection difficulty = +0.5

All inputs lie in `[0,1]` and increase with ease of exploitation. In particular,
`attack_ease=1` means low complexity for the attacker. The achievable first-step
range is `sigmoid(-4)=0.018` to `sigmoid(2)=0.881`. These coefficients are not
fitted and must be calibrated before probabilities are interpreted empirically.

## Conditional path model

The logistic model produces the first-step marginal estimate `P(s_1)`. Every
later step must provide `conditional_probability = P(s_j | s_(j-1))`. The
engine rejects a multi-step path when a later conditional is missing; it does
not silently substitute an unconditional step score.

## Candidate-path enumeration

`enumerate_candidate_paths()` performs deterministic bounded depth-first search
from declared exposure nodes to declared business-asset nodes. It rejects
cycles, applies an edge-feasibility predicate, prunes at `max_depth`, orders
results by length and lexical identity, and returns at most `top_k`. Worst-case
time is `O(b^d)` for branching factor `b` and depth bound `d`.

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
The implementation clamps the heuristic at zero. The expression is not derived
as expected loss and is treated as a second-order penalty diagnostic.

## CVSS treatment

The reference implementation accepts a normalized exploitability-related feature in `[0,1]`. It does not treat the CVSS Base Score as an exploitability probability.
