# Copyright (c) 2026
"""Complete-row MAE/RMSE/R2 with explicit units, arithmetic limits and nonvalues."""

import math
from collections.abc import Callable
from dataclasses import dataclass

from devtools.learning.identity import source_fingerprint as fingerprint
from devtools.learning.measurement.contracts import (
    Measured,
    NonValueKind,
    NoValue,
)
from devtools.learning.regression.contracts import (
    ContinuousTarget,
    RegressionPopulation,
)
from devtools.learning.regression.state import RegressionPredictions

type RegressionValue = Measured[float] | NoValue


def _undefined(reason: str, detail: str) -> NoValue:
    return NoValue(NonValueKind.UNDEFINED, reason, detail)


def _finite_measurement(value: float) -> Measured[float]:
    if not math.isfinite(value):
        msg = "nonfinite result"
        raise OverflowError(msg)
    return Measured(float(value))


def _arithmetic(compute: Callable[[], float]) -> RegressionValue:
    try:
        return _finite_measurement(compute())
    except (OverflowError, ValueError, ZeroDivisionError):
        return _undefined(
            "unrepresentable_regression_arithmetic",
            (
                "The declared binary64 calculation is not finitely representable;"
                " no rows were dropped."
            ),
        )


@dataclass(frozen=True, slots=True)
class RegressionEvaluation:
    """Retain the declared RegressionEvaluation scientific values and invariants."""

    population_id: str
    input_identity: str
    target_values_identity: str
    target: ContinuousTarget
    row_ids: tuple[str, ...]
    mae: RegressionValue
    rmse: RegressionValue
    r2: RegressionValue
    sse: float | None
    sst: float | None


def evaluate_regression(
    population: RegressionPopulation,
    predictions: RegressionPredictions,
) -> RegressionEvaluation:
    """Measure exact original rows; a nonvalue never shrinks their denominator."""
    if (
        type(population) is not RegressionPopulation
        or type(predictions) is not RegressionPredictions
    ):
        msg = "typed original regression population and predictions required"
        raise TypeError(msg)
    x = population.inputs
    if (
        predictions.population_id,
        predictions.row_ids,
        predictions.target,
        predictions.input_identity,
    ) != (x.population_id, x.row_ids, population.target, x.content_identity):
        msg = "original row order, target units and prediction population differ"
        raise ValueError(msg)
    return _evaluate_values(population, predictions.values)


def _evaluate_values(
    population: RegressionPopulation,
    values: tuple[float, ...],
) -> RegressionEvaluation:
    """Existing v1 formulas shared after each concrete prediction-type check."""
    x = population.inputs
    n = len(x.row_ids)
    empty = _undefined(
        "empty_regression_population",
        "No original paired observations; no positive denominator exists.",
    )
    mae: RegressionValue = empty
    rmse: RegressionValue = empty
    r2: RegressionValue = empty
    sse = sst = None
    if n:
        errors = tuple((a - b for a, b in zip(population.values, values, strict=True)))
        mae = _arithmetic(lambda: math.fsum(abs(e) for e in errors) / n)
        sum_squared = _arithmetic(lambda: math.fsum(e**2 for e in errors))
        if isinstance(sum_squared, Measured):
            sse = sum_squared.value
            rmse = _arithmetic(lambda: math.sqrt(sum_squared.value / n))
        else:
            rmse = sum_squared

        def total_variation() -> float:
            center = math.fsum(population.values) / n
            return math.fsum((v - center) ** 2 for v in population.values)

        variation = _arithmetic(total_variation)
        if isinstance(variation, Measured):
            sst = variation.value
            if sst == 0:
                r2 = _undefined(
                    "constant_regression_target",
                    (
                        "SST is zero on the exact target population; no forced "
                        "zero/one R"
                        "2 convention."
                    ),
                )
            elif isinstance(sum_squared, Measured):
                r2 = _arithmetic(lambda: 1 - sum_squared.value / variation.value)
            else:
                r2 = sum_squared
        else:
            r2 = variation
    return RegressionEvaluation(
        x.population_id,
        x.content_identity,
        fingerprint(population.values),
        population.target,
        x.row_ids,
        mae,
        rmse,
        r2,
        sse,
        sst,
    )
