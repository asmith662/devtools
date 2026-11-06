# mypy: disable-error-code="import-untyped"
# Copyright (c) 2026
"""Concrete native regression fits, isolated from backend-light retained replay."""

import math
import platform
import warnings
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from importlib import import_module
from time import perf_counter
from typing import Any, cast
from uuid import uuid4

from devtools.learning.evidence.context import ExecutionContext, ExecutionRecorder
from devtools.learning.evidence.events import Admitted, ExecutionEvent, Fact
from devtools.learning.integrations.sklearn.regression.parity import (
    IDENTICAL,
    STRICT,
    inspect_native_query,
)
from devtools.learning.regression.contracts import (
    RegressionInput,
    RegressionMethod,
    RegressionPopulation,
    RegressionRole,
    RegressionSpecification,
)
from devtools.learning.regression.limits import version_limits
from devtools.learning.regression.state import (
    FittedRegression,
    RegressionPredictions,
    training_mean,
    validate_training_state,
)
from devtools.learning.regression.verification import inspect_knn_query
from devtools.learning.representation.features import FeatureTable
from devtools.learning.representation.standardization import (
    FittedFeatureStandardization,
)

_NEIGHBOR_COUNT = 5


@dataclass(slots=True)
class NativeRegressionFit:
    """Retain the declared NativeRegressionFit scientific values and invariants."""

    state: FittedRegression
    estimator: object | None
    native_fit_seconds: float
    validation_version: str = "native-regression-parity-v1"
    parity_receipts: list[dict[str, object]] = field(default_factory=list)

    def predict(self, inputs: RegressionInput) -> RegressionPredictions:
        """Qualify the original native behavior against the retained pure state."""
        self.parity_receipts.clear()
        predicted = self.state.predict(inputs)
        self._check_native(inputs.features, predicted)
        return predicted

    def _check_native(
        self,
        features: FeatureTable,
        predicted: RegressionPredictions,
    ) -> None:
        if self.estimator is None or not features.rows:
            return

        if self.validation_version not in (STRICT, IDENTICAL):
            msg = "unsupported native validation version"
            raise ValueError(msg)
        threadpool_limits = import_module("threadpoolctl").threadpool_limits
        if not (self.state.preparation is not None):
            msg_0 = "Required numerical state invariant is absent."
            raise AssertionError(msg_0)
        rows = self.state.preparation.transform(features).features.rows
        qualified = self._qualify_queries(rows, predicted)
        model = cast("Any", self.estimator)
        with warnings.catch_warnings(), threadpool_limits(limits=1):
            warnings.simplefilter("error")
            native = model.predict(rows)
            if self.state.specification.method is RegressionMethod.KNN:
                self._check_neighbors(model, rows, native, predicted, qualified)
        if len(native) != len(predicted.row_ids) or any(
            (
                not math.isclose(float(a), b, rel_tol=1e-10, abs_tol=1e-12)
                for j, (a, b) in enumerate(
                    zip(native, predicted.values, strict=True),
                )
                if qualified[j]
            ),
        ):
            msg = "native and retained original regression predictions disagree"
            raise ValueError(msg)

    def _check_neighbors(
        self,
        model: object,
        rows: tuple[tuple[float, ...], ...],
        native: Sequence[float],
        predicted: RegressionPredictions,
        qualified: list[bool],
    ) -> None:
        """Verify native membership and distances under the selected parity contract."""
        native_model = cast("Any", model)
        distances, indices = native_model.kneighbors(
            rows,
            n_neighbors=5,
            return_distance=True,
        )
        if not (predicted.neighbor_row_ids is not None):
            msg_0 = "Required numerical state invariant is absent."
            raise AssertionError(msg_0)
        if not (predicted.neighbor_distances is not None):
            msg_0 = "Required numerical state invariant is absent."
            raise AssertionError(msg_0)
        for j, (members, ds) in enumerate(
            zip(
                predicted.neighbor_row_ids,
                predicted.neighbor_distances,
                strict=True,
            ),
        ):
            if self.validation_version == IDENTICAL:
                if self.state.specification.version != "regression-specification-v2":
                    msg = "new parity requires deterministic kNN v2"
                    raise ValueError(msg)
                native_ids = tuple(
                    self.state.training_row_ids[int(i)] for i in indices[j]
                )
                native_distances = tuple(float(d) for d in distances[j])
                classifications = inspect_native_query(
                    self.state,
                    rows[j],
                    native_ids,
                    native_distances,
                    float(native[j]),
                )
                self.parity_receipts.append(
                    {
                        "query_row_id": predicted.row_ids[j],
                        "native_ids": native_ids,
                        "native_distances": native_distances,
                        "native_value": float(native[j]),
                        "classifications": classifications,
                    },
                )
                continue
            if not qualified[j]:
                continue
            actual = {
                self.state.training_row_ids[int(i)]: float(d)
                for i, d in zip(indices[j], distances[j], strict=True)
            }
            if set(actual) != set(members) or any(
                (
                    not math.isclose(actual[i], d, rel_tol=1e-10, abs_tol=1e-12)
                    for i, d in zip(members, ds, strict=True)
                ),
            ):
                msg = "native and retained five-neighbor membership/distance disagree"
                raise ValueError(msg)

    def _qualify_queries(
        self,
        rows: tuple[tuple[float, ...], ...],
        predicted: RegressionPredictions,
    ) -> list[bool]:
        """Inspect deterministic original queries before qualifying native parity."""
        qualified = [True] * len(rows)
        if self.state.specification.version == "regression-specification-v2":
            for j, row in enumerate(rows):
                ids, ds, value, qualified[j] = inspect_knn_query(self.state, row)
                if (
                    predicted.neighbor_row_ids is None
                    or predicted.neighbor_distances is None
                    or predicted.neighbor_row_ids[j] != ids
                    or (predicted.neighbor_distances[j] != ds)
                    or (predicted.values[j] != value)
                ):
                    msg = "independent deterministic neighbor arithmetic differs"
                    raise ValueError(msg)
        return qualified


