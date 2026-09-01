# event_scalar (next-night sleep-like)

Evaluation unit: **one participant-night**. A participant contributes several
rows; each has its own opaque `evaluation_unit_id` composed of participant,
diet date, sleep-night date and an ordinal. Predict one scalar per event.

Inputs are the day's activity/diet summaries and the prior night's value. The
target is next-night mean sleeping heart rate in bpm; primary metric is R2 on
the held-out participant split. Splitting is by participant, so all of one
participant's nights are on the same side.
