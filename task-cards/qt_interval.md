# QT Interval Task Card

Status: draft

Task id: `qt_interval`

Evidence status: grounded

Evidence reviewed: 2026-07-14

## Target

Raw `ecg.qt_ms`, not QTc. HealthFormer names
“QT Interval” but omits its field and correction status; this is an analogue,
not paper parity.

Implementation facts:

- target field: `qt_ms`
- target dataset: `ecg`
- target source: None (loaded through HPP `hpp_data_loader`)
- target construction: mean of same-stage records per participant; then range guard
- evaluation-unit grain: participant
- default research stage: `00_00_visit`; V1-to-V2 Y: `02_00_visit`
- valid range: 200-700 ms (broad PhenoBench plausibility guard, not a
  clinical interval or source mask)
- primary metric: R2

## Why This Matters

QT spans ventricular depolarization and repolarization but varies with heart
rate. This Task tests longitudinal forecastability, not QTc, long-QT syndrome,
arrhythmia risk, medication effects, or interventions.

## Related HPP Measurements

Heart rate/RR, QTc, QRS, rhythm, and quality provide context; medications,
electrolytes, sleep, and ECG embeddings are companion data. An HPP study
linked sleep heart-rate features to a QTc/QT endpoint, not causally to raw QT.

## Clinically Meaningful Variants

Raw QT has no defensible fixed bins. A formula-named QTc Task should use
same-recording QT and RR before aggregation, pre-specify rhythm/QRS eligibility,
and compare Fridericia/Framingham with Bazett analyzer QTc. Never
apply QTc thresholds here.

## Baselines And Ceilings

`NoFeaturesPredictor` contributes no modality features; `DemographicFloorStrategy`
fits age, sex, and BMI. Last observation carried forward (LOCF) copies prior QT.
Ordinary least squares (OLS) and trees fit prior QT plus those covariates.
HealthFormer reports LOCF and token-ID linear models; PB OLS uses continuous
measurements, so it is family-aligned, not numerically equivalent. Trees are
PB-only. New representations must beat the best same-cohort row.

## Caveats

Heart-rate change, T-wave detection, rhythm/QRS, quality, medications,
electrolytes, and software era may confound. Reviewed Y spans 326-610 ms and
prior QT 300-618 ms. The guard is non-clinical; one ECG is not a diagnosis.

## Metrics

R2 is primary. Breadth rows include MAE/RMSE, correlations, coverage, LOCF
delta, residuals, and age/sex/BMI views. Deep runs should add calibration and
residual strata for heart rate/RR, QRS, rhythm/quality, and software era.

## References

- Lutsker et al. (2026), <https://arxiv.org/abs/2604.27899>.
- Diament et al. (2023), HPP sleep study,
  <https://doi.org/10.48550/arXiv.2311.08979>.
- Postema and Wilde (2014), QT interpretation,
  <https://doi.org/10.2174/1573403X10666140514103612>.
- Vandenberk et al. (2016), QT correction,
  <https://doi.org/10.1161/JAHA.116.003264>.
- HPP [`ecg` dataset documentation](https://github.com/PhenoAI/research-os/tree/main/assets/datasets/ecg).

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29. V1 Nightingale and sleep are proposed beyond
age/sex/BMI. ECG heart rate/RR, QTc, all other ECG fields, and the waveform
remain excluded. See
`04-cardiovascular-lipid.md`.

## v0 Final-Test Status

The classical release is complete: Ridge/logistic and GBDT are remotely verified on every approved exact cohort and rendered in the Figure 1 task deep dives. TabSwift is deferred until GPU execution is configured; it is not a missing or failed row.

## Open Questions

- Should a formula-pinned QTc Task enter the deep section?
- Which rhythm, QRS, quality, and software-era sensitivity cohorts are required?
