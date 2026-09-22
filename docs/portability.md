# Cohort Portability

PhenoBench portability means binding another cohort to an existing Task Card
and executable evaluation contract. This guide does not add a new benchmark
contract. It records how cohort-specific data implement the same scientific
question.

## Preserve the question

The Task Card defines the invariant question semantics: the target construct,
prediction setting, allowed information, direction of prediction, and intended
time horizon. Its claim boundary must also remain invariant. A cross-sectional
association does not become forecasting, diagnosis, causation, or clinical
utility when evaluated in another cohort.

If a cohort cannot implement those semantics, define a distinct Task rather
than report its result in the existing Benchmark Track.

## Bind the cohort

Document every cohort-specific binding:

- **Target:** target field, unit, assay or derivation, and timepoint.
- **Population:** eligibility rules, exclusions, and quality control.
- **Predictors:** predictor mapping from the contract's allowed inputs to cohort
  fields, including units and transformations.
- **Visits:** visit mapping, temporal windows, and rules for selecting or
  aggregating repeated measurements.
- **Evaluation unit:** the scored entity, such as participant, visit, event, or
  sequence.
- **Independence:** participant grouping and split construction, including how
  repeated observations and related participants are kept from leaking across
  splits.
- **Evaluation:** comparator and metric implementations, missing-output policy,
  and any cohort-specific thresholds.

Bindings may change storage details, but not the Task's scientific meaning or
the executable prediction and scoring interfaces.

## Validation gates

Before publishing a transported result:

1. Confirm target units, direction, timepoint, and plausible ranges against
   cohort documentation.
2. Verify eligibility and quality-control counts at each filtering step.
3. Validate predictor and visit mappings on representative records.
4. Test evaluation-unit uniqueness, participant grouping, and split isolation.
5. Run fabricated contract examples through prediction and scoring.
6. Reproduce the declared comparator and metric on identical scored support.
7. Review missingness, exclusions, and subgroup support for material changes to
   the estimand.

Record provenance for the cohort release, source fields, extraction code,
mapping version, Task Card version, evaluation-contract version, split seed or
identifiers, and validation outputs. Do not publish participant data or private
infrastructure identifiers.

## Portability is not external validation

Passing these gates establishes **technical portability**: the cohort has been
mapped faithfully enough to execute the same Task. It does not establish
**empirical external validation**. Comparable performance, calibration, and
subgroup behavior must be measured in the transported cohort before making
generalization claims.
