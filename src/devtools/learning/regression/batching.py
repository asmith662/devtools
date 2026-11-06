# Copyright (c) 2026
"""Computational ranges of ONE source population, never new scientific roles."""

from collections.abc import Callable
from dataclasses import asdict, dataclass

from devtools.learning.classification.linear import _hash
from devtools.learning.measurement.contracts import nonempty
from devtools.learning.regression.contracts import RegressionInput, RegressionMethod
from devtools.learning.regression.limits import REGRESSION_V2, prediction_byte_bound
from devtools.learning.regression.state import FittedRegression, RegressionPredictions


@dataclass(frozen=True, slots=True)
class RegressionBatching:
    batch_size: int
    maximum_distance_operations: int
    maximum_output_bytes: int = REGRESSION_V2.prediction_bytes
    version: str = "regression-batching-v1"

    def __post_init__(self) -> None:
        if (
            self.version != "regression-batching-v1"
            or type(self.batch_size) is not int
            or (not 1 <= self.batch_size <= REGRESSION_V2.prediction_rows)
            or (type(self.maximum_distance_operations) is not int)
            or (
                not 1
                <= self.maximum_distance_operations
                <= REGRESSION_V2.distance_operations
            )
            or (type(self.maximum_output_bytes) is not int)
            or (not 1 <= self.maximum_output_bytes <= REGRESSION_V2.prediction_bytes)
        ):
            msg = "explicit finite regression batch/work bounds required"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class RegressionPredictionBatch:
    start: int
    stop: int
    row_ids: tuple[str, ...]
    prediction_sha256: str

    def __post_init__(self) -> None:
        if (
            type(self.start) is not int
            or type(self.stop) is not int
            or (not 0 <= self.start < self.stop <= REGRESSION_V2.prediction_rows)
            or (type(self.row_ids) is not tuple)
            or (len(self.row_ids) != self.stop - self.start)
            or (len(set(self.row_ids)) != len(self.row_ids))
            or (len(self.prediction_sha256) != 64)
            or any(c not in "0123456789abcdef" for c in self.prediction_sha256)
        ):
            msg = "exact bounded prediction batch rows/digest required"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class RegressionBatchEvidence:
    specification: RegressionBatching
    state_identity: str
    input_identity: str
    prediction_identity: str
    batches: tuple[RegressionPredictionBatch, ...]
    version: str = "regression-batch-evidence-v1"

    def __post_init__(self) -> None:
        if (
            self.version != "regression-batch-evidence-v1"
            or type(self.specification) is not RegressionBatching
            or type(self.batches) is not tuple
            or (not self.batches)
        ):
            msg = "explicit complete bounded prediction batch evidence"
            raise ValueError(msg)
        for value in (
            self.state_identity,
            self.input_identity,
            self.prediction_identity,
        ):
            nonempty(value)
        next_start = 0
        rows: list[str] = []
        for batch in self.batches:
            if (
                type(batch) is not RegressionPredictionBatch
                or batch.start != next_start
                or batch.stop - batch.start > self.specification.batch_size
            ):
                msg = "ordered gap-free nonoverlapping batch ranges required"
                raise ValueError(msg)
            next_start = batch.stop
            rows.extend(batch.row_ids)
        if len(set(rows)) != len(rows):
            msg = "duplicate original rows across prediction batches"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class BatchedRegressionPredictions:
    predictions: RegressionPredictions
    evidence: RegressionBatchEvidence

    def __post_init__(self) -> None:
        if (
            type(self.predictions) is not RegressionPredictions
            or type(self.evidence) is not RegressionBatchEvidence
            or self.predictions.content_identity != self.evidence.prediction_identity
            or (self.predictions.input_identity != self.evidence.input_identity)
            or (
                tuple(r for b in self.evidence.batches for r in b.row_ids)
                != self.predictions.row_ids
            )
        ):
            msg = "complete original prediction reassembly correspondence"
            raise ValueError(msg)


