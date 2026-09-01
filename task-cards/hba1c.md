# HbA1c Task Card

Status: draft

Task id: `hba1c`

Evidence status: grounded

Evidence reviewed: 2026-08-15

## Target

Cross-sectional HbA1c regression on HPP V1.

Implementation facts:

- target field: `bt__hba1c`
- target unit: percent (NGSP/DCCT units, not IFCC mmol/mol)
- target dataset: `blood_tests`
- target source: `weizmann`
- default research stage: `00_00_visit`
- valid range: 3.0-15.0 percent; a PhenoBench plausibility filter, not a
  diagnostic interval
- primary metric: R2

## HPP data source

Target loads from the pinned Weizmann `blood_tests` source. The live operational source
HMO table was audited as a candidate replacement.
**Audit decision: keep Weizmann.** Paired agreement is strong (94.9% exact), but
operational source + `events` yields net −3.5% baseline coverage with ~23% cohort
turnover and no offsetting gain, and 998 operational source participants carry hba1c with
no recorded unit (`%` vs `mmol/mol`). Rationale and reconsideration triggers:
blood-test source audit §9.

## Why This Matters

HbA1c is the standard long-horizon glycemic marker. It captures average glucose
exposure over weeks to months and is clinically tied to diabetes diagnosis,
diabetes progression, microvascular complications, and cardiovascular risk.

For multimodal foundation-model evaluation, HbA1c is a direct metabolic target:
CGM-derived signals should have a plausible route to predicting it. That makes
it useful as an early sanity check for whether an embedding contains metabolic
information beyond demographics.

**What a row here does not support.** A predicted HbA1c is a same-visit
association with one laboratory value. It is not a diagnosis, does not establish
glycemic control over any future period, and says nothing about microvascular or
cardiovascular outcomes - those are the endpoints HbA1c is *validated against*
in the clinical literature, not endpoints this Task measures.

## Related HPP Measurements

Demonstrated in HPP, and one of these should temper the expectation above:

- **In this cohort's non-diabetic range, CGM time-in-range and HbA1c are almost
  unrelated.** Godneva et al., 8,687 HPP adults, report TIR correlating with
  HbA1c at r = 0.04, with time in tight range showing no significant
  association at all - while the same TIR correlates with mean glucose at
  r = 0.62 and with the glucose management indicator at r = 0.63
  (Godneva et al. 2026). So "CGM should predict HbA1c" holds for *mean-glucose*
  summaries far better than for range-occupancy summaries, and the restricted
  non-diabetic range is doing much of the work.
- Time above 140 mg/dL carries prospective signal for incident metabolic
  conditions (age- and sex-adjusted HR 1.34, 95% CI 1.26-1.42), which HbA1c
  itself is not shown to capture here (Godneva et al. 2026).
- CGMap gives the HPP reference distribution of CGM-derived measures in
  non-diabetic individuals (Keshet et al. 2023).

**A matched-cohort comparison is already committed, and an earlier version of
this card said none was.** On the snapshot's `Matched-cohort comparison` track,
n = 1,103, the full IGLU panel reaches **ΔR2 = +0.105 (95% CI [+0.010, +0.202])**
over the demographic floor, while Nightingale metabolites
(+0.005 [-0.030, +0.035]), DXA regional lean mass and grip strength all span
zero. So CGM summaries clear the floor on matched support and the other
modalities do not - which is the comparison this card asked for.

Read that against the Godneva reading above rather than instead of it: the IGLU
panel is mean-glucose-like, and it is range-occupancy that fails to track HbA1c.

Proposed rather than shown: that a *learned* CGM representation beats the
engineered panel. The physiological-time-series ECG route below is the one place
a clearly negative answer is already recorded.

## Clinically Meaningful Variants

**A categorical HbA1c Task is more defensible than a categorical FPG one, and
still not defensible on this measurement as configured.** ADA classifies
HbA1c ≥6.5% as diabetes and 5.7-6.4% as prediabetes (ADA 2026), and unlike a
fasting draw HbA1c integrates weeks of exposure, so it is far less sensitive to
day-of-visit state. Three things block a threshold Task here anyway:

- **Units and assay alignment are not incidental.** The target is in NGSP/DCCT
  percent; IFCC mmol/mol is the other reporting scale, and a threshold applied
  to the wrong scale is silently wrong rather than loudly wrong. The blood-test
  source audit already found 998 operational source participants carrying an hba1c
  value with **no recorded unit**, which is exactly this failure waiting to
  happen on a source swap.
