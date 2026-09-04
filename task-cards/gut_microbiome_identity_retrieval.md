# Gut Microbiome Longitudinal Identity Retrieval Task Card

Task id: `gut_microbiome_identity_retrieval`

Evidence status: grounded

Evidence reviewed: 2026-08-03

Benchmark status: complete

## Target

Closed-set same-person longitudinal retrieval. Each eligible participant
contributes one V1 gut-microbiome sample as the query and one V2 sample as the
gallery mate. The relevance target is exact participant identity: every query
has exactly one relevant gallery item.

Implementation facts:

- target: same-participant relevance between a query and gallery sample
- target dataset: **`gut_microbiome`** on the class - this is the Track-facing
  value, and a Benchmark Track keys on it. The specimen index is read from
  `ds.omics.gut_mb_reads`, which is where the data lives rather than what the
  Task declares; naming only the table here described a Track this Task does not
  resolve
- target source: None, meaning the primary source of `target_dataset`
- representation sources: MetaPhlAn species, MetaPhlAn SGB-level strain, and
  URS abundance tables, evaluated as separate Predictor rows
- feature selection: primary microbiome rows use all observed features on the
  fixed query/gallery candidate set; capped and PCA-compressed rows are
  sensitivity controls only
- target construction: pair one `00_00_visit` sample with one `02_00_visit`
  sample per participant; when a stage has repeated samples, select the sample
  with the most non-human reads and break ties by sample id
- evaluation-unit grain: one participant-specific query/gallery sample pair
- candidate policy: closed-set, one gallery sample per eligible participant,
  with a shared cohort requiring both visits and all three raw feature spaces
- target shape: ranking
- eval category: retrieval
- primary metric: Recall@1
- primary microbiome distance: Aitchison CLR distance with documented
  multiplicative zero replacement. The replacement delta is half the single
  global minimum positive abundance after closing every query and gallery row
  in the fixed evaluation cohort; nonzero values are shrunk within each row.

## Why This Matters

This Task asks whether a longitudinal biospecimen retains enough
participant-specific signal to retrieve its matched follow-up sample within a
declared HPP gallery. It can support a cohort-constrained identifiability and
persistence claim after technical controls. It cannot by itself establish
artifact-free biological persistence, general representation quality,
open-world identification, clinical usefulness, or privacy safety.

Successful identity retrieval is privacy-relevant. Aggregate metrics and
anonymous rank distributions are reviewable; raw participant identities,
sample ids, and per-query match records must not be persisted by default.

## Related HPP Measurements

HPP gut microbiome documentation reports 7,007 participants with at least two
visits and identifies sequencing batch (`bcl_id`) as an important longitudinal
covariate. Age, sex, and BMI are available as demographic shortcut controls.
Sequencing batch, production date, and human/non-human read counts are
technical shortcut controls. These controls determine whether retrieval is
more plausibly biological or acquisition-driven; they are not alternative
health targets.

## Clinically Meaningful Variants

There are no clinical bins for identity retrieval. The following are separate
benchmark variants rather than thresholds on this Task:

- pairwise verification with a declared false-match operating point;
- open-set identification where some queries have no gallery mate;
- cross-modal matching between different HPP modalities;
- similar-patient retrieval with phenotype or clinical relevance labels.

## Baselines And Ceilings

The floor is a uniform ranking, equivalent to the expected score of a random
gallery permutation. It must yield Recall@K = K / gallery size under the
declared tie policy.

Required controls and comparators:

- uniform/random ranking floor;
- identity-shuffled relevance null for every feature-bearing run;
- age, sex, and BMI representation;
- sequencing-batch and read-depth technical representation;
- MetaPhlAn species ranked by Aitchison CLR distance;
- MetaPhlAn SGB-level strain abundance ranked by Aitchison CLR distance;
- URS abundance ranked by Aitchison CLR distance;
- square-root cosine rows for continuity with the first completed benchmark;
- raw-cosine species-abundance sensitivity;
- a 32-component PCA compression control fitted only on the gallery index.

Fixed pretrained and learned metric embeddings are future Predictor rows. An
identity-trained representation is a task-specific ceiling, not evidence of
general representation quality.

## Caveats

- Closed-set Recall@1 assumes every query has a mate and does not measure
  rejection of unknown participants.
- Performance depends on gallery size, visit interval, feature selection,
  normalization, distance, and sample-selection policy.
- Sequencing batch, kit, processing date, read depth, disease state,
  medication, household, and duplicate samples can mimic identity signal.
- MetaPhlAn "strain" rows are SGB-level bins, not classical microbial strains.
- Raw abundance geometry is compositional and method-dependent; CLR requires
  explicit zero handling before distances are computed.
- Gallery-fitted PCA is a classical compression baseline, not a learned
  participant-identity model.
- Sharing a cohort across raw feature spaces improves comparator fairness but
  excludes participants missing any of those representations.
- Same-person matching is a re-identification surface; embeddings or rankings
  should not be released without a threat-model review.

## Metrics

Recall@1 is primary. Also report Recall@5, Recall@10, MRR, median rank,
normalized median rank, gallery size, and a CMC curve. Exact ties receive their
expected random position within the tied block; an all-equal representation
must therefore score at chance rather than perfect retrieval.

