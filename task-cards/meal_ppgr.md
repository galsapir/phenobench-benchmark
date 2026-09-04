# Meal-Anchored PPGR Task Card

Task id: `meal_ppgr`

Evidence status: grounded

Evidence reviewed: 2026-08-15

## TaskSpec v0

Evaluation unit:

- one logged meal
- canonical key: `evaluation_unit_id`
- fallback key construction:
  `participant_id|meal_id|meal_start`

Required artifact columns:

- `participant_id` or HPP UUID alias `participant_uuid`
- `meal_start`
- `ppgr_iauc_0_120`

Optional but preferred artifact columns:

- `meal_id`
- `participant_day`
- `time_block`
- `evaluation_unit_id`

The larger-HPP support artifact uses `target_ppgr` and `meal_anchor_time` as
source-column aliases for the same PPGR 0-120 scoring surface.

Current protocol:

- anchor: logged meal time
- label: 0-120 minute PPGR iAUC after the meal anchor
- default split unit: participant
- default split seed: `participant_id_split_v1`
- non-participant split units require explicit opt-in and are annotated as
  participant-leakage-risk protocol variants
- default held-out split: test
- Task input: `evaluation_unit_id` array
- tabular baseline Predictor: explicit pre-activity feature whitelist
- default tabular activity policy: activity-blind
- missing feature handling: train-split median imputation inside Ridge-family Strategies
- runnable floor: `MealPpgrPreActivityFeaturePredictor` + `RidgeStrategy`

Approved v0 tracks on the checksum-bound normalized trajectory bundle:

- two-hour raw premeal CGM
- the same raw premeal CGM plus target-meal diet

Each track ranks Ridge and GBDT.

Both v0 tracks use the same nutrition-complete logged-meal population exposed
by the pinned normalized bundle. “CGM-only” means target-meal diet is withheld
from the Predictor; it does not mean diet-incomplete meals are eligible. This
keeps the diet-addition comparison paired on identical events and limits the
standalone CGM claim to nutrition-complete loggers.

The first Predictor uses the eight native 15-minute CGM observations directly.
It may append the 13 target-meal nutrition fields. Baseline/slope and IGLU
summaries are Predictor choices, not the Allowed Information Set.

Artifact-mode Predictor `feature_columns` is required. This is the main leakage guard:
the artifact may contain labels, post-meal readouts, alignment fields,
predictions, and exploratory activity columns, but only explicitly whitelisted
numeric columns enter the Predictor output.

If the artifact bundle ships a `column_manifest.csv`, set
`predictor.kwargs.column_manifest_path` as well. Selected feature columns must
be marked `predictor_input`; columns marked `target`, `readout`, `exposure`,
`prediction`, `future`, `fold`, or `provenance` fail before feature-matrix
construction.

Forbidden feature families:

- PPGR / iAUC / AUC / response shape fields
- post-meal CGM summaries
- future or next-meal fields
- response-derived alignment or correction fields
- activity, step, energy, distance, MET, and heart-rate fields for
  activity-blind runs
- post-anchor activity windows for pre-anchor activity runs

## Target

Meal-level regression of postprandial glucose response after a logged meal.

Implementation facts:

- target field: `ppgr_iauc_0_120` (the `DEFAULT_TARGET_FIELD` in
  `phenobench/event_artifacts/meal_ppgr.py`; constructor-overridable)
- target dataset: `meal_level_cgm_diet` - a materialized meal-level CGM/diet
  artifact, or synthetic smoke data
- target source: `materialized_artifact`. The logged meal anchor table is what
  the artifact is built from, not the declared source
- target unit: mg/dL·min (incremental area under the curve, so a rate-times-time
  quantity rather than a concentration)
- default research stage: not applicable
- valid range: not yet enforced
- primary metric: R2
- anchor: logged meal time
- label window: 0-120 minutes after meal anchor
- default split unit: participant
- default split seed: `participant_id_split_v1`
- private artifact config:
  the internal evaluation configuration
