# Alanine Aminotransferase Task Card

Task id: `alt`

Evidence status: grounded

Evidence reviewed: 2026-07-28

Benchmark status: complete

## Target

Alanine Aminotransferase as a continuous participant-visit scalar.

Implementation facts:

- bodily system: hepatobiliary
- target route: `blood_tests.bt__alt_gpt`
- unit: U/L
- acquisition/source: pinned Weizmann blood-test source; nearest completed visit within 180 days
- default stages: `00_00_visit` and `02_00_visit`
- collapse: participant-stage mean
- range/QC: 1-1000 U/L broad plausibility guard
- paper fidelity: exact HealthFormer endpoint

## Why This Matters

ALT is a common marker of hepatocellular injury. Prediction does not diagnose MASLD, fibrosis, or a liver disease cause.

## Related HPP Measurements

AST, GGT, bilirubin, albumin, liver ultrasound, BMI, alcohol, and medications.

## Benchmark-Track Evidence

literature review supports Nightingale metabolic profiles and DXA regional
body composition as the two strongest systemic liver modalities beyond
age/sex/BMI. The fixed Nightingale panel contains no ALT, AST, albumin, or
platelets, avoiding direct target reconstruction. ALT remains an injury marker,
not a steatosis measurement, so these tracks ask about metabolic context for
ALT variation and cannot be interpreted as MASLD detection.

## V0 Benchmark Execution

The frozen same-visit V1→V1 matrix completed on 2026-07-29; this is distinct
from the longitudinal HealthFormer-inspired evidence below. All six v0 rows
are locally successful and remotely `FINISHED` in operational source.

- Nightingale: n=5,498; test=831; best R2=0.200 (CPU TabSwift).
- DXA: n=3,754; test=570; best R2=0.177 (CPU TabSwift).
- The paired modality-gain intervals for both linear and GBDT rows cross zero
  in both tracks; no robust added-information claim is supported.
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

- Mask same-window liver tests and any FIB-3/FIB-4/HSI/MAFLD feature containing ALT.
- Exercise, medication, alcohol, acute injury, assay upper limits, age, and sex affect ALT.
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
- common cohort: n=1002; train=701, validation=163, test=138

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.077 | 8.120 | 0.369 |
| Linear | `linear` | 0.273 | 7.208 | 0.562 |
| Trees | `gbdt_delta_r2` | 0.193 | 7.591 | 0.553 |
| LOCF | `last_observation_carried_forward` | -0.078 | 8.774 | 0.514 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