def regression_batch_ranges(
    state: FittedRegression,
    inputs: RegressionInput,
    specification: RegressionBatching,
    *,
    ranges: tuple[tuple[int, int], ...] | None = None,
) -> tuple[tuple[int, int], ...]:
    """Validate finite full work and exact ranges without predicting or fitting."""
    if (
        type(state) is not FittedRegression
        or type(inputs) is not RegressionInput
        or type(specification) is not RegressionBatching
    ):
        msg = "typed original state/input and explicit batch specification"
        raise ValueError(msg)
    if (
        inputs.features.feature_names,
        inputs.features.feature_value_kinds,
        inputs.feature_units,
    ) != (state.feature_names, state.feature_value_kinds, state.feature_units):
        msg = "original ordered prediction schema/units required"
        raise ValueError(msg)
    count = len(inputs.row_ids)
    if not 1 <= count <= REGRESSION_V2.prediction_rows:
        msg = "bounded nonempty complete prediction population required"
        raise ValueError(msg)
    work = (
        count * len(state.training_row_ids) * len(state.feature_names)
        if state.specification.method is RegressionMethod.KNN
        else 0
    )
    if work > specification.maximum_distance_operations:
        msg = "complete-corpus prediction work exceeds caller budget"
        raise ValueError(msg)
    if (
        prediction_byte_bound(
            inputs.row_ids,
            state.training_row_ids,
            (
                inputs.population_id,
                state.target.identity,
                state.target.quantity,
                state.target.unit,
            ),
            neighbors=state.specification.method is RegressionMethod.KNN,
        )
        > specification.maximum_output_bytes
    ):
        msg = "complete prediction payload exceeds caller budget"
        raise ValueError(msg)
    if ranges is None:
        ranges = tuple(
            (start, min(count, start + specification.batch_size))
            for start in range(0, count, specification.batch_size)
        )
    if type(ranges) is not tuple or not ranges:
        msg = "explicit immutable complete batch ranges required"
        raise ValueError(msg)
    next_start = 0
    for pair in ranges:
        if (
            type(pair) is not tuple
            or len(pair) != 2
            or any(type(v) is not int for v in pair)
            or (pair[0] != next_start)
            or (not pair[0] < pair[1] <= count)
            or (pair[1] - pair[0] > specification.batch_size)
        ):
            msg = "batch overlap/gap/order/size before materialization"
            raise ValueError(msg)
        next_start = pair[1]
    if next_start != count:
        msg = "missing final batch or original prediction rows"
        raise ValueError(msg)
    return ranges


def predict_regression_batches(
    state: FittedRegression,
    inputs: RegressionInput,
    specification: RegressionBatching,
    *,
    ranges: tuple[tuple[int, int], ...] | None = None,
    progress: Callable[[int, int], None] | None = None,
) -> BatchedRegressionPredictions:
    """Apply ONE retained state; complete corpus, one batch/one query intermediate.

    Explicit optional progress callbacks perform only caller-requested observation;
    they supply no fitting/prediction authority. Whole-population metrics follow
    complete original-row reassembly, never an average of batch metrics.
    """
    ranges = regression_batch_ranges(state, inputs, specification, ranges=ranges)
    prediction = state._predict_ranges(
        inputs,
        ranges,
        larger=True,
        work_limit=specification.maximum_distance_operations,
        progress=progress,
    )
    identity = prediction.content_identity
    batches = tuple(
        (
            RegressionPredictionBatch(
                start,
                stop,
                inputs.row_ids[start:stop],
                _hash(
                    (
                        identity,
                        start,
                        stop,
                        prediction.values[start:stop],
                        None
                        if prediction.neighbor_row_ids is None
                        else prediction.neighbor_row_ids[start:stop],
                        None
                        if prediction.neighbor_distances is None
                        else prediction.neighbor_distances[start:stop],
                    ),
                ),
            )
            for start, stop in ranges
        ),
    )
    return BatchedRegressionPredictions(
        prediction,
        RegressionBatchEvidence(
            specification,
            state.content_identity,
            inputs.content_identity,
            identity,
            batches,
        ),
    )


def verify_regression_batches(
    state: FittedRegression,
    inputs: RegressionInput,
    result: BatchedRegressionPredictions,
) -> None:
    """Reconstruct complete arithmetic; a saved digest is never a verified flag."""
    actual = predict_regression_batches(
        state,
        inputs,
        result.evidence.specification,
        ranges=tuple((b.start, b.stop) for b in result.evidence.batches),
    )
    if asdict(actual) != asdict(result):
        msg = "original source/state/batch arithmetic differs"
        raise ValueError(msg)
