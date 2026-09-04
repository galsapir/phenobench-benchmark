# Hypothyroidism Status Task Card

Task id: `hypothyroidism_status`

Evidence status: grounded

Evidence reviewed: 2026-07-29

Benchmark status: complete

## Target

Participant-level binary classification of active reported hypothyroidism
status from the live `medical_condition` route.

Implementation facts:

- positive condition codes: `5A00`, `5A00.2`
- condition source stage: not exposed by the live `medical_condition` route;
  labels are not stage-filtered
- target dataset: `medical_condition`
- curated phenotype equivalent: not present in current `curated_phenotypes`
- default covariates: age, sex, BMI from baseline anthropometrics
- primary metric: ROC AUC

## Why This Matters

Hypothyroidism is a common endocrine condition with broad metabolic effects.
It was selected in DS-1584 as a review-ready condition with enough HPP support
for a disease-status benchmark.

## Benchmark-Track Evidence

External metabolomic studies distinguish biochemically defined subclinical and
clinical hypothyroidism, supporting a cross-modal question. They do not validate
the HPP label: this Task has an active self-report/medical-condition label
without visit timing, medication confirmation, or TSH/free-T4 adjudication.
The supported outcome is therefore reported condition status, not biochemical
or incident hypothyroidism.

## Baselines And Ceilings

The required floor is a no-modality-feature classifier baseline:
`NoFeaturesPredictor` contributes no modality features, and
`DemographicClassifierFloorStrategy` fits age, sex, and BMI.

Useful future comparators include thyroid function labs, medication records,
clinical chemistry, questionnaire features, and MMFM participant embeddings.

## Caveats

- Labels come from self-reported active medical-condition rows, not thyroid lab
  thresholds or medication adjudication.
- Treated hypothyroidism may have normal contemporaneous labs, so lab-based
  comparators and diagnosis labels can disagree.
- The route exposes no onset date or research stage; do not describe the target
  or result as V1, V2, incident disease, or disease progression.
- A **Condition-Control** means no active hypothyroidism row, not absence of all
  endocrine disease.

## Metrics

Primary: ROC AUC. Secondary: average precision, accuracy, balanced accuracy,
Brier score, positive rate, split sizes.

## References

- DS-1584 Yeela-selected condition curation:
  `pha_condition_projection/DS-1584/condition_candidates_detailed.csv`.
  **Does not resolve** in this repository or in HPP documentation / HPP documentation /
  HPP documentation; kept because it is the only pointer to how this condition
  was selected, and marked so it is not read as a repo path.
- Shao et al. (2023), metabolomics of biochemically defined hypothyroidism,
  <https://doi.org/10.1210/clinem/dgac555>.
- Biondi et al. (2019), subclinical hypothyroidism definition and interpretation,
  <https://doi.org/10.1001/jama.2019.9052>.

## V0 Benchmark Execution

The two participant-level tracks completed on 2026-07-29; both Ridge/GBDT rows
per track are locally successful and remotely `FINISHED` in operational source.


- Nightingale: n=10,128; test=1,542 (102 positive, 1,440 negative); best
  AUROC=0.681 (logistic regression). The paired delta AUROC over age/sex/BMI
  was +0.015 [-0.011, 0.040].
- DXA: n=9,001; test=1,351 (87 positive, 1,264 negative); best AUROC=0.668
  (logistic regression), with paired delta AUROC
  +0.004 [-0.013, 0.021].
- Full rows and provenance:
  deep dive and
  aggregate review.

## Open Questions

- Should future versions add a lab-defined thyroid dysfunction Task alongside
  this condition-status Task?
