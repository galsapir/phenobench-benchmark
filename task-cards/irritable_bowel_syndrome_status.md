# Irritable Bowel Syndrome Status Task Card

Status: draft

Task id: `irritable_bowel_syndrome_status`

Evidence status: grounded

Evidence reviewed: 2026-08-15

## Target

Participant-level binary classification of irritable bowel syndrome status from
the curated IBS phenotype table.

Implementation facts:

- target dataset release: `anat_curated_phenotype`
- target table: `anat.curated_phenotype.ibs`
- target column read: `curated_phenotype`. **This is hardcoded in the loader**
  (`hpp_loader.py:1450`), not taken from the Task
- `target_field` on the class is `ibs__curated_phenotype` and is **inert on
  this release** - it is read only by the alternate `frozen_v1_2` route
  (`_curated_phenotype_status.py:336`). Do not treat it as the operative field
- positive label: `Positive IBS Criteria`
- negative label: `No IBS diagnosis`
- excluded states: `Uknown`, missing
- default research stage: `00_00_visit`
- default covariates: age, sex, BMI from baseline anthropometrics
- primary metric: ROC AUC

## Why This Matters

Irritable bowel syndrome is a gastrointestinal condition selected in DS-1584.
It is particularly relevant for gut microbiome and multimodal evaluation, but
the first PhenoBench row is the demographic floor.

**What a row here does not support.** This is same-visit discrimination of a
curated status label built on Rome-IV-positive criteria. It is not a diagnosis -
IBS is a clinical diagnosis of exclusion requiring that organic disease be ruled
out, which a questionnaire-derived criteria label does not do - and it is not
subtype identification.

## Related HPP Measurements

Demonstrated in HPP and persisted in this repository, from
`docs/figure1/irritable_bowel_syndrome_status_review.json`,
test split:

- V1 gut species reaches test ROC AUC = 0.569 (95% CI [0.532, 0.610]) on a
  cohort of 11,726.
- V1 logged diet reaches ROC AUC = 0.537 (95% CI [0.478, 0.596]) on 5,046.

**Both are close to chance, and the diet interval includes 0.5.** On the largest
cohort in this card set, gut microbiome species barely discriminate this label
beyond age, sex and BMI. That is the honest headline for the modality this Task
was built to test, and it should be stated before any future positive result is
reported on a smaller or differently selected cohort.

The result is also a useful check on expectations set elsewhere: microbiome
associations with metabolic phenotypes in HPP are well documented, but they do
not automatically transfer to a symptom-criteria label.

**The logistic paired margins do not demonstrate lift beyond the floor**: gut
species **ΔAUROC = -0.024 (95% CI [-0.070, +0.027])** and logged diet
**+0.015 ([-0.032, +0.060])**, both spanning zero. So neither modality
demonstrably discriminates this label beyond age, sex and BMI - the raw AUROCs
near 0.55 are the floor.

Proposed rather than shown: that a subtype-aware or symptom-severity target
would be more separable than this binary. Nothing committed answers it.

**These are `reviewable` rows, not `final` ones.** Measured across the committed
leaderboards: all 787 rows carry `curation_state: reviewable` and none is
`final`. A complete fresh v0 re-run is committed to, so every figure in this
section is pre-re-run evidence that the re-run supersedes - persisted and citable
today, not a frozen result. **Which curation states the Figure 1 export accepts
is the export track's live question, not this card's**; read the two counts
above, not a gate.

## Clinically Meaningful Variants

The binary is already the categorical variant, and its boundary is a
questionnaire criteria set rather than a threshold.

**Rome IV criteria are the source of record and they are not a diagnosis.**
Rome IV defines IBS by recurrent abdominal pain with defecation-related features
over a specified period, and it explicitly operates after organic disease is
excluded. The curated label captures the criteria part; the exclusion part
happens in a clinic and is not represented here. So the label is best read as
*meets IBS symptom criteria*, and a row must not be reported as IBS detection or
prevalence.

Two further properties:

- **Subtype is collapsed.** Rome IV distinguishes IBS-C, IBS-D, IBS-M and IBS-U
  by stool pattern, and these have different biology and different plausible
  microbiome signals. Pooling them is a likely contributor to the near-chance
  result above, and separating them is the obvious next Task rather than a bin
  on this one.
- **Excluded is not negative.** `Uknown` - spelled as the upstream panel spells
  it - and missing are dropped rather than scored as controls.

## Baselines And Ceilings

The required floor is a no-modality-feature classifier baseline:
`NoFeaturesPredictor` contributes no modality features, and
`DemographicClassifierFloorStrategy` fits age, sex, and BMI.

Useful future comparators include gut microbiome species, diet/questionnaire
features, medication records, and MMFM participant embeddings.

## Caveats

- Labels come from the curated IBS panel and use its Rome-IV-positive status,
  not clinician-adjudicated IBS.
- IBS subtype and symptom severity are collapsed out of the binary label.
- A **Condition-Control** means `No IBS diagnosis` in the curated panel, not
  absence of all GI symptoms or GI diagnoses.

## Metrics

Primary: ROC AUC. Secondary: average precision, accuracy, balanced accuracy,
Brier score, positive rate, split sizes.

## References

- DS-1584 Yeela-selected condition curation:
  `pha_condition_projection/DS-1584/condition_candidates_detailed.csv`.
  **Does not resolve** in this repository or in research-os / research-harness /
  research-os-stable; kept because it is the only pointer to how this condition
  was selected, and marked so it is not read as a repo path.
- HPP refreshed curated-phenotype docs for `anat.curated_phenotype.ibs`.

## v0 Final-Test Status

- Two approved Benchmark Tracks use either a frozen 200-species MetaPhlAn-4
  panel or the exact V1 16-field diet panel, each with age, sex, and BMI.
- Logistic regression and GBDT produced four remotely verified rows. Best
  held-out AUROC was 0.569 for gut species and 0.537 for diet.
- Reported gain is over the matched demographic-only classifier. LOCF does not
  apply because this participant-level status Task has no prior-target input.
- These are cross-sectional discrimination results, not diagnostic or causal
  claims. TabSwift is deferred until GPU execution. Full contract and results:
  `05-sleep-gut-aging.md`.

## Open Questions

- Should a future Task expose IBS subtype or symptom-severity labels?
