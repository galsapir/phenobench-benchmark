# ApoB Task Card

Task id: `apob`

Evidence status: grounded

Evidence reviewed: 2026-08-15

## Target

Apolipoprotein B concentration from the HPP Nightingale NMR panel.
Continuous-scalar regression. The default research stage is `00_00_visit`, but
the Task can be configured for another available stage.

Implementation facts:

- target field: `ApoB`
- target dataset: `nightingale`
- target source: None
- default research stage: `00_00_visit`
- valid range: 0.3-3.0 g/L
- primary metric: R2

## Why This Matters

ApoB approximates the number of atherogenic lipoprotein particles. It is often
more clinically informative than LDL-C when LDL-C and particle number are
discordant, especially in insulin resistance or hypertriglyceridemia.

For PhenoBench, ApoB is a strong lipid-axis target because the demographic
floor is low and the clinically meaningful signal should come from molecular,
dietary, metabolic, or genetic information rather than age/sex/BMI alone.

**What a row here does not support.** A predicted ApoB is a same-visit
association with an NMR panel value. It is not a cardiovascular risk estimate,
not a treatment indication, and not interchangeable with a clinical ApoB
immunoassay result, which is what every published ApoB threshold is defined on.

## Related HPP Measurements

Demonstrated in HPP and persisted in this repository, from the deep dive in
an internal review record, test split:

- The best raw scores come from GBDT: V1 CGM + demographics reaches test R2 =
  0.075 (95% CI [0.046, 0.106]) on a cohort of 9,137; V1 DXA + demographics
  reaches R2 = 0.029 (95% CI [-0.006, 0.059]) on 6,574.
- On the Ridge paired rows, CGM reaches **ΔR2 = +0.033 (95% CI [+0.014,
  +0.054])** and clears the demographic floor; DXA reaches **+0.003 ([-0.010,
  +0.017])** and does not.
- The GBDT paired deltas do not show the same split: CGM reaches +0.017
  ([-0.009, +0.043]) and DXA reaches -0.008 ([-0.031, +0.013]); both intervals
  cross zero.

Added CGM signal is therefore method-specific: Ridge demonstrates it here;
GBDT does not. Body composition adds nothing demonstrable with either method.

The contrast with `tg` survives and is better stated on the deltas: on DXA,
triglycerides clear the floor by +0.122 ([+0.086, +0.166]) where ApoB manages
+0.003 on Ridge. Those are different cohorts, so it is an unmatched corpus
comparison.

Proposed rather than shown: that dietary, genetic or learned representations
recover ApoB where DXA does not.

**These are `reviewable` rows, not `final` ones.** Measured across the committed
leaderboards: all 787 rows carry `curation_state: reviewable` and none is
`final`. A complete fresh v0 re-run is committed to, so every figure in this
section is pre-re-run evidence that the re-run supersedes - persisted and citable
today, not a frozen result. **Which curation states the Figure 1 export accepts
is the export track's live question, not this card's**; read the two counts
above, not a gate.

## Clinically Meaningful Variants

**ApoB is the one lipid target here with genuinely actionable thresholds, and
they still do not transfer to this measurement.** Guideline ApoB goals are
stated in mg/dL against risk stratum and are defined on standardised clinical
immunoassays. This Task's target is the **Nightingale NMR `ApoB` in g/L**. Two
independent mismatches block a bin:

- **Units.** g/L and mg/dL differ by a factor of 100, so a threshold applied
  without conversion is wrong by two orders of magnitude - the failure mode is
  silent, because both numbers look plausible in their own scale.
- **Platform.** Even converted, an NMR-derived ApoB is not the immunoassay the
  goals were validated against. Agreement between the two is an empirical
  question this repository has not measured, and until it is measured the
  conversion is arithmetic rather than equivalence.

A risk-stratified target is also not a diagnostic cutoff: ApoB goals depend on
the patient's cardiovascular risk category, so a single-threshold binary would
misrepresent the guideline even on the right assay in the right units.

The continuous target stays primary. If a categorical lipid Task is wanted, the
curated `hyperlipidemia_status` label is the supported route.

## Baselines And Ceilings

The required floor is a no-modality-feature baseline: `NoFeaturesPredictor`
contributes no modality features, and `DemographicFloorStrategy` fits age, sex,
and BMI. The task code records surrogate floor R2 around 0.02.

Natural comparators include LDL-C, non-HDL-C, triglycerides, and engineered
Nightingale/lipidomics feature models. A model that only improves LDL-C but not
ApoB should not be claimed to capture atherogenic particle burden broadly.

## Caveats

- ApoB can be medication-confounded, especially by statins and other
  lipid-lowering therapy.
- NMR ApoB is not the same assay as a clinical immunoassay; assay agreement
  should be checked before making clinical-equivalence claims.
- Same-visit lipid features may be direct or near-direct measurement leakage.
- A good ApoB score supports lipid-axis information, not prospective MACE
  prediction unless paired with incident outcomes.

## Metrics

Primary metric is R2. Secondary MAE is useful in g/L. Audit views should include
demographic-floor delta R2, split Ns, and medication/statin sensitivity when
available.

## References

- Source material: `docs/task_cards/source_material/foundation-model-surrogate-targets-v1.md`
- Thanassoulis et al., 2014, statin-trial meta-analysis relating apoB change to
  risk reduction: <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4187506/>
- Sniderman et al., 2024, apoB discordance and cardiovascular prevention:
  <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11242442/>
- Han et al. (2026), multi-omics dietary patterns and cardiometabolic risk,
  *medRxiv*, <https://doi.org/10.64898/2026.02.23.26346874>. Local copy in **HPP documentation**:
  `assets/papers/hpp/han_2026_multi_omics_characterization_of_biologic/`.

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29. literature and HPP review prioritizes V1 DXA
and CGM beyond age/sex/BMI. All lipid/Nightingale inputs remain excluded because
same-assay siblings can reconstruct ApoB. See
`04-cardiovascular-lipid.md`.

## v0 Final-Test Status

The classical release is complete: Ridge/logistic and GBDT are remotely verified on every approved exact cohort and rendered in the Figure 1 task deep dives.

## Open Questions

- Should clinical ApoB, if available in HPP blood chemistry, become a separate
  task or a validation check for NMR ApoB?
- What medication exclusion or stratification policy should be used for
  lipid-lowering therapy?
- Which lipidomics feature set should define the near-term engineered ceiling?