- public CGMacros artifact config:
  the internal evaluation configuration

## Why This Matters

This task tests whether PhenoBench can express a temporal clinical evaluation:
predict a future post-meal glycemic response from information available before
the post-meal interval.

The useful manuscript asset is not only that post-meal steps are associated
with lower PPGR. The stronger PhenoBench asset is a leakage-sensitive,
meal-anchored prediction frame that can rank high-response meal occasions before
post-meal behavior is observed.

This task can support activity-blind or pre-activity PPGR prediction. It cannot
by itself support a claim that recommending movement after a meal causes lower
PPGR.

**What a row here does not support.** A predicted iAUC is a meal-level
association under free-living conditions. It is not a dietary recommendation,
not evidence that acting on the prediction changes glycemia, and not a clinical
endpoint. The distinction matters more here than on a laboratory target, because
the obvious application - telling someone which meals to avoid - is an
intervention claim, and interventions are established by trials.

## Related HPP Measurements

Demonstrated in HPP:

- **A personalised PPGR-targeting diet beat a Mediterranean diet on glycemic
  control in a randomised trial.** Ben-Yacov et al. randomised 225 adults with
  prediabetes to a Mediterranean or a PPT diet driven by a machine-learning
  predictor over clinical and microbiome features, over 6 months with 6 months
  of follow-up (Ben-Yacov et al. 2021). That trial is what an intervention claim
  looks like, and it is the reason a row here must not be reported as one: the
  trial tested acting on predictions, this Task tests making them.
- CGMap provides the HPP reference distribution for CGM-derived measures in
  non-diabetic individuals, which is the population this artifact's meals sit in
  (Keshet et al. 2023).

**The committed track clears its demographic floor by a wide margin**: premeal
CGM + target-meal diet reaches
**ΔR2 = +0.170 (95% CI [+0.159, +0.180])** on n = 9,550 meals, with a very tight
interval because the unit of analysis is a meal and there are many of them. Note
that is a per-meal interval, not a per-participant one, so it is not comparable
to the participant-level intervals elsewhere in this card set.

Proposed rather than shown, and the honest state of the target itself: HPP work
in preparation analyses >75,000 postprandial responses from >4,000 adults and
argues that conventional summary metrics miss temporal structure that
multi-scale representations recover. That is a manuscript in preparation with no
DOI, so it is a reason to keep the summary-metric question open rather than
evidence to cite - see Open Questions.

## Clinically Meaningful Variants

**A categorical "high responder" variant is the obvious extension and it does
not have a threshold to inherit.** Postprandial iAUC has no diagnostic cutoff:
the quantity depends on the label window (this Task uses 0-120 minutes), the
baseline convention, the sensor, and the meal itself, so any bin is defined
relative to the cohort's own distribution rather than to a clinical standard.
A "high PPGR meal" is a percentile statement about these meals, and it must be
reported as one.

Two Task-specific reasons a bin would mislead:

- **The unit of analysis is a meal, not a person.** A threshold on meal-level
  iAUC mixes within-person variation with between-person variation, so the same
  cutoff labels a metabolically healthy participant's large meal and an impaired
  participant's ordinary one identically.
- **The intervention framing rides on the bin.** Once meals are labelled
  high/low, a row reads as a recommendation engine, which is exactly the claim
  the non-claim above refuses and the Ben-Yacov trial actually tested.

Ranking, which the Task already supports, is the defensible categorical-adjacent
output: it orders meal occasions without asserting a clinical boundary.

## Baselines And Ceilings

The current runnable floor is `MealPpgrPreActivityFeaturePredictor` plus
`RidgeStrategy`. The Task supplies meal event IDs; the Predictor aligns
explicitly whitelisted pre-activity tabular features to those IDs.

