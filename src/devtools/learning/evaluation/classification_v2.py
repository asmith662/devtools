# Copyright (c) 2026
"""Versioned binary F1 arithmetic; no fitting or execution authority."""

from .classification import ClassificationEvaluation


def binary_f1_components(
    evaluation: ClassificationEvaluation,
) -> tuple[float | None, ...]:
    """F1 for required integer classes 0,1; an absent direct denominator is undefined.

    A zero-TP class with false positives or false negatives has measured F1 zero,
    even when its separate precision or recall ratio is undefined.
    """
    if any(type(c) is not int or c not in (0, 1) for c in evaluation.categories):
        msg = "v2 requires exact integer binary labels 0 and 1"
        raise ValueError(msg)
    result = []
    for label in (0, 1):
        category = next(
            (c for c in evaluation.per_category if c.category == label),
            None,
        )
        tp = category.true_positive_count if category else 0
        support = category.support if category else 0
        predicted = category.predicted_count if category else 0
        denominator = support + predicted  # 2*TP + FP + FN
        result.append(2 * tp / denominator if denominator else None)
    return tuple(result)


def macro_f1_value(
    evaluation: ClassificationEvaluation,
    *,
    version: int,
) -> float | None:
    """Read a supported F1 version without changing undefined results."""
    if type(version) is not int or version not in (1, 2):
        msg = "explicit supported classification metric version required"
        raise ValueError(msg)
    if version == 1:
        return evaluation.macro_f1
    values = binary_f1_components(evaluation)
    return (
        None
        if any(v is None for v in values)
        else sum(v for v in values if v is not None) / 2
    )
