# participant_scalar (HbA1c-like)

Evaluation unit: **one participant**. Each `participant_id` (a canonical UUID)
appears once in `input.csv` and must appear exactly once in `predictions.csv`.

Inputs are a few demographic/anthropometric columns. The target is a scalar in
percent; the real Task's primary metric is R2 on the held-out participant split.
