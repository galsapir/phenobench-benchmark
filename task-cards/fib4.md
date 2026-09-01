# FIB-4 / FIB-3 Task Card

Status: draft

Task ids: `fib4`, `fib3`

Evidence status: grounded

Evidence reviewed: 2026-07-28

Benchmark status: complete

## Target

Cross-sectional FIB liver-score regression on HPP V1. The shared card covers
two related derived targets:

- `fib4`: the standard age-containing FIB-4 score.
- `fib3`: the age-residualized sibling without the explicit age term.

Current PhenoBench implementation computes:

```text
FIB-4 = age * AST / (platelets * sqrt(ALT))
FIB-3 = AST / (platelets * sqrt(ALT))
```

Implementation facts:

Shared by both Task ids:

- source components: age, AST, ALT, platelets
- AST field: `bt__ast_got`
- ALT field: `bt__alt_gpt`
- platelet field: `bt__platelets`
- target source: `weizmann`
- default research stage: `00_00_visit`
- primary metric: R2

For `fib4`:

- valid range: 0.1-10.0

For `fib3`:

- valid range: 0.001-1.0

## HPP data source

The AST / ALT / platelet inputs load from the pinned Weizmann `blood_tests`
source. The live operational source HMO table was audited as a candidate replacement.
**Audit decision: keep Weizmann.** operational source + `events` yields net −23.9%
baseline coverage with ~40% cohort turnover, low exact agreement (58.1%), and a
platelet input that shows an html_parser–associated discrepancy. Rationale and
reconsideration triggers:
blood-test source audit §9.

## Why This Matters

FIB-4 is a simple clinical liver-fibrosis score. It is widely used because it
requires only age and routine blood tests. It has reported associations with
cardiovascular events, cardiovascular mortality, and all-cause mortality.

For PhenoBench, FIB-4 is useful partly because it is clinically familiar and
partly because it exposes a common benchmark trap: formula-derived targets can
look predictable for reasons that are not biologically interesting.

## Baselines And Ceilings

The required floor is a no-modality-feature baseline: `NoFeaturesPredictor`
contributes no modality features. **This card covers two Task ids and they now
differ:** FIB-4's `DemographicFloorStrategy` fits **sex and BMI**, and FIB-3's
still fits age, sex and BMI.

Age was dropped from FIB-4 in #6 (2026-08-20) because it appears directly in the
target formula's numerator, which made the floor structurally inflated: current
code documents Surrogate's FIB-4 floor at about R2 0.31, while the source
material estimates about R2 0.40-0.60 because age dominates the score. FIB-3 kept
all three, because its formula takes AST, ALT and platelets and none of those is
a floor covariate.

**The FIB-4 scores below predate that change**, measured against the age/sex/BMI
floor, so read them as historical rather than as the current matrix - figure 1
marks those contracts `historical` and their replacements `configured` with no
verified route yet. **The FIB-3 history is unaffected.**

The more meaningful liver-signal question is whether a model captures AST, ALT,
and platelet-related information beyond age. `Fib3Task` is the cleaner paired
task because it removes the explicit age term from the formula and has a much
lower demographic floor around R2 0.07 in the task code.

## Benchmark-Track Evidence

OpenEvidence review supports Nightingale metabolomics as the primary systemic
fibrosis modality and DXA body composition as secondary. The proposed fixed
27-field Nightingale panel contains no AST, ALT, platelets, or albumin, so it
does not directly expose a FIB component. An age/sex/BMI floor is
formula-circular for FIB-4 because age is a direct numerator term, which is why
the v0 FIB-4 floor no longer holds age. FIB-3 should still accompany FIB-4 as the
cleaner liver-signal headline; a strong FIB-4 score alone is not evidence of
fibrosis biology.

## V0 Benchmark Execution

The frozen same-visit V1→V1 matrices completed on 2026-07-29. All twelve rows
across FIB-3 and FIB-4 are locally successful and remotely `FINISHED` in
operational source.

- FIB-3 Nightingale: n=4,371; test=656; best R2=0.123 (CPU TabSwift).
  DXA: n=2,908; test=443; best R2=0.105 (CPU TabSwift).
- FIB-4 Nightingale: n=4,371; test=656; best R2=0.345 (Ridge).
  DXA: n=2,907; test=443; best R2=0.357 (CPU TabSwift).
- FIB-4 demographic floors were R2 0.315-0.331, confirming the predeclared
  age-formula circularity; FIB-3 remains the cleaner sensitivity analysis.
- Full rows and provenance:
  FIB-3 deep dive,
  FIB-4 deep dive, and
  aggregate review.

## Caveats

- Age is literally in the FIB-4 formula, so demographic performance can be
  misleading.
- ALT and platelets also vary with age, compounding the age signal.
- FIB-4 was developed in diseased cohorts; interpretation in a healthy
  population is less straightforward.
- Standard clinical cutoffs can overcall fibrosis in older healthy adults.
- Strong raw R2 may reflect formula reconstruction, not liver-specific biology.

## Metrics

- Primary: R2 for continuous score regression.
- Useful companion: AUROC for clinically relevant FIB-4 thresholds, if the task
  is extended to classification.
- Essential audit: report `Fib3Task` or age-residualized comparison whenever
  making a liver-specific claim.

## References

- Source material: `docs/task_cards/source_material/foundation-model-surrogate-targets-v1.md`
- Liver fibrosis scores prognosis meta-analysis: <https://pubmed.ncbi.nlm.nih.gov/36001034/>
- Caussy et al. (2019), serum metabolites and advanced fibrosis:
  <https://doi.org/10.1136/gutjnl-2018-317584>
- Ciardullo et al. (2022), body-fat distribution, steatosis, and fibrosis:
  <https://doi.org/10.1093/ajcn/nqac059>
- Age and sex reference values for FIB-4 in healthy adults: <https://www.tandfonline.com/doi/full/10.1080/00365513.2025.2559352>
- FIB-3 without age factor: <https://www.ghadvances.org/article/S2772-5723(22)00127-3/fulltext>
- Demographic floor estimate source: <https://www.nature.com/articles/s41598-025-30518-z>

## Open Questions

- Should FIB-4 remain a primary task, or should FIB-3 become the preferred liver
  signal task?
- Which FIB-4 classification threshold is appropriate for a healthy HPP-like
  cohort?
- **Resolved (#6, 2026-08-20): no warning.** The overlap is removed where the
  remainder is still a demographic floor, and the row stops competing where it
  is not. FIB-4 declares `demographic_features: [sex, bmi]`, dropping the age
  term the formula takes. A row that still supplies its target's ingredients
  carries `benchmark_role: reference` and
  `test_a_publishing_row_that_declares_a_formula_overlap_does_not_rank` refuses
  the ranked combination, so the guarantee is a refusal rather than a label.
  **FIB-3 is unchanged and keeps age, sex and BMI**, because its formula takes
  AST, ALT and platelets and none of those is a floor covariate, so it had no
  overlap to remove. This card is shared between the two Task ids, so the
  distinction matters: the floor comparison between them is no longer
  like-for-like on covariates, which is the point rather than a side effect.
