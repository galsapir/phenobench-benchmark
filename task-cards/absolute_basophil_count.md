# Absolute Basophil Count Task Card

Task id: `absolute_basophil_count`

Evidence status: grounded

Evidence reviewed: 2026-07-15

Benchmark status: complete

## Target

Absolute basophil count from the HPP five-part CBC differential, collapsed by participant and visit.

Implementation facts:

- bodily system: immune
- target dataset/field: `cbc.ba_number`
- unit: 10^3/µL
- acquisition: Beckman Coulter DxH 560, EDTA whole blood
- default stages: `00_00_visit` and `02_00_visit`
- collapse: participant-stage mean
- range/QC: 0-50 10^3/µL broad plausibility guard; continuous target
- paper fidelity: HPP immune extension
- evidence confidence: low; known source discordance

## Why This Matters

Absolute basophil count measures circulating basophil abundance. Prediction alone does not diagnose an immune disorder or establish cell function.

## Related HPP Measurements

The CBC contains red-cell indices, platelet measurements, total WBC, and the
five-part absolute and percentage differential. These are related measurements,
not independent labels.

## Clinically Meaningful Variants

The continuous measurement is primary. Clinical low/high categories depend on
age, sex, pregnancy, symptoms, laboratory reference intervals, and repeat
testing; no diagnostic category is transferred into this Task.

## Baselines And Ceilings

For V1→V2 evaluation, compare age/sex/BMI demographic floor, prior-value LOCF,
OLS on prior value plus demographics, and GBDT on the same inputs. All rows must
share one cohort and split.

## Caveats

- Mask the full same-visit CBC and HMO CBC, including WBC and every differential absolute/percentage field; absolute count is approximately WBC × percentage.
- HPP basophils have poor concordance with HMO reports and a compressed analyzer distribution; this Task is exploratory and low-confidence.
- A good score supports prediction of this analyzer-derived value only; it does
  not establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns,
target quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Reicher et al. (2024), HPP longitudinal aging phenotypes, <https://doi.org/10.1038/s43587-024-00734-9>.
- HPP documentation `cbc` dataset documentation and field/QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=2215; train=1517, validation=363, test=335

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.007 | 0.010 | 0.086 |
| Linear | `linear` | 0.368 | 0.008 | 0.618 |
| Trees | `gbdt_delta_r2` | 0.333 | 0.008 | 0.601 |
| LOCF | `last_observation_carried_forward` | 0.204 | 0.009 | 0.616 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- The v0 systemic Benchmark Tracks received clinical review on 2026-07-28.
