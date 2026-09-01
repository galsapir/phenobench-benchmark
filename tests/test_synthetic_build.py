# ABOUTME: Tests that the synthetic bundle generator is deterministic and matches committed files.
# ABOUTME: Also checks identifier formats stay fabricated-looking and physiologically bounded values.
import csv
import uuid
from pathlib import Path

from submission_materials.synthetic import build_bundles

REPO = Path(__file__).resolve().parents[1]


def test_generator_matches_committed_files():
    outputs = build_bundles()
    for rel, data in outputs.items():
        assert (REPO / "synthetic" / rel).read_bytes() == data, rel


def test_generator_is_deterministic():
    assert build_bundles() == build_bundles()


def test_participant_ids_are_uuids():
    rows = list(csv.DictReader((REPO / "synthetic/participant_scalar/input.csv").read_text().splitlines()))
    for r in rows:
        assert str(uuid.UUID(r["participant_id"])) == r["participant_id"]


def test_bundles_are_tiny():
    for name in ["participant_scalar", "event_scalar", "sequence"]:
        n = len((REPO / "synthetic" / name / "input.csv").read_text().splitlines()) - 1
        assert 0 < n <= 64, name
