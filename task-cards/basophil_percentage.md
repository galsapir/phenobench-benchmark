# Basophil Percentage Task Card

Status: draft

Task id: `basophil_percentage`

Evidence status: grounded

Evidence reviewed: 2026-07-15

Benchmark status: complete

## Target

Basophil percentage from the HPP five-part CBC differential, collapsed by participant and visit.

Implementation facts:

- bodily system: immune
- target dataset/field: `cbc.ba`
- unit: %
- acquisition: Beckman Coulter DxH 560, EDTA whole blood
- default stages: `00_00_visit` and `02_00_visit`
- collapse: participant-stage mean
- range/QC: 0-100%; continuous target
- paper fidelity: HPP immune extension
- evidence confidence: low; known source discordance

## Why This Matters

Basophil percentage measures relative composition of circulating leukocytes. It is compositional and does not equal absolute cell abundance or immune function.

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

- Mask the full same-visit CBC and HMO CBC, including WBC and every differential absolute/percentage field; differential percentages sum to approximately 100%.
- HPP basophils have poor concordance with HMO reports and a compressed analyzer distribution; this Task is exploratory and low-confidence.
- A good score supports prediction of this analyzer-derived value only; it does
  not establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns,
target quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Reicher et al. (2024), HPP longitudinal aging phenotypes, <https://doi.org/10.1038/s43587-024-00734-9>.
- HPP Research OS `cbc` dataset documentation and field/QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=2215; train=1517, validation=363, test=335

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.002 | 0.129 | 0.066 |
| Linear | `linear` | 0.263 | 0.111 | 0.521 |
| Trees | `gbdt_delta_r2` | 0.192 | 0.116 | 0.440 |
| LOCF | `last_observation_carried_forward` | -0.026 | 0.131 | 0.518 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
