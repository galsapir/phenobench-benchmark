# Fatty Liver Disease Status Task Card

Task id: `fatty_liver_disease_status`

Evidence status: grounded

Evidence reviewed: 2026-07-28

Benchmark status: complete

## Target

Participant-level binary classification of fatty liver disease status from the
curated MAFLD phenotype table.

Implementation facts:

- target dataset release: `anat_curated_phenotype`
- target table: `anat.curated_phenotype.mafld`
- target column read: `curated_phenotype`. **This is hardcoded in the loader**
  (an internal review record), not taken from the Task
- `target_field` on the class is `mafld__curated_phenotype` and is **inert on
  this release** - it is read only by the alternate `frozen_v1_2` route
  (`_curated_phenotype_status.py:336`). Do not treat it as the operative field
- positive label: `MAFLD/NASH`
- negative label: `Normal liver`
- excluded states: `Suspected MAFLD/NASH / Intermediate risk`, missing
- default research stage: `00_00_visit`
- default covariates: age, sex, BMI from baseline anthropometrics
- primary metric: ROC AUC

## Why This Matters

Fatty liver disease is a cardiometabolic liver condition selected in DS-1584.
It complements `fli`, which is a continuous derived Fatty Liver Index, rather
than duplicating it.

## Baselines And Ceilings

The required floor is a no-modality-feature classifier baseline:
`NoFeaturesPredictor` contributes no modality features, and
`DemographicClassifierFloorStrategy` fits age, sex, and BMI.

Useful future comparators include liver enzymes, FLI/FIB scores, lipid panels,
gut microbiome species, and MMFM participant embeddings.

## Benchmark-Track Evidence

literature review prioritized Nightingale metabolomics/lipoproteins and DXA
regional body composition for binary MASLD prediction beyond age/sex/BMI.
Unlike FLI, this target has no explicit triglyceride/BMI/GGT/waist formula, so
the fixed 27-field Nightingale panel and six-field DXA panel are eligible
cross-modal inputs. The label is still a curated phenotype rather than biopsy
or a single direct imaging measurement.

## V0 Benchmark Execution

The frozen same-visit V1→V1 matrix completed on 2026-07-29. All six rows are
locally successful and remotely `FINISHED` in operational source.

- Nightingale: n=6,025; test=920; best AUROC=0.816 (CPU TabSwift). Paired
  linear and GBDT gains over age/sex/BMI were both +0.009, with intervals
  crossing zero.
- DXA: n=7,207; test=1,083; best AUROC=0.867 (CPU TabSwift). Paired gains
  were +0.045 [0.027, 0.063] for logistic regression and +0.053
  [0.032, 0.077] for GBDT.
- Full rows and provenance:
  deep dive and
  aggregate review.

## Caveats

- Labels come from the curated MAFLD panel, not adjudicated biopsy or
  elastography.
- Suspected/intermediate-risk MAFLD is excluded from this binary case/control
  slice.
- Supporting liver-enzyme columns inside the curated phenotype table are curation
  snapshots, not live biomarker values.
- BMI is a strong clinical floor feature and may explain much of the label.
- Alcohol and medication context are not represented in the current binary
  definition.

## Metrics

Primary: ROC AUC. Secondary: average precision, accuracy, balanced accuracy,
Brier score, positive rate, split sizes.

## References

- DS-1584 Yeela-selected condition curation:
  `pha_condition_projection/DS-1584/condition_candidates_detailed.csv`.
  **Does not resolve** in this repository or in HPP documentation / HPP documentation /
  HPP documentation; kept because it is the only pointer to how this condition
  was selected, and marked so it is not read as a repo path.
- Existing `fli` Task for a derived continuous fatty-liver index.
- HPP refreshed curated-phenotype docs for `anat.curated_phenotype.mafld`.
- Masoodi et al. (2021), metabolomics/lipidomics in NAFLD:
  <https://doi.org/10.1038/s41575-021-00502-9>.
- Pang et al. (2022), adiposity, metabolomics, and NAFLD risk:
  <https://doi.org/10.1093/ajcn/nqab392>.

## Open Questions

- Should this Task be paired with an imaging- or FLI-defined fatty-liver target
  before making model-value claims?
- Should the suspected/intermediate-risk label become positive in a broader
  MAFLD-risk Task?
