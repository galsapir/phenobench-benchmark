# Fatty Liver Index Task Card

Status: draft

Task id: `fli`

Evidence status: grounded

Evidence reviewed: 2026-07-28

Benchmark status: complete

## Target

Fatty Liver Index, a formula-derived hepatic-steatosis surrogate.
Continuous-scalar regression on the 0-100 FLI scale. The default research stage
is `00_00_visit`, but the Task can be configured for another available stage.

Implementation facts:

- target formula: logistic transform of triglycerides, BMI, GGT, and waist
  circumference
- component fields: `bt__triglycerides`, `bt__ggt`, BMI, waist circumference
- target source: `weizmann` for blood-test components
- default research stage: `00_00_visit`
- valid range: 0.0-100.0
- primary metric: R2

## HPP data source

The triglyceride and GGT inputs load from the pinned Weizmann `blood_tests`
source. The live operational source HMO table was audited as a candidate replacement.
**Audit decision: keep Weizmann.** Agreement is excellent, but operational source +
`events` yields the largest coverage loss (net −32.3%) on the smallest cohort
(2,267 → 1,535); switching would gut an already power-limited task. Rationale and
reconsideration triggers:
blood-test source audit §9.

## Why This Matters

FLI is a simple, validated surrogate for hepatic steatosis when direct imaging
is not available. It connects liver, adiposity, and metabolic-risk axes and can
serve as a practical liver target before ultrasound/MRI-PDFF endpoints are
fully benchmarked.

## Baselines And Ceilings

The required floor is a no-modality-feature baseline: `NoFeaturesPredictor`
contributes no modality features, and `DemographicFloorStrategy` fits **age and
sex**. BMI was dropped in #6 (2026-08-20) because it is directly in the target
formula: a floor holding BMI recovers `0.139 * BMI` rather than measuring
demographic signal, which inflated it to very high R2. Both the floor and the
paired model arms declare `demographic_features: [age, sex]`, so the two sides of
the delta stay comparable.

**The scores below predate that change.** They were measured against the
age/sex/BMI floor, so read them as historical evidence rather than as the current
matrix - figure 1 marks those contracts `historical` and their replacements
`configured` with no verified route yet.

Natural comparators include liver ultrasound, MRI-PDFF where available, ALT,
AST, GGT, FIB-3/FIB-4, and metabolic-feature models. The cleaner scientific
claim is liver signal beyond BMI/waist and triglyceride reconstruction.

## Benchmark-Track Evidence

OpenEvidence review prioritized Nightingale and DXA for direct hepatic-fat
targets but identified FLI as a formula-reconstruction trap. FLI contains
triglycerides, BMI, GGT, and waist. A Nightingale track must therefore exclude
`Total_TG`, `VLDL_TG`, `LDL_TG`, and `HDL_TG`; a DXA track remains
formula-proximal because regional adiposity correlates with BMI and waist.
These rows can quantify formula predictability, but liver attenuation or the
curated disease-status Task is the stronger biological headline.

## V0 Benchmark Execution

The frozen same-visit V1→V1 matrix completed on 2026-07-29. All six rows are
locally successful and remotely `FINISHED` in operational source.

- Nightingale without triglyceride fields: n=1,902; test=269; best R2=0.870
  (CPU TabSwift).
- DXA: n=1,270; test=179; best R2=0.849 (CPU TabSwift).
- Both tracks add predictability over age/sex/BMI in the paired rows, but the
  high scores remain formula-proximity evidence, not independent liver biology -
  and the age/sex/BMI floor is exactly the comparator #6 retired, so the delta
  these rows report is not the one the current configs measure.
- Full rows and provenance: deep dive and
  aggregate review.

## Caveats

- BMI and waist are formula inputs, so body-size predictors can reconstruct
  much of the target.
- TG and GGT are same-visit blood-test inputs; same-panel predictors can leak.
- FLI is a steatosis proxy, not a fibrosis score and not a full MAFLD
  diagnosis.
- Clinical cutoffs such as 30/60 should be validated for the HPP cohort before
  classification claims.

## Metrics

Primary metric is R2. Secondary MAE and threshold AUROC for FLI >= 60 may be
useful only if a classification variant is explicitly declared. Always report
demographic-floor delta R2 and consider BMI/waist-residualized analyses.

## References

- Source material: `docs/task_cards/source_material/foundation-model-surrogate-targets-v1.md`
- Bedogni et al., 2006, Fatty Liver Index derivation:
  <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1636651/>
- Foschi et al., 2021, external validation of fatty-liver surrogate indices:
  <https://doi.org/10.3390/jcm10030520>
- Pang et al. (2022), adiposity, metabolomics, and NAFLD risk:
  <https://doi.org/10.1093/ajcn/nqab392>
- Lind et al. (2021), distinct metabolomic profiles for liver and visceral fat:
  <https://doi.org/10.1210/clinem/dgaa693>
- Keshet et al. (2024), gut-microbiome features of metabolic health,
  *Nature Communications*, <https://doi.org/10.1038/s41467-024-53832-y>. Local copy in **research-os**:
  `assets/papers/hpp/keshet_2024_identification_of_gut_microbiome_feature/`.

## Open Questions

- Should liver ultrasound or MRI-derived liver fat supersede FLI as the
  headline liver-fat target?
- **Resolved (#6, 2026-08-20): BMI is removed from the floor, and the inflated
  floor does not remain as a warning.** The v0 FLI configs declare
  `demographic_features: [age, sex]`, so the floor measures demographic signal
  instead of recovering `0.139 * BMI`. Waist was never part of this question:
  the floor covariates were age, sex and BMI, and waist reaches the formula
  through the Task's own `load_target` rather than through the covariates.
  Annotating the inflated floor was the rejected design, because a reader meets
  the number before the caveat.
- What cutoff, if any, is appropriate for HPP classification rows?
