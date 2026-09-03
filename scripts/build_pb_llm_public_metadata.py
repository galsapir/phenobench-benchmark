# ABOUTME: Builds allowlisted PhenoBench-LLM taxonomy, coverage, and cohort metadata for public release.
# ABOUTME: Reads aggregate results plus private manifests but writes no identifiers, target values, or paths.
from __future__ import annotations

import argparse
import csv
import importlib
import json
import sys
from pathlib import Path
from typing import Any


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def cohort_row(
    task: str, cohort_dir: Path, ranking_dir: Path, source_commit: str
) -> dict[str, object]:
    source_task = task.removesuffix("_group_rank")
    manifest = json.loads(
        (cohort_dir / f"{source_task}.cohort_manifest.json").read_text()
    )
    if task.endswith("_group_rank"):
        rank = json.loads(
            (ranking_dir / f"{source_task}.rank_manifest.json").read_text()
        )
        scored_n = rank["cohort_n"]
        support_sha256 = rank["cohort_ids_file_sha256"]
        sampling_method = f"{rank['n_groups']} seeded groups of {rank['group_size']}"
        sampling_seed = rank["groups_seed"]
    else:
        scored_n = manifest["scored_cohort_n"]
        support_sha256 = manifest["scored_cohort_ids_sha256"]
        sampling_method = manifest["sampling"]["method"]
        sampling_seed = manifest["sampling"]["seed"]
    return {
        "task": task,
        "cohort_source_task": source_task,
        "eval_split": manifest["eval_split"],
        "split_source": manifest["split_source"],
        "scored_cohort_n": scored_n,
        "scored_support_sha256": support_sha256,
        "eligible_cohort_n": manifest["task_eligible_n"],
        "complete_evidence_n": manifest["validation_complete_evidence_n"],
        "sampling_method": sampling_method,
        "sampling_seed": sampling_seed,
        "source_commit": source_commit,
    }


def load_task_specs(source_root: Path) -> dict[str, Any]:
    sys.path.insert(0, str(source_root))
    try:
        return dict(importlib.import_module("pb_llm_experiment.evidence").TASKS)
    finally:
        sys.path.pop(0)


def build(
    aggregate: Path,
    cohort_dir: Path,
    ranking_dir: Path,
    task_specs_root: Path,
    output: Path,
    source_commit: str,
) -> None:
    rows = read_rows(aggregate)
    specs = load_task_specs(task_specs_root)
    tasks: dict[str, tuple[str, str]] = {}
    for row in rows:
        tasks[row["task"]] = (row["category"], row["metric"])

    taxonomy = []
    for task, (category, metric) in sorted(tasks.items()):
        source_task = task.removesuffix("_group_rank")
        spec = specs[source_task]
        taxonomy.append(
            {
                "task": task,
                "category": category,
                "primary_metric": metric,
                "n_models_evaluated": sum(row["task"] == task for row in rows),
                "target_label": spec.target_label,
                "unit_phrase": spec.unit_phrase,
                "response_field": (
                    "ranking_high_to_low"
                    if category == "ordering"
                    else spec.response_field
                ),
                "positive_label": spec.positive_label,
                "parent_task": spec.parent_task or "",
            }
        )
    write_csv(
        output / "task-taxonomy.csv",
        [
            "task",
            "category",
            "primary_metric",
            "n_models_evaluated",
            "target_label",
            "unit_phrase",
            "response_field",
            "positive_label",
            "parent_task",
        ],
        taxonomy,
    )

    coverage = [
        {
            "task": row["task"],
            "category": row["category"],
            "primary_metric": row["metric"],
            "model_key": row["model_key"],
        }
        for row in sorted(rows, key=lambda item: (item["task"], item["model_key"]))
    ]
    write_csv(
        output / "model-task-coverage.csv",
        ["task", "category", "primary_metric", "model_key"],
        coverage,
    )

    cohorts = [
        cohort_row(task, cohort_dir, ranking_dir, source_commit)
        for task in sorted(tasks)
    ]
    (output / "cohort-manifests.json").write_text(
        json.dumps({"schema_version": 1, "cohorts": cohorts}, indent=2) + "\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build sanitized PhenoBench-LLM metadata."
    )
    parser.add_argument(
        "--aggregate", type=Path, default=Path("data/pb-llm/task_rows.csv")
    )
    parser.add_argument("--cohort-dir", type=Path, required=True)
    parser.add_argument("--ranking-dir", type=Path, required=True)
    parser.add_argument("--task-specs-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("pb-llm/metadata"))
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    build(
        args.aggregate,
        args.cohort_dir,
        args.ranking_dir,
        args.task_specs_root,
        args.output,
        args.source_commit,
    )


if __name__ == "__main__":
    main()
