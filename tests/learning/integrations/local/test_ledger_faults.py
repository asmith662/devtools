# Copyright (c) 2026
"""Independent inspection of actual committed SQLite history after owned corruption."""

from __future__ import annotations

import json
import os
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import TYPE_CHECKING, cast
from uuid import uuid4

import pytest

from devtools.learning.evidence.context import ExecutionContext, RecordingError
from devtools.learning.evidence.events import Admitted, Fact, StageStarted
from devtools.learning.integrations.local.ledger import (
    SQLiteExecutionRecorder,
    SQLiteInspectionSession,
    inspect_child_execution_ids,
    inspect_execution,
    inspect_execution_ids,
)
from tests.learning.integrations.local.test_ledger import _event, _history

if TYPE_CHECKING:
    from collections.abc import Callable


def _payload(
    database: Path,
    sequence: int,
    kind: str,
    payload: dict[str, object],
) -> None:
    """Replace only an owned event payload, keeping its SQL envelope consistent."""
    with closing(sqlite3.connect(database)) as connection, connection:
        row = connection.execute(
            "SELECT document FROM events WHERE sequence=?",
            (sequence,),
        ).fetchone()
        data = json.loads(row[0])
        data["kind"], data["payload"] = kind, payload
        connection.execute(
            "UPDATE events SET document=?,kind=? WHERE sequence=?",
            (json.dumps(data), kind, sequence),
        )


@pytest.mark.parametrize(
    ("sequence", "kind", "payload", "reason"),
    [
        (4, "Admitted", {"operation": "control", "facts": []}, "repeated admission"),
        (
            4,
            "StageStarted",
            {"stage": "second", "description": "Second", "facts": []},
            "Unfinished stage",
        ),
        (
            6,
            "StageFinished",
            {"stage": "foreign", "duration_seconds": 0.0},
            "Stage finish differs",
        ),
        (
            5,
            "Progress",
            {"stage": "rows", "unit": "rows", "completed": 0, "total": 2},
            "Invalid stage/progress",
        ),
        (
            5,
            "Progress",
            {"stage": "foreign", "unit": "rows", "completed": 2, "total": 2},
            "Invalid stage/progress",
        ),
        (
            2,
            "Progress",
            {"stage": "rows", "unit": "rows", "completed": 1, "total": 2},
            "active occurrence",
        ),
        (
            6,
            "Progress",
            {"stage": "rows", "unit": "rows", "completed": 2, "total": 2},
            "finished stage",
        ),
        (
            4,
            "Diagnostic",
            {
                "category": "input",
                "severity": "error",
                "symptom": "authored",
                "stage": "foreign",
                "exception_chain": [],
                "traceback_text": None,
                "truncated": False,
                "root_cause": None,
            },
            "Diagnostic differs",
        ),
    ],
)
def test_reader_rechecks_lifecycle_instead_of_trusting_projection(
    tmp_path: Path,
    sequence: int,
    kind: str,
    payload: dict[str, object],
    reason: str,
) -> None:
    """A completed projection cannot launder contradictory stored observations."""
    database = tmp_path / "science.sqlite"
    identity = _history(database)
    _payload(database, sequence, kind, payload)
    with pytest.raises(RecordingError, match=reason):
        inspect_execution(database, identity)


