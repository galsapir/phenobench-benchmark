# Container submission contract

A submission is an OCI image. Maintainers run it manually against private
evaluation data; nothing here is self-service.

## Contract

- Submitter provides a **public registry reference pinned by immutable digest**,
  e.g. `ghcr.io/team/model@sha256:...` or `docker.io/team/model@sha256:...`.
  Tags are not accepted.
- Evaluator mounts one task bundle read-only at `/input`
  (`manifest.json`, `input.csv`, plus any files the manifest names).
- Evaluator mounts an empty writable directory at `/output`.
- The image's **default entrypoint** reads the manifest and inputs and writes
  `/output/predictions.csv` with exactly the columns
  `manifest.identifier_columns + [manifest.prediction_column]`.
- One container invocation processes one task bundle.
- **No network** (`--network none`). Bundle all weights inside the image.
- stdout/stderr are diagnostic only; the prediction file is authoritative.
- Fails validation: non-zero exit, timeout, missing output, malformed schema,
  duplicate identifiers, unknown identifiers, incomplete coverage of the
  identifiers in `input.csv`, non-finite predictions.

## Reproducible invocation

```bash
mkdir -p .local-output/participant_scalar
docker run --rm \
  --network none \
  --cpus 4 \
  --memory 16g \
  -v "$PWD/synthetic/participant_scalar:/input:ro" \
  -v "$PWD/.local-output/participant_scalar:/output" \
  IMAGE_BY_DIGEST
uv run scripts/validate_predictions.py synthetic/participant_scalar .local-output/participant_scalar/predictions.csv
```

Defaults are conservative CPU limits (4 CPUs, 16 GB, wall-clock timeout on the
order of one hour per bundle at the maintainer's discretion). GPU evaluation
may be possible depending on maintainer capacity; it is not guaranteed and no
service level is promised.

## Reference image

`Dockerfile` + `predict.py` build a deliberately trivial image that emits a
constant (scalar grains) or last-observed-glucose persistence (sequence grain).
Its purpose is contract verification, not performance. `test.sh` builds it and
runs it offline on all three synthetic bundles, then validates the outputs.
