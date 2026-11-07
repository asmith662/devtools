# Copyright (c) 2026
"""Genuine authored binary fits followed by explicit retained-state fault injection."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING, cast

import pytest

from devtools.learning.classification.linear import (
    BinaryLinearTraining,
    FittedBinaryLinearClassifier,
)
from devtools.learning.classification.margin import FittedMarginClassifier
from devtools.learning.representation.features import FeatureTable, FeatureValueKind

if TYPE_CHECKING:
    from collections.abc import Callable

type State = FittedBinaryLinearClassifier | FittedMarginClassifier
type Witness = tuple[State, BinaryLinearTraining]


@pytest.mark.parametrize("method", ["square-logistic", "square-margin"])
def test_fitted_binary_arithmetic_is_label_free(
    fitted: Callable[[str], Witness],
    method: str,
) -> None:
    """Consume actual retained parameters and check exact-zero class selection."""
    state, training = fitted(method)
    prediction = state.classify(training.features)
    assert len(prediction) == len(training.targets)
    assert set(prediction) <= {0, 1}
    zero = replace(state, coefficients=(0.0,) * len(state.feature_names), intercept=0.0)
    assert zero.classify(training.features) == (0,) * len(training.targets)


@pytest.mark.parametrize("method", ["square-logistic", "square-margin"])
@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("feature_names", ()),
        ("feature_names", ("x", "x")),
        ("coefficients", ()),
        ("intercept", float("inf")),
        ("intercept", True),
        ("training_input_sha256", None),
        ("training_input_sha256", "foreign"),
        ("fitting_execution_id", "foreign"),
        ("configuration", ()),
        ("configuration", (("x", "1"), ("x", "2"))),
        ("configuration", (("x",),)),
        ("backend_observations", []),
        ("backend_observations", (("python", ""),)),
        ("references", ()),
    ],
)
def test_corrupt_fitted_binary_metadata_refuses(
    fitted: Callable[[str], Witness],
    method: str,
    field: str,
    bad: object,
) -> None:
    """Preserve immutable schema, native observations and distinct fitting identity."""
    state, _ = fitted(method)
    reconstruct = cast("Callable[..., State]", replace)
    with pytest.raises((ValueError, TypeError)):
        reconstruct(state, **{field: bad})
    with pytest.raises(ValueError, match="distinct model"):
        replace(state, state_id=state.fitting_execution_id)


@pytest.mark.parametrize("method", ["square-logistic", "square-margin"])
def test_incompatible_or_overflowing_query_has_no_prediction(
    fitted: Callable[[str], Witness],
    method: str,
) -> None:
    """Refuse foreign coordinates and unrepresentable retained score arithmetic."""
    state, training = fitted(method)
    foreign = replace(
        training.features,
        feature_names=tuple("foreign-" + n for n in state.feature_names),
    )
    with pytest.raises(ValueError, match="incompatible ordered"):
        state.classify(foreign)
    oversized = replace(
        state,
        coefficients=(1e308,) * len(state.feature_names),
        intercept=0.0,
    )
    query = FeatureTable(
        state.feature_names,
        ((2.0,) * len(state.feature_names),),
        training.features.feature_value_kinds,
    )
    with pytest.raises(ValueError, match="nonfinite retained"):
        oversized.classify(query)


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("features", None),
        ("features", FeatureTable((), (), ())),
        ("targets", (0,) * 8),
        ("targets", (False,) * 8),
        ("row_ids", ("duplicate",) * 8),
        ("row_ids", ("missing",)),
        ("references", ()),
    ],
)
def test_training_requires_original_aligned_binary_source(
    fitted: Callable[[str], Witness],
    field: str,
    bad: object,
) -> None:
    """Invalid source declarations cannot become native fitting inputs."""
    _, training = fitted("square-logistic")
    reconstruct = cast("Callable[..., BinaryLinearTraining]", replace)
    with pytest.raises((ValueError, TypeError)):
        reconstruct(training, **{field: bad})
    discrete = replace(
        training.features,
        feature_value_kinds=(FeatureValueKind.DISCRETE,)
        * len(training.features.feature_names),
    )
    with pytest.raises(ValueError, match="continuous training"):
        replace(training, features=discrete)


def test_margin_cannot_claim_a_different_fitted_objective(
    fitted: Callable[[str], Witness],
) -> None:
    """The retained margin declaration requires L2 squared-hinge configuration."""
    state, _ = fitted("square-margin")
    with pytest.raises(ValueError, match="retained margin objective"):
        replace(state, configuration=(("penalty", "l1"), ("loss", "hinge")))