Meaningful model claims should clear simple tabular pre-activity baselines:
meal composition, meal timing, pre-meal CGM state, and basic participant
phenotype. Stronger comparators include participant-grouped RidgeCV and a
materialized activity-blind PPGR prediction model trained out-of-fold by
participant.

For the post-meal activity paper lineage, the reusable S17 score is the
`glycemic_labs` activity-blind ridge model. For the newer HPP meal-PPGR
benchmark, `habitual_cgm` is the stronger no-activity baseline but carries a
different same-era CGM leakage concern and should be claimed separately.

MMFM-backed temporal Predictors should follow
`docs/walkthroughs/mmfm-temporal-predictor-contract.md`.

## Caveats

- `ppgr_iauc_0_120` is label-only. It must never enter features, covariates,
  predictor outputs, embeddings, or split keys.
- Post-meal CGM-derived fields are label/readout fields, not inputs.
- Activity-blind runs must exclude all activity fields.
- Artifact-mode tabular Predictors require an explicit feature whitelist.
  Automatic numeric feature discovery is allowed only for synthetic smoke data.
- Pre-activity runs may use only activity windows ending at or before the meal
  anchor.
- Exclude post-meal activity, future activity, active energy, distance, heart
  rate, next-meal timing, and response-derived alignment fields.
- Corrected meal-time alignment can be useful for measurement-error sensitivity,
  but response-derived alignment should not be used as a pre-activity feature.
- Default participant grouping keeps all meals from one participant in one
  split. Day-, meal-, or time-block splits require explicit opt-in and must be
  interpreted as participant-leakage-risk protocol variants.
- Existing full-connection CGM summary features may include future CGM relative
  to a meal and are not automatically valid for this task.
- Canonical v0 publication requires the verified batch runner because it binds
  participant-cluster intervals and the paired diet estimate to exact persisted
  predictions. A direct generic config run is staging evidence only.

## Metrics

- Primary: R2 on the configured held-out split.
- Secondary: RMSE and MAE.
- Useful audit views: split unit, label window, feature allow/forbid audit,
  participant counts, meal counts, and performance by meal-response strata.

## Verifier Surface

Treat verifier rows as normal task-ingestion material, not as an afterthought.
Verifier checks and manifest validation tiers are related but not the same.
The task-card verifier surface separates the following checks:

| Tier | What it checks | Current status |
|---|---|---|
| Contract smoke | Task loads event rows, Predictor blocks leakage columns, grouped splits are preserved, and Ridge scores. | Covered by synthetic/unit tests. |
| Artifact-mode framework validation | Real materialized meal artifact can run through PhenoBench with explicit features and participant grouping. | Covered by private HPP and CGMacros runs. |
| External OOF parity | Externally computed OOF predictions are scored through the standard Task metric path and match documented reference metrics. | Covered for the 2026-06-08 S17 package by `scripts/verify_meal_ppgr_temporal_package.py` and the internal evaluation configuration. |
| Source-result reproduction | Known manuscript or upstream result rows match shipped tables/artifacts. | Covered for private paper-output CSV anchors; not covered for full raw-data recomputation. |

The current manifest `validation_tier` vocabulary is stricter:

- `external_oof_parity`: external OOF predictions scored through the Meal PPGR
  Task contract; this validates PhenoBench scoring and alignment, not raw-data
  retraining.
- `external_submission`: external submitted predictions scored through the Task
  contract without a separate parity claim.
- `in_framework_deterministic_baseline`: deterministic predictions computed
  inside PhenoBench and scored through the Task contract.

Minimum verifier bundle for a new Meal PPGR artifact:

- artifact path or source URI
- artifact row count and participant count
- artifact checksum or manifest checksum when available
- required-column check
- selected Predictor `feature_columns`
- split unit and split counts
- activity policy
- label window
- primary metric row
- known external anchor row if one exists

Current enforced-in-code facts:

