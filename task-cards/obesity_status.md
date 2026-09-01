# Obesity Status Task Card

Status: draft

Task id: `obesity_status`

Evidence status: grounded

Evidence reviewed: 2026-07-29

## Target

Participant-level binary classification of obesity status from the curated BMI
phenotype table.

Implementation facts:

- target dataset release: `anat_curated_phenotype`
- target table: `anat.curated_phenotype.bmi`
- target column read: `curated_phenotype`. **This is hardcoded in the loader**
  (`hpp_loader.py:1450`), not taken from the Task
- `target_field` on the class is `bmi__curated_phenotype` and is **inert on
  this release** - it is read only by the alternate `frozen_v1_2` route
  (`_curated_phenotype_status.py:336`). Do not treat it as the operative field
- positive labels: `Obese`, `Severe obesity`
- negative labels: `Normal`, `Overweight`
- excluded states: `Underweight`, missing
- default research stage: `00_00_visit`
- default covariates: age, sex, BMI from baseline anthropometrics
- primary metric: ROC AUC

## Why This Matters

Obesity is a common metabolic condition selected in DS-1584. It is included as
a binary BMI-class status benchmark, not as a replacement for continuous
anthropometric Tasks such as VAT, waist, or waist-to-hip ratio.

## Baselines And Ceilings

The required floor is a no-modality-feature classifier baseline:
`NoFeaturesPredictor` contributes no modality features, and
`DemographicClassifierFloorStrategy` fits age, sex, and BMI.

Useful future comparators include anthropometric measurements, DXA body
composition, sleep/activity features, gut microbiome species, and MMFM
participant embeddings.

## Benchmark-Track Evidence

The current target is defined by BMI categories and the current floor includes
BMI. This makes the floor partly deterministic rather than merely strong:
modality addition cannot be interpreted honestly. The Task should not be
ranked in v0 unless BMI is removed from the allowed floor or the target changes
to an obesity phenotype not defined by BMI.

## Caveats

- BMI is part of the requested demographic floor and is also clinically central
  to obesity definition; the demographic floor is partly definitional here.
- Labels come from the curated BMI panel, not self-reported diagnosis rows.
- Underweight is excluded rather than treated as a healthy/non-obese control.
- This Task should not be used to claim multimodal value unless compared
  against the BMI-containing floor.

## Metrics

Primary: ROC AUC. Secondary: average precision, accuracy, balanced accuracy,
Brier score, positive rate, split sizes.

## References

- DS-1584 Yeela-selected condition curation:
  `pha_condition_projection/DS-1584/condition_candidates_detailed.csv`.
  **Does not resolve** in this repository or in research-os / research-harness /
  research-os-stable; kept because it is the only pointer to how this condition
  was selected, and marked so it is not read as a repo path.
- Existing VAT, waist, and waist-to-hip ratio Tasks for continuous body-size
  targets.
- HPP refreshed curated-phenotype docs for `anat.curated_phenotype.bmi`.

## Open Questions

- Should the full BMI class label become a multiclass/ordinal Task?
