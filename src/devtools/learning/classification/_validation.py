# Copyright (c) 2026

"""Pure, concrete training checks shared by inspection and sklearn construction."""

from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum

from devtools.learning.representation.features import FeatureTable, FeatureValueKind
from devtools.learning.representation.targets import (
    CategoryValue,
    category_identity,
    validate_category_values,
)

_MINIMUM_CATEGORIES = 2


class ClassificationRequirement(Enum):
    """Conditions of the selected classifier's attributed training contract."""

    SPECIFICATION = "specification"

    PREPARED_FEATURES = "prepared_features"

    NONEMPTY_POPULATION = "nonempty_population"

    FEATURE_SCHEMA = "feature_schema"

    FEATURE_KINDS = "feature_kinds"

    TARGET_VALUES = "target_values"

    TARGET_LENGTH = "target_length"

    OBSERVED_CLASSES = "observed_classes"

    NEIGHBOR_COUNT = "neighbor_count"

    POPULATION_IDENTITY = "population_identity"

    POPULATION_SCOPE = "population_scope"

    TARGET_IDENTITY = "target_identity"

    CATEGORY_TASK = "category_task"

    ROW_BINDING = "row_binding"

    FITTING_AUTHORIZATION = "fitting_authorization"

    BACKEND_AVAILABILITY = "backend_availability"

    RESOURCE_SUFFICIENCY = "resource_sufficiency"

    PREDICTIVE_EFFECTIVENESS = "predictive_effectiveness"


@dataclass(frozen=True, slots=True)
class TrainingCheck:
    requirement: ClassificationRequirement

    satisfied: bool | None

    explanation: str

    exception: type[ValueError] | type[TypeError] = ValueError

    coordinates: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class CheckedTraining:
    checks: tuple[TrainingCheck, ...]

    targets: tuple[CategoryValue, ...]

    categories: tuple[CategoryValue, ...]

    codes: tuple[int, ...]


def inspect_training(
    features: FeatureTable | None,
    targets: tuple[CategoryValue, ...] | None,
    *,
    label: str,
    continuous_only: bool = False,
    neighbor_count: int | None = None,
    observation_count: int | None = None,
) -> CheckedTraining:
    """Inspect without backend work; absent dependent inputs produce unknowns."""
    checks: list[TrainingCheck] = []

    def check(
        requirement: ClassificationRequirement,
        condition: bool | None,
        failure: str,
        success: str,
        *,
        coordinates: tuple[str, ...] = (),
    ) -> None:

        checks.append(
            TrainingCheck(
                requirement,
                condition,
                success if condition else failure,
                coordinates=coordinates,
            ),
        )

    count = features.observation_count if features is not None else observation_count

    check(
        ClassificationRequirement.NONEMPTY_POPULATION,
        count > 0 if count is not None else None,
        f"{label} requires a non-empty population",
        f"The supplied training population contains {count} observations.",
    )

    check(
        ClassificationRequirement.FEATURE_SCHEMA,
        bool(features.feature_names) if features is not None else None,
        f"{label} requires at least one feature",
        "FeatureTable supplies identified, ordered finite numerical coordinates.",
    )

    discrete = (
        tuple(
            (
                name
                for name, kind in zip(
                    features.feature_names,
                    features.feature_value_kinds,
                    strict=True,
                )
                if kind is not FeatureValueKind.CONTINUOUS
            ),
        )
        if features is not None
        else ()
    )

    check(
        ClassificationRequirement.FEATURE_KINDS,
        not discrete or not continuous_only if features is not None else None,
        "Gaussian Naïve Bayes requires continuous features"
        if continuous_only
        else f"{label} supports continuous and discrete prepared features",
        "All coordinates are continuous."
        if continuous_only
        else "Continuous and discrete FeatureTable coordinates are supported.",
        coordinates=discrete if continuous_only else (),
    )

    if neighbor_count is not None:
        check(
            ClassificationRequirement.NEIGHBOR_COUNT,
            neighbor_count <= count if count is not None else None,
            "neighbor_count cannot exceed the training population",
            f"neighbor_count={neighbor_count} does not exceed {count} rows.",
        )

    valid: tuple[CategoryValue, ...] = ()

    target_error: TypeError | ValueError | None = None

    if targets is not None:
        try:
            valid = validate_category_values(targets)

        except (TypeError, ValueError) as error:
            target_error = error

    if target_error is not None:
        checks.append(
            TrainingCheck(
                ClassificationRequirement.TARGET_VALUES,
                False,
                str(target_error),
                TypeError if isinstance(target_error, TypeError) else ValueError,
            ),
        )

    else:
        check(
            ClassificationRequirement.TARGET_VALUES,
            bool(valid) if targets is not None else None,
            "training targets must not be empty"
            if targets is not None
            else "No target observations were supplied.",
            "Targets are actual nonempty, finite typed category observations.",
        )

    check(
        ClassificationRequirement.TARGET_LENGTH,
        len(targets) == count if targets is not None and count is not None else None,
        "feature and target observation counts must match",
        "Feature and target lengths match; original row identity is not proven.",
    )

    categories: list[CategoryValue] = []

    codes: list[int] = []

    by_identity: dict[tuple[type[object], object], int] = {}

    for target in valid:
        identity = category_identity(target)

        if identity not in by_identity:
            by_identity[identity] = len(categories)

            categories.append(target)

        codes.append(by_identity[identity])

    check(
        ClassificationRequirement.OBSERVED_CLASSES,
        len(categories) >= _MINIMUM_CATEGORIES
        if targets is not None and target_error is None
        else None,
        f"{label} requires at least two classes",
        f"{len(categories)} actually observed typed categories are present.",
    )

    return CheckedTraining(tuple(checks), valid, tuple(categories), tuple(codes))


def validate_training(
    features: FeatureTable,
    targets: Iterable[CategoryValue],
    *,
    label: str,
    continuous_only: bool = False,
    neighbor_count: int | None = None,
) -> CheckedTraining:
    """Apply the same hard predicates, preserving concrete constructor errors."""
    if not isinstance(features, FeatureTable):
        msg = "training_features must use FeatureTable"
        raise TypeError(msg)

    preliminary = inspect_training(
        features,
        None,
        label=label,
        continuous_only=continuous_only,
        neighbor_count=neighbor_count,
    )

    for check in preliminary.checks:
        if check.requirement is ClassificationRequirement.TARGET_VALUES:
            break

        if check.satisfied is not True:
            raise check.exception(check.explanation)

    result = inspect_training(
        features,
        tuple(targets),
        label=label,
        continuous_only=continuous_only,
        neighbor_count=neighbor_count,
    )

    for check in result.checks:
        if check.satisfied is not True:
            raise check.exception(check.explanation)

    return result
