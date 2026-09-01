# ABOUTME: Trivial reference predictor that satisfies the PhenoBench container contract for every bundle grain.
# ABOUTME: Reads /input/manifest.json and input.csv, writes /output/predictions.csv; stdlib only, deterministic.
from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path

INPUT = Path(os.environ.get("PB_INPUT", "/input"))
OUTPUT = Path(os.environ.get("PB_OUTPUT", "/output"))


def main() -> int:
    manifest = json.loads((INPUT / "manifest.json").read_text())
    id_cols = manifest["identifier_columns"]
    pred_col = manifest["prediction_column"]
    constant = float(manifest["example_constant_prediction"])
    rows = list(csv.DictReader((INPUT / manifest["input_file"]).read_text().splitlines()))
    unit_col = id_cols[0]

    out_rows = []
    if manifest["grain"] == "sequence":
        offsets = manifest["required_offsets_minutes"]
        for r in rows:
            last = r.get("glucose_mg_dl_tp0")
            value = float(last) if last not in (None, "") else constant
            for o in offsets:
                out_rows.append({unit_col: r[unit_col], id_cols[1]: o, pred_col: value})
    else:
        for r in rows:
            out_rows.append({unit_col: r[unit_col], pred_col: constant})

    OUTPUT.mkdir(parents=True, exist_ok=True)
    with (OUTPUT / manifest["prediction_file_name"]).open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=id_cols + [pred_col], lineterminator="\n")
        w.writeheader()
        w.writerows(out_rows)
    print(f"[reference-predictor] task={manifest['task_id']} rows={len(out_rows)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
