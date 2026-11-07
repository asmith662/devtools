# Copyright (c) 2026
"""Scientific effect and publication boundaries under explicit component faults."""

from __future__ import annotations

import importlib.util
from dataclasses import replace
from importlib import import_module
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, cast

import pytest

from devtools.learning.evidence.context import ExecutionContext
from devtools.learning.evidence.events import Admitted
from devtools.learning.integrations.local import operations
from devtools.learning.integrations.local.operations import (
    _binary_predictions,
    _publish_result,
    _Recorder,
    _regression_predictions,
    correspondence,
    execute_plan,
    knn7_predict,
    quality,
)
from devtools.learning.investigation.classification.contracts import (
    ExecutionAuthorization,
)
from devtools.learning.investigation.errors import LearningUnavailableError
from devtools.learning.investigation.plans import LearningPlan
from devtools.learning.measurement.contracts import EvidenceReference
from tests.learning.fixtures import authored_task

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.learning.integrations.local.publication import PublicationInspection


def _grant(plan: LearningPlan) -> ExecutionAuthorization:
    return ExecutionAuthorization(
        plan.identity,
        (plan.method,),
        EvidenceReference("learning_execution_grant-v1", "unit", plan.identity),
    )


@pytest.mark.parametrize("reservation", [None, -1, 33 << 20, True])
def test_invalid_scientific_storage_reservation_refuses(
    tmp_path: Path,
    reservation: int | None,
) -> None:
    """No unbounded or negative reservation can authorize publication."""
    with _Recorder(tmp_path / "science.sqlite") as recorder:
        with pytest.raises(ValueError, match="publication bound"):
            recorder.reserve_publication(reservation)
        recorder.reserve_publication(0)
        with pytest.raises(ValueError, match="publication bound"):
            recorder.reserve_publication(0)


def test_publication_byte_ceiling_refuses_before_artifact_writes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The raw serialized member bound is checked separately from reservations."""
    plan = authored_task("regression").plan("mean", "online", "storage-control")
    monkeypatch.setattr(operations, "MAX_PUBLICATION_BYTES", 1)
    with (
        _Recorder(tmp_path / "science.sqlite") as recorder,
        pytest.raises(ValueError, match="retained scientific state"),
        ExecutionContext(recorder, Admitted("storage-control")) as run,
    ):
        _publish_result(tmp_path, {"state": "authored"}, plan, recorder, run)
    assert not (tmp_path / "publication").exists()


def test_prediction_dispatch_and_metric_family_refusals() -> None:
    """Wrong model, schema and metric families cannot become finite observations."""
    binary = authored_task("classification").plan("knn7", "online", "dispatch-control")
    quantitative = authored_task("regression").plan(
        "knn-v2",
        "online",
        "dispatch-control",
    )
    training, _held = binary.populations()
    typed = cast("Any", training)
    features = typed.features
    with pytest.raises(ValueError, match="schema"):
        knn7_predict(typed, replace(features, feature_names=("wrong", "constant")))
    with pytest.raises(TypeError, match="binary predictions"):
        quality(binary, cast("Any", None))
    with pytest.raises(TypeError, match="quantitative predictions"):
        quality(quantitative, (0, 1))
    with pytest.raises(TypeError, match="deterministic regression state"):
        correspondence(quantitative, None, None)
    with pytest.raises(TypeError, match="retained binary state"):
        _binary_predictions(None, typed, None, features)
    with pytest.raises(TypeError, match="native regression fit"):
        _regression_predictions(None, cast("Any", None))
    wrong = SimpleNamespace(
        classify=lambda _: tuple(1 - x for x in knn7_predict(typed, features)),
    )
    with pytest.raises(ValueError, match="kNN prediction disagreement"):
        _binary_predictions(None, typed, cast("Any", wrong), features)


def test_unavailable_numerics_refuse_before_operation_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Optional dependencies remain unavailable observations, with zero effects."""
    plan = authored_task("regression").plan("mean", "online", "dependency-control")
    monkeypatch.setattr(importlib.util, "find_spec", lambda _: None)
    with pytest.raises(LearningUnavailableError, match="unavailable"):
        execute_plan(plan, _grant(plan), tmp_path / "operation")
    assert not tuple(tmp_path.iterdir())


def test_wrong_held_component_refuses_before_any_native_fit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Simulate a corrupted population decoder return after exact plan admission."""
    plan = authored_task("classification").plan("knn7", "online", "source-control")
    training, _ = plan.populations()
    _, held = (
        authored_task("regression")
        .plan("mean", "online", "source-control")
        .populations()
    )
    monkeypatch.setattr(LearningPlan, "populations", lambda _: (training, held))
    with (
        import_module("threadpoolctl").threadpool_limits(limits=1),
        pytest.raises(TypeError, match="binary held population"),
    ):
        execute_plan(plan, _grant(plan), tmp_path / "operation")


def test_publication_component_cannot_return_missing_manifest_as_success(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Refuse a simulated bad return after genuine Mean arithmetic and publication."""
    plan = authored_task("regression").plan("mean", "online", "publication-control")

    def reported(
        root: Path,
        result: dict[str, object],
        plan: LearningPlan,
        recorder: _Recorder,
        run: ExecutionContext,
    ) -> PublicationInspection:
        return replace(
            _publish_result(root, result, plan, recorder, run),
            manifest=None,
        )

    monkeypatch.setattr(operations, "_publish_result", reported)
    with (
        import_module("threadpoolctl").threadpool_limits(limits=1),
        pytest.raises(ValueError, match="did not retain a manifest"),
    ):
        execute_plan(plan, _grant(plan), tmp_path / "operation")
    assert tuple((tmp_path / "operation/publication/generations").glob("*/result.json"))
