# PR Interval Task Card

Status: draft

Task id: `pr_interval`

Evidence status: grounded

Evidence reviewed: 2026-07-15

Benchmark status: complete

## Target

PR Interval as a continuous participant-visit measurement.

Implementation facts:

- bodily system: cardiovascular/lipid
- target route: `ecg.pr_ms`
- unit: ms
- device/acquisition: Norav 1200HR, 10-second 12-lead ECG at 1 kHz
- construction/QC: participant-stage mean after ECG pipeline QC
- valid range: 50-400 ms broad plausibility guard
- default stages: `00_00_visit` and `02_00_visit`
- paper fidelity: exact HealthFormer endpoint

## Why This Matters

PR interval measures atrial-to-ventricular conduction time. Prediction does not diagnose atrioventricular block or establish electrophysiologic disease.

## Related HPP Measurements

Heart rate, RR, QRS, QT/QTc, ECG axes/diagnostics, medication, and electrolytes.

## Clinically Meaningful Variants

Continuous prediction is primary. Diagnostic thresholds or categories require
measurement-, device-, protocol-, and population-compatible validation and are
not implied by this Task.

## Baselines And Ceilings

For V1→V2 evaluation, compare age/sex/BMI demographic floor, prior-value LOCF,
OLS on prior value plus demographics, and GBDT on the same inputs. Use one
cohort and split for every comparison.

## Caveats

- Mask the full same-visit ECG family and waveform, including all intervals, axes, diagnoses, and alternate PR aliases.
- Heart rate, autonomic tone, medication, conduction disease, and a documented analyzer software shift affect values.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns, target
quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Kligfield et al. (2007), ECG standardization, <https://doi.org/10.1161/CIRCULATIONAHA.106.180200>.
- HPP Research OS `ecg` dataset documentation and QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=6675; train=4574, validation=1071, test=1030

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.058 | 23.532 | 0.243 |
| Linear | `linear` | 0.672 | 13.881 | 0.820 |
| Trees | `gbdt_delta_r2` | 0.669 | 13.958 | 0.818 |
| LOCF | `last_observation_carried_forward` | 0.650 | 14.333 | 0.820 |

<!-- healthformer-wave-evidence:end -->

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29. V1 Nightingale and sleep are proposed beyond
age/sex/BMI. The complete same-visit ECG family and waveform remain excluded.
See `04-cardiovascular-lipid.md`.

## v0 Final-Test Status

The classical release is complete: Ridge/logistic and GBDT are remotely verified on every approved exact cohort and rendered in the Figure 1 task deep dives. TabSwift is deferred until GPU execution is configured; it is not a missing or failed row.

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
