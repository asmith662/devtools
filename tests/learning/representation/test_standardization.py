# Copyright (c) 2026
# Adapted independent contracts from donor
# e069092e9b83c349ddb4efee09a3b1891ea0ad63.
"""Independent population-statistic fixtures and managed representation invariants."""

from __future__ import annotations

import dataclasses
import math
import sqlite3
import sys
from dataclasses import replace
from fractions import Fraction
from typing import TYPE_CHECKING, Never, cast
from uuid import UUID

import pytest

from devtools.learning.evidence.context import ExecutionContext, RecordingError
from devtools.learning.evidence.events import (
    Admitted,
    Diagnostic,
    ExecutionEvent,
    Outcome,
    StageStarted,
)
from devtools.learning.integrations.local.ledger import (
    SQLiteExecutionRecorder,
    inspect_execution,
)
from devtools.learning.representation.features import FeatureTable, FeatureValueKind
from devtools.learning.representation.observations import PopulationScope
from devtools.learning.representation.standardization import (
    FeatureStandardizationSpecification,
    fit_feature_standardization,
)

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path
HUGE_DEVIATION = 1e308
FIT_EVENT_LIMIT = 20
APPLY_EVENT_LIMIT = 15


def _table(
    values: Sequence[float | Sequence[float]],
    names: tuple[str, ...] = ("x",),
    kinds: tuple[FeatureValueKind, ...] | None = None,
) -> FeatureTable:
    """Construct independently authored typed feature rows."""
    return FeatureTable(
        names,
        tuple(
            (float(cast("float", v)),)
            if len(names) == 1
            else tuple(cast("Sequence[float]", v))
            for v in values
        ),
        kinds or (FeatureValueKind.CONTINUOUS,) * len(names),
    )


def test_independent_known_population_statistics_and_fixed_application() -> None:
    """Independent known population statistics and fixed application."""
    features = _table((1, 2, 3, 4))
    state = fit_feature_standardization(
        FeatureStandardizationSpecification(("x",)),
        features,
        population_id="training",
    )
    assert state.training_means == (2.5,)
    assert state.training_standard_deviations == (math.sqrt(1.25),)
    result = state.transform(_table((5, -1)))
    assert result.features.rows == ((2.5 / math.sqrt(1.25),), (-3.5 / math.sqrt(1.25),))
    assert state.training_standard_deviations != (math.sqrt(5 / 3),)
    assert result.fitted_state_id == state.state_id
    assert result.execution_id != state.construction_execution_id
    assert state.variance_convention == "population_n"
    assert not hasattr(state, "rows")


@pytest.mark.parametrize("values", [(7,), (7, 7, 7), (0, 0)])
def test_exact_constants_and_later_only_variation(values: tuple[int, ...]) -> None:
    """Exact constants and later only variation."""
    state = fit_feature_standardization(
        FeatureStandardizationSpecification(("x",)),
        _table(values),
        population_id="training",
    )
    assert state.training_standard_deviations == (0.0,)
    assert state.effective_scales == (1.0,)
    assert state.constant_coordinates == (True,)
    assert all(row == (0.0,) for row in state.transform(_table(values)).features.rows)
    assert state.transform(_table((values[0] + 2,))).features.rows == ((2.0,),)


@pytest.mark.parametrize("offset", [1000000000000.0, 1000000000000000.0])
def test_large_offset_small_spread(offset: float) -> None:
    """Large offset small spread."""
    values = (offset + 1, offset + 2, offset + 3, offset + 4)
    state = fit_feature_standardization(
        FeatureStandardizationSpecification(("x",)),
        _table(values),
        population_id="training",
    )
    assert state.training_means == (offset + 2.5,)
    assert state.training_standard_deviations == (math.sqrt(1.25),)


def test_tiny_nonconstant_spread_without_squared_variance_underflow() -> None:
    """Tiny nonconstant spread without squared variance underflow."""
    state = fit_feature_standardization(
        FeatureStandardizationSpecification(("x",)),
        _table((0, 1e-300)),
        population_id="training",
    )
    assert state.training_standard_deviations == (5e-301,)
    assert state.constant_coordinates == (False,)
    assert state.transform(_table((0, 1e-300))).features.rows == ((-1.0,), (1.0,))


def test_unrepresentable_positive_deviation_refuses_not_constant() -> None:
    """Unrepresentable positive deviation refuses not constant."""
    with pytest.raises(ValueError, match="underflows"):
        fit_feature_standardization(
            FeatureStandardizationSpecification(("x",)),
            _table((0, math.ulp(0.0))),
            population_id="training",
        )


