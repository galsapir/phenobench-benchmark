# FPG Task Card

Task id: `fpg`

Evidence status: grounded

Evidence reviewed: 2026-08-15

## Target

Fasting plasma glucose. Continuous-scalar regression. The default research
stage is `00_00_visit`, but the Task can be configured for another available
stage.

Implementation facts:

- target field: `bt__glucose`
- target dataset: `blood_tests`
- target source: `weizmann`
- target unit: mg/dL
- default research stage: `00_00_visit`
- valid range: 40.0-400.0 mg/dL; a PhenoBench plausibility filter, not a
  diagnostic interval
- primary metric: R2

## HPP data source

Target loads from the pinned Weizmann `blood_tests` source. The live operational source
HMO table was audited as a candidate replacement.
**Audit decision: keep Weizmann.** operational source + `events` yields net −15.2%
baseline coverage with ~33% cohort turnover and a p99 |Δ| ≈ 11 mg/dL tail, with
no offsetting gain. Rationale and reconsideration triggers:
blood-test source audit §9.

## Why This Matters

Fasting plasma glucose is a short-horizon glycemic state marker. It is less
stable than HbA1c and more sensitive to fasting compliance, stress, illness,
and recent behavior, but it is clinically familiar and directly tied to
diabetes screening.

For PhenoBench, FPG is mainly a secondary glycemic probe. It checks whether
CGM, diet, sleep, activity, and metabolic features capture current glycemic
state beyond age/sex/BMI.

**What a row here does not support.** A predicted FPG is a same-visit
association with a single laboratory draw. It is not a diagnosis, not a
prospective statement about incident diabetes, and not evidence of clinical
utility. Those are three separate designs with their own endpoints and scoring.

## Related HPP Measurements

Demonstrated in HPP, on this cohort and device family:

- **Fasting glucose is far less stable within a person than a single draw
  suggests.** Shilo et al. measured FG across 59,565 morning windows in 8,315
  non-diabetic HPP adults aged 40-70: mean 96.2 ± 12.87 mg/dL, rising
  0.234 mg/dL per year of age, with intraperson day-to-day SD 7.52 ± 4.31 mg/dL
  (Shilo et al. 2024). This is the same cohort this Task scores.
- **Time spent in elevated glycemic ranges carries prospective signal.** Godneva
  et al., 8,687 HPP adults, report age- and sex-adjusted hazard ratios of 1.34
  (95% CI 1.26-1.42) for incident metabolic conditions per higher time above
  140 mg/dL, and 1.21 (1.15-1.26) above 180 mg/dL (Godneva et al. 2026).
- CGMap provides the HPP reference distribution for CGM-derived measures in
  non-diabetic individuals and their associations with clinical parameters
  (Keshet et al. 2023).

**And the committed rows do answer the paired question, which an earlier version
of this card said they did not.** The snapshot carries demographic-floor deltas,
not just raw R2, and both tracks clear the floor: V1 CGM + demographics
**ΔR2 = +0.169 (95% CI [+0.084, +0.247])** on n = 6,844, and V1 Nightingale NMR
**ΔR2 = +0.027 ([+0.000, +0.053])** on n = 6,165. So CGM summaries do improve
same-visit FPG prediction beyond age/sex/BMI on this cohort.

The two tracks sit on different cohorts (6,844 against 6,165), so the CGM margin
being larger is **not** a paired comparison between the modalities. Each delta
corrects its own model against its own floor on its own participants; ranking
them across cohorts is the same unmatched-comparison error a within-track delta
does not fix.

Still proposed rather than shown: that a *learned* CGM representation beats these
engineered summaries. The delta above is for the IGLU-style panel.

## Clinically Meaningful Variants

