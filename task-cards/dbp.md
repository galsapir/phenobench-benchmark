# Diastolic Blood Pressure Task Card

Task id: `dbp`

Evidence status: grounded

Evidence reviewed: 2026-07-19

Benchmark status: complete

## Target

Diastolic Blood Pressure as a continuous participant-visit measurement.

Implementation facts:

- bodily system: cardiovascular/lipid
- target route: `blood_pressure.sitting_blood_pressure_diastolic`
- unit: mmHg
- device/acquisition: OMRON HEM-RML31; backup/manual source is not row-labelled
- construction/QC: canonical first sitting reading after rest; participant-stage mean; documented BP QC
- valid range: 10-180 mmHg
- default stages: `00_00_visit` and `02_00_visit`
- paper fidelity: exact HealthFormer endpoint

## Why This Matters

DBP reflects arterial pressure during cardiac relaxation and adds information distinct from SBP; it carries independent cardiovascular prognostic value particularly in middle-aged adults, while systolic pressure dominates risk in older adults (Flint et al. 2019). Prediction does not diagnose hypertension or establish treatment need.

## Related HPP Measurements

SBP, pulse pressure, MAP, pulse rate, orthostatic readings, medications, BMI, and vascular measures.

## Clinically Meaningful Variants

Continuous prediction is primary. Guideline diastolic thresholds differ across bodies
(ACC/AHA 2017 places stage 1 hypertension at DBP 80-89 mmHg and stage 2 at >=90 mmHg;
ESH 2023 and ESC 2024 place hypertension at DBP >=90 mmHg), and a hypertension diagnosis
generally rests on more than a single office reading -- typically repeated readings and often
out-of-office (home or ambulatory) confirmation. This single-visit participant-mean DBP is
therefore not a hypertension label, and diagnostic bins are not implied by this Task.

## Baselines And Ceilings

For V1→V2 evaluation, compare age/sex/BMI demographic floor, prior-value LOCF,
OLS on prior value plus demographics, and GBDT on the same inputs. Use one
cohort and split for every comparison.

## Caveats

- Mask the full same-visit blood-pressure family, including repeat/contralateral DBP, SBP, MAP, pulse pressure, and derived hypertension states.
- Cuff size, posture, rest, medication, acute state, and unlabelled backup/manual measurements affect DBP.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns, target
quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Leiherer et al. (2024), earlier-life SBP/DBP and cardiovascular risk, <https://doi.org/10.1016/j.isci.2024.109097>.
- Whelton et al. (2017), ACC/AHA high-blood-pressure guideline (DBP thresholds), <https://doi.org/10.1161/HYP.0000000000000065>.
- Mancia et al. (2023), ESH guidelines for the management of arterial hypertension, <https://doi.org/10.1097/HJH.0000000000003480>.
- McEvoy et al. (2024), ESC guidelines for elevated blood pressure and hypertension, <https://doi.org/10.1093/eurheartj/ehae178>.
- Flint et al. (2019), systolic and diastolic BP and cardiovascular outcomes, <https://doi.org/10.1056/NEJMoa1803180>.
- HPP documentation `blood_pressure` dataset documentation and QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=5901; train=4077, validation=928, test=896

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.133 | 9.961 | 0.366 |
| Linear | `linear` | 0.401 | 8.280 | 0.634 |
| Trees | `gbdt_delta_r2` | 0.400 | 8.290 | 0.633 |
| LOCF | `last_observation_carried_forward` | 0.135 | 9.948 | 0.622 |

<!-- healthformer-wave-evidence:end -->

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29. HPP and literature review supports V1 sleep and
fundus morphology beyond age/sex/BMI. The full same-visit BP and vascular family
must remain excluded. See
`04-cardiovascular-lipid.md`.

## v0 Final-Test Status

The classical release is complete: Ridge/logistic and GBDT are remotely verified on every approved exact cohort and rendered in the Figure 1 task deep dives.

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
