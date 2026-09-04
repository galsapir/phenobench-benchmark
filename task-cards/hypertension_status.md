# Hypertension Status Task Card

Task id: `hypertension_status`

Evidence status: grounded

Evidence reviewed: 2026-08-15

## Target

Binary curated hypertension phenotype. The default research stage is
`00_00_visit`, but the Task can be configured for another available stage.

Implementation facts:

- target dataset release: `anat_curated_phenotype`
- target table: `anat.curated_phenotype.hypertension`
- target column read: `curated_phenotype`. **This is hardcoded in the loader**
  (an internal review record), not taken from the Task
- `target_field` on the class is `hypertension__curated_phenotype` and is **inert on
  this release** - it is read only by the alternate `frozen_v1_2` route
  (`_curated_phenotype_status.py:336`). Do not treat it as the operative field
- default research stage: `00_00_visit`
- positive label: `Hypertension`
- negative label: `Non hypertensive`
- excluded states: `High BP without diagnosis of hypertension`, `Suspected
  hypertension`, missing
- primary metric: ROC AUC

## Why This Matters

This task captures the first Xue oral-microbiome disease-classification surface
as a reusable HPP disease-status benchmark. The initial config tests oral
MetaPhlAn species abundances against curated hypertension labels on canonical
splits.

**What a row here does not support.** This is same-visit discrimination of a
curated status label. It is not a diagnosis, not incident-hypertension
prediction, and not evidence of screening utility. The label is a curation
product, so a high AUC states that the curation is recoverable, not that
hypertension is being detected.

## Related HPP Measurements

Demonstrated in HPP and persisted in this repository, from
an internal review record,
test split:

- V1 fundus + demographics reaches test ROC AUC = 0.805 (95% CI [0.762, 0.845])
  on a cohort of 4,025.
- V1 sleep + demographics reaches ROC AUC = 0.743 (95% CI [0.700, 0.786]) on
  5,125.

Retinal microvascular structure leading is the same ordering the continuous
`sbp` Task shows (fundus R2 = 0.374 against sleep's 0.255), which is a
consistency check across two different targets on the same axis rather than an
independent finding.

**On the logistic paired comparison the two committed tracks split.** Fundus
reaches **ΔAUROC = +0.040 (95% CI [+0.013, +0.067])** on n = 4,025 and clears
the demographic floor; sleep reaches **+0.009 ([-0.002, +0.020])** on n = 5,125
and does not. So the raw AUROCs above (0.805 and 0.743) are mostly floor, and
only the fundus track demonstrates added signal.

Still proposed rather than shown: the oral-microbiome track this Task was
actually built for. That is the Xue-inspired configuration, and no committed row
answers it.

**These are `reviewable` rows, not `final` ones.** Measured across the committed
leaderboards: all 787 rows carry `curation_state: reviewable` and none is
`final`. A complete fresh v0 re-run is committed to, so every figure in this
section is pre-re-run evidence that the re-run supersedes - persisted and citable
today, not a frozen result. **Which curation states the Figure 1 export accepts
is the export track's live question, not this card's**; read the two counts
above, not a gate.

## Clinically Meaningful Variants

The binary is already the categorical variant. The live question is what its
boundary excludes.

**The curated label is not a threshold classification and must not be reported
as one.** Clinical hypertension is defined by a diagnostic procedure - repeated
readings on separate occasions under specified conditions, with ambulatory or
home confirmation where white-coat or masked hypertension is suspected - not by
a single number. Reconstructing this label from the `sbp` field would apply a
cutoff to the mean of two sitting readings at one visit, which is not that
procedure, and `sbp` records why in more detail.

Two properties of this label to state plainly:

- **Excluded is not negative, and the exclusions are exactly the ambiguous
  cases.** `High BP without diagnosis of hypertension` and `Suspected
  hypertension` are dropped rather than scored as controls. That is the right
  call for label quality, and it means the operating population omits the
  boundary group a screening tool would most need to resolve - so the AUC above
  is measured on an easier problem than screening.
- **Treated hypertension reads as positive while presenting with normal
  pressure**, so any feature set that detects treatment effects rather than
  pressure biology will score well.

## Baselines And Ceilings

- **Floor**: demographic classifier baseline.
  `DemographicClassifierFloorStrategy` fits age, sex, and BMI.
- **Paper-inspired track**: `oral_microbiome_abundance` species features with
  manifest read-count QC (`metaphlan4_aligned_read_count >= 5000`).

## Caveats

- The Xue paper's exact hypertension case count differs from the current
  curated-phenotype route; this is HPP-native canonical-split ingestion, not
  exact paper parity.
- Intermediate BP states are excluded, not treated as controls.
- No phenotype-filtered oral marker selection is applied yet. Any future marker
  selection must be train-fold-only.

## Metrics

Primary: ROC AUC. Secondary: average precision, accuracy, balanced accuracy,
Brier score, positive rate, split sizes.

## References

- Xue oral microbiome disease-classification paper artifacts in HPP documentation.
- HPP documentation run: `research_runs/phenobench-paper-task/xue_oral_microbiome_2026_06_21/`.

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29. V1 sleep and fundus morphology are proposed
beyond age/sex/BMI. Same-visit BP, vascular measurements, and derived
hypertension fields remain excluded. See
`04-cardiovascular-lipid.md`.

## v0 Final-Test Status

The classical release is complete: Ridge/logistic and GBDT are remotely verified on every approved exact cohort and rendered in the Figure 1 task deep dives.

## Open Questions

- Should Xue follow-up add MAFLD, obesity, prediabetes, and hypercholesterolemia
  as separate disease-status Tasks?
- Should oral marker selection become a reusable Strategy?
