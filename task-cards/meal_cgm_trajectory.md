# Meal-Conditioned CGM Trajectory Task Card

Status: draft

Task id: `meal_cgm_trajectory`

Evidence status: grounded

Evidence reviewed: 2026-07-23

## Target

Predict nine absolute CGM values at exactly `0, 15, ..., 120` minutes after a
logged meal.

The frozen V2 target is linearly interpolated at those exact event-relative
timestamps from bracketing raw CGM readings exactly 15 minutes apart. Target
construction requires complete bracketing support at all nine coordinates.
Inputs may use only raw CGM strictly before `meal_start_utc`.

This supersedes the V1 nearest-bin label construction. Existing V1 metrics and
leaderboard rows are historical and are not directly comparable to V2.

## Why This Matters

Postmeal glucose response depends on both the meal and the participant's
recent metabolic context. A shared event-relative target with model-selected
history lets simple baselines and future Chronos-2 or GluFormer V2 adapters
compete on the same scoreable events without forcing one input representation
on every model.

## Evaluation Unit And Split

- Unit: one isolated logged meal, keyed by `evaluation_unit_id`.
- Anchor: `meal_start_utc`; `meal_start_local` preserves the
  `Asia/Jerusalem` view.
- CGM session: `connection_id`, not research stage alone.
- Split: participant, using `participant_id_split_v1`.
- Task `X`: event IDs.
- Target: absolute interstitial glucose in mg/dL.

All meals from one participant stay in one split. The Task does not require a
particular amount of premeal history. Predictor support determines which
events a model can serve.

## Normalized Artifact Bundle

The artifact path is a directory or S3 prefix containing:

1. `evaluation_meals.parquet`: event identity, participant, connection,
   UTC/local anchor, isolation/QC fields, target-meal nutrition, and nine
   targets.
2. `cgm_history.parquet`: deduplicated raw CGM keyed by participant,
   connection, and `timestamp_utc`, plus `timestamp_local` and `cgm_mg_dl`.
3. `meal_history.parquet`: historical context meals keyed by participant and
   connection. The target meal comes from `evaluation_meals` and need not be
   duplicated here.
4. `manifest.json`: schema version, units, table counts/digests, alignment
   policy, and target coordinates.

Participant IDs must be canonical UUID strings in real artifacts. Upstream
construction uses `hpp_data_loader` for normalization.

`connection_id` prevents CGM from separate sensor sessions in the same
participant/stage from mixing. Past meals are restricted to the target
connection and `[meal_start - history_window, meal_start)`.

The published immutable V2 bundle is:

```text
an internal artifact
```

It contains 259,040 evaluation events. A real-load audit found 258,421 events
(99.761%) with complete native two-hour history and 231,207 events (89.255%)
with at least 96 trailing contiguous native points inside a 120-hour window.
These are context-support counts, not model-submission counts.

## Model-Selected History

Predictors declare:

```text
history_window_hours
```

There is no parallel minute/day option.

- Simple baselines use `history_window_hours=2.0`.
- The intended Chronos-2 adapter policy uses
  `history_window_hours=120.0` (five days).

The shared context exposes two distinct views:

- `raw_cgm_history`: native sensor timestamps in
  `[meal_start - history_window, meal_start)`. This lets model adapters
  preserve native sensor phase.
- `aligned_cgm_history`: values interpolated at exact meal-relative
  15-minute coordinates using source readings from the same bounded history
  window. This is an optional strict event-grid view; an off-grid anchor can
  leave the earliest coordinate unavailable because readings before
  `meal_start - history_window` are never borrowed.

Neither view includes post-anchor source CGM. The target meal is returned
separately from earlier meals through an input-only allowlist; it never
contains `cgm_post_*` labels or target-derived diagnostics.

Baseline support requires a complete contiguous native sequence for its
selected window. The two-hour default therefore has eight points, but their
timestamps retain the sensor's native phase.
The intended Chronos-2 support policy for a five-day maximum requires at least
96 trailing native readings, each exactly 15 minutes apart, with the newest
reading no more than 15 minutes before the meal. An older contiguous block
does not qualify. Support decisions and reason counts are determined before
prediction and persisted as Predictor provenance.

## Task-Fixed Cohort

The Task accepts `history_window_hours` and `minimum_native_contiguous_points`
under the same names, and they do a different job: they fix which evaluation
units are eligible, and are reported in `benchmark_required_data_roles` as
`cgm_history:premeal_{h}h:min_contiguous_points={n}`. Both are `None` by
default, which fixes nothing and lets the Predictor's declared support define
the cohort.

The two sides are therefore not one value copied twice, and equality is not the
rule. A Task that fixes a cohort refuses a run whose Predictor support misses
any unit of it; a Task that fixes nothing narrows to whatever the Predictor
supports. A configuration holding `None` on the Task against `2.0` on the
Predictor is the normal shape.

## Meal Construction And Nutrition

Hagai/Smadar preprocessing owns food-log clustering and nutrient scaling.
Foods are joined to the per-100-g lookup, multiplied by `weight / 100`, and
summed within a meal.

The target meal and every historical meal expose:

| Field | Unit |
|---|---|
| `energy_kcal` | kcal |
| `carbohydrate_g` | g |
| `available_carb_g` | g |
| `protein_g` | g |
| `fat_g` | g |
| `fiber_g` | g |
| `sodium_mg` | mg |
| `caffeine_mg` | mg |
| `water_g` | g |
| `alcohol_g` | g |
| `total_sugars_g` | g |
| `n_food_items` | count |
| `n_distinct_foods` | count |

