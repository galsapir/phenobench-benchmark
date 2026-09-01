# LDL-C Task Card

Status: draft

Task ids: `ldl`, `ldl_nmr`

Evidence status: grounded

Evidence reviewed: 2026-08-15

## Target

Low-density lipoprotein cholesterol. Continuous-scalar regression. The default
research stage is `00_00_visit`, but the Tasks can be configured for another
available stage. PhenoBench currently exposes two measurement routes:

Implementation facts:

For `ldl` (clinical blood test):

- target field: `bt__ldl_cholesterol`
- target dataset: `blood_tests`
- target source: `weizmann`
- target unit: mg/dL
- valid range: 20.0-500.0 mg/dL
- primary metric: R2

For `ldl_nmr` (Nightingale NMR):

- target field: `Clinical_LDL_C`
- target dataset: `nightingale`
- target source: None (Nightingale's primary source is set in the loader)
- target unit: **mmol/L**, not "NMR units" - an earlier version of this card
  hedged the unit, and the hedge is what makes a threshold slip through
- valid range: 0.5-8.0 mmol/L
- primary metric: R2

Both default to `00_00_visit` with age/sex/BMI covariates at the configured
research stage. **The two ids are different measurements in different units on
different platforms, not two spellings of one target.**

## HPP data source

Target loads from the pinned Weizmann `blood_tests` source. The live operational source
HMO table was audited as a candidate replacement.
**Audit decision: keep Weizmann for now.** LDL is the one blood target where operational source
materially expands coverage (+51.0% net N), but it still replaces ~27% of the
current cohort and carries a p99 |Δ| ≈ 32 mg/dL with a small negative bias. A
switch should be reconsidered after pre-specifying and meeting an LDL agreement
tolerance and validating that the operational source-only participants are genuine
baseline draws. Evidence and reconsideration triggers:
blood-test source audit §9.

## Why This Matters

LDL-C is the canonical causal lipid risk factor for atherosclerotic
cardiovascular disease and the main target of lipid-lowering therapy, supported
by Mendelian-randomization and treatment-trial evidence. It is clinically
familiar, but it is also strongly influenced by genetics and medications, so
demographic-only prediction should be weak.

The paired clinical/NMR tasks are useful for assay-robustness checks. A result
that appears only on one route may reflect assay/platform quirks rather than
general LDL biology.

**What a row here does not support.** A predicted LDL-C is a same-visit
association. It is not a cardiovascular risk estimate and not a treatment
indication, and the causal evidence that makes LDL-C important - Mendelian
randomisation and lipid-lowering trials - is evidence about *lowering* LDL-C,
not about predicting it from other modalities.

## Related HPP Measurements

Demonstrated in HPP and persisted in this repository, from
`docs/figure1/ldl_review.json`, test split:

- V1 CGM + demographics reaches test R2 = 0.022 (95% CI [-0.020, 0.062]) on a
  cohort of 3,153.
- V1 DXA + demographics reaches R2 = 0.016 (95% CI [-0.024, 0.047]) on 1,892.

**Both intervals cross zero, and so do the paired margins against the
demographic floor**: DXA **ΔR2 = +0.004 (95% CI [-0.013, +0.023])**, CGM
**-0.014 ([-0.050, +0.022])**. On this cohort neither glucose dynamics nor body
composition demonstrably predicts LDL-C beyond age, sex and BMI - the expected
result for a trait dominated by genetics and lipid-lowering medication.

`tg` on the same two modalities clears the floor by +0.122 and +0.053. Those are
different cohorts, so read it as an unmatched corpus comparison rather than a
controlled contrast.

Proposed rather than shown: that genetic scores or dietary features recover what
DXA and CGM cannot. Nothing committed answers it.

**These are `reviewable` rows, not `final` ones.** Measured across the committed
leaderboards: all 787 rows carry `curation_state: reviewable` and none is
`final`. A complete fresh v0 re-run is committed to, so every figure in this
section is pre-re-run evidence that the re-run supersedes - persisted and citable
today, not a frozen result. **Which curation states the Figure 1 export accepts
is the export track's live question, not this card's**; read the two counts
above, not a gate.

## Clinically Meaningful Variants

**LDL-C thresholds are treatment targets stratified by cardiovascular risk, not
diagnostic cutoffs, so there is no single boundary to bin on** - and on the NMR
route there is a second, mechanical block on top of that.

- **The two ids need different conversions, and the factor is analyte-specific.**
  Converting a cholesterol value between mmol/L and mg/dL uses the molar mass of
  cholesterol (≈38.7 mg/dL per mmol/L). The triglyceride factor is different
  (≈88.6, see `tg`). So "convert the NMR route to clinical units" is not one
  rule applied to a lipid panel; it is per analyte, and using the wrong one
  produces a plausible-looking number.
- **Conversion is not equivalence.** A Nightingale `Clinical_LDL_C` in converted
  mg/dL is still not the enzymatic assay a guideline threshold was validated on,
  and the cohorts differ too: the clinical route carries 3,153 participants here
  against the NMR route's own eligibility.
- **A threshold would also cross a medication boundary.** Participants on
  statins sit below a target *because* of treatment, so a bin mixes untreated
  biology with treated biology unless medication is modelled, which this Task
  does not do.

The continuous targets stay primary on both routes. `hyperlipidemia_status` is
the supported categorical lipid route, and it takes its label from the curated
phenotype rather than from a threshold on either field here.

## Baselines And Ceilings

The required floor is a no-modality-feature baseline: `NoFeaturesPredictor`
contributes no modality features, and `DemographicFloorStrategy` fits age, sex,
and BMI. General adult-cohort expectations are low, roughly R2 0.02-0.08 for
clinical LDL-C. The task code records surrogate-run context
around R2 0.03 for clinical LDL-C and about R2 0.006 for NMR LDL-C.

Natural comparators are ApoB, non-HDL-C, triglycerides/remnant cholesterol, and
engineered lipidomics/Nightingale feature models. ApoB is the better particle
burden target when LDL-C and particle count are discordant.

## Physiological Time-Series V1

the internal evaluation configuration evaluates
a residual 1-D CNN trained end-to-end on target-blind samples from the baseline
10-second, 12-lead ECG against same-visit `ldl_nmr`. This is an exploratory
representation probe: no direct raw-ECG-to-LDL precedent was found in the
research review, and no Nightingale field is allowed in the model input.
Interpret held-out delta-R2 over age/sex/BMI as association evidence, not
lipid-panel replacement.

Held-out exploratory result (test n=884): temporal R² 0.0360 versus tuned
age/sex/BMI R² 0.0246, delta-R² +0.0114 (95% CI
[-0.0121, +0.0354]); temporal MAE 0.4892 versus 0.4964 mmol/L,
delta-MAE -0.0072 mmol/L (95% CI [-0.0152, +0.0010]). Both paired
intervals include zero, so this is not evidence of improvement.

## Caveats

- Statins and other lipid-lowering therapies can dominate LDL-C levels.
- Fasting status matters less than for triglycerides but source/assay route
  still matters.
- Same-panel Nightingale features can leak the NMR LDL target.
- LDL-C prediction is not the same as cardiovascular event prediction.
- Clinical LDL-C and NMR LDL-C should not be pooled without assay calibration.

## Metrics

Primary metric is R2. Secondary MAE should be reported in the task's native
units. For shared-card interpretation, report clinical and NMR rows separately
and compare demographic-floor delta R2 on matched support when possible.

## References

- Source material: `docs/task_cards/source_material/foundation-model-surrogate-targets-v1.md`
- Holmes et al., 2015, Mendelian randomization of blood lipids for coronary
  heart disease: <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4344957/>
- Sniderman et al., 2024, lipid discordance and apoB context:
  <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11242442/>
- Reicher et al. (2025), deep phenotyping of the health/disease continuum,
  *Nature Medicine*, <https://doi.org/10.1038/s41591-025-03790-9>. Local copy in **research-os**:
  `assets/papers/hpp/reicher_2025_deep_phenotyping_of_healthdisease_contin/`.

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29. V1 DXA and CGM are proposed for both clinical and
NMR LDL routes beyond age/sex/BMI. Every clinical/NMR/lipidomics sibling and
derived lipid score remains excluded to prevent same-assay reconstruction. See
`04-cardiovascular-lipid.md`.

## v0 Final-Test Status

The classical release is complete: Ridge/logistic and GBDT are remotely verified on every approved exact cohort and rendered in the Figure 1 task deep dives. TabSwift is deferred until GPU execution is configured; it is not a missing or failed row.

## Open Questions

- Which medication fields should be required for statin sensitivity analyses?
- Should `ldl` and `ldl_nmr` have a formal assay-concordance report before
  being compared side by side?
- Is ApoB the preferred headline lipid task for Q2 demos, leaving LDL-C as a
  comparator?
