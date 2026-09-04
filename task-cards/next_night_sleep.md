# Next-Night Sleep Task Card

Task id: `next_night_sleep`

Evidence status: grounded

Evidence reviewed: 2026-08-15

## TaskSpec v0

Evaluation unit:

- one participant prior-day diet / next-night WatchPAT sleep row
- canonical key: `evaluation_unit_id`
- current artifact grain:
  `participant_id + diet_local_date + sleep_night_date + night + collection timestamp + ordinal`

Required artifact columns:

- `participant_id`
- `evaluation_unit_id`
- `phenobench_split`
- `diet_local_date`
- `sleep_night_date`
- `target_mean_sleeping_heart_rate_bpm`

Current protocol:

- anchor: `sleep_night_date`
- input window: diet/activity/context from `diet_local_date`, the day before sleep
- label window: next-night WatchPAT physiology
- split unit: participant
- split column: `phenobench_split`
- default held-out split: test
- Task input: `evaluation_unit_id`
- tabular floor: `NextNightSleepFeaturePredictor` + `RidgeStrategy`

Artifact-mode `feature_columns` is required by `NextNightSleepFeaturePredictor`.
The Task owns rows, labels, splits, and evaluation-unit ids. The Predictor owns
the feature set. The artifact carries labels, negative controls, temporal audit
fields, split metadata, and same-night sleep fields in one table, so automatic
numeric feature discovery would make leakage a schema accident.

If the artifact bundle ships a `column_manifest.csv`, set
`predictor.kwargs.column_manifest_path` as well. Selected feature columns must
be marked `predictor_input`; columns marked `target`, `readout`, `exposure`,
`prediction`, `future`, `fold`, or `provenance` fail before feature-matrix
construction.

Forbidden feature families:

- all `target_*` sleep labels
- all `negctrl_*` outcomes
- target-night sleep audit fields such as `sleep_start_time_il`
- same-night sleep/QC fields such as `ahi`, `tst_min`, `quality_score_heart_rate`
- split, identity, and evaluation-unit audit fields

Previous-night sleep fields are pre-anchor fields in the current artifact spec.
They are not blanket-forbidden by the Task, but the first private artifact
config excludes them and uses diet/activity/baseline context only.

## Target

Implementation facts:

- target field: `target_mean_sleeping_heart_rate_bpm` (the `DEFAULT_TARGET_FIELD`
  in `phenobench/event_artifacts/next_night_sleep.py`; constructor-overridable)
- target dataset: `next_night_sleep_participant_nights`
- target source: `materialized_artifact`. A row-level S3 artifact is what it is
  built from, not the declared source
- target unit: `bpm` on the class - **correct only for the default target
  field.** The runnable suite below also carries percentages, minutes and
  seconds, and the ClassVar does not change with `target_field`, so do not read
  the unit off the Task when running another target
- primary metric: R2
- secondary metrics: RMSE, MAE, Pearson r
- config: the internal evaluation configuration

Additional supported target fields in the artifact:

- `target_sleep_efficiency_pct`
- `target_total_sleep_time_min`
- `target_deep_sleep_pct`
- `target_rem_sleep_pct`
- `target_light_sleep_pct`
- `target_sleep_latency_sec`
- `target_waso_sec`

Current runnable target suite:

- `target_mean_sleeping_heart_rate_bpm`
- `target_total_sleep_time_min`
- `target_sleep_efficiency_pct`
- `target_sleep_latency_sec`
- `target_waso_sec`
- `target_deep_sleep_pct`
- `target_rem_sleep_pct`
- `target_light_sleep_pct`

The same Task/config surface can run any target in this suite by setting
`task.kwargs.target_field` and `predictor.kwargs.target_field` in the private
artifact YAML or through `phenobench run --set`. All targets share the same
participant-night rows, split semantics, leakage guards, and regression
metrics. Feature-set variants are Predictor configs over the same Task.

## Why This Matters

This task tests cross-time, cross-system relations: whether prior-day diet and
baseline context can predict next-night sleep physiology. It is the next
temporal PhenoBench lane after meal-level PPGR because it exercises repeated
participant-night units, participant-level splitting, future-field leakage
policy, and row-level evaluation ids without adding a broad temporal platform.

The strongest source anchor is sleeping heart rate: the Shkolnik/HPP documentation
scorecard preserves fiber and whole-plant associations with overnight HR better
than several other sleep outcomes.

