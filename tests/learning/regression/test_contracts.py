# Copyright (c) 2026
"""Source identity, quantity, role, version and complete-row numerical semantics."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING, cast
from uuid import uuid4

import pytest

from devtools.learning.evaluation.regression.metrics import evaluate_regression
from devtools.learning.measurement.contracts import Measured, NoValue
from devtools.learning.regression.contracts import (
    RegressionMethod,
    RegressionPopulation,
    RegressionRole,
    RegressionSpecification,
)
from devtools.learning.regression.limits import (
    REGRESSION_V2,
    check_text,
    version_limits,
)
from devtools.learning.regression.state import RegressionPredictions
from devtools.learning.representation.observations import PopulationScope
from tests.learning.fixtures import authored_task

if TYPE_CHECKING:
    from collections.abc import Callable


def _population() -> RegressionPopulation:
    training, _ = (
        authored_task("regression")
        .plan("mean", "online", "contract-control")
        .populations()
    )
    assert isinstance(training, RegressionPopulation)
    return training


@pytest.mark.parametrize(
    ("owner", "field", "bad"),
    [
        ("target", "kind", "encoded-category"),
        ("target", "version", "foreign"),
        ("target", "unit", ""),
        ("inputs", "features", None),
        ("inputs", "role", "training"),
        ("inputs", "row_ids", []),
        ("inputs", "row_ids", ()),
        ("inputs", "row_ids", ("duplicate",) * 8),
        ("inputs", "feature_units", []),
        ("inputs", "feature_units", ()),
        ("inputs", "source_identity", ""),
        ("inputs", "version", "foreign"),
        ("population", "inputs", None),
        ("population", "target", None),
        ("population", "values", []),
        ("population", "values", ()),
        ("population", "values", (1,) * 8),
        ("population", "values", (float("nan"),) * 8),
        ("population", "missing_policy", "impute"),
        ("population", "version", "regression-population-v1"),
    ],
)
def test_unadmitted_regression_semantics_cannot_be_coerced(
    owner: str,
    field: str,
    bad: object,
) -> None:
    """A numeric container does not establish source role, quantity or valid rows."""
    population = _population()
    value: object = {
        "population": population,
        "inputs": population.inputs,
        "target": population.target,
    }[owner]
    reconstruct = cast("Callable[..., object]", replace)
    with pytest.raises((ValueError, TypeError)):
        reconstruct(value, **{field: bad})


def test_explicit_units_roles_and_specification_versions_remain_distinct() -> None:
    """Preserve unknown units without inventing conversions or category semantics."""
    population = _population()
    units = ("authored-unit",) * len(population.inputs.feature_units)
    inputs = replace(population.inputs, feature_units=units)
    assert inputs.schema_identity != population.inputs.schema_identity
    assert inputs.content_identity != population.inputs.content_identity
    assert replace(population.target, unit=None).unit is None
    assert tuple(role.scope for role in RegressionRole) == (
        PopulationScope.TRAINING,
        PopulationScope.VALIDATION,
        PopulationScope.TEST,
    )
    for index, method in enumerate(RegressionMethod):
        specification = RegressionSpecification(method)
        assert specification.complexity == index
        assert specification.configuration
        assert specification.identity
    with pytest.raises(TypeError, match="concrete regression method"):
        RegressionSpecification(cast("RegressionMethod", "mean"))
    with pytest.raises(ValueError, match="unsupported regression specification"):
        RegressionSpecification(RegressionMethod.MEAN, "regression-specification-v2")
    assert (
        RegressionSpecification(RegressionMethod.KNN).configuration
        != RegressionSpecification(
            RegressionMethod.KNN,
            "regression-specification-v2",
        ).configuration
    )


def test_capacity_text_bounds_apply_to_all_original_v2_identities() -> None:
    """Reject oversized retained identity text before creating a state or native fit."""
    population = _population()
    oversized = "x" * (REGRESSION_V2.text_bytes + 1)
    with pytest.raises(ValueError, match="bounded regression identity"):
        replace(
            population.inputs,
            version="regression-input-v2",
            source_identity=oversized,
        )
    v2 = replace(population.inputs, version="regression-input-v2")
    with pytest.raises(ValueError, match="bounded regression identity"):
        replace(
            population,
            inputs=v2,
            version="regression-population-v2",
            target=replace(population.target, quantity=oversized),
        )
    assert version_limits("authored-v2", "authored") is REGRESSION_V2
    check_text((None, "authored"))


def _predictions(
    population: RegressionPopulation,
    values: tuple[float, ...],
) -> RegressionPredictions:
    return RegressionPredictions(
        uuid4(),
        "authored-method",
        population.inputs.content_identity,
        population.inputs.population_id,
        population.inputs.row_ids,
        population.target,
        values,
    )


@pytest.mark.parametrize(
    ("targets", "predicted"),
    [
        ((1.0, 2.0), (1e200, 1e200)),
        ((1e200, -1e200), (1e200, -1e200)),
        ((1e308, -1e308), (-1e308, 1e308)),
    ],
)
def test_unrepresentable_measurements_keep_the_original_denominator(
    targets: tuple[float, ...],
    predicted: tuple[float, ...],
) -> None:
    """Overflow is an explicit nonvalue; no row dropping or forced R2 convention."""
    original = _population()
    inputs = replace(
        original.inputs,
        features=replace(
            original.inputs.features,
            rows=original.inputs.features.rows[:2],
        ),
        row_ids=original.inputs.row_ids[:2],
    )
    population = replace(original, inputs=inputs, values=targets)
    evaluated = evaluate_regression(population, _predictions(population, predicted))
    assert evaluated.row_ids == population.inputs.row_ids
    assert evaluated.target == population.target
    assert isinstance(evaluated.r2, NoValue)
    assert evaluated.r2.reason_code == "unrepresentable_regression_arithmetic"
    assert isinstance(evaluated.mae, (Measured, NoValue))


def test_measurement_rejects_foreign_or_reordered_predicted_population() -> None:
    """Scientific arithmetic cannot hide a source, target-unit or row-order mismatch."""
    population = _population()
    predicted = _predictions(population, population.values)
    with pytest.raises(ValueError, match="original row order"):
        evaluate_regression(
            population,
            replace(predicted, row_ids=tuple(reversed(predicted.row_ids))),
        )
    with pytest.raises(TypeError, match="typed original regression"):
        evaluate_regression(cast("RegressionPopulation", None), predicted)
