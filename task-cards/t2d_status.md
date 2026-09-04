# T2D Status Task Card

Task id: `t2d_status`

Evidence status: grounded

Evidence reviewed: 2026-08-15

## Target

Participant-level binary classification:

- positive label: self-reported diabetes, HbA1c ≥6.5%, or fasting plasma
  glucose ≥126 mg/dL
- negative label: at least one valid normal-range HbA1c or fasting glucose
  measurement, with no positive or intermediate-glycaemia evidence
- excluded labels: HbA1c 5.7–6.4%, fasting glucose 100–125 mg/dL, unknown
  laboratory status, and known type 1 diabetes `5A10`

Implementation facts:

- target dataset: `anat_curated_phenotype_diabetes`
- target source: `anat.curated_phenotype.diabetes` - the dataset and the source
  are two different strings on this Task; earlier text here used the source name
  for both
- target field: `composite_diabetes_compatible_status`, a label composed from
  `self_reported_diabetic`, `bloodtest_hba1c` and `bloodtest_fpg` only
- type 1 exclusion codes: `5A10`
- target unit: binary status; target shape: categorical
- default research stage: `00_00_visit`
- default covariates: age, sex, BMI from `anthropometrics`
- primary metric: ROC AUC

Unlike `prediabetes_status`, this Task does **not** take the curated-phenotype
mixin - it composes its own label from the three named inputs, which is why its
positive/negative rule is spelled out above rather than delegated to a label map.

This is a Carletti-2025-inspired HPP analogue. The paper trained a binary
normoglycemic-vs-T2D model on PROGRESS and applied a glycemic-risk score to HPP.
The PhenoBench Task is HPP-native T2D status on canonical splits, so it should
not be described as paper-faithful replication.

The replaced singular `medical_condition` route found only 21 positives and
five canonical-test positives. The checksum-bound final CGM and DXA cohorts
contain 4,236 and 3,028 participants respectively. CGM has 65/15/19 positives
across train/validation/test (99 total); DXA has 40/9/13 (62 total).

## Why This Matters

T2D status is a clinically grounded categorical metabolic target. It is useful
for testing whether CGM and multimodal feature surfaces add disease-state
signal beyond age, sex, and BMI.

The Carletti paper makes this a useful forcing case for PhenoBench because it
needs categorical target support, probability-valued classifier Strategies, and
clear analogue-vs-paper-faithful provenance.

**What a row here does not support.** This is same-visit discrimination of a
research label composed from self-report and two laboratory fields. It is not an
adjudicated diagnosis, not incident-T2D prediction, and not a screening-utility
claim. It also does not establish diabetes *type*: the label excludes coded type 1
diabetes but HbA1c and FPG cannot themselves distinguish types.

## Related HPP Measurements

Demonstrated in HPP:

- **Both laboratory legs of this label are measurably unstable at the
  boundary.** Of 5,328 HPP participants normal on a first fasting-glucose
  reading, 3% reached the diabetes range (≥126 mg/dL) and 40% the prediabetes
  range on sequential measurement within the same study (Shilo et al. 2024).
  This Task's exclusion of the intermediate band removes much of that churn
  from the scored population, which is a strength of the label rule rather than
  an accident.
- **Incident metabolic disease, including diabetes, is predicted by CGM range
  occupancy in this cohort**: 444 new metabolic conditions among 6,550
  participants over 2.6 ± 1.3 years, with an age- and sex-adjusted HR of 1.34
  (95% CI 1.26-1.42) per higher time above 140 mg/dL (Godneva et al. 2026).
  That is a different estimand from this Task and should not be cited as
  support for a cross-sectional row.
- CGMap gives the HPP reference distribution for CGM measures in non-diabetic
  individuals (Keshet et al. 2023).

The class balance recorded below - 99 positives across the CGM cohort, 62 across
DXA - is the operative constraint on what any of this can demonstrate here.

**On the GBDT paired comparison against the demographic floor the two tracks
split**: V1 CGM reaches **ΔAUROC = +0.182 (95% CI [+0.118, +0.251])** on
n = 4,236 and clears; V1 DXA reaches **+0.079 ([-0.073, +0.205])** on n = 3,028
and does not. So CGM summaries add real discrimination for this label beyond
age, sex and BMI, and DXA is not demonstrated to - on a positive count small
enough that the DXA interval is wide rather than informative.

## Clinically Meaningful Variants

This Task *is* the categorical variant, and its label rule is already the
threshold decision. Two variants are worth naming, one defensible and one not:

- **Defensible: the full ordinal.** Exposing non-diabetes / prediabetes /
  diabetes as one ordered label would use the intermediate band this Task
  discards, and would make the boundary explicit rather than excluded. It needs
  a different Strategy contract and its own cohort, so it is a new Task, not a
  variant flag. `prediabetes_status` currently covers the lower boundary as a
  separate binary.