This PhenoBench task is predictive. It is not the Shkolnik target-trial
emulation and does not estimate causal effects.

**What a row here does not support.** A predicted next-night value is a
next-day association across participant-nights. It is not a causal statement
that changing prior-day diet or activity changes sleep, not a sleep-disorder
diagnosis, and not a clinical recommendation. The causal question has a separate
design - the target-trial emulation this Task deliberately is not.

## Related HPP Measurements

Demonstrated in HPP and persisted in this repository, from
an internal review record,
test split:

- Prior-day diet reaches test R2 = 0.149 (95% CI [0.115, 0.181]) on 29,642
  participant-nights.
- Prior-day wearable activity reaches R2 = 0.113 (95% CI [0.078, 0.145]) on
  18,242.
- Prior-day diet + wearable activity reaches R2 = 0.135 (95% CI [0.097, 0.168])
  on the same 18,242 as activity alone.

**All three tracks clear their own matched demographic floor.** Diet + activity
reaches **ΔR2 = +0.155 (95% CI [+0.121, +0.187])**, diet alone
**+0.109 ([+0.089, +0.129])**, and activity alone
**+0.067 ([+0.039, +0.095])**.

The diet-only arm sits on a different cohort: it scores 29,642 nights while both
wearable-bearing arms score 18,242, because requiring wearable data drops about
38% of the nights. A within-track delta corrects each model for its own
demographic floor, but it does **not** create a paired diet-versus-combination
comparison across those cohorts. The combination has the largest persisted
within-track margin; whether it beats diet alone remains untested on common
support. Activity alone and the combination do share support, but the snapshot
does not persist a paired model-versus-model interval for their difference.

**These n values are participant-nights, not participants.** Rows are repeated
within person, splitting is participant-level, and an R2 computed across
correlated nights is not comparable to a participant-level R2 elsewhere in this
card set.

Proposed rather than shown: that any of this reflects a dietary or activity
effect on sleep rather than shared participant structure. The paired margins
above are associations across participant-nights, and the causal question has
its own design.

**These are `reviewable` rows, not `final` ones.** Measured across the committed
leaderboards: all 787 rows carry `curation_state: reviewable` and none is
`final`. A complete fresh v0 re-run is committed to, so every figure in this
section is pre-re-run evidence that the re-run supersedes - persisted and citable
today, not a frozen result. **Which curation states the Figure 1 export accepts
is the export track's live question, not this card's**; read the two counts
above, not a gate.

## Clinically Meaningful Variants

**Some targets in this suite have clinical thresholds and the Task should still
not bin them.** Sleep efficiency below 85% is a common insomnia-research
convention and total sleep time under 7 hours is a public-health guideline
boundary, but both are stated for habitual sleep assessed over time, not for a
single night - and this Task's unit of analysis is one night.

Three blocks, in order of how much they matter here:

- **A one-night bin is not the clinical construct.** Sleep guidelines and
  insomnia criteria describe habitual patterns and, for insomnia, daytime
  consequences and persistence over weeks. A single night below a cutoff is
  ordinary variation for most people.
- **The device defines the value.** Efficiency, WASO, latency and stage
  percentages are scoring-algorithm outputs, and thresholds set on
  polysomnography do not carry to a home wearable's staging without validation
  this repository has not done.
- **The default target has no threshold at all.** Mean sleeping heart rate,
  the runnable default, has no clinical cutoff - which is part of why it is the
  default.

A habitual variant - aggregating nights per participant before scoring - is the
defensible route to a categorical sleep Task, and it is a different Task with a
different unit of analysis, not a bin on these rows.

## Baselines And Ceilings

The current runnable floors are Ridge on Predictor-supplied feature sets:

- full floor: diet + baseline activity/context
- diet-only floor: diet composition/timing only
- activity-context floor: self-reported baseline/lifestyle activity minutes
- wearable-activity floor: prior-day `activity_daily` wearable/app rollups

The activity-context floor is not true day-N wearable activity. The
wearable-activity floor is the first true day-level activity -> sleep feature
artifact. It uses wearable/app rollups, not raw minute/event windows.

Meaningful claims should clear this simple tabular floor using the same
participant split and evaluation-unit universe. Stronger comparators can add
multimodal embeddings or modality-specific predictors, but must not move the
split, target, or feature leakage boundary.

For Adva handoff, the stable contract is: use the same `evaluation_unit_id`
rows/splits, use allowed pre-anchor raw windows or embeddings, and predict the
configured `target_*` sleep value. External predictions can be scored through a
submitted-prediction artifact keyed by `evaluation_unit_id`. The template config
is the internal evaluation configuration.

