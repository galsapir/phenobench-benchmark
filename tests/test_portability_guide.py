# ABOUTME: Verifies that the public cohort-portability guide documents the required bindings.
# ABOUTME: Keeps the guide discoverable without defining a second benchmark contract.
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_portability_guide_is_discoverable_and_complete() -> None:
    readme = (ROOT / "README.md").read_text()
    guide = (ROOT / "docs" / "portability.md").read_text().lower()

    assert "[cohort portability](docs/portability.md)" in readme
    for required_text in (
        "task card",
        "executable evaluation contract",
        "claim boundary",
        "target field",
        "unit",
        "timepoint",
        "eligibility",
        "quality control",
        "predictor mapping",
        "visit mapping",
        "evaluation unit",
        "participant grouping",
        "split",
        "comparator",
        "metric",
        "validation gates",
        "provenance",
        "external validation",
    ):
        assert required_text in guide

    assert "second contract" not in guide
