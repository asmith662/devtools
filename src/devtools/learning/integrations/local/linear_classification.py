# Copyright (c) 2026
"""Explicit versioned binary-linear state encoding; no optimizer or pickle."""

import json
from dataclasses import asdict
from uuid import UUID

from devtools.learning.classification.linear import FittedBinaryLinearClassifier
from devtools.learning.integrations.local._codec import array as _array
from devtools.learning.integrations.local._codec import (
    decode_references,
)
from devtools.learning.integrations.local._codec import nonempty_text as _text
from devtools.learning.integrations.local._codec import retained_object as _object
from devtools.learning.integrations.local.feasibility import json_document


def model_document(model: FittedBinaryLinearClassifier) -> dict[str, object]:
    """Retain state/source UUIDs separately from numerical content identity."""
    return _object(
        json_document(
            {
                "schema": "binary-linear-classifier-v1",
                "state": asdict(model),
                "content_sha256": model.content_identity,
            },
        ),
    )


def _real(value: object) -> float:
    if type(value) is not float:
        msg = "original binary64 state values required"
        raise ValueError(msg)
    return value


def _pairs(value: object) -> tuple[tuple[str, str], ...]:
    result = []
    for item in _array(value):
        pair = _array(item)
        if len(pair) != 2:
            msg = "observed key/value pair required"
            raise ValueError(msg)
        result.append((_text(pair[0]), _text(pair[1])))
    return tuple(result)


def decode_model(raw: bytes) -> FittedBinaryLinearClassifier:
    """Refuse extra meanings and inconsistent content, not just malformed JSON."""
    document = _object(json.loads(raw))
    if document.get("schema") != "binary-linear-classifier-v1":
        msg = "unsupported numerical state codec"
        raise ValueError(msg)
    s = _object(document["state"])
    if _array(s["categories"]) != [0, 1] or any(
        type(v) is not int for v in _array(s["categories"])
    ):
        msg = "original integer category meaning required"
        raise ValueError(msg)
    result = FittedBinaryLinearClassifier(
        tuple(_text(v) for v in _array(s["feature_names"])),
        _text(s["target_identity"]),
        tuple(_real(v) for v in _array(s["coefficients"])),
        _real(s["intercept"]),
        _text(s["training_population_id"]),
        _text(s["training_input_sha256"]),
        UUID(_text(s["fitting_execution_id"])),
        _pairs(s["configuration"]),
        _pairs(s["backend_observations"]),
        decode_references(s["references"]),
        UUID(_text(s["state_id"])),
    )
    if model_document(result) != document:
        msg = "retained numerical state/content meaning differs"
        raise ValueError(msg)
    return result
