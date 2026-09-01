# Serum Urate Task Card

Status: draft

Task id: `urate`

Evidence status: grounded

Evidence reviewed: 2026-07-29

Benchmark status: complete

## Target

Serum Urate as a continuous participant-visit scalar.

Implementation facts:

- bodily system: renal/metabolic
- target route: pinned Weizmann `blood_tests.bt__uric_acid`
- unit: mg/dL
- acquisition/source: pinned Weizmann blood-test source; nearest completed visit within 180 days
- default stages: `00_00_visit` and `02_00_visit`
- collapse: participant-stage mean
- range/QC: 0.5-20 mg/dL broad plausibility guard
- paper fidelity: exact HealthFormer intervention/cross-modal analyte

## Why This Matters

Serum urate reflects purine metabolism and renal handling. Prediction does not diagnose gout or establish urate-lowering treatment benefit.

## Related HPP Measurements

Creatinine/eGFR, medications, diet, alcohol, metabolic markers, and gout history.

## Clinically Meaningful Variants

Continuous prediction is primary. Any clinical category requires
measurement-compatible thresholds, population validation, and a separate Task;
this card does not authorize diagnostic bins.

## Baselines And Ceilings

For V1→V2 evaluation, compare an age, sex, and BMI floor, prior-value LOCF, OLS on prior
value plus allowed demographics, and GBDT on the same inputs. Use one cohort and
split for all comparisons.

## Caveats

- Mask same-window urate aliases and any derived hyperuricemia/gout label; exclude future medication/outcome data.
- Sex-specific reference ranges, renal function, diuretics, fasting state, and allopurinol materially affect values.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Benchmark-Track Evidence

OpenEvidence review and broader Paperclip search support the fixed DXA panel
for both V1→V1 and V1→V2 tracks. Visceral fat has replicated dose-dependent
associations with serum urate beyond basic anthropometrics. This motivates a
regional-adiposity benchmark; it does not establish causality. Mask every urate
alias, gout/hyperuricaemia label, medication field, and blood-test input. The
V1→V2 Allowed Information Set does not include V1 urate.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns,
target quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- FitzGerald et al. (2020), American College of Rheumatology gout guideline, <https://doi.org/10.1002/acr.24180>.
- HPP Research OS `blood_tests` dataset documentation and field/QC inventory.
- PhenoBench issue-15 blood-source audit applies to every `blood_tests` Task in this card set.
- Gu et al. (2025), visceral adipose tissue and serum urate:
  <https://doi.org/10.1186/s12889-025-22557-y>.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=515; train=355, validation=84, test=76

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.420 | 1.098 | 0.668 |
| Linear | `linear` | 0.827 | 0.600 | 0.912 |
| Trees | `gbdt_delta_r2` | 0.773 | 0.686 | 0.883 |
| LOCF | `last_observation_carried_forward` | 0.805 | 0.636 | 0.917 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
