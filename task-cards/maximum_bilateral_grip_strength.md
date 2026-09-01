# Maximum Bilateral Grip Strength Task Card

Status: draft

Task id: `maximum_bilateral_grip_strength`

Evidence status: grounded

Evidence reviewed: 2026-07-29

## Target

Maximum of the first valid left- and right-hand attempts, requiring both sides
and `piera_hand_grip_status == success`. Equal opportunities are compared for
every participant; the maximum need not be the dominant hand. Later-introduced
second attempts are excluded, so this is not a clinical best-of-three measure
or a one-to-one HealthFormer parameter.

Implementation facts:

- target fields: `hand_grip_strength_left`, `hand_grip_strength_right`
- target dataset: `hand_grip`
- target source: None (loaded through HPP `hpp_data_loader`)
- default research stage: `00_00_visit`
- valid range: 1-90 kg
- primary metric: R2

## Why This Matters

Grip strength is a low-cost measure of muscle function and a core
sarcopenia/frailty component. Lower strength is associated with adverse
outcomes, but this Task supports forecasting, not diagnosis, prognosis, or
causality.

## Related HPP Measurements

EWGSOP2 pairs strength with muscle quantity, making DXA appendicular lean mass
a grounded companion. Plasma metabolomics and objective activity provide
independent biological and behavioral views of muscle function.

## Clinically Meaningful Variants

Raw kg remains primary. Age and sex belong in the demographic floor and
stratified residuals; normalizing Y would create a reference-dependent Task. A
future low-strength variant may test EWGSOP2 cutoffs below 27 kg for men and
16 kg for women after calibration on HPP's later two-attempt subset.

## Baselines And Ceilings

`NoFeaturesPredictor` contributes no modality features; `DemographicFloorStrategy`
fits age, sex, and BMI. Last observation carried forward (LOCF) copies prior Y.
Ordinary least squares (OLS) and gradient-boosted trees (GBDT) fit prior Y plus
demographics. HealthFormer reported
LOCF and per-modality linear baselines, not trees or the demographic floor.
Compare representations on one cohort.

## Benchmark-Track Evidence

The frozen v0 tracks use the fixed nine-field V1 Nightingale amino-acid panel
(`Ala`, `Gln`, `Gly`, `His`, `Ile`, `Leu`, `Val`, `Phe`, `Tyr`) plus V1 age,
sex, and BMI for both V1 and V2 grip targets. OpenEvidence and Paperclip
support plasma metabolomics and branched-chain amino acids as independent
muscle-mass and strength signals. Every hand-grip and DXA field is excluded.

Gait Fusion is not v0-benchmark-ready. Raw Newton skeleton files exist on S3,
but no canonical operational source contract, checksum-bound embeddings, or accessible
checkpoint was found. The canonical V1 engineered-gait cohort overlaps 345 V1
and zero V2 eligible grip targets, so gait remains a future blocked candidate.

## Caveats

- Age and sex explain substantial variance and must remain visible.
- First-attempt-only semantics improve visit comparability but can understate
  maximal strength.
- Pain, handedness, effort, and device technique contribute noise.

## Metrics

R2 is primary. Also report RMSE and MAE in kg, Pearson r, Spearman rho,
same-cohort deltas against LOCF, and sex- and age-stratified residuals.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- HPP `hand_grip` dataset documentation for attempt fields and Piera QC.
- Cruz-Jentoft et al. (2019), EWGSOP2 consensus,
  <https://doi.org/10.1093/ageing/afy169>.
- Reijnierse et al. (2017), grip protocol comparison,
  <https://doi.org/10.1002/jcsm.12181>.
- Gabet et al. (2026), HPP gait foundation model,
  <https://doi.org/10.48550/arXiv.2603.25283>.

## Open Questions

- Should a later deep task model side-specific trajectories or asymmetry?