@pytest.mark.parametrize(
    "mutation",
    ["unacknowledged", "parent", "activation", "first-kind", "membership"],
)
def test_relationship_index_refuses_corrupt_original_admissions(
    tmp_path: Path,
    mutation: str,
) -> None:
    """Require an acknowledged live-parent admission for every indexed child."""
    database = tmp_path / "science.sqlite"
    identity = _history(database)
    with closing(sqlite3.connect(database)) as connection, connection:
        if mutation == "activation":
            connection.execute("DELETE FROM events WHERE sequence=1")
        elif mutation == "membership":
            connection.execute("DELETE FROM events")
        else:
            data = json.loads(
                connection.execute(
                    "SELECT document FROM events WHERE sequence=1",
                ).fetchone()[0],
            )
            if mutation == "unacknowledged":
                data["observed_at"] = None
            elif mutation == "parent":
                data["parent_execution_id"] = str(uuid4())
            else:
                data["kind"] = "StageStarted"
                data["payload"] = {"stage": "rows", "description": "Rows", "facts": []}
            connection.execute(
                "UPDATE events SET document=?,kind=? WHERE sequence=1",
                (json.dumps(data), data["kind"]),
            )
    with pytest.raises(
        RecordingError,
        match=r"Unacknowledged|relationship|admission|membership",
    ):
        inspect_child_execution_ids(database, identity)


def test_post_terminal_effects_cannot_hide_in_a_completed_source(
    tmp_path: Path,
) -> None:
    """A valid failed terminal may retain a stage, but no later progress is admitted."""
    database = tmp_path / "science.sqlite"
    identity = _history(database)
    _payload(database, 6, "Terminal", {"outcome": "failed", "facts": []})
    _payload(
        database,
        7,
        "Progress",
        {"stage": "rows", "unit": "rows", "completed": 2, "total": 2},
    )
    with closing(sqlite3.connect(database)) as connection, connection:
        data = json.loads(
            connection.execute(
                "SELECT document FROM events WHERE sequence=6",
            ).fetchone()[0],
        )
        connection.execute("UPDATE executions SET outcome='failed'")
        connection.execute("UPDATE activations SET ended_at=?", (data["occurred_at"],))
    with pytest.raises(RecordingError, match="after terminal"):
        inspect_execution(database, identity)


def test_missing_terminal_projection_and_foreign_keys_are_not_success(
    tmp_path: Path,
) -> None:
    """Reject projection constraints and foreign references independently."""
    database = tmp_path / "science.sqlite"
    identity = _history(database)
    with closing(sqlite3.connect(database)) as connection, connection:
        connection.execute("PRAGMA ignore_check_constraints=ON")
        connection.execute("UPDATE executions SET outcome=NULL")
    with pytest.raises(RecordingError, match=r"integrity|Terminal projection"):
        inspect_execution(database, identity)
    other = tmp_path / "foreign.sqlite"
    identity = _history(other)
    with closing(sqlite3.connect(other)) as connection, connection:
        connection.execute("UPDATE activations SET execution_id=?", (str(uuid4()),))
    with pytest.raises(RecordingError, match="foreign-key"):
        inspect_execution(other, identity)


@pytest.mark.parametrize("shape", ["version", "columns", "unrelated"])
def test_existing_schema_is_never_reinitialized(tmp_path: Path, shape: str) -> None:
    """An unrelated or incompatible database refuses without replacing its content."""
    database = tmp_path / "science.sqlite"
    with closing(sqlite3.connect(database)) as connection, connection:
        if shape == "columns":
            for name in ("executions", "activations", "events"):
                connection.execute("CREATE TABLE " + name + " (foreign_column)")
            connection.execute("PRAGMA user_version=1")
        elif shape == "unrelated":
            connection.execute("CREATE TABLE unrelated (x)")
        else:
            connection.execute("PRAGMA user_version=2")
    before = database.read_bytes()
    with pytest.raises(RecordingError, match="schema"):
        SQLiteExecutionRecorder(database)
    assert database.read_bytes() == before


def test_real_existing_database_cannot_shrink_below_its_page_budget(
    tmp_path: Path,
) -> None:
    """The declared file ceiling is checked against actual allocated SQLite pages."""
    database = tmp_path / "science.sqlite"
    with (
        SQLiteExecutionRecorder(database) as recorder,
        ExecutionContext(
            recorder,
            Admitted("authored", (Fact("oversized-control", "x" * (300 << 10)),)),
        ),
    ):
        pass
    with pytest.raises(RecordingError, match="explicit page ceiling"):
        SQLiteExecutionRecorder(database, maximum_database_bytes=262144)
    with SQLiteExecutionRecorder(database):
        pass


