# VAT Task Card

Status: draft

Task id: `vat`

Evidence status: grounded

Evidence reviewed: 2026-07-29

## Target

DXA-derived visceral adipose tissue mass. Continuous-scalar regression. The
default research stage is `00_00_visit`, but the Task can be configured for
another available stage.

Current PhenoBench implementation:

- target field: `total_scan_vat_mass`
- target dataset: `dxa`
- default research stage: `00_00_visit`
- valid range: 1.0-6000.0 g
- primary metric: R2

## Why This Matters

VAT is a central adiposity readout for metabolic risk. Unlike BMI, it measures
visceral fat directly and captures a body-composition axis that routine
screening can miss.

The Shilo 2026 insulin-resistance surrogate paper makes VAT a useful
paper-to-PhenoBench pilot because its headline result maps to the existing
`vat` Task rather than a new target. The paper predicts DXA VAT from routine
clinical measurements, so the PB asset mapping is:

- Task: existing `vat`
- Predictor: `hpp_participant_features`
- Strategy: `ridge`
- Configs: `vat_anthropometric_routine.*` and
  `vat_circumference_routine.*`

## Baselines And Ceilings

- **Floor**: no-modality-feature baseline. `NoFeaturesPredictor` contributes
  no modality features, and `DemographicFloorStrategy` fits age, sex, and BMI.
- **Anthropometric routine track**:
  `HppParticipantFeaturePredictor x RidgeStrategy`, adding weight, height,
  sitting systolic BP, and sitting diastolic BP to the task covariates. This
  represents Shilo's paper feature set after keeping age, sex, and BMI in the
  task covariate channel.
- **Circumference routine track**: same as the anthropometric routine track,
  plus waist circumference, hip circumference, and waist-to-hip ratio.
- **Engineered gait track**: `HppModalityFeaturePredictor x RidgeCVStrategy`
  over `gait_movements` engineered features. This is a Gabet-2026-inspired
  analogue against the existing VAT target, not the paper's Gait Fusion
  embedding result. The `vat_gait_engineered_visit2.*` row pins the target and
  predictor to `02_00_visit` because the baseline visit has weak gait/DXA
  overlap for this paper-shaped row.
- **Fundus AutoMorph track**:
  `FundusAutoMorphFeaturePredictor x RidgeCVStrategy` over the 18 loader-native
  AutoMorph vessel features. This is a RetiMap-inspired cross-sectional
  analogue against VAT, not the paper's incident-CVD, survival, or
  paper-specific feature-cluster result.
- **Sleep summary track**:
  `HppParticipantFeaturePredictor x RidgeCVStrategy` over loader-native WatchPAT
  respiratory, architecture, heart-rate, and SpO2 summaries averaged across
  baseline nights. This is a Kohn-sleep-inspired analogue, not the paper's full
  PRV/HRV or sex-stratified phenome-wide model.
- **Gut microbiome species track**:
  `GutMicrobiomeAbundancePredictor x RidgeCVStrategy` over HPP
  `gut_microbiome` MetaPhlAn4 species features. This is a
  Rothschild/Keshet/Zahavi-shaped raw-abundance analogue, not gut-microbiome
  embedding parity or a disease-atlas association scan.
- **CGM IGLU track**: `CgmIgluPredictor x RidgeCVStrategy` over stable-loader
  CGM summary features. This is a Shilo/GluFormer-shaped analogue against VAT,
  not GluFormer embedding parity or a paper-faithful insulin-resistance model.

## Benchmark-Track Evidence

OpenEvidence review and paperclip search identified a replicated,
BMI-independent plasma NMR signature of VAT. A separate external prediction
study found little added Nightingale value after waist was supplied; the v0
track therefore excludes waist and every DXA field and asks for lift over only
age, sex, and BMI. Existing gait, CGM, sleep, microbiome, and routine-feature
examples remain exploratory rather than additional frozen tracks.

## Caveats

