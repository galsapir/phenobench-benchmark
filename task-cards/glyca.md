# GlycA Task Card

Task id: `glyca`

Evidence status: grounded

Evidence reviewed: 2026-08-15

## Target

Nightingale NMR GlycA concentration. Continuous-scalar regression. The default
research stage is `00_00_visit`, but the Task can be configured for another
available stage.

Implementation facts:

- target field: `GlycA`
- target dataset: `nightingale`
- target source: None (Nightingale's primary source is set in the loader, not
  on the Task)
- target unit: mmol/L
- default research stage: `00_00_visit`
- valid range: 0.5-3.0 mmol/L; a PhenoBench plausibility filter, not a
  reference interval
- primary metric: R2

## Why This Matters

GlycA is an NMR inflammatory biomarker reflecting glycosylated acute-phase
proteins. It is more stable than hsCRP and has been associated with myocardial
infarction and mortality in population cohorts.

For PhenoBench, GlycA is a useful inflammation-axis target because it is
measured in the same Nightingale panel as many metabolic biomarkers but is not
just a standard lipid or glucose target.

**What a row here does not support.** GlycA is an inflammatory-state marker
measured on one NMR platform at one visit. A row is a same-visit association: it
is not a diagnosis of any inflammatory condition, and it is emphatically not the
myocardial-infarction or mortality prediction that the external GlycA literature
reports - those are prospective endpoints in other cohorts, and citing them as
motivation is not the same as claiming them here.

## Related HPP Measurements

Demonstrated in HPP, and persisted in this repository rather than asserted:

- **Two matched tracks are already scored on canonical test splits**, both from
  the 2026-07-29 deep dive in
  an internal review record:
  V1 CBC + demographics reaches test R² = 0.150 (95% CI [0.077, 0.217]) on a
  checksum-bound cohort of 2,760 with 8 features, and V1 DXA + demographics
  reaches R² = 0.120 (95% CI [0.071, 0.166]) on 6,580. TabSwift is top-ranked in
  both; the gradient-boosted and cross-validated linear rows sit within the
  intervals, so no method separation is established.
- Both tracks exclude every CBC input and target history as a leakage guard, and
  the CBC track's native support before Task eligibility was 5,225 participants
  against the 2,760 that survive it - the eligibility narrowing is large enough
  to matter when comparing the two tracks' numbers.

**Both tracks clear the demographic floor on the paired comparison**, which is
the quantity that matters rather than the raw R2 above: CBC
**ΔR2 = +0.074 (95% CI [+0.018, +0.127])** on n = 2,760 and DXA
**ΔR2 = +0.059 ([+0.035, +0.085])** on n = 6,580. The eight-field CBC panel is
therefore a real result, not a floor artefact.

Proposed rather than shown: that a learned multimodal representation beats it.
Nothing committed answers that, and the CBC delta is the number to beat.

**These are `reviewable` rows, not `final` ones.** Measured across the committed
leaderboards: all 787 rows carry `curation_state: reviewable` and none is
`final`. A complete fresh v0 re-run is committed to, so every figure in this
section is pre-re-run evidence that the re-run supersedes - persisted and citable
today, not a frozen result. **Which curation states the Figure 1 export accepts
is the export track's live question, not this card's**; read the two counts
above, not a gate.

## Clinically Meaningful Variants

**No categorical GlycA variant is defensible, and unlike the glycemic targets
the reason is that no clinical threshold exists at all.** GlycA is a composite
NMR signal from glycosylated acute-phase proteins; it has no diagnostic cutoff,
no guideline-endorsed reference interval, and its published associations with
myocardial infarction, stroke and mortality are reported per standard deviation
or per quartile within each study cohort rather than against a fixed value.

Two properties make a transferred cutoff worse here than elsewhere:

- **The value is platform-defined.** GlycA is a Nightingale NMR quantity, not a
  standardised assay with an interconversion to another platform's inflammatory
  measure. A cutoff from one NMR cohort does not carry to another cohort's
  calibration, and it does not carry to hsCRP at all - the two are correlated
  markers of different things, and the card should not be read as licensing a
  swap.
- **The distribution is shifted by transient state.** Acute infection and
  chronic inflammatory disease move GlycA substantially, and the default cohort
  applies no such exclusion, so any binning would place a state-dependent
  subgroup on one side of the line.

Quartiles or standard-deviation bands are the honest way to report a
distribution here, and they are a presentation choice, not a Task. The
continuous target stays primary.

## Benchmark-Track Evidence

Benchmark-Track Evidence reviewed: 2026-07-29.

literature review prioritized DXA body composition as the strongest
independent shared predictor panel: adiposity is consistently associated with
GlycA through inflammatory state. The existing matched HPP deep dive also
found useful CBC signal. These findings motivate separate DXA and CBC tracks;
they do not establish causality. Same-assay Nightingale remains a ceiling only.

## Baselines And Ceilings

The required floor is a no-modality-feature baseline: `NoFeaturesPredictor`
contributes no modality features, and `DemographicFloorStrategy` fits age, sex,
and BMI. The task code records a low demographic floor around R2 0.07, while
the source material expected R2 0.10-0.20 before HPP estimation.

Natural comparators include hsCRP if available, leukocyte/inflammatory blood
markers, NMR engineered features, diet/microbiome features, and sleep/activity
tracks. Same-panel NMR predictors need explicit leakage review.

## Caveats

- GlycA is an inflammatory-state marker, not a disease diagnosis.
- Acute infection, chronic inflammatory disease, medication, and batch/assay
  effects can dominate signal.
- Nightingale features may contain near-direct correlates of GlycA.
- A good GlycA score should be claimed as inflammatory biomarker signal, not
  MI or mortality prediction.

## Metrics

Primary metric is R2. Secondary MAE and Spearman are useful. Audit views should
include demographic-floor delta R2, split Ns, same-panel leakage exclusions,
and sensitivity to participants with acute inflammatory outliers if available.

## References

- Source material: `docs/task_cards/source_material/foundation-model-surrogate-targets-v1.md`
- Riggs et al., 2022, GlycA and hsCRP associations with MI and ischemic stroke:
  <https://doi.org/10.1016/j.ajpc.2022.100373>
- Gruppen et al., 2019, GlycA and mortality in PREVEND plus meta-analysis:
  <https://doi.org/10.1111/joim.12953>
- Kohn et al. (2025), the Human Phenotype Project metabolic abstract, *SLEEP*,
  <https://doi.org/10.1093/sleep/zsaf090.0054>. Local copy in **HPP documentation**:
  `assets/papers/hpp/kohn_2025_0054_the_human_phenotype_project_metabol/`.
- Dullaart et al., 2015, GlycA, adiposity, and glucose-tolerance status:
  <https://doi.org/10.1016/j.clinbiochem.2015.05.001>

## Open Questions

- Is hsCRP available and mature enough to act as a clinical comparator?
- Which Nightingale feature exclusions are needed to avoid measuring GlycA by
  proxy from the same panel?
- Should inflammatory disease or acute-infection exclusions be part of the
  default cohort?
