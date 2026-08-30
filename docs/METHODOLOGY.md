# Methodology Mapping to the Manuscript

| Manuscript concept | Code |
|---|---|
| SKG: G=(V,E,lambda,rho) | `graph.py` |
| Step exploitability | `RiskModel.step_probability()` |
| Conditional path probability | `RiskModel.path_probability()` |
| Business impact | `RiskModel.impact()` |
| Path expected loss | `RiskModel.path_risk()` |
| Normalized prioritization score | `RiskModel.normalize()` |
| Bayesian evidence update | `bayes.py` |
| Overlap correction | `overlap.py` |
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

## CVSS treatment

The reference implementation accepts a normalized exploitability-related feature in `[0,1]`. It does not treat the CVSS Base Score as an exploitability probability.
