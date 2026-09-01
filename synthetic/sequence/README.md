# sequence (meal-conditioned CGM trajectory-like)

Evaluation unit: **one logged meal**, but the prediction is a **trajectory**:
one value for each offset in `manifest.required_offsets_minutes` (15..120 min
after the meal, every 15 min). `predictions.csv` therefore has
`events x offsets` rows keyed by (`evaluation_unit_id`, `offset_minutes`), and
every pair must be present exactly once.

Inputs are meal macronutrients and the pre-meal glucose readings at fixed
event-relative offsets (-60..0 min). Target is interstitial glucose in mg/dL;
primary metric is RMSE over all grid points on the held-out participant split.
