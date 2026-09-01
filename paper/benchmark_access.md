# Benchmark access and participation

PhenoBench is released as an evaluation boundary rather than a data release. The
evaluation cohort consists of private, deeply phenotyped participant data that
cannot be distributed; the benchmark therefore separates what is public (the
task definitions, evaluation-unit schemas, metrics, and submission contract)
from what remains evaluator-owned (inputs, targets, and splits).

To make the contract concrete, the release includes schema-faithful, entirely
synthetic example bundles for each evaluation grain: participant-level scalar
prediction, event-level scalar prediction, and fixed-grid sequence prediction.
Every value in these bundles is fabricated; they demonstrate the interface, not
the data.

Model submissions are containerized. A participant supplies an OCI image
referenced by an immutable content digest; the image reads a task bundle from a
read-only mount and writes a prediction file to an output mount, without
network access. Maintainers execute accepted submissions against the private
evaluation data. Outputs pass schema and identifier-alignment validation and
then curation before any result is added to the static leaderboard, which is
regenerated deterministically from a versioned result snapshot carrying source
and provenance fields.

This path improves reproducibility, since the same pinned image can be re-run
by maintainers, without exposing participant data. Evaluation is currently
maintainer-operated rather than self-service: submissions are run as capacity
permits, and neither turnaround time nor publication of every result is
guaranteed.