To export the full train/validation/test row contract:

```bash
uv run --extra hpp python scripts/export_next_night_sleep_submission_contract.py \
  an internal artifact \
  an internal artifact
```

To export only the final scored test rows:

```bash
uv run --extra hpp python scripts/export_next_night_sleep_submission_contract.py \
  an internal artifact \
  an internal artifact \
  --eval-split test
```

The exported contract table carries row keys, split labels, temporal anchors,
and `y_true`. The submitted prediction artifact should be a separate
`evaluation_unit_id` -> `y_pred` table.

The current uploaded contracts live at:

- `an internal artifact`
- `an internal artifact`
- `an internal artifact`
- `an internal artifact`

The all-splits contract has 29,642 HR-target-complete rows, 9,525
participants, zero duplicate `evaluation_unit_id` values, split counts train
20,393 / validation 4,671 / test 4,578, and parquet SHA-256
`an internal digest`.

The test-only contract has 4,578 test rows, 1,458 participants, zero duplicate
`evaluation_unit_id` values, and parquet SHA-256
`an internal digest`.

## Caveats

- AHI is out of scope for this Task.
- `sleep_start_time_il` uses WatchPAT `collection_timestamp`.
- Sleep end is not available from the loader-backed Shkolnik source; do not
  invent it.
- Participant IDs are UUID strings in this artifact. HPP namespace normalization
  belongs upstream in `hpp_data_loader`, not in generic Predictors.
- The S3 artifact is private and must not be committed.
- The row-level artifact is larger than the paper freeze: 29,647 person-nights
  from 9,526 participants vs paper 4,793 person-nights.
- Causal scorecard anchors and PhenoBench predictive scores are different
  evidence types.

## Metrics

- Primary: R2 on the configured held-out split.
- Secondary: RMSE, MAE, Pearson r.
- Audit views: split counts, participant counts, target missingness,
  duplicate evaluation-unit ids, and manifest checksums.

## Verifier Surface

Minimum verifier checks:

- required bundle files exist
- `checksums/SHA256SUMS` passes, including the parquet
- row count = 29,647
- participant count = 9,526
- duplicate `evaluation_unit_id` count = 0
- split counts:
  - train: 20,398
  - validation: 4,671
  - test: 4,578
- target missingness matches `manifest/target_missingness.csv`
- row-computable scorecard anchors match current artifact values
- causal anchors are explicitly labelled as not row-verifiable

Verifier command:

```bash
uv run --extra hpp python scripts/verify_next_night_sleep_artifact.py \
  an internal artifact \
  --provenance-out the internal evaluation configuration \
  --include-predictor-artifact
```

Use `--include-predictor-artifact` only for feature Predictor configs where
the Predictor reads the same verified parquet as the Task. Omit it for
submitted-prediction configs, where the Predictor artifact is the submission
file.

Local verified copy used in this session:

```bash
uv run python scripts/verify_next_night_sleep_artifact.py \
  /tmp/shkolnik_sleep_task_v2026_06_03 \
  --provenance-out /tmp/phenobench-next-night-sleep-artifact-provenance.json \
  --include-predictor-artifact
```

Verifier-backed private configs attach
`/tmp/phenobench-next-night-sleep-artifact-provenance.json` through
`persistence.artifact_provenance_path`, so their run manifests carry verifier
and artifact evidence. The wearable activity builder artifact has its own build
provenance and is not covered by this verifier path.

## Private Artifact Validation

On 2026-06-03, the bundle at
`an internal artifact` passed checksum,
count, split, missingness, and row-anchor verification.

PhenoBench private artifact validation commands:

```bash
uv run --extra hpp phenobench run \
  the internal evaluation configuration \
  --no-predictions

uv run --extra hpp phenobench run \
  the internal evaluation configuration \
  --no-predictions

uv run --extra hpp phenobench run \
  the internal evaluation configuration \
  --no-predictions

uv run --extra hpp python scripts/build_next_night_wearable_activity_sleep_artifact.py \
  an internal artifact \
  an internal artifact

uv run --extra hpp phenobench run \
  the internal evaluation configuration \
  --no-predictions

uv run --extra hpp python scripts/export_next_night_sleep_submission_contract.py \
  an internal artifact \
  an internal artifact

uv run --extra hpp python scripts/export_next_night_sleep_submission_contract.py \
  an internal artifact \
  an internal artifact \
  --eval-split test
```

