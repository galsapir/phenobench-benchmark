# Liver Stiffness Task Card

Status: draft

Task id: `liver_stiffness`

Evidence status: grounded

Evidence reviewed: 2026-07-28

Benchmark status: complete

## Target

Liver Stiffness as a continuous participant-visit measurement.

Implementation facts:

- bodily system: hepatobiliary
- target route: `liver_ultrasound.r__elasticity`
- unit: kPa
- device/acquisition: Supersonic Aixplorer MACH 30 C6-1X 2D-SWE; not FibroScan
- construction/QC: participant-stage 2D-SWE elasticity; range filter; stability-index sensitivity audit where upstream Q-box fields are available
- valid range: 2-75 kPa
- default stages: `00_00_visit` and `02_00_visit`
- paper fidelity: paper-inspired analogue; HealthFormer exact liver target is attenuation

## Why This Matters

2D-SWE elasticity is a noninvasive liver-stiffness measurement related to fibrosis. Prediction does not stage fibrosis or diagnose cirrhosis.

## Related HPP Measurements

Attenuation, speed of sound, viscosity, Q-box duplicates/stability, liver enzymes, FIB-4, BMI, and alcohol.

## Benchmark-Track Evidence

OpenEvidence review found the strongest independent systemic evidence for
plasma metabolomic profiles, with DXA fat distribution as a secondary,
predominantly cross-sectional modality. Advanced-fibrosis studies support
metabolite signal beyond routine scores, while regional adiposity associates
with elastography-defined fibrosis beyond BMI. The fixed Nightingale panel
contains no AST, ALT, platelets, albumin, or liver-ultrasound input.

## V0 Benchmark Execution

The frozen same-visit V1→V1 matrix completed on 2026-07-29; this is distinct
from the longitudinal HealthFormer-inspired evidence below. All six v0 rows
are locally successful and remotely `FINISHED` in operational source.

- Nightingale: n=7,069; test=1,067; best R2=0.120 (Ridge), with paired
  delta R2 +0.018 [0.001, 0.035].
- DXA: n=8,600; test=1,286; best R2=0.106 (CPU TabSwift); Ridge's paired
  delta R2 was +0.017 [0.005, 0.030].
- Full rows and provenance:
  deep dive and
  aggregate review.

## Clinically Meaningful Variants

Continuous prediction is primary. Diagnostic thresholds or categories require
measurement-, device-, protocol-, and population-compatible validation and are
not implied by this Task.

## Baselines And Ceilings

For V1→V2 evaluation, compare age/sex/BMI demographic floor, prior-value LOCF,
OLS on prior value plus demographics, and GBDT on the same inputs. Use one
cohort and split for every comparison.

## Caveats

- Mask the full same-visit liver-ultrasound family, especially the exact Q-box elasticity duplicate and all raw Q-box values.
- Fasting, inflammation, congestion, cholestasis, operator/ROI, BMI, and device-specific cutoffs affect stiffness; attenuation measures steatosis, not stiffness.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns, target
quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Herrmann et al. (2018), biopsy-referenced 2D-SWE meta-analysis, <https://doi.org/10.1002/hep.29179>.
- Rinella et al. (2023), AASLD NAFLD practice guidance, <https://doi.org/10.1097/HEP.0000000000000323>.
- Caussy et al. (2019), serum metabolites and advanced fibrosis, <https://doi.org/10.1136/gutjnl-2018-317584>.
- Ciardullo et al. (2022), body-fat distribution and elastography-defined liver disease, <https://doi.org/10.1093/ajcn/nqac059>.
- HPP Research OS `liver_ultrasound` dataset documentation and QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=5307; train=3639, validation=838, test=830

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.101 | 1.301 | 0.319 |
| Linear | `linear` | 0.178 | 1.244 | 0.426 |
| Trees | `gbdt_delta_r2` | 0.181 | 1.242 | 0.428 |
| LOCF | `last_observation_carried_forward` | -0.011 | 1.380 | 0.379 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
