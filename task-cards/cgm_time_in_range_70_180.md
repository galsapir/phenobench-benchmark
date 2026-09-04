# CGM Time in Range 70-180 Task Card

Task id: `cgm_time_in_range_70_180`

Evidence status: grounded

Evidence reviewed: 2026-07-29

Benchmark status: complete (V1 demographic floor; cross-modal value-add not run — #28)

## Target

CGM Time in Range 70-180 as a continuous HPP scalar.

Implementation facts:

- bodily system: metabolic/metabolomics
- target route: `cgm.iglu_in_range_70_180`
- unit: %
- acquisition: Abbott Libre Pro/Pro IQ CGM, nominally 14 days
- construction/QC: percent of upstream QC-passing readings between 70 and 180 mg/dL, then participant-stage mean
- valid range: 0-100%
- paper fidelity: paper-inspired scalarization of HealthFormer's raw CGM modality

## Why This Matters

TIR 70-180 is a familiar CGM summary. In HPP it has a strong ceiling near 100%, which compresses its variance. This is a V1 cross-sectional demographic-floor benchmark (cross-modal value-add tracked in #28), not forecasting; the near-zero demographic R2 is consistent with the ceiling. Ceiling/variance diagnostics are tracked in #35.

## Benchmark-Track Evidence

literature review, CGMap, and HPP insulin-resistance work support DXA body
composition and a non-glycaemic Nightingale panel as compact independent
cross-modal tracks. Evidence is mainly cross-sectional association; the
benchmark tests held-out prediction. Every same-visit CGM field remains masked.

## Related HPP Measurements

Complementary above/below-range fractions, mean/CV, GMI, HbA1c, meals, activity, and medication.

## Clinically Meaningful Variants

The continuous measurement is primary. Device-, protocol-, and population-
specific clinical thresholds are secondary diagnostics only and do not define
a diagnosis in this Task.

## Baselines And Ceilings

V1-only evaluation compares age/sex/BMI linear and tree floors on one cohort/split. LOCF and prior-target models are prohibited because paired coverage is inadequate.

## Caveats

- The planned cross-modal shape (#28) must mask the full same-visit CGM family and raw stream, especially complementary range bins and composite scores; this wave runs only the demographic floor.
- Only 222 paired summaries exist, so this Task is V1 same-visit only. Ceiling prevalence is not yet reported (tracked in #35); do not transfer diabetes treatment targets to this generally healthy cohort.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, and split Ns.
Target-distribution (quantiles), constant/median-baseline, and ceiling-prevalence
diagnostics are not yet computed for this wave; they are tracked in
#35.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Shilo et al. (2023), HPP CGM atlas, <https://doi.org/10.1016/j.cmet.2023.04.002>.
- Battelino et al. (2019), CGM time-in-range consensus, <https://doi.org/10.2337/dci19-0028>.
- Bent et al. (2021), iGLU CGM feature construction, <https://doi.org/10.1371/journal.pone.0248560>.
- HPP documentation `cgm` dataset documentation and QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: HPP V1 cross-sectional; V2 repeat support was insufficient
- common cohort: n=11483; train=7906, validation=1832, test=1745

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.011 | 9.004 | 0.105 |
| Trees | `demographic_tree` | 0.005 | 9.030 | 0.090 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
