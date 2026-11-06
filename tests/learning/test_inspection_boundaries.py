# Copyright (c) 2026
"""Independent reader fault controls over genuinely fitted owned evidence."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from datetime import timedelta
from typing import TYPE_CHECKING, Any, cast
from uuid import UUID, uuid4

import pytest

from devtools.learning.classification.linear import BinaryLinearTraining
from devtools.learning.evidence.events import Admitted, Fact, Terminal
from devtools.learning.integrations.local import inspection
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
from devtools.learning.integrations.local.ledger import (
    inspect_child_execution_ids,
    inspect_execution,
)
from devtools.learning.integrations.local.linear_classification import model_document
from devtools.learning.integrations.local.operations import LearningPublication, quality
from devtools.learning.investigation.classification.contracts import (
    ExecutionAuthorization,
)
from devtools.learning.investigation.plans import BinaryProblem
from devtools.learning.measurement.contracts import EvidenceReference, Measured
from devtools.learning.regression.contracts import RegressionInput, RegressionPopulation
from devtools.learning.regression.state import RegressionPredictions
from devtools.resources.filesystem import BinaryFile, TextFile
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


@pytest.mark.parametrize("fault", ["format", "schema"])
def test_scientific_reader_refuses_wrong_filesystem_component_return(
    witness: Callable[[str], Witness],
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
) -> None:
    """Original publication is intact; the explicit filesystem return is faulty."""
    inspected, grant, _, saved = witness("mean")
    path = inspected.reference.root
    if fault == "format":
        returned: BinaryFile | TextFile = TextFile(path, "authored format fault")
    else:
        returned = BinaryFile(
            path,
            json.dumps(dict(saved, schema="learning-operation-v1")).encode(),
        )
    monkeypatch.setattr(inspection, "read", lambda *_args, **_kwargs: returned)
    with pytest.raises(
        (TypeError, ValueError),
        match=r"binary scientific|schema/plan/grant",
    ):
        inspect_learning(inspected.reference, inspected.plan, grant)


def test_independent_observation_family_and_fitted_type_guards(
    witness: Callable[[str], Witness],
) -> None:
    """Actual fitted witnesses cannot substitute across source and state families."""
    binary = witness("knn7")[0]
    regression = witness("mean")[0]
    _, held = binary.plan.populations()
    assert isinstance(held, BinaryProblem)
    labels = binary.predict(held.features)
    assert isinstance(labels, tuple)
    with pytest.raises(TypeError, match="binary source populations"):
        _verify_binary_observation(regression, labels, binary.quality)
    with pytest.raises(TypeError, match="binary fitted state"):
        _verify_binary_observation(
            replace(binary, state=regression.state),
            labels,
            binary.quality,
        )
    with pytest.raises(TypeError, match="quantitative fitted state"):
        _verify_regression_observation(binary, cast("Any", None), binary.quality)
    with pytest.raises(TypeError, match="quantitative source populations"):
        _verify_regression_observation(
            replace(binary, state=regression.state),
            cast("Any", None),
            binary.quality,
        )


@pytest.mark.parametrize(
    "fault",
    ["producer-kind", "fit-ack", "children", "preparation-ack"],
)
def test_independent_reader_component_faults_cannot_certify_custody(
    witness: Callable[[str], Witness],
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
) -> None:
    """Inject named reader-report faults over unchanged genuine histories."""
    inspected, grant, manifest, original_saved = witness(
        "ridge" if fault == "preparation-ack" else "knn7",
    )
    saved = _saved((inspected, grant, manifest, original_saved))
    database = inspected.reference.root.value / "science.sqlite"
    fitting_id = UUID(saved["fitting_execution_id"])
    producer_id = UUID(saved["producing_execution_id"])
    preparation_id = UUID(saved["preparation"]["construction_execution_id"])
    fit = inspect_execution(database, fitting_id)
    assert fit is not None

    def reported(path: Path, identity: UUID) -> object:
        history = inspect_execution(path, identity)
        if history is None:
            return None
        last = history.events[-1]
        if fault == "producer-kind" and identity == producer_id:
            last = replace(last, payload=Admitted("faulty-reader-return"))
        elif fault == "fit-ack" and identity == fitting_id:
            assert isinstance(last.payload, Terminal)
            last = replace(
                last,
                payload=replace(
                    last.payload,
                    facts=(Fact("state_identity", "0" * 64),),
                ),
            )
        elif fault == "preparation-ack" and identity == preparation_id:
            last = replace(
                last,
                observed_at=fit.events[0].occurred_at + timedelta(seconds=1),
            )
        return replace(history, events=(*history.events[:-1], last))

    if fault == "children":
        original = inspect_child_execution_ids
        monkeypatch.setattr(
            inspection,
            "inspect_child_execution_ids",
            lambda *args: (*original(*args), uuid4()),
        )
    else:
        monkeypatch.setattr(inspection, "inspect_execution", reported)
    with pytest.raises(
        (TypeError, ValueError),
        match=(
            r"acknowledgments absent|before fitting|child executions|"
            r"binary fit acknowledgment"
        ),
    ):
        inspect_learning(inspected.reference, inspected.plan, grant)