Run shape:

- rows after HR target completeness filter: 29,642
- train rows: 20,393
- validation rows: 4,671
- test rows: 4,578

Ridge on the whitelisted full diet/activity/context matrix produced:

- R2: `0.17314358205201197`
- Pearson r: `0.4169137561679564`
- RMSE: `7.246793791368403`
- MAE: `5.714542167026927`

Ridge on the diet-only matrix produced:

- R2: `0.02940665670891951`
- Pearson r: `0.17352184032733942`
- RMSE: `7.851443448528947`
- MAE: `6.153020498840096`

Ridge on the activity-context matrix produced:

- R2: `0.045928049349985844`
- Pearson r: `0.21843789384853896`
- RMSE: `7.784333191795299`
- MAE: `6.131290524457683`

The wearable-activity artifact is uploaded at:

- `an internal artifact`
- `an internal artifact`

Artifact shape:

- rows: 29,647
- participants: 9,526
- duplicate evaluation-unit ids: 0
- split rows: train 20,398; validation 4,671; test 4,578
- rows with at least one wearable/app activity feature: 18,246
- parquet SHA-256:
  `an internal digest`

Ridge on the wearable-activity matrix produced a prediction-persisting
validation run:

- R2: `0.00926178342431061`
- Pearson r: `0.0968556888075241`
- RMSE: `7.93250419778403`
- MAE: `6.235871995712132`

The submitted-prediction handoff was validated with the uploaded test contract by
creating a toy `y_true + 0.1` prediction sidecar and scoring
the internal evaluation configuration. The evaluation produced R2 `0.9998425515844614`, RMSE `0.1`, and
`n_eval=4578`.

This validates the PhenoBench task/config path on the private row-level
artifact. It does not reproduce the Shkolnik causal target-trial analysis;
that gap is tracked in GitHub issue #90.

Target-suite Ridge baselines on the same rows/split/feature allowlist:

| Target | R2 | Pearson r | RMSE | MAE | Test rows |
|---|---:|---:|---:|---:|---:|
| `target_mean_sleeping_heart_rate_bpm` | 0.173144 | 0.416914 | 7.246794 | 5.714542 | 4,578 |
| `target_total_sleep_time_min` | 0.015244 | 0.128777 | 51.576650 | 41.379601 | 4,578 |
| `target_sleep_efficiency_pct` | 0.023017 | 0.156820 | 4.601467 | 3.588636 | 4,578 |
| `target_sleep_latency_sec` | 0.002411 | 0.054306 | 413.227151 | 336.064929 | 4,578 |
| `target_waso_sec` | 0.022183 | 0.153442 | 1243.777456 | 943.349878 | 4,578 |
| `target_deep_sleep_pct` | 0.040342 | 0.206258 | 4.998524 | 3.961079 | 4,556 |
| `target_rem_sleep_pct` | 0.017607 | 0.138307 | 7.093781 | 5.694971 | 4,556 |
| `target_light_sleep_pct` | 0.032095 | 0.185216 | 9.894463 | 7.913819 | 4,556 |

Sleeping HR remains the strongest first benchmark. The other targets are valid
task variants, but the baseline signal is modest.

## References

- `docs/sessions/2026-06-03-shkolnik-sleep-task-ingest.md`
- `an internal artifact`
- `an internal artifact`
- <https://github.com/mashaashkolnik/causal_framework>

## v0 Final-Test Status

- Three approved Benchmark Tracks use prior-day diet, prior-day wearable
  activity, or their union to predict next-night mean sleeping heart rate.
- Ridge and GBDT produced six remotely verified rows on checksum-bound,
  participant-held-out event cohorts. Best held-out R² values were 0.149,
  0.113, and 0.135.
- Their gain is relative to the matched demographic-only model. Previous-night
  sleep would change the Allowed Information Set and therefore belongs in a
  separate Benchmark Track or reference, not inside these three Tracks.
-  Full contract and results:
  `05-sleep-gut-aging.md`.

## Open Questions

- Should sleep efficiency or total sleep time get committed sibling private
  configs, or should the target suite stay documented as `target_field`
  variants on one private config?
- Should previous-night sleep become a separate future Benchmark Track or
  reference?
- Should verifier bundles become a first-class convention across temporal Tasks?
- Should a higher-resolution raw wearable activity window artifact be added
  after the day-level rollup task lands?
