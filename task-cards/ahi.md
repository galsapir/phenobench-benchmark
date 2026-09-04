# AHI Task Card

Task id: `ahi`

Evidence status: grounded

Evidence reviewed: 2026-07-29

## Target

Apnea-Hypopnea Index — number of apnea + hypopnea events per hour of sleep —
averaged across recorded nights for the configured research stage. The default
stage is `00_00_visit`. Continuous-scalar regression. AHI is the canonical
clinical sleep-disordered-breathing readout, with established severity
thresholds: <5 normal, 5–15 mild, 15–30 moderate, ≥30 severe OSA.

Current PhenoBench implementation:

- target field: `ahi` (matches `urp/pipelines/fusion_model/fusion_cgm_sleep/data.py`)
- target dataset: `sleep`
- target source: None (no upstream-source qualifier; the `sleep` dataset is treated as single-source)
- default research stage: `00_00_visit`
- valid range: 0.0 – 200.0 events/hr (see Caveats; tighter bound than the fusion-side `None`)
- primary metric: R²

## Why This Matters

AHI is the **comparator, not the headline**, on phenobench's sleep axis. The
source-material's primary sleep surrogate is Hypoxic Burden (HB); AHI is
documented there as a "well-known comparator, even though it's weaker"
(`docs/task_cards/source_material/foundation-model-surrogate-targets-v1.md`).
Three reasons:

1. **Head-to-head, AHI loses to HB on CVD outcomes.** Same-cohort studies
   (MrOS n=2743, SHHS n=5111) show HB top-quintile HR 2.73 / 1.96 for CVD
   mortality while AHI is **not** significant in the same models
   (PMC6451769).
2. **AHI is BMI-confounded; HB isn't.** BMI/WC/body fat explain <2% of HB
   variance vs ~78% by ventilatory burden (AJRCCM 202209-1808OC). The
   demographic-floor baseline already absorbs much of AHI's signal; a
   "beats the floor" claim on AHI is weaker evidence of sleep biology than
   the same claim on HB.
3. **AHI counts events; HB integrates desaturation severity.** HB strictly
   contains more information about the physiological insult.

AHI is still worth having because clinical thresholds are familiar — it
gives leaderboard readers a legible anchor. But the "did the sleep encoder
learn sleep biology?" claim belongs on HB once that task lands. This task's
role is to unblock the sleep axis and provide the comparator.

For fusion parity: AHI is the only sleep-axis member of the locked
five-surrogate panel (`hba1c`, `ahi`, `glyca`, `vat`, `triglycerides`) in
`urp/pipelines/fusion_model/fusion_cgm_sleep_eval/the internal evaluation configuration.
Porting AHI to phenobench lets the same panel be evaluated on both sides.

## Baselines And Ceilings

- **Floor**: no-modality-feature baseline. `NoFeaturesPredictor` contributes
  no modality features, and `DemographicFloorStrategy` fits age, sex, and BMI
  only. Captures a meaningful fraction of AHI variance because BMI is the
  dominant non-sleep predictor of obstructive events.
- **Empirical floor (parity runs, 2026-06-02)**:
  - **Maximal cohort** (full HPP AHI cohort at `00_00_visit`,
    n = 9711, splits 6692/1549/1470, α = 1.0): R² ≈ **0.241**.
  - **Matched cohort** (restricted to fusion's A_static cohort via
    `phase0/data/alignment_table.csv`, n = 3444 matches fusion exactly,
    splits 2373/552/519, α = 1.0): R² ≈ **0.274**.
  - **Strict parity** (matched cohort + matched train/val split extracted
    from `fusion_dataset.pkl` + matched α = 10 + matched BMI imputation
    policy, n_train = 2841, n_val = 603): R² = **0.230335**.
- **Fusion-side reference**: the fusion `fusion_cgm_sleep` Phase 0 reports
  `r2_demo = 0.230317` (RidgeCV α-grid `[0.01..1000]`, α-selected = 10)
  on n = 3444 (A_static trained-tuples cohort ∩ valid AHI).
- **Parity verdict**:
  - Maximal: ΔR² = +0.010 (within ±0.10). Different cohort + estimator.
  - Matched: ΔR² = +0.044 (within ±0.10). Same cohort; remaining gap from
    split + α policy.
  - Strict: ΔR² = **+1.77 × 10⁻⁵** (within ±0.001). Wiring is verified to
    machine-precision: same source data, same per-pid collapse, same
    valid_range, same demographics, same imputation policy, same split,
    same α — phenobench reproduces fusion's r2_demo to 5 decimal places.
  See `scripts/verify_ahi_floor_parity.py` for the reproducible check
  (`--mode {maximal,matched,strict,all}`).
- **Sleep-modality ceiling** (when wired): a sleep-encoder embedding via
  `ParticipantEmbeddingPredictor` + `RidgeCVStrategy`. The interesting
  number is `delta_r2_vs_floor` on the leaderboard — populated automatically
  per `docs/decisions.md` 2026-05-18 pairing-infra decision.
- **Cross-modality null**: CGM features via `CgmIgluPredictor` should
  *not* lift over the floor; failure to lift here is the expected and
  useful negative signal.

## Physiological Time-Series V1

the internal evaluation configuration evaluates
a residual 1-D CNN trained end-to-end on target-blind baseline 12-lead ECG
samples against the participant's mean WatchPAT AHI. Because the predictor
contains no WatchPAT channel or derived sleep summary, it is a cross-modal
representation probe rather than a same-sensor reconstruction. It remains
same-stage association, not future OSA forecasting or diagnosis. Published
ECG-to-OSA evidence uses overnight single-lead recordings; transferring that
precedent to one resting 10-second 12-lead ECG is exploratory.
The target is the mean of the available baseline-night AHI values. It is not a
guaranteed three-night target. A 10-second resting ECG contains no observed
overnight respiratory-event sequence, so this route is an association proxy.

Held-out exploratory result (test n=861): temporal R² 0.1560 versus tuned
age/sex/BMI R² 0.2382, delta-R² -0.0822 (95% CI
[-0.1476, -0.0113]); temporal MAE 6.0121 versus 5.7925 events/hour,
delta-MAE +0.2196 events/hour (95% CI [-0.0388, +0.4686]). The paired
MAE interval includes zero; the R² comparison favors demographics.

## Caveats

- **BMI confounding is severe.** Lifting above the demographic floor on
  AHI may indicate the encoder learned BMI more accurately, not sleep
  biology. The honest claim requires both raw R² and residualized-after-
  demographics inspection. HB is the better headline target for this
  reason.
- **Per-night → per-visit collapse is `mean`** (matches the fusion-side
  note in `urp/pipelines/fusion_model/fusion_cgm_sleep/the internal evaluation configuration).
  This loses night-to-night variability; a per-night AHI task could be a
  separate version.
