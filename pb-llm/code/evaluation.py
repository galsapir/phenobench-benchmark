# ABOUTME: Provides dependency-free parsing and primary metrics for the public PhenoBench-LLM contract.
# ABOUTME: Operates on caller-supplied values and never reads participant-level or private experiment data.
from __future__ import annotations

import json
import math
import re
from collections.abc import Mapping, Sequence
from itertools import combinations

_FENCE_RE = re.compile(r"^```(?:json)?\s*\n(.*?)\n```\s*$", re.DOTALL)


def parse_prediction(content_text: str | None, response_field: str) -> float | None:
    """Return a finite numeric response field from a JSON object, otherwise None."""
    if not isinstance(content_text, str):
        return None
    text = content_text.strip()
    fenced = _FENCE_RE.match(text)
    if fenced:
        text = fenced.group(1).strip()
    try:
        payload = json.loads(text)
    except (json.JSONDecodeError, RecursionError):
        return None
    if not isinstance(payload, dict):
        return None
    value = payload.get(response_field)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    number = float(value)
    return number if math.isfinite(number) else None


def parse_ranking(content_text: str | None, labels: set[str]) -> list[str] | None:
    """Return a complete permutation of the expected labels, otherwise None."""
    if not isinstance(content_text, str):
        return None
    text = content_text.strip()
    fenced = _FENCE_RE.match(text)
    if fenced:
        text = fenced.group(1).strip()
    try:
        payload = json.loads(text)
    except (json.JSONDecodeError, RecursionError):
        return None
    order = payload.get("ranking_high_to_low") if isinstance(payload, dict) else None
    if not isinstance(order, list):
        return None
    cleaned = [
        str(value).strip().upper().removeprefix("PARTICIPANT").strip(" :")
        for value in order
    ]
    return cleaned if sorted(cleaned) == sorted(labels) else None


def _paired(
    target: Sequence[float], prediction: Sequence[float]
) -> list[tuple[float, float]]:
    if len(target) != len(prediction):
        raise ValueError("target and prediction lengths differ")
    return [
        (float(y), float(p))
        for y, p in zip(target, prediction, strict=True)
        if math.isfinite(float(y)) and math.isfinite(float(p))
    ]


def r2(target: Sequence[float], prediction: Sequence[float]) -> float:
    """Coefficient of determination over complete target/prediction pairs."""
    pairs = _paired(target, prediction)
    if len(pairs) < 2:
        return math.nan
    mean = sum(y for y, _ in pairs) / len(pairs)
    total = sum((y - mean) ** 2 for y, _ in pairs)
    return 1.0 - sum((p - y) ** 2 for y, p in pairs) / total if total > 0 else math.nan


def roc_auc(target: Sequence[float], probability: Sequence[float]) -> float:
    """Binary AUROC as the positive/negative pair concordance rate, with ties worth one half."""
    pairs = _paired(target, probability)
    positive = [min(1.0, max(0.0, p)) for y, p in pairs if y > 0.5]
    negative = [min(1.0, max(0.0, p)) for y, p in pairs if y <= 0.5]
    if not positive or not negative:
        return math.nan
    score = sum(
        1.0 if pos > neg else 0.5 if pos == neg else 0.0
        for pos in positive
        for neg in negative
    )
    return score / (len(positive) * len(negative))


def pairwise_accuracy(target: Sequence[float], prediction: Sequence[float]) -> float:
    """Accuracy over scored ranking pairs; prediction ties receive one-half credit."""
    pairs = _paired(target, prediction)
    if not pairs:
        return math.nan
    correct = [0.5 if p == 0.5 else float((p > 0.5) == (y > 0.5)) for y, p in pairs]
    return sum(correct) / len(correct)


def head_to_head_win_rates(
    rows: Sequence[Mapping[str, str | float]],
) -> dict[str, dict[str, float | int]]:
    """Compute model win rates from task rows, comparing only models observed on the same task."""
    by_task: dict[str, dict[str, float]] = {}
    for row in rows:
        task = str(row["task"])
        model = str(row["model_key"])
        score = float(row["llm_full"])
        if not math.isfinite(score):
            continue
        if model in by_task.setdefault(task, {}):
            raise ValueError(f"duplicate task/model row: {task}/{model}")
        by_task[task][model] = score

    wins: dict[str, float] = {}
    games: dict[str, int] = {}
    for scores in by_task.values():
        for first, second in combinations(sorted(scores), 2):
            wins.setdefault(first, 0.0)
            wins.setdefault(second, 0.0)
            games[first] = games.get(first, 0) + 1
            games[second] = games.get(second, 0) + 1
            if scores[first] > scores[second]:
                wins[first] += 1.0
            elif scores[second] > scores[first]:
                wins[second] += 1.0
            else:
                wins[first] += 0.5
                wins[second] += 0.5
    return {
        model: {
            "wins": wins[model],
            "games": games[model],
            "win_rate": wins[model] / games[model],
        }
        for model in sorted(games)
        if games[model]
    }
