# Copyright (c) 2026
"""Real SQLite transactions and adversarial scientific history inspections.

These are authored lifecycle controls, not scientific fits or replayed studies.
Faults alter only independently owned test databases, after genuine commits.
"""

from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from dataclasses import replace
from typing import TYPE_CHECKING, cast
from uuid import UUID, uuid4

import pytest

from devtools.core.time import Timestamp
from devtools.learning.evidence.context import ExecutionContext, RecordingError
from devtools.learning.evidence.events import (
    Activated,
    Admitted,
    Diagnostic,
    ExecutionEvent,
    Fact,
    FailureCategory,
    Lifecycle,
    Outcome,
    Payload,
    Progress,
    Severity,
    StageFinished,
    StageStarted,
    Terminal,
)
from devtools.learning.integrations.local._codec import decode, encode
from devtools.learning.integrations.local.ledger import (
    SQLiteExecutionRecorder,
    SQLiteInspectionSession,
    inspect_child_execution_ids,
    inspect_execution,
    inspect_execution_ids,
)

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path


def _event(
    context: ExecutionContext,
    sequence: int,
    payload: Payload,
) -> ExecutionEvent:
    return ExecutionEvent(
        event_id=uuid4(),
        execution_id=context.execution_id,
        activation_id=context.activation_id,
        producer="ledger-control",
        sequence=sequence,
        occurred_at=Timestamp.now().value,
        elapsed_seconds=0.0,
        payload=payload,
    )


def _history(database: Path) -> UUID:
    with SQLiteExecutionRecorder(database) as recorder:
        with ExecutionContext(recorder, Admitted("control")) as context:
            context.stage("rows", "Inspect authored rows", FailureCategory.INPUT)
            context.progress("rows", 1, 2)
            context.progress("rows", 2, 2)
        return context.execution_id


@pytest.mark.parametrize("bad", [-1, True, float("nan"), float("inf"), 31])
def test_invalid_timeout_cannot_create_store(tmp_path: Path, bad: float) -> None:
    """Refuse invalid admission limits before creating any file."""
    database = tmp_path / "history.sqlite"
    with pytest.raises(ValueError, match="timeout_seconds"):
        SQLiteExecutionRecorder(database, timeout_seconds=bad)
    assert not database.exists()


@pytest.mark.parametrize("bad", [True, 0, 262143, 2**31 + 1])
def test_invalid_storage_ceiling_cannot_create_store(tmp_path: Path, bad: int) -> None:
    """Require a finite explicit SQLite page budget before opening the store."""
    database = tmp_path / "history.sqlite"
    with pytest.raises(ValueError, match="file bound"):
        SQLiteExecutionRecorder(database, maximum_database_bytes=bad)
    assert not database.exists()


def test_recording_requires_live_single_writer_and_preserves_atomicity(
    tmp_path: Path,
) -> None:
    """Real lock contention and SQL rollback never fabricate a terminal success."""
    database = tmp_path / "history.sqlite"
    with SQLiteExecutionRecorder(database) as recorder:
        with pytest.raises(RecordingError, match="open execution recorder"):
            SQLiteExecutionRecorder(database)
        with closing(sqlite3.connect(database)) as connection, connection:
            connection.execute(
                "CREATE TRIGGER reject_terminal BEFORE INSERT ON events "
                "WHEN NEW.kind='Terminal' BEGIN "
                "SELECT RAISE(ABORT,'terminal rejected'); END",
            )
        context = ExecutionContext(recorder, Admitted("control"))
        with pytest.raises(RecordingError, match="terminal rejected"), context:
            context.completed()
        history = inspect_execution(database, context.execution_id)
        assert history is not None
        assert history.incomplete
        assert history.lifecycle is Lifecycle.RUNNING
        assert not any(isinstance(e.payload, Terminal) for e in history.events)
    with pytest.raises(RecordingError, match="closed"):
        recorder.record(_event(context, 1, Admitted("late")))


