# ABOUTME: Runs the reference predictor script directly (no Docker) on each synthetic bundle.
# ABOUTME: Its output must pass the prediction validator; Docker execution is covered by container/test.sh.
import os
import subprocess
import sys
from pathlib import Path

import pytest

from submission_materials.predictions import validate_predictions

REPO = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("bundle", ["participant_scalar", "event_scalar", "sequence"])
def test_reference_predictor_output_validates(bundle, tmp_path):
    env = {**os.environ, "PB_INPUT": str(REPO / "synthetic" / bundle), "PB_OUTPUT": str(tmp_path)}
    subprocess.run([sys.executable, str(REPO / "container/predict.py")], env=env, check=True, capture_output=True)
    validate_predictions(REPO / "synthetic" / bundle, tmp_path / "predictions.csv")
