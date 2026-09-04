# Hemoglobin Task Card

Task id: `hemoglobin`

Evidence status: grounded

Evidence reviewed: 2026-07-29

Benchmark status: complete

## Target

Hemoglobin concentration from the HPP complete blood count (CBC), collapsed by participant and visit.

Implementation facts:

- bodily system: hematologic
- target dataset/field: `cbc.hgb`
- unit: g/dL
- acquisition: Beckman Coulter DxH 560, EDTA whole blood
- default stages: `00_00_visit` and `02_00_visit`
- collapse: participant-stage mean
- range/QC: 5-25 g/dL broad plausibility guard; continuous target
- paper fidelity: exact HealthFormer endpoint
- evidence confidence: standard HPP measurement

## Why This Matters

Hemoglobin summarizes oxygen-carrying capacity and is a clinically familiar
hematologic measurement. In HPP's adult cohort, interpretation varies with sex
and age. Prediction does not diagnose anemia or identify its cause.

## Related HPP Measurements

The CBC contains hematocrit and red-cell indices; ferritin and other blood tests
add iron, renal, and inflammatory context. HPP sex-specific factors capture
menstrual and menopausal context. These are related measurements,
not independent labels.

## Benchmark-Track Evidence

Population NMR/MS profiling finds sex-specific hemoglobin associations with
fatty-acid species, branched-chain amino-acid catabolites, heme catabolites, and
lipoprotein particles. DXA provides a distinct lean-mass and regional-adiposity
question beyond BMI. Neither track may include any same-visit CBC field.

## Clinically Meaningful Variants

The continuous measurement is primary. WHO defines anemia in adults as hemoglobin
below 13.0 g/dL in men and below 12.0 g/dL in non-pregnant women; these cutoffs are
specified for venous automated-analyzer hemoglobin in g/dL and so are measurement-compatible
with this HPP target. Age-specific adult thresholds have been proposed but are not yet
adopted in major guidelines. A separate adult anemia Task built on these cutoffs, auditing
age and sex strata, would identify low hemoglobin but does not identify anemia cause or
replace iron, renal, inflammatory, or clinical workup.

## Baselines And Ceilings

For V1→V2 evaluation, compare age/sex/BMI demographic floor, prior-value LOCF,
OLS on prior value plus demographics, and GBDT on the same inputs. All rows must
share one cohort and split.

## Caveats

- Mask the full same-visit CBC and HMO blood-count equivalents. RBC, hematocrit, MCH, and MCHC can approximately reconstruct hemoglobin.
- Sex, hydration, altitude, inflammation, and CBC analyzer calibration affect interpretation.
- Do not silently add race-based threshold adjustments; any categorical variant
  needs a separately reviewed label specification.
- A good score supports prediction of this analyzer-derived value only; it does
  not establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns,
target quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Reicher et al. (2024), HPP longitudinal aging phenotypes, <https://doi.org/10.1038/s43587-024-00734-9>.
- Kaul et al. (2018), population metabolomic fingerprints of ferritin and hemoglobin, <https://doi.org/10.3390/nu10111800>.
- Pasricha et al. (2024), WHO hemoglobin thresholds, <https://doi.org/10.1016/S0140-6736(24)00502-6>.
- Braat et al. (2024), age- and sex-specific hemoglobin thresholds for defining
  anemia, <https://doi.org/10.1016/S2352-3026(24)00030-9>.
- HPP documentation `cbc` dataset documentation and field/QC inventory.

## V0 Benchmark Execution

The two same-visit V1 tracks completed on 2026-07-29; both Ridge/GBDT rows per
track are locally successful and remotely `FINISHED` in operational source.

- Nightingale: n=2,752; test=438; best R2=0.470 (Ridge), with paired delta R2
  +0.025 [-0.003, 0.052] over age/sex/BMI.
- DXA: n=4,502; test=687; best R2=0.463 (Ridge), with paired delta R2
  +0.017 [0.005, 0.030].
- Full rows and provenance:
  deep dive and
  aggregate review.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=2215; train=1516, validation=364, test=335

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.415 | 0.890 | 0.645 |
| Linear | `linear` | 0.679 | 0.659 | 0.824 |
| Trees | `gbdt_delta_r2` | 0.665 | 0.673 | 0.816 |
| LOCF | `last_observation_carried_forward` | 0.621 | 0.716 | 0.808 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
- Adult anemia-status label construction is tracked in
  #31.
- Cross-modal V1 value-add is tracked in
  #28.
