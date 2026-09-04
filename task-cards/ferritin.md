# Ferritin Task Card

Task id: `ferritin`

Evidence status: grounded

Evidence reviewed: 2026-07-29

Benchmark status: complete

## Target

Ferritin as a continuous participant-visit scalar.

Implementation facts:

- bodily system: hematologic
- target route: `blood_tests.bt__ferritin`
- unit: ng/mL
- acquisition/source: pinned Weizmann blood-test source (assay/device not documented in reachable HPP dataset docs); records selected by exact research stage, then participant-stage mean
- default stages: `00_00_visit` and `02_00_visit`
- collapse: participant-stage mean
- range/QC: 1-5000 ng/mL broad plausibility guard
- paper fidelity: HPP hematopoietic extension

## Why This Matters

Ferritin is used to assess iron stores but is also an acute-phase reactant. Prediction does not by itself establish iron deficiency or overload.

## Related HPP Measurements

Hemoglobin, MCV, iron/transferrin markers, CRP/inflammation, liver tests, sex, and menstrual factors.

## Benchmark-Track Evidence

Population NMR/MS profiling finds sex-specific ferritin associations with
fatty-acid species, branched-chain amino-acid catabolites, heme catabolites, and
lipoprotein particles. This supports a Nightingale track for total ferritin.
Because ferritin is an acute-phase reactant, a fixed panel containing GlycA may
capture inflammation and cannot be interpreted as prediction of iron stores.

## Clinically Meaningful Variants

Continuous prediction is primary. Iron-deficiency thresholds are guideline- and
context-dependent: WHO defines iron deficiency as serum ferritin below 15 ng/mL in adults
without inflammation and below 70 ng/mL in the presence of infection or inflammation, and
the AGA uses below 45 ng/mL when evaluating anemic patients for iron-deficiency anemia.
Ferritin is an acute-phase reactant, so any cutoff is assay- and inflammation-dependent.
Because the HPP Weizmann ferritin assay and device are not documented here, these thresholds
are external context and do not define labels for this Task without assay-compatible
validation; this card does not authorize diagnostic bins.

## Baselines And Ceilings

For V1→V2 evaluation, compare an age, sex, and BMI floor, prior-value LOCF, OLS on prior
value plus allowed demographics, and GBDT on the same inputs. Use one cohort and
split for all comparisons.

## Caveats

- Mask same-window iron studies, ferritin aliases, and deterministic iron-status labels.
- Inflammation, liver disease, infection, supplementation, sex, and menstrual status alter ferritin independently of iron stores.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns,
target quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Reicher et al. (2024), HPP longitudinal aging phenotypes, <https://doi.org/10.1038/s43587-024-00734-9>.
- World Health Organization (2020), WHO guideline on use of ferritin concentrations to assess iron status, <https://www.who.int/publications/i/item/9789240000124>.
- Garcia-Casal et al. (2021), ferritin as an index of iron deficiency and overload, <https://doi.org/10.1002/14651858.CD011817.pub2>.
- Kaul et al. (2018), population metabolomic fingerprints of ferritin and hemoglobin, <https://doi.org/10.3390/nu10111800>.
- Ko et al. (2020), AGA guideline on iron-deficiency-anemia evaluation (ferritin <45 ng/mL), <https://doi.org/10.1053/j.gastro.2020.06.046>.
- Cullis et al. (2018), BSH investigation of a raised serum ferritin, <https://doi.org/10.1111/bjh.15166>.
- HPP documentation `blood_tests` dataset documentation and field/QC inventory.
- PhenoBench issue-15 blood-source audit applies to every `blood_tests` Task in this card set.

## V0 Benchmark Execution

The two same-visit V1 tracks completed on 2026-07-29; both Ridge/GBDT rows per
track are locally successful and remotely `FINISHED` in operational source.  Results predict total ferritin,
not iron stores.

- Nightingale: n=3,351; test=512; best R2=0.217 (GBDT), with paired delta R2
  +0.063 [-0.001, 0.104] over the GBDT age/sex/BMI floor.
- DXA, exploratory: n=2,178; test=334; best R2=0.209 (GBDT), with paired
  delta R2 +0.071 [-0.016, 0.107].
- Full rows and provenance:
  deep dive and
  aggregate review.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=394; train=264, validation=70, test=60

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | -0.009 | 71.037 | 0.258 |
| Linear | `linear` | 0.735 | 36.422 | 0.867 |
| Trees | `gbdt_delta_r2` | 0.487 | 50.631 | 0.774 |
| LOCF | `last_observation_carried_forward` | 0.685 | 39.656 | 0.868 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
