# ABOUTME: Shared repository path constants and a --check helper for the build scripts.
# ABOUTME: Keeps generated-file locations in one place so builders and checkers agree.
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

DEFAULT_SNAPSHOT = REPO / "snapshots" / "provisional" / "results.json"
SITE_GENERATED = REPO / "site" / "generated"


def write_or_check(outputs: dict[Path, bytes], check: bool) -> int:
    """Write outputs, or with check=True report any that differ from disk without writing."""
    stale = [p for p, data in outputs.items() if not p.exists() or p.read_bytes() != data]
    if check:
        for p in stale:
            print(f"stale: {p.relative_to(REPO)}", file=sys.stderr)
        return 1 if stale else 0
    for p, data in outputs.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    return 0
