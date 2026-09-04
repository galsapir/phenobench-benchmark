# NMR Glycine Task Card

Task id: `glycine_nmr`

Evidence status: grounded

Evidence reviewed: 2026-07-29

Benchmark status: complete

## Target

NMR Glycine as a continuous participant-visit scalar.

Implementation facts:

- bodily system: metabolic/metabolomics
- target route: `nightingale.Gly`
- unit: mmol/L
- acquisition/source: HPP Nightingale serum 1H-NMR (Bruker 500 MHz)
- default stages: `00_00_visit` and `02_00_visit`
- collapse: participant-stage mean
- range/QC: 0.03-2 mmol/L
- paper fidelity: paper-inspired HPP NMR breadth analogue

## Why This Matters

Glycine is a circulating amino acid with metabolic associations and useful repeat coverage in HPP. Prediction does not imply a causal protective effect.

## Benchmark-Track Evidence

literature review and literature results support DXA body composition as the
stronger independent panel: circulating glycine is inversely associated with
abdominal adiposity and insulin-resistant states. CGM is a complementary
functional-metabolism panel, but direct CGM-to-glycine prediction evidence is
limited; the benchmark tests that hypothesis rather than assuming it.

## Related HPP Measurements

BCAA, aromatic amino acids, glucose, HbA1c, renal/liver measurements, diet, and body composition.

## Clinically Meaningful Variants

Continuous prediction is primary. Any clinical category requires
measurement-compatible thresholds, population validation, and a separate Task;
this card does not authorize diagnostic bins.

## Baselines And Ceilings

For V1→V2 evaluation, compare an age, sex, and BMI floor, prior-value LOCF, OLS on prior
value plus allowed demographics, and GBDT on the same inputs. Use one cohort and
split for all comparisons.

## Caveats

- Mask the full same-visit Nightingale panel and any direct glycine alias.
- Fasting, diet, renal clearance, hepatic metabolism, and sample processing affect concentration.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns,
target quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Julkunen et al. (2023), NMR metabolic biomarker reference atlas, <https://doi.org/10.1038/s41467-023-36231-7>.
- Floegel et al. (2013), serum metabolites and type 2 diabetes risk, <https://doi.org/10.2337/db12-0495>.
- Lustgarten et al. (2013), glycine, regional body fat, and insulin resistance,
  <https://doi.org/10.1371/journal.pone.0084034>.
- Adeva-Andany et al. (2018), insulin resistance and glycine metabolism,
  <https://doi.org/10.1007/s00726-017-2508-0>.
- HPP documentation `nightingale` dataset documentation and field/QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=3407; train=2354, validation=542, test=511

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.106 | 0.081 | 0.327 |
| Linear | `linear` | 0.549 | 0.057 | 0.742 |
| Trees | `gbdt_delta_r2` | 0.516 | 0.059 | 0.720 |
| LOCF | `last_observation_carried_forward` | 0.401 | 0.066 | 0.737 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
