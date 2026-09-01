# Corrected QT Interval Task Card

Status: draft

Task id: `qtc`

Evidence status: grounded

Evidence reviewed: 2026-07-15

Benchmark status: complete

## Target

Corrected QT Interval as a continuous participant-visit measurement.

Implementation facts:

- bodily system: cardiovascular/lipid
- target route: `ecg.qtc_ms`
- unit: ms
- device/acquisition: Norav 1200HR, 10-second 12-lead ECG at 1 kHz
- construction/QC: participant-stage mean; analyzer QTc is Bazett for approximately 99.7% of rows
- valid range: 300-650 ms broad plausibility guard
- default stages: `00_00_visit` and `02_00_visit`
- paper fidelity: paper-inspired analogue; HealthFormer exact target is raw QT

## Why This Matters

QTc adjusts ventricular repolarization duration for heart rate. Prediction does not diagnose long-QT syndrome or arrhythmia risk.

## Related HPP Measurements

Raw QT, RR/heart rate, QT formula, QRS/PR, medications, electrolytes, sex, and ECG diagnoses.

## Clinically Meaningful Variants

Continuous prediction is primary. Diagnostic thresholds or categories require
measurement-, device-, protocol-, and population-compatible validation and are
not implied by this Task.

## Baselines And Ceilings

For V1→V2 evaluation, compare age/sex/BMI demographic floor, prior-value LOCF,
OLS on prior value plus demographics, and GBDT on the same inputs. Use one
cohort and split for every comparison.

## Physiological Time-Series V1

the internal evaluation configuration evaluates
a multi-rate residual temporal encoder trained end-to-end on target-blind
actigraph, PAT-infrared, SpO2, and heart-rate windows from baseline WatchPAT
nights against baseline clinic ECG QTc. The predictor contains no ECG waveform
or interval field. This same-visit cross-modal association probe does not
predict future repolarization or replace ECG. It is cross-sectional and must
not be compared numerically with the longitudinal V1→V2 rows below.
Its cheap comparator is same-support age/sex/BMI; valid-night count was audited
and was essentially uncorrelated with QTc, so LOCF is neither available nor
appropriate for this construct.

Held-out cross-sectional exploratory result (test n=860): temporal R² 0.0892
versus tuned age/sex/BMI R² 0.0836, delta-R² +0.0056 (95% CI
[-0.0343, +0.0463]); temporal MAE 16.4965 versus 16.4526 ms, delta-MAE
+0.0440 ms (95% CI [-0.3845, +0.4446]). Both comparisons are
consistent with a tie.

## Caveats

- Mask the full same-visit ECG family and waveform, explicitly raw QT, RR, heart rate, formula, and any recomputed QTc.
- Bazett over/under-corrects at extreme heart rates; sex, medication, electrolytes, and analyzer rules affect interpretation.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.
- The physiological time-series route and the V1→V2 execution table answer
  different questions and use different cohorts; they are non-rankable.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns, target
quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Vink et al. (2018), QTc interpretation, <https://doi.org/10.1161/CIRCULATIONAHA.118.033943>.
- HPP Research OS `ecg` dataset documentation and QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=6826; train=4689, validation=1087, test=1050

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.060 | 21.220 | 0.252 |
| Linear | `linear` | 0.280 | 18.574 | 0.532 |
| Trees | `gbdt_delta_r2` | 0.291 | 18.428 | 0.541 |
| LOCF | `last_observation_carried_forward` | 0.021 | 21.659 | 0.520 |

<!-- healthformer-wave-evidence:end -->

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29. V1 Nightingale and sleep are proposed beyond
age/sex/BMI. ECG QT/RR/heart rate, all other ECG fields, and the waveform remain
excluded to prevent formula reconstruction. See
`04-cardiovascular-lipid.md`.

## v0 Final-Test Status

The classical release is complete: Ridge/logistic and GBDT are remotely verified on every approved exact cohort and rendered in the Figure 1 task deep dives. TabSwift is deferred until GPU execution is configured; it is not a missing or failed row.

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
