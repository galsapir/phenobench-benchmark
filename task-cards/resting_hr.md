# Resting ECG Heart Rate Task Card

Status: draft

Task id: `resting_hr`

Evidence status: grounded

Evidence reviewed: 2026-08-15

## Target

`resting_hr` predicts `ecg.hr_bpm`: heart rate in beats per minute from the
10-second resting 12-lead ECG acquired during the HPP clinical visit.

Implementation facts:

- Task: `RestingHrTask`
- target dataset: `ecg`
- target field: `hr_bpm`
- target source: None
- target unit: bpm
- default research stage: `00_00_visit`
- valid range: 30.0-130.0 bpm; a PhenoBench plausibility filter, not a clinical
  interval
- primary metric: `r2`
- Additional scalar metrics: `rmse`, `mae`, `pearson_r`, `spearman_r` when
  target and prediction are non-constant.

## Why This Matters

Diament 2023 used sleep-derived heart-rate / HRV features to predict resting
heart rate measured by 10-second ECG at the testing center. The paper reported
that sleep heart-rate features improved MAE from 7.13 bpm for age/sex/BMI to
5.19 bpm, with correlation 0.69.

The PhenoBench task represents the stable target. Paper-inspired configs attach
specific sleep-derived feature surfaces.

**What a row here does not support.** The target is a **clinic** resting heart
rate from a 10-second ECG at one visit. It is not a resting heart rate in the
physiological sense of a stable trait, not an overnight or ambulatory measure,
and not a cardiovascular risk estimate. A single 10-second acquisition in a
clinical setting carries white-coat and posture effects that an overnight
measurement does not.

**The setting is the whole subtlety on this Task, and the corpus already records
it.** Heart rate is a WatchPAT input channel, so a sleep or WatchPAT arm can
look like it is recomputing the target when it is not. The `cgm_sleep_ecg`
configs state the resolution in their `review.source_match_rationale`: the
target is a clinic resting heart rate read from the `ecg` dataset while a
WatchPAT arm reads an overnight `watchpat_hr` channel, so two heart-rate
measurements in two settings make a high score **cross-setting transfer rather
than derivation**. Anyone adding a heart-rate-bearing modality here should
declare the same way rather than leave a reader to infer it.

## Related HPP Measurements

Demonstrated in HPP and persisted in this repository, from
`docs/figure1/resting_hr_review.json`,
test split:

- V1 sleep + demographics reaches test R2 = 0.454 (95% CI [0.410, 0.495]) on a
  cohort of 9,382.
- V1 Nightingale + demographics reaches R2 = 0.127 (95% CI [0.094, 0.159]) on
  9,420.

The sleep result is the largest single-modality effect in the cardiovascular
family of cards, and it is the direction Diament et al. reported - overnight
heart-rate features carry most of the recoverable signal in a clinic ECG heart
rate. The gap to Nightingale metabolomics is large, but the two tracks are
**not** the same people: 9,382 against 9,420 participants under different
`cohort_id` hashes. Similar sizes do not establish common support, so read this
as an unmatched corpus comparison rather than a controlled contrast.

**Against the demographic floor both tracks clear**: sleep
**ΔR2 = +0.384 (95% CI [+0.343, +0.424])**, Nightingale
**+0.058 ([+0.034, +0.086])**. The sleep figure is a within-track margin, and it
is the informative one: almost the whole of that track's raw 0.454 is added
signal rather than floor, which is what makes the setting caveat load-bearing
rather than pedantic.

The two tracks sit on different cohorts (9,382 against 9,420), so sleep's larger
margin is not a paired comparison against Nightingale.

Read it with that caveat: part of that margin is two measurements of the same
physiological quantity in different settings, which is why the
`benchmark_claim` on those arms is transfer and not derivation.

**These are `reviewable` rows, not `final` ones.** Measured across the committed
leaderboards: all 787 rows carry `curation_state: reviewable` and none is
`final`. A complete fresh v0 re-run is committed to, so every figure in this
section is pre-re-run evidence that the re-run supersedes - persisted and citable
today, not a frozen result. **Which curation states the Figure 1 export accepts
is the export track's live question, not this card's**; read the two counts
above, not a gate.

## Clinically Meaningful Variants

**A categorical variant is not defensible on a single 10-second clinic
acquisition.** Bradycardia and tachycardia are defined at 60 and 100 bpm, which
are the closest things to fixed thresholds anywhere in this card set - but they
are clinical findings interpreted with symptoms, medication and context, not
labels applied to one research measurement. Three specific blocks:

