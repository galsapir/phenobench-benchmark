# Thyroid-Stimulating Hormone Task Card

Status: draft

Task id: `tsh`

Evidence status: grounded

Evidence reviewed: 2026-07-29

Benchmark status: complete

## Target

Thyroid-Stimulating Hormone as a continuous participant-visit scalar.

Implementation facts:

- bodily system: endocrine
- target route: `blood_tests.bt__tsh`
- unit: mIU/L
- acquisition/source: pinned Weizmann blood-test source; nearest completed visit within 180 days
- default stages: `00_00_visit` and `02_00_visit`
- collapse: participant-stage mean
- range/QC: 0.001-500 mIU/L broad plausibility guard
- paper fidelity: exact HealthFormer intervention-panel analyte

## Why This Matters

TSH is the primary biochemical signal in thyroid-axis screening. TSH alone does not diagnose hypothyroidism or define treatment need.

## Related HPP Measurements

Free T4/T3, thyroid medication, hypothyroidism status, age, sex, and pregnancy-related factors.

## Benchmark-Track Evidence

Population metabolomics evidence is mixed for continuous TSH. A large
multi-cohort analysis associated higher TSH with an adverse lipoprotein profile,
whereas targeted KORA metabolomics found many FT4 associations but none with
TSH. DXA studies report smaller, sex- and adiposity-dependent associations.
Nightingale and DXA therefore motivate empirical cross-modal tracks, not an
expected clinical screening model.

## Clinically Meaningful Variants

Continuous prediction is primary. Any clinical category requires
measurement-compatible thresholds, population validation, and a separate Task;
this card does not authorize diagnostic bins.

## Baselines And Ceilings

For V1→V2 evaluation, compare an age, sex, and BMI floor, prior-value LOCF, OLS on prior
value plus allowed demographics, and GBDT on the same inputs. Use one cohort and
split for all comparisons.

## Caveats

- Mask the full target-window blood-test family, thyroid hormones, derived thyroid states, and same-visit hypothyroidism labels.
- Reference intervals depend on assay, age, pregnancy, acute illness, and medication; use continuous prediction only.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns,
target quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Ku et al. (2023), TSH reference-interval considerations, <https://doi.org/10.3803/EnM.2023.1778>.
- van Vliet et al. (2021), multi-cohort TSH and metabolomic/lipid profiles, <https://doi.org/10.1186/s12916-021-02130-1>.
- Jourdan et al. (2013), thyroid hormones and targeted metabolomics, <https://doi.org/10.1007/s11306-013-0563-4>.
- Sun et al. (2024), TSH and DXA adiposity, <https://doi.org/10.1371/journal.pone.0314704>.
- HPP Research OS `blood_tests` dataset documentation and field/QC inventory.
- PhenoBench issue-15 blood-source audit applies to every `blood_tests` Task in this card set.

## V0 Benchmark Execution

The two same-visit V1 tracks completed on 2026-07-29; both Ridge/GBDT rows per
track are locally successful and remotely `FINISHED` in operational source. TabSwift
is deferred until GPU execution is configured.

- Nightingale: n=4,276; test=644; best R2=0.007 (GBDT), with no clear gain
  over age/sex/BMI.
- DXA: n=3,029; test=456; best R2=-0.000 (Ridge), with no clear gain over
  age/sex/BMI.
- Full rows and provenance:
  deep dive and
  aggregate review.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=629; train=449, validation=97, test=83

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | -0.038 | 2.021 | 0.060 |
| Linear | `linear` | 0.271 | 1.693 | 0.595 |
| Trees | `gbdt_delta_r2` | 0.259 | 1.708 | 0.534 |
| LOCF | `last_observation_carried_forward` | 0.376 | 1.567 | 0.632 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
