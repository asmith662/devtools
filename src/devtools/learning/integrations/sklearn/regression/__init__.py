# mypy: disable-error-code="import-untyped"
# Copyright (c) 2026
"""Concrete native regression fits, isolated from backend-light retained replay."""

import math
import platform
import warnings
from collections.abc import Callable
from dataclasses import dataclass, field
from importlib import import_module
from time import perf_counter
from uuid import uuid4

from devtools.learning.evidence.context import ExecutionContext, ExecutionRecorder
from devtools.learning.evidence.events import Admitted, ExecutionEvent, Fact
from devtools.learning.regression.batching import (
    BatchedRegressionPredictions,
    RegressionBatching,
    predict_regression_batches,
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

    def predict_batches(
        self,
        inputs: RegressionInput,
        specification: RegressionBatching,
        *,
        progress: Callable[[int, int], None] | None = None,
    ) -> BatchedRegressionPredictions:
        """Qualify each numerical batch against ONE original native fitted model."""
        self.parity_receipts.clear()
        result = predict_regression_batches(self.state, inputs, specification)
        for batch in result.evidence.batches:
            features = FeatureTable(
                inputs.features.feature_names,
                inputs.features.rows[batch.start : batch.stop],
                inputs.features.feature_value_kinds,
            )
            self._check_native(features, result.predictions, batch.start, batch.stop)
            if progress is not None:
                progress(batch.stop, len(inputs.row_ids))
        return result

    def _check_native(
        self,
        features: FeatureTable,
        predicted: RegressionPredictions,
        start: int = 0,
        stop: int | None = None,
    ) -> None:
        if self.estimator is None or not features.rows:
            return
        from devtools.learning.integrations.sklearn.regression.parity import (
            IDENTICAL,
            STRICT,
            inspect_native_query,
        )

        if self.validation_version not in (STRICT, IDENTICAL):
            msg = "unsupported native validation version"
            raise ValueError(msg)
        if stop is None:
            stop = len(predicted.row_ids)
        from typing import Any, cast

        threadpool_limits = import_module("threadpoolctl").threadpool_limits
        if not (self.state.preparation is not None):
            msg_0 = "Required numerical state invariant is absent."
            raise AssertionError(msg_0)
        rows = self.state.preparation.transform(features).features.rows
        qualified = [True] * len(rows)
        if self.state.specification.version == "regression-specification-v2":
            from devtools.learning.regression.verification import inspect_knn_query

            for j, row in enumerate(rows):
                ids, ds, value, qualified[j] = inspect_knn_query(self.state, row)
                if (
                    predicted.neighbor_row_ids is None
                    or predicted.neighbor_distances is None
                    or predicted.neighbor_row_ids[start + j] != ids
                    or (predicted.neighbor_distances[start + j] != ds)
                    or (predicted.values[start + j] != value)
                ):
                    msg = "independent deterministic neighbor arithmetic differs"
                    raise ValueError(msg)
        model = cast("Any", self.estimator)
        with warnings.catch_warnings(), threadpool_limits(limits=1):
            warnings.simplefilter("error")
            native = model.predict(rows)
            if self.state.specification.method is RegressionMethod.KNN:
                distances, indices = model.kneighbors(
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
                        predicted.neighbor_row_ids[start:stop],
                        predicted.neighbor_distances[start:stop],
                        strict=True,
                    ),
                ):
                    if self.validation_version == IDENTICAL:
                        if (
                            self.state.specification.version
                            != "regression-specification-v2"
                        ):
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
                                "query_row_id": predicted.row_ids[start + j],
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
        if len(native) != stop - start or any(
            (
                not math.isclose(float(a), b, rel_tol=1e-10, abs_tol=1e-12)
                for j, (a, b) in enumerate(
                    zip(native, predicted.values[start:stop], strict=True),
                )
                if qualified[j]
            ),
        ):
            msg = "native and retained original regression predictions disagree"
            raise ValueError(msg)


def fit_regression(
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
            import numpy as np

            scipy = import_module("scipy")
            sklearn = import_module("sklearn")
            Ridge = import_module("sklearn.linear_model").Ridge
            KNeighborsRegressor = import_module("sklearn.neighbors").KNeighborsRegressor
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
                    ridge = Ridge(alpha=1.0, fit_intercept=True, solver="svd")
                    native_start = perf_counter()
                    ridge.fit(rows.rows, training.values)
                    native_seconds = perf_counter() - native_start
                    coefficients = tuple(float(v) for v in ridge.coef_)
                    intercept = float(ridge.intercept_)
                    estimator = ridge
                else:
                    knn = KNeighborsRegressor(
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
