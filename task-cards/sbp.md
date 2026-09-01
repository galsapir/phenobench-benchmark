# Systolic Blood Pressure Task Card

Status: draft

Task id: `sbp`

Evidence status: grounded

Evidence reviewed: 2026-08-15

## Target

Participant systolic blood pressure, computed from the available sitting
systolic readings. Continuous-scalar regression. The default research stage is
`00_00_visit`, but the Task can be configured for another available stage.

Implementation facts:

- target fields: `sitting_blood_pressure_systolic`,
  `sitting_second_blood_pressure_systolic`
- combination rule: **row-wise NaN-safe mean of the two sitting readings**, not
  a single field. A participant with one reading contributes that reading
- target dataset: `blood_pressure`
- target source: None
- target unit: mmHg
- default research stage: `00_00_visit`
- valid range: 60.0-300.0 mmHg, **applied to the averaged value** rather than to
  either reading individually - averaging happens first
- primary metric: R2

## Why This Matters

SBP is one of the strongest routine cardiovascular risk factors and a
treatment target with randomized-trial evidence that lowering SBP reduces
cardiovascular events. It is also influenced by sleep, activity, diet,
adiposity, medication, and measurement context, so it is a useful multimodal
current-state target.

**What a row here does not support.** A predicted SBP is a same-visit
association with the mean of two sitting readings taken at one research visit.
It is not a blood-pressure diagnosis, not an ambulatory or home BP estimate, and
not a cardiovascular risk estimate. The trial evidence that makes SBP matter is
evidence about *lowering* it, which prediction does not touch.

## Related HPP Measurements

Demonstrated in HPP and persisted in this repository, from
`docs/figure1/sbp_review.json`, test split:

- V1 fundus + demographics reaches test R2 = 0.374 (95% CI [0.329, 0.418]) on a
  cohort of 7,803.
- V1 sleep + demographics reaches R2 = 0.255 (95% CI [0.211, 0.298]) on 9,425.

Both sit above the demographic floor this card records (~0.27) only in the
fundus case; the sleep track is close to it, so the sleep number should not be
read as added physiological signal without the paired floor comparison on
matched support. Retinal microvascular structure carrying the stronger SBP
signal is the expected direction - the fundus vessels are a target organ of
chronic pressure - and it is consistent with the related `cimt` and
`hypertension_status` tracks, where fundus also leads.

**The paired margins are committed, and both clear the floor - but the sleep one
is method-specific.** Fundus reaches **ΔR2 = +0.084 (95% CI [+0.058, +0.112])**
on n = 7,803. Sleep reaches **+0.016 ([+0.007, +0.026])** on n = 9,425 for the
Ridge row, while the gradient-boosted row on the same track is
+0.007 ([-0.007, +0.023]) and spans zero. So sleep adds a small but real margin
under one method and an undemonstrated one under the other, and any claim on
that track should name the method. An earlier version of this card said the
paired comparison was missing; it is in the snapshot.

Proposed rather than shown: that either margin reflects pressure biology rather
than shared age and adiposity structure.

**These are `reviewable` rows, not `final` ones.** Measured across the committed
leaderboards: all 787 rows carry `curation_state: reviewable` and none is
`final`. A complete fresh v0 re-run is committed to, so every figure in this
section is pre-re-run evidence that the re-run supersedes - persisted and citable
today, not a frozen result. **Which curation states the Figure 1 export accepts
is the export track's live question, not this card's**; read the two counts
above, not a gate.

## Clinically Meaningful Variants

**A categorical SBP variant is not defensible on this measurement, and the
reason is measurement protocol rather than the absence of a threshold.**
Hypertension thresholds are well defined and clinically actionable - but they
are defined on a *diagnostic procedure*, not on a number: repeated readings on
separate occasions, with specified rest, posture and cuff conditions, and
increasingly with ambulatory or home confirmation because white-coat and masked
hypertension are common. This target is the mean of two sitting readings at one
visit, which is a research measurement, not that procedure.

Two further blocks:

- **Treatment is invisible.** Participants on antihypertensives sit lower
  *because* of treatment, so a threshold bin would place controlled hypertensive
  participants among the normotensive and label the untreated as the disease
  group. The Task does not model medication.
- **The averaging rule interacts with the threshold.** Because the valid range
  and any bin would apply to the mean of two readings, a participant with one
  extreme and one normal reading crosses or misses a cutoff by an averaging
  convention rather than by physiology.

`hypertension_status` is the supported categorical route on this axis, and it
takes its label from the curated phenotype rather than from a threshold on this
field - which is also why that Task excludes `High BP without diagnosis of
hypertension` and `Suspected hypertension` instead of scoring them as controls.

## Baselines And Ceilings

The required floor is a no-modality-feature baseline: `NoFeaturesPredictor`
contributes no modality features, and `DemographicFloorStrategy` fits age, sex,
and BMI. The task code records a moderate-to-high demographic floor around R2
0.27.

Natural comparators include antihypertensive-aware clinical models, repeated
BP summaries, activity/sleep features, and vascular-imaging features. A row
must clear the demographic floor before claiming added physiological signal.

## Caveats

- Antihypertensive medication can suppress the observed target and confound
  apparent predictor effects.
- Single-visit BP is noisy; posture, cuff, timing, stress, and white-coat
  effects matter.
- Same-visit BP-derived features are direct leakage.
- Regression on SBP is not equivalent to incident hypertension or MACE
  prediction.

## Metrics

Primary metric is R2. Secondary MAE in mmHg is clinically interpretable.
Useful audits include demographic-floor delta R2, medication sensitivity,
split Ns, and high/low BP subgroup error.

## References

- Source material: `docs/task_cards/source_material/foundation-model-surrogate-targets-v1.md`
- Canoy et al., 2022, blood-pressure lowering and cardiovascular prevention:
  <https://doi.org/10.1007/s11886-022-01706-4>
- Diament et al. (2023), a multimodal dataset of 21,412 recorded nights,
  *arXiv*, <https://doi.org/10.48550/arxiv.2311.08979>. Local copy in **research-os**:
  `assets/papers/hpp/diament_2023_a_multimodal_dataset_of_21412_recorded_n/`.

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29. HPP and OpenEvidence review supports V1 sleep and
fundus morphology beyond age/sex/BMI. The full same-visit BP and vascular family
must remain excluded. See
`04-cardiovascular-lipid.md`.

## v0 Final-Test Status

The classical release is complete: Ridge/logistic and GBDT are remotely verified on every approved exact cohort and rendered in the Figure 1 task deep dives. TabSwift is deferred until GPU execution is configured; it is not a missing or failed row.

## Open Questions

- Should medication-adjusted SBP or untreated-subgroup SBP be a separate task?
- Should standing/lying BP variants be exposed separately or remain out of
  scope for the first card?
- What empirical HPP floor should be considered meaningful for Q2 demos?
