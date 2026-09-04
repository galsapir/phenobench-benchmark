# Serum Albumin Task Card

Task id: `albumin`

Evidence status: grounded

Evidence reviewed: 2026-07-28

Benchmark status: complete

## Target

Serum Albumin as a continuous participant-visit scalar.

Implementation facts:

- bodily system: hepatobiliary
- target route: `blood_tests.bt__albumin`
- unit: g/dL
- acquisition/source: pinned Weizmann blood-test source; nearest completed visit within 180 days
- default stages: `00_00_visit` and `02_00_visit`
- collapse: participant-stage mean
- range/QC: 1-7 g/dL
- paper fidelity: exact HealthFormer endpoint

## Why This Matters

Serum albumin reflects synthesis, inflammation, hydration, nutrition, and loss. Prediction does not isolate liver synthetic function or diagnose disease.

## Related HPP Measurements

Nightingale albumin, total protein, liver enzymes, renal measurements, inflammation, and body composition.

## Benchmark-Track Evidence

literature review ranked plasma NMR metabolomics and DXA regional body
composition as the two most defensible systemic liver modalities. Albumin needs
a stricter target mask than the other liver Tasks: every clinical or
Nightingale albumin field must be absent. The proposed fixed 27-field
Nightingale lipid/fatty-acid/GlycA panel contains no albumin, ALT, AST, or
platelet field and is therefore eligible. DXA is an orthogonal secondary track.
Neither turns albumin into a liver-specific endpoint.

## V0 Benchmark Execution

The frozen same-visit V1→V1 matrix completed on 2026-07-29; this is distinct
from the longitudinal HealthFormer-inspired evidence below. All six v0 rows
are locally successful and remotely `FINISHED` in operational source.

- Nightingale: n=4,110; test=614; best R2=0.143 (CPU TabSwift).
- DXA: n=2,702; test=402; best R2=0.127 (CPU TabSwift).
- All paired modality-gain intervals touch or cross zero, so the results do
  not support a robust added-information claim beyond age/sex/BMI.
- Full rows and provenance: deep dive and
  aggregate review.

## Clinically Meaningful Variants

Continuous prediction is primary. Any clinical category requires
measurement-compatible thresholds, population validation, and a separate Task;
this card does not authorize diagnostic bins.

## Baselines And Ceilings

For V1→V2 evaluation, compare an age, sex, and BMI floor, prior-value LOCF, OLS on prior
value plus allowed demographics, and GBDT on the same inputs. Use one cohort and
split for all comparisons.

## Caveats

- Mask clinical and Nightingale albumin, same-window protein/liver panels, and derived scores containing albumin.
- Hydration, inflammation, renal/gastrointestinal loss, nutrition, and assay differences confound interpretation.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns,
target quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Reicher et al. (2024), HPP longitudinal aging phenotypes, <https://doi.org/10.1038/s43587-024-00734-9>.
- Rinella et al. (2023), AASLD NAFLD practice guidance, <https://doi.org/10.1097/HEP.0000000000000323>.
- Masoodi et al. (2021), metabolomics/lipidomics in NAFLD, <https://doi.org/10.1038/s41575-021-00502-9>.
- HPP documentation `blood_tests` dataset documentation and field/QC inventory.
- PhenoBench issue-15 blood-source audit applies to every `blood_tests` Task in this card set.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=652; train=443, validation=115, test=94

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.174 | 0.196 | 0.423 |
| Linear | `linear` | 0.390 | 0.168 | 0.630 |
| Trees | `gbdt_delta_r2` | 0.325 | 0.177 | 0.574 |
| LOCF | `last_observation_carried_forward` | 0.187 | 0.194 | 0.609 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