Run-level review figures should be aggregate-only and live under
`review/retrieval/`:

Primary review artifacts for feature-bearing runs:

- `retrieval_performance_summary.png` for Top 1/5/10, MRR, shuffled Top 1,
  random Top 1, and gallery size in one reviewer-facing summary;
- `retrieval_cmc_curve.png` for the fraction of participants recovered within
  the top K gallery matches;
- `retrieval_same_vs_different_distance_density.png` for same-person versus
  sampled-different distance density;
- `retrieval_same_vs_different_distance_ecdf.png` for threshold-readiness and
  verification-style separation.

QA artifacts:

- `retrieval_rank_distribution.png` for rank histogram and ECDF;
- `retrieval_shuffled_null_comparison.png` for true matching versus the
  identity-shuffled null.

Conditional QA artifact:

- `retrieval_tie_block_distribution.png` only when an exact feature-bearing run
  has nontrivial score ties.

The uniform/random run uploads only `retrieval_performance_summary.png`,
`retrieval_cmc_curve.png`, and `retrieval_shuffled_null_comparison.png`.

Report 95% query-participant bootstrap confidence intervals with the gallery
held fixed, plus the identity-shuffled null from the same similarity matrix.
All comparator rows must share the Task cohort fingerprint and candidate count.

## References

- HPP `gut_microbiome` dataset documentation in the HPP documentation.
- Franzosa et al. (2015), *Identifying personal microbiomes using metagenomic
  codes*, <https://doi.org/10.1073/pnas.1423854112>.
- Gloor et al. (2017), *Microbiome datasets are compositional: and this is not
  optional*, <https://doi.org/10.3389/fmicb.2017.02224>.
- Martín-Fernández et al. (2003), *Dealing with zeros and missing values in
  compositional data sets using nonparametric imputation*,
  <https://doi.org/10.1023/A:1023866030544>.
- Chen et al. (2021), *The long-term genetic stability and individual
  specificity of the human gut microbiome*,
  <https://doi.org/10.1016/j.chom.2021.03.005>.
- Mayer et al. (2023), *Distance-based linkage of personal microbiome
  records*, <https://doi.org/10.1016/j.cose.2023.103538>.
- NIST Face Recognition Technology Evaluation, identification and
  verification protocol definitions,
  <https://pages.nist.gov/frvt/html/frvt1N.html>.

## Completion Gate

The Task counts as complete only after the card is grounded; the uniform,
demographic, technical, primary Aitchison species/strain/URS, sqrt-cosine
continuity, species raw, and species PCA configs run on the same real HPP
cohort; terminal operational source/execution registry rows are fetchable; null controls behave as
expected; and aggregate review plots contain no participant-level data.

## Execution Evidence

All required real rows were refreshed on 2026-08-03 with one shared V1-to-V2 cohort:

- participants/candidates: 5,945
- random-gallery Recall@1 baseline: 0.0168%
- per-query predictions, ranks, participant ids, sample ids, and embeddings:
  not persisted
- generated retrieval figures: aggregate-only PNGs under each run's
  `review/retrieval/` folder and included in `review/review_summary.json`
- review bundle:
  the internal evaluation configuration

| Row | Features | Distance / transform | Recall@1 | Recall@5 | MRR | Mean rank |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| Uniform floor | - | uniform random ranking | 0.017% | 0.084% | 0.002 | 2,973.0 |
| Age + sex + BMI | 4 | cosine | 0.387% | 1.850% | 0.025 | 670.0 |
| Technical metadata | 330 | cosine | 0.034% | 0.050% | 0.002 | 2,564.1 |
| Species, primary | 4,188 | Aitchison CLR, multiplicative half-min zeros | 85.114% | 88.124% | 0.866 | 100.1 |
| SGB strain, primary | 4,346 | Aitchison CLR, multiplicative half-min zeros | 85.887% | 88.663% | 0.872 | 97.6 |
| URS, primary | 3,067 | Aitchison CLR, multiplicative half-min zeros | 86.594% | 89.167% | 0.879 | 90.5 |
| Species, continuity | 4,188 | square-root cosine | 69.504% | 76.939% | 0.731 | 164.0 |
| SGB strain, continuity | 4,346 | square-root cosine | 71.119% | 78.234% | 0.746 | 159.7 |
| URS, continuity | 3,067 | square-root cosine | 70.177% | 77.696% | 0.738 | 157.9 |
| Species, raw sensitivity | 4,188 | raw cosine | 25.114% | 36.283% | 0.309 | 452.5 |
| Species, PCA-32 control | 32 | gallery-fitted PCA + cosine | 31.405% | 46.728% | 0.387 | 277.4 |

The fixed shuffled-identity null was near chance for every feature-bearing row.
Square-root preprocessing materially changes the result, and the low technical
control does not prove artifact-free biological persistence. Gallery-size,
time-gap, matched-negative, open-set/privacy, and pretrained-representation
work is tracked in #40,
#41, and
#42.

## Open Questions

- Should future versions stratify by exact follow-up interval once a reliable
  stool collection timestamp is available?
- Should family or household members be retained as hard negatives or reported
  as a separate slice?
- Which pretrained microbiome representation should be the first model-based
  Predictor comparator?
- What release policy should govern participant-level embeddings and ranks?
