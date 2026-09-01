# Participant Synthetic Regression Task Card

Status: draft

Task id: `participant_synthetic_regression`

Evidence status: seed

Evidence reviewed: 2026-08-15

Grounding does not apply: a participant-shaped synthetic target for framework
tests, with no clinical referent. Assessed and found out of scope.

## Target

Synthetic participant-shaped continuous regression target used for framework
tests. It is not an HPP clinical target.

Implementation facts:

- target field: synthetic `y`
- target dataset: synthetic
- target source: none
- primary metric: R2

## Why This Matters

This task tests participant-level split semantics, participant IDs, and
framework compatibility without private HPP data. It is useful for engineering
confidence, not scientific claims.

## Baselines And Ceilings

No clinical demographic floor applies. Baselines are synthetic-contract
baselines used by tests.

## Caveats

- No clinical or biological claim is supported.
- Synthetic participant IDs are not HPP participants.
- Do not compare synthetic task metrics to real clinical task metrics.

## Metrics

Primary metric is R2. Metric values are framework fixtures.

## References

- PhenoBench architecture: `docs/architecture.md`
- Synthetic participant task implementation:
  `phenobench/tasks/participant_synthetic.py`

## Open Questions

- Should participant-shaped synthetic cards remain alongside real clinical
  cards or be moved to a framework-test appendix?
