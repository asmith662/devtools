# Copyright (c) 2026
"""Closed scientific JSON decoding, including adversarial authored wire values."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING
from uuid import uuid4

import pytest

from devtools.core.time import Timestamp
from devtools.learning.evidence.events import (
    Diagnostic,
    ExceptionFact,
    ExecutionEvent,
    FailureCategory,
    Severity,
)
from devtools.learning.identity import source_fingerprint
from devtools.learning.integrations.local._codec import (
    _default,
    array,
    decode,
    decode_references,
    encode,
    integer,
    nonempty_text,
    optional_boolean,
    optional_integer,
    optional_text,
    retained_object,
    strings,
)
from devtools.learning.integrations.local.classification.codec import document
from devtools.learning.integrations.local.feasibility import json_document
from devtools.learning.integrations.local.tables import _real, _table
from devtools.learning.investigation.errors import LearningUnavailableError
from devtools.learning.measurement.contracts import NonValueKind

if TYPE_CHECKING:
    from collections.abc import Callable


def _diagnostic() -> dict[str, object]:
    return retained_object(
        json.loads(
            encode(
                ExecutionEvent(
                    event_id=uuid4(),
                    execution_id=uuid4(),
                    activation_id=uuid4(),
                    producer="authored",
                    sequence=1,
                    occurred_at=Timestamp.now().value,
                    elapsed_seconds=0.0,
                    payload=Diagnostic(
                        FailureCategory.INPUT,
                        Severity.ERROR,
                        "authored",
                        "fit",
                        (ExceptionFact("builtins.ValueError", "authored", "primary"),),
                        "trace",
                    ),
                ),
            ),
        ),
    )


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("category", "unknown"),
        ("severity", "unknown"),
        ("symptom", 1),
        ("stage", 1),
        ("traceback_text", 1),
        ("truncated", 1),
        ("exception_chain", None),
        ("exception_chain", [None]),
        ("exception_chain", [{}]),
        ("exception_chain", [{"type_name": "x", "message": 1, "relation": "primary"}]),
        ("root_cause", "a model-generated rationale"),
    ],
)
def test_diagnostic_codec_refuses_foreign_values(field: str, bad: object) -> None:
    """A serialized hypothesis or malformed chain cannot become factual diagnosis."""
    data = _diagnostic()
    payload = data["payload"]
    assert isinstance(payload, dict)
    payload[field] = bad
    with pytest.raises((ValueError, TypeError)):
        decode(json.dumps(data))


def test_closed_event_and_payload_membership() -> None:
    """Retained evidence never silently accepts extra fields or a different root."""
    for wire in ("[]", "{}", "null"):
        with pytest.raises(ValueError, match=r"object|fields"):
            decode(wire)
    data = _diagnostic()
    data["extra"] = "unadmitted"
    with pytest.raises(ValueError, match="event fields"):
        decode(json.dumps(data))
    del data["extra"]
    payload = data["payload"]
    assert isinstance(payload, dict)
    payload["extra"] = "unadmitted"
    with pytest.raises(ValueError, match="payload fields"):
        decode(json.dumps(data))
    del payload["extra"]
    assert (
        decode(json.dumps(data)).payload
        == decode(encode(decode(json.dumps(data)))).payload
    )


@pytest.mark.parametrize(
    ("reader", "bad"),
    [
        (retained_object, []),
        (retained_object, {1: "foreign key"}),
        (array, ()),
        (nonempty_text, ""),
        (nonempty_text, 1),
        (integer, True),
        (integer, 1.0),
        (optional_integer, "1"),
        (optional_boolean, 1),
        (optional_text, " "),
        (decode_references, [{}]),
        (_real, 1),
        (_real, True),
    ],
)
def test_wire_readers_preserve_exact_types(
    reader: Callable[[object], object],
    bad: object,
) -> None:
    """JSON-like shape alone is insufficient for a retained scientific value."""
    with pytest.raises(
        ValueError,
        match=r"requires|must|expected|declaration|unsupported|original",
    ):
        reader(bad)


def test_optional_wire_values_remain_explicitly_unknown() -> None:
    """Unknown values retain None; actual booleans and integers stay distinct."""
    assert optional_boolean(None) is None
    assert optional_boolean(value=False) is False
    assert optional_boolean(value=True) is True
    assert optional_integer(None) is None
    assert optional_integer(0) == 0
    assert optional_text(None) is None
    assert optional_text("authored") == "authored"
    assert decode_references([]) == ()
    assert strings([]) == ()
    assert strings(["authored"]) == ("authored",)
    assert _table(
        {
            "feature_names": ["x"],
            "rows": [[1.0]],
            "feature_value_kinds": ["continuous"],
        },
    ).rows == ((1.0,),)


def test_unknown_stored_values_and_extra_fact_fields_refuse() -> None:
    """The closed event serializer cannot smuggle arbitrary state or extra facts."""
    with pytest.raises(TypeError, match="unsupported stored value"):
        _default(object())
    data = _diagnostic()
    data["kind"] = "Admitted"
    data["payload"] = {
        "operation": "authored",
        "facts": [{"name": "source", "value": "authored", "extra": True}],
    }
    with pytest.raises(ValueError, match="invalid fact fields"):
        decode(json.dumps(data))


def test_unsupported_objects_have_no_implicit_scientific_serialization() -> None:
    """Serialize only declared scalar, identity and timestamp boundaries."""
    identity = uuid4()
    time = Timestamp.now().value
    value = {"id": identity, "time": time, "kind": NonValueKind.UNAVAILABLE}
    expected = {"id": str(identity), "time": time.isoformat(), "kind": "unavailable"}
    assert json_document(value) == expected
    assert document(value) == expected
    assert source_fingerprint(NonValueKind.UNAVAILABLE) == source_fingerprint(
        "unavailable",
    )
    for serializer in (source_fingerprint, json_document, document):
        with pytest.raises(TypeError, match="unsupported"):
            serializer(object())
    unavailable = LearningUnavailableError("optional numerical dependency absent")
    assert unavailable.observation.kind is NonValueKind.UNAVAILABLE
    assert unavailable.observation.reason_code == "numerical_dependencies_unavailable"
