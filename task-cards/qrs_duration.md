# QRS Duration Task Card

Task id: `qrs_duration`

Evidence status: grounded

Evidence reviewed: 2026-07-15

Benchmark status: complete

## Target

QRS Duration as a continuous participant-visit measurement.

Implementation facts:

- bodily system: cardiovascular/lipid
- target route: `ecg.qrs_ms`
- unit: ms
- device/acquisition: Norav 1200HR, 10-second 12-lead ECG at 1 kHz
- construction/QC: participant-stage mean after ECG pipeline QC
- valid range: 50-250 ms broad plausibility guard
- default stages: `00_00_visit` and `02_00_visit`
- paper fidelity: paper-inspired ECG-family analogue

## Why This Matters

QRS duration measures ventricular depolarization time. Prediction does not diagnose bundle-branch block or ventricular disease.

## Related HPP Measurements

PR, QT/QTc, heart rate/RR, QRS axis/morphology, ECG diagnoses, medication, and electrolytes.

## Clinically Meaningful Variants

Continuous prediction is primary. Diagnostic thresholds or categories require
measurement-, device-, protocol-, and population-compatible validation and are
not implied by this Task.

## Baselines And Ceilings

For V1→V2 evaluation, compare age/sex/BMI demographic floor, prior-value LOCF,
OLS on prior value plus demographics, and GBDT on the same inputs. Use one
cohort and split for every comparison.

## Caveats

- Mask the full same-visit ECG family and waveform, especially QRS morphology/diagnoses and alternate duration fields.
- Automated interval boundaries, pacing, conduction disease, lead quality, and software changes affect QRS.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns, target
quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Kligfield et al. (2009), intraventricular-conduction ECG standardization, <https://doi.org/10.1161/CIRCULATIONAHA.108.191095>.
- HPP documentation `ecg` dataset documentation and QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=6833; train=4696, validation=1087, test=1050

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.141 | 10.733 | 0.385 |
| Linear | `linear` | 0.521 | 8.016 | 0.724 |
| Trees | `gbdt_delta_r2` | 0.530 | 7.945 | 0.728 |
| LOCF | `last_observation_carried_forward` | 0.420 | 8.818 | 0.708 |

<!-- healthformer-wave-evidence:end -->

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29. V1 Nightingale and sleep are proposed beyond
age/sex/BMI. The complete same-visit ECG family and waveform remain excluded.
See `04-cardiovascular-lipid.md`.

## v0 Final-Test Status

The classical release is complete: Ridge/logistic and GBDT are remotely verified on every approved exact cohort and rendered in the Figure 1 task deep dives.

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