def _fit_parameters(
    specification: RegressionSpecification,
    training: RegressionPopulation,
    preparation: FittedFeatureStandardization,
) -> tuple[
    object,
    float,
    tuple[float, ...],
    float,
    FeatureTable | None,
    tuple[float, ...] | None,
    tuple[tuple[str, str], ...],
]:
    """Fit exactly the selected Ridge or five-neighbor model with one native thread."""
    t = training.inputs
    coefficients: tuple[float, ...] = ()
    corpus = None
    targets = None
    backend: tuple[tuple[str, str], ...] = (("python", platform.python_version()),)
    np = import_module("numpy")

    scipy = import_module("scipy")
    sklearn = import_module("sklearn")
    ridge_class = import_module("sklearn.linear_model").Ridge
    neighbor_class = import_module("sklearn.neighbors").KNeighborsRegressor
    threadpool_limits = import_module("threadpoolctl").threadpool_limits
    rows = preparation.transform(t.features).features
    backend += (
        ("sklearn", sklearn.__version__),
        ("numpy", np.__version__),
        ("scipy", scipy.__version__),
    )
    with warnings.catch_warnings(), threadpool_limits(limits=1):
        warnings.simplefilter("error")
        if specification.method is RegressionMethod.RIDGE:
            ridge = ridge_class(alpha=1.0, fit_intercept=True, solver="svd")
            native_start = perf_counter()
            ridge.fit(rows.rows, training.values)
            native_seconds = perf_counter() - native_start
            coefficients = tuple(float(v) for v in ridge.coef_)
            intercept = float(ridge.intercept_)
            estimator = ridge
        else:
            knn = neighbor_class(
                n_neighbors=5,
                weights="uniform",
                metric="euclidean",
                algorithm="brute",
                n_jobs=1,
            )
            native_start = perf_counter()
            knn.fit(rows.rows, training.values)
            native_seconds = perf_counter() - native_start
            corpus = rows
            targets = training.values
            intercept = 0.0
            estimator = knn
    return estimator, native_seconds, coefficients, intercept, corpus, targets, backend


def fit_regression(  # noqa: PLR0913 -- explicit scientific provenance/custody; see release qualification review
    specification: RegressionSpecification,
    training: RegressionPopulation,
    preparation: FittedFeatureStandardization | None,
    *,
    recorder: ExecutionRecorder,
    parent: ExecutionContext | None = None,
    observer: Callable[[ExecutionEvent], None] | None = None,
) -> NativeRegressionFit:
    """One real fit per authorized concrete method; no prediction-side refitting."""
    if training.inputs.role is not RegressionRole.TRAINING:
        msg = "only original training targets may enter fitting"
        raise ValueError(msg)
    limits = version_limits(training.inputs.version, "regression-input")
    if (
        specification.version == "regression-specification-v2"
        and training.inputs.version != "regression-input-v2"
    ):
        msg = "deterministic numerical specification requires capacity-v2 input"
        raise ValueError(msg)
    if not 1 <= len(training.values) <= limits.training_rows:
        msg = "declared original training capacity before native fitting"
        raise ValueError(msg)
    if (
        specification.version == "regression-specification-v2"
        and len(training.values) < _NEIGHBOR_COUNT
    ):
        msg = "five actual training rows required before deterministic native fitting"
        raise ValueError(msg)
    with ExecutionContext(
        recorder,
        Admitted(
            "regression.fit",
            (
                Fact("specification_identity", specification.identity),
                Fact("training_identity", training.content_identity),
            ),
        ),
        parent=parent,
        observer=observer,
    ) as run:
        t = training.inputs
        estimator = None
        native_seconds = 0.0
        coefficients: tuple[float, ...] = ()
        intercept = training_mean(training.values)
        corpus = None
        targets = None
        backend: tuple[tuple[str, str], ...] = (("python", platform.python_version()),)
        if specification.method is RegressionMethod.MEAN:
            if preparation is not None:
                msg = "mean requires no feature preparation"
                raise ValueError(msg)
        else:
            if (
                preparation is None
                or preparation.fitting_population_id != t.population_id
                or preparation.source_identity != t.source_identity
            ):
                msg = "original training-only numerical preparation required"
                raise ValueError(msg)
            (
                estimator,
                native_seconds,
                coefficients,
                intercept,
                corpus,
                targets,
                backend,
            ) = _fit_parameters(specification, training, preparation)
        state = FittedRegression(
            specification,
            training.target,
            t.features.feature_names,
            t.features.feature_value_kinds,
            t.feature_units,
            t.population_id,
            t.row_ids,
            training.content_identity,
            preparation,
            coefficients,
            intercept,
            corpus,
            targets,
            run.execution_id,
            uuid4(),
            backend,
            training.inputs.version.replace("regression-input", "fitted-regression"),
        )
        validate_training_state(state, training)
        run.completed(
            (
                Fact("state_identity", state.content_identity),
                Fact("state_id", str(state.state_id)),
                Fact("native_fit", specification.method is not RegressionMethod.MEAN),
            ),
        )
    return NativeRegressionFit(state, estimator, native_seconds)
