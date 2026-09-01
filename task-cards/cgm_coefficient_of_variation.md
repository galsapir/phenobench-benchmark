# CGM Coefficient of Variation Task Card

Status: draft

Task id: `cgm_coefficient_of_variation`

Evidence status: grounded

Evidence reviewed: 2026-07-29

Benchmark status: complete (V1 demographic floor; cross-modal value-add not run — #28)

## Target

CGM Coefficient of Variation as a continuous HPP scalar.

Implementation facts:

- bodily system: metabolic/metabolomics
- target route: `cgm.iglu_cv`
- unit: %
- acquisition: Abbott Libre Pro/Pro IQ CGM, nominally 14 days
- construction/QC: upstream 100 × SD / mean over QC-passing connection, then participant-stage mean
- valid range: 0-100%
- paper fidelity: paper-inspired scalarization of HealthFormer's raw CGM modality

## Why This Matters

CGM CV is a scale-normalized glycaemic-variability measure. This is a V1 cross-sectional demographic-floor benchmark (cross-modal value-add tracked in [#28](https://github.com/PhenoAI/phenobench/issues/28)), not forecasting. Prediction does not establish instability-related clinical risk or diabetes status.

## Benchmark-Track Evidence

OpenEvidence review, CGMap, and HPP insulin-resistance work support DXA body
composition and a non-glycaemic Nightingale panel as compact independent
cross-modal tracks. Evidence is mainly cross-sectional association; the
benchmark tests held-out prediction. Every same-visit CGM field remains masked.

## Related HPP Measurements

CGM mean/SD/MAGE/CONGA, TIR, GMI, HbA1c, meals, activity, and medication.

## Clinically Meaningful Variants

The continuous measurement is primary. The international consensus target of CV <36%
distinguishes stable from unstable glycemia and was set from hypoglycemia risk in
diabetes management (Danne et al. 2017; Battelino et al. 2019); healthy non-diabetic
adults sit well below it (within-person CV about 17%). That threshold is a
glycemic-management target, not a diagnosis, and it is derived largely in diabetes
populations, so it does not define a label in this predominantly non-diabetic HPP Task.

## Baselines And Ceilings

V1-only evaluation compares age/sex/BMI linear and tree floors on one cohort/split. LOCF and prior-target baselines are not run for this wave because paired V1/V2 coverage is inadequate.

## Caveats

- The planned cross-modal shape ([#28](https://github.com/PhenoAI/phenobench/issues/28)) must mask the full same-visit CGM family and raw stream, explicitly including mean and SD components that reconstruct CV; this wave runs only the demographic floor.
- Only 222 paired V1/V2 summaries exist; this Task is V1 same-visit only. CV is unstable when mean or usable wear duration is poor, so retain upstream QC; note CV can also rise even as variability improves if mean glucose falls.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, and split Ns.
Target-distribution (quantiles), constant/median-baseline, and ceiling diagnostics
are not yet computed for this wave; they are tracked in
[#35](https://github.com/PhenoAI/phenobench/issues/35).

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Keshet et al. (2023), CGMap HPP CGM atlas, <https://doi.org/10.1016/j.cmet.2023.04.002>.
- Battelino et al. (2019), CGM time-in-range consensus, <https://doi.org/10.2337/dci19-0028>.
- Broll et al. (2021), iglu R package for CGM metrics, <https://doi.org/10.1371/journal.pone.0248560>.
- Danne et al. (2017), international consensus on CGM (CV <36% target), <https://doi.org/10.2337/dc17-1600>.
- Shah et al. (2019), CGM profiles in healthy people without diabetes (within-person CV ~17%), <https://doi.org/10.1210/jc.2018-02763>.
- Selvin et al. (2023), within-person and between-sensor CGM metric variability, <https://doi.org/10.1093/clinchem/hvac192>.
- HPP Research OS `cgm` dataset documentation and QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: HPP V1 cross-sectional; V2 repeat support was insufficient
- common cohort: n=11483; train=7906, validation=1832, test=1745

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.020 | 4.023 | 0.142 |
| Trees | `demographic_tree` | 0.021 | 4.019 | 0.151 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
