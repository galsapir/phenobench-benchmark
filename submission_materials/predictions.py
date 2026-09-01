# ABOUTME: Validates a predictions.csv against a task bundle manifest and input identifiers.
# ABOUTME: Row order is irrelevant; duplicate, unknown, missing identifiers and non-finite values fail closed.
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any

MANIFEST_SCHEMA_VERSION = 1
GRAINS = ("participant", "event", "sequence")


class PredictionError(ValueError):
    """Raised when a prediction file violates the bundle contract."""


def load_manifest(bundle_dir: Path) -> dict[str, Any]:
    manifest = json.loads((Path(bundle_dir) / "manifest.json").read_text())
    if manifest.get("manifest_schema_version") != MANIFEST_SCHEMA_VERSION:
        raise PredictionError("manifest: unsupported manifest_schema_version")
    if manifest.get("grain") not in GRAINS:
        raise PredictionError("manifest: grain must be one of " + ", ".join(GRAINS))
    if not manifest.get("identifier_columns"):
        raise PredictionError("manifest: identifier_columns is required")
    if manifest["grain"] == "sequence" and not manifest.get("required_offsets_minutes"):
        raise PredictionError("manifest: sequence grain requires required_offsets_minutes")
    return manifest


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    text = Path(path).read_text()
    reader = csv.DictReader(text.splitlines())
    rows = list(reader)
    if reader.fieldnames is None:
        raise PredictionError(f"{path.name}: empty file")
    return list(reader.fieldnames), rows


def expected_keys(bundle_dir: Path, manifest: dict[str, Any]) -> set[tuple[str, ...]]:
    """Identifier tuples every valid prediction file must cover exactly once."""
    _, input_rows = _read_csv(Path(bundle_dir) / manifest["input_file"])
    unit_col = manifest["identifier_columns"][0]
    units = [r[unit_col] for r in input_rows]
    if manifest["grain"] == "sequence":
        offsets = [str(o) for o in manifest["required_offsets_minutes"]]
        return {(u, o) for u in units for o in offsets}
    return {(u,) for u in units}


def _parse_rows(manifest: dict[str, Any], path: Path) -> list[tuple[tuple[str, ...], float]]:
    id_cols = list(manifest["identifier_columns"])
    pred_col = manifest["prediction_column"]
    columns, rows = _read_csv(path)
    required = id_cols + [pred_col]
    if columns != required:
        raise PredictionError(f"{path.name}: columns must be exactly {required}, got {columns}")
    parsed = []
    for n, row in enumerate(rows, start=2):
        try:
            value = float(row[pred_col])
        except (TypeError, ValueError) as exc:
            raise PredictionError(f"{path.name} line {n}: prediction must be a finite number") from exc
        if not math.isfinite(value):
            raise PredictionError(f"{path.name} line {n}: prediction must be a finite number")
        parsed.append((tuple(row[c] for c in id_cols), value))
    return parsed


def validate_predictions(bundle_dir: Path, predictions_path: Path) -> list[tuple[tuple[str, ...], float]]:
    bundle_dir = Path(bundle_dir)
    manifest = load_manifest(bundle_dir)
    parsed = _parse_rows(manifest, Path(predictions_path))
    expected = expected_keys(bundle_dir, manifest)
    seen: set[tuple[str, ...]] = set()
    for key, _ in parsed:
        if key in seen:
            raise PredictionError(f"duplicate identifier {key}")
        seen.add(key)
    unknown = seen - expected
    if unknown:
        raise PredictionError(f"unknown identifier(s): {sorted(unknown)[:5]}")
    missing = expected - seen
    if missing:
        raise PredictionError(f"missing identifier(s): {len(missing)} of {len(expected)}, e.g. {sorted(missing)[:3]}")
    return parsed


def canonical_digest(bundle_dir: Path, predictions_path: Path) -> str:
    """Order-independent digest of (identifier, prediction) pairs."""
    parsed = sorted(validate_predictions(bundle_dir, predictions_path))
    payload = "\n".join(",".join(k) + "," + repr(v) for k, v in parsed).encode()
    return "sha256:" + hashlib.sha256(payload).hexdigest()