- artifact mode requires `artifact_path`
- `MealPpgrTask` emits `evaluation_unit_ids` as `TaskData.X`
- `MealPpgrPreActivityFeaturePredictor` artifact mode requires explicit `feature_columns`
- selected features must exist and be numeric
- selected features are checked against forbidden-name patterns
- missing predictor features are train-median imputed inside Ridge/RidgeCV
- participant/day/time-block/meal split keys are grouped
- `evaluation_unit_ids` are emitted into `TaskData`
- imported prediction artifacts align by `evaluation_unit_id`, not row order
- exact OOF parity runs carry `validation_tier=external_oof_parity` in Strategy
  metadata, the top-level run manifest, and the `[run-complete]` summary

Current documentation-only facts:

- artifact provenance and sync location
- source-paper output anchors
- checksum status for private/public bundles
- why each feature whitelist is scientifically defensible
- which downstream claims are not validated by the PhenoBench run

## Private Artifact Validation

The current exact handoff package is:

```text
an internal artifact
```

Package verifier:

```bash
uv run python scripts/verify_meal_ppgr_temporal_package.py \
  an internal artifact \
  --provenance-out /tmp/phenobench-meal-ppgr-temporal-package-provenance.json
```

Exact S17 OOF parity config:

```bash
uv run phenobench run the internal evaluation configuration \
  --no-predictions
```

The S17 and larger-HPP OOF configs attach that provenance JSON through
`persistence.artifact_provenance_path`, so `manifest.json` records verifier
status, bundle digest, S3 evidence when available, and artifact sha256 for the
scored artifact surface.

Reference-manifest parity after a run:

```bash
uv run python scripts/verify_manifest_reference.py \
  experiments/meal_ppgr/<run_id>/manifest.json \
  docs/walkthroughs/meal_ppgr/reference/s17_oof_manifest_reference.json
```

This scores the 56,490-row S17 logged-primary Meal Event Manifest and
`pred_ridge_no_activity` OOF parity predictions:

- validation tier: `external_oof_parity`
- split seed: `meal_ppgr_split_v1`
- R2: `0.16860482655181896`
- Pearson r: `0.4113669255097197`
- RMSE: `1130.0383980365195`
- MAE: `828.0009218570281`
- OOF meals: `56490`
- participants: `1627`

Larger-HPP source-model context:

```bash
uv run phenobench run the internal evaluation configuration \
  --no-predictions
```

This scores the 438,609-row `glycemic_labs` OOF support artifact:

- split seed: `meal_ppgr_split_v1`
- R2: `0.16757593683048144`
- Pearson r: `0.4093613169327452`
- RMSE: `1154.8263974180438`
- MAE: `840.973689093693`
- OOF meals: `438609`
- participants: `9589`

Do not mix these. The 56,490-row S17 surface is the Adva handoff row universe;
the 438,609-row surface is larger-HPP source-model context.

The validated private bundle at
`an internal artifact`
supported a real artifact-mode PhenoBench run over
`predicted_ppgr_oof_logged_primary.parquet`.

Run shape:

- 56,490 meals
- 1,627 participants
- participant-grouped split
- historical split seed: `meal_ppgr_split_v1`
- activity-blind feature whitelist
- train-split median imputation for missing feature values

The current event-key Task / pre-activity Predictor evaluation produced:

- R2: `0.18083879431104433`
- Pearson r: `0.4258475371449602`
- RMSE: `1114.6110599035796`
- MAE: `817.3937846209922`
- held-out test meals: `7503`

This validates the PhenoBench task/predictor contract on the paper artifact. It
does not retrain the manuscript's larger-HPP activity-blind OOF model.

A historical reference evaluation scored the older
2026-06-03 local `pred_ridge_no_activity` artifact over all logged-primary
rows:

- validation tier: `external_oof_parity`
- R2: `0.16860482655181896`
- Pearson r: `0.4113669255097197`
- RMSE: `1130.0383980365195`
- MAE: `828.0009218570281`
- OOF meals: `56490`
- participants: `1627`

