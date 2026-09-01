# Loneliness Status Task Card

Status: draft

Task id: `loneliness_status`

Evidence status: grounded

Evidence reviewed: 2026-07-29

## Target

Three-class current loneliness response from the HPP psychological and social
health questionnaire.

Implementation facts:

- target field: `health_mental_current_lonely`
- target dataset: `psychological_and_social_health`
- default research stage: `00_00_visit`
- labels: `No`, `Yes`, `Do not know`
- excluded states: missing, `Prefer not to answer`
- primary metric: balanced accuracy

## Why This Matters

This task captures the Arun 2026 loneliness-classification result as a real
PhenoBench categorical benchmark instead of collapsing it to binary. It tests
whether questionnaire panels can predict a mental-health self-report target on
canonical HPP splits.

## Baselines And Ceilings

- **Floor**: demographic classifier baseline.
  `DemographicClassifierFloorStrategy` fits age, sex, and BMI.
- **Paper-inspired track**: `questionnaire_categorical_features` over
  sociodemographics, lifestyle/environment, and psychological/social-health
  fields, excluding the target field.

## Caveats

- Many questionnaire fields can be target-adjacent. Current configs exclude the
  exact target field; broader proxy-review policy remains human-reviewed.
- The paper's exact 108-variable panel and RFE protocol are not fully encoded.
- Feature selection is not yet train-fold-only RFE; this first track uses the
  routed questionnaire fields with one-hot categorical encoding.

## Metrics

Primary: balanced accuracy. Secondary: accuracy, macro F1, weighted F1, log
loss, split sizes.

## Benchmark-Track Evidence

OpenEvidence review and broader Paperclip search support one objective-sleep
track. Actigraphic sleep fragmentation and efficiency associate with loneliness
beyond demographics, with evidence of bidirectionality. HPP's own
questionnaire study also selected subjective sleep patterns, but those fields
are too target-adjacent for this cross-modal track. Exclude all questionnaire,
lifestyle, social, and psychological fields—not only the exact target.

## References

- Arun 2026 loneliness-classification paper artifacts in Research OS.
- Research OS run: `research_runs/phenobench-paper-task/arun_loneliness_2026_06_21/`.
- Benson et al. (2021), objective sleep and loneliness:
  <https://doi.org/10.1093/sleep/zsaa140>.

## Open Questions

- Should future configs add a reviewed proxy-exclusion list beyond the target
  field?
- Should RFE/MI ranking become a Strategy with train-fold-only feature
  selection?
