# Diet-to-Sleep Causal Effect Task Card

Status: draft

Task id: `diet_sleep_causal_effect`

Evidence status: grounded

Evidence reviewed: 2026-07-15

## Decision Summary

The first Atomic Unit should estimate the effect of high versus low exposure-day
fiber density on next-night mean sleeping heart rate. Participant-day/night
sequences are the input rows; the output is one overlap-restricted population
average treatment effect (ATE), not a participant-level effect prediction.

This card specifies a registered observational-emulation Task
(`TargetShape.CAUSAL_EFFECT`, paired with `CausalAipwStrategy`). It reports one
aggregate ATE per Atomic Unit, stays off the leaderboard, and writes no
`predictions.parquet`.

Every real-data run derives its current claim classification from the persisted
balance gate and control diagnostics. Run-specific status, estimates, and cohort
counts live in
the internal evaluation configuration
and the generated deep-dive snapshot; this static Task Card does not duplicate
them. The companion contract plan records
the runtime surfaces and source build path.

## Target Trial

| Element | Proposed first contract |
|---|---|
| Eligibility | HPP adults with an unambiguous `D0 -> S0` baseline and all frozen adjustment fields observed before the first positive-energy `D1` dietary event; do not condition eligibility on later `D1` or `S1` observation |
| Trial occasion | One exposure diet-day and immediately following sleep night, nested within participant |
| Baseline | Complete prior diet day `D0`, prior valid sleep `S0` completed before the first positive-energy `D1` dietary event, and fixed information observed by then |
| Time zero | Immediately before the first positive-energy dietary event on exposure day `D1`, using the raw event timestamp |
| Treatment | `A=1`: `D1` fiber density at or above cutoff `c`; `A=0`: below `c` |
| Exposure unit | `fiber_density = 100 * fiber_g / total_energy_kcal` (g fiber per 100 kcal, matching the paper, the source tables, and the implementation) |
| Follow-up | First positive-energy `D1` event through completion of the immediately following valid WatchPAT sleep `S1` |
| Outcome | `S1` mean sleeping heart rate, beats/minute |
| Contrast | High minus low fiber-density day |
| Estimand | ATE in the prespecified retained common-support/trimmed (overlap) population. Implemented primary estimator: doubly-robust cross-fit AIPW with participant-clustered efficient-influence-function analytic SE; Hájek-IPW and the outcome-model estimate are reported as sensitivity. |
| Grouping unit | Participant for nuisance folds and uncertainty |
| Result grain | One aggregate estimate, CI, and diagnostic bundle per Atomic Unit |

`D0 -> S0 -> D1 -> S1` is a logical order, not an assumed calendar-date
equation. The causal artifact builder must retain source timestamps, local
dates, and WatchPAT night ordinals and reject ambiguous or out-of-order rows.
Target eligibility is assessed before time zero. Observed `D1` diet and `S1`
sleep define the later analysis set, not eligibility; persist their observation
indicators and missingness reasons, report attrition, and state the conditional
observation assumption required by a complete-case estimate. A prespecified
selection-weighted sensitivity is required when the source can support it.

The treatment is a composite dietary behavior, not an isolated fiber dose.
Different foods can place a day in the same arm, limiting the consistency and
actionability of the effect.

## Treatment Cutoff

The cutoff is Task identity, not a Strategy hyperparameter.

1. Prefer the paper's numeric cutoff with unit and cohort provenance.
2. If it cannot be recovered, use the median **baseline-day** fiber density on a
   versioned, outcome-blind threshold-development subset (a deterministic
   `train_fraction_for_cutoff` of the analysis participants). The subset overlaps
   the analysis participants but never sees the outcome — that outcome-blindness,
   not participant-disjointness, is what justifies using it to freeze the cutoff.
3. Freeze the numeric cutoff before outcome, overlap, balance, or control
   inspection; assign equality to the high arm.
4. Persist the cutoff, units, cohort fingerprint, split seed, and equality rule.

The manuscript says baseline-day medians define treatment, while the public
code uses the target-day exposure median. These are different estimands and
must be separate claim rows if both are retained.

## Required Data

Every implemented adjustment field precedes the first positive-energy `D1`
event. The **Implemented analogue adjustment set** used by the canonical result
is:

- age, sex, and BMI from the latest anthropometrics record observed strictly
  before each occasion's time zero;
- `D0` fiber density, total kcal, caffeine, and alcohol;
- `S0` total sleep time, efficiency, wake after sleep onset, REM percentage,
  and mean sleeping heart rate;
- whether `D1` is a weekend day.

**Paper/ideal covariates not implemented in this analogue** include the broader
`D0` nutrient, food-quality, and meal-timing panel; `S0` deep/light sleep,
latency, and number of wakes; day-level activity; smoking and medical history;
and daily mood/stress. They remain paper-fidelity gaps and are not part of the
executed adjustment set.

