# Mean Bilateral Ankle Pressure Task Card

Status: draft

Task id: `mean_ankle_pressure`

Evidence status: grounded

Evidence reviewed: 2026-07-15

Benchmark status: complete

## Target

Mean Bilateral Ankle Pressure as a continuous participant-visit measurement.

Implementation facts:

- bodily system: cardiovascular/lipid
- target route: `vascular_health r_ankle_pressure + l_ankle_pressure`
- unit: mmHg
- device/acquisition: Viasonix Falcon cuff and PPG, supine
- construction/QC: require valid left and right values and non-failure QC; arithmetic bilateral mean per participant-stage
- valid range: each side 70-250 mmHg
- default stages: `00_00_visit` and `02_00_visit`
- paper fidelity: bilateral adaptation of the exact HealthFormer right-ankle endpoint

## Why This Matters

Ankle systolic pressure is a direct peripheral vascular measurement. The bilateral mean is not ABI and does not diagnose peripheral artery disease.

## Related HPP Measurements

ABI, side-specific ankle/brachial pressures, PWV, BP, symptoms, and cardiovascular risk factors.

## Clinically Meaningful Variants

Continuous prediction is primary. Diagnostic thresholds or categories require
measurement-, device-, protocol-, and population-compatible validation and are
not implied by this Task.

## Baselines And Ceilings

For V1→V2 evaluation, compare age/sex/BMI demographic floor, prior-value LOCF,
OLS on prior value plus demographics, and GBDT on the same inputs. Use one
cohort and split for every comparison.

## Caveats

- Mask the full same-visit vascular family, especially side pressures, brachial pressures, ABI ratios, and waveforms.
- Cuff technique, calcified/noncompressible arteries, body position, and device QC affect pressure; requiring both sides changes the cohort.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns, target
quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Thurston et al. (2019), ankle-brachial pressure-index review, <https://doi.org/10.1177/1708538119842395>.
- HPP Research OS `vascular_health` dataset documentation and QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=5348; train=3694, validation=851, test=803

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.156 | 19.395 | 0.398 |
| Linear | `linear` | 0.384 | 16.566 | 0.621 |
| Trees | `gbdt_delta_r2` | 0.387 | 16.520 | 0.623 |
| LOCF | `last_observation_carried_forward` | 0.149 | 19.468 | 0.597 |

<!-- healthformer-wave-evidence:end -->

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29. V1 Nightingale and fundus morphology are proposed
beyond age/sex/BMI. The complete same-visit BP, ABI/PWV/pressure, carotid, and
vascular-waveform families remain excluded. See
`04-cardiovascular-lipid.md`.

## v0 Final-Test Status

The classical release is complete: Ridge/logistic and GBDT are remotely verified on every approved exact cohort and rendered in the Figure 1 task deep dives. TabSwift is deferred until GPU execution is configured; it is not a missing or failed row.

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
