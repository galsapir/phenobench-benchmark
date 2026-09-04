# Bilateral Thigh-to-Ankle Pulse-Wave Velocity Task Card

Task id: `thigh_ankle_pwv`

Evidence status: grounded

Evidence reviewed: 2026-07-15

Benchmark status: complete (longitudinal V1→V2 claim REJECTED — between-wave scale shift; excluded from headline aggregates; V1-only rescope tracked in #37)

## Target

Bilateral Thigh-to-Ankle Pulse-Wave Velocity as a continuous participant-visit measurement.

Implementation facts:

- bodily system: cardiovascular/lipid
- target route: `vascular_health bilateral thigh-to-ankle PWV`
- unit: m/s
- device/acquisition: Viasonix Falcon/PRO peripheral vascular protocol
- construction/QC: require valid left and right values and non-failure QC; arithmetic bilateral mean per participant-stage
- valid range: each side 1-20 m/s
- default stages: `00_00_visit` and `02_00_visit`
- paper fidelity: paper-inspired vascular analogue

## Why This Matters

Peripheral thigh-to-ankle PWV captures lower-extremity muscular-artery stiffness. It is not carotid-femoral or brachial-ankle PWV.

## Related HPP Measurements

Side-specific PWV, transit time/distance, ABI, ankle/brachial pressures, BP, age, and vascular risk factors.

## Clinically Meaningful Variants

Continuous prediction is primary. Diagnostic thresholds or categories require
measurement-, device-, protocol-, and population-compatible validation and are
not implied by this Task.

## Baselines And Ceilings

For V1→V2 evaluation, compare age/sex/BMI demographic floor, prior-value LOCF,
OLS on prior value plus demographics, and GBDT on the same inputs. Use one
cohort and split for every comparison.

## Caveats

- **The V1→V2 longitudinal claim is rejected and excluded from the headline aggregates.** On the paired cohort (n=2251, `ds.silverdb.abi_all`), the V2 mean is 1.63 m/s (~1.1 SD) below V1 with test-retest r=0.47. PWV physiologically increases with age, so this wrong-direction shift reflects the thigh-ankle PWV segment being discontinued in July 2023 (device/protocol change), not forecasting error; it fully explains LOCF R2 = -1.65. V1 and V2 are not like-for-like. A V1-only cross-sectional rescope is tracked in #37.
- Mask the full same-visit vascular family, including both PWV sides, distances, transit times, pressures, ABI, and waveform paths.
- The HPP segment was discontinued in July 2023. Method-specific central-PWV cutoffs must not be transferred to this peripheral segment.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns, target
quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Watahiki et al. (2020), thigh-ankle segment physiology, <https://doi.org/10.2147/VHRM.S284248>.
- Reference Values for Arterial Stiffness Collaboration (2010), method-specific PWV context, <https://doi.org/10.1093/eurheartj/ehq165>.
- HPP documentation `vascular_health` dataset documentation and QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=2250; train=1569, validation=353, test=328

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.149 | 1.311 | 0.390 |
| Linear | `linear` | 0.299 | 1.190 | 0.548 |
| Trees | `gbdt_delta_r2` | 0.255 | 1.226 | 0.507 |
| LOCF | `last_observation_carried_forward` | -1.652 | 2.314 | 0.504 |

<!-- healthformer-wave-evidence:end -->

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29. V1 Nightingale and fundus morphology are proposed
beyond age/sex/BMI, with all same-visit vascular/BP inputs excluded. Only the V1
target is eligible for v0 because the documented V1/V2 scale shift invalidates
the longitudinal comparison. See
`04-cardiovascular-lipid.md`.

## v0 Final-Test Status

The classical release is complete: Ridge/logistic and GBDT are remotely verified on every approved exact cohort and rendered in the Figure 1 task deep dives.

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