The lookup is imputed. Caffeine and alcohol have heavy real zero modes; zero
must not be reinterpreted as missing.

Both meal tables preserve `nutrition_qc_caffeine_implausible` (caffeine above
1000 mg) and `nutrition_qc_sugars_exceed_carbs` (total sugars above total
carbohydrate) as boolean audit fields. Evaluation-meal flags are persisted in
Task row metadata for QC-clean sensitivity scoring. They are not baseline
model features by default; raw nutrient values remain unchanged.

The bundle exposes raw CGM plus target/prior-meal nutrients for a future
Chronos-2 adapter; that adapter must rasterize meal events as covariates.
Original Chronos and Chronos-Bolt are target-series-only, and no canonical
Chronos-family submission exists yet. GluFormer V2 can additionally consume
caffeine, water, alcohol, and total sugars.

## Isolation And Leakage

- Immediate meal-isolation rules remain independent of model history.
- No other caloric event is allowed in `[-120, 0)` or outside the target
  meal's 30-minute cluster through `+120` minutes.
- Earlier meals outside that immediate interval remain available as model
  context.
- Logged meal time is the only anchor.
- Target-derived alignment, rise/peak filters, postmeal summaries, and future
  activity are forbidden inputs.
- Connection boundaries must be observed before an event is eligible.

Expanding `history_window_hours` never expands the meal-isolation interval.

## Baselines And Ceilings

The baseline Predictor selects two hours, produces eight native contiguous CGM
values in timestamp order, appends the target-meal fields, and emits a flat
feature matrix. Sequence Strategies must set `history_length` equal to the
Predictor's declared `history_points`, so the last-value baseline always uses
the final premeal reading. Longer windows are valid baseline configurations;
eight points are not part of the Task contract.

The baseline ladder remains last value, linear drift, train-mean response,
recursive ARX, multi-output ridge, and MLP. All V2 real scores must be rerun.

An artifact-mode last-value pipeline smoke using the one-shot
Predictor-to-Task bundle handoff completed without persistence in 46.37 seconds
at 2,983,580 KiB peak RSS (2.845 GiB). The Task verified an in-memory
fingerprint over the complete canonical evaluation-meal table before accepting
the handoff. Its supported cohort was 258,421
meals (619 excluded for incomplete native history), split into 178,699 train,
40,328 validation, and 39,394 test rows; all emitted prediction matrices had
nine coordinates. Test metrics were RMSE 19.1913, MAE 13.2149, early RMSE
17.6716, late RMSE 20.3255, peak-glucose MAE 21.7531, time-to-peak MAE 49.9572
minutes, iAUC MAE 1068.6529 mg/dL·min, participant-median RMSE 17.4997, and
participant-p90 RMSE 25.8095. This is implementation smoke evidence, not a
persisted canonical run or a V2 leaderboard score.

Chronos-2 adapters, GluFormer, and other external systems submit:

```text
evaluation_unit_id, sequence_coordinate, prediction
```

at exactly `0, 15, ..., 120`. A native-grid model must align its forecast to
these exact event-relative timestamps before submission. PhenoBench applies
the same split, scoring, persistence, and review path.

The meal-specific generated-sequence Predictor derives support from the V2
context bundle before the Task loads, independently of which prediction IDs
were submitted. It records the requested history, minimum contiguous-point
policy, support counts, and both context-manifest and prediction-artifact
digests. Test-only submissions may leave non-emitted train/validation rows as
NaN; the passthrough Strategy rejects non-finite predictions on every emitted
split. Prediction-file membership never shrinks the context-derived support
cohort.

## Metrics

- Primary: pooled pointwise RMSE in mg/dL.
- Secondary: pooled MAE; RMSE at 0–45 and 60–120 minutes; peak-glucose MAE;
  time-to-peak MAE; positive-iAUC MAE; participant RMSE median and p90.
- `participant_rmse_median` is a marginal summary of one Eval Run. A paired
  peer comparison is the median of participant-level RMSE differences, not the
  difference between two runs' marginal medians.
- Review: trajectory bands, horizon errors/bias, residual correlation,
  endpoint calibration, and private representative traces.

## Caveats

- Diet timing and quantity are self-reported.
- CGM is interstitial and noisy.
- Model-specific support can differ. Coverage and common-event intersections
  must accompany comparisons.
- Exact interpolation changes V1 labels by a scientifically meaningful amount;
  V1 results must not be relabeled as V2.
- Real V2 baseline and learned-model reruns remain required before this Task
  Card can become canonical.

## References

- Zeevi D, et al. *Cell*. 2015. <https://doi.org/10.1016/j.cell.2015.11.001>
- Berry SE, et al. *Nature Medicine*. 2020.
  <https://doi.org/10.1038/s41591-020-0934-0>
- Shilo S, et al. *European Journal of Epidemiology*. 2021.
  <https://doi.org/10.1007/s10654-021-00753-5>
- Rossman H, et al. CGM physical-activity preprocessing.
  <https://github.com/hrossman/cgm-physical-activity/tree/an internal digest>
- Amazon Science. Chronos forecasting model family; Chronos-2 documents
  covariate-informed forecasting.
  <https://github.com/amazon-science/chronos-forecasting>

## Open Questions

- Which minimum-history policy should each external model register?
- Which common-event intersection should be required when external models use
  policies stricter than the audited 120-hour/96-point support rule?
- Should prior-meal nutrition become a required input for any canonical
  external-model track?
