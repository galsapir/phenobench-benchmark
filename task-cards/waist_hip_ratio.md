# Waist-Hip Ratio Task Card

Status: draft

Task id: `waist_hip_ratio`

Evidence status: grounded

Evidence reviewed: 2026-07-29

## Target

Waist-to-hip ratio. Continuous-scalar regression. The default research stage is
`00_00_visit`, but the Task can be configured for another available stage.

Implementation facts:

- target field: `waist_to_hip_ratio`
- target dataset: `anthropometrics`
- target source: None
- default research stage: `00_00_visit`
- valid range: 0.5-1.5
- primary metric: R2

## Why This Matters

Waist-hip ratio captures body-fat distribution rather than absolute body size.
It is clinically interpretable as a central-adiposity marker and complements
BMI, waist circumference, and VAT.

For PhenoBench, WHR is a body-shape probe where sex and BMI explain substantial
signal but do not fully define the target.

## Baselines And Ceilings

The required floor is a no-modality-feature baseline: `NoFeaturesPredictor`
contributes no modality features, and `DemographicFloorStrategy` fits age, sex,
and BMI. The task code records a moderate floor around R2 0.46.

Natural comparators include waist, hip circumference, BMI, VAT, gait/activity
features, and metabolic panels. The meaningful claim is added shape/metabolic
signal beyond sex and BMI.

## Benchmark-Track Evidence

OpenEvidence review found that direct waist, hip, and regional-DXA features are
too close to this ratio for a clean modality-addition claim. The proposed V1/V2
track therefore uses only age, sex, BMI, and the fixed Nightingale panel. Its
interpretation is metabolic information about body-fat distribution, not
algebraic reconstruction of WHR.

## Caveats

- Sex distribution can dominate the task.
- Measurement protocol and hip/waist field quality matter.
- Same-anthropometrics predictors can trivially reconstruct the ratio.
- WHR prediction is not the same as incident cardiometabolic disease
  prediction.

## Metrics

Primary metric is R2. Secondary MAE and Spearman are useful. Audit views should
include sex-stratified residuals and demographic-floor delta R2.

## References

- Source material: `docs/task_cards/source_material/foundation-model-surrogate-targets-v1.md`
- Waist/central-adiposity clinical context from the source material's
  body-composition section.
- Reicher et al. (2025), deep phenotyping of the health/disease continuum,
  *Nature Medicine*, <https://doi.org/10.1038/s41591-025-03790-9>. Local copy in **research-os**:
  `assets/papers/hpp/reicher_2025_deep_phenotyping_of_healthdisease_contin/`.
- Neeland et al. (2019), replicated NMR signature of visceral adiposity,
  <https://doi.org/10.1161/JAHA.118.010810>.

## Open Questions

- Should hip circumference be exposed as a separate task or remain only as a
  component of WHR?
- Should WHR rows require sex-stratified reporting?
- Which anthropometric feature routes are too close to the target to be useful?
