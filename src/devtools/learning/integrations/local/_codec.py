# Copyright (c) 2026
"""Private version-one JSON translation; no runtime objects or dynamic registry."""

from __future__ import annotations

import json
from dataclasses import asdict, fields
from datetime import datetime
from typing import cast
from uuid import UUID

from devtools.learning.evidence.events import (
    Activated,
    Admitted,
    Diagnostic,
    ExceptionFact,
    ExecutionEvent,
    Fact,
    FailureCategory,
    Outcome,
    Payload,
    Progress,
    Severity,
    StageFinished,
    StageStarted,
    Terminal,
)
from devtools.learning.measurement.contracts import EvidenceReference


def _default(value: object) -> str:
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    msg = f"unsupported stored value: {type(value).__name__}"
    raise TypeError(msg)


def encode(event: ExecutionEvent) -> str:
    value = asdict(event)
    value["kind"] = event.kind
    return json.dumps(value, default=_default, allow_nan=False, sort_keys=True)


def _object(value: object) -> dict[str, object]:
    if not isinstance(value, dict) or any(not isinstance(k, str) for k in value):
        msg = "expected JSON object"
        raise ValueError(msg)
    return cast("dict[str, object]", value)


def _str(value: object) -> str:
    if not isinstance(value, str):
        msg = "expected text"
        raise ValueError(msg)
    return value


def _int(value: object) -> int:
    if type(value) is not int:
        msg = "expected integer"
        raise ValueError(msg)
    return value


def _number(value: object) -> float:
    if type(value) not in (int, float):
        msg = "expected number"
        raise ValueError(msg)
    return float(cast("float", value))


def _boolean(value: object) -> bool:
    if type(value) is not bool:
        msg = "expected boolean"
        raise ValueError(msg)
    return value


def _list(value: object) -> list[object]:
    if not isinstance(value, list):
        msg = "expected list"
        raise ValueError(msg)
    return cast("list[object]", value)


def _facts(value: object) -> tuple[Fact, ...]:
    result = []
    for item in _list(value):
        obj = _object(item)
        if set(obj) != {"name", "value"}:
            msg = "invalid fact fields"
            raise ValueError(msg)
        result.append(Fact(_str(obj["name"]), cast("str | int | float | bool | None", obj["value"])))
    return tuple(result)


def _optional_text(value: object) -> str | None:
    return None if value is None else _str(value)


def decode(text: str) -> ExecutionEvent:
    value = _object(json.loads(text))
    if set(value) != {f.name for f in fields(ExecutionEvent)} | {"kind"}:
        msg = "invalid event fields"
        raise ValueError(msg)
    p = _object(value["payload"])
    kind = _str(value["kind"])
    payload: Payload
    if kind == "Admitted":
        payload = Admitted(_str(p["operation"]), _facts(p["facts"]))
    elif kind == "Activated":
        payload = Activated(
            _int(p["process_id"]),
            _str(p["hostname"]),
            _str(p["python_version"]),
            _str(p["platform"]),
        )
    elif kind == "StageStarted":
        payload = StageStarted(
            _str(p["stage"]), _str(p["description"]), _facts(p["facts"]),
        )
    elif kind == "StageFinished":
        payload = StageFinished(_str(p["stage"]), _number(p["duration_seconds"]))
    elif kind == "Progress":
        payload = Progress(
            _str(p["stage"]),
            _str(p["unit"]),
            None if p["completed"] is None else _int(p["completed"]),
            None if p["total"] is None else _int(p["total"]),
        )
    elif kind == "Diagnostic":
        chain = []
        for item in _list(p["exception_chain"]):
            member = _object(item)
            if set(member) != {f.name for f in fields(ExceptionFact)}:
                msg = "invalid exception fields"
                raise ValueError(msg)
            chain.append(
                ExceptionFact(
                    _str(member["type_name"]),
                    _str(member["message"]),
                    _str(member["relation"]),
                ),
            )
        if p["root_cause"] is not None:
            msg = "unsupported causal assertion"
            raise ValueError(msg)
        payload = Diagnostic(
            FailureCategory(_str(p["category"])),
            Severity(_str(p["severity"])),
            _str(p["symptom"]),
            _optional_text(p["stage"]),
            tuple(chain),
            _optional_text(p["traceback_text"]),
            _boolean(p["truncated"]),
        )
    elif kind == "Terminal":
        payload = Terminal(Outcome(_str(p["outcome"])), _facts(p["facts"]))
    else:
        msg = "unsupported event kind"
        raise ValueError(msg)
    if set(p) != {f.name for f in fields(payload)}:
        msg = "invalid payload fields"
        raise ValueError(msg)
    return ExecutionEvent(
        event_id=UUID(_str(value["event_id"])),
        execution_id=UUID(_str(value["execution_id"])),
        activation_id=UUID(_str(value["activation_id"])),
        producer=_str(value["producer"]),
        sequence=_int(value["sequence"]),
        occurred_at=datetime.fromisoformat(_str(value["occurred_at"])),
        observed_at=None
        if value["observed_at"] is None
        else datetime.fromisoformat(_str(value["observed_at"])),
        elapsed_seconds=_number(value["elapsed_seconds"]),
        payload=payload,
        parent_execution_id=None
        if value["parent_execution_id"] is None
        else UUID(_str(value["parent_execution_id"])),
        schema_version=_int(value["schema_version"]),
    )


def retained_object(value: object) -> dict[str, object]:
    if type(value) is not dict or any(type(k) is not str for k in value):
        msg = "retained evidence requires an object with string keys"
        raise ValueError(msg)
    return cast("dict[str, object]", value)


def array(value: object) -> list[object]:
    if type(value) is not list:
        msg = "retained evidence requires a JSON array"
        raise ValueError(msg)
    return cast("list[object]", value)


def nonempty_text(value: object) -> str:
    if type(value) is not str or not value.strip():
        msg = "retained evidence requires nonempty text"
        raise ValueError(msg)
    return value


def optional_text(value: object) -> str | None:
    return None if value is None else nonempty_text(value)


def integer(value: object) -> int:
    if type(value) is not int:
        msg = "retained evidence requires an exact integer"
        raise ValueError(msg)
    return value


def optional_integer(value: object) -> int | None:
    return None if value is None else integer(value)


def optional_boolean(value: object) -> bool | None:
    if value is not None and type(value) is not bool:
        msg = "declaration must be boolean or unknown"
        raise ValueError(msg)
    return value


def strings(value: object) -> tuple[str, ...]:
    return tuple(nonempty_text(v) for v in array(value))


def decode_references(value: object) -> tuple[EvidenceReference, ...]:
    """Decode reference identities; source integrity is a separate owner check."""
    result = []
    for item in array(value):
        data = retained_object(item)
        if set(data) != {"relation", "identity", "sha256"}:
            msg = "unsupported evidence reference fields"
            raise ValueError(msg)
        result.append(
            EvidenceReference(
                nonempty_text(data["relation"]),
                nonempty_text(data["identity"]),
                optional_text(data["sha256"]),
            ),
        )
    return tuple(result)
