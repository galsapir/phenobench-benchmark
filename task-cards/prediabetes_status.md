# Prediabetes Status Task Card

Status: draft

Task id: `prediabetes_status`

Evidence status: grounded

Evidence reviewed: 2026-08-15

## Target

Participant-level binary classification of prediabetes status from the curated
diabetes phenotype table.

Implementation facts:

- target dataset release: `anat_curated_phenotype` (the mixin default,
  `_curated_phenotype_status.py:62`)
- target table: `anat.curated_phenotype.diabetes`, resolved from
  `anat_table = "diabetes"`
- target column read: `curated_phenotype`. **This is hardcoded in the loader**
  (`hpp_loader.py:1450`), not taken from the Task
- `target_field` on the class is `diabetes__curated_phenotype` and is **inert on
  this release** - it is read only by the alternate `frozen_v1_2` route
  (`_curated_phenotype_status.py:336`). Do not treat it as the operative field
- label map: `{"non-diabetes": 0, "prediabetes": 1}`
- excluded states: `diabetes`, `low confidence diabetes`, missing
- default research stage: `00_00_visit`
- default covariates: age, sex, BMI from baseline anthropometrics
- primary metric: ROC AUC

## Why This Matters

Prediabetes is a clinically important metabolic risk state and a distinct
Yeela-selected DS-1584 condition. It is separate from `t2d_status`, which
explicitly excludes prediabetes from its T2D-vs-normoglycemic definition.

**What a row here does not support.** This is same-visit discrimination of a
curated status label. It is not a diagnosis, not incident-prediabetes
prediction, and not evidence that any feature set would change management. The
label itself is a curation product, so a high AUC is a statement about
recovering that curation, not about identifying a clinical state.

## Related HPP Measurements

Demonstrated in HPP:

- **Prediabetes is among the incident outcomes CGM range-occupancy predicts in
  this cohort.** Godneva et al. followed 6,550 HPP participants a mean of
  2.6 ± 1.3 years; 444 reported a new metabolic condition (prediabetes,
  diabetes, MASLD or hyperlipidemia), and time above 140 mg/dL carried an age-
  and sex-adjusted HR of 1.34 (95% CI 1.26-1.42) (Godneva et al. 2026). That is
  *incident* risk on self-reported diagnoses, a different estimand from this
  Task's same-visit label.
- **The fasting-glucose leg of any prediabetes definition is unstable in HPP.**
  Of 5,328 HPP participants normal on a first fasting-glucose reading, 40% fell
  into the prediabetes range on sequential measurement (Shilo et al. 2024).
- CGMap gives the HPP reference distribution for CGM measures in non-diabetic
  individuals (Keshet et al. 2023).

**The committed rows settle half of the Benchmark-Track hypothesis below, which
an earlier version of this card said they did not.** On the logistic paired
comparison against the demographic floor: V1 CGM **ΔAUROC = +0.049 (95% CI
[+0.018, +0.081])** on n = 11,320 clears the floor; V1 DXA **+0.020 ([-0.004,
+0.044])** on n = 8,868 does not. So CGM summaries discriminate this curated
label beyond age/sex/BMI and DXA body composition is not demonstrated to.

Proposed rather than shown: that either reflects prediabetes physiology rather
than the curation's own inputs.

## Clinically Meaningful Variants

The binary is already the categorical variant, so the live question is whether
its boundary is the right one.

**The ordinal label is the defensible extension; a threshold-derived variant is
not.** ADA defines prediabetes by FPG 100-125 mg/dL, HbA1c 5.7-6.4%, or a
2-hour OGTT value (ADA 2026), and WHO's impaired-fasting-glucose band starts at
110 mg/dL instead - so "prediabetes" is not one measurement with one cutoff, and
reconstructing it from HPP lab fields would mint a fourth definition rather than
apply a validated one. The curated panel exists precisely to avoid that, and it
combines self-report with glycemic support features rather than thresholding a
single live lab.

Two consequences worth stating plainly:

- **The curated label is not interchangeable with an ADA or WHO classification**,
  and a row here must not be reported as ADA-defined prediabetes prevalence or
  detection.
- **Excluded is not negative.** Curated `diabetes` and `low confidence diabetes`
  participants are dropped, not scored as controls, so the operating population
  is prediabetes-vs-non-diabetes and the positive rate is not a cohort
  prevalence.

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29.

OpenEvidence review supports CGM summaries and DXA body composition as compact
status-discrimination panels beyond age, sex, and BMI. CGM differences between
prediabetes and normoglycaemia are cross-sectional correlates, not incident
disease prediction. HbA1c, fasting glucose, diabetes-condition fields, and
glucose-lowering medication must stay out of predictors because they support
the curated label.

## Baselines And Ceilings

The required floor is a no-modality-feature classifier baseline:
`NoFeaturesPredictor` contributes no modality features, and
`DemographicClassifierFloorStrategy` fits age, sex, and BMI.

Useful future comparators include HbA1c, fasting glucose, CGM summaries,
dietary features, gut microbiome species, and MMFM participant embeddings.

## Caveats

- Labels come from the curated diabetes panel, which combines self-report and
  glycemic support features rather than a single live lab threshold.
- Participants with curated diabetes or low-confidence diabetes are excluded,
  not treated as controls.
- The diabetes panel is forward-propagated by the upstream curation.
- HbA1c and fasting glucose are close to the diagnostic boundary and should be
  interpreted as strong clinical comparators, not neutral features.

## Metrics

Primary: ROC AUC. Secondary: average precision, accuracy, balanced accuracy,
Brier score, positive rate, split sizes.

## References

- DS-1584 Yeela-selected condition curation:
  `pha_condition_projection/DS-1584/condition_candidates_detailed.csv`.
  **Does not resolve** in this repository or in research-os / research-harness /
  research-os-stable; kept because it is the only pointer to how this condition
  was selected, and marked so it is not read as a repo path.
- Existing `t2d_status` Task Card for the T2D-vs-normoglycemic boundary.
- HPP `curated_phenotypes` dataset docs for the diabetes curated phenotype.
- Rákóczi et al. (2026), CGM classification versus HbA1c and fasting glucose,
  <https://doi.org/10.1016/j.diabres.2026.113394>.
- Godneva et al. (2026), the spectrum of normoglycemia and time in glycemic
  ranges, *Diabetes Care*, <https://doi.org/10.2337/dc25-2154>.
- Shilo et al. (2024), continuous glucose monitoring and intrapersonal
  variability in fasting glucose, *Nature Medicine*,
  <https://doi.org/10.1038/s41591-024-02908-9>.
- Keshet et al. (2023), CGMap, *Cell Metabolism*,
  <https://doi.org/10.1016/j.cmet.2023.04.002>.
- ADA Standards of Care in Diabetes 2026, diagnosis and classification,
  <https://doi.org/10.2337/dc26-S002>.

## Open Questions

- Should a future Task expose the full non-diabetes / prediabetes / diabetes
  ordinal label instead of this binary prediabetes-vs-non-diabetes slice?
- What exactly does the curated panel use to assign `prediabetes`, and how much
  of it is self-report? The card can say the panel combines self-report with
  glycemic support features, but no committed artifact in this repo records the
  rule, so the label's relationship to ADA or WHO criteria is undocumented on
  our side. Until that is written down, the non-claim above is doing load-bearing
  work.
