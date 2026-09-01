# Oxygen Desaturation Index Task Card

Status: draft

Task id: `odi`

Evidence status: grounded

Evidence reviewed: 2026-07-29

Benchmark status: complete

## Target

Oxygen Desaturation Index as a continuous HPP scalar.

Implementation facts:

- bodily system: respiratory/hypoxaemia
- target route: `sleep.odi`
- unit: events/hour
- acquisition: WatchPAT-300 home monitoring, approximately three nights
- construction/QC: mean valid nights; 4% desaturation definition; Standard QC plus PAT and SpO2 quality scores >=25
- valid range: 0-200 events/hour
- paper fidelity: exact HealthFormer input measurement; new endpoint row

## Why This Matters

ODI measures the frequency of nocturnal oxygen desaturations and complements AHI with a hypoxaemia-focused signal. Prediction does not diagnose OSA.

## Related HPP Measurements

AHI/RDI, REM/NREM ODI, minimum/mean SpO2, desaturation counts, hypoxic burden, TST, and BMI.

## Clinically Meaningful Variants

The continuous measurement is primary. Device-, protocol-, and population-
specific clinical thresholds are secondary diagnostics only and do not define
a diagnosis in this Task.

## Baselines And Ceilings

For V1→V2 evaluation, compare age/sex/BMI demographic floor, prior-value LOCF, OLS on prior value plus demographics, and GBDT on the same inputs on one cohort/split.

## Caveats

- Mask the full same-visit sleep family, especially ODI variants, desaturation counts, SpO2 summaries, hypoxic burden, AHI, and RDI.
- The 4% rule, oximeter quality, event scoring, and averaging across nights affect ODI; thresholds from other rules are not transferable.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Benchmark-Track Evidence

OpenEvidence review and HPP/Paperclip evidence support the fixed DXA panel as
the minimal modality for V1→V1 and V1→V2 tracks. Regional adiposity associates
with desaturation burden beyond BMI, while CGM evidence is weak outside
diabetes. Exclude the complete sleep/oximetry family. The V1→V2 Allowed
Information Set contains no V1 ODI or sleep summary.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns, target
quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Kohn et al. (2025), HPP multi-night sleep phenotyping, <https://doi.org/10.1038/s41591-024-03481-x>.
- Yalamanchali et al. (2013), WatchPAT validation meta-analysis, <https://doi.org/10.1001/jamaoto.2013.5338>.
- HPP Research OS `sleep` dataset documentation and QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=4189; train=2868, validation=671, test=650

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.176 | 5.388 | 0.427 |
| Linear | `linear` | 0.604 | 3.733 | 0.778 |
| Trees | `gbdt_delta_r2` | 0.574 | 3.875 | 0.758 |
| LOCF | `last_observation_carried_forward` | 0.572 | 3.883 | 0.774 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
