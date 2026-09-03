# PhenoBench-LLM public package

This directory documents the validation-set proof of concept in which external
language models received structured evidence packets and estimated withheld
phenotypes. It contains the frozen prompt contracts, public schemas, one wholly
fabricated example, cohort-level provenance, evaluation settings, and the
dependency-free parsing and primary-metric functions.

The aggregate results are in [`../data/pb-llm/`](../data/pb-llm/):

- `task_rows.csv`: one task/model result row, including matched baselines;
- `category_summary.csv`: summaries within each task category;
- `win_rates.csv`: all available task/model comparisons; and
- `win_rates_common.csv`: the 11 tasks evaluated by all 14 models.

The last table is the headline comparison. PhenoBench does not combine the four
task categories or heterogeneous metrics into a universal benchmark score.

## Prompt contract

`prompts/system.txt` and `prompts/participant-estimate.txt` reproduce the scalar
prompt with placeholders for task-specific content. The task question was one
of the following:

- Regression: `Estimate this participant's {{TARGET_LABEL}}, measured at the
  same study visit, in {{UNIT_PHRASE}}.`
- Classification: `Estimate the probability (0 to 1) that this participant
  {{POSITIVE_LABEL}}, as determined at the same study visit
  ({{TARGET_LABEL}}).`
- Longitudinal: `Estimate this participant's {{TARGET_LABEL}}, in
  {{UNIT_PHRASE}}. The evidence below was measured at the baseline visit,
  including the baseline value of the same measurement.`

`{{NMR_UNITS}}` was `mmol/L (percent for *_pct)`. JSON keys and task-specific
response fields were deterministic. The Task Card arm prepended
`prompts/task-card-prefix.txt`; its card was stripped of implementation facts,
benchmark results, target ranges, tables, and numeric cohort facts. The ranking
prompts and schema document the four-person ordering tasks.

## Evidence and response

The full packet contained age, sex, BMI, 19 CGM iglu summaries, and 33
Nightingale NMR measurements. HbA1c estimators GMI and eA1c were never shown.
Arms exposed demographics alone, demographics plus either modality, or the
full packet. Controls included closed-book prediction and shuffled packets.

The schemas describe the public structure. In scalar runs, `estimate` in the
example response schema was replaced by the task-specific response-field name;
classification responses were constrained to `[0, 1]`. Provider-enforced
structured output was requested where supported. Responses were accepted only
when that field parsed to a finite JSON number.

## Evaluation

All results are exploratory validation-set results. Scalar tasks used at most
150 evaluation units sampled from the task's complete-evidence validation
support. Ordering tasks used 120 seeded groups of four. The exact aggregate
coverage is in `metadata/model-task-coverage.csv`; absence means a model/task
pair was not evaluated.

`configs/evaluation.json` freezes arms, metrics, baselines, models, and seeds.
`code/evaluation.py` provides strict response parsing plus R², AUROC, and
pairwise accuracy. Cohort-level counts and support hashes are in
`metadata/cohort-manifests.json`. These hashes support alignment checks; they
cannot recover or access cohort rows.

The headline win rate compares every pair of models on each common task, gives
ties half credit, then divides each model's wins by its head-to-heads. Its 95%
interval is a 2,000-replicate task-level percentile bootstrap with seed
20260826.

## What remains private

Participant-level evidence and targets, populated prompts, raw model responses,
provider request/response logs, prediction artifacts, and execution paths are
not distributed. They cannot be reconstructed from this package. Reproducing
provider calls also requires independent credentials and access to the named
model endpoints.

See [`PRIVACY_REVIEW.md`](PRIVACY_REVIEW.md) for the release checks and explicit
exclusions.

## Maintainer refresh

After the private pipeline publishes updated allowlisted aggregate tables,
regenerate the public taxonomy, coverage, and cohort metadata with:

```bash
uv run scripts/build_pb_llm_public_metadata.py \
  --cohort-dir "$PB_LLM_SOURCE/data/cohorts" \
  --ranking-dir "$PB_LLM_SOURCE/data/ranking" \
  --task-specs-root "$PB_LLM_SOURCE/src" \
  --source-commit "$PB_LLM_SOURCE_COMMIT"
```

Then run the full test suite and privacy scan before updating the repository
manifest. The generator admits only named fields; adding a source field requires
an explicit code and test change.