def test_unadmitted_occurrence_and_pending_stage_cannot_emit_effects(
    tmp_path: Path,
) -> None:
    """Refuse orphaned children and effects before valid activation."""
    with SQLiteExecutionRecorder(tmp_path / "science.sqlite") as recorder:
        context = ExecutionContext(recorder, Admitted("authored"))
        with pytest.raises(ValueError, match="first"):
            recorder.record(_event(context, 2, Admitted("authored")))
        with pytest.raises(ValueError, match="admitted activation"):
            recorder.record(_event(context, 2, StageStarted("rows", "Rows")))
        recorder.record(_event(context, 1, Admitted("authored")))
        with pytest.raises(ValueError, match="requires activation"):
            recorder.record(_event(context, 2, StageStarted("rows", "Rows")))
        remote = ExecutionContext(
            recorder,
            Admitted("child"),
            parent_execution_id=uuid4(),
        )
        with pytest.raises(RecordingError, match="did not acknowledge") as raised:
            remote.__enter__()
        assert isinstance(raised.value.__cause__, ValueError)
        assert "active recorded parent" in str(raised.value.__cause__)


def test_snapshot_source_change_and_missing_order_events_refuse(tmp_path: Path) -> None:
    """Expire changed read sources and refuse invented event ordering."""
    database = tmp_path / "science.sqlite"
    identity = _history(database)
    with SQLiteInspectionSession(database) as session:
        assert session.database == database.resolve()
        history = session.inspect_execution(identity)
        assert history is not None
        first = history.events[0].event_id
        with pytest.raises(RecordingError, match="ordering events missing"):
            session.recorded_before(first, uuid4())
    with SQLiteInspectionSession(database) as session:
        original = database.stat()
        os.utime(
            database,
            ns=(original.st_atime_ns, original.st_mtime_ns + 1_000_000_000),
        )
        with pytest.raises(RecordingError, match="expired"):
            session.inspect_execution(identity)
    assert inspect_execution_ids(database) == (identity,)


def test_invalid_reader_and_recorder_argument_types_refuse(tmp_path: Path) -> None:
    """No implicit path, UUID or event coercion creates scientific custody."""
    database = tmp_path / "science.sqlite"
    identity = _history(database)
    calls: tuple[tuple[Callable[..., object], tuple[object, ...]], ...] = (
        (SQLiteExecutionRecorder, ("foreign",)),
        (SQLiteInspectionSession, ("foreign",)),
        (inspect_execution, (database, "foreign")),
        (inspect_child_execution_ids, (database, "foreign")),
        (inspect_execution_ids, ("foreign",)),
    )
    for call, args in calls:
        with pytest.raises(TypeError, match=r"Path|UUID"):
            call(*args)
    with pytest.raises(ValueError, match="filesystem path"):
        SQLiteExecutionRecorder(Path(":memory:"))
    with (
        SQLiteExecutionRecorder(database) as recorder,
        pytest.raises(TypeError, match="ExecutionEvent"),
    ):
        cast("Callable[[object], object]", recorder.record)(None)
    with SQLiteInspectionSession(database) as session:
        for method in (session.inspect_execution, session.child_execution_ids):
            with pytest.raises(TypeError, match="UUID"):
                cast("Callable[[object], object]", method)(None)
        with pytest.raises(TypeError, match="UUID"):
            cast("Callable[..., object]", session.recorded_before)(identity, "foreign")
        with pytest.raises(TypeError, match="Path"):
            cast("Callable[..., object]", session.require_database)(None)
    with (
        pytest.raises(RecordingError, match="regular database"),
        SQLiteInspectionSession(tmp_path),
    ):
        pytest.fail("directory became a scientific ledger")