def test_large_finite_values_and_overflowing_centered_difference() -> None:
    """Large finite values and overflowing centered difference."""
    limit = sys.float_info.max
    values = (limit, limit, limit, limit, -limit)
    state = fit_feature_standardization(
        FeatureStandardizationSpecification(("x",)),
        _table(values),
        population_id="training",
    )
    actual = state.transform(_table(values)).features.rows
    independent = tuple(
        float(
            (Fraction(v) - Fraction(state.training_means[0]))
            / Fraction(state.effective_scales[0]),
        )
        for v in values
    )
    assert [r[0] for r in actual] == pytest.approx(independent)
    assert all(math.isfinite(r[0]) for r in actual)
    assert state.training_standard_deviations[0] > HUGE_DEVIATION


def test_application_overflow_or_underflow_refuses() -> None:
    """Application overflow or underflow refuses."""
    tiny = fit_feature_standardization(
        FeatureStandardizationSpecification(("x",)),
        _table((0, 1e-300)),
        population_id="training",
    )
    with pytest.raises(ValueError, match="overflows"):
        tiny.transform(_table((1e308,)))
    large = fit_feature_standardization(
        FeatureStandardizationSpecification(("x",)),
        _table((-1e308, 1e308)),
        population_id="training",
    )
    with pytest.raises(ValueError, match="underflows"):
        large.transform(_table((math.ulp(0.0),)))


def test_alignment_extra_discrete_coordinates_and_empty_later() -> None:
    """Alignment extra discrete coordinates and empty later."""
    features = _table(
        ((9, 1, 0), (11, 3, 1)),
        ("y", "x", "indicator"),
        (
            FeatureValueKind.CONTINUOUS,
            FeatureValueKind.CONTINUOUS,
            FeatureValueKind.DISCRETE,
        ),
    )
    state = fit_feature_standardization(
        FeatureStandardizationSpecification(("x",)),
        features,
        population_id="training",
    )
    assert state.feature_names == ("x",)
    assert state.transform(features).features.rows == ((-1.0,), (1.0,))
    reordered = _table(
        ((4, 2, 99),),
        ("indicator", "x", "y"),
        (
            FeatureValueKind.DISCRETE,
            FeatureValueKind.CONTINUOUS,
            FeatureValueKind.CONTINUOUS,
        ),
    )
    assert state.transform(reordered).features.rows == ((0.0,),)
    assert state.transform(_table(())).features.rows == ()
    with pytest.raises(ValueError, match="missing required"):
        state.transform(_table((1,), names=("other",)))
    with pytest.raises(ValueError, match="continuous"):
        state.transform(_table((1,), kinds=(FeatureValueKind.DISCRETE,)))


@pytest.mark.parametrize(
    "names",
    [(), ("x", "x"), ("",), (True,), tuple(str(i) for i in range(129))],
)
def test_invalid_selected_feature_specification(names: tuple[str, ...]) -> None:
    """Invalid selected feature specification."""
    with pytest.raises((ValueError, TypeError)):
        FeatureStandardizationSpecification(names)


def test_specification_rejects_string_and_copies_selected_names() -> None:
    """Specification rejects string and copies selected names."""
    with pytest.raises(TypeError):
        FeatureStandardizationSpecification(cast("tuple[str, ...]", "x"))
    names = ["x"]
    specification = FeatureStandardizationSpecification(cast("tuple[str, ...]", names))
    names[0] = "mutated"
    assert specification.feature_names == ("x",)


@pytest.mark.parametrize(
    "scope",
    [PopulationScope.VALIDATION, PopulationScope.TEST, "training"],
)
def test_forbidden_fitting_population_scope(scope: PopulationScope) -> None:
    """Forbidden fitting population scope."""
    with pytest.raises(ValueError, match="evaluation populations"):
        fit_feature_standardization(
            FeatureStandardizationSpecification(("x",)),
            _table((1, 2)),
            population_id="training",
            scope=scope,
        )


@pytest.mark.parametrize(
    "value",
    [float("nan"), float("inf"), -float("inf"), True, "1"],
)
def test_feature_contract_nonfinite_or_unsupported(value: float) -> None:
    """Feature contract nonfinite or unsupported."""
    with pytest.raises((ValueError, TypeError)):
        FeatureTable(("x",), ((value,),), (FeatureValueKind.CONTINUOUS,))


def test_empty_discrete_and_wrong_contracts_refuse() -> None:
    """Empty discrete and wrong contracts refuse."""
    with pytest.raises(ValueError, match="nonempty population"):
        fit_feature_standardization(
            FeatureStandardizationSpecification(("x",)),
            _table(()),
            population_id="training",
        )
    with pytest.raises(ValueError, match="continuous quantitative"):
        fit_feature_standardization(
            FeatureStandardizationSpecification(("x",)),
            _table((0, 1), kinds=(FeatureValueKind.DISCRETE,)),
            population_id="training",
        )
    with pytest.raises(TypeError):
        fit_feature_standardization(
            cast("FeatureStandardizationSpecification", "zscore"),
            _table((1, 2)),
            population_id="training",
        )
    with pytest.raises(TypeError):
        fit_feature_standardization(
            FeatureStandardizationSpecification(("x",)),
            cast("FeatureTable", [[1]]),
            population_id="training",
        )