- **Medication.** Beta blockers and rate-controlling drugs move heart rate
  directly, so a bradycardia bin would largely label treated participants. The
  Task does not model medication.
- **Fitness inverts the meaning.** A trained endurance athlete below 60 bpm is
  the healthy end of the distribution while a bradycardic patient is not, and
  nothing in the target distinguishes them.
- **Acquisition.** A 10-second clinic ECG with white-coat effect is not the
  resting condition the thresholds assume; the overnight channel discussed above
  would be closer, and it is a different measurement.

The continuous target stays primary. If a rhythm-abnormality Task is wanted, it
should come from a rhythm label rather than from a bin on this scalar.

## Baselines And Ceilings

The floor is a no-modality-feature baseline: `NoFeaturesPredictor` contributes
no modality features, and `DemographicFloorStrategy` fits age, sex, and BMI.

The Diament-inspired comparison config is:

```text
the internal evaluation configuration
```

It uses the stable-loader WatchPAT heart-rate summary fields:

- `heart_rate_mean_during_sleep`
- `heart_rate_min_during_sleep`
- `heart_rate_max_during_sleep`
- `heart_rate_mean_during_nrem`
- `heart_rate_mean_during_rem`
- `heart_rate_mean_during_wake`

These fields are averaged across baseline sleep nights before fitting.

The natural ceiling is the paper's broader HRV feature surface, not the current
stable-loader heart-rate summary row. Any sleep-feature claim should compare
against the demographic floor on matched support and state whether it is a
stable-loader analogue or a paper-faithful HRV route.

## Physiological Time-Series V1

the internal evaluation configuration
evaluates a multi-rate residual temporal encoder trained end-to-end on
target-blind actigraph, PAT-infrared, SpO2, and heart-rate windows from up to
three baseline WatchPAT nights. It retains the same clinic ECG target and
matched demographic floor. It remains paper-inspired because it does not
reproduce the paper's full 447-feature HRV surface.

This route is a target-adjacent pipeline positive control because nocturnal
heart rate is an input. On the exact 860-participant test support, the temporal
model reached R² 0.4408 and MAE 5.114 bpm. A train-only Ridge using sampled HR
mean/SD plus age/sex/BMI reached R² 0.4519 and MAE 5.198 bpm. Temporal minus
proxy delta-R² was -0.0111 (95% CI [-0.0400, +0.0164]); delta-MAE was
-0.084 bpm (95% CI [-0.227, +0.062]). This supports ingestion/training
validity, not a temporal-representation advantage.

## Caveats

This is not an exact Diament HRV replication. The paper feature group mainly
uses the broader HRV feature surface, including the `sleep_all_hrv` table and
the paper's 447-feature matrix. The stable PhenoBench config uses loader-exposed
heart-rate summaries only.

The exact HRV feature surface should become either a promoted loader key
(`sleep_hrv`) or an artifact-backed Predictor before claiming paper-faithful
replication.

Beating demographics is insufficient for this task. Every model claim must
also compare with a sampled-HR proxy on identical support.

ECG `hr_bpm` is a short resting measurement. It is affected by recent activity,
clinic context, medications, caffeine, arrhythmia, and measurement time. It is a
useful autonomic-tone target, not a complete cardiovascular endpoint.

## Metrics

Primary metric is R2. Secondary MAE in bpm is clinically interpretable and is
the easiest comparison to the Diament paper. Pearson and Spearman are useful
rank/linear diagnostics when target and prediction are non-constant.

## References

- Diament et al. 2023, "A Multimodal Dataset of 21,412 Recorded Nights for Sleep
  and Respiratory Research"
- Research OS paper-task run:
  `research_runs/phenobench-paper-task/diament_sleep_hr_2026_06_18/`

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29. V1 Nightingale and sleep are proposed beyond
age/sex/BMI. Sleep heart rate is deliberately retained as a target-adjacent
positive control and must be compared with the sampled-HR proxy; ECG inputs are
excluded. See
`04-cardiovascular-lipid.md`.

## v0 Final-Test Status

The classical release is complete: Ridge/logistic and GBDT are remotely verified on every approved exact cohort and rendered in the Figure 1 task deep dives. TabSwift is deferred until GPU execution is configured; it is not a missing or failed row.

## Open Questions

- Should loader-native HRV features be promoted so this can become a
  paper-faithful Diament route?
- Which medications or arrhythmia flags should be excluded or audited?
- Should clinic ECG resting HR be paired with sleep nocturnal-HR-dipping tasks?
