# Non-HDL Cholesterol Task Card

Status: draft

Task id: `non_hdl`

Evidence status: grounded

Evidence reviewed: 2026-07-15

Benchmark status: complete

## Target

Non-HDL Cholesterol as a continuous participant-visit scalar.

Implementation facts:

- bodily system: cardiovascular/lipid
- target route: `blood_tests.bt__non_hdl_cholesterol`
- unit: mg/dL
- acquisition/source: pinned Weizmann blood-test source; nearest completed visit within 180 days
- default stages: `00_00_visit` and `02_00_visit`
- collapse: participant-stage mean
- range/QC: 20-1000 mg/dL
- paper fidelity: exact HealthFormer endpoint

## Why This Matters

Non-HDL cholesterol captures cholesterol carried by atherogenic particles. Prediction does not diagnose dyslipidemia or prove treatment benefit.

## Related HPP Measurements

Total cholesterol, HDL-C, LDL-C, triglycerides, ApoB, lipid medication, and NMR lipoproteins.

## Clinically Meaningful Variants

Continuous prediction is primary. Any clinical category requires
measurement-compatible thresholds, population validation, and a separate Task;
this card does not authorize diagnostic bins.

## Baselines And Ceilings

For V1→V2 evaluation, compare an age, sex, and BMI floor, prior-value LOCF, OLS on prior
value plus allowed demographics, and GBDT on the same inputs. Use one cohort and
split for all comparisons.

## Caveats

- Mask total cholesterol, HDL, non-HDL and their clinical/NMR aliases because non-HDL is algebraically total cholesterol minus HDL.
- Fasting status matters less than for triglycerides, but assay/source, medication, and acute illness still affect values.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns,
target quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Khan et al. (2024), non-HDL cholesterol and cardiovascular risk, <https://doi.org/10.1161/CIRCULATIONAHA.123.067626>.
- HPP Research OS `blood_tests` dataset documentation and field/QC inventory.
- PhenoBench issue-15 blood-source audit applies to every `blood_tests` Task in this card set.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=862; train=613, validation=145, test=104

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.008 | 35.961 | 0.112 |
| Linear | `linear` | 0.446 | 26.888 | 0.683 |
| Trees | `gbdt_delta_r2` | 0.392 | 28.155 | 0.631 |
| LOCF | `last_observation_carried_forward` | 0.441 | 27.003 | 0.690 |

<!-- healthformer-wave-evidence:end -->

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29. V1 DXA and CGM are proposed beyond age/sex/BMI.
All lipid inputs remain excluded, especially total cholesterol and HDL because
their subtraction algebraically reconstructs non-HDL. See
`04-cardiovascular-lipid.md`.

## v0 Final-Test Status

The classical release is complete: Ridge/logistic and GBDT are remotely verified on every approved exact cohort and rendered in the Figure 1 task deep dives. TabSwift is deferred until GPU execution is configured; it is not a missing or failed row.

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
