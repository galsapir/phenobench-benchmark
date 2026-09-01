# Sleep Efficiency Task Card

Status: draft

Task id: `sleep_efficiency`

Evidence status: grounded

Evidence reviewed: 2026-07-19

Benchmark status: complete

## Target

Sleep Efficiency as a continuous HPP scalar.

Implementation facts:

- bodily system: sleep physiology
- target route: `sleep.sleep_efficiency`
- unit: %
- acquisition: WatchPAT-300 home monitoring, three nights
- construction/QC: mean valid nights within participant-stage; Standard-tier sleep QC (`ahi` non-null)
- valid range: 50-100%
- paper fidelity: exact HealthFormer endpoint

## Why This Matters

Sleep efficiency is `(total sleep time / time in bed) x 100` and captures sleep
continuity through both delayed sleep onset and time awake after onset. Prediction
does not diagnose insomnia or establish subjective sleep quality.

## Related HPP Measurements

TST, time in bed, wake/stage durations, AHI, ODI, SpO2, heart rate, and sleep
questionnaires are direct sleep relatives. Activity, CGM, psychological
questionnaires, medication, and menopause measures add cross-modal context.

## Clinically Meaningful Variants

The continuous measurement is primary. An 85% threshold is commonly used as a
descriptive or insomnia-treatment guide, but does not by itself define insomnia.
The standard denominator is time in bed; alternative sleep-episode denominators
would define a different target.

## Baselines And Ceilings

For V1→V2 evaluation, compare age/sex/BMI demographic floor, prior-value LOCF, OLS on prior value plus demographics, and GBDT on the same inputs on one cohort/split.

## Caveats

- Mask the full same-visit sleep family, especially TST/time-in-bed/wake/stage durations and percentages that reconstruct efficiency.
- WatchPAT (peripheral arterial tonometry) estimates sleep algorithmically rather than from PSG EEG stages and agrees only moderately with polysomnography; sleep efficiency is comparatively stable night-to-night versus stage-level metrics (Chouraki et al. 2022), and HPP averages three nights.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns, target
quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Kohn et al. (2025), HPP multi-night sleep phenotyping, <https://doi.org/10.1038/s41591-024-03481-x>.
- Diament et al. (2023), HPP WatchPAT-300 multi-night sleep dataset, <https://arxiv.org/abs/2311.08979>.
- Reed and Sacco (2016), sleep-efficiency denominator considerations,
  <https://doi.org/10.5664/jcsm.5498>.
- Perlis et al. (2022), insomnia assessment and treatment,
  <https://doi.org/10.1016/S0140-6736(22)00879-0>.
- Yalamanchali et al. (2013), WatchPAT validation meta-analysis, <https://doi.org/10.1001/jamaoto.2013.5338>.
- Chouraki et al. (2022), night-to-night variability of home sleep parameters, <https://doi.org/10.1093/sleep/zsac319>.
- HPP Research OS `sleep` dataset documentation and QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=4187; train=2867, validation=671, test=649

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.014 | 4.953 | 0.127 |
| Linear | `linear` | 0.454 | 3.685 | 0.679 |
| Trees | `gbdt_delta_r2` | 0.429 | 3.769 | 0.658 |
| LOCF | `last_observation_carried_forward` | 0.387 | 3.904 | 0.679 |

<!-- healthformer-wave-evidence:end -->

## v0 Final-Test Status

- Approved Benchmark Tracks predict V1 and V2 sleep efficiency from the exact
  V1 16-field diet panel plus age, sex, and BMI; no prior sleep value enters.
- Ridge and GBDT produced four remotely verified rows. Best held-out R² was
  0.019 at V1 and 0.015 at V2.
- Reported gain is over the matched demographic-only model. Prior-target LOCF
  consumes a different Allowed Information Set and remains a separate
  historical reference, not a floor inside these diet Tracks.
- TabSwift is deferred until GPU execution. Full contract and results:
  `05-sleep-gut-aging.md`.

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
- Cross-modal V1 value-add is tracked in
  [#28](https://github.com/PhenoAI/phenobench/issues/28).
- Objective/subjective discordance and night-variability surfaces are tracked in
  [#29](https://github.com/PhenoAI/phenobench/issues/29).
