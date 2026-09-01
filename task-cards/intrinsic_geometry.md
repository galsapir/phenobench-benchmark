# Intrinsic Geometry Task Card

Status: draft

Task id: `intrinsic_geometry`

Evidence status: seed

Evidence reviewed: 2026-08-15

Grounding does not apply: this is a label-free geometry diagnostic over an
embedding matrix. It has no target Y at all, and the Evidence Grounding
Contract is about defining Y. Assessed and found out of scope.

## Target

No clinical target. This task evaluates label-free geometry diagnostics for an
embedding matrix.

Implementation facts:

- target shape: none
- target field: none
- target dataset: none
- primary metric: `rankme_normalized`
- eval category: intrinsic

## Why This Matters

Intrinsic geometry checks can detect representation collapse, dimensionality
pathologies, and paired-view structure issues before a supervised clinical row
is interpreted. They are framework diagnostics, not evidence that a model
learned a phenotype.

## Baselines And Ceilings

No supervised demographic floor applies. Natural comparators are frozen
reference embeddings, paired-view diagnostics, permutation/null checks, and
the specific geometry metrics documented in the walkthrough configs.

## Caveats

- Good geometry does not imply clinical utility.
- Bad geometry can explain downstream failure but does not identify the
  clinical source of failure.
- Metrics are sensitive to preprocessing, sample support, and duplicate rows.
- Do not compare geometry metrics across embeddings unless the input matrix
  construction is matched.

## Metrics

Primary metric is `rankme_normalized`. Other geometry metrics should be read
as diagnostics rather than clinical endpoints.

## References

- PhenoBench architecture: `docs/architecture.md`
- Walkthrough configs under the internal evaluation configuration
- No HPP clinical paper is claimed as direct support for this framework-only
  diagnostic task.

## Open Questions

- Which geometry metrics should be stable enough for leaderboard display?
- Should intrinsic diagnostics live in a separate index from clinical Task
  Cards?
