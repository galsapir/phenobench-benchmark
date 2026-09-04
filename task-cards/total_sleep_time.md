# Total Sleep Time Task Card

Task id: `total_sleep_time`

Evidence status: grounded

Evidence reviewed: 2026-07-19

Benchmark status: complete

## Target

Total Sleep Time as a continuous HPP scalar.

Implementation facts:

- bodily system: sleep physiology
- target route: `sleep.total_sleep_time`
- unit: hours
- acquisition: WatchPAT-300 home monitoring, three nights
- construction/QC: precomputed per-night `total_sleep_time` (seconds) divided by 3600 to hours, then participant-stage mean of valid nights; Standard QC (`ahi` non-null)
- valid range: 2-12 hours
- paper fidelity: exact HealthFormer input measurement; new endpoint row

## Why This Matters

TST is a clinically legible measure of sleep duration. Prediction does not establish sleep sufficiency, insomnia, or sleep need.

## Related HPP Measurements

Time in bed, study duration, wake and sleep-stage durations, efficiency, activity, questionnaires, and circadian timing.

## Clinically Meaningful Variants

Continuous prediction is primary. Population sleep-duration guidance (AASM and the Sleep
Research Society: at least 7 hours, with 7-9 hours appropriate for adults; slightly less in
older adults) is a health recommendation, not an individual sufficiency threshold or a
diagnosis: sleep need varies between people, and no quantitative TST cutoff defines insomnia.
Such guidance does not define a label in this Task.

## Baselines And Ceilings

For V1→V2 evaluation, compare age/sex/BMI demographic floor, prior-value LOCF, OLS on prior value plus demographics, and GBDT on the same inputs on one cohort/split.

## Caveats

- Mask the full same-visit sleep family, especially time-in-bed/study/wake/stage durations and efficiency.
- WatchPAT (peripheral arterial tonometry) estimates sleep rather than measuring PSG EEG stages and agrees only moderately with polysomnography; a single night's TST is only moderately reliable while averaging three nights raises reliability substantially (Gaines et al. 2015). The 2-hour floor is a validity guard, not a recommended sleep duration.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns, target
quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Kohn et al. (2025), HPP multi-night sleep phenotyping, <https://doi.org/10.1038/s41591-024-03481-x>.
- Diament et al. (2023), HPP WatchPAT-300 multi-night sleep dataset, <https://arxiv.org/abs/2311.08979>.
- Watson et al. (2015), AASM/SRS recommended sleep duration for adults, <https://doi.org/10.5664/jcsm.4950>.
- Gaines et al. (2015), short- and long-term stability of objective sleep measures, <https://doi.org/10.5665/sleep.5152>.
- Yalamanchali et al. (2013), WatchPAT validation meta-analysis, <https://doi.org/10.1001/jamaoto.2013.5338>.
- HPP documentation `sleep` dataset documentation and QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=4173; train=2857, validation=669, test=647

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.008 | 1.028 | 0.110 |
| Linear | `linear` | 0.244 | 0.898 | 0.494 |
| Trees | `gbdt_delta_r2` | 0.224 | 0.909 | 0.477 |
| LOCF | `last_observation_carried_forward` | 0.100 | 0.979 | 0.495 |

<!-- healthformer-wave-evidence:end -->

## v0 Final-Test Status

- Approved Benchmark Tracks predict V1 and V2 total sleep time from the exact
  V1 16-field diet panel plus age, sex, and BMI; no prior sleep value enters.
- Ridge and GBDT produced four remotely verified rows. Best held-out R² was
  0.044 at V1 and 0.017 at V2.
- Reported gain is over the matched demographic-only model. Prior-target LOCF
  consumes a different Allowed Information Set and remains a separate
  historical reference, not a floor inside these diet Tracks.
-  Full contract and results:
  `05-sleep-gut-aging.md`.

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