- DXA failed-scan zeros must not become biological low-VAT labels. The task's
  valid range and loader path should keep filtering obvious invalid values.
- BMI is already a task covariate. Do not duplicate BMI in the predictor output
  for this Shilo mapping unless the task covariate contract changes.
- Paper R2 values are not strict parity targets because PhenoBench uses
  canonical participant splits.
- The Shilo paper reports R2 and Spearman rho. Scalar tasks now log Spearman
  as a secondary metric, but R2 remains the primary leaderboard metric.
- Gabet's paper-faithful Gait Fusion embeddings/raw skeleton route is not
  exposed through the HPP loader. `vat_gait_engineered.*` rows must be described
  as engineered-gait analogue rows.
- Gabet stage-matched rows must report their visit explicitly. The
  `04_00_visit` route was tested and should not be promoted from the initial
  evidence because the held-out R2 was unstable despite a positive rank
  correlation.
- `vat_fundus_automorph.*` rows must keep only good-quality central-position
  fundus captures and participant-mean AutoMorph vessel features. Disc/cup
  features, image paths, QC scores, side/position metadata, and incident-CVD
  outcomes are out of scope.
- `vat_sleep_summary.*` rows may include AHI/RDI/ODI as sleep predictors for
  VAT, but those fields would be direct leakage for an AHI target row. Do not
  reuse this feature list for `ahi` without an explicit leakage exclusion.
- `vat_gut_microbiome_species.*` rows use the HPP loader's MetaPhlAn4 species
  frame, prevalence filtering, and canonical PB splits. They should not be
  compared as exact parity against papers using URS species, strain-level,
  pangenome, HUMAnN3 pathway, or learned embedding surfaces.
- `vat_cgm_iglu.*` rows are same-visit CGM-summary analogues. They are useful
  for a CGM-metabolic axis benchmark, but they should not be read as causal,
  incident, GluFormer, or exact Shilo insulin-resistance surrogate parity.

## Metrics

Primary metric is R2. Secondary metrics should include MAE in grams and
Spearman rank correlation when available. For paper-inspired rows, report
demographic-floor delta R2 and support-matched floor rows before making
modality-value claims.

## References

- Shilo et al. 2026, "Heterogeneity of Insulin Resistance Surrogates in
  Non-Diabetic Adults".
- Shilo et al. (2026), heterogeneity of insulin-resistance surrogates,
  *medRxiv*, <https://doi.org/10.64898/2026.05.02.26352290>. Local copy in
  **research-os**: `assets/papers/hpp/shilo_2026_heterogeneity_of_insulin_resistance_surr/`.
- Neeland et al. (2019), replicated NMR signature of VAT,
  <https://doi.org/10.1161/JAHA.118.010810>.
- Boone et al. (2022), external VAT prediction comparison,
  <https://doi.org/10.1093/aje/kwab298>.
- Gabet et al. (2026), a gait foundation model predicting multi-system traits,
  *arXiv*, <https://doi.org/10.48550/arXiv.2603.25283>. Local copy in
  **research-os**: `assets/papers/hpp/gabet_2026_a_gait_foundation_model_predicts_multi_s/`.
- RetiMap mapping evidence in Research OS:
  `research_runs/phenobench-paper-task/next_batch_2026_06_22/`.
- Kohn sleep mapping evidence in Research OS:
  `research_runs/phenobench-paper-task/next_batch_2026_06_22/`.
- Gut microbiome mapping evidence in Research OS:
  `research_runs/phenobench-paper-task/hpp_full_corpus_asset_map_2026_06_22/`
  and prior `paper-replicate` runs for Rothschild, Keshet, Weissglas-Volkov,
  Zahavi, and Segev.

## Open Questions

- Should VAT rows require support-matched demographic floors by default?
- Which DXA QC fields should be exposed in review packets?
- Should stage-matched gait/VAT rows remain paper-specific examples or become
  normal starter configs?
