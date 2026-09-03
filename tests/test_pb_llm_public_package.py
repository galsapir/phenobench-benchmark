# ABOUTME: Validates the sanitized PhenoBench-LLM public package and its evaluation helpers.
# ABOUTME: Guards reproducibility artifacts against participant data, private paths, and schema drift.
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
PACKAGE = ROOT / "pb-llm"


def _load_evaluation_module():
    path = PACKAGE / "code" / "evaluation.py"
    spec = importlib.util.spec_from_file_location("pb_llm_public_evaluation", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_manifest_module():
    path = ROOT / "scripts" / "build_manifest.py"
    spec = importlib.util.spec_from_file_location("public_manifest", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_public_package_contains_documented_release_artifacts() -> None:
    required = {
        "README.md",
        "prompts/system.txt",
        "prompts/participant-estimate.txt",
        "prompts/closed-book.txt",
        "schemas/evidence-packet.schema.json",
        "schemas/response.schema.json",
        "examples/synthetic-input.json",
        "examples/synthetic-output.json",
        "metadata/task-taxonomy.csv",
        "metadata/model-task-coverage.csv",
        "metadata/cohort-manifests.json",
        "configs/evaluation.json",
        "code/evaluation.py",
        "PRIVACY_REVIEW.md",
    }
    assert required <= {
        str(path.relative_to(PACKAGE)) for path in PACKAGE.rglob("*") if path.is_file()
    }


def test_templates_are_placeholders_and_synthetic_example_matches_schemas() -> None:
    participant_template = (
        PACKAGE / "prompts" / "participant-estimate.txt"
    ).read_text()
    assert "{{TASK_QUESTION}}" in participant_template
    assert "{{EVIDENCE_PACKET_JSON}}" in participant_template
    assert "{{RESPONSE_FIELD}}" in participant_template

    evidence = json.loads((PACKAGE / "examples" / "synthetic-input.json").read_text())
    response = json.loads((PACKAGE / "examples" / "synthetic-output.json").read_text())
    evidence_schema = json.loads(
        (PACKAGE / "schemas" / "evidence-packet.schema.json").read_text()
    )
    response_schema = json.loads(
        (PACKAGE / "schemas" / "response.schema.json").read_text()
    )
    assert set(evidence) <= set(evidence_schema["properties"])
    cgm_fields = evidence_schema["properties"]["cgm"]["propertyNames"]["enum"]
    nmr_fields = evidence_schema["properties"]["nightingale"]["propertyNames"]["enum"]
    assert len(cgm_fields) == 19 and not {"iglu_gmi", "iglu_ea1c"} & set(cgm_fields)
    assert len(nmr_fields) == 33
    assert set(response) == set(response_schema["required"])
    assert evidence["demographics"]["sex"] in {"female", "male"}
    assert "Synthetic example" in response["reasoning"]


def test_evaluation_helpers_parse_and_score_without_private_data() -> None:
    evaluation = _load_evaluation_module()
    assert (
        evaluation.parse_prediction(
            '{"estimate": 5.6, "reasoning": "synthetic"}', "estimate"
        )
        == 5.6
    )
    assert (
        evaluation.parse_prediction(
            '{"estimate": true, "reasoning": "synthetic"}', "estimate"
        )
        is None
    )
    assert evaluation.parse_prediction("not json", "estimate") is None
    assert evaluation.r2([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]) == pytest.approx(1.0)
    assert evaluation.roc_auc([0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8]) == pytest.approx(
        0.75
    )
    assert evaluation.pairwise_accuracy([0, 1, 1], [0.2, 0.8, 0.5]) == pytest.approx(
        5 / 6
    )
    assert evaluation.parse_ranking(
        '{"ranking_high_to_low": ["A", "C", "B"], "reasoning": "synthetic"}',
        {"A", "B", "C"},
    ) == ["A", "C", "B"]
    assert (
        evaluation.parse_ranking('{"ranking_high_to_low": ["A", "A"]}', {"A", "B"})
        is None
    )


def test_head_to_head_win_rates_use_only_matched_tasks() -> None:
    evaluation = _load_evaluation_module()
    rows = [
        {"task": "a", "model_key": "m1", "llm_full": 0.8},
        {"task": "a", "model_key": "m2", "llm_full": 0.7},
        {"task": "b", "model_key": "m1", "llm_full": 0.5},
        {"task": "b", "model_key": "m2", "llm_full": 0.5},
        {"task": "c", "model_key": "m1", "llm_full": 0.9},
    ]
    assert evaluation.head_to_head_win_rates(rows) == {
        "m1": {"wins": 1.5, "games": 2, "win_rate": 0.75},
        "m2": {"wins": 0.5, "games": 2, "win_rate": 0.25},
    }


def test_head_to_head_code_reproduces_published_point_estimates() -> None:
    evaluation = _load_evaluation_module()
    with (ROOT / "data" / "pb-llm" / "task_rows.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    observed = evaluation.head_to_head_win_rates(rows)
    with (ROOT / "data" / "pb-llm" / "win_rates.csv").open(newline="") as handle:
        published = list(csv.DictReader(handle))
    for row in published:
        assert observed[row["model_key"]]["win_rate"] == pytest.approx(
            float(row["win_rate"])
        )


def test_taxonomy_and_coverage_match_public_aggregate_results() -> None:
    with (ROOT / "data" / "pb-llm" / "task_rows.csv").open(newline="") as handle:
        result_rows = list(csv.DictReader(handle))
    result_pairs = {(row["task"], row["model_key"]) for row in result_rows}

    with (PACKAGE / "metadata" / "task-taxonomy.csv").open(newline="") as handle:
        taxonomy = list(csv.DictReader(handle))
    assert len(taxonomy) == 40
    assert set(taxonomy[0]) == {
        "task",
        "category",
        "primary_metric",
        "n_models_evaluated",
        "target_label",
        "unit_phrase",
        "response_field",
        "positive_label",
        "parent_task",
    }
    assert {row["task"] for row in taxonomy} == {row["task"] for row in result_rows}

    with (PACKAGE / "metadata" / "model-task-coverage.csv").open(newline="") as handle:
        coverage = list(csv.DictReader(handle))
    assert {(row["task"], row["model_key"]) for row in coverage} == result_pairs


def test_evaluation_config_matches_public_models_and_provenance() -> None:
    config = json.loads((PACKAGE / "configs" / "evaluation.json").read_text())
    cohorts = json.loads((PACKAGE / "metadata" / "cohort-manifests.json").read_text())[
        "cohorts"
    ]
    with (PACKAGE / "metadata" / "model-task-coverage.csv").open(newline="") as handle:
        coverage = list(csv.DictReader(handle))
    with (ROOT / "data" / "pb-llm" / "win_rates.csv").open(newline="") as handle:
        leaderboard = list(csv.DictReader(handle))

    configured_models = {row["model_key"] for row in config["models"]}
    assert configured_models == {row["model_key"] for row in coverage}
    assert configured_models == {row["model_key"] for row in leaderboard}
    assert len(configured_models) == 14
    assert {row["source_commit"] for row in cohorts} == {config["source_commit"]}
    ranking_cohorts = [row for row in cohorts if row["task"].endswith("_group_rank")]
    assert len(ranking_cohorts) == 6
    assert all(row["sampling_method"] == "120 seeded groups of 4" for row in ranking_cohorts)
    assert all(row["sampling_seed"] == 20260826 for row in ranking_cohorts)


def test_cohort_manifests_are_allowlisted_and_cover_every_public_task() -> None:
    payload = json.loads((PACKAGE / "metadata" / "cohort-manifests.json").read_text())
    allowed = {
        "task",
        "cohort_source_task",
        "eval_split",
        "split_source",
        "scored_cohort_n",
        "scored_support_sha256",
        "eligible_cohort_n",
        "complete_evidence_n",
        "sampling_method",
        "sampling_seed",
        "source_commit",
    }
    assert payload["schema_version"] == 1
    assert len(payload["cohorts"]) == 40
    assert all(set(row) == allowed for row in payload["cohorts"])
    assert all(row["eval_split"] == "validation" for row in payload["cohorts"])
    assert all(
        re.fullmatch(r"[0-9a-f]{64}", row["scored_support_sha256"])
        for row in payload["cohorts"]
    )


def test_generated_metadata_uses_repository_line_endings() -> None:
    for path in (PACKAGE / "metadata").glob("*.csv"):
        assert b"\r\n" not in path.read_bytes(), path


def test_manifest_builder_ignores_untracked_files(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    tracked = tmp_path / "tracked.txt"
    untracked = tmp_path / "untracked.txt"
    tracked.write_text("public\n")
    untracked.write_text("local only\n")
    subprocess.run(["git", "add", tracked.name], cwd=tmp_path, check=True)

    manifest = _load_manifest_module()

    assert manifest.public_files(tmp_path) == [tracked]


def test_release_has_no_forbidden_file_types_or_private_path_markers() -> None:
    forbidden_suffixes = {".parquet", ".jsonl"}
    forbidden_markers = (
        "/home/",
        "/Users/",
        "participant_id",
        "evaluation_unit_id",
        "OPENROUTER_API_KEY",
        "AWS_SECRET_ACCESS_KEY",
        "postgres://",
        "s3://",
    )
    forbidden_patterns = (
        re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE),
        re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.IGNORECASE),
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    )
    files = [
        path for path in PACKAGE.rglob("*") if path.is_file() and path.suffix != ".pyc"
    ]
    assert not {path.suffix for path in files} & forbidden_suffixes
    for path in files:
        text = path.read_text()
        assert not any(marker in text for marker in forbidden_markers), path
        assert not any(pattern.search(text) for pattern in forbidden_patterns), path


def test_release_files_are_digest_pinned_in_repository_manifest() -> None:
    entries = {}
    for line in (ROOT / "MANIFEST.sha256").read_text().splitlines():
        digest, path = line.split("  ", maxsplit=1)
        entries[path] = digest
    for path in PACKAGE.rglob("*"):
        if not path.is_file() or path.suffix == ".pyc":
            continue
        relative = str(path.relative_to(ROOT))
        assert relative in entries
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entries[relative]
