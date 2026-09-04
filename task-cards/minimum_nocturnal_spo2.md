# Minimum Nocturnal SpO2 Task Card

Task id: `minimum_nocturnal_spo2`

Evidence status: grounded

Evidence reviewed: 2026-07-29

Benchmark status: complete

## Target

Minimum Nocturnal SpO2 as a continuous HPP scalar.

Implementation facts:

- bodily system: respiratory/hypoxaemia
- target route: `sleep.saturation_min_value`
- unit: %
- acquisition: WatchPAT-300 home monitoring, approximately three nights
- construction/QC: per-night nadir followed by participant-stage mean; Standard QC plus SpO2 quality score >=25
- valid range: 50-100%
- paper fidelity: paper-inspired HPP SpO2 analogue

## Why This Matters

Minimum nocturnal SpO2 captures the depth of the worst observed desaturation. It is a noisy nadir, not a diagnosis or a complete measure of hypoxic burden.

## Related HPP Measurements

Mean SpO2, time below saturation thresholds, ODI, AHI/RDI, hypoxic burden, TST, and pulmonary/cardiovascular measurements.

## Clinically Meaningful Variants

The continuous measurement is primary. Device-, protocol-, and population-
specific clinical thresholds are secondary diagnostics only and do not define
a diagnosis in this Task.

## Baselines And Ceilings

For V1→V2 evaluation, compare age/sex/BMI demographic floor, prior-value LOCF, OLS on prior value plus demographics, and GBDT on the same inputs on one cohort/split.

## Caveats

- Mask the full same-visit sleep family, especially every SpO2/desaturation/ODI/hypoxic-burden summary and raw oximetry.
- A single artifact can determine a nightly nadir; averaging nightly minima improves stability but changes interpretation from a raw minimum.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Benchmark-Track Evidence

literature review and HPP/literature evidence support the fixed DXA panel as
the minimal modality for V1→V1 and V1→V2 tracks. Regional fat and lean
distribution associate with nocturnal oxygenation beyond BMI, while CGM
evidence is weak outside diabetes. Exclude the complete sleep/oximetry family.
The V1→V2 Allowed Information Set contains no V1 SpO₂ or sleep summary.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns, target
quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Kohn et al. (2025), HPP multi-night sleep phenotyping, <https://doi.org/10.1038/s41591-024-03481-x>.
- Yalamanchali et al. (2013), WatchPAT validation meta-analysis, <https://doi.org/10.1001/jamaoto.2013.5338>.
- HPP documentation `sleep` dataset documentation and QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=4189; train=2868, validation=671, test=650

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.104 | 3.909 | 0.326 |
| Linear | `linear` | 0.257 | 3.559 | 0.508 |
| Trees | `gbdt_delta_r2` | 0.245 | 3.587 | 0.497 |
| LOCF | `last_observation_carried_forward` | -0.108 | 4.347 | 0.476 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
