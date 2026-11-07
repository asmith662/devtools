# Copyright (c) 2026
"""Independent count arithmetic and semantic corruption refusals."""

from dataclasses import replace

import pytest

from devtools.learning.evaluation.classification import (
    ClassificationConfusionMatrix,
    ClassificationEvaluation,
    PerCategoryEvaluation,
    evaluate_classification,
)
from devtools.learning.evaluation.classification_v2 import (
    binary_f1_components,
    macro_f1_value,
)


def test_type_identity_and_independent_counts() -> None:
    """A category's exact type determines the confusion matrix position."""
    result = evaluate_classification(("a", 1, 1.0, True), ("a", 1, True, 1.0))
    assert result.categories == ("a", 1, 1.0, True)
    expected_accuracy = 2 / 4
    assert result.accuracy == expected_accuracy
    assert result.confusion_matrix.count(1.0, True) == 1
    assert result.macro_precision == result.macro_recall == expected_accuracy
    assert result.macro_f1 is None
    with pytest.raises(KeyError):
        result.confusion_matrix.count("missing", 1)


def test_f1_versions_preserve_nonvalues() -> None:
    """Direct counts measure zero F1 where harmonic v1 remains undefined."""
    wrong = evaluate_classification((0, 1), (1, 0))
    assert binary_f1_components(wrong) == (0.0, 0.0)
    assert macro_f1_value(wrong, version=1) is None
    assert macro_f1_value(wrong, version=2) == 0.0
    absent = evaluate_classification((0,), (0,))
    assert macro_f1_value(absent, version=1) == 1.0
    assert macro_f1_value(absent, version=2) is None
    imperfect = evaluate_classification((0, 0, 1), (0, 1, 1))
    assert imperfect.macro_f1 == pytest.approx(2 / 3)
    assert macro_f1_value(imperfect, version=2) == pytest.approx(2 / 3)
    missing = evaluate_classification((0,), (1,))
    assert missing.macro_precision is missing.macro_recall is None
    with pytest.raises(ValueError, match="binary"):
        binary_f1_components(evaluate_classification((True,), (True,)))
    with pytest.raises(ValueError, match="version"):
        macro_f1_value(wrong, version=3)


@pytest.mark.parametrize(
    ("categories", "counts"),
    [((), ()), ((0, 0), ((1, 0), (0, 1))), ((0,), ()), ((0,), ((-1,),))],
)
def test_matrix_corruption(
    categories: tuple[int, ...],
    counts: tuple[tuple[int, ...], ...],
) -> None:
    """A malformed matrix cannot be accepted as evaluation evidence."""
    with pytest.raises(ValueError, match="confusion"):
        ClassificationConfusionMatrix(categories, counts)


@pytest.mark.parametrize("counts", [(-1, 0, 0), (1, 1, 2)])
def test_category_count_corruption(counts: tuple[int, int, int]) -> None:
    """True positives cannot exceed source or prediction population."""
    with pytest.raises(ValueError, match=r"counts|positives"):
        PerCategoryEvaluation(0, *counts)


@pytest.mark.parametrize(
    "changes",
    [
        {"observation_count": 0},
        {"correct_count": 3},
        {"confusion_matrix": None},
        {"per_category": ()},
        {"per_category": (None, None)},
        {
            "per_category": (
                PerCategoryEvaluation(1, 1, 1, 1),
                PerCategoryEvaluation(0, 1, 1, 1),
            ),
        },
        {"observation_count": 3},
        {"correct_count": 1},
        {
            "per_category": (
                PerCategoryEvaluation(0, 2, 1, 1),
                PerCategoryEvaluation(1, 1, 1, 1),
            ),
        },
    ],
)
def test_evaluation_correspondence(changes: dict[str, object]) -> None:
    """Every redundant metric field must agree with the independent matrix."""
    original = evaluate_classification((0, 1), (0, 1))
    with pytest.raises((ValueError, TypeError)):
        replace(original, **changes)  # type: ignore[arg-type]


def test_no_empty_or_misaligned_evaluation() -> None:
    """An absent population cannot become a perfect score."""
    with pytest.raises(ValueError, match="requires"):
        evaluate_classification((), ())
    with pytest.raises(ValueError, match="match"):
        evaluate_classification((0,), ())
    result = evaluate_classification((0, 1), (0, 1))
    assert isinstance(result, ClassificationEvaluation)
    assert result.macro_precision == result.macro_recall == result.macro_f1 == 1.0
