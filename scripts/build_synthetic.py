#!/usr/bin/env python3
# ABOUTME: Writes the generated files of the three synthetic task bundles under synthetic/.
# ABOUTME: Deterministic; --check verifies committed files match the generator without writing.
from __future__ import annotations

import argparse
import sys

from _paths import REPO, write_or_check

from submission_materials.synthetic import build_bundles


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    outputs = {REPO / "synthetic" / rel: data for rel, data in build_bundles().items()}
    return write_or_check(outputs, args.check)


if __name__ == "__main__":
    sys.exit(main())