def test_duplicate_and_ordered_recording(tmp_path: Path) -> None:
    """Retrying one identical acknowledgment differs from executing a second effect."""
    with SQLiteExecutionRecorder(tmp_path / "history.sqlite") as recorder:
        context = ExecutionContext(recorder, Admitted("control"))
        admission = _event(context, 1, Admitted("control"))
        acknowledged = recorder.record(admission)
        assert acknowledged == recorder.record(admission)
        with pytest.raises(ValueError, match="Conflicting"):
            recorder.record(replace(admission, payload=Admitted("foreign")))
        with pytest.raises(ValueError, match="observation time"):
            recorder.record(
                replace(admission, event_id=uuid4(), observed_at=Timestamp.now().value),
            )
        with pytest.raises(ValueError, match="order"):
            recorder.record(_event(context, 3, Activated(1, "host", "3", "windows")))
        recorder.record(_event(context, 2, Activated(1, "host", "3", "windows")))
        recorder.record(_event(context, 3, StageStarted("fit", "Fit")))
        with pytest.raises(ValueError, match="finished stage"):
            recorder.record(_event(context, 4, Terminal(Outcome.COMPLETED)))
        recorder.record(_event(context, 4, Terminal(Outcome.FAILED)))
        with pytest.raises(ValueError, match="already terminal"):
            recorder.record(_event(context, 5, Terminal(Outcome.COMPLETED)))


@pytest.mark.parametrize(
    "payload,reason",
    [
        (Activated(1, "host", "3", "windows"), "twice"),
        (StageStarted("second", "Second"), "finish the active"),
        (StageFinished("foreign", 0.0), "match active stage"),
        (Progress("foreign", "rows"), "match active stage"),
        (
            Diagnostic(FailureCategory.INPUT, Severity.ERROR, "failure", "foreign"),
            "differs",
        ),
    ],
)
def test_invalid_transition_is_rolled_back(
    tmp_path: Path,
    payload: Payload,
    reason: str,
) -> None:
    """Reject conflicting live stages and preserve the last acknowledged sequence."""
    with SQLiteExecutionRecorder(tmp_path / "history.sqlite") as recorder:
        context = ExecutionContext(recorder, Admitted("control"))
        recorder.record(_event(context, 1, Admitted("control")))
        recorder.record(_event(context, 2, Activated(1, "host", "3", "windows")))
        recorder.record(_event(context, 3, StageStarted("fit", "Fit")))
        with pytest.raises(ValueError, match=reason):
            recorder.record(_event(context, 4, payload))
        recorder.record(_event(context, 4, Terminal(Outcome.FAILED)))
        history = inspect_execution(recorder.database, context.execution_id)
        assert history is not None
        assert len(history.events) == 4


@pytest.mark.parametrize(
    "payload",
    [
        Progress("rows", "bytes", 1, 2),
        Progress("rows", "rows", 0, 2),
        Progress("rows", "rows", None, None),
        Progress("rows", "rows", 1, 3),
    ],
)
def test_progress_cannot_change_unit_total_or_reverse(
    tmp_path: Path,
    payload: Progress,
) -> None:
    """The stored current-stage progress is the authority for monotonicity."""
    with SQLiteExecutionRecorder(tmp_path / "history.sqlite") as recorder:
        context = ExecutionContext(recorder, Admitted("control"))
        observations: tuple[Payload, ...] = (
            Admitted("control"),
            Activated(1, "h", "3", "w"),
            StageStarted("rows", "Rows"),
            Progress("rows", "rows", 1, 2),
        )
        for sequence, item in enumerate(observations, 1):
            recorder.record(_event(context, sequence, item))
        with pytest.raises(ValueError, match="preserve unit"):
            recorder.record(_event(context, 5, payload))


@pytest.mark.parametrize(
    "statement",
    [
        "DELETE FROM events WHERE sequence=3",
        "UPDATE executions SET lifecycle='pending',outcome=NULL",
        "UPDATE executions SET operation='foreign'",
        "UPDATE executions SET outcome='failed'",
        "UPDATE executions SET active_stage='foreign'",
        "UPDATE activations SET pid=12345678",
        "UPDATE activations SET ended_at=started_at",
        "UPDATE events SET document='{}' WHERE sequence=1",
        "UPDATE events SET kind='foreign' WHERE sequence=1",
        "UPDATE events SET id='foreign' WHERE sequence=1",
    ],
)
def test_corrupt_projection_cannot_be_accepted(tmp_path: Path, statement: str) -> None:
    """Independent inspection checks actual committed SQL and retained envelopes."""
    database = tmp_path / "history.sqlite"
    identity = _history(database)
    with closing(sqlite3.connect(database)) as connection, connection:
        connection.execute(statement)
    with pytest.raises(RecordingError):
        inspect_execution(database, identity)


