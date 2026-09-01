# White Blood Cell Count Task Card

Status: draft

Task id: `wbc`

Evidence status: grounded

Evidence reviewed: 2026-07-15

Benchmark status: complete

## Target

Total white blood cell count from the HPP CBC, collapsed by participant and visit.

Implementation facts:

- bodily system: immune
- target dataset/field: `cbc.wbc`
- unit: 10^3/µL
- acquisition: Beckman Coulter DxH 560, EDTA whole blood
- default stages: `00_00_visit` and `02_00_visit`
- collapse: participant-stage mean
- range/QC: 0.1-100 10^3/µL broad plausibility guard; continuous target
- paper fidelity: exact HealthFormer endpoint
- evidence confidence: standard HPP measurement

## Why This Matters

WBC is a broad marker of circulating immune-cell abundance. Prediction does not establish infection, inflammation, marrow disease, or immune function.

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

- Mask the full same-visit CBC and HMO CBC. Differential absolute counts and percentages algebraically constrain total WBC.
- Acute illness, medication, collection timing, and the DxH 560 analyzer affect values.
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
- common cohort: n=2214; train=1516, validation=363, test=335

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.011 | 1.579 | 0.138 |
| Linear | `linear` | 0.474 | 1.152 | 0.691 |
| Trees | `gbdt_delta_r2` | 0.417 | 1.213 | 0.647 |
| LOCF | `last_observation_carried_forward` | 0.369 | 1.261 | 0.694 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- The v0 systemic Benchmark Tracks received clinical review on 2026-07-28.
