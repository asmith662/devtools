# Copyright (c) 2026
"""Authored negative contracts; these constructor controls perform no native fits."""

from __future__ import annotations

from dataclasses import replace
from datetime import timedelta, timezone
from typing import TYPE_CHECKING, cast
from uuid import uuid4

import pytest

from devtools.core.time import Timestamp
from devtools.learning.evidence.context import exception_diagnostic
from devtools.learning.evidence.events import (
    Activated,
    Admitted,
    Diagnostic,
    ExceptionFact,
    ExecutionEvent,
    Fact,
    FailureCategory,
    Outcome,
    Progress,
    Severity,
    StageFinished,
    StageStarted,
    Terminal,
)
from devtools.learning.investigation.classification.contracts import (
    ExecutionAuthorization,
)
from devtools.learning.measurement.contracts import (
    EvidenceReference,
    NonValueKind,
    NoValue,
    validate_references,
)

if TYPE_CHECKING:
    from collections.abc import Callable


def _prototype(kind: str) -> object:
    now = Timestamp.now().value
    return {
        "fact": Fact("rows", 1),
        "admitted": Admitted("authored", (Fact("source", "authored"),)),
        "activated": Activated(1, "host", "3", "windows"),
        "started": StageStarted("rows", "Inspect rows"),
        "finished": StageFinished("rows", 0.0),
        "progress": Progress("rows", "rows", 1, 2),
        "exception": ExceptionFact("builtins.ValueError", "authored", "primary"),
        "diagnostic": Diagnostic(FailureCategory.INPUT, Severity.ERROR, "authored"),
        "terminal": Terminal(Outcome.COMPLETED),
        "nonvalue": NoValue(
            NonValueKind.UNAVAILABLE,
            "authored",
            "Unavailable control",
        ),
        "reference": EvidenceReference("source", "authored", "0" * 64),
        "grant": ExecutionAuthorization(
            "authored",
            ("a", "b"),
            EvidenceReference("authority", "authored"),
        ),
        "event": ExecutionEvent(
            event_id=uuid4(),
            execution_id=uuid4(),
            activation_id=uuid4(),
            producer="authored",
            sequence=1,
            occurred_at=now,
            elapsed_seconds=0.0,
            payload=Admitted("authored"),
        ),
    }[kind]


@pytest.mark.parametrize(
    ("kind", "field", "bad"),
    [
        ("fact", "name", ""),
        ("fact", "name", None),
        ("fact", "value", object()),
        ("fact", "value", []),
        ("fact", "value", float("nan")),
        ("fact", "value", float("inf")),
        ("admitted", "operation", ""),
        ("admitted", "facts", []),
        ("admitted", "facts", (object(),)),
        ("admitted", "facts", (Fact("x", 1), Fact("x", 2))),
        ("activated", "process_id", 0),
        ("activated", "process_id", -1),
        ("activated", "process_id", True),
        ("activated", "hostname", ""),
        ("activated", "python_version", ""),
        ("activated", "platform", ""),
        ("started", "stage", ""),
        ("started", "description", ""),
        ("started", "facts", []),
        ("finished", "stage", ""),
        ("finished", "duration_seconds", -1),
        ("finished", "duration_seconds", float("nan")),
        ("finished", "duration_seconds", True),
        ("progress", "completed", -1),
        ("progress", "completed", True),
        ("progress", "completed", 3),
        ("progress", "completed", None),
        ("progress", "total", -1),
        ("progress", "total", False),
        ("progress", "unit", ""),
        ("progress", "stage", ""),
        ("exception", "type_name", ""),
        ("exception", "message", None),
        ("exception", "relation", "hypothesis"),
        ("diagnostic", "category", "input"),
        ("diagnostic", "severity", "error"),
        ("diagnostic", "symptom", ""),
        ("diagnostic", "stage", ""),
        ("diagnostic", "exception_chain", []),
        ("diagnostic", "exception_chain", (object(),)),
        ("diagnostic", "traceback_text", 1),
        ("diagnostic", "truncated", 1),
        ("diagnostic", "root_cause", "model hypothesis"),
        ("terminal", "outcome", "completed"),
        ("terminal", "facts", []),
        ("nonvalue", "kind", "unavailable"),
        ("nonvalue", "reason_code", ""),
        ("nonvalue", "detail", ""),
        ("nonvalue", "diagnostic_event_id", "foreign"),
        ("reference", "relation", ""),
        ("reference", "identity", ""),
        ("reference", "sha256", "F" * 64),
        ("reference", "sha256", "0" * 63),
        ("reference", "sha256", 1),
        ("grant", "authority", None),
        ("grant", "candidate_ids", []),
        ("grant", "candidate_ids", ()),
        ("grant", "candidate_ids", ("a", "a")),
        ("grant", "candidate_ids", ("b", "a")),
        ("grant", "plan_identity", ""),
        ("event", "event_id", "foreign"),
        ("event", "execution_id", 1),
        ("event", "activation_id", None),
        ("event", "parent_execution_id", 1),
        ("event", "schema_version", True),
        ("event", "schema_version", 2),
        ("event", "producer", ""),
        ("event", "sequence", 0),
        ("event", "sequence", True),
        ("event", "occurred_at", None),
        ("event", "elapsed_seconds", -1),
        ("event", "elapsed_seconds", True),
        ("event", "elapsed_seconds", float("nan")),
        ("event", "payload", object()),
    ],
)
def test_invalid_scientific_contract_has_no_typed_observation(
    kind: str,
    field: str,
    bad: object,
) -> None:
    """Wrong types, invented causes and contradictory identities are refused."""
    reconstruct = cast("Callable[..., object]", replace)
    with pytest.raises((ValueError, TypeError)):
        reconstruct(_prototype(kind), **{field: bad})


