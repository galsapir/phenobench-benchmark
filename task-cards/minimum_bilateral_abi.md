# Minimum Bilateral ABI Task Card

Task id: `minimum_bilateral_abi`

Evidence status: grounded

Evidence reviewed: 2026-07-14

## Target

ABI is ankle systolic pressure divided by the higher brachial pressure per leg.
PhenoBench requires both sides, takes `min(l_abi, r_abi)`, then averages
participant records. Device failures are excluded; warnings remain. This is a
worst-side family endpoint, not a one-to-one HealthFormer parameter.

Implementation facts:

- target fields: `l_abi`, `r_abi`
- target dataset: `vascular_health`
- target source: None (loaded through HPP `hpp_data_loader`)
- default research stage: `00_00_visit`
- valid range: 0-3 (dimensionless)
- primary metric: R2

## Why This Matters

PAD is often asymmetric, so the lower side captures unilateral impairment that
an average or higher side can hide. The Task forecasts a vascular phenotype;
it is not screening guidance, a PAD diagnosis, event-risk estimation, or causal
inference.

## Related HPP Measurements

HPP work analyzed ABI with PWV, blood pressure, and carotid IMT. Candidate
companions include ECG/fundus, lipids, HbA1c, renal function, smoking, and
activity; these remain proposed inputs unless cited.

## Clinically Meaningful Variants

A clinical variant must preserve per-leg categories: abnormal at or below 0.90,
borderline 0.91-0.99, normal 1.00-1.40, and noncompressible above 1.40. A
participant output should retain both legs or be multilabel; binning the current
minimum can hide contralateral high ABI, so this requires a separate Task.

## Baselines And Ceilings

`NoFeaturesPredictor` contributes no modality features; `DemographicFloorStrategy`
fits age, sex, and BMI. Last observation carried forward (LOCF) copies prior Y.
Ordinary least squares (OLS) and gradient-boosted trees (GBDT) fit prior Y plus
demographics. HealthFormer reported
LOCF and per-modality linear baselines, not trees or the demographic floor.
Compare representations on one cohort.

## Caveats

- Requiring both sides reduces cohort size; the scalar discards laterality,
  bilateral burden, and contralateral high ABI.
- ABI warnings are retained because most represent missing timestamps rather
  than failed measurements.

## Metrics

R2 is primary. Also report RMSE, MAE, Pearson r, Spearman rho, same-cohort
deltas against LOCF, and residuals across low/normal/high ABI bands.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- HPP `vascular_health` dataset documentation for bilateral ABI and Piera QC.
- 2024 ACC/AHA lower-extremity PAD guideline,
  <https://doi.org/10.1161/CIR.0000000000001251>.
- Aboyans et al. (2012), AHA ABI measurement statement,
  <https://doi.org/10.1161/CIR.0b013e318276fbcb>.
- Reicher et al. (2024), HPP phenome-wide aging map,
  <https://doi.org/10.1038/s43587-024-00734-9>.

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29. V1 Nightingale and fundus morphology are proposed
beyond age/sex/BMI. The complete same-visit BP, ABI/PWV/pressure, carotid, and
vascular-waveform families remain excluded. See
`04-cardiovascular-lipid.md`.

## v0 Final-Test Status

The classical release is complete: Ridge/logistic and GBDT are remotely verified on every approved exact cohort and rendered in the Figure 1 task deep dives.

## Open Questions

- Should the categorical Task emit per-leg or participant-level multilabel Y?
