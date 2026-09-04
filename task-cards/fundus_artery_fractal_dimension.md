# Fundus Artery Fractal Dimension Task Card

Task id: `fundus_artery_fractal_dimension`

Evidence status: grounded

Evidence reviewed: 2026-07-19

Benchmark status: complete

## Target

Fundus Artery Fractal Dimension as a continuous participant-visit measurement.

Implementation facts:

- bodily system: ophthalmic/retinal
- target route: `fundus.automorph_artery_fractal_dimension`
- unit: unitless
- device/acquisition: iCare DRSplus non-mydriatic confocal camera, 45° color fundus imaging
- construction/QC: filter AutoMorph quality `good` and central captures; average recaptures within eye; require both eyes; bilateral mean per participant-stage
- valid range: 1-2
- default stages: `00_00_visit` and `02_00_visit`
- paper fidelity: paper-inspired RetiMap representative

## Why This Matters

This target quantifies the AutoMorph artery fractal dimension, a dimensionless index of the
geometric complexity of the arterial network (higher values indicate more branching); the
code guards it to the 1-2 range. In HPP, arterial fractal dimension decreases with age and
is higher in males (RetiMap; Shapira et al. 2024). Prediction here supports retinal
morphology estimation, not diagnosis of retinal or systemic disease.

## Related HPP Measurements

The other 17 AutoMorph vessel measures, image quality, eye/position, BP, glycaemia, lipids, and vascular phenotypes.

## Clinically Meaningful Variants

Continuous prediction is primary. Diagnostic thresholds or categories require
measurement-, device-, protocol-, and population-compatible validation and are
not implied by this Task.

## Baselines And Ceilings

For V1→V2 evaluation, compare age/sex/BMI demographic floor, prior-value LOCF,
OLS on prior value plus demographics, and GBDT on the same inputs. Use one
cohort and split for every comparison.

## Caveats

- Mask the entire same-visit fundus modality, including every AutoMorph output, image/mask path, quality score, eye/position-derived feature, and target aliases.
- These are camera- and pipeline-specific color-fundus features; fractal dimension depends
  on the image, segmentation, and AutoMorph implementation, so values are not comparable
  across pipelines or devices and other-pipeline normatives are context, not thresholds for
  this AutoMorph artery output. HPP has no OCT/OCTA, FAZ, RNFL, CRAE, CRVE, or AVR route for
  this batch.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns, target
quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Zhou et al. (2022), AutoMorph, <https://doi.org/10.1167/tvst.11.7.12>.
- Shapira et al. (2024), RetiMap: HPP retinal vascular measures (medRxiv preprint), <https://doi.org/10.1101/2024.04.05.24305164>.
- HPP documentation `fundus` dataset documentation and QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=2298; train=1589, validation=356, test=353

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.032 | 0.023 | 0.180 |
| Linear | `linear` | 0.637 | 0.014 | 0.799 |
| Trees | `gbdt_delta_r2` | 0.586 | 0.015 | 0.766 |
| LOCF | `last_observation_carried_forward` | 0.590 | 0.015 | 0.792 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- The v0 systemic Benchmark Tracks received clinical review on 2026-07-28.
