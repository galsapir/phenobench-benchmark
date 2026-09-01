# Chronological Age Task Card

Status: draft

Task id: `chronological_age`

Evidence status: grounded

Evidence reviewed: 2026-08-15

## Target

Participant chronological age. Continuous-scalar regression. The default
research stage is `00_00_visit`, but the Task can be configured for another
available stage.

Implementation facts:

- target field: `age`
- target dataset: `anthropometrics`
- target source: None
- target unit: years
- default research stage: `00_00_visit`
- valid range: 18.0-120.0 years
- primary metric: R2
- default covariates: sex, BMI
- derived outputs: `biological_age_residual_years` and
  `biological_age_centered_residual_years` in `predictions.parquet` when
  predictions are persisted

## Why This Matters

Chronological-age prediction is the safe PhenoBench surface for aging-clock
papers. In Reicher/Bar 2024, biological-age scores are derived from held-out
age predictions centered within age bins, so they should be logged as derived
strategy outputs or artifact metadata unless a reviewed clock-target policy is
added.

The paper-to-PhenoBench mapping is:

- Task: `chronological_age`
- Predictor: system/modal participant features
- Strategy: supervised regression on canonical PB splits
- Secondary artifact: biological-age residual or centered BA score

`biological_age_residual_years` is defined as
`predicted_chronological_age_years - chronological_age_years`; positive values
mean older-than-chronological. This is a row-level derived output, not a
separate observed target.

`biological_age_centered_residual_years` is defined as
`predicted_chronological_age_years - mean(predicted_chronological_age_years |
split, sex, floor_chronological_age_year)`. This mirrors the paper's sex and
1-year age-bin centering shape, but uses split-local centering for PB artifacts
so train predictions do not set the eval-row baseline.

**What a row here does not support.** The target is a date of birth. Predicting
it well means a modality carries age-correlated structure - nothing more. In
particular the derived residual is **not a validated measure of biological age
or of ageing rate**: a positive residual says a model placed a participant older
than their years on the information it was given, which is a property of the
model and the modality as much as of the participant. Treating it as a clinical
ageing phenotype needs a reviewed clock-target policy, longitudinal validation
against outcomes, and a stability analysis that none of these rows provide.

## Related HPP Measurements

Demonstrated in HPP and persisted in this repository, from
`docs/figure1/chronological_age_review.json`,
test split:

- V1 sleep reaches test R2 = 0.273 (95% CI [0.237, 0.305]) on a cohort of 9,453.
- V1 Nightingale reaches R2 = 0.124 (95% CI [0.093, 0.152]) on 10,128.
- V1 CGM reaches R2 = 0.094 (95% CI [0.064, 0.125]) on 11,483.
- The four-modality fusion (CGM + sleep + diet + …) reaches R2 = 0.421
  (95% CI [0.365, 0.467]) on 5,491.

**Read the fusion number against its cohort, not against the others.** It scores
5,491 participants where the single-modality rows score 9,453-11,483, because
requiring every modality shrinks the eligible population by roughly half. A
fusion arm can therefore beat a single modality partly by scoring an easier or
simply different set of people; the paired comparison on matched support is what
separates the two explanations, and it is not in these numbers.

**This card's snapshot carries no paired deltas against a demographic floor**,
unlike every other card in this set - the tracks are single-modality with no
floor comparator recorded, which is expected here because age is the target and
cannot be a covariate. So the R2 values above are raw predictability, and there
is no committed margin to quote.

Proposed rather than shown: that any of this reflects biological ageing rather
than modality-specific age structure. Nothing committed distinguishes them.

**These are `reviewable` rows, not `final` ones.** Measured across the committed
leaderboards: all 787 rows carry `curation_state: reviewable` and none is
`final`. A complete fresh v0 re-run is committed to, so every figure in this
section is pre-re-run evidence that the re-run supersedes - persisted and citable
today, not a frozen result. **Which curation states the Figure 1 export accepts
is the export track's live question, not this card's**; read the two counts
above, not a gate.

## Baselines And Ceilings

- **Floor**: no-modality-feature baseline. `NoFeaturesPredictor` contributes
  no modality features, and `DemographicFloorStrategy` fits only allowed
  demographic covariates: sex and BMI here, because age is the target and is
  forbidden as a covariate. For OOF modality comparisons, use named support
  cohorts so the floor and modality row score the same participants.