**No categorical FPG variant is defensible on a single research visit, and the
HPP evidence is what rules it out rather than a general caution.** ADA
thresholds classify FPG ≥126 mg/dL as diabetes and 100-125 mg/dL as impaired
fasting glucose (ADA 2026); WHO's impaired-fasting-glucose band starts at 110 mg/dL,
so the same measurement bins differently by guideline. Applied to this cohort
the instability dominates either choice: of 5,328 HPP participants who would
have been called normal on their first FG, **40% would be reclassified into the
prediabetes range and 3% into the diabetes range** on sequential measurement
within the same study (Shilo et al. 2024).

So a binary or ordinal FPG Task built on one visit would be scoring label noise
against a threshold, and would read as diagnosis while measuring draw-to-draw
variation. The continuous target stays primary. A categorical variant becomes
defensible only with a repeat-measurement label rule - the confirmatory second
test clinical diagnosis already requires - and that is a different cohort
construction, not a binning of this one.

`prediabetes_status` and `t2d_status` are the supported categorical routes;
both take their labels from the curated diabetes phenotype rather than from a
threshold on this field.

## Baselines And Ceilings

- **Floor**: no-modality-feature baseline. `NoFeaturesPredictor` contributes
  no modality features, and `DemographicFloorStrategy` fits age, sex, and BMI.
- **CGM IGLU track**: `CgmIgluPredictor x RidgeCVStrategy` over stable-loader
  CGM summary features. This is a GluFormer-inspired analogue, not a GluFormer
  embedding, intervention-simulation, or incident-endpoint result.
- **Near ceiling**: engineered CGM summaries and same-window glycemic labs are
  strong comparators, but same-assay blood-test features require leakage review.

## Caveats

- Same-visit CGM summaries and fasting glucose are physiologically adjacent;
  rows should be interpreted as current-state glycemic probing, not prospective
  disease prediction.
- GluFormer paper-faithful rows require an embedding artifact contract with
  model/version provenance and target-window alignment.
- Incident diabetes, cardiovascular, or intervention claims need a separate
  endpoint/scoring design and must not be represented as this scalar row.
- HPP `bt__glucose` follows the current task convention as fasting glucose;
  confirm fasting-state metadata before making strict fasting claims.

## Metrics

Primary metric is R2. Secondary MAE in mg/dL is useful. For CGM-adjacent rows,
report demographic-floor delta R2 and compare against simple CGM-summary
baselines on matched support.

## References

- Source material: `docs/task_cards/source_material/foundation-model-surrogate-targets-v1.md`
- GluFormer mapping evidence in HPP documentation:
  `research_runs/phenobench-paper-task/next_batch_2026_06_22/`.
- Shilo et al. (2024), continuous glucose monitoring and intrapersonal
  variability in fasting glucose, *Nature Medicine*,
  <https://doi.org/10.1038/s41591-024-02908-9>.
- Godneva et al. (2026), the spectrum of normoglycemia and time in glycemic
  ranges, *Diabetes Care*, <https://doi.org/10.2337/dc25-2154>.
- Keshet et al. (2023), CGMap, *Cell Metabolism*,
  <https://doi.org/10.1016/j.cmet.2023.04.002>.
- ADA Standards of Care in Diabetes 2026, diagnosis and classification,
  <https://doi.org/10.2337/dc26-S002>.
- WHO/IDF (2006), *Definition and diagnosis of diabetes mellitus and
  intermediate hyperglycaemia*, for the 110 mg/dL impaired-fasting-glucose
  lower bound that differs from ADA's 100 mg/dL.

## Open Questions

- What HPP fasting-state metadata should be surfaced in run review packets?
  Unresolved, and it bounds the target's meaning: `bt__glucose` is treated as
  fasting by task convention, and nothing in the Task verifies fasting state.
- Should FPG delta become a separate task, or should HbA1c remain the preferred
  longitudinal glycemic target?
- Which CGM engineered-feature baseline should define the near-term ceiling?
- Given the measured intraperson variability, what is the reducible ceiling on
  R2 here? A perfect same-visit predictor still faces a target whose own
  day-to-day SD is 7.52 mg/dL against a between-person SD of 12.87. Nobody has
  derived the implied bound, and it would change how a modest R2 is read.