- **Heavy-tailed distribution.** Most participants are near zero (no OSA),
  with a long tail of severe cases. R² on raw AHI can be dominated by the
  few extreme participants. Secondary metrics (Spearman ρ, MAE) are more
  robust.
- **`valid_range = (0, 200)` is a guard, not a clinical cutoff.** Real AHI
  cannot be negative; >200 events/hr is essentially sensor/scoring error.
  Fusion uses `None` here; phenobench requires a tuple, so the tighter
  bound rejects obvious outliers without trimming clinically meaningful
  severe-OSA cases.
- **Label noise from device + scoring rules.** HPP sleep data is
  WatchPAT-derived (home device, not in-lab PSG). AASM scoring rule
  edition matters (2012 vs 2017, 3% vs 4% desaturation criterion).
  Treat HPP AHI as label-noisy.
- **AHI ≠ OSA diagnosis.** Clinical OSA diagnosis combines AHI with
  symptoms (daytime sleepiness, etc.). A model that predicts AHI well
  is not necessarily a diagnostic-quality OSA model.

## Metrics

- Primary: R².
- Secondary: MAE (clinically interpretable in events/hr), Spearman ρ
  (robust to the heavy tail).
- Audit views: residualized R² after regressing out demographics, split
  Ns, cohort ID, and the `delta_r2_vs_floor` column on the leaderboard
  once a sleep-modality row exists.

## Benchmark-Track Evidence

literature review prioritizes DXA and Nightingale as two distinct
cross-modal V1 tracks. DXA regional adiposity is more informative than BMI
alone for sleep-disordered breathing. HPP evidence directly links VAT to pAHI
and shows that NMR metabolites predict clinical OSA beyond age and BMI, with
strong sex heterogeneity. Both tracks must exclude every sleep, oximetry,
respiratory-event, and hypoxic-burden field. These are same-stage association
benchmarks, not OSA diagnosis.

## References

- Source material (which lists AHI as a comparator to Hypoxic Burden, not
  as a primary surrogate):
  `docs/task_cards/source_material/foundation-model-surrogate-targets-v1.md`
  (sleep section, §"Hypoxic Burden"/L94-L96).
- Fusion-side wiring: `urp/pipelines/fusion_model/fusion_cgm_sleep/data.py:134-140`
  (target map entry) and `urp/pipelines/fusion_model/fusion_cgm_sleep_eval/the internal evaluation configuration
  (locked surrogate panel).
- Hypoxic Burden ≫ AHI for CVD mortality:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC6451769/> (MrOS + SHHS).
- AHI BMI-confounding context:
  <https://www.atsjournals.org/doi/10.1164/rccm.202209-1808OC>.
- Urtnasan et al. (2018), overnight single-lead ECG OSA-event detection:
  <https://doi.org/10.1007/s10916-018-0963-0>.
- AASM Scoring Manual (rule version applied by the HPP sleep pipeline
  should be confirmed by the data owner; relevant for label-noise context).

## Open Questions

- Confirm with the data owner that the upstream HPP sleep field is literally
  `ahi`, rather than a similarly named rule-specific field.
- Confirm whether the benchmark's per-visit collapse should remain the mean of
  all valid baseline records or use a worst-night/rule-specific construction.
- The executable V1 route loads bare `ahi` and takes an unfiltered mean over
  non-null baseline records after the Task's numeric validity guard. It does
  not guarantee a fixed night count or apply a separate night-eligibility
  filter.
- Confirm AASM scoring rule edition used by HPP (2012 vs 2017) for the
  card's label-noise context.
- Should a `ahi_log1p` variant be the first version instead of raw-scale
  `AhiTask`, given the heavy-tailed distribution?
- ~~What is the empirical HPP AHI demographic-floor R²?~~ Answered
  2026-06-02. Three runs, increasingly strict:
  - Maximal HPP cohort (n = 9711, α = 1): R² ≈ 0.241.
  - Cohort matched to fusion's A_static (n = 3444, α = 1): R² ≈ 0.274.
  - Strict parity (n = 3444, matched split, α = 10): R² = 0.230335 vs
    fusion's r2_demo = 0.230317 — ΔR² = +1.77 × 10⁻⁵.
  See `scripts/verify_ahi_floor_parity.py`.
- Is `(0, 200)` the right `valid_range`, or should we use the field's
  documented sensor maximum from the WatchPAT specification?