- **Sleep track**: `HppModalityFeaturePredictor x RidgeCVStrategy` over
  loader-native WatchPAT sleep features after conservative age-leak exclusions.
- **CGM track**: `HppModalityFeaturePredictor x RidgeCVStrategy` over
  loader-native CGM summary features after conservative age-leak exclusions.
- **Nightingale track**: `HppParticipantFeaturePredictor x RidgeCVStrategy`
  over an explicit NMR lipid-biomarker allowlist. This is not the paper's
  3,098-cluster LC-MS lipidomics feature space.
- **Serum lipidomics OOF track**:
  `HppModalityFeaturePredictor x SexStratifiedLightGBMCVStrategy` over
  annotated HPP serum lipidomics features. This is a closer blood-lipid
  analogue than Nightingale NMR, but still not the paper's gated 3,098-cluster
  WIS LC-MS matrix.
- **Renal OOF track**:
  `HppParticipantFeaturePredictor x SexStratifiedLightGBMCVStrategy` over
  long-form blood-test pivots for creatinine, urea, sodium, and potassium. This
  is the first Reicher/Bar age-clock panel in PB that exercises explicit
  `blood_tests:<measurement>` feature specs.
- **Frailty OOF track**:
  `HppParticipantFeaturePredictor x SexStratifiedLightGBMCVStrategy` over
  hand-grip, DXA lean-mass, height, and weight fields. This maps the paper's
  frailty-system route, but the current PB config exposes raw fields rather
  than derived best-grip, ALM, or ALMI features.
- **Olink proteomics OOF track**:
  `OlinkProteomicsPredictor x SexStratifiedLightGBMCVStrategy` over the whole
  Olink Reveal NPX proteome (~1,000 proteins after a >=0.10 detection-rate
  filter), the plasma-proteome analogue of the serum-lipidomics OOF track.
  Below-LOD cells are left NaN under the default `nan_below_lod` policy and
  train-median imputed in-strategy. A ridge baseline
  (`OlinkProteomicsPredictor x SexStratifiedRidgeCVStrategy`) pairs the synthetic
  smoke. Config:
  `chronological_age_olink_proteomics_lightgbm_oof.operational source.example.yaml`.
- **Sex-stratified age-clock tracks**:
  `Hpp*FeaturePredictor x SexStratifiedRidgeCVStrategy` variants for sleep,
  CGM, and Nightingale. These fit one model per sex stratum and use BMI as the
  remaining demographic covariate.
- **LightGBM age-clock tracks**:
  `Hpp*FeaturePredictor x SexStratifiedLightGBMCVStrategy` variants for sleep,
  CGM, and Nightingale. These are closer to Reicher/Bar 2024: one LightGBM
  regressor per sex stratum and train-split OOF predictions for BA artifacts.
  Validation/test rows are still PB split rows predicted by full train-stratum
  models, not full paper OOF across the complete matched cohort.
- **LightGBM OOF tracks**:
  `chronological_age_*_lightgbm_oof` configs score every row in the
  predictor-support cohort via sex-stratified K-fold predictions. They are the
  closest current PB analogue to the paper's OOF reporting protocol, while
  still using PB loader feature routes and caveats.
- **Reviewed artifact track**:
  `ParticipantFeatureArtifactPredictor x SexStratifiedLightGBMCVStrategy` for
  regenerated Reicher-style per-system matrices. For paper-parity probes, use
  a named matched-support cohort, sex-only demographic features for
  stratification, `subsample_freq=1`, and inner early stopping controls.
- **MMFM/fusion embedding tracks**:
  `ParticipantEmbeddingPredictor` or `FusionTuplePredictor` over imported
  Adva/Alon MMFM artifacts. These configs use `split_source: artifact` and
  `cohort_spec: predictor_support`, because the artifact defines the available
  participant set and train/validation split. In this context, "fusion" means
  imported MMFM/fusion embeddings, not naive concatenation of HPP feature
  tables. The current starter artifacts are CGM+sleep static handoff artifacts;
  a diet+activity+CGM+sleep artifact should use the same predictor contract
  once available.