- **HbA1c is not a pure glucose readout.** Anything shortening red-cell
  lifespan biases it downward - modelled and verified for T2DM patients by
  Zhang et al. (2025) - and haemoglobin variants shift it independently of
  glycemia, with Kerdsinchai et al. (2025) reporting significantly lower HbA1c
  in non-diabetic haemoglobin H disease and calling for disease-specific
  reference ranges. A binary Task inherits that bias as label error concentrated
  in a subpopulation, which a continuous target merely blurs.
- The cohort is largely non-diabetic by construction, so a ≥6.5% positive class
  would be small and the boundary class (5.7-6.4%) would dominate - the same
  class-degeneracy hazard `t2d_status` documents for hash splits.

The continuous target stays primary. `prediabetes_status` and `t2d_status` are
the supported categorical glycemic routes, and both take labels from the curated
diabetes phenotype rather than from a threshold on this field.

## Baselines And Ceilings

The required floor is a no-modality-feature baseline: `NoFeaturesPredictor`
contributes no modality features, and `DemographicFloorStrategy` fits age, sex,
and BMI.

Meaningful model claims should clear that floor on the same cohort and split.
For CGM-adjacent models, simple glucose-summary or IGLU-feature baselines are
strong comparators, because HbA1c is closely tied to mean glucose.

Expected demographic floor from the source material is roughly R2 0.10-0.18,
mostly age-driven. Empirical HPP floors should be treated as the authority once
available.

## Physiological Time-Series V1

the internal evaluation configuration evaluates
a residual 1-D CNN trained end-to-end on target-blind samples from the baseline
10-second, 12-lead ECG. It is a same-visit representation probe inspired by
published raw-ECG HbA1c prediction, not forecasting and not a substitute for
laboratory HbA1c. The primary result is held-out delta-R2 versus the
age/sex/BMI floor on identical support.

Held-out exploratory result (test n=343): temporal R² 0.0127 versus tuned
age/sex/BMI R² 0.1143, delta-R² -0.1016 (95% CI
[-0.1730, -0.0390]); temporal MAE 0.3237% versus 0.2983%, delta-MAE
+0.0254% (95% CI [+0.0128, +0.0385]). This route did not beat
demographics.

## Caveats

- HbA1c is not pure glucose exposure. RBC lifespan, hemoglobinopathies, anemia,
  and other non-glycemic biology can shift it.
- Medication changes can dominate longitudinal HbA1c deltas.
- A model that mainly learns age, sex, or BMI is not clinically interesting for
  this task, even if raw R2 looks acceptable.
- CGM-derived features have a strong path to HbA1c, so failure here is a useful
  negative signal for metabolic encoders.
- Conversely, success here alone is not enough to claim broad metabolic
  understanding.

## Metrics

- Primary: R2.
- Secondary: MAE.
- Useful audit views: residualized performance after demographics, split Ns,
  cohort ID, and comparison to CGM-feature baselines.

## References

- Source material: `docs/task_cards/source_material/foundation-model-surrogate-targets-v1.md`
- UK Biobank HbA1c field 30750: <https://biobank.ndph.ox.ac.uk/ukb/field.cgi?id=30750>
- HbA1c and cardiovascular disease meta-analysis: <https://pubmed.ncbi.nlm.nih.gov/15381515/>
- Godneva et al. (2026), the spectrum of normoglycemia and time in glycemic
  ranges, *Diabetes Care*, <https://doi.org/10.2337/dc25-2154>. Source of the
  TIR-HbA1c r = 0.04 reading above.
- Keshet et al. (2023), CGMap, *Cell Metabolism*,
  <https://doi.org/10.1016/j.cmet.2023.04.002>.
- ADA Standards of Care in Diabetes 2026, diagnosis and classification,
  <https://doi.org/10.2337/dc26-S002>.
- Zhang et al. (2025), rectifying the impact of shorter red blood cell lifespan
  on HbA1c, *Frontiers in Endocrinology*,
  <https://doi.org/10.3389/fendo.2025.1500660>.
- Kerdsinchai et al. (2025), HbA1c levels in haemoglobin H disease,
  *Biochemistry and Biophysics Reports*,
  <https://doi.org/10.1016/j.bbrep.2025.102165>.

## Open Questions

- What HPP empirical floor should become the canonical threshold for "clears
  demographics"?
- Which CGM-feature baseline is the right near-term ceiling: IGLU, mean glucose,
  or a broader engineered-feature model? The Godneva reading argues for a
  mean-glucose summary over a range-occupancy one, but that is an inference from
  a correlation table, not a measured PhenoBench comparison.
- Should longitudinal HbA1c delta become a separate task card rather than a
  variant of this one?
- Does HPP record haemoglobinopathy or anaemia status well enough to flag the
  participants whose HbA1c is biased for non-glycemic reasons? Unresolved, and
  it bounds how far a residual analysis can go.
