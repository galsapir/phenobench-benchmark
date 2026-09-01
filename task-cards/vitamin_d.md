# 25-Hydroxyvitamin D Task Card

Status: draft

Task id: `vitamin_d`

Evidence status: grounded

Evidence reviewed: 2026-07-29

Benchmark status: complete

## Target

25-Hydroxyvitamin D as a continuous participant-visit scalar.

Implementation facts:

- bodily system: endocrine
- target route: `blood_tests.bt__vitamin_d`
- unit: ng/mL
- acquisition/source: pinned Weizmann blood-test source; nearest completed visit within 180 days
- default stages: `00_00_visit` and `02_00_visit`
- collapse: participant-stage mean
- range/QC: 3-200 ng/mL
- paper fidelity: exact HealthFormer intervention-panel analyte

## Why This Matters

25-hydroxyvitamin D is the standard circulating vitamin-D status measurement. Prediction does not establish deficiency, supplementation need, or causal benefit.

## Related HPP Measurements

Season, supplement use, sun exposure, BMI, calcium, renal/liver measurements, and bone density.

## Benchmark-Track Evidence

Population NMR studies associate 25(OH)D with lipoprotein, fatty-acid, and
saturation profiles beyond abdominal obesity. DXA studies associate regional
fat distribution with 25(OH)D beyond BMI. These findings motivate Nightingale
and DXA tracks; they do not remove confounding by season, supplementation, sun
exposure, renal function, or ancestry.

## Clinically Meaningful Variants

Continuous prediction is primary. Any clinical category requires
measurement-compatible thresholds, population validation, and a separate Task;
this card does not authorize diagnostic bins.

## Baselines And Ceilings

For V1→V2 evaluation, compare an age, sex, and BMI floor, prior-value LOCF, OLS on prior
value plus allowed demographics, and GBDT on the same inputs. Use one cohort and
split for all comparisons.

## Caveats

- Mask same-window vitamin-D aliases and derived deficiency labels; supplement use is a confounder/proxy, not deterministic leakage.
- Season is a major unmodeled source of variation because the current Task
  collapses participant-stage values without retaining collection month.
- HPP documentation flags cross-assay/calibration concerns. Live EAV mixes ng/mL and nmol/L; the pinned Task source stays in ng/mL and must not be silently replaced.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns,
target quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Demay et al. (2024), Endocrine Society vitamin-D guideline, <https://doi.org/10.1210/clinem/dgae290>.
- Vogt et al. (2016), population NMR/MS profile of 25(OH)D, <https://doi.org/10.1093/ije/dyw222>.
- HPP Research OS `blood_tests` dataset documentation and field/QC inventory.
- PhenoBench issue-15 blood-source audit applies to every `blood_tests` Task in this card set.

## V0 Benchmark Execution

The two same-visit V1 tracks completed on 2026-07-29; both Ridge/GBDT rows per
track are locally successful and remotely `FINISHED` in operational source. TabSwift
is deferred until GPU execution is configured. Collection season remains unmodeled.

- Nightingale: n=2,283; test=336; best R2=0.121 (Ridge). GBDT showed paired
  delta R2 +0.063 [0.005, 0.128] over age/sex/BMI.
- DXA: n=1,575; test=246; best R2=0.089 (Ridge), with paired delta R2
  +0.035 [0.011, 0.059].
- Full rows and provenance:
  deep dive and
  aggregate review.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=227; train=161, validation=36, test=30

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | -0.010 | 9.463 | 0.346 |
| Linear | `linear` | 0.090 | 8.979 | 0.477 |
| Trees | `gbdt_delta_r2` | 0.079 | 9.036 | 0.454 |
| LOCF | `last_observation_carried_forward` | -0.297 | 10.724 | 0.437 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
