# Migraine Status Task Card

Task id: `migraine_status`

Evidence status: grounded

Evidence reviewed: 2026-07-29

## Target

Participant-level binary classification of migraine status from the curated
migraine phenotype table.

Implementation facts:

- target dataset release: `anat_curated_phenotype`
- target table: `anat.curated_phenotype.migraine`
- target column read: `curated_phenotype`. **This is hardcoded in the loader**
  (an internal review record), not taken from the Task
- `target_field` on the class is `migraine__curated_phenotype` and is **inert on
  this release** - it is read only by the alternate `frozen_v1_2` route
  (`_curated_phenotype_status.py:336`). Do not treat it as the operative field
- positive labels: `Self reported migraine, untreated`, `Migraine with
  antimigraine preparations`, `Severe migraine with chronic treatment`
- negative label: `No reported migrane`
- excluded states: missing
- default research stage: `00_00_visit`
- default covariates: age, sex, BMI from baseline anthropometrics
- primary metric: ROC AUC

## Why This Matters

Migraine is a common neurologic condition selected in DS-1584. It gives
PhenoBench a non-metabolic condition-status benchmark where demographic floor
behavior and multimodal signal may differ from cardiometabolic Tasks.

## Baselines And Ceilings

The required floor is a no-modality-feature classifier baseline:
`NoFeaturesPredictor` contributes no modality features, and
`DemographicClassifierFloorStrategy` fits age, sex, and BMI.

Useful future comparators include questionnaire features, sleep features,
medication records, and MMFM participant embeddings.

## Caveats

- Labels come from the curated migraine panel, not adjudicated neurologist
  diagnosis.
- Severity and treatment strata are collapsed into one positive class.
- A **Condition-Control** means `No reported migrane` in the curated panel, not
  absence of all headache disorders.

## Metrics

Primary: ROC AUC. Secondary: average precision, accuracy, balanced accuracy,
Brier score, positive rate, split sizes.

## Benchmark-Track Evidence

literature review and broader literature search support sleep and Nightingale
as two distinct V1 tracks. Prospective and diary studies link sleep disruption
to migraine, while replicated plasma NMR studies identify HDL, lipid,
fatty-acid, and other metabolic associations after age, sex, and BMI
adjustment. These are association benchmarks. Exclude migraine/headache
questionnaires, medications, and every curated-phenotype field.

## References

- DS-1584 Yeela-selected condition curation:
  `pha_condition_projection/DS-1584/condition_candidates_detailed.csv`.
  **Does not resolve** in this repository or in HPP documentation / HPP documentation /
  HPP documentation; kept because it is the only pointer to how this condition
  was selected, and marked so it is not read as a repo path.
- HPP refreshed curated-phenotype docs for `anat.curated_phenotype.migraine`.
- Onderwater et al. (2019), plasma NMR metabolome and migraine:
  <https://doi.org/10.1212/WNL.0000000000007313>.
- Tiseo et al. (2020), migraine and sleep:
  <https://doi.org/10.1186/s10194-020-01192-5>.

## Open Questions

- Should non-migraine headache-disorder phenotypes become a separate broader
  headache Task?
- Should a future Task keep the curated migraine severity/treatment levels as
  an ordinal target?
