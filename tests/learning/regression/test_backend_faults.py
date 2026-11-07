# Copyright (c) 2026
"""Original native parity guards against explicitly authored backend reports."""

from __future__ import annotations

import copy
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.learning.integrations.local.ledger import SQLiteExecutionRecorder
from devtools.learning.integrations.sklearn.regression import (
    NativeRegressionFit,
    fit_regression,
)
from devtools.learning.integrations.sklearn.regression.parity import IDENTICAL, STRICT
from devtools.learning.regression.contracts import (
    RegressionMethod,
    RegressionPopulation,
    RegressionRole,
    RegressionSpecification,
)
from devtools.learning.regression.state import FittedRegression, RegressionPredictions

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

type Witnesses = Callable[[str], tuple[FittedRegression, RegressionPopulation]]


class _ReportedEstimator:
    """Report retained values with a selected fault; perform no fitting."""

    def __init__(
        self,
        state: FittedRegression,
        predictions: RegressionPredictions,
    ) -> None:
        self.values = predictions.values
        assert predictions.neighbor_distances is not None
        assert predictions.neighbor_row_ids is not None
        self.distances = predictions.neighbor_distances
        self.indices = tuple(
            tuple(state.training_row_ids.index(identity) for identity in row)
            for row in predictions.neighbor_row_ids
        )

    def predict(self, _: object) -> tuple[float, ...]:
        """Return authored report values without numerical optimization."""
        return self.values

    def kneighbors(
        self,
        _: object,
        *,
        n_neighbors: int,
        return_distance: bool,
    ) -> tuple[tuple[tuple[float, ...], ...], tuple[tuple[int, ...], ...]]:
        """Return authored neighbor reports while retaining call semantics."""
        assert n_neighbors == len(self.indices[0])
        assert return_distance
        return self.distances, self.indices


@pytest.mark.parametrize("contract", [STRICT, IDENTICAL])
def test_exact_authored_native_reports_and_identity_parity_receipts(
    fitted_states: Witnesses,
    contract: str,
) -> None:
    """Check authored reports against actual retained arithmetic."""
    state, training = fitted_states("knn-v2")
    predicted = state.predict(training.inputs)
    model = _ReportedEstimator(state, predicted)
    fit = NativeRegressionFit(state, model, 0.0, contract)
    assert fit.predict(training.inputs) == predicted
    assert bool(fit.parity_receipts) == (contract == IDENTICAL)


@pytest.mark.parametrize("fault", ["version", "values", "neighbors", "distance"])
def test_false_native_reports_cannot_pass_retained_parity(
    fitted_states: Witnesses,
    fault: str,
) -> None:
    """Finite false reports remain refusals without another native fit or retry."""
    state, training = fitted_states("knn-v2")
    predicted = state.predict(training.inputs)
    model = _ReportedEstimator(state, predicted)
    contract = STRICT
    if fault == "version":
        contract = "unknown"
    elif fault == "values":
        model.values = tuple(value + 10 for value in predicted.values)
    elif fault == "neighbors":
        model.indices = tuple((0,) * len(row) for row in model.indices)
    else:
        model.distances = tuple(
            tuple(value + 10 for value in row) for row in model.distances
        )
    fit = NativeRegressionFit(state, model, 0.0, contract)
    with pytest.raises(
        ValueError,
        match=r"validation version|predictions disagree|membership/distance",
    ):
        fit.predict(training.inputs)


@pytest.mark.parametrize(
    "fault",
    ["preparation", "ids", "distances", "arithmetic", "legacy"],
)
def test_corrupted_component_reports_reach_backend_invariant_guards(
    fitted_states: Witnesses,
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
) -> None:
    """Simulate an invalid retained-component return; do not certify its state."""
    original, training = fitted_states("knn-v2")
    state = copy.copy(original)
    predicted = original.predict(training.inputs)
    model = _ReportedEstimator(state, predicted)
    contract = STRICT
    if fault == "preparation":
        object.__setattr__(state, "preparation", None)
    elif fault == "arithmetic":
        predicted = replace(
            predicted,
            values=tuple(value + 1 for value in predicted.values),
        )
    else:
        object.__setattr__(
            state,
            "specification",
            RegressionSpecification(RegressionMethod.KNN),
        )
        if fault == "legacy":
            contract = IDENTICAL
        else:
            predicted = copy.copy(predicted)
            object.__setattr__(
                predicted,
                "neighbor_row_ids" if fault == "ids" else "neighbor_distances",
                None,
            )
    monkeypatch.setattr(FittedRegression, "predict", lambda *_: predicted)
    fit = NativeRegressionFit(state, model, 0.0, contract)
    with pytest.raises(
        (AssertionError, ValueError),
        match=r"invariant|arithmetic|requires deterministic",
    ):
        fit.predict(training.inputs)


@pytest.mark.parametrize(
    "fault",
    ["role", "capacity", "version", "rows", "mean-preparation", "missing-preparation"],
)
def test_fit_refusals_precede_native_optimization(
    fitted_states: Witnesses,
    tmp_path: Path,
    fault: str,
) -> None:
    """Use real fitting populations; malformed controls never reach a native call."""
    witness, original = fitted_states("knn-v2")
    training = original
    spec = witness.specification
    preparation = witness.preparation
    if fault == "role":
        training = replace(
            original,
            inputs=replace(original.inputs, role=RegressionRole.DEVELOPMENT),
        )
    elif fault == "capacity":
        training = replace(
            original,
            inputs=replace(
                original.inputs,
                row_ids=(),
                features=replace(original.inputs.features, rows=()),
            ),
            values=(),
        )
    elif fault == "version":
        training = replace(
            original,
            inputs=replace(original.inputs, version="regression-input-v1"),
            version="regression-population-v1",
        )
    elif fault == "rows":
        training = replace(
            original,
            inputs=replace(
                original.inputs,
                row_ids=original.inputs.row_ids[:1],
                features=replace(
                    original.inputs.features,
                    rows=original.inputs.features.rows[:1],
                ),
            ),
            values=original.values[:1],
        )
    elif fault == "mean-preparation":
        spec = RegressionSpecification(RegressionMethod.MEAN)
    else:
        preparation = None
    with (
        SQLiteExecutionRecorder(tmp_path / "science.sqlite") as recorder,
        pytest.raises(
            ValueError,
            match=r"training targets|capacity|training rows|preparation",
        ),
    ):
        fit_regression(spec, training, preparation, recorder=recorder)
