# Copyright (c) 2026
"""Independent reader fault controls over genuinely fitted owned evidence."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import TYPE_CHECKING, Any, cast
from uuid import UUID, uuid4

import pytest

from devtools.learning.classification.linear import BinaryLinearTraining
from devtools.learning.integrations.local.inspection import (
    InspectedLearning,
    _binary_state,
    _execution_order,
    _fitting,
    _independent_f1,
    _load,
    _preparation,
    _producer,
    _regression_state,
    _verify_binary_observation,
    _verify_observation,
    _verify_regression_observation,
    inspect_learning,
)
from devtools.learning.integrations.local.ledger import inspect_execution
from devtools.learning.integrations.local.linear_classification import model_document
from devtools.learning.integrations.local.operations import LearningPublication, quality
from devtools.learning.investigation.classification.contracts import (
    ExecutionAuthorization,
)
from devtools.learning.investigation.plans import BinaryProblem
from devtools.learning.measurement.contracts import EvidenceReference, Measured
from devtools.learning.regression.contracts import RegressionInput, RegressionPopulation
from devtools.learning.regression.state import RegressionPredictions
from devtools.tools.learning import ManagedLearningWorker
from tests.learning.fixtures import authored_task

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from devtools.learning.evidence.publication import PublicationManifest
    from devtools.learning.representation.features import FeatureTable

type Witness = tuple[
    InspectedLearning,
    ExecutionAuthorization,
    PublicationManifest,
    dict[str, Any],
]


@pytest.fixture(scope="module")
def witness(tmp_path_factory: pytest.TempPathFactory) -> Callable[[str], Witness]:
    """Each engineering witness is fitted once, lazily under active measurement."""
    root = tmp_path_factory.mktemp("inspection-controls")
    cache: dict[str, Witness] = {}

    def get(method: str) -> Witness:
        if method not in cache:
            family = "regression" if method in {"mean", "ridge"} else "classification"
            plan = authored_task(family).plan(method, "online", "inspection-control")
            grant = ExecutionAuthorization(
                plan.identity,
                (method,),
                EvidenceReference("learning_execution_grant-v1", "unit", plan.identity),
            )
            reference = asyncio.run(
                ManagedLearningWorker.current().execute(plan, grant, root / method),
            )
            inspected = inspect_learning(reference, plan, grant)
            manifest, saved = _load(reference, plan, grant)
            cache[method] = inspected, grant, manifest, cast("dict[str, Any]", saved)
        return cache[method]

    return get


def _saved(value: Witness) -> dict[str, Any]:
    return cast("dict[str, Any]", json.loads(json.dumps(value[-1])))


@pytest.mark.parametrize(
    ("truth", "predicted", "expected"),
    [
        ((0, 1), (0, 1), 1.0),
        ((0, 1), (1, 0), None),
        ((0, 0), (0, 0), 1.0),
        ((0, 1), (0, 0), None),
    ],
)
def test_independent_legacy_f1_retains_denominator_meaning(
    truth: tuple[int, ...],
    predicted: tuple[int, ...],
    expected: float | None,
) -> None:
    """Version-one undefined denominators remain unavailable, including zero F1."""
    assert _independent_f1(truth, predicted, 1) == expected


def test_label_free_consumer_refuses_missing_state_and_wrong_family_inputs(
    witness: Callable[[str], Witness],
) -> None:
    """A successful inspection does not authorize another family of inputs."""
    inspected, _, _, _ = witness("mean")
    _, held = inspected.plan.populations()
    assert isinstance(held, RegressionPopulation)
    with pytest.raises(TypeError, match="regression inputs"):
        inspected.predict(cast("FeatureTable", held))
    empty = replace(inspected, state=None)
    assert isinstance(held.inputs, RegressionInput)
    with pytest.raises(TypeError, match="binary feature"):
        empty.predict(held.inputs)
    with pytest.raises(TypeError, match="fitted state"):
        empty.predict(held.inputs.features)


def test_foreign_reference_and_absent_publication_refuse_without_execution(
    witness: Callable[[str], Witness],
    tmp_path: Path,
) -> None:
    """Reference identities and original publication remain independently required."""
    inspected, grant, _, _ = witness("mean")
    with pytest.raises(ValueError, match="foreign scientific"):
        inspect_learning(
            replace(inspected.reference, plan_identity="foreign"),
            inspected.plan,
            grant,
        )
    absent = LearningPublication(
        inspected.reference.root,
        "missing",
        "0" * 64,
        inspected.plan.identity,
    )
    with pytest.raises(ValueError, match="missing, changed"):
        inspect_learning(absent, inspected.plan, grant)
    assert not tuple(tmp_path.iterdir())


@pytest.mark.parametrize(
    "fault",
    ["producer", "grant", "prediction", "publisher", "fit"],
)
def test_original_occurrence_and_ack_boundaries(
    witness: Callable[[str], Witness],
    fault: str,
) -> None:
    """Actual original histories cannot be replaced by foreign occurrence claims."""
    value = witness("mean")
    inspected, grant, manifest, _ = value
    saved = _saved(value)
    database = inspected.reference.root.value / "science.sqlite"
    history = _producer(saved, database, manifest, inspected.plan, grant)
    predict, _, _ = _execution_order(history, manifest, database)
    if fault == "producer":
        saved["producing_execution_id"] = str(uuid4())
        with pytest.raises(ValueError, match="completed original"):
            _producer(saved, database, manifest, inspected.plan, grant)
    elif fault == "grant":
        saved["runtime"] = {"invented": True}
        with pytest.raises(ValueError, match="grant/state correspondence"):
            _producer(saved, database, manifest, inspected.plan, grant)
    elif fault == "prediction":
        with pytest.raises(ValueError, match="before measurement"):
            _execution_order(replace(history, execution_id=uuid4()), manifest, database)
    elif fault == "publisher":
        with pytest.raises(ValueError, match="causally reordered"):
            _execution_order(
                history,
                replace(manifest, publication_execution_id=None),
                database,
            )
    else:
        saved["fitting_execution_id"] = str(uuid4())
        with pytest.raises(ValueError, match="before prediction"):
            _fitting(saved, database, history, predict)


@pytest.mark.parametrize("fault", ["missing", "source", "occurrence", "arithmetic"])
def test_preparation_requires_original_source_ack_and_statistics(
    witness: Callable[[str], Witness],
    fault: str,
) -> None:
    """Retained preparation copies cannot invent original statistics or custody."""
    value = witness("ridge")
    inspected, _, _, _ = value
    saved = _saved(value)
    database = inspected.reference.root.value / "science.sqlite"
    original_fit = inspect_execution(database, UUID(saved["fitting_execution_id"]))
    assert original_fit is not None
    if fault == "missing":
        saved["preparation"] = None
    elif fault == "source":
        saved["preparation"]["source_identity"] = "foreign"
    elif fault == "occurrence":
        saved["preparation"]["construction_execution_id"] = str(uuid4())
    else:
        saved["preparation"]["training_means"][0] += 1.0
    with pytest.raises(ValueError, match="preparation"):
        _preparation(saved, inspected.plan, database, original_fit)
    if fault == "source":
        mean_value = witness("mean")
        altered = _saved(mean_value)
        altered["preparation"] = _saved(value)["preparation"]
        with pytest.raises(ValueError, match="must not silently prepare"):
            _preparation(altered, mean_value[0].plan, database, original_fit)


@pytest.mark.parametrize("fault", ["method", "state-ack"])
def test_regression_fit_requires_exact_method_and_state_ack(
    witness: Callable[[str], Witness],
    fault: str,
) -> None:
    """Original retained state arithmetic does not substitute for its fit ACK."""
    value = witness("mean")
    inspected, _, _, _ = value
    saved = _saved(value)
    database = inspected.reference.root.value / "science.sqlite"
    fit = inspect_execution(database, UUID(saved["fitting_execution_id"]))
    assert fit is not None
    training, _ = inspected.plan.populations()
    if fault == "method":
        saved["state"]["execution_id"] = str(uuid4())
    else:
        saved["state"]["backend"].append(["corruption-control", "authored"])
    with pytest.raises(ValueError, match=r"granted plan|acknowledgment differs"):
        _regression_state(cast("Any", training), inspected.plan, saved, database, fit)


@pytest.mark.parametrize("method", ["knn7", "square-logistic"])
@pytest.mark.parametrize("fault", ["source", "configuration"])
def test_binary_state_requires_exact_source_and_configuration(
    witness: Callable[[str], Witness],
    method: str,
    fault: str,
) -> None:
    """Valid retained encodings still require exact scientific correspondence."""
    value = witness(method)
    inspected, _, _, _ = value
    saved = _saved(value)
    training, _ = inspected.plan.populations()
    assert isinstance(training, BinaryLinearTraining)
    if method == "knn7":
        saved["state"]["training"]["source_identity"] = "invented"
    else:
        state = cast("Any", inspected.state)
        altered = (
            replace(state, target_identity="foreign")
            if fault == "source"
            else replace(state, configuration=(("invented", "configuration"),))
        )
        saved["state"] = model_document(altered)
    with pytest.raises(ValueError, match=r"source|configuration"):
        _binary_state(
            training,
            inspected.preparation,
            inspected.plan,
            saved,
            UUID(saved["fitting_execution_id"]),
        )


@pytest.mark.parametrize("fault", ["predictions", "quality", "parity", "arithmetic"])
def test_regression_observation_requires_independent_arithmetic(
    witness: Callable[[str], Witness],
    fault: str,
) -> None:
    """Original fit acceptance cannot certify corrupted result or metric claims."""
    value = witness("mean")
    inspected, _, _, _ = value
    saved = _saved(value)
    _, held = inspected.plan.populations()
    assert isinstance(held, RegressionPopulation)
    predictions = inspected.predict(held.inputs)
    assert isinstance(predictions, RegressionPredictions)
    if fault == "arithmetic":
        changed = replace(predictions, values=tuple(x + 1 for x in predictions.values))
        with pytest.raises(ValueError, match="prediction arithmetic"):
            _verify_regression_observation(inspected, changed, inspected.quality)
        with pytest.raises(ValueError, match="MAE arithmetic"):
            _verify_regression_observation(inspected, predictions, Measured(1000.0))
    else:
        saved["native_correspondence" if fault == "parity" else fault] = "corrupted"
        with pytest.raises(ValueError, match=r"parity scope|evidence differs"):
            _verify_observation(inspected, saved)


def test_binary_observation_recounts_votes_features_and_f1(
    witness: Callable[[str], Witness],
) -> None:
    """Recomputed votes and F1 refuse plausible but false finite observations."""
    inspected, _, _, _ = witness("knn7")
    _, held = inspected.plan.populations()
    assert isinstance(held, BinaryProblem)
    predictions = inspected.predict(held.features)
    assert isinstance(predictions, tuple)
    measured, _ = quality(inspected.plan, predictions)
    changed = tuple(1 - label for label in predictions)
    with pytest.raises(ValueError, match="prediction arithmetic"):
        _verify_binary_observation(inspected, changed, measured)
    with pytest.raises(ValueError, match="F1 counts"):
        _verify_binary_observation(inspected, predictions, Measured(-1.0))
    with pytest.raises(ValueError, match="feature construction"):
        _verify_binary_observation(
            replace(inspected, binary_training=None),
            predictions,
            measured,
        )
