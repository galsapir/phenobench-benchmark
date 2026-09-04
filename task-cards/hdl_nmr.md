# NMR HDL Cholesterol Task Card

Task id: `hdl_nmr`

Evidence status: grounded

Evidence reviewed: 2026-07-15

Benchmark status: complete

## Target

NMR HDL Cholesterol as a continuous participant-visit scalar.

Implementation facts:

- bodily system: cardiovascular/lipid
- target route: `nightingale.HDL_C`
- unit: mmol/L
- acquisition/source: HPP Nightingale serum 1H-NMR (Bruker 500 MHz)
- default stages: `00_00_visit` and `02_00_visit`
- collapse: participant-stage mean
- range/QC: 0.1-5 mmol/L
- paper fidelity: assay-substituted analogue of the HealthFormer clinical HDL endpoint

## Why This Matters

HDL-C is a standardized lipid measurement, but its causal interpretation is limited. This Task predicts the Nightingale assay value, not clinical cardiovascular protection.

## Related HPP Measurements

Total cholesterol, LDL-C, triglycerides, ApoA1, and clinical HDL/non-HDL assays.

## Clinically Meaningful Variants

Continuous prediction is primary. Any clinical category requires
measurement-compatible thresholds, population validation, and a separate Task;
this card does not authorize diagnostic bins.

## Baselines And Ceilings

For V1→V2 evaluation, compare an age, sex, and BMI floor, prior-value LOCF, OLS on prior
value plus allowed demographics, and GBDT on the same inputs. Use one cohort and
split for all comparisons.

## Caveats

- Mask the full same-visit Nightingale panel and clinical HDL/total-cholesterol algebraic equivalents.
- NMR HDL-C is not interchangeable with every enzymatic clinical assay; fasting and sample handling can shift the lipid panel.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns,
target quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Julkunen et al. (2023), NMR metabolic biomarker reference atlas, <https://doi.org/10.1038/s41467-023-36231-7>.
- Voight et al. (2012), HDL-C Mendelian-randomization interpretation, <https://doi.org/10.1016/S0140-6736(12)60312-2>.
- HPP documentation `nightingale` dataset documentation and field/QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=3404; train=2351, validation=542, test=511

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.146 | 0.398 | 0.385 |
| Linear | `linear` | 0.372 | 0.341 | 0.611 |
| Trees | `gbdt_delta_r2` | 0.351 | 0.347 | 0.595 |
| LOCF | `last_observation_carried_forward` | 0.020 | 0.426 | 0.607 |

<!-- healthformer-wave-evidence:end -->

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29. V1 DXA and CGM are proposed beyond age/sex/BMI.
All Nightingale, clinical-lipid, lipidomics, and derived-lipid inputs remain
excluded to prevent same-assay reconstruction. See
`04-cardiovascular-lipid.md`.

## v0 Final-Test Status

The classical release is complete: Ridge/logistic and GBDT are remotely verified on every approved exact cohort and rendered in the Figure 1 task deep dives.

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
