# Copyright (c) 2026
"""Selected scientific wire helpers and explicit versioned invariants."""

import json
from dataclasses import Field, asdict
from typing import ClassVar, Protocol, cast
from uuid import UUID

from devtools.learning.integrations.local._codec import array
from devtools.learning.integrations.local._codec import nonempty_text as text
from devtools.learning.integrations.local._codec import retained_object as obj
from devtools.learning.integrations.local.classification.codec import (
    document,
    preparation,
)
from devtools.learning.integrations.local.tables import _table
from devtools.learning.regression.contracts import (
    ContinuousTarget,
    RegressionInput,
    RegressionMethod,
    RegressionPopulation,
    RegressionRole,
    RegressionSpecification,
)
from devtools.learning.regression.limits import REGRESSION_V2
from devtools.learning.regression.state import FittedRegression, RegressionPredictions
from devtools.learning.representation.features import FeatureValueKind


class DataclassValue(Protocol):
    """Retain the declared DataclassValue scientific values and invariants."""

    __dataclass_fields__: ClassVar[dict[str, Field[object]]]


def exact(result: object, value: object) -> None:
    """Apply the explicit exact contract within this owner."""
    if document(asdict(cast("DataclassValue", result))) != value:
        msg = "noncanonical or unsupported regression schema fields"
        raise ValueError(msg)


def real(value: object) -> float:
    """Apply the explicit real contract within this owner."""
    if type(value) is not float:
        msg = "original continuous binary64 value required"
        raise TypeError(msg)
    return value


def optional_unit(value: object) -> str | None:
    """Apply the explicit optional unit contract within this owner."""
    return None if value is None else text(value)


def target(value: object) -> ContinuousTarget:
    """Apply the explicit target contract within this owner."""
    d = obj(value)
    result = ContinuousTarget(
        text(d["identity"]),
        text(d["quantity"]),
        optional_unit(d["unit"]),
        text(d["kind"]),
        text(d["version"]),
    )
    exact(result, d)
    return result


def inputs(value: object) -> RegressionInput:
    """Apply the explicit inputs contract within this owner."""
    d = obj(value)
    result = RegressionInput(
        _table(d["features"]),
        tuple(optional_unit(v) for v in array(d["feature_units"])),
        tuple(text(v) for v in array(d["row_ids"])),
        text(d["population_id"]),
        text(d["source_identity"]),
        RegressionRole(d["role"]),
        text(d["version"]),
    )
    exact(result, d)
    return result


def population(value: object) -> RegressionPopulation:
    """Apply the explicit population contract within this owner."""
    d = obj(value)
    result = RegressionPopulation(
        inputs(d["inputs"]),
        target(d["target"]),
        tuple(real(v) for v in array(d["values"])),
        text(d["missing_policy"]),
        text(d["version"]),
    )
    exact(result, d)
    return result


def specification(value: object) -> RegressionSpecification:
    """Apply the explicit specification contract within this owner."""
    d = obj(value)
    result = RegressionSpecification(RegressionMethod(d["method"]), text(d["version"]))
    exact(result, d)
    return result


def state(value: object, *, maximum_bytes: int | None = None) -> FittedRegression:
    """Apply the explicit state contract within this owner."""
    d = obj(value)
    if maximum_bytes is not None and (
        type(maximum_bytes) is not int
        or not 1 <= maximum_bytes <= REGRESSION_V2.state_bytes
    ):
        msg = "explicit bounded retained-state payload required"
        raise ValueError(msg)
    if d.get("version") == "fitted-regression-v2" and len(
        json.dumps(d, sort_keys=True, allow_nan=False).encode(),
    ) > (maximum_bytes if maximum_bytes is not None else REGRESSION_V2.state_bytes):
        msg = "bounded serialized retained regression state required"
        raise ValueError(msg)
    result = FittedRegression(
        specification(d["specification"]),
        target(d["target"]),
        tuple(text(v) for v in array(d["feature_names"])),
        tuple(FeatureValueKind(v) for v in array(d["feature_value_kinds"])),
        tuple(optional_unit(v) for v in array(d["feature_units"])),
        text(d["training_population_id"]),
        tuple(text(v) for v in array(d["training_row_ids"])),
        text(d["training_identity"]),
        None if d["preparation"] is None else preparation(d["preparation"]),
        tuple(real(v) for v in array(d["coefficients"])),
        real(d["intercept"]),
        None if d["neighbor_features"] is None else _table(d["neighbor_features"]),
        None
        if d["neighbor_targets"] is None
        else tuple(real(v) for v in array(d["neighbor_targets"])),
        UUID(text(d["execution_id"])),
        UUID(text(d["state_id"])),
        tuple(
            (text(array(pair)[0]), text(array(pair)[1])) for pair in array(d["backend"])
        ),
        text(d["version"]),
    )
    exact(result, d)
    return result


def predictions(value: object) -> RegressionPredictions:
    """Apply the explicit predictions contract within this owner."""
    d = obj(value)
    result = RegressionPredictions(
        UUID(text(d["state_id"])),
        text(d["method_identity"]),
        text(d["input_identity"]),
        text(d["population_id"]),
        tuple(text(v) for v in array(d["row_ids"])),
        target(d["target"]),
        tuple(real(v) for v in array(d["values"])),
        None
        if d["neighbor_row_ids"] is None
        else tuple(
            tuple(text(v) for v in array(row)) for row in array(d["neighbor_row_ids"])
        ),
        None
        if d["neighbor_distances"] is None
        else tuple(
            tuple(real(v) for v in array(row)) for row in array(d["neighbor_distances"])
        ),
        text(d["version"]),
    )
    exact(result, d)
    return result