def test_deterministic_statistics_immutable_state_and_distinct_occurrences() -> None:
    """Deterministic statistics immutable state and distinct occurrences."""
    first, second = (
        fit_feature_standardization(
            FeatureStandardizationSpecification(("x",)),
            _table((2, 4, 9)),
            population_id="training",
        ),
        fit_feature_standardization(
            FeatureStandardizationSpecification(("x",)),
            _table((2, 4, 9)),
            population_id="training",
        ),
    )
    assert first.training_means == second.training_means
    assert first.training_standard_deviations == second.training_standard_deviations
    assert first.fitting_input_sha256 == second.fitting_input_sha256
    assert first.state_id != second.state_id
    assert first.construction_execution_id != second.construction_execution_id
    with pytest.raises(dataclasses.FrozenInstanceError):
        first.training_means = (0.0,)  # type: ignore[misc]  # deliberate frozen mutation
    snapshot = dataclasses.asdict(first)
    first.transform(_table((999999,)))
    assert dataclasses.asdict(first) == snapshot
    with pytest.raises(ValueError, match="statistics require"):
        replace(first, effective_scales=(True,))
    with pytest.raises(ValueError, match="deviation/constant/effective scale conflict"):
        replace(first, constant_coordinates=(True,))
    with pytest.raises(ValueError, match="fitting population/coordinate counts"):
        replace(first, fitting_observation_count=True)


def test_workload_bounds_and_binary64_source_limit() -> None:
    """Workload bounds and binary64 source limit."""
    with pytest.raises(ValueError, match="bounds"):
        fit_feature_standardization(
            FeatureStandardizationSpecification(("x",)),
            _table((1,) * 100001),
            population_id="training",
        )
    state = fit_feature_standardization(
        FeatureStandardizationSpecification(("x",)),
        _table((2**54, 2**54 + 1)),
        population_id="training",
    )
    assert state.constant_coordinates == (True,)


def test_managed_fit_apply_identities_statistics_and_observer_failure(
    tmp_path: Path,
) -> None:
    """Managed fit apply identities statistics and observer failure."""

    def _fail_observer() -> Never:
        message = "optional observer fixture"
        raise RuntimeError(message)

    def observer(event: ExecutionEvent) -> None:
        if isinstance(event.payload, StageStarted):
            _fail_observer()

    database = tmp_path / "execution.sqlite"
    with (
        SQLiteExecutionRecorder(database) as recorder,
        ExecutionContext(recorder, Admitted("standardization.fixture")) as parent,
    ):
        state = fit_feature_standardization(
            FeatureStandardizationSpecification(("x",)),
            _table((1, 3)),
            population_id="training",
            source_identity="source",
            representation_identity="prepared",
            recorder=recorder,
            parent=parent,
            observer=observer,
        )
        result = state.transform(
            _table((7,)),
            population_id="held-out",
            scope=PopulationScope.VALIDATION,
            recorder=recorder,
            parent=parent,
        )
        parent.completed()
    history = inspect_execution(database, state.construction_execution_id)
    assert history is not None
    assert history.outcome is Outcome.COMPLETED
    assert any(isinstance(e.payload, Diagnostic) for e in history.events)
    applied = inspect_execution(database, result.execution_id)
    assert applied is not None
    assert applied.outcome is Outcome.COMPLETED
    assert applied.parent_execution_id == history.parent_execution_id
    assert result.features.rows == ((5.0,),)
    assert len(history.events) < FIT_EVENT_LIMIT
    assert len(applied.events) < APPLY_EVENT_LIMIT


def test_required_recording_failure_does_not_return_state() -> None:
    """Required recording failure does not return state."""

    class Broken:
        def record(self, event: ExecutionEvent) -> Never:
            del event
            message = "required recording fixture"
            raise RecordingError(message)

    with pytest.raises(RecordingError):
        fit_feature_standardization(
            FeatureStandardizationSpecification(("x",)),
            _table((1, 2)),
            population_id="training",
            recorder=Broken(),
        )
    with pytest.raises(ValueError, match="observer/parent requires"):
        fit_feature_standardization(
            FeatureStandardizationSpecification(("x",)),
            _table((1, 2)),
            population_id="training",
            observer=lambda _event: None,
        )


def test_managed_invalid_input_is_acknowledged_failure(tmp_path: Path) -> None:
    """Managed invalid input is acknowledged failure."""
    database = tmp_path / "execution.sqlite"
    with (
        SQLiteExecutionRecorder(database) as recorder,
        pytest.raises(ValueError, match="nonempty population"),
    ):
        fit_feature_standardization(
            FeatureStandardizationSpecification(("x",)),
            _table(()),
            population_id="training",
            recorder=recorder,
        )
    with sqlite3.connect(database) as connection:
        identity = connection.execute("select id from executions").fetchone()[0]
    history = inspect_execution(database, UUID(identity))
    assert history is not None
    assert history.outcome is Outcome.FAILED