Forbidden propensity inputs include `S1` sleep fields, negative-control
outcomes, future diagnoses, participant identity, and target-day variables that
are components, co-treatments, or downstream of the composite diet treatment.

The analogue admits only variables observed before the first positive-energy
`D1` event. If the
paper/private manifest instead used `D1` activity, mood/stress, alcohol, or
caffeine fields, those fields belong only in a separately labelled literal-code
comparator with their timing exposed; they cannot silently enter the analogue's
adjustment set. This resolves the otherwise contradictory “same-day covariate”
and time-zero definitions.

## Estimation Protocol

The runnable row is a methodological analogue, not literal public-code
reproduction. As implemented (`phenobench/causal.py`):

1. enumerate pre-time-zero eligible occasions using only baseline data;
2. derive `D1` treatment and immediate-`S1` outcome observation separately and
   freeze the complete analysis set;
3. assign five deterministic participant-disjoint nuisance folds (frozen in the
   artifact and consumed by the Strategy, not re-derived);
4. fit one probability-calibrated gradient-boosted propensity model per outer
   fold on the other participants (CatBoost in the paper; the implementation uses
   `HistGradientBoosting` to stay dependency-light), plus a gradient-boosted
   T-learner outcome model;
5. emit one out-of-fold propensity and out-of-fold `mu0`/`mu1` per occasion;
6. apply the frozen symmetric propensity trim (overlap population);
7. **primary estimator: doubly-robust cross-fit AIPW** — the mean of
   `mu1 - mu0 + A(Y-mu1)/e - (1-A)(Y-mu0)/(1-e)` — with a participant-clustered
   efficient-influence-function analytic SE. Hájek-IPW and the outcome-only mean
   are reported as single-robust sensitivity estimates;
8. participant-cluster bootstrap (full refit) as an inference cross-check,
   keeping the treatment cutoff and trim frozen;
9. surface the estimate together with the missingness, overlap, effective sample
   size, weighted-ASMD balance-gate outcome, and control diagnostics — a
   balance-gate breach is reported as a residual-confounding caveat, not hidden.

The Hájek-IPW formulation retained below is the sensitivity/paper-fidelity
comparator; AIPW is the reported primary because it is doubly robust under the
modest overlap and heavy weight tails here.

Any clipped-weight result is a separately labelled regularized sensitivity; it
does not inherit the ordinary trimmed-overlap ATE label.

The literal public-code comparator is a separate `paper_code_reproduction`
row: 70% participant propensity training, predictions and Platt calibration on
all rows, row bootstrap, and fixed propensities. It is useful for provenance,
but its inference and leakage behavior must not be silently mixed with the
grouped analogue.

## Controls And Validity Gates

The implemented control package is deliberately weak and cannot validate the
causal claim:

- heart-rate signal-quality score is the only candidate null outcome, but the
  eligibility quality gate makes it range-restricted and low-power;
- prior-night sleeping HR is a pre-treatment placebo. A point estimate near the
  primary effect is a residual-confounding red flag, although its wide interval
  cannot prove bias;
- Body-position outcomes are exploratory, not null negative controls. Supine and
  left-side sleep have plausible treatment-to-position and position-to-HR paths,
  so they may be mediators and cannot provide confounding reassurance.

Required weighted absolute standardized mean differences (ASMD):

- `<=0.05` for age, sex, BMI, and every baseline-sleep field;
- `<=0.10` for the complete frozen adjustment set and the top 15 propensity
  contributors.

Also report treatment-arm counts, retained fraction, arm-specific effective
sample size, propensity support, and weight tails. Report every implemented
control or placebo regardless of direction; no parameter may be tuned to make a
diagnostic appear reassuring.

The caffeine-timing positive control has a different treatment and cohort. It
should be a linked validation Atomic Unit, not another fiber outcome.

## Metrics And Outputs

Primary reported quantity:

- `ate_bpm`, with the participant-clustered EIF analytic 95% CI. The
  participant-cluster bootstrap interval is a 120-full-refit inference
  cross-check and is reported separately; disagreement between the two intervals
  remains visible. The publication builder rejects any other refit count.

Secondary quantities:

- weighted arm means and percent contrast;
- overlap retained fraction and arm-specific effective sample size;
- raw and weighted ASMD table;
- propensity and weight distributions;
- control, placebo, and exploratory-position estimates with their validity role;
- cohort flow, assumption/fidelity table, and artifact hashes.

These are estimate/validity fields, not supervised-learning accuracy metrics.
There is no observed ATE truth in HPP, so effect magnitude, p-value, or proximity
to the paper's `-1.14 bpm` estimate cannot rank methods. A method leaderboard
requires a paired semi-synthetic Task with known ATE/CATE truth and metrics such
as bias, interval coverage, and policy value.

The real HPP row should use `eval_mode: system`,
`eval_category: counterfactual`, `metric_family: causal_effect`, and
`persistence.leaderboard: false`. It must not write ordinary
`predictions.parquet` or imply that observed `Y` is a causal label.

## Baselines And Ceilings