- **The label already fires on ONE abnormal value, and that is the thing to
  know about it.** `positive = self_reported | hba1c >= 6.5 | fpg >= 126.0`
  (an internal review record), with no confirmatory second measurement anywhere in
  the rule; `tests/test_an internal review record pins HbA1c-only and FPG-only cases as
  positive. ADA requires a confirmatory second test for an asymptomatic person
  (ADA 2026), and the HPP reclassification measurement above shows why: 3% of
  participants normal on a first fasting glucose reach the diabetes range on a
  later one. **So this is a permissive research label, not a confirmed
  diagnosis, and its positive class contains single-measurement positives.**
  An earlier version of this card claimed the Task "declines to call a single
  abnormal research measurement a diagnosis" - it declines to call it a
  diagnosis in prose, but the label rule does not require confirmation, and
  reading the two together implied a stricter contract than the code has.
  Tightening it to require confirmation would be a cohort change, not a wording
  change.

The thresholds themselves (≥6.5%, ≥126 mg/dL) do transfer, because they are
guideline-defined on the same quantities in comparable adult populations - but
they define a *research label*, not a diagnosis, and the distinction is the
whole content of the non-claim above.

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29.

literature review supports CGM summaries and DXA body composition as compact
status-discrimination panels beyond age, sex, and BMI. These are
cross-sectional disease-state associations, not incident T2D prediction.
The approved label route is CGM-independent, so CGM can be evaluated without
constructing its own target. ADA diagnostic thresholds ground the laboratory
components. A single abnormal research measurement is not a confirmed
clinical diagnosis, and HbA1c/FPG do not establish diabetes type.

The condition-code exclusion is intentionally limited to ICD-11 `5A10`
(type 1 diabetes). ICD-11 `5A41` denotes hypoglycaemia without associated
diabetes; it is not a type 1 code and is not part of this exclusion.

## Baselines And Ceilings

The required floor is a no-modality-feature classifier baseline:
`NoFeaturesPredictor` contributes no modality features, and
`DemographicClassifierFloorStrategy` fits age, sex, and BMI.

The first classical feature comparator is `CgmIgluPredictor` plus
`LogisticRegressionStrategy`. This is a stable-loader analogue of the paper's
CGM spike-feature model, not an exact spike-feature reproduction.

Meaningful future ceilings include:

- exact Carletti spike features from raw CGM
- food and gut-microbiome feature groups
- tree-based classifier Strategy, matching the paper's XGBoost family
- imported external PROGRESS-trained probabilities, if the model artifact is
  available

## Caveats

- The composite is an adult diabetes-compatible research label, not an
  adjudicated T2D diagnosis.
- Self-reported prediabetes with normal same-visit HbA1c/FPG is not separately
  excluded and may appear among controls.
- One abnormal HbA1c or FPG is not confirmatory in an asymptomatic person.
- HbA1c should not be used as a predictor for this Task because it anchors
  glycemic status and is a comparator in the source paper.
- Canonical hash splits are not stratified. Rare positive labels can create
  one-class train or eval splits; the Task fails loud in that case.
- The v1.2 plural `medical_conditions` table contains a broader English-name
  `pre diabetes` surface coded as `5A40`; that route is not used here and may
  be the better basis for a separate Carletti HPP risk-profile analogue.
- HPP-only model training changes the scientific claim. Carletti's reported
  external HPP AUC/AUPRC cannot be assumed comparable unless the exact external
  protocol is reproduced.

## Metrics

- Primary: ROC AUC.
- Secondary: average precision, balanced accuracy, accuracy, Brier score,
  positive rate, split Ns.

ROC AUC and average precision use positive-class probabilities. Accuracy and
balanced accuracy use threshold 0.5 and are secondary only.

## References

- Carletti et al. (2025), multimodal AI correlates of glucose spikes,
  *Nature Medicine*, <https://doi.org/10.1038/s41591-025-03849-7>. Local copy in
  **HPP documentation**: `assets/papers/hpp/carletti_2025_multimodal_ai_correlates_of_glucose_spik/`.
- HPP medical-condition code route, in **HPP documentation**:
  `assets/datasets/medical_conditions/loader.md`
- Prediabetes/T2D code caveat, in **HPP documentation**:
  `assets/datasets/medical_conditions/notes.md`
- Bragg et al. (2022), circulating NMR biomarkers and incident T2D risk,
  <https://doi.org/10.1186/s12916-022-02354-9>.
- ADA Standards of Care in Diabetes 2026, diagnosis and classification,
  <https://doi.org/10.2337/dc26-S002>.
- WHO ICD-11 MMS 2026, `5A10` type 1 diabetes and `5A41` hypoglycaemia
  without associated diabetes,
  <https://icd.who.int/browse/2026-01/mms/en#1651053999>.
- Shilo et al. (2024), continuous glucose monitoring and intrapersonal
  variability in fasting glucose, *Nature Medicine*,
  <https://doi.org/10.1038/s41591-024-02908-9>.
- Godneva et al. (2026), the spectrum of normoglycemia and time in glycemic
  ranges, *Diabetes Care*, <https://doi.org/10.2337/dc25-2154>.
- Keshet et al. (2023), CGMap, *Cell Metabolism*,
  <https://doi.org/10.1016/j.cmet.2023.04.002>.

## Open Questions

- Should categorical clinical Tasks move to stratified canonical splits, or
  should class-degenerate splits remain a loud data-routing failure?
- Where should paper provenance live in run manifests: config metadata,
  leaderboard row columns, or a separate paper-task registry?
