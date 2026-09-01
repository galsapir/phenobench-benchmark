# Hyperlipidemia Status Task Card

Status: draft

Task id: `hyperlipidemia_status`

Evidence status: grounded

Evidence reviewed: 2026-08-15

## Target

Participant-level binary classification of hyperlipidemia status from curated
lipid phenotype axes.

Implementation facts:

- target dataset release: `anat_curated_phenotype` (the mixin default)
- target table: `anat.curated_phenotype.hyperlipidemia`, resolved from
  `anat_table = "hyperlipidemia"`
- target fields: `hypertriglyceridemia`, `hyperlipoproteinemia`,
  `combined_hyperlipoproteinemia`. This Task takes
  `_CompositeCuratedPhenotypeStatusMixin`, so the operative declaration is the
  plural `target_fields` plus the per-field positive/negative value maps; the
  singular `target_field` it inherits is **inert on this release**
- positive labels: `Hypertriglyceridemia`, `Hypercholesterolemia`,
  `High Cholesterol Values`, `Controlled Hypercholesterolemia`, combined
  hyperlipoproteinemia `True`
- negative labels: `Normal Triglycerides`, `Normal Cholesterol Values`,
  `High Normal`, combined hyperlipoproteinemia `False`
- excluded labels: `Borderline High LDL`, `Normal Triglycerides or Controlled
  by Omega-3`, missing
- default research stage: `00_00_visit`
- default covariates: age, sex, BMI from baseline anthropometrics
- primary metric: ROC AUC

## Why This Matters

Hyperlipidemia is a common cardiovascular risk state and one of the
Yeela-selected DS-1584 conditions with enough HPP support for evaluation.

This Task is not a duplicate of LDL-C, LDL-NMR, triglycerides, TG-NMR, or ApoB:
those Tasks measure continuous lipid biomarkers, while this Task evaluates a
diagnosis-style condition label.

**What a row here does not support.** This is same-visit discrimination of a
curated composite label. It is not a diagnosis, not a cardiovascular risk
estimate, and not incident-hyperlipidemia prediction. Several positive values
name *treated* states - `Controlled Hypercholesterolemia` is a positive - so the
label mixes untreated biology with successfully treated biology, and a model can
score well by detecting either.

## Related HPP Measurements

Demonstrated in HPP and persisted in this repository, from
`docs/figure1/hyperlipidemia_status_review.json`,
test split:

- V1 CGM + demographics reaches test ROC AUC = 0.704 (95% CI [0.655, 0.749]) on
  a cohort of 3,487.
- V1 DXA + demographics reaches ROC AUC = 0.697 (95% CI [0.635, 0.753]) on
  2,350.

**Both clear chance and NEITHER clears the demographic floor**, and the second
half is the one that matters. On the logistic paired rows: DXA
**ΔAUROC = -0.002 (95% CI [-0.045, +0.041])** and CGM
**-0.002 ([-0.023, +0.021])** - both centred on zero. So the ~0.70 AUROCs above
are largely age, sex and BMI, and neither body composition nor glucose dynamics
demonstrates incremental discrimination under these probes.

An earlier version of this card read those AUROCs as a contrast with `ldl`
("clear chance comfortably"). Against the floor the two Tasks agree rather than
contrast: incremental value beyond demographics is not demonstrated for either
the continuous LDL-C target or this label on these tracks.

**These are `reviewable` rows, not `final` ones.** Measured across the committed
leaderboards: all 787 rows carry `curation_state: reviewable` and none is
`final`. A complete fresh v0 re-run is committed to, so every figure in this
section is pre-re-run evidence that the re-run supersedes - persisted and citable
today, not a frozen result. **Which curation states the Figure 1 export accepts
is the export track's live question, not this card's**; read the two counts
above, not a gate.

## Clinically Meaningful Variants

The binary is already the categorical variant, and the live question is what its
boundary means.

**The curated label is not a threshold classification and must not be reported
as one.** Clinical hyperlipidemia definitions rest on lipid cutoffs that are
risk-stratified rather than diagnostic, stated per analyte and per assay - and
this label instead composes three curated axes (`hypertriglyceridemia`,
`hyperlipoproteinemia`, `combined_hyperlipoproteinemia`) with an explicit
value-by-value positive and negative mapping. Reconstructing it from the `ldl`,
`tg` or `apob` fields would mint a fourth definition rather than apply a
validated one, and would additionally cross the unit and platform boundaries
those cards document.

Three properties of this label to state plainly:

- **Treated states count as positive.** `Controlled Hypercholesterolemia` is a
  positive value, so the label is closer to "has this diagnosis" than to "has
  abnormal lipids now".
- **Excluded is not negative.** `Borderline High LDL` and `Normal Triglycerides
  or Controlled by Omega-3` are dropped, not scored as controls, so the positive
  rate is not a cohort prevalence.
- **Every lipid measurement is excluded from predictors by design**, because
  they define or reveal the label. That exclusion is what makes the DXA and CGM
  numbers above meaningful rather than circular.

## Baselines And Ceilings

The required floor is a no-modality-feature classifier baseline:
`NoFeaturesPredictor` contributes no modality features, and
`DemographicClassifierFloorStrategy` fits age, sex, and BMI.

Useful future comparators include lipid panels, lipidomics, medication-aware
clinical models, gut microbiome species, and MMFM participant embeddings.

## Caveats

- Labels come from curated lipid phenotype axes, not adjudicated chart
  diagnosis.
- The refreshed `curated_phenotype` headline is a degenerate
  placeholder; this Task intentionally uses the documented sibling fields.
- A **Condition-Control** means curated lipid-axis values are normal/non-mixed
  under this Task's map; it does not mean globally healthy.
- Supporting lipid columns inside `anat.curated_phenotype.hyperlipidemia` are
  curated recompute inputs, not raw live biomarker features.
- Lipid-lowering medication use may weaken or invert biomarker associations.
- Continuous lipid Tasks remain the cleaner target when the scientific question
  is lipid concentration rather than diagnosis status.

## Metrics

Primary: ROC AUC. Secondary: average precision, accuracy, balanced accuracy,
Brier score, positive rate, split sizes.

## References

- DS-1584 Yeela-selected condition curation:
  `pha_condition_projection/DS-1584/condition_candidates_detailed.csv`.
  **Does not resolve** in this repository or in research-os / research-harness /
  research-os-stable; kept because it is the only pointer to how this condition
  was selected, and marked so it is not read as a repo path.
- HPP `curated_phenotypes` dataset docs for the hyperlipidemia sibling fields.

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29. V1 DXA and CGM are proposed beyond age/sex/BMI.
All lipid measurements, derived scores, and curated recompute columns remain
excluded because they define or reveal this composite label. See
`04-cardiovascular-lipid.md`.

## v0 Final-Test Status

The classical release is complete: Ridge/logistic and GBDT are remotely verified on every approved exact cohort and rendered in the Figure 1 task deep dives. TabSwift is deferred until GPU execution is configured; it is not a missing or failed row.

## Open Questions

- Should future versions exclude participants with lipid-lowering medication
  exposure or model it as a covariate?
- Should `Borderline High LDL` and `Normal Triglycerides or Controlled by
  Omega-3` stay excluded, or become a separate broader hyperlipidemia target?
