# Contributing to PhenoBench

PhenoBench accepts model-evaluation requests through a manual,
maintainer-operated process. Human Phenotype Project evaluation data remain
private.

## Submit a model

1. Choose a Benchmark Track from the public catalog. Methods are comparable
   only within a Track that fixes the Task, split, metric, and allowed inputs.
2. Develop against the fabricated bundles under `synthetic/`.
3. Package the predictor as an OCI image using `container/README.md`.
4. Push the image to a public registry and pin it by immutable digest:
   `registry.example/model@sha256:...`.
5. Open a **Model submission** issue and complete every required field.

Maintainers review the request, run accepted images without network access,
validate the output contract, and curate aggregate results before publication.
There is no guaranteed turnaround, no automated queue, and no guarantee that
every submitted image will be run or published.

Never attach participant data, predictions on private evaluation inputs,
credentials, registry tokens, or private infrastructure links to an issue.

## Improve public materials

Corrections to task cards, documentation, schemas, and synthetic examples are
welcome as pull requests. Explain the scientific or interface decision and add
or update tests for executable behavior. Synthetic examples must remain fully
fabricated.

Code is Apache-2.0. Documentation, task cards, synthetic examples, and
aggregate results are CC BY 4.0; see `LICENSE-DOCS`.
