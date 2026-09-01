# Fundus Vein Tortuosity Density Task Card

Status: draft

Task id: `fundus_vein_tortuosity_density`

Evidence status: grounded

Evidence reviewed: 2026-07-15

Benchmark status: complete

## Target

Fundus Vein Tortuosity Density as a continuous participant-visit measurement.

Implementation facts:

- bodily system: ophthalmic/retinal
- target route: `fundus.automorph_vein_tortuosity_density`
- unit: 1/pixels
- device/acquisition: iCare DRSplus 45°×40° color fundus imaging
- construction/QC: filter AutoMorph quality `good` and central captures; average recaptures within eye; require both eyes; bilateral mean per participant-stage
- valid range: 0-2
- default stages: `00_00_visit` and `02_00_visit`
- paper fidelity: paper-inspired RetiMap representative

## Why This Matters

This target quantifies AutoMorph local-curvature tortuosity density on veins. Prediction supports repeatable retinal morphology estimation, not diagnosis of retinal or systemic disease.

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
- These are camera- and pipeline-specific color-fundus features. HPP has no OCT/OCTA, FAZ, RNFL, CRAE, CRVE, or AVR route for this batch.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns, target
quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Zhou et al. (2022), AutoMorph, <https://doi.org/10.1167/tvst.11.7.12>.
- Shapira et al. (2024), HPP retinal microvascular architecture, <https://doi.org/10.1101/2024.04.05.24305164>.
- HPP Research OS `fundus` dataset documentation and QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=2298; train=1589, validation=356, test=353

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | -0.004 | 0.026 | 0.044 |
| Linear | `linear` | 0.445 | 0.020 | 0.670 |
| Trees | `gbdt_delta_r2` | 0.433 | 0.020 | 0.661 |
| LOCF | `last_observation_carried_forward` | 0.365 | 0.021 | 0.672 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- The v0 systemic Benchmark Tracks received clinical review on 2026-07-28.