- **Fusion lift diagnostic**:
  `FusionTuplePredictor x RidgeCVDeltaR2Strategy` logs demographics-only R2,
  demographics+embedding R2, delta-R2, bootstrap CI, and permutation p-value
  as scalar metrics.
- **Olink proteome lift diagnostic**:
  `OlinkProteomicsPredictor x RidgeCVDeltaR2Strategy` logs demographics-only R2,
  demographics+proteome R2, delta-R2, bootstrap CI, and permutation p-value on
  one predictor-support cohort/fold set.

## Caveats

- Do not include `age`, age-matched percentiles, z-scores, baseline trackers,
  visit counters, birth fields, or model-derived BA scores in predictor
  features.
- PB canonical participant splits are not the paper's sex-stratified 3-fold
  OOF scheme. Leaderboard rows are paper-inspired unless a paper-faithful
  strategy is added.
- Reicher/Bar 2024 trained sex-specific LightGBM models. The sex-stratified
  RidgeCV starter rows match the sex-specific model shape but use RidgeCV.
  LightGBM rows require the optional `boosting` extra. OOF LightGBM rows should
  be compared separately from canonical validation/test leaderboard rows.
- `SexStratifiedLightGBMCVStrategy` supports optional `subsample_freq`,
  `early_stopping_validation_fraction`, and `early_stopping_rounds` controls
  for closer reproduction of paper-style LightGBM age-clock training. Defaults
  preserve the simpler PB starter behavior.
- Biological age is not an observed target here. Treat BA residuals/scores as
  derived outputs until a reviewed imported-clock target contract exists.
- `biological_age_centered_residual_years` is still a derived output, not an
  observed target. It is split-local PB centering, not the paper's full
  sex-stratified OOF BA workflow.
- Exact blood-lipid parity is gated by the paper's LC-MS lipid-cluster route.
- Diagnosis and menopause association scorecards belong to follow-up analysis
  artifacts, not the primary scalar age leaderboard row.
- Olink proteomics enters as a whole-proteome feature route (`olink_proteomics`,
  information source `olink`). Organ/system panel clocks are deferred; any
  future route needs separate review and must not become a `panel` kwarg on the
  whole-proteome predictor.
- Olink selection bias: participants with QC-passed Olink skew slightly older
  and narrower in age (mean ~51.8 vs ~50.4 years for non-Olink), so the
  proteomic clock describes the assayed sub-population, not the full HPP cohort.
  The narrower age spread can also depress absolute R2.
- Olink NPX is log2 and relative; below-LOD (~13.5% of QC-passed cells) is
  left-censored, not missing-at-random. The default `nan_below_lod` policy drops
  those cells to NaN for leakage-safe train-median imputation; `keep` and
  `half_lod_impute` are ablation arms that change the surviving feature count
  and can inflate R2 via below-LOD noise.
- For the Olink lift diagnostic, `r2_demo_embed` is a pooled (non-stratified)
  Ridge and is NOT the sex-stratified LightGBM OOF headline R2. Do not
  cross-compare the two; the delta-R2 is only valid internally against its own
  demographics-only floor.

## Metrics

Primary metric is R2 for chronological-age prediction. Secondary MAE in years
is essential for clinical readability. For aging-clock work, persist and audit
`biological_age_residual_years` and `biological_age_centered_residual_years`
when available, but do not treat them as observed targets.

## References

- Reicher, N. et al. 2024, "Phenome-wide associations of human aging uncover
  sex-specific dynamics".
- Reicher et al. (2024), phenome-wide associations of human ageing,
  *Nature Aging*, <https://doi.org/10.1038/s43587-024-00734-9>. Local copy in **research-os**:
  `assets/papers/hpp/reicher_2024_phenome_wide_associations_of_human_aging/`.
- Research OS replication package:
  `research_runs/paper-replicate/reicher_2024_phenome_wide_associations_of_human_aging/`.
- Argentieri, M.A. et al. (2024), proteomic aging clock predicting mortality and
  age-related disease (UK Biobank Olink),
  <https://doi.org/10.1038/s41591-024-03164-7>.

## v0 Final-Test Status