This validates that PhenoBench can score the documented external OOF output
through a normal config. It still does not prove raw HPP retraining.

## Public CGMacros Artifact Validation

On 2026-06-03, public PhysioNet CGMacros v1.0.0 was materialized into a
MealPpgrTask artifact and synced to:

```text
an internal artifact
```

Artifact shape:

- 1,689 meals
- 45 participants
- 0-120 min PPGR iAUC label
- best available CGM source per meal: 1,648 Dexcom, 41 Libre
- skipped rows: 16 insufficient CGM coverage, 1 missing meal macros
- activity-blind feature whitelist over meal composition, timing, pre-meal CGM
  state, participant biomarkers, and meal type

PhenoBench run:

- config: the internal evaluation configuration
- run id: an internal evaluation
- participant-grouped split
- historical split seed: `meal_ppgr_split_v1`
- R2: `0.2594341544722222`
- Pearson r: `0.5157548295561057`
- RMSE: `3050.3544771706643`
- MAE: `2206.6448843648095`
- held-out test meals: `210`

Exploratory post-meal activity-proxy readout:

- Fitbit activity calories: slope per within-participant SD `-250.953`
  mg/dL*min, bootstrap 95% CI `-412.870` to `-94.465`
- Fitbit MET-minutes: slope per within-participant SD `-220.596`
  mg/dL*min, bootstrap 95% CI `-396.828` to `-45.578`
- Fitbit HR mean: slope per within-participant SD `4.110` mg/dL*min,
  bootstrap 95% CI `-133.554` to `161.339`
- Steps: insufficient coverage, 4 complete meals from 1 participant

This is a public external sanity check for the meal-anchored temporal task and
for a broad activity-proxy direction. CGMacros does not provide enough step
coverage to validate the manuscript's Apple step-bin or step-dose estimates.

## References

Sources of record:

- Ben-Yacov et al. (2021), personalized postprandial-glucose-targeting diet
  versus Mediterranean diet in prediabetes, *Diabetes Care*,
  <https://doi.org/10.2337/DC21-0162>.
- Keshet et al. (2023), CGMap, *Cell Metabolism*,
  <https://doi.org/10.1016/j.cmet.2023.04.002>.

**Unresolved manuscript references, carried over and left in place
deliberately.** The five below name a manuscript working tree, not this
repository, and none of them resolves here or anywhere else on the analysis
host. They are kept because they are the only pointer to where the design came
from, and marked because a reader will otherwise take them for repo paths:

- `PAPER.md`, "Targeting post-meal physical activity using glycemic-response
  predictions from over 400,000 meals." - **does not resolve**
- `SUPPLEMENTARY.md`, Supplementary Notes 3, 6, and 7. - **does not resolve**
- `src/ppgr_prediction.py` - **does not resolve**
- `steps/s17_predicted_ppgr_rescue.py` - **does not resolve**
- `steps/s20_curve_shape_timing.py` - **does not resolve**

## Open Questions

- Should participant-grouped RidgeCV become a separate Strategy for repeated
  meal-level observations?
- Should corrected-time sensitivity be a task variant or a separate config over
  a precomputed artifact?
- Should the private artifact path become a stable named local data source, or
  stay documented as an external sync step?
- Should verifier bundles live beside source research-run outputs, inside
  PhenoBench docs, or both?
- **Where does the manuscript working tree live?** Five of this card's
  references name files that resolve in no repository reachable from here, so
  the design rationale behind the 0-120 minute window and the iAUC choice is
  currently uncitable. Naming the repo, as `tyg` now does for its
  foundation_models sweep, would close this.
- **Is `ppgr_iauc_0_120` the right summary?** HPP work in preparation over
  >75,000 responses argues that conventional summary metrics miss temporal
  structure that multi-scale representations recover. If that publishes, the
  target definition - not just the model - is what it puts in question, and a
  changed target field moves every Atomic Unit on this Task.
