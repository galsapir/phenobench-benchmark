# Lean Body Mass Task Card

Task id: `lean_body_mass`

Evidence status: grounded

Evidence reviewed: 2026-07-29

## Target

DXA-derived total lean body mass. Continuous-scalar regression. The default
research stage is `00_00_visit`, but the Task can be configured for another
available stage.

Implementation facts:

- target field: `body_comp_total_lean_mass`
- target dataset: `body_composition`
- target source: None
- default research stage: `00_00_visit`
- valid range: 10000.0-150000.0 g
- primary metric: R2

## Why This Matters

Lean body mass is relevant to sarcopenia, frailty, mobility, metabolic reserve,
and aging. It is a useful body-composition target, but absolute total lean mass
is heavily determined by sex, height/body size, and BMI.

For PhenoBench, this is mainly a secondary body-composition probe. The claim to
care about is added signal beyond crude anthropometrics.

## Baselines And Ceilings

The required floor is a no-modality-feature baseline: `NoFeaturesPredictor`
contributes no modality features, and `DemographicFloorStrategy` fits age, sex,
and BMI. The task code records a very high demographic floor around R2 0.78.

Natural comparators include plasma metabolomics, objective activity, grip
strength, and frailty-system age-clock panels. A row that does not clear the
floor is not informative.

## Benchmark-Track Evidence

The frozen v0 tracks use the fixed nine-field V1 Nightingale amino-acid panel
(`Ala`, `Gln`, `Gly`, `His`, `Ile`, `Leu`, `Val`, `Phe`, `Tyr`) plus V1 age,
sex, and BMI for both V1 and V2 lean-mass targets. literature and literature
support amino-acid and branched-chain-amino-acid associations with muscle mass
and strength. Same-scan regional DXA fields remain excluded.

Gait Fusion is not v0-benchmark-ready. Raw Newton skeleton files exist on S3,
but no canonical operational source contract, checksum-bound embeddings, or accessible
checkpoint was found. The available engineered-gait V1 cohort overlaps only
448 V1 and 113 V2 eligible lean-mass targets, so gait remains a future blocked
candidate.

## Caveats

- Absolute lean mass is strongly confounded by sex and body size.
- DXA scan quality, device/calibration, hydration, and segmentation can add
  noise.
- Total lean mass is not the same as appendicular lean mass index or
  sarcopenia diagnosis.
- Same-DXA predictor features are likely leakage.

## Metrics

Primary metric is R2. Secondary MAE is most readable in kg after converting
the stored gram-scale target. Audit views should include demographic-floor
delta R2, sex-stratified residuals, and support-cohort matching when comparing
modality predictors.

## References

- Source material: `docs/task_cards/source_material/foundation-model-surrogate-targets-v1.md`
- Brown et al., 2015, sarcopenia and mortality:
  <https://doi.org/10.1002/jcsm.12073>
- Abramowitz et al., 2018, muscle mass, BMI, and mortality:
  <https://doi.org/10.1371/journal.pone.0194697>
- Reicher et al. (2024), phenome-wide associations of human ageing,
  *Nature Aging*, <https://doi.org/10.1038/s43587-024-00734-9>. Local copy in **HPP documentation**:
  `assets/papers/hpp/reicher_2024_phenome_wide_associations_of_human_aging/`.
- Gabet et al. (2026), HPP gait foundation model,
  <https://doi.org/10.48550/arXiv.2603.25283>.
- Moore et al. (2018), metabolomic profiles of muscle mass and strength,
  <https://doi.org/10.18632/aging.101574>.

## Open Questions

- Should appendicular lean mass or ALMI become the primary muscle target?
- Which DXA QC fields should be enforced before leaderboard rows are trusted?
