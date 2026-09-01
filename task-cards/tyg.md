# TyG Task Card

Status: draft

Task id: `tyg`

Evidence status: grounded

Evidence reviewed: 2026-08-15

## Target

TyG is the Triglyceride-Glucose index, a fasting-blood insulin-resistance
surrogate:

```text
TyG = ln(triglycerides_mg_dl * fasting_glucose_mg_dl / 2)
```

Implementation facts:

- target field: `None`; this is a derived formula target, computed from
  `bt__triglycerides` and `bt__glucose` rather than read from a column
- target dataset: `None`; the target is not read from a dataset directly
- `benchmark_target_field`: `tyg` - this is the name the Benchmark Track sees
- target dataset the formula reads: `blood_tests`
- target source: `weizmann`
- target unit: unitless index
- default research stage: `00_00_visit`
- valid range: `6.0` to `13.0`
- primary metric: `r2`

The component windows are applied before computing the product:
triglycerides `20` to `1500` mg/dL and glucose `40` to `400` mg/dL.
`bt__glucose` follows the `FpgTask` convention and is treated as fasting
glucose.

## HPP data source

The triglyceride and glucose inputs load from the pinned Weizmann `blood_tests`
source. The live operational source HMO table was audited as a candidate replacement.
**Audit decision: keep Weizmann.** Agreement is strong, but operational source + `events`
yields net −19.0% baseline coverage with ~36% cohort turnover and no offsetting
gain. Rationale and reconsideration triggers:
blood-test source audit §9.

## Why This Matters

TyG is cheap, scalable, and biologically adjacent to insulin resistance. It is
not a clamp measurement and should not be read as a direct insulin-resistance
phenotype. In PhenoBench it is useful as a reporting target and as a candidate
metabolic axis for probing whether embeddings add signal beyond demographics.

The §P CGM-side contribution check found that TyG should not currently count
as a clean CGM-sleep bimodal target. CGM's apparent TyG signal is explained by
the fasting-glucose factor: on the pre-registered screen, CGM's incremental ΔR²
over `demo + ln(FPG)` was **−0.000, 95% CI [−0.032, +0.029]** (n = 353
validation participants), against a raw CGM lift over demographics of +0.040
CI [−0.011, +0.094] which itself crosses zero. Sleep carried independent signal
(+0.066, CI [+0.022, +0.110]), so TyG remains reportable but not the
mechanism-bimodal slot. Derivation and the frozen pass rule are in the
foundation_models sweep cited below, **not in this repository**.

**What a row here does not support.** TyG is a formula over two fasting
laboratory values. Predicting it well is not a measurement of insulin
resistance, is not a clamp-equivalent result, and is not a statement about
diabetes risk. Because the formula contains fasting glucose outright, a
glucose-adjacent modality can score well by reconstructing one factor - which is
exactly what the screen above measured and found.

## Related HPP Measurements

Demonstrated in HPP:

- **IR surrogates do not identify the same people.** Shilo et al. analysed TyG
  alongside TyG-BMI, METS-IR, TG/HDL and FPG in 10,114 non-diabetic HPP adults
  aged 35-75 and found them *moderately inter-correlated but capturing distinct
  metabolic facets* (Shilo et al. 2026). So a result on TyG does not transfer to
  "insulin resistance" as a construct, and it does not transfer to another
  surrogate.
- **CGM predicts visceral fat weakly, and anthropometry predicts it well.** In
  the same cohort, DEXA-derived VAT is predicted at R² = 0.659 from
  anthropometrics alone but only R² = 0.078 from CGM features, with glycemic
  *variability* markers outperforming mean-glucose metrics (Shilo et al. 2026).
  That is the adiposity-dominance this card's floor discussion assumes, measured.
- 1.2% of the HPP cohort carry elevated visceral adiposity despite both a normal
  BMI and a normoglycemic HbA1c (Shilo et al. 2026) - the discordant group any
  demographics-plus-BMI floor is blind to by construction.

