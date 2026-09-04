# Gut Species Richness Task Card

Task id: `gut_species_richness`

Evidence status: grounded

Evidence reviewed: 2026-07-15

Benchmark status: complete

## Target

Gut Species Richness as a continuous HPP scalar.

Implementation facts:

- bodily system: gut microbiome
- target route: `gut_microbiome species-level positive relative_abundance`
- unit: observed species/sample
- acquisition: OMNIgene GUT OM-200 stool collection, shotgun sequencing, MetaPhlAn 4
- construction/QC: count distinct positive `clade_name` per participant/sample at `level == species`, then participant-stage mean
- valid range: 1-5000 observed species
- paper fidelity: paper-inspired scalarization of HealthFormer's species-abundance modality

## Why This Matters

Observed species richness is a simple microbiome alpha-diversity measure distinct from Shannon diversity. Prediction does not establish gut health or causal ecological benefit.

## Related HPP Measurements

Shannon/Simpson diversity, strain/SGB profiles, abundance features, sequencing depth, stool metadata, diet, medication, and host phenotypes.

## Clinically Meaningful Variants

The continuous measurement is primary. Device-, protocol-, and population-
specific clinical thresholds are secondary diagnostics only and do not define
a diagnosis in this Task.

## Baselines And Ceilings

For V1→V2 evaluation, compare age/sex/BMI demographic floor, prior-value LOCF, OLS on prior value plus demographics, and GBDT on the same inputs on one cohort/split.

## Caveats

- Mask all same-visit microbiome taxa/abundances and every richness/diversity derivative; sequencing depth and batch are QC/evaluation strata only.
- Richness depends on sequencing depth, taxonomic pipeline/version, detection threshold, and specimen handling; it is not exp(Shannon).
- A good score supports prediction of this measurement only; it does not
  establish diagnosis, causality, or intervention response.

## Metrics

Primary R2. Also report RMSE, MAE, Pearson r, Spearman rho, split Ns, target
quantiles, and same-cohort deltas versus LOCF.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- Segev et al. (2026), HPP gut-microbiome richness analysis, <https://doi.org/10.1038/s41591-026-04312-x>.
- Blanco-Míguez et al. (2023), MetaPhlAn 4, <https://doi.org/10.1038/s41587-023-01688-w>.
- HPP documentation `gut_microbiome species-level positive relative_abundance` dataset documentation and QC inventory.

## Execution Evidence

<!-- healthformer-wave-evidence:start -->

- protocol: paired HPP V1→V2; every baseline uses the same eligible participants
- common cohort: n=5943; train=4113, validation=938, test=892

| Baseline | Strategy | Test R2 | RMSE | Pearson r |
| --- | --- | ---: | ---: | ---: |
| Demographic | `demographic_floor` | 0.016 | 64.612 | 0.129 |
| Linear | `linear` | 0.614 | 40.453 | 0.784 |
| Trees | `gbdt_delta_r2` | 0.607 | 40.851 | 0.780 |
| LOCF | `last_observation_carried_forward` | 0.577 | 42.355 | 0.785 |

<!-- healthformer-wave-evidence:end -->

## v0 Final-Test Status

- Approved Benchmark Tracks predict V1 and V2 species richness from the exact
  V1 16-field diet panel plus age, sex, and BMI; no prior microbiome value
  enters.
- Ridge and GBDT produced four remotely verified rows. Best held-out R² was
  0.049 at V1 and 0.046 at V2.
- Reported gain is over the matched demographic-only model. Prior-target LOCF
  consumes a different Allowed Information Set and remains a separate
  historical reference, not a floor inside these diet Tracks.
-  Full contract and results:
  `05-sleep-gut-aging.md`.

## Open Questions

- Domain-expert review remains outstanding; evidence grounding and real-run gates are complete.
