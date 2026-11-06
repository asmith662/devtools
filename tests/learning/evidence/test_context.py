# Copyright (c) 2026
"""Actual committed effects versus missing or invalid scientific acknowledgments."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, cast
from uuid import uuid4

import pytest

from devtools.learning.evidence.context import ExecutionContext, RecordingError
from devtools.learning.evidence.events import (
    Admitted,
    Diagnostic,
    ExecutionEvent,
    FailureCategory,
    Outcome,
    Severity,
)
from devtools.learning.integrations.local.ledger import (
    SQLiteExecutionRecorder,
    inspect_execution,
)

if TYPE_CHECKING:
    from pathlib import Path


@dataclass
class _BadAcknowledgment:
    """Commit real SQL, then simulate only the return-channel corruption."""

    real: SQLiteExecutionRecorder
    kind: str
    fault: str
    previous: ExecutionEvent | None = None

    def record(self, event: ExecutionEvent) -> ExecutionEvent:
        """Never undo a potentially completed commit or automatically replay it."""
        committed = self.real.record(event)
        previous, self.previous = self.previous, committed
        if event.kind != self.kind:
            return committed
        if self.fault == "missing":
            return event
        if self.fault == "foreign":
            return replace(committed, event_id=uuid4())
        assert previous is not None
        return previous


def _attempt(context: ExecutionContext) -> None:
    with context:
        context.stage("rows", "Inspect authored rows", FailureCategory.INPUT)
        context.completed()


@pytest.mark.parametrize(
    ("kind", "fault"),
    [
        ("Admitted", "missing"),
        ("Admitted", "foreign"),
        ("Activated", "missing"),
        ("Activated", "foreign"),
        ("Activated", "stale"),
        ("StageStarted", "missing"),
        ("StageStarted", "foreign"),
        ("StageStarted", "stale"),
        ("Terminal", "missing"),
        ("Terminal", "foreign"),
        ("Terminal", "stale"),
    ],
)
def test_committed_effect_does_not_imply_acknowledged_acceptance(
    tmp_path: Path,
    kind: str,
    fault: str,
) -> None:
    """A bad return cannot authorize later computation or falsely acknowledge it."""
    database = tmp_path / "science.sqlite"
    with SQLiteExecutionRecorder(database) as recorder:
        context = ExecutionContext(
            _BadAcknowledgment(recorder, kind, fault),
            Admitted("authored"),
        )
        with pytest.raises(RecordingError, match="acknowledgment") as raised:
            _attempt(context)
    assert raised.value.execution_id == context.execution_id
    history = inspect_execution(database, context.execution_id)
    assert history is not None
    assert tuple(e.sequence for e in history.events) == tuple(
        range(1, len(history.events) + 1),
    )
    if kind == "Terminal":
        assert history.outcome is Outcome.COMPLETED
        assert raised.value.computation_outcome is Outcome.COMPLETED
    else:
        assert history.incomplete
        assert raised.value.computation_outcome is None
    # Only one effect exists, including when its acknowledgment was corrupted.
    assert sum(e.kind == kind for e in history.events) == 1


@pytest.mark.parametrize(
    "error",
    [KeyboardInterrupt("authored stop"), SystemExit("authored stop")],
)
def test_caught_process_interruption_is_not_success(
    tmp_path: Path,
    error: BaseException,
) -> None:
    """Observe real context termination while retaining the original interruption."""
    database = tmp_path / "science.sqlite"
    with SQLiteExecutionRecorder(database) as recorder:
        context = ExecutionContext(recorder, Admitted("authored"))

        def interrupt() -> None:
            with context:
                raise error

        with pytest.raises(type(error), match="authored stop"):
            interrupt()
    history = inspect_execution(database, context.execution_id)
    assert history is not None
    assert history.outcome is Outcome.INTERRUPTED
    diagnostics = [
        e.payload for e in history.events if isinstance(e.payload, Diagnostic)
    ]
    assert diagnostics[0].category is FailureCategory.INTERRUPTION
    assert diagnostics[0].root_cause is None


def test_parent_context_requires_live_shared_recorder_custody(tmp_path: Path) -> None:
    """Neither a stale parent nor a different writer can issue child lineage."""
    with (
        SQLiteExecutionRecorder(tmp_path / "first.sqlite") as first,
        SQLiteExecutionRecorder(tmp_path / "second.sqlite") as second,
    ):
        parent = ExecutionContext(first, Admitted("parent"))
        with pytest.raises(ValueError, match="active and nonterminal"):
            ExecutionContext(first, Admitted("child"), parent=parent)
        with parent:
            with pytest.raises(ValueError, match="share the required recorder"):
                ExecutionContext(second, Admitted("child"), parent=parent)
            with pytest.raises(ValueError, match="UUID and no live parent"):
                ExecutionContext(
                    first,
                    Admitted("child"),
                    parent=parent,
                    parent_execution_id=parent.execution_id,
                )
            with pytest.raises(ValueError, match="entered twice"):
                parent.__enter__()
            with pytest.raises(ValueError, match="active stage"):
                parent.progress("rows")
        with pytest.raises(ValueError, match="already terminal"):
            parent.__exit__(None, None, None)
        with pytest.raises(ValueError, match="active and nonterminal"):
            parent.completed()


def test_context_validates_request_and_current_stage_progress(tmp_path: Path) -> None:
    """Refused updates retain the original active stage and acknowledged progress."""
    with SQLiteExecutionRecorder(tmp_path / "science.sqlite") as recorder:
        with pytest.raises(TypeError, match="request must use Admitted"):
            ExecutionContext(recorder, cast("Admitted", None))
        with ExecutionContext(recorder, Admitted("authored")) as context:
            assert context.active_stage is None
            context.stage("rows", "Inspect rows", FailureCategory.INPUT)
            assert context.active_stage == "rows"
            context.progress("rows", 1, 2)
            with pytest.raises(ValueError, match="monotone"):
                context.progress("rows", 0, 2)
            context.diagnostic(
                Diagnostic(
                    FailureCategory.INPUT, Severity.WARNING, "authored warning", "rows",
                ),
            )
            context.progress("rows", 2, 2)
        with (
            pytest.raises(TypeError, match="category must use FailureCategory"),
            ExecutionContext(recorder, Admitted("invalid-category")) as invalid,
        ):
            invalid.stage("rows", "Rows", cast("FailureCategory", "input"))
