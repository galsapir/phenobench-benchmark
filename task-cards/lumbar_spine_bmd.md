# Lumbar Spine BMD Task Card

Status: draft

Task id: `lumbar_spine_bmd`

Evidence status: grounded

Evidence reviewed: 2026-07-29

## Target

Raw AP-spine DXA `dxa.spine_l1_l4_bmd`, in g/cm2. This is the recorded L1-L4
summary, not whole-body `body_spine_bmd` or a T-/Z-score. Participant records
are averaged before means below 0.01 are filtered. PhenoBench does not re-read
images or exclude individual vertebrae, so Y is not adjudicated clinically.

Implementation facts:

- target field: `spine_l1_l4_bmd`
- target dataset: `dxa`
- target source: None (loaded through HPP `hpp_data_loader`)
- default research stage: `00_00_visit`
- valid range: 0.01-3.0 g/cm2
- primary metric: R2

## Why This Matters

Central spine and hip DXA are clinical reference measurements; L1-L4 is one
recommended site, not the sole gold standard. This slowly changing skeletal
trait supports forecasting, not osteoporosis diagnosis, fracture-risk
prediction, or causal inference.

## Related HPP Measurements

In HPP women, bone density aligned more strongly with time from menopause than
chronological age, grounding `sex_specific_factors`. Same-visit companions
include hip/femoral-neck DXA, fracture history, grip, and gait.

## Clinically Meaningful Variants

Do not apply universal g/cm2 thresholds. A future site-specific Task may use
`spine_l1_l4_t_score` in postmenopausal women and men aged at least 50;
premenopausal women and men under 50 require Z-score interpretation. A
patient-level osteoporosis phenotype should combine valid spine,
hip/femoral-neck sites, and fracture history.

## Baselines And Ceilings

`NoFeaturesPredictor` contributes no modality features; `DemographicFloorStrategy`
fits age, sex, and BMI. Last observation carried forward (LOCF) copies prior Y.
Ordinary least squares (OLS) and gradient-boosted trees (GBDT) fit prior Y plus
demographics. HealthFormer reported
LOCF and per-modality linear baselines, not trees or the demographic floor.
Compare representations on one cohort.

## Benchmark-Track Evidence

OpenEvidence review and broader literature search prioritize grip strength and
objective movement/activity over NMR, CGM, sleep, or same-scan DXA features for
a leakage-safe BMD benchmark. HPP gait work also reports strong prediction of
bone-density traits. Same-visit DXA body composition is excluded because it
shares the target acquisition; V1 grip is valid for both V1 and V2 targets.

## Caveats

- Raw BMD avoids circularity from demographic reference scores but retains
  strong age, sex, and menopause structure.
- Degeneration, fracture, calcification, positioning, or hardware can inflate
  lumbar BMD; ISCD vertebral exclusions are not applied here.
- Longitudinal clinical change requires facility-specific precision estimates.

## Metrics

R2 is primary. Also report RMSE and MAE in g/cm2, Pearson r, Spearman rho,
same-cohort deltas against LOCF, and age/sex-stratified residuals.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- HPP `dxa` dataset documentation for `spine_l1_l4_bmd`.
- ISCD (2023), Adult Official Positions, <https://iscd.org/official-positions-2023/>.
- Reicher et al. (2025), HPP health-disease continuum,
  <https://doi.org/10.1038/s41591-025-03790-9>.
- Montgomery et al. (2024), objective activity and BMD,
  <https://doi.org/10.1093/jbmr/zjae017>.
- Gabet et al. (2026), HPP gait foundation model,
  <https://doi.org/10.48550/arXiv.2603.25283>.

## Open Questions

- Should a patient-level bone-health Task jointly model spine, hip, and
  fracture history?
