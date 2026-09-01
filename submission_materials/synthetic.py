# ABOUTME: Deterministically generates the three entirely fabricated synthetic task bundles.
# ABOUTME: Values come from a seeded PRNG and hand-written ranges, never from any participant data.
from __future__ import annotations

import csv
import io
import json
import random
import uuid
from typing import Any

SEED = 20260825
SEQUENCE_OFFSETS = [15, 30, 45, 60, 75, 90, 105, 120]
PRIOR_CGM_OFFSETS = [-60, -45, -30, -15, 0]


def _csv(columns: list[str], rows: list[dict[str, Any]]) -> bytes:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=columns, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue().encode()


def _json(obj: Any) -> bytes:
    return (json.dumps(obj, indent=2) + "\n").encode()


def _fake_uuid(rng: random.Random) -> str:
    return str(uuid.UUID(int=rng.getrandbits(128), version=4))


def _manifest(task_id: str, grain: str, id_cols: list[str], target: str, **extra: Any) -> dict[str, Any]:
    return {
        "manifest_schema_version": 1,
        "task_id": task_id,
        "grain": grain,
        "identifier_columns": id_cols,
        "input_file": "input.csv",
        "prediction_file_name": "predictions.csv",
        "prediction_column": "prediction",
        "target_description": target,
        "data_origin": "synthetic; every value fabricated from a seeded generator",
        **extra,
    }


def _output_schema(id_cols: list[dict[str, str]], target_unit: str) -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "predictions.csv row",
        "description": "CSV with exactly these columns in this order; one row per identifier tuple from input.csv.",
        "type": "object",
        "additionalProperties": False,
        "required": [c["name"] for c in id_cols] + ["prediction"],
        "properties": {**{c["name"]: {"type": "string", "description": c["description"]} for c in id_cols},
                       "prediction": {"type": "number", "description": f"finite value in {target_unit}"}},
    }


def participant_scalar(rng: random.Random) -> dict[str, bytes]:
    rows, preds = [], []
    for _ in range(24):
        pid = _fake_uuid(rng)
        age = rng.randint(40, 70)
        sex = rng.choice(["female", "male"])
        bmi = round(rng.uniform(19.0, 34.0), 1)
        rows.append({"participant_id": pid, "age_years": age, "sex": sex, "bmi": bmi})
        preds.append({"participant_id": pid, "prediction": round(5.0 + 0.01 * (age - 40) + 0.02 * (bmi - 25), 2)})
    manifest = _manifest("participant_scalar_hba1c_like", "participant", ["participant_id"],
                         "HbA1c-like scalar in percent, one per participant", example_constant_prediction=5.4)
    schema = _output_schema([{"name": "participant_id", "description": "canonical UUID from input.csv"}], "percent")
    return {"manifest.json": _json(manifest), "input.csv": _csv(list(rows[0]), rows),
            "example_predictions.csv": _csv(["participant_id", "prediction"], preds), "output_schema.json": _json(schema)}


def event_scalar(rng: random.Random) -> dict[str, bytes]:
    rows, preds = [], []
    participants = [_fake_uuid(rng) for _ in range(6)]
    for pid in participants:
        for night in range(rng.randint(3, 6)):
            diet_date = f"2031-03-{10 + night:02d}"
            sleep_date = f"2031-03-{11 + night:02d}"
            eid = f"{pid}:diet={diet_date}:sleep={sleep_date}:row={night}"
            steps = rng.randint(2000, 14000)
            kcal = rng.randint(1400, 3200)
            late = round(rng.uniform(0, 600), 0)
            prior_hr = round(rng.uniform(48, 72), 1)
            rows.append({"evaluation_unit_id": eid, "participant_id": pid, "diet_local_date": diet_date,
                         "sleep_night_date": sleep_date, "daily_steps": steps, "daily_energy_kcal": kcal,
                         "late_eating_kcal": late, "prior_night_mean_sleeping_hr_bpm": prior_hr})
            preds.append({"evaluation_unit_id": eid, "prediction": round(prior_hr + 0.002 * late - 0.0001 * steps, 2)})
    manifest = _manifest("event_scalar_next_night_sleep_like", "event", ["evaluation_unit_id"],
                         "next-night mean sleeping heart rate-like scalar in bpm, one per participant-night",
                         example_constant_prediction=60.0)
    schema = _output_schema([{"name": "evaluation_unit_id", "description": "opaque event key from input.csv"}], "bpm")
    return {"manifest.json": _json(manifest), "input.csv": _csv(list(rows[0]), rows),
            "example_predictions.csv": _csv(["evaluation_unit_id", "prediction"], preds), "output_schema.json": _json(schema)}


def sequence(rng: random.Random) -> dict[str, bytes]:
    rows, preds = [], []
    participants = [_fake_uuid(rng) for _ in range(4)]
    for pid in participants:
        for meal in range(3):
            eid = f"{pid}:meal={meal}"
            carbs = rng.randint(10, 110)
            base = rng.uniform(80, 120)
            prior = {f"glucose_mg_dl_t{o:+d}".replace("+", "p").replace("-", "m"): round(base + rng.uniform(-6, 6), 1) for o in PRIOR_CGM_OFFSETS}
            rows.append({"evaluation_unit_id": eid, "participant_id": pid, "meal_local_time": f"2031-04-0{meal + 1}T08:30:00",
                         "carbohydrates_g": carbs, "protein_g": rng.randint(5, 40), "fat_g": rng.randint(3, 35), **prior})
            last = prior["glucose_mg_dl_tp0"]
            for o in SEQUENCE_OFFSETS:
                rise = carbs * 0.6 * (o / 60.0) * (2.0 - o / 60.0)
                preds.append({"evaluation_unit_id": eid, "offset_minutes": o, "prediction": round(last + rise, 1)})
    manifest = _manifest("sequence_meal_cgm_trajectory_like", "sequence", ["evaluation_unit_id", "offset_minutes"],
                         "post-meal interstitial glucose-like trajectory in mg/dL on a fixed 15-minute grid",
                         required_offsets_minutes=SEQUENCE_OFFSETS, example_constant_prediction=100.0)
    schema = _output_schema([{"name": "evaluation_unit_id", "description": "opaque meal key from input.csv"},
                             {"name": "offset_minutes", "description": "one of manifest.required_offsets_minutes, as an integer string"}], "mg/dL")
    return {"manifest.json": _json(manifest), "input.csv": _csv(list(rows[0]), rows),
            "example_predictions.csv": _csv(["evaluation_unit_id", "offset_minutes", "prediction"], preds),
            "output_schema.json": _json(schema)}


def build_bundles() -> dict[str, bytes]:
    """Map of 'bundle/file' -> bytes for every generated file, from one seeded generator."""
    rng = random.Random(SEED)
    out: dict[str, bytes] = {}
    for name, builder in [("participant_scalar", participant_scalar), ("event_scalar", event_scalar), ("sequence", sequence)]:
        for fname, data in builder(rng).items():
            out[f"{name}/{fname}"] = data
    return out
