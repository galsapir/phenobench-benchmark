#!/usr/bin/env python3
# ABOUTME: Validates one predictions.csv against one synthetic task bundle and prints its canonical digest.
# ABOUTME: Exit 0 on a valid file; exit 1 with the first violation on stderr otherwise.
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import _paths  # noqa: F401  (adds repo root to sys.path)

from submission_materials.predictions import PredictionError, canonical_digest


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("bundle", type=Path)
    ap.add_argument("predictions", type=Path)
    args = ap.parse_args()
    try:
        digest = canonical_digest(args.bundle, args.predictions)
    except PredictionError as exc:
        print(f"invalid: {exc}", file=sys.stderr)
        return 1
    print(f"valid bundle={args.bundle.name} digest={digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