def test_snapshot_identity_membership_order_and_children(tmp_path: Path) -> None:
    """A read-only owner has exact source, event ordering and child membership."""
    database = tmp_path / "history.sqlite"
    with SQLiteExecutionRecorder(database) as recorder:
        with ExecutionContext(recorder, Admitted("parent")) as parent:
            with ExecutionContext(recorder, Admitted("child"), parent=parent) as child:
                pass
    with SQLiteInspectionSession(database) as session:
        parent_history = inspect_execution(
            database,
            parent.execution_id,
            session=session,
        )
        assert parent_history is not None
        assert session.inspect_execution(parent.execution_id) is parent_history
        assert session.inspect_execution(uuid4()) is None
        assert inspect_child_execution_ids(
            database,
            parent.execution_id,
            session=session,
        ) == (child.execution_id,)
        assert inspect_execution_ids(database, session=session) == (
            parent.execution_id,
            child.execution_id,
        )
        assert session.execution_ids(operation="child") == (child.execution_id,)
        assert session.execution_ids(operation="absent") == ()
        first, last = (
            parent_history.events[0].event_id,
            parent_history.events[-1].event_id,
        )
        assert session.recorded_before(first, last)
        assert not session.recorded_before(last, first)
        assert session.child_execution_ids(child.execution_id) == ()
        with pytest.raises(ValueError, match="distinct"):
            session.recorded_before(first, first)
        with pytest.raises(ValueError, match="operation"):
            session.execution_ids(operation=" ")
        with pytest.raises(RecordingError, match="another database"):
            session.require_database(tmp_path / "foreign.sqlite")
    with pytest.raises(RecordingError, match="Closed"):
        session.execution_ids()
    with pytest.raises(RecordingError, match="single-use"), session:
        pytest.fail("reentered a consumed snapshot")


@pytest.mark.parametrize(
    "field,value",
    [
        ("kind", "foreign"),
        ("kind", 1),
        ("sequence", True),
        ("elapsed_seconds", False),
        ("producer", []),
        ("payload", []),
        ("schema_version", 2),
        ("observed_at", "invalid"),
        ("parent_execution_id", "invalid"),
        ("event_id", "invalid"),
    ],
)
def test_codec_refuses_malformed_envelope(
    tmp_path: Path,
    field: str,
    value: object,
) -> None:
    """The closed codec refuses malformed serialized scientific evidence."""
    with SQLiteExecutionRecorder(tmp_path / "history.sqlite") as recorder:
        context = ExecutionContext(recorder, Admitted("control"))
        event = _event(context, 1, Admitted("control"))
    data = json.loads(encode(event))
    data[field] = value
    with pytest.raises((ValueError, TypeError)):
        decode(json.dumps(data))


@pytest.mark.parametrize(
    "payload",
    [
        Admitted("control", (Fact("input", "x"),)),
        Activated(1, "host", "3", "windows"),
        StageStarted("fit", "Fit"),
        StageFinished("fit", 0.0),
        Progress("fit", "rows"),
        Progress("fit", "rows", 1, 2),
        Diagnostic(FailureCategory.NUMERICAL, Severity.ERROR, "authored failure"),
        Terminal(Outcome.CANCELLED),
    ],
)
def test_codec_roundtrip_keeps_typed_observation(
    tmp_path: Path,
    payload: Payload,
) -> None:
    """Round trips retain nominal IDs, typed non-success and original timing."""
    with SQLiteExecutionRecorder(tmp_path / "history.sqlite") as recorder:
        context = ExecutionContext(recorder, Admitted("control"))
        event = _event(context, 1, payload)
    assert decode(encode(event)) == event


@pytest.mark.parametrize(
    "changes",
    [
        {"event_id": "foreign"},
        {"parent_execution_id": 1},
        {"occurred_at": None},
        {"elapsed_seconds": float("nan")},
        {"elapsed_seconds": -1},
        {"producer": ""},
        {"sequence": 0},
        {"schema_version": True},
        {"payload": object()},
    ],
)
def test_event_contract_rejects_invalid_identity_and_time(
    tmp_path: Path,
    changes: dict[str, object],
) -> None:
    """Invalid constructor input cannot become a scientific event."""
    with SQLiteExecutionRecorder(tmp_path / "history.sqlite") as recorder:
        context = ExecutionContext(recorder, Admitted("control"))
        event = _event(context, 1, Admitted("control"))
    reconstruct = cast("Callable[..., ExecutionEvent]", replace)
    with pytest.raises((ValueError, TypeError)):
        reconstruct(event, **changes)
