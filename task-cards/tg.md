# Triglycerides Task Card

Status: draft

Task ids: `tg`, `tg_nmr`

Evidence status: grounded

Evidence reviewed: 2026-08-15

## Target

Fasting or same-visit triglyceride concentration. Continuous-scalar regression.
The default research stage is `00_00_visit`, but the Tasks can be configured
for another available stage. PhenoBench currently exposes two measurement
routes:

Implementation facts:

For `tg` (clinical blood test):

- target field: `bt__triglycerides`
- target dataset: `blood_tests`
- target source: `weizmann`
- target unit: mg/dL
- valid range: 20.0-1500.0 mg/dL
- primary metric: R2

For `tg_nmr` (Nightingale NMR):

- target field: `Total_TG`
- target dataset: `nightingale`
- target source: None (Nightingale's primary source is set in the loader)
- target unit: **mmol/L**, not "NMR units" - an earlier version of this card
  hedged the unit, and the hedge is what makes a threshold slip through
- valid range: 0.2-15.0 mmol/L
- primary metric: R2

Both default to `00_00_visit` with age/sex/BMI covariates at the configured
research stage. **The two ids are different measurements in different units on
different platforms, not two spellings of one target.**

## HPP data source

Target loads from the pinned Weizmann `blood_tests` source. The live operational source
HMO table was audited as a candidate replacement.
**Audit decision: keep Weizmann.** Rank agreement is high (ρ 0.990), but
operational source + `events` yields net −14.7% baseline coverage with ~33% cohort
turnover and the largest absolute tail (p99 |Δ| ≈ 45 mg/dL). Rationale and
reconsideration triggers:
blood-test source audit §9.

## Why This Matters

Triglycerides reflect triglyceride-rich lipoproteins, remnant metabolism, diet,
insulin resistance, sleep, alcohol, and activity. They are more lifestyle
responsive and noisier than LDL-C, making them useful for testing whether
multimodal representations capture dynamic metabolic state.

The clinical and NMR routes should be treated as paired assay views, not as
interchangeable labels.

**What a row here does not support.** A predicted triglyceride value is a
same-visit association, not a cardiovascular risk estimate and not a dietary or
lifestyle recommendation. Triglycerides also move with the fasting state, so a
row is a statement about this cohort's draw conditions as much as about biology.

## Related HPP Measurements

Demonstrated in HPP and persisted in this repository, from
`docs/figure1/tg_review.json`, test split:

- V1 DXA + demographics reaches test R2 = 0.210 (95% CI [0.153, 0.262]) on a
  cohort of 3,573.
- V1 CGM + demographics reaches R2 = 0.151 (95% CI [0.102, 0.195]) on 5,752.

**These are the largest lipid-family effects in this card set**, though that is a
cross-cohort observation rather than a tested ranking. The contrast with `ldl` on
the same two modalities is the point: LDL-C sits at 0.016 and
0.022, while triglycerides are clearly predictable from body composition and
glucose dynamics. **These are different cohorts, not one**: TG scores 3,573 and
5,752 participants, LDL 1,892 and 3,153, under four different `cohort_id`
hashes, and raw R2 across two targets are different estimands besides. So the
lifestyle-responsive versus genetically-driven reading stays a **hypothesis
consistent with an unmatched corpus comparison**, pending a common-support
evaluation - not something these rows establish.

**Both TG tracks clear the demographic floor on the paired comparison**, which
is the quantity a modality claim rests on: DXA **ΔR2 = +0.122 (95% CI [+0.086,
+0.166])** and CGM **+0.053 ([+0.017, +0.086])**. `ldl` on the same two
modalities does not clear its own floor (+0.004 and -0.014, both spanning zero).

Each of those is a within-track statement about its own cohort. Read together
they are consistent with the lifestyle-versus-genetic split, and they do not test
it: TG and LDL-C are different targets on different participants, so no paired
comparison exists here.

Related, in the wider HPP literature: Shilo et al. analysed the TG/HDL ratio
alongside other insulin-resistance surrogates in 10,114 non-diabetic HPP adults
and found the surrogates only moderately inter-correlated, capturing distinct
metabolic facets (Shilo et al. 2026). Triglycerides feed two of those surrogates
and the `tyg` Task, so a result here is entangled with that family by
construction.

**These are `reviewable` rows, not `final` ones.** Measured across the committed
leaderboards: all 787 rows carry `curation_state: reviewable` and none is
`final`. A complete fresh v0 re-run is committed to, so every figure in this
section is pre-re-run evidence that the re-run supersedes - persisted and citable
today, not a frozen result. **Which curation states the Figure 1 export accepts
is the export track's live question, not this card's**; read the two counts
above, not a gate.

## Clinically Meaningful Variants

**Triglyceride thresholds exist and are the most transferable in this family,
and three things still block a bin on these fields.**

- **Units, with a factor different from the other lipids.** Converting
  triglycerides between mmol/L and mg/dL uses ≈88.6 mg/dL per mmol/L, against
  ≈38.7 for cholesterol (see `ldl`). A single "NMR to clinical" rule applied
  across a lipid panel is wrong for at least one analyte, and wrong quietly.
- **The fasting state is not verified.** Clinical triglyceride cutoffs are
  stated for a defined fasting condition, and non-fasting values run higher.
  This Task's own title says "fasting or same-visit", and nothing in the Task
  checks which - the same unresolved fasting-metadata question `fpg` records.
- **Platform.** A Nightingale `Total_TG` is not the enzymatic assay the cutoffs
  were set on, and converting does not make it one.

The continuous targets stay primary on both routes.
`hyperlipidemia_status` is the supported categorical lipid route.

## Baselines And Ceilings

The required floor is a no-modality-feature baseline: `NoFeaturesPredictor`
contributes no modality features, and `DemographicFloorStrategy` fits age, sex,
and BMI. The task code records demographic floor R2 around 0.11-0.12.

Natural comparators include ApoB, LDL-C, TyG, fasting glucose, CGM summary
features, dietary features, sleep/OSA summaries, and engineered lipidomics or
NMR feature models. Same-assay lipid features are a high leakage risk.

## Caveats

- Triglycerides are highly variable and sensitive to fasting compliance,
  recent diet, alcohol, illness, and medication.
- CGM or diet features may legitimately predict TG via insulin resistance and
  carbohydrate exposure, but same-window interpretation should remain
  current-state, not prospective.
- NMR TG and clinical TG should not be merged without assay calibration.
- Strong TG prediction does not by itself imply remnant-cholesterol or MACE
  prediction.

## Metrics

Primary metric is R2. Secondary MAE should be reported in native units. Useful
audits include log-scale sensitivity, demographic-floor delta R2, matched
support across `tg`/`tg_nmr`, and medication/fasting-status sensitivity when
available.

## References

- Source material: `docs/task_cards/source_material/foundation-model-surrogate-targets-v1.md`
- Holmes et al., 2015, triglycerides in Mendelian-randomization CHD analysis:
  <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4344957/>
- Zhao et al., 2024, remnant cholesterol/triglycerides and cardiometabolic
  multimorbidity: <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10951224/>
- Shilo et al. (2026), heterogeneity of insulin-resistance surrogates,
  *medRxiv*, <https://doi.org/10.64898/2026.05.02.26352290>. Local copy in **research-os**:
  `assets/papers/hpp/shilo_2026_heterogeneity_of_insulin_resistance_surr/`.

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29. V1 DXA and CGM are proposed for both clinical and
NMR triglyceride routes beyond age/sex/BMI. Every clinical/NMR/lipidomics
sibling and lipid-derived score remains excluded to prevent same-assay
reconstruction. See
`04-cardiovascular-lipid.md`.

## v0 Final-Test Status

The classical release is complete: Ridge/logistic and GBDT are remotely verified on every approved exact cohort and rendered in the Figure 1 task deep dives. TabSwift is deferred until GPU execution is configured; it is not a missing or failed row.

## Open Questions

- Should the primary metric be computed on raw TG or log-transformed TG for
  heavy-tail robustness?
- What fasting-status evidence is available for the HPP blood draw used here?
- Which same-assay lipid features should be excluded from predictor allowlists?
