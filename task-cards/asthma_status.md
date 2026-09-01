# Asthma Status Task Card

Status: draft

Task id: `asthma_status`

Evidence status: grounded

Evidence reviewed: 2026-07-29

## Target

Participant-level binary classification of asthma status from the curated
asthma phenotype table.

Implementation facts:

- target dataset release: `anat_curated_phenotype`
- target table: `anat.curated_phenotype.asthma`
- target column read: `curated_phenotype`. **This is hardcoded in the loader**
  (`hpp_loader.py:1450`), not taken from the Task
- `target_field` on the class is `asthma__curated_phenotype` and is **inert on
  this release** - it is read only by the alternate `frozen_v1_2` route
  (`_curated_phenotype_status.py:336`). Do not treat it as the operative field
- positive label: `Asthma`
- negative label: `normal`
- excluded states: missing
- default research stage: `00_00_visit`
- default covariates: age, sex, BMI from baseline anthropometrics
- primary metric: ROC AUC

## Why This Matters

Asthma is a common pulmonary condition selected in DS-1584. It broadens the
condition-status Task set beyond cardiometabolic and endocrine outcomes.

## Baselines And Ceilings

The required floor is a no-modality-feature classifier baseline:
`NoFeaturesPredictor` contributes no modality features, and
`DemographicClassifierFloorStrategy` fits age, sex, and BMI.

Useful future comparators include questionnaire features, medication records,
spirometry if available, microbiome features, and MMFM participant embeddings.

## Caveats

- Labels come from the curated asthma panel, not spirometry or
  clinician-adjudicated asthma.
- Allergic and non-allergic asthma may be heterogeneous under the curated
  binary label.
- A **Condition-Control** means `normal` in the curated asthma panel, not
  absence of allergy or other pulmonary disease.

## Metrics

Primary: ROC AUC. Secondary: average precision, accuracy, balanced accuracy,
Brier score, positive rate, split sizes.

## Benchmark-Track Evidence

OpenEvidence review and broader Paperclip search support Nightingale and DXA
as distinct V1 tracks. GlycA and fatty-acid profiles have asthma associations
beyond BMI, while DXA central adiposity adds sex-dependent information.
HPP pseudo-outcome work also reports substantial metabolomic lift for asthma,
but it did not directly classify this curated label. Exclude asthma/allergy
questionnaires, medication, spirometry, and all curated-phenotype fields.

## References

- DS-1584 Yeela-selected condition curation:
  `pha_condition_projection/DS-1584/condition_candidates_detailed.csv`.
  **Does not resolve** in this repository or in research-os / research-harness /
  research-os-stable; kept because it is the only pointer to how this condition
  was selected, and marked so it is not read as a repo path.
- HPP refreshed curated-phenotype docs for `anat.curated_phenotype.asthma`.
- Li et al. (2024), GlycA and respiratory disease:
  <https://doi.org/10.1038/s41467-024-47845-w>.

## Open Questions

- Should asthma be split by allergic vs non-allergic status if source labels
  support it?
