# NMR Total Branched-Chain Amino Acids Task Card

Status: draft

Task id: `total_bcaa_nmr`

Evidence status: grounded

Evidence reviewed: 2026-07-29

Benchmark status: complete

## Target

NMR Total Branched-Chain Amino Acids as a continuous participant-visit scalar.

Implementation facts:

- bodily system: metabolic/metabolomics
- target route: `nightingale.Total_BCAA`
- unit: mmol/L
- acquisition/source: HPP Nightingale serum 1H-NMR (Bruker 500 MHz)
- default stages: `00_00_visit` and `02_00_visit`
- collapse: participant-stage mean
- range/QC: 0.05-2 mmol/L
- paper fidelity: paper-inspired HPP NMR breadth analogue

## Why This Matters

Total BCAA summarizes circulating isoleucine, leucine, and valine and is associated with metabolic state. Prediction does not establish insulin resistance or causality.

## Benchmark-Track Evidence

OpenEvidence review and Paperclip results support DXA body composition as the
stronger independent panel because adiposity and fat distribution are
consistently associated with circulating BCAAs. CGM provides a complementary
glucose-regulation panel, but circulating BCAA can remain stable despite
improved insulin sensitivity; predictive value is therefore an open benchmark
question, not an expected result.

## Related HPP Measurements

Isoleucine, leucine, valine, aromatic amino acids, glucose, HbA1c, BMI, and diet.

## Clinically Meaningful Variants

Continuous prediction is primary. Any clinical category requires
measurement-compatible thresholds, population validation, and a separate Task;
this card does not authorize diagnostic bins.

## Baselines And Ceilings

For V1→V2 evaluation, compare an age, sex, and BMI floor, prior-value LOCF, OLS on prior
value plus allowed demographics, and GBDT on the same inputs. Use one cohort and
split for all comparisons.

## Caveats

- Mask the full same-visit Nightingale panel, explicitly including Ile, Leu, and Val because Total_BCAA is their sum.
- Diet, fasting, exercise, liver function, and renal function affect circulating amino acids.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns,
target quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Julkunen et al. (2023), NMR metabolic biomarker reference atlas, <https://doi.org/10.1038/s41467-023-36231-7>.
- Wang et al. (2011), amino-acid signatures and incident diabetes, <https://doi.org/10.1038/nm.2307>.
- Ho et al. (2016), BMI-associated metabolomic profiles,
  <https://doi.org/10.1371/journal.pone.0148361>.
- Lee et al. (2021), BCAA metabolism, insulin sensitivity, and liver fat,
  <https://doi.org/10.1007/s00125-020-05296-0>.
- HPP Research OS `nightingale` dataset documentation and field/QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=3407; train=2354, validation=542, test=511

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.139 | 0.107 | 0.382 |
| Linear | `linear` | 0.140 | 0.107 | 0.383 |
| Trees | `gbdt_delta_r2` | 0.116 | 0.108 | 0.363 |
| LOCF | `last_observation_carried_forward` | -0.613 | 0.146 | 0.245 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
