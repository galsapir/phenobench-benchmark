# One-Minute Orthostatic SBP Drop Task Card

Status: draft

Task id: `orthostatic_sbp_drop_1min`

Evidence status: grounded

Evidence reviewed: 2026-07-19

Benchmark status: complete

## Target

One-Minute Orthostatic SBP Drop as a continuous participant-visit measurement.

Implementation facts:

- bodily system: autonomic/cardiovascular
- target route: `blood_pressure lying and standing-one-minute SBP`
- unit: mmHg
- device/acquisition: OMRON HEM-RML31 protocol; lying after rest and standing at one minute
- construction/QC: lying SBP minus standing-one-minute SBP; require both components; positive means a fall
- valid range: derived drop -200 to 200 mmHg; components require 20-300 mmHg
- default stages: `00_00_visit` and `02_00_visit`
- paper fidelity: paper-inspired HPP autonomic analogue

## Why This Matters

The continuous one-minute SBP change captures early blood-pressure compensation
after standing, integrating vascular and baroreflex responses; larger one-minute falls
reflect weaker early orthostatic compensation and are associated with adverse outcomes
including falls, syncope, fractures, and mortality (Juraschek et al. 2017). It is one
component of the orthostatic response, not a standalone diagnosis of autonomic dysfunction
or orthostatic hypotension.

## Related HPP Measurements

Lying and one-/three-minute standing DBP and pulse, dizziness, medications,
nightly HRV, ECG, glycaemic status, activity, hydration, and vascular measures.

## Clinically Meaningful Variants

Continuous prediction is primary. A one-minute systolic fall overlaps with the systolic
component of classical orthostatic hypotension (a sustained SBP fall of at least 20 mmHg or
DBP fall of at least 10 mmHg within three minutes of standing; Freeman et al. 2011) and can
be an early manifestation of it, but this Task does not by itself establish classical
orthostatic hypotension: it carries no diastolic reading, no sustained or repeated
measurement across the three-minute window, and no symptoms. Nor does it establish initial
orthostatic hypotension, which requires beat-to-beat monitoring within the first 15 seconds
of standing.

## Baselines And Ceilings

For V1→V2 evaluation, compare age/sex/BMI demographic floor, prior-value LOCF,
OLS on prior value plus demographics, and GBDT on the same inputs. Use one
cohort and split for every comparison.

## Caveats

- Mask the full same-visit BP family; lying and standing components, later standing readings, and derived orthostatic flags directly reveal the target.
- The clinical >=20 mmHg threshold also depends on DBP, timing, repeatability,
  medications, and symptoms; negative target values represent an SBP rise.
- HRV and pulse-response features can support a future autonomic phenotype, but
  should not be retrofitted into the definition of this measured endpoint.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns, target
quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Freeman et al. (2011), consensus statement on the definition of orthostatic hypotension, <https://doi.org/10.1007/s10286-011-0119-5>.
- Juraschek et al. (2018), orthostatic hypotension and cardiovascular outcomes, <https://doi.org/10.1161/JAHA.118.008884>.
- Juraschek et al. (2017), timing of orthostatic assessment and adverse outcomes,
  <https://doi.org/10.1001/jamainternmed.2017.2937>.
- American Heart Association (2024), orthostatic hypotension in adults with
  hypertension, <https://doi.org/10.1161/HYP.0000000000000236>.
- HPP Research OS `blood_pressure` dataset documentation and QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=3592; train=2485, validation=560, test=547

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.022 | 9.327 | 0.153 |
| Linear | `linear` | 0.088 | 9.006 | 0.299 |
| Trees | `gbdt_delta_r2` | 0.071 | 9.091 | 0.271 |
| LOCF | `last_observation_carried_forward` | -0.447 | 11.345 | 0.277 |

<!-- healthformer-wave-evidence:end -->

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29. Direct modality evidence is limited; V1 DXA
tests regional lean/fat distribution and V1 sleep tests nocturnal autonomic and
oxygenation physiology beyond age/sex/BMI. All BP components remain excluded.
See `04-cardiovascular-lipid.md`.

## v0 Final-Test Status

The classical release is complete: Ridge/logistic and GBDT are remotely verified on every approved exact cohort and rendered in the Figure 1 task deep dives. TabSwift is deferred until GPU execution is configured; it is not a missing or failed row.

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
- The multimeasure autonomic endpoint audit is tracked in
  [#30](https://github.com/PhenoAI/phenobench/issues/30).
- Cross-modal V1 value-add is tracked in
  [#28](https://github.com/PhenoAI/phenobench/issues/28).
