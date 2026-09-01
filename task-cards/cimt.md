# CIMT Task Card

Status: draft

Task id: `cimt`

Evidence status: grounded

Evidence reviewed: 2026-08-15

## Target

Mean carotid intima-media thickness from HPP carotid ultrasound.
Continuous-scalar regression. The default research stage is `00_00_visit`, but
the Task can be configured for another available stage.

Implementation facts:

- target field: `imt_mean`
- target dataset: `carotid_ultrasound`
- target source: None
- target unit: mm
- default research stage: `00_00_visit`
- valid range: 0.3-3.0 mm; a PhenoBench plausibility filter, not a clinical
  interval
- primary metric: R2

## Why This Matters

CIMT is a subclinical vascular-structure marker associated with atherosclerosis
and cardiovascular risk. It is clinically interpretable but not a current
headline screening target, so PhenoBench should treat it as a secondary
vascular-aging target.

**What a row here does not support.** A predicted CIMT is a same-visit
association with an operator-acquired ultrasound measurement. It is not a
diagnosis of atherosclerosis, not a plaque assessment, and not a cardiovascular
risk estimate. Guidelines have moved away from CIMT as a risk-stratification
tool precisely because adding it to established risk scores did not improve
prediction usefully, so a strong row here is a statement about the measurement,
not about risk.

## Related HPP Measurements

Demonstrated in HPP and persisted in this repository, from
`docs/figure1/cimt_review.json`, test split:

- V1 fundus + demographics reaches test R2 = 0.299 (95% CI [0.256, 0.342]) on a
  cohort of 7,403.
- V1 Nightingale + demographics reaches R2 = 0.270 (95% CI [0.224, 0.310]) on
  6,983.

**The paired comparison is committed and it confirms this directly**: fundus
reaches **ΔR2 = +0.015 (95% CI [-0.002, +0.030])** and Nightingale
**+0.006 ([-0.012, +0.023])** - both span zero. So neither track demonstrates
vascular-morphology signal beyond age, sex and BMI on this cohort. **That is the
finding to carry**: CIMT is strongly age-dependent, a raw R2 near 0.3 is mostly
age being recovered, and the measured margins are indistinguishable from zero.

Retinal microvasculature leading again matches the ordering on `sbp` and
`hypertension_status`, where fundus also leads - three targets on one axis with
the same modality ranking.

**These are `reviewable` rows, not `final` ones.** Measured across the committed
leaderboards: all 787 rows carry `curation_state: reviewable` and none is
`final`. A complete fresh v0 re-run is committed to, so every figure in this
section is pre-re-run evidence that the re-run supersedes - persisted and citable
today, not a frozen result. **Which curation states the Figure 1 export accepts
is the export track's live question, not this card's**; read the two counts
above, not a gate.

## Clinically Meaningful Variants

**No categorical CIMT variant is defensible, and unlike the lipid targets the
problem is that the measurement itself is not standardised across devices.**
CIMT values depend on the scanner, the insonation angle, which carotid segments
are measured, whether plaque is included, and the reading convention (mean of
means, maximum, near or far wall). Published "high CIMT" cutoffs and
percentile-based abnormality rules are therefore protocol-specific, and the
common clinical use is a **percentile for age and sex within the measuring
laboratory's own reference**, not a fixed millimetre threshold.

Two consequences:

- **A fixed millimetre bin would encode this laboratory's protocol as though it
  were a clinical standard.** The card's `imt_mean` is one convention among
  several, and nothing here establishes agreement with the references those
  cutoffs come from.
- **An age-sex percentile variant would be circular on this Task.** Since most
  of the predictable variance is age, a percentile-for-age label removes the
  signal the demographic floor already captures and leaves a much harder,
  smaller-variance target - which may be the more interesting Task, but it is a
  different one with its own floor.

The continuous target stays primary. Carotid plaque presence, which the card
lists as a comparator, is the categorical vascular variant with a defensible
definition, and it is a separate measurement rather than a bin on this one.

## Baselines And Ceilings

The required floor is a no-modality-feature baseline: `NoFeaturesPredictor`
contributes no modality features, and `DemographicFloorStrategy` fits age, sex,
and BMI. The task code records a moderate demographic floor around R2 0.28
because CIMT is strongly age-dependent.

Natural comparators include carotid plaque, SBP, lipid markers, retinal vessel
features, ECG/vascular embeddings, and clinical risk-factor models. Claims
should focus on vascular morphology signal beyond age.

## Caveats

- Age can dominate raw performance.
- CIMT adds modest incremental risk information beyond standard clinical risk
  factors in some settings.
- Ultrasound measurement protocol and segmentation quality can add noise.
- Strong CIMT prediction should not be claimed as incident CVD prediction
  unless evaluated against event outcomes.

## Metrics

Primary metric is R2. Secondary MAE in mm and Spearman are useful. Audit views
should include demographic-floor delta R2 and age-stratified residuals.

## References

- Source material: `docs/task_cards/source_material/foundation-model-surrogate-targets-v1.md`
- Tschiderer et al., 2020, CIMT and incident carotid plaque meta-analysis:
  <https://doi.org/10.1111/eci.13217>
- Mitra et al., 2025, CIMT and CVD risk factors in UK Biobank:
  <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12162042/>
- Talmor-Barkan et al. (2026), RetiMap automated retinal vascular measurement.
  **Manuscript in preparation, no DOI** - treat as HPP context rather than a
  citable source. Local copy in **research-os**:
  `assets/papers/hpp/talmor_barkan_2026_retimap_automated_retinal_vascular_measu/`.

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29. NMR metabolomics and retinal morphology are the
proposed V1 systemic tracks; same-visit carotid, BP, and vascular features are
excluded. CIMT remains V1-only until a like-for-like V2 target is audited. See
`04-cardiovascular-lipid.md`.

## v0 Final-Test Status

The classical release is complete: Ridge/logistic and GBDT are remotely verified on every approved exact cohort and rendered in the Figure 1 task deep dives. TabSwift is deferred until GPU execution is configured; it is not a missing or failed row.

## Open Questions

- Should carotid plaque or vascular age become a stronger vascular endpoint
  than CIMT?
- What ultrasound QC fields should be surfaced in run review packets?
- Should CIMT rows be excluded from headline demos unless age-residualized
  performance is reported?
