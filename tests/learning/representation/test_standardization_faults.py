# Copyright (c) 2026
"""Retained preparation guards and explicit arithmetic-library fault controls."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, cast

import pytest

from devtools.learning.representation import standardization as module
from devtools.learning.representation.features import FeatureValueKind
from devtools.learning.representation.observations import PopulationScope
from devtools.learning.representation.standardization import (
    FeatureStandardizationSpecification,
    _z,
    fit_feature_standardization,
)
from tests.learning.representation.test_standardization import _table


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        ("specification", "invented", TypeError),
        ("fitting_population_id", "", ValueError),
        ("fitting_scope", PopulationScope.TEST, ValueError),
        ("fitting_input_sha256", "invented", ValueError),
        ("construction_execution_id", "invented", ValueError),
        ("training_means", (0.0, 1.0), ValueError),
        ("feature_value_kinds", (FeatureValueKind.DISCRETE,), ValueError),
    ],
)
def test_fitted_preparation_cannot_lose_semantics(
    field: str,
    value: object,
    error: type[Exception],
) -> None:
    """Real fitted statistics retain typed identities, dimensions and roles."""
    state = fit_feature_standardization(
        FeatureStandardizationSpecification(("x",)),
        _table((1, 2)),
        population_id="training",
    )
    with pytest.raises(error):
        replace(state, **{field: cast("Any", value)})
    with pytest.raises(ValueError, match="identities differ"):
        replace(state, state_id=state.construction_execution_id)


@pytest.mark.parametrize(
    ("field", "value"),
    [("execution_id", "invented"), ("scope", "test"), ("input_sha256", "wrong")],
)
def test_application_cannot_invent_scope_or_correspondence(
    field: str,
    value: object,
) -> None:
    """A transformed result preserves exact selected-input and occurrence metadata."""
    state = fit_feature_standardization(
        FeatureStandardizationSpecification(("x",)),
        _table((1, 2)),
        population_id="training",
    )
    result = state.transform(_table((3,)))
    with pytest.raises((TypeError, ValueError)):
        replace(result, **{field: cast("Any", value)})
    with pytest.raises(TypeError, match="scope"):
        state.transform(_table((3,)), scope=cast("Any", "future"))
    with pytest.raises(ValueError, match="explicit recorder"):
        state.transform(_table((3,)), observer=lambda _: None)


def test_unrepresentable_fraction_and_statistical_backend_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Actual Fraction overflow and simulated library failure remain refusals."""
    with pytest.raises(ValueError, match="not finitely representable"):
        _z(1e308, -1e308, 1e-308)

    def fail(_: object) -> float:
        message = "simulated statistics-library failure"
        raise OverflowError(message)

    monkeypatch.setattr(module, "mean", fail)
    with pytest.raises(ValueError, match="not finitely representable"):
        fit_feature_standardization(
            FeatureStandardizationSpecification(("x",)),
            _table((1, 2)),
            population_id="training",
        )