- Four approved representation-probe Benchmark Tracks use V1 Nightingale, CGM,
  sleep, or CGM + sleep + diet + activity fusion, with sex and BMI but no age
  input.
- Sex-stratified Ridge and LightGBM produced eight remotely verified rows. Best
  held-out R² values were 0.124, 0.094, 0.273, and 0.421, respectively.
- The fusion artifact is checksum- and four-source-provenance-bound, but this
  release does not independently audit every upstream pretraining variable for
  age-correlated side channels. Treat 0.421 as a representation-probe result.
- TabSwift is deferred until GPU execution. Full contract and results:
  `05-sleep-gut-aging.md`.

## Olink Proteomic Clock — Initial Validation

First real-data validation of the Olink proteome route (baseline `00_00_visit`,
`min_detection_rate=0.10`, `nan_below_lod`, `cohort_spec=predictor_support`).
These are validation evidence, not published leaderboard rows.
The implementation and validation discussion are recorded in
[PR #149](https://github.com/PhenoAI/phenobench/pull/149); no dedicated
leaderboard rows are committed for these numbers.

**The figures below are an uncommitted validation read and are not reproducible
from this repository.** No leaderboard row, review JSON or report under
`reports/` holds them, so a reader cannot re-derive them from the tree and a
re-run will not reproduce them without the PR's configuration. A pull-request
discussion is a record of a conversation, not a persisted derivation - the
distinction this repository has already paid for once, when a widely quoted
overlap figure was removed for having no derivation behind it. They are kept
because the result is real and worth knowing; they are marked so nobody quotes
them as committed evidence. See Open Questions.

- **Whole-proteome OOF clock** (`sex_stratified_lightgbm_cv`, `eval_split=oof`):
  R² = 0.726, cohort n = 4,870 (train/validation/test 3,376 / 740 / 754).
- **Proteome vs demographic floor** (`ridge_cv_delta_r2`, same cohort/folds,
  1000-bootstrap / 1000-permutation): demographics-only R² = 0.017,
  demographics+proteome (pooled Ridge) R² = 0.792, ΔR² = 0.774
  (95% CI [0.742, 0.807], permutation p < 0.001). The proteome supplies
  essentially the entire age signal over the sex+BMI floor (~2% → ~79% variance
  explained). The pooled-Ridge 0.792 is not the OOF headline 0.726 — different
  model and eval split; do not cross-compare.

## Clinically Meaningful Variants

**No categorical variant of chronological age is meaningful, and that is not the
interesting question here - the derived residual is.** Age is a continuous known
quantity; binning it would create an age-group classification Task whose labels
are already available, which measures nothing.

The live variant question is whether `biological_age_residual_years` should
become a target in its own right, and the answer is not yet:

- **It is a model output, not a measurement.** The residual depends on which
  modality the clock saw and how well it fits, so two clocks disagree about the
  same participant by construction. A "biological age" Task would be scoring one
  model against another model's output.
- **Thresholds on it have no clinical standing.** There is no validated cutoff
  for an accelerated-ageing label, and any percentile bin would be relative to
  this cohort's own clock.
- **The centering convention is load-bearing.** `biological_age_centered_
  residual_years` centres within split, sex and 1-year age bin, so the value a
  participant receives depends on who else is in their split - which is
  defensible for an artifact and unacceptable for a target.

The card already records the right disposition: log these as derived Strategy
outputs or artifact metadata, and gate a clock target behind a reviewed policy.

## Open Questions

- Which imported biological-age clock target, if any, should become a separate
  reviewed task?
- Should OOF age-clock rows be separated from standard validation/test
  leaderboard rows in the public UI?
- Which age-leak feature families need automated checks beyond the current
  card warnings?
- **Should the Olink validation figures be persisted or dropped?** They are the
  only numbers on this card with no derivation in the tree. Persisting them
  under `reports/` or as a review JSON would make them citable; leaving them
  qualified, as now, keeps a real result visible at the cost of it being
  unverifiable here. Alon's call on 2026-08-15 was to qualify rather than strip
  or persist, because persisting is a run's worth of work outside the evidence
  track.
- Does the four-modality fusion beat the single-modality rows **on matched
  support**? Its cohort is 5,491 against 9,453-11,483, so the committed
  comparison cannot separate a better model from an easier population.
