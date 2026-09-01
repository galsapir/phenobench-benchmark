# Synthetic task bundles

Three tiny, entirely fabricated bundles, one per evaluation-unit grain. They are
schema-faithful examples of what a submitted container reads and writes. No value
here comes from any participant; everything is produced by a seeded generator
(`submission_materials/synthetic.py`, run via `scripts/build_synthetic.py`).

| bundle | grain | identifier columns | prediction rows |
|---|---|---|---|
| `participant_scalar/` | one row per participant | `participant_id` | one per participant |
| `event_scalar/` | one row per repeated event (night) | `evaluation_unit_id` | one per event |
| `sequence/` | one value per event per time offset | `evaluation_unit_id`, `offset_minutes` | events x offsets |

Each bundle contains:

- `manifest.json`: schema version, grain, identifier columns, prediction column, target description.
- `input.csv`: model inputs only. No targets. Targets are evaluator-owned and private.
- `example_predictions.csv`: a valid prediction file, demonstrating the interface only.
- `output_schema.json`: JSON schema of one prediction row.
- `README.md`: what one row means.

Validate any prediction file with:

```bash
uv run scripts/validate_predictions.py synthetic/<bundle> path/to/predictions.csv
```

Rules enforced by the validator: exact column set and order; every identifier
tuple from `input.csv` present exactly once; no unknown identifiers; finite
numeric predictions. Row order does not matter.
