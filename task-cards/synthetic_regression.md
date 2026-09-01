# Synthetic Regression Task Card

Status: draft

Task id: `synthetic_regression`

Evidence status: seed

Evidence reviewed: 2026-08-15

Grounding does not apply: this is a framework-test Task with a generated
target and no clinical referent, so there is no measurement to define, no
claim boundary to draw and no literature to cite. `seed` records that it was
assessed and found out of scope, which an absent field cannot.

## Target

Synthetic continuous regression target used for framework tests and examples.
It is not an HPP clinical target.

Implementation facts:

- target field: synthetic
- target dataset: synthetic
- target source: none
- primary metric: R2

## Why This Matters

This task exists to validate Task/Predictor/Strategy plumbing without requiring
private HPP data. It should make framework behavior testable and reproducible,
but it should not be used for scientific interpretation.

## Baselines And Ceilings

No clinical demographic floor applies. Baselines are synthetic-contract
baselines used by tests.

## Caveats

- No clinical, biological, or HPP cohort claim is supported.
- Results are only meaningful for framework regression testing.
- Do not include synthetic rows in scientific demos except to explain
  mechanics.

## Metrics

Primary metric is R2. Metric values are test fixtures, not model evidence.

## References

- PhenoBench architecture: `docs/architecture.md`
- Synthetic task implementation: `phenobench/tasks/synthetic.py`

## Open Questions

- Should synthetic tasks be hidden from the main clinical card index?
