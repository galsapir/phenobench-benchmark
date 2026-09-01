# eGFR Task Card

Status: draft

Task id: `egfr`

Evidence status: grounded

Evidence reviewed: 2026-07-29

## Target

Cross-sectional eGFR regression on HPP V1 using the CKD-EPI 2021 race-free
formula.

Current PhenoBench implementation computes eGFR from:

- serum creatinine: `bt__creatinine`
- age
- sex

Implementation facts:

- target name: `egfr`
- target field: `egfr`
- target dataset: `derived_renal_indices`
- target source: **`derived`**, not `weizmann`. This is a computed target, and
  `target_source` is what the Benchmark Track sees. The Weizmann `blood_tests`
  pin describes where the **creatinine input** comes from - see HPP data source
  below - and naming it here misdescribed the declared source
- default research stage: `00_00_visit`
- valid range: 10.0-150.0 mL/min/1.73m2
- primary metric: R2

## HPP data source

The creatinine input loads from the pinned Weizmann `blood_tests` source. The
live operational source HMO table was audited as a candidate replacement.
**Audit decision: keep Weizmann.** Creatinine agreement is tight, but the CKD-EPI
formula amplifies per-participant differences (eGFR p99 |Δ| ≈ 10.6), and
operational source + `events` yields net −18.1% baseline coverage with ~34% cohort
turnover. Rationale and reconsideration triggers:
blood-test source audit §9.

## Why This Matters

eGFR is the standard clinical estimate of kidney filtration. It is used for CKD
staging, medication dosing, kidney-disease monitoring, and risk stratification.
It is a clinically recognizable target and connects to long-term kidney and
cardiovascular outcomes.

For PhenoBench, eGFR is also a useful stress test for benchmark interpretation:
the target is formula-derived, and the formula already includes age and sex.

## Baselines And Ceilings

The required floor is a no-modality-feature baseline: `NoFeaturesPredictor`
contributes no modality features, and `DemographicFloorStrategy` fits age, sex,
and BMI.

This floor is structurally inflated because age and sex are inputs to CKD-EPI.
Current code documents Surrogate's eGFR demographic floor around R2 0.22. The
source material estimates an age+sex floor around R2 0.15-0.25.

The remaining variance is largely creatinine-driven. Creatinine reflects kidney
function, muscle mass, diet, and assay effects. A model with direct access to
Nightingale creatinine or closely related chemistry can trivially look strong.

## Caveats

- Age and sex are directly embedded in the target formula.
- High raw R2 can mean the model recovered formula inputs, not kidney-specific
  physiology.
- Creatinine is not a pure kidney-function marker; it also reflects muscle mass
  and diet.
- Nightingale creatinine and clinical serum creatinine may differ by aliquot and
  platform, creating systematic offsets.
- Single-timepoint eGFR does not fully establish chronic kidney disease, which
  clinically requires chronicity.

## Metrics

- Primary: R2 for continuous eGFR regression.
- Secondary: MAE.
- Possible extension: AUROC or ordinal metrics for CKD categories, with clear
  chronicity caveats.
- Essential audit: residualized analysis that separates formula-input recovery
  from kidney-specific signal.

## Benchmark-Track Evidence

OpenEvidence review and broader Paperclip search support V1 Nightingale as the
minimal cross-modal track. Large population NMR studies associate lipoprotein,
fatty-acid, and GlycA traits with creatinine-based eGFR after demographic
adjustment, but the relationship is cross-sectional and may reflect reduced
clearance or altered metabolism. The benchmark must exclude creatinine and all
eGFR aliases. DXA was not selected: lean mass changes creatinine generation and
would make this formula-derived target especially difficult to interpret.

## References

- Source material: `docs/task_cards/source_material/foundation-model-surrogate-targets-v1.md`
- UK Biobank creatinine field: <https://biobank.ndph.ox.ac.uk/ukb/field.cgi?id=30700>
- UK Biobank cystatin C field: <https://biobank.ctsu.ox.ac.uk/ukb/field.cgi?id=30720>
- Kidney function trajectories from UK Biobank EMR: <https://www.nature.com/articles/s41598-025-85391-7>
- Barrios et al. (2018), NMR biomarkers of renal function:
  <https://doi.org/10.1038/s41598-018-33507-7>.
- Nankivell et al. (2020), muscle mass and creatinine eGFR:
  <https://doi.org/10.1016/j.eclinm.2020.100662>.

## Open Questions

- Should a creatinine-residualized eGFR variant be a separate task?
- Should CKD staging become a curated phenotype card rather than an eGFR
  regression variant?
- **Resolved (#6, 2026-08-20): it does not warn, it refuses or corrects.** Where
  dropping the overlapping covariate leaves a demographic floor, the config drops
  it (FLI loses BMI, FIB-4 loses age) and the row keeps competing. eGFR is the
  case where it does not: CKD-EPI takes creatinine, age AND sex, so removing the
  overlap would leave a BMI-only floor and model arms stripped of age and sex. So
  eGFR's rows keep their covariates, declare `covariate_in_formula: [age, sex]`,
  and carry `benchmark_role: reference` instead of ranking. Model-accessible
  biomarkers are a separate question and this does not answer it: creatinine
  access is excluded by the panel rather than by this mechanism.
