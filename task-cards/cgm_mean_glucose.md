# CGM Mean Glucose Task Card

Status: draft

Task id: `cgm_mean_glucose`

Evidence status: grounded

Evidence reviewed: 2026-07-29

Benchmark status: complete (V1 demographic floor; cross-modal value-add not run — #28)

## Target

CGM Mean Glucose as a continuous HPP scalar.

Implementation facts:

- bodily system: metabolic/metabolomics
- target route: `cgm.iglu_mean`
- unit: mg/dL
- acquisition: Abbott Libre Pro/Pro IQ CGM, nominally 14 days
- construction/QC: upstream iGLU summary over QC-passing connection, then participant-stage mean
- valid range: 40-500 mg/dL
- paper fidelity: paper-inspired scalarization of HealthFormer's raw CGM modality

## Why This Matters

Mean interstitial glucose summarizes ambient glycaemic exposure during the
monitoring period, including values and excursions missed by a single fasting
sample. This is a V1 cross-sectional demographic-floor benchmark (age/sex/BMI): it
is not glucose forecasting, not yet a cross-modal test (that value-add is tracked
in [#28](https://github.com/PhenoAI/phenobench/issues/28)), and does not replace
fasting glucose or HbA1c.

## Benchmark-Track Evidence

OpenEvidence review, CGMap, and HPP insulin-resistance work support DXA body
composition and a non-glycaemic Nightingale panel as compact independent
cross-modal tracks. Evidence is mainly cross-sectional association; the
benchmark tests held-out prediction. Every same-visit CGM field remains masked.

## Related HPP Measurements

CGM SD/CV/TIR and GMI/eA1c are same-modality relatives. HbA1c, fasting glucose,
meals, activity, sleep, anthropometrics, medications, and retinal measures are
candidate cross-modal correlates.

## Clinically Meaningful Variants

The continuous measurement is primary. In adults without diabetes, mean sensor glucose
sits near 98-104 mg/dL over 10-14 days of wear (rising modestly beyond age 60); such
normative values are sensor-specific (reported largely for Dexcom G6) and do not transfer
directly to this Abbott Libre Pro target. Mean glucose maps to an estimated HbA1c via the
glucose management indicator (GMI) but is not interchangeable with laboratory HbA1c or
fasting glucose (Selvin 2024); neither a value nor a prediction defines diabetes in this Task.

## Baselines And Ceilings

V1-only evaluation compares age/sex/BMI linear and tree floors on one cohort/split. LOCF and prior-target baselines are not run for this wave because paired V1/V2 coverage is inadequate.

## Caveats

- The planned cross-modal shape ([#28](https://github.com/PhenoAI/phenobench/issues/28)) must mask the full same-visit CGM family and raw stream, especially AUC, GMI/eA1c, and every mean-derived feature; this wave runs only the demographic floor, so no CGM features enter X yet.
- Only 222 HPP participants currently have paired V1/V2 summaries; this Task is V1 same-visit only for this wave.
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
- Shah et al. (2019), CGM profiles in healthy people without diabetes,
  <https://doi.org/10.1210/jc.2018-02763>.
- Battelino et al. (2019), CGM time-in-range consensus, <https://doi.org/10.2337/dci19-0028>.
- Broll et al. (2021), iglu R package for CGM metrics, <https://doi.org/10.1371/journal.pone.0248560>.
- Selvin (2024), glucose management indicator versus laboratory HbA1c, <https://doi.org/10.2337/dci23-0086>.
- HPP Research OS `cgm` dataset documentation and QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: HPP V1 cross-sectional; V2 repeat support was insufficient
- common cohort: n=11483; train=7906, validation=1832, test=1745

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.058 | 11.338 | 0.242 |
| Trees | `demographic_tree` | 0.040 | 11.444 | 0.214 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
- Cross-modal V1 value-add is tracked in
  [#28](https://github.com/PhenoAI/phenobench/issues/28).
- CGM/laboratory discordance and progression surfaces are tracked in
  [#29](https://github.com/PhenoAI/phenobench/issues/29).
