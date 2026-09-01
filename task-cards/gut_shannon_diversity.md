# Gut Shannon Diversity Task Card

Status: draft

Task id: `gut_shannon_diversity`

Evidence status: grounded

Evidence reviewed: 2026-07-14

## Target

Species-level natural-log Shannon entropy, `H = -sum(p * ln(p))`. Duplicate
taxa are averaged, positive abundances renormalized per sample, H computed in
nats, then repeated samples averaged per participant/stage. Y is entropy, not
the effective number `exp(H)`.

Implementation facts:

- target field: `gut_shannon_diversity` - the declared, Track-facing value. The
  quantity behind it is derived species-level Shannon entropy rather than a
  stored column
- target dataset: `gut_microbiome`
- target source: None (loaded through HPP `hpp_data_loader`)
- default research stage: `00_00_visit`
- valid range: 0.01-8.5 nats; a plausibility filter, not clinical bins
- primary metric: R2

## Why This Matters

Shannon summarizes richness and evenness. It supports ecological forecasting,
not a universal gut-health score, diagnosis, taxon interpretation, or causal
dietary claim.

## Related HPP Measurements

In 10,068 HPP participants, diet logs predicted Shannon at r = 0.24. Separate
HPP work linked broader functional microbiome features to CGM, DXA, and liver
ultrasound; that evidence is not Shannon-specific.

## Clinically Meaningful Variants

No universal clinical threshold is defensible: 30 of 41 meta-analyzed
healthy-versus-disease comparisons found no difference. Disease status should
be Y with Shannon optionally as X; quantile bins are diagnostics, not clinical
classes.

## Baselines And Ceilings

`NoFeaturesPredictor` contributes no modality features; `DemographicFloorStrategy`
fits age, sex, and BMI. Last observation carried forward (LOCF) copies prior Y.
Ordinary least squares (OLS) and gradient-boosted trees (GBDT) fit prior Y plus
demographics. HealthFormer reported
LOCF and per-modality linear baselines, not trees or the demographic floor.
Compare representations on one cohort.

## Caveats

- Shannon is compositional and sensitive to sequencing, taxonomy, handling,
  and batch (`bcl_id`).
- Stage is the temporal key because this route has no reliable sample timestamp.
- Diversity discards taxon identity; similar Shannon values can describe very
  different communities.
- HealthFormer curated 1,259 species; the loader exposes a broader cohort-wide
  set, so this Task is not parameter-identical.

## Metrics

R2 is primary. Also report RMSE, MAE, Pearson r, Spearman rho, LOCF deltas, and
target-decile residuals. Batch residuals require carrying `bcl_id` into
evaluation.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- HPP `gut_microbiome` documentation for species abundance fields.
- Segev et al. (2026), HPP diet-microbiome associations,
  <https://doi.org/10.1038/s41591-026-04312-x>.
- Keshet and Segal (2024), HPP microbiome and metabolic-health map,
  <https://doi.org/10.1038/s41467-024-53832-y>.
- Ma et al. (2019), diversity-disease meta-analysis,
  <https://doi.org/10.1038/s41396-019-0395-y>.

## v0 Final-Test Status

- Approved Benchmark Tracks predict V1 and V2 Shannon diversity from the exact
  V1 16-field diet panel plus age, sex, and BMI; no prior microbiome value
  enters.
- Ridge and GBDT produced four remotely verified rows. Best held-out R² was
  0.048 at V1 and 0.069 at V2.
- Reported gain is over the matched demographic-only model. Prior-target LOCF
  consumes a different Allowed Information Set and remains a separate
  historical reference, not a floor inside these diet Tracks.
- TabSwift is deferred until GPU execution. Full contract and results:
  `05-sleep-gut-aging.md`.

## Open Questions

- Should `bcl_id` and read-depth QC be carried into a batch sensitivity view?
