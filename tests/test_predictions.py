# ABOUTME: Tests the prediction validator against the three synthetic task bundles.
# ABOUTME: Proves row order is irrelevant and identifier alignment (no dup/unknown/missing) is required.
import csv
import io
import random
from pathlib import Path

import pytest

from submission_materials.predictions import PredictionError, canonical_digest, load_manifest, validate_predictions

REPO = Path(__file__).resolve().parents[1]
BUNDLES = ["participant_scalar", "event_scalar", "sequence"]


def rows_of(path: Path) -> list[dict]:
    return list(csv.DictReader(path.read_text().splitlines()))


def write_rows(path: Path, rows: list[dict], columns: list[str]) -> Path:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=columns, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    path.write_text(buf.getvalue())
    return path


@pytest.fixture(params=BUNDLES)
def bundle(request):
    return REPO / "synthetic" / request.param


@pytest.fixture
def example(bundle):
    rows = rows_of(bundle / "example_predictions.csv")
    return rows, list(rows[0].keys())


def test_example_predictions_validate(bundle):
    validate_predictions(bundle, bundle / "example_predictions.csv")


def test_manifest_declares_identifier_columns(bundle):
    m = load_manifest(bundle)
    assert m["identifier_columns"]
    assert m["manifest_schema_version"] == 1
    assert m["grain"] in {"participant", "event", "sequence"}


def test_row_order_is_irrelevant(bundle, example, tmp_path):
    rows, cols = example
    shuffled = rows[:]
    random.Random(7).shuffle(shuffled)
    assert shuffled != rows
    p = write_rows(tmp_path / "shuffled.csv", shuffled, cols)
    validate_predictions(bundle, p)
    assert canonical_digest(bundle, p) == canonical_digest(bundle, bundle / "example_predictions.csv")


def test_duplicate_identifier_fails(bundle, example, tmp_path):
    rows, cols = example
    p = write_rows(tmp_path / "dup.csv", rows + [rows[0]], cols)
    with pytest.raises(PredictionError, match="duplicate"):
        validate_predictions(bundle, p)


def test_unknown_identifier_fails(bundle, example, tmp_path):
    rows, cols = example
    bad = dict(rows[0])
    id_col = load_manifest(bundle)["identifier_columns"][0]
    bad[id_col] = "not-a-real-id"
    p = write_rows(tmp_path / "unknown.csv", rows + [bad], cols)
    with pytest.raises(PredictionError, match="unknown"):
        validate_predictions(bundle, p)


def test_missing_identifier_fails(bundle, example, tmp_path):
    rows, cols = example
    p = write_rows(tmp_path / "missing.csv", rows[1:], cols)
    with pytest.raises(PredictionError, match="missing"):
        validate_predictions(bundle, p)


def test_non_numeric_prediction_fails(bundle, example, tmp_path):
    rows, cols = example
    rows = [dict(r) for r in rows]
    rows[0]["prediction"] = "abc"
    p = write_rows(tmp_path / "nonnum.csv", rows, cols)
    with pytest.raises(PredictionError, match="finite"):
        validate_predictions(bundle, p)


def test_nan_prediction_fails(bundle, example, tmp_path):
    rows, cols = example
    rows = [dict(r) for r in rows]
    rows[0]["prediction"] = "nan"
    p = write_rows(tmp_path / "nan.csv", rows, cols)
    with pytest.raises(PredictionError, match="finite"):
        validate_predictions(bundle, p)


def test_wrong_columns_fail(bundle, example, tmp_path):
    rows, cols = example
    renamed = [{("id" if k == cols[0] else k): v for k, v in r.items()} for r in rows]
    p = write_rows(tmp_path / "cols.csv", renamed, ["id"] + cols[1:])
    with pytest.raises(PredictionError, match="column"):
        validate_predictions(bundle, p)


def test_sequence_requires_every_offset(tmp_path):
    bundle = REPO / "synthetic" / "sequence"
    rows = rows_of(bundle / "example_predictions.csv")
    cols = list(rows[0].keys())
    kept = [r for r in rows if not (r["evaluation_unit_id"] == rows[0]["evaluation_unit_id"] and r["offset_minutes"] == rows[0]["offset_minutes"])]
    p = write_rows(tmp_path / "gap.csv", kept, cols)
    with pytest.raises(PredictionError, match="missing"):
        validate_predictions(bundle, p)


def test_sequence_rejects_off_grid_offset(tmp_path):
    bundle = REPO / "synthetic" / "sequence"
    rows = [dict(r) for r in rows_of(bundle / "example_predictions.csv")]
    cols = list(rows[0].keys())
    rows[0]["offset_minutes"] = "17"
    p = write_rows(tmp_path / "offgrid.csv", rows, cols)
    with pytest.raises(PredictionError, match="unknown"):
        validate_predictions(bundle, p)


def test_input_rows_have_no_target_columns(bundle):
    header = (bundle / "input.csv").read_text().splitlines()[0].lower()
    assert "target" not in header and "label" not in header
