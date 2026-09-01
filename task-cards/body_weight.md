# Body Weight Task Card

Status: draft

Task id: `body_weight`

Evidence status: grounded

Evidence reviewed: 2026-07-29

Benchmark status: complete

## Target

Body Weight as a continuous participant-visit scalar.

Implementation facts:

- bodily system: anthropometric
- target route: `anthropometrics.weight`
- unit: kg
- acquisition/source: HPP clinic scale (Shekel h120-4)
- default stages: `00_00_visit` and `02_00_visit`
- collapse: participant-stage mean
- range/QC: 30-200 kg
- paper fidelity: exact HealthFormer endpoint

## Why This Matters

Weight is a familiar longitudinal anthropometric measurement and a component of many metabolic phenotypes. Prediction does not identify body composition or cause of change.

## Related HPP Measurements

Height, BMI, waist/hip measures, DXA fat/lean mass, medications, pregnancy, and edema-related measurements.

## Clinically Meaningful Variants

Continuous prediction is primary. Any clinical category requires
measurement-compatible thresholds, population validation, and a separate Task;
this card does not authorize diagnostic bins.

## Baselines And Ceilings

For V1→V2 evaluation, compare an age/sex floor, prior-value LOCF, OLS, and
GBDT. V1 BMI may enter a V2 forecast, but same-visit BMI is prohibited because
it contains weight. Use one cohort and split for all comparisons.

## Benchmark-Track Evidence

OpenEvidence review found stronger independent Nightingale evidence for VAT
than for weight itself. Weight remains in the shared adiposity/body-size track
as a representation probe, not a clinical headline. V1 age, sex, BMI, and the
fixed Nightingale panel may predict V1 or V2 weight; height, waist, hip, every
DXA field, and same-visit BMI remain excluded. The V1 floor is age/sex only;
the V2 track may use V1 BMI.

## Caveats

- For same-visit prediction, BMI is prohibited because it contains weight. V1 BMI is allowed only as a past covariate for V2 prediction.
- Clothing, hydration, pregnancy, edema, scale calibration, and time of day affect weight; weight is not adiposity.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns,
target quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Reicher et al. (2025), Human Phenotype Project cohort profile, <https://doi.org/10.1038/s41591-025-03790-9>.
- Jakicic et al. (2024), physical-activity and weight-management guidance, <https://doi.org/10.1249/MSS.0000000000003520>.
- HPP Research OS `anthropometrics` dataset documentation and field/QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=5845; train=4038, validation=913, test=894

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.765 | 7.093 | 0.875 |
| Linear | `linear` | 0.912 | 4.357 | 0.955 |
| Trees | `gbdt_delta_r2` | 0.907 | 4.473 | 0.952 |
| LOCF | `last_observation_carried_forward` | 0.909 | 4.407 | 0.954 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- Should a future Task predict weight change rather than absolute V2 weight?
