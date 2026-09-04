# Waist Circumference Task Card

Task id: `waist`

Evidence status: grounded

Evidence reviewed: 2026-07-29

## Target

Waist circumference. Continuous-scalar regression. The default research stage
is `00_00_visit`, but the Task can be configured for another available stage.

Implementation facts:

- target field: `waist_circumference`
- target dataset: `anthropometrics`
- target source: None
- default research stage: `00_00_visit`
- valid range: 50.0-200.0 cm
- primary metric: R2

## Why This Matters

Waist circumference is a simple abdominal-adiposity measure and a clinically
legible cardiometabolic-risk marker. It can capture central adiposity better
than BMI alone, but it remains strongly tied to body size.

For PhenoBench, waist is useful as a low-cost body-shape target and as a
comparator to DXA VAT.

## Baselines And Ceilings

The required floor is a no-modality-feature baseline: `NoFeaturesPredictor`
contributes no modality features, and `DemographicFloorStrategy` fits age, sex,
and BMI. The task code records a high floor around R2 0.74 because BMI is
mechanically close to waist.

Natural comparators include BMI-only/anthropometric models, VAT, waist-to-hip
ratio, activity/gait features, and metabolic feature sets. The interesting
number is lift over the anthropometric floor, not raw R2.

## Benchmark-Track Evidence

literature review and literature search support a BMI-independent Nightingale
signature most strongly for VAT, not waist itself. Waist remains a useful
body-shape probe when every direct anthropometric reconstruction field is
excluded. The proposed V1/V2 track uses only age, sex, BMI, and the fixed
Nightingale panel.

## Caveats

- BMI can almost reconstruct waist; raw performance can be misleading.
- Measurement protocol, clothing, posture, and operator variation can add
  noise.
- Waist is not the same as visceral fat or cardiometabolic event risk.
- Same-anthropometrics predictors can leak target-adjacent measurements.

## Metrics

Primary metric is R2. Secondary MAE in cm is useful. Audit views should include
demographic-floor delta R2 and matched comparison to `vat`.

## References

- Source material: `docs/task_cards/source_material/foundation-model-surrogate-targets-v1.md`
- Waist-circumference cardiovascular-risk context from the source material's
  INTERHEART reference.
- Shilo et al. (2026), heterogeneity of insulin-resistance surrogates,
  *medRxiv*, <https://doi.org/10.64898/2026.05.02.26352290>. Local copy in **HPP documentation**:
  `assets/papers/hpp/shilo_2026_heterogeneity_of_insulin_resistance_surr/`.
- Neeland et al. (2019), replicated NMR signature of VAT,
  <https://doi.org/10.1161/JAHA.118.010810>.

## Open Questions

- Should waist be mainly a comparator for VAT rather than a headline target?
- Which anthropometric predictors should be excluded to avoid trivial
  reconstruction?
- Should sex-specific or ethnicity-specific waist thresholds be added for
  classification variants?
