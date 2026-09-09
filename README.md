# PhenoBench

PhenoBench turns the Human Phenotype Project into a versioned benchmark for
asking what each measurement and representation can predict. This public release
provides:

- an aggregate catalog of 90 clinically grounded tasks, 3 framework diagnostics,
  and their valid Benchmark Tracks;
- static per-track leaderboards generated from the final Figure 1 evidence;
- all 960 aggregate rows behind the matched model-family comparison;
- aggregate evidence for the earlier meal-CGM evaluation reported in the paper;
- the 40-task PhenoBench-LLM proof-of-concept leaderboard;
- a sanitized PhenoBench-LLM reproducibility package with frozen prompts,
  schemas, synthetic examples, evaluation code, and cohort-level provenance;
- privacy-reviewed Task Cards;
- fabricated, schema-faithful input/output examples;
- a digest-pinned OCI prediction contract; and
- a manual model-submission path.

No participant data, private predictions, credentials, or private execution
identifiers are distributed here.

## Explore

Read the [PhenoBench paper on arXiv](https://arxiv.org/abs/2609.06080). Citation metadata
is available in [`CITATION.cff`](CITATION.cff).

Visit the [PhenoBench benchmark atlas](https://galsapir.github.io/phenobench-benchmark/),
or serve the repository locally:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000/site/generated/`. Machine-readable evidence
lives under `data/`; clinical context lives under `task-cards/`.

PhenoBench does not define one universal score. Results are ranked only within
a Benchmark Track that fixes the Task, cohort, split, metric, and allowed
information.

## Submit a model

Develop against the bundles under `synthetic/`, package the predictor using
`container/README.md`, and open a Model submission issue with a public OCI
image pinned by immutable digest. Evaluation is maintainer-operated and
capacity-limited. See `CONTRIBUTING.md`.

## Validate the public contracts

Python 3.11+ and [uv](https://docs.astral.sh/uv/) are required.

```bash
uv sync --frozen
uv run pytest -q
uv run scripts/validate_predictions.py synthetic/participant_scalar synthetic/participant_scalar/example_predictions.csv
```

The private release pipeline imports only allowlisted aggregate results,
regenerates this repository, and reruns privacy and contract checks whenever a
source result changes.

## Repository map

```text
data/                 allowlisted aggregate PB and PhenoBench-LLM evidence
pb-llm/               sanitized PhenoBench-LLM prompts, contracts and evaluation metadata
task-cards/           sanitized scientific context for public Tasks
site/generated/       static landing page and 93 per-task/diagnostic result pages
synthetic/            fabricated participant, event, and sequence examples
container/            OCI contract and offline reference predictor
schemas/              machine-readable result contract
paper/                manuscript-ready benchmark access text
scripts/              public schema and synthetic-bundle validators
tests/                executable prediction-contract tests
```

Code is Apache-2.0. Documentation, Task Cards, synthetic examples, and
aggregate results are CC BY 4.0. See `LICENSE` and `LICENSE-DOCS`.
