#!/usr/bin/env bash
# ABOUTME: Builds the reference image and runs it offline on all three synthetic bundles.
# ABOUTME: Validates each output with scripts/validate_predictions.py; fails on any error.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
IMAGE="${IMAGE:-phenobench-reference:local}"

docker build -q -t "$IMAGE" "$REPO/container" >/dev/null
for bundle in participant_scalar event_scalar sequence; do
  out="$REPO/.local-output/$bundle"
  rm -rf "$out"; mkdir -p "$out"
  docker run --rm --network none --cpus 2 --memory 2g \
    -v "$REPO/synthetic/$bundle:/input:ro" \
    -v "$out:/output" \
    "$IMAGE"
  test -f "$out/predictions.csv"
  (cd "$REPO" && uv run scripts/validate_predictions.py "synthetic/$bundle" "$out/predictions.csv")
done
echo "container: reference image valid on all bundles"
