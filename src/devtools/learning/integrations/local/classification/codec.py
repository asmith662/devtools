# Copyright (c) 2026
"""Selected scientific wire helpers and explicit versioned invariants."""

from dataclasses import asdict
from uuid import UUID

from devtools.learning.integrations.local._codec import array, integer
from devtools.learning.integrations.local._codec import nonempty_text as text
from devtools.learning.integrations.local._codec import retained_object as obj
from devtools.learning.integrations.local.feasibility import json_document
from devtools.learning.integrations.local.tables import _table
from devtools.learning.representation.observations import PopulationScope
from devtools.learning.representation.standardization import (
    FeatureStandardizationSpecification,
    FittedFeatureStandardization,
)


def document(value: object) -> dict[str, object]:
    """Use existing JSON primitive semantics for explicitly owned values."""
    return obj(json_document(value))


def preparation(value: object) -> FittedFeatureStandardization:
    """Apply the explicit preparation contract within this owner."""
    p = obj(value)
    result = FittedFeatureStandardization(
        FeatureStandardizationSpecification(
            tuple(text(v) for v in array(obj(p["specification"])["feature_names"])),
        ),
        _table(
            {
                "feature_names": obj(p["specification"])["feature_names"],
                "rows": [],
                "feature_value_kinds": p["feature_value_kinds"],
            },
        ).feature_value_kinds,
        tuple(float(str(v)) for v in array(p["training_means"])),
        tuple(float(str(v)) for v in array(p["training_standard_deviations"])),
        tuple(float(str(v)) for v in array(p["effective_scales"])),
        tuple(v is True for v in array(p["constant_coordinates"])),
        text(p["fitting_population_id"]),
        PopulationScope(text(p["fitting_scope"])),
        integer(p["fitting_observation_count"]),
        text(p["fitting_input_sha256"]),
        UUID(text(p["construction_execution_id"])),
        None if p["source_identity"] is None else text(p["source_identity"]),
        None
        if p["representation_identity"] is None
        else text(p["representation_identity"]),
        UUID(text(p["state_id"])),
    )
    if document(asdict(result)) != p:
        msg = "original standardization meaning differs"
        raise ValueError(msg)
    return result