def test_occurrence_ids_and_time_cannot_be_conflated() -> None:
    """Parent, activation and execution remain distinct and timestamps UTC."""
    event = _prototype("event")
    assert isinstance(event, ExecutionEvent)
    with pytest.raises(ValueError, match="must differ"):
        replace(event, activation_id=event.execution_id)
    with pytest.raises(ValueError, match="different execution"):
        replace(event, parent_execution_id=event.execution_id)
    for time in (
        event.occurred_at.replace(tzinfo=None),
        event.occurred_at.replace(tzinfo=timezone(timedelta(hours=1))),
    ):
        with pytest.raises(ValueError, match="timezone-aware UTC"):
            replace(event, observed_at=time)
    parent = uuid4()
    assert replace(event, parent_execution_id=parent).parent_execution_id == parent


@pytest.mark.parametrize("references", [[], (object(),)])
def test_reference_collection_cannot_alias_mutable_or_foreign_objects(
    references: object,
) -> None:
    """A reference tuple validates attribution, without claiming source integrity."""
    validate = cast("Callable[[object], None]", validate_references)
    with pytest.raises(TypeError, match="immutable tuple"):
        validate(references)
    validate_references(())
    validate_references((EvidenceReference("authored", "source"),))


def test_exception_cause_and_context_are_observations_not_root_causes() -> None:
    """Retain both chain relations while leaving scientific causation unknown."""
    cause = ArithmeticError("actual cause")
    error = ValueError("primary")
    error.__cause__ = cause
    diagnostic = exception_diagnostic(error, FailureCategory.NUMERICAL, "measure")
    assert tuple(item.relation for item in diagnostic.exception_chain) == (
        "primary",
        "cause",
    )
    assert diagnostic.root_cause is None
    assert not diagnostic.truncated
    error.__cause__ = None
    error.__suppress_context__ = False
    error.__context__ = cause
    diagnostic = exception_diagnostic(error, FailureCategory.INPUT, None)
    assert tuple(item.relation for item in diagnostic.exception_chain) == (
        "primary",
        "context",
    )
    error.__suppress_context__ = True
    assert (
        len(exception_diagnostic(error, FailureCategory.INPUT, None).exception_chain)
        == 1
    )
    empty = exception_diagnostic(ValueError(), FailureCategory.INPUT, None)
    assert empty.symptom == "ValueError"


def test_exception_evidence_is_finitely_bounded_even_for_cycles() -> None:
    """Bound oversized diagnostics and retain explicit truncation."""
    error = ValueError("x" * 5000)
    cursor: BaseException = error
    for index in range(10):
        following = ValueError(str(index))
        cursor.__cause__ = following
        cursor = following
    diagnostic = exception_diagnostic(error, FailureCategory.INPUT, None)
    expected_depth = 8
    expected_message_limit = 4000
    assert diagnostic.truncated
    assert len(diagnostic.exception_chain) == expected_depth
    assert len(diagnostic.exception_chain[0].message) == expected_message_limit
    cursor.__cause__ = error
    assert exception_diagnostic(error, FailureCategory.INPUT, None).truncated
