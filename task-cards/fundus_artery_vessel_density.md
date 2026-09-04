# Fundus Artery Mask Area Fraction Task Card

Task id: `fundus_artery_vessel_density`

Evidence status: grounded

Evidence reviewed: 2026-07-19

Benchmark status: complete

## Target

Color-fundus artery-mask area fraction as a continuous participant-visit
measurement. The registered Task id retains the source field's `vessel_density`
name.

Implementation facts:

- bodily system: ophthalmic/retinal
- target route: `fundus.automorph_artery_vessel_density`
- unit: ratio
- device/acquisition: iCare DRSplus non-mydriatic confocal camera, 45° color fundus imaging
- construction/QC: filter AutoMorph quality `good` and central captures; average recaptures within eye; require both eyes; bilateral mean per participant-stage
- valid range: 0-1
- default stages: `00_00_visit` and `02_00_visit`
- paper fidelity: paper-inspired RetiMap representative; not OCTA density

## Why This Matters

This color-fundus artery-mask area fraction quantifies the proportion of the
analyzed image occupied by AutoMorph-classified artery pixels. It is a structural mask-density feature,
not a perfusion or OCTA measurement. Prediction supports retinal
morphology estimation, not diagnosis of retinal or systemic disease.

## Related HPP Measurements

The other 17 AutoMorph vessel measures, image quality, and eye/position are
same-modality relatives. Blood pressure, glycaemia, lipids, body composition,
sleep apnea, and vascular phenotypes are candidate systemic correlates reported
in HPP RetiMap analyses.

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
- These are camera- and pipeline-specific color-fundus features. OCTA capillary
  density, perfusion, or FAZ findings cannot be transferred to this target: this
  artery-mask area fraction is a structural proportion of the image occupied by larger
  reflectance-visible vessels, whereas OCTA perfusion density
  is a depth-resolved capillary-flow measure. HPP has no OCT/OCTA, FAZ, RNFL, CRAE, CRVE,
  or AVR route for this batch.
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns, target
quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Zhou et al. (2022), AutoMorph, <https://doi.org/10.1167/tvst.11.7.12>.
- Durbin et al. (2017), OCTA retinal microvascular density quantification, <https://doi.org/10.1001/jamaophthalmol.2017.0080>.
- Shapira et al. (2024), RetiMap: HPP retinal vascular measures (medRxiv preprint), <https://doi.org/10.1101/2024.04.05.24305164>.
- HPP documentation `fundus` dataset documentation and QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=2298; train=1589, validation=356, test=353

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.055 | 0.004 | 0.241 |
| Linear | `linear` | 0.737 | 0.002 | 0.859 |
| Trees | `gbdt_delta_r2` | 0.704 | 0.002 | 0.840 |
| LOCF | `last_observation_carried_forward` | 0.712 | 0.002 | 0.854 |

<!-- healthformer-wave-evidence:end -->

## Open Questions

- The v0 systemic Benchmark Tracks received clinical review on 2026-07-28.
- Cross-modal V1 value-add is tracked in
  #28.
- A retinal-systemic association surface is tracked in
  #29.
