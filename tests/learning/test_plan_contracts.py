# Copyright (c) 2026
"""Effect-free source, role, metric and work admission over authored inputs."""

from __future__ import annotations

import json
from dataclasses import replace
from typing import TYPE_CHECKING, Any, cast

import pytest

from devtools.learning.investigation.plans import (
    MAX_REQUEST_BYTES,
    LearningPlan,
    binary_problem,
    canonical,
)
from tests.learning.fixtures import authored_task

if TYPE_CHECKING:
    from collections.abc import Callable


def _plan(family: str) -> LearningPlan:
    return authored_task(family).plan(
        "knn7" if family == "classification" else "mean",
        "online",
        "plan-contract-control",
    )


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("task_identity", ""),
        ("invocation_identity", ""),
        ("family", "clustering"),
        ("method", "histogram"),
        ("phase", "training"),
        ("metric", "regression.mae:v1"),
        ("problem_json", "[]"),
        ("source_json", "[]"),
    ],
)
def test_unadmitted_plan_cannot_produce_execution_authority(
    field: str,
    bad: str,
) -> None:
    """Invalid family, metric and source shape refuse before any worker is created."""
    reconstruct = cast("Callable[..., LearningPlan]", replace)
    with pytest.raises(ValueError, match=r"nonempty|unsupported|incompatible|object"):
        reconstruct(_plan("classification"), **{field: bad})


@pytest.mark.parametrize("family", ["classification", "regression"])
def test_foreign_source_refuses_even_with_valid_populations(family: str) -> None:
    """A source identity is not repaired by compatible numeric rows."""
    plan = _plan(family)
    source = json.loads(plan.source_json)
    source["source_identity"] = "foreign-source"
    with pytest.raises(ValueError, match=r"foreign binary source|source/schema"):
        replace(plan, source_json=canonical(source))


def test_request_and_retained_state_envelopes_refuse_before_decoding() -> None:
    """The packet and derived state limits are separate finite admission contracts."""
    plan = _plan("classification")
    with pytest.raises(ValueError, match="frozen input bound"):
        replace(plan, problem_json="x" * (MAX_REQUEST_BYTES + 1))
    source = json.loads(plan.source_json)
    source["authored_oversized_metadata"] = "x" * (700 << 10)
    with pytest.raises(ValueError, match="retained-state envelope"):
        replace(plan, source_json=canonical(source))


@pytest.mark.parametrize(
    "fault",
    [
        "problem-fields",
        "training-fields",
        "schema",
        "role-overlap",
        "population",
        "empty-target",
        "foreign-category",
    ],
)
def test_binary_source_membership_and_target_contracts(fault: str) -> None:
    """Original category meaning and disjoint held rows precede fit permission."""
    data = json.loads(_plan("classification").problem_json)
    if fault == "problem-fields":
        data["extra"] = "foreign"
    elif fault == "training-fields":
        data["training"]["extra"] = "foreign"
    elif fault == "schema":
        data["evaluation_features"]["feature_names"] = ["foreign", "constant"]
    elif fault == "role-overlap":
        data["evaluation_row_ids"][0] = data["training"]["row_ids"][0]
    elif fault == "population":
        data["evaluation_population_id"] = data["training"]["population_id"]
    elif fault == "empty-target":
        data["evaluation_targets"] = []
    else:
        data["evaluation_targets"][0] = 2
    with pytest.raises(
        ValueError,
        match=r"unsupported binary|exact original binary|aligned disjoint",
    ):
        binary_problem(data)


@pytest.mark.parametrize(
    ("path", "bad"),
    [
        ("training.inputs.role", "development"),
        ("evaluation.inputs.role", "training"),
        ("evaluation.inputs.feature_units", ["foreign-unit", None]),
        ("evaluation.target.unit", "foreign-target-unit"),
        ("evaluation.inputs.source_identity", "foreign-source"),
        ("evaluation.inputs.row_ids", ["r0", "r1"]),
        ("evaluation.inputs.population_id", "training"),
    ],
)
def test_regression_source_role_and_unit_correspondence(path: str, bad: object) -> None:
    """Typed quantities still require exact training and evaluation correspondence."""
    plan = _plan("regression")
    data = json.loads(plan.problem_json)
    target: Any = data
    parts = path.split(".")
    for part in parts[:-1]:
        target = target[part]
    target[parts[-1]] = bad
    with pytest.raises(ValueError, match="source/schema/unit/target/role"):
        replace(plan, problem_json=canonical(data))


def test_empty_training_refuses_before_native_mean_fitting() -> None:
    """A syntactically typed empty source is not an admitted fitting population."""
    plan = _plan("regression")
    data = json.loads(plan.problem_json)
    data["training"]["inputs"]["features"]["rows"] = []
    data["training"]["inputs"]["row_ids"] = []
    data["training"]["values"] = []
    with pytest.raises(ValueError, match="population/cell bounds"):
        replace(plan, problem_json=canonical(data))


def _binary_work_input(count: int, dimension: int) -> dict[str, Any]:
    """Create only authored JSON declarations; this helper never executes a fit."""
    data: dict[str, Any] = json.loads(_plan("classification").problem_json)
    names = ["x" + str(i) for i in range(dimension)]
    features = {
        "feature_names": names,
        "feature_value_kinds": ["continuous"] * dimension,
        "rows": [[float(i)] * dimension for i in range(count)],
    }
    data["training"]["features"] = features
    data["training"]["targets"] = [i % 2 for i in range(count)]
    data["training"]["row_ids"] = ["fitting-" + str(i) for i in range(count)]
    data["evaluation_features"] = features
    data["evaluation_targets"] = [i % 2 for i in range(count)]
    data["evaluation_row_ids"] = ["held-" + str(i) for i in range(count)]
    return data


@pytest.mark.parametrize(
    ("count", "dimension", "reason"),
    [
        (6, 2, "seven original training rows"),
        (8, 129, "population/cell bounds"),
        (500, 32, "neighbor inspection work"),
    ],
)
def test_population_and_distance_work_bounds_precede_effects(
    count: int,
    dimension: int,
    reason: str,
) -> None:
    """Bound numerical work before native construction, without exercising that work."""
    with pytest.raises(ValueError, match=reason):
        replace(
            _plan("classification"),
            problem_json=canonical(_binary_work_input(count, dimension)),
        )


def test_quantitative_problem_decoder_refuses_extra_fields() -> None:
    """Closed original populations cannot acquire invented side-channel fields."""
    plan = _plan("regression")
    value = json.loads(plan.problem_json)
    value["unadmitted"] = True
    with pytest.raises(ValueError, match="problem fields"):
        replace(plan, problem_json=canonical(value))


def test_quantitative_admission_rejects_wrong_decoder_component_family(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Simulate a decoder fault before any grant, observation or fitting effect."""
    plan = _plan("regression")
    wrong = _plan("classification").populations()
    monkeypatch.setattr(LearningPlan, "populations", lambda _: wrong)
    with pytest.raises(TypeError, match="typed quantitative"):
        replace(plan)
