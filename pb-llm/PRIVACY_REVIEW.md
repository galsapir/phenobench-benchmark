# Public-release privacy review

Review date: 2026-09-03. Scope: every file below `pb-llm/` plus the generated
metadata inputs and the already-public aggregate tables under `data/pb-llm/`.

## Allowlist

Only these source classes were admitted:

- frozen prompt text with placeholders;
- structural JSON schemas;
- hand-authored fabricated input and output;
- task/category/metric/model coverage already present in aggregate results;
- aggregate leaderboard tables already published by this repository;
- cohort counts, split labels, deterministic sampling facts, support SHA-256
  digests, and source commit; and
- parsing and metric functions that operate on caller-supplied values.

Cohort manifests were generated through an explicit field allowlist. Target
fields, target summaries, data-loader settings, source filenames, and execution
locations from the source manifests were dropped.

## Exclusions

The package contains no cohort rows, direct identifiers, pseudonymous row keys,
populated prompts, raw responses, reasoning traces, prediction rows, provider
logs, credentials, private URLs, private filesystem locations, Parquet files,
or JSON Lines stores. Uncertain artifacts were excluded rather than sanitized.

## Checks performed

The following checks were run over the complete candidate package:

1. Enumerated every file and rejected `.parquet`, `.jsonl`, database, archive,
   credential, key, and environment-file extensions.
2. Searched case-insensitively for identifier-field names, email addresses,
   UUIDs, home-directory paths, cloud credentials, API/token/key assignments,
   GitHub tokens, OpenRouter secrets, provider request IDs, internal hostnames,
   and private URI schemes.
3. Compared `metadata/task-taxonomy.csv` and
   `metadata/model-task-coverage.csv` with the published aggregate task rows.
4. Asserted that every cohort record has exactly the documented allowlisted
   fields and that all 40 public tasks are covered.
5. Parsed every JSON artifact and ran the full public test suite.

No forbidden file type, credential pattern, internal path, direct identifier,
participant-level record, or unexpected cohort-manifest field was found. The
support digests are one-way SHA-256 hashes of complete sets, not row-level
identifiers.