**The committed corpus adds a second, larger measurement that agrees with the
screen's direction on CGM and disagrees on sleep.** Against the demographic
floor: DXA **ΔR2 = +0.182 (95% CI [+0.124, +0.240])** on n = 3,514 clears
comfortably, while sleep **+0.016 ([-0.012, +0.047])** on n = 4,036 does not.
The foundation_models screen found sleep carrying independent TyG signal on 353
validation participants (+0.066 [+0.022, +0.110]); this larger committed cohort
does not reproduce that. Two different cohorts, splits and feature routes, so
neither supersedes the other - but the sleep claim is not settled, and the card
should not be read as though it were.

Proposed rather than shown: that a learned representation adds TyG signal beyond
demographics *and* beyond `ln(FPG)`. The screen answers that for CGM only.

## Clinically Meaningful Variants

**No categorical TyG variant is defensible, and the reason is stronger here than
for a measured analyte: TyG has no diagnostic threshold to transfer.** Published
TyG cutoffs for identifying insulin resistance are derived per study population
against a local reference standard, and they move with the assay units of both
components, the fasting protocol, and the population's adiposity distribution.
There is no guideline cutoff comparable to FPG ≥126 mg/dL or HbA1c ≥6.5%.

Two further blocks specific to this Task:

- **The index inherits two assays.** A threshold applied to a TyG computed from
  a different triglyceride or glucose method is not the same threshold. The
  components here are pinned to Weizmann `blood_tests`; a source swap changes
  the index distribution without changing the formula.
- **The construct is not the target.** Since HPP's own surrogates disagree with
  each other (above), binning TyG would produce an "insulin resistant" label
  that neither the clamp nor another surrogate would reproduce.

If a categorical insulin-resistance Task is wanted, the defensible route is a
measured one - fasting insulin or a clamp-anchored reference where available -
not a bin on this index. That is the open question below, already recorded.

## Baselines And Ceilings

The default floor is a no-modality-feature baseline: `NoFeaturesPredictor`
contributes no modality features, and `DemographicFloorStrategy` fits age, sex,
and BMI. This matters because adiposity can dominate insulin-resistance
surrogates; any embedding result should be interpreted as lift over that
demographic floor, not as raw TyG predictability.

For CGM-specific interpretation, compare against a model that controls for
`ln(FPG)`. A CGM lift that disappears after this control is glucose
reconstruction, not evidence that CGM encodes the triglyceride component.

## Caveats

- Formula-derived target: TyG includes glucose directly, so CGM predictors can
  look useful by reconstructing the glucose term.
- Fasting assumption: `bt__glucose` is treated as fasting glucose by convention;
  any upstream source drift would change interpretation.
- Insulin-resistance proxy: TyG is not clamp-measured insulin resistance.
- Adiposity confounding: demographic and BMI signal should be expected.
- Cohort intersections can be much smaller than the full TG/FPG cohort when
  frozen CGM and sleep embedding caches are required.
- In the 2026-06-20 CGM/sleep screen, `n_tyg` is validation/eval n, not the
  full train+val accessible cohort.

## Metrics

Primary metric is `r2` on the configured eval split. For modality-claiming
work, report demographic-floor ΔR² and, for CGM, a nested
`demo + ln(FPG)` control. For CGM-sleep claims, use paired within-target
comparisons rather than cross-target R² subtraction.

## References

- Simental-Mendía et al., 2008: original TyG index.
- Guerrero-Romero et al., 2010: TyG validation against clamp-derived insulin
  resistance.
- Shilo et al. (2026), heterogeneity of insulin-resistance surrogates in 10,114
  non-diabetic HPP adults, *medRxiv*,
  <https://doi.org/10.64898/2026.05.02.26352290>.
- **foundation_models** `sweeps/tyg_cgm_contribution_check_20260620/iteration_summary.md`:
  the frozen pre-registration and the measured CGM-side contribution screen
  (C1-C4 criteria, results run 2026-06-20). **That path is in the
  foundation_models repository, not phenobench** - an earlier version of this
  card cited it as if it resolved here, and it does not.

## Open Questions

- Whether a measured-insulin surrogate should replace TyG as the next
  mechanism-bimodal candidate.
- Whether future cache expansion changes the CGM-over-`ln(FPG)` result enough
  to reopen TyG's bimodal-target status.