- Unadjusted high-minus-low outcome difference: descriptive diagnostic only.
- Public-code estimator: paper-implementation comparator, not a validity floor.
- Grouped cross-fitted estimator: recommended observational analogue.
- Optional representation-augmented propensity/outcome models: separate
  benchmark claim, always added to the same frozen core adjustment panel.
- Semi-synthetic known-truth data: the only proposed method-ranking surface.

## Source Artifact And Current Evidence

An earlier feasibility pass reused the day-grain `next_night_sleep` *predictive*
artifact and hit a wall: that artifact exposed only integer min/max logged-event
hours (engineered `first_meal_h` / `last_meal_h` features), not raw event times,
so exact `S0.end < time_zero(D1) < S1.start` ordering could not be established and
~75% of rows showed wrong-night lower bounds. That was an **artifact-export
limitation, not a source-data limitation** — and it is now resolved by building a
purpose-specific causal artifact directly from `ds.silverdb` source
(`build_diet_sleep_causal_artifact.py`), all `participant_uuid`-native:

- exact `time_zero` = first positive-energy `D1` event, `MIN(collection_timestamp)`
  from `diet_logging_detailed_all` (1-minute resolution, converted UTC→local);
- exact WatchPAT `study_start_time` / `study_end_time` from `sleep_all` enforce
  `S0.end < time_zero(D1) < S1.start` per row, the check the predictive artifact
  could not perform;
- duration-weighted mean sleeping HR from stage-wise NREM/REM means under the
  source-verified valid-night QC gate;
- daily fiber density (g/100 kcal) + baseline nutrient panel from
  `diet_logging_daily_all`; demographics from a strict backward as-of join to
  `anthropometrics_all` (`collection_timestamp < time_zero` per occasion).

The purpose-built analysis cohort is smaller than a loose predictive join because
it requires two consecutive valid WatchPAT nights (S0+S1), HR-quality ≥90, exact
ordering, and pre-index observed demographics. The committed aggregate source
summary records the minimum, median, and maximum anthropometrics-to-time-zero lag;
the generated deep dive reads the pre-trim
and analyzed cohort counts directly from the source-build summary and results.
The cross-fit AIPW estimate and its diagnostics, controls, and sensitivity analyses are reported in
the internal evaluation configuration;
the aggregate cohort-flow ledger is in
`source_build_summary.json`.

Remaining paper-fidelity gaps (documented, not blockers for a
`paper_inspired_analogue`): no `ds.silverdb` source for daily mood/stress or
day-level activity; the available precomputed supine/left-side outcomes are
exploratory and invalid as null controls; not the paper-frozen 4,793-night cohort.

## Why This Matters

This task would test whether PhenoBench can compare causal estimators and
representation-assisted nuisance models under a fixed observational question.
It supports an HPP target-trial estimate conditional on explicit assumptions
and diagnostics. It cannot prove an individual diet recommendation, identify
participant effects, remove unmeasured confounding, or validate an estimator
against causal truth.

## Clinically Meaningful Variants

The paper's full `exposure x eight-outcome` matrix should be a derived batch of
single-estimand Atomic Units. BH-FDR belongs in the within-exposure batch report,
not inside one multi-outcome Task. Continuous-dose and participant-level CATE
variants are scientifically plausible but are new estimands and need separate
cards and validation.

## Caveats

- Observational identification requires consistency, conditional
  exchangeability, positivity, no interference, and adequate measurement.
- Self-reported diet and median splits introduce exposure error and treatment
  heterogeneity.
- The modest number of repeated occasions provides limited within-person
  identification; retaining only switchers would change the estimand.
- Public production preprocessing and the exact covariate manifest are absent.
- Post-baseline diet/sleep observation can select the complete analysis set;
  causal interpretation needs an explicit missingness assumption and audit.
- The manuscript/public code disagree on exposure count, threshold source,
  calibration scope, and bootstrap interpretation.
- Current sleep-stage fields rely on proprietary WatchPAT algorithms.
- Results may not transport beyond the generally healthy Israeli HPP cohort.

## References

- Shkolnik M, Sapir G, Shilo S, et al. “Day-to-day dietary variation shapes
  overnight sleep physiology: a target-trial emulation in 4.8 thousand
  person-nights.” *medRxiv* (2026).
  [doi:10.64898/2026.02.17.26346471](https://doi.org/10.64898/2026.02.17.26346471)
- Shkolnik et al. public implementation, inspected at commit
  [`ef8b411e`](https://github.com/mashaashkolnik/causal_framework/tree/an internal digest).

## Open Questions

1. Approve the first row as a grouped cross-fitted observational analogue, with
   literal public-code reproduction kept separate?
2. Approve one exposure/outcome estimand per Atomic Unit and FDR at batch level?
3. Which name should the observational-emulation validation tier use?
4. What domain-equivalence margins should negative controls satisfy?
5. Which exact artifact/freeze supplies the paper's full covariates, cutoff,
   and 4,793-night cohort?
