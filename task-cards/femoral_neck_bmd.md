# Femoral-Neck Bone Mineral Density Task Card

Status: draft

Task id: `femoral_neck_bmd`

Evidence status: grounded

Evidence reviewed: 2026-07-29

Benchmark status: complete

## Target

Femoral-Neck Bone Mineral Density as a continuous participant-visit measurement.

Implementation facts:

- bodily system: musculoskeletal
- target route: `bone_density.femur_neck_mean_bmd`
- unit: g/cm²
- device/acquisition: GE Lunar Prodigy Advance / enCORE OneScan DXA
- construction/QC: use upstream left/right arithmetic mean; array-index appointment collapse; exclude zero failed-scan sentinel
- valid range: 0.01-3.0 g/cm² broad plausibility guard
- default stages: `00_00_visit` and `02_00_visit`
- paper fidelity: paper-inspired skeletal-imaging analogue

## Why This Matters

Femoral-neck BMD is a standard fracture-risk measurement site. Prediction does not diagnose osteoporosis or estimate fracture risk by itself.

## Related HPP Measurements

Left/right/total-hip BMD, T/Z scores, lumbar BMD, whole-body BMD, DXA body composition, age, sex, weight, and vitamin D.

## Clinically Meaningful Variants

Continuous prediction is primary. Diagnostic thresholds or categories require
measurement-, device-, protocol-, and population-compatible validation and are
not implied by this Task.

## Baselines And Ceilings

For V1→V2 evaluation, compare age/sex/BMI demographic floor, prior-value LOCF,
OLS on prior value plus demographics, and GBDT on the same inputs. Use one
cohort and split for every comparison.

## Benchmark-Track Evidence

OpenEvidence review and literature search support grip strength and objective
movement/activity as the cleanest independent BMD modalities beyond age, sex,
and BMI. PhenoBench therefore proposes V1 grip for both V1 and V2 BMD. Every
same-visit DXA/bone-density field remains excluded; the existing prior-BMD
rows are persistence references, not modality-addition tracks.

## Caveats

- Mask every same-visit DXA field, especially side/mean BMD, T/Z/young-adult references, and body-composition values; dose/metadata are never predictors.
- T/Z scores use age/sex reference information and are prohibited as predictors. Positioning, artifacts, device calibration, and bilateral averaging affect BMD.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns, target
quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Baim et al. (2008), ISCD official positions, <https://doi.org/10.1097/SMJ.0b013e31817a8b02>.
- Johnell et al. (2005), BMD and fracture prediction, <https://doi.org/10.1359/JBMR.050304>.
- HPP Research OS `bone_density` dataset documentation and QC inventory.
- Montgomery et al. (2024), objective activity and BMD,
  <https://doi.org/10.1093/jbmr/zjae017>.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=4716; train=3233, validation=753, test=730

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.224 | 0.114 | 0.485 |
| Linear | `linear` | 0.934 | 0.033 | 0.967 |
| Trees | `gbdt_delta_r2` | 0.931 | 0.034 | 0.965 |
| LOCF | `last_observation_carried_forward` | 0.926 | 0.035 | 0.965 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
