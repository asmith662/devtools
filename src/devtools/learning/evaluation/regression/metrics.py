# Copyright (c) 2026
"""Complete-row MAE/RMSE/R2 with explicit units, arithmetic limits and nonvalues."""

import math
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from devtools.core.time import Timestamp
from devtools.learning.identity import source_fingerprint as fingerprint
from devtools.learning.measurement.contracts import (
    FieldBinding,
    Measured,
    MeasurementBasis,
    MeasurementBinding,
    MeasurementBundle,
    MeasurementContext,
    MetricDefinition,
    MetricParameter,
    NonValueKind,
    NoValue,
    OutputContract,
    UnitMeaning,
    ValueShape,
)
from devtools.learning.regression.contracts import (
    ContinuousTarget,
    RegressionPopulation,
)
from devtools.learning.regression.state import RegressionPredictions
from devtools.learning.representation.features import FeatureValueKind
from devtools.learning.representation.observations import ColumnRole, MissingValuePolicy

type RegressionValue = Measured[float] | NoValue


class RegressionMeasure(Enum):
    """Retain the declared RegressionMeasure scientific values and invariants."""

    MAE = "mae"
    RMSE = "rmse"
    R2 = "r2"
    MAE_SKILL = "mae_skill"


@dataclass(frozen=True, slots=True)
class RegressionMetricDefinition(MetricDefinition[float]):
    """Retain the declared RegressionMetricDefinition scientific values and invariants."""

    measure: RegressionMeasure

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        if not isinstance(self.measure, RegressionMeasure):
            msg = "typed regression metric required"
            raise TypeError(msg)
        self.validate_definition()

    @property
    def semantic_key(self) -> str:
        """Apply the explicit semantic key contract within this owner."""
        return "regression." + self.measure.value

    @property
    def version(self) -> int:
        """Apply the explicit version contract within this owner."""
        return 1

    @property
    def parameters(self) -> tuple[MetricParameter, ...]:
        """Apply the explicit parameters contract within this owner."""
        formula = {
            RegressionMeasure.MAE: "fsum(abs(truth-prediction))/N",
            RegressionMeasure.RMSE: "sqrt(fsum((truth-prediction)^2)/N)",
            RegressionMeasure.R2: "1-SSE/SST;SST=fsum((truth-fsum(truth)/N)^2)",
            RegressionMeasure.MAE_SKILL: "1-candidate_MAE/same_task_reference_MAE",
        }[self.measure]
        return (
            MetricParameter("formula", formula),
            MetricParameter("weights", "equal_original_observation_mass"),
            MetricParameter("missing", "complete_paired_population_required"),
            MetricParameter(
                "undefined",
                "empty_or_zero_required_denominator_or_binary64_overflow",
            ),
            MetricParameter(
                "direction",
                "lower"
                if self.measure in (RegressionMeasure.MAE, RegressionMeasure.RMSE)
                else "higher",
            ),
            MetricParameter(
                "units",
                "same_declared_target_units"
                if self.measure in (RegressionMeasure.MAE, RegressionMeasure.RMSE)
                else "dimensionless",
            ),
        )

    @property
    def output(self) -> OutputContract:
        """Apply the explicit output contract within this owner."""
        return OutputContract(
            ValueShape.REAL,
            UnitMeaning.SOURCE_QUANTITY
            if self.measure in (RegressionMeasure.MAE, RegressionMeasure.RMSE)
            else UnitMeaning.DIMENSIONLESS,
        )

    def validate_value(self, value: float) -> None:
        """Apply the explicit validate value contract within this owner."""
        if (
            type(value) is not float
            or not math.isfinite(value)
            or (
                self.measure in (RegressionMeasure.MAE, RegressionMeasure.RMSE)
                and value < 0
            )
            or (
                self.measure in (RegressionMeasure.R2, RegressionMeasure.MAE_SKILL)
                and value > 1
            )
        ):
            msg = "finite regression metric in its legitimate range required"
            raise ValueError(msg)

    def validate_binding(
        self,
        binding: MeasurementBinding,
        basis: MeasurementBasis | None,
    ) -> None:
        """Apply the explicit validate binding contract within this owner."""
        if (
            not isinstance(binding, FieldBinding)
            or binding.declared_role is not ColumnRole.TARGET
            or binding.declared_value_kind is not FeatureValueKind.CONTINUOUS
            or (basis is None)
            or (basis.population_count != basis.effective_count)
        ):
            msg = "complete continuous-target source field basis required"
            raise ValueError(msg)


def _undefined(reason: str, detail: str) -> NoValue:
    return NoValue(NonValueKind.UNDEFINED, reason, detail)


def _arithmetic(compute: Callable[[], float]) -> RegressionValue:
    try:
        value = compute()
        if not math.isfinite(value):
            msg = "nonfinite result"
            raise OverflowError(msg)
        return Measured(float(value))
    except (OverflowError, ValueError, ZeroDivisionError):
        return _undefined(
            "unrepresentable_regression_arithmetic",
            "The declared binary64 calculation is not finitely representable; no rows were dropped.",
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
                    "SST is zero on the exact target population; no forced zero/one R2 convention.",
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


def mae_skill(
    candidate: RegressionEvaluation,
    reference: RegressionEvaluation,
) -> RegressionValue:
    """Paired unitless skill; positive means less MAE than the declared reference."""
    if (
        candidate.population_id,
        candidate.input_identity,
        candidate.target_values_identity,
        candidate.target,
        candidate.row_ids,
    ) != (
        reference.population_id,
        reference.input_identity,
        reference.target_values_identity,
        reference.target,
        reference.row_ids,
    ):
        msg = "same original task/population/target scale and units required"
        raise ValueError(msg)
    if not isinstance(candidate.mae, Measured) or not isinstance(
        reference.mae,
        Measured,
    ):
        return NoValue(
            NonValueKind.UNAVAILABLE,
            "incomplete_regression_skill",
            "Required original paired MAE is not measured.",
        )
    if reference.mae.value <= 0:
        return _undefined(
            "zero_reference_mae",
            "No positive original reference MAE for scale normalization.",
        )
    candidate_value, reference_value = (candidate.mae.value, reference.mae.value)
    return _arithmetic(lambda: 1 - candidate_value / reference_value)


def regression_measurements(
    evaluation: RegressionEvaluation,
    context: MeasurementContext,
    *,
    at: datetime | None = None,
    bundle_id: UUID | None = None,
    execution_id: UUID | None = None,
) -> MeasurementBundle[float]:
    """Use source-unit field bindings without extending common measurement types."""
    at = at or Timestamp.now().value
    target = evaluation.target
    binding = FieldBinding(
        target.identity,
        ColumnRole.TARGET,
        FeatureValueKind.CONTINUOUS,
        MissingValuePolicy(nan_is_missing=False),
        target.unit,
    )
    observations = tuple(
        (
            RegressionMetricDefinition(measure).observe(
                value,
                context_id=context.context_id,
                key="regression/" + measure.value,
                binding=binding,
                basis=MeasurementBasis(
                    len(evaluation.row_ids),
                    len(evaluation.row_ids),
                ),
                collected_at=at,
            )
            for measure, value in (
                (RegressionMeasure.MAE, evaluation.mae),
                (RegressionMeasure.RMSE, evaluation.rmse),
                (RegressionMeasure.R2, evaluation.r2),
            )
        ),
    )
    return MeasurementBundle(
        bundle_id or uuid4(),
        at,
        (context,),
        observations,
        execution_id,
    )
