# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- authored event facts; no model invocation
"""Available structured command reports, conservative merging and privacy."""

from __future__ import annotations

import json
from dataclasses import asdict, replace
from typing import Any

import pytest

from devtools.agents.integrations.codex.commands import (
    CodexCommandObserver,
    project_known_command,
)
from devtools.agents.integrations.codex.errors import CodexOutputError
from devtools.observability.commands.models import CommandOrigin
from devtools.observability.commands.patterns import summarize_patterns

ORIGIN = CommandOrigin("codex-worker", "task", "cli-invocation", "commands")


def event(kind: str = "item.completed", /, **fields: object) -> bytes:
    return json.dumps(
        {"type": kind, "item": {"id": "item_1", "type": "command_execution", **fields}},
    ).encode()


@pytest.mark.parametrize("order", ["normal", "reverse", "partial", "repeat"])
def test_known_reports_and_out_of_order_partial_fields(order: str) -> None:
    observer = CodexCommandObserver(ORIGIN)
    start = event(
        "item.started",
        command="git status --porcelain=v1 -z",
        status="in_progress",
    )
    done = event(
        exit_code=0,
        status="completed",
        **({} if order == "partial" else {"command": "git status --porcelain=v1 -z"}),
    )
    rows = [done, start] if order == "reverse" else [start, done]
    if order == "repeat":
        rows *= 2
    for row in rows:
        observer.feed(row)
    observer.feed(b'{"type":"turn.completed"}')
    report = observer.report()
    assert report.terminal_observed
    assert report.malformed_records == 0
    assert len(report.observations) == 1
    value = report.observations[0]
    assert value.outcome == "succeeded"
    assert value.exit_code == 0
    assert value.entered is None
    assert value.duration is None
    assert value.origin == replace(ORIGIN, call="commands/item_1")
    assert value.pattern.family == "git"
    assert value.pattern.operation == "status"
    assert not value.capture_incomplete
    assert summarize_patterns((value, value))[0].frequency == 1


@pytest.mark.parametrize(
    "fault",
    [
        "unknown",
        "missing-end",
        "no-exit",
        "failure",
        "command-conflict",
        "exit-conflict",
        "status-conflict",
    ],
)
def test_unknown_or_conflicting_outcomes(fault: str) -> None:
    observer = CodexCommandObserver(ORIGIN)
    observer.feed(
        event("item.started", command="git diff --check", status="in_progress"),
    )
    if fault != "missing-end":
        observer.feed(
            event(
                status="completed",
                **(
                    {}
                    if fault == "no-exit"
                    else {"exit_code": 9 if fault == "failure" else 0}
                ),
            ),
        )
    if fault == "command-conflict":
        observer.feed(
            event(command="PRIVATE_SENTINEL shell", exit_code=0, status="completed"),
        )
    elif fault == "exit-conflict":
        observer.feed(event(exit_code=7, status="completed"))
    elif fault == "status-conflict":
        observer.feed(event(exit_code=0, status="failed"))
    if fault == "unknown":
        # A finished turn with a command item does not supply missing process facts.
        observer.feed(
            event("item.started", id="item_2", command="unknown PRIVATE_SENTINEL"),
        )
    observer.feed(b'{"type":"turn.failed"}')
    value = observer.report().observations[0]
    if "conflict" in fault:
        assert value.outcome == "conflict"
        assert value.exit_code is None
    elif fault in {"missing-end", "no-exit"}:
        assert value.outcome == "unknown"
        assert value.exit_code is None
    elif fault == "failure":
        assert value.outcome == "failed"
        assert value.exit_code == 9
    else:
        assert value.outcome == "succeeded"
        assert observer.report().observations[1].outcome == "unknown"
    assert value.entered is None
    assert value.duration is None
    assert "PRIVATE_SENTINEL" not in json.dumps(asdict(observer.report()))


@pytest.mark.parametrize(
    "line",
    [
        b"not json PRIVATE_SENTINEL",
        b"[]",
        b"{}",
        b"\xff",
        b'{"type":"x","type":"y"}',
        b'{"type":"item.started","item":[]}',
        event(id=None),
        event(command=12),
        event(exit_code=True),
        event(status="mystery"),
        b'{"type":"item.started","item":{"id":"x","type":"command_execution","priv\\u0061te":1,"private":2}}',
        b'{"type":"x","value":NaN}',
    ],
)
def test_malformed_event_safe_failure_preserves_prefix(line: bytes) -> None:
    observer = CodexCommandObserver(ORIGIN)
    observer.feed(event("item.started", command="git diff --check"))
    with pytest.raises(CodexOutputError) as failure:
        observer.feed(line)
    assert "PRIVATE_SENTINEL" not in str(failure.value)
    report = observer.report()
    assert report.malformed_records == 1
    assert len(report.observations) == 1
    assert report.observations[0].capture_incomplete
    assert report.observations[0].outcome == "unknown"


def test_private_payload_never_enters_patterns_or_report() -> None:
    observer = CodexCommandObserver(ORIGIN)
    observer.feed(
        event(
            command="python -c PRIVATE_SENTINEL",
            aggregated_output="PRIVATE_SENTINEL",
            exit_code=0,
            status="completed",
        ),
    )
    observer.feed(
        b'{"type":"item.completed","item":{"type":"agent_message","text":"PRIVATE_SENTINEL"}}',
    )
    observer.feed(b'{"type":"thread.started","thread_id":"PRIVATE_SENTINEL"}')
    result = observer.report()
    assert result.observations[0].pattern.family == "unknown"
    assert "PRIVATE_SENTINEL" not in json.dumps(asdict(result))
    assert "PRIVATE_SENTINEL" not in json.dumps(
        [asdict(x) for x in summarize_patterns(result.observations)],
    )
    assert not result.terminal_observed
    assert result.observations[0].capture_incomplete


def test_json_decoder_recursion_failure_is_controlled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Native decoders differ across Python versions; inject the decoder failure,
    # rather than assuming a particular supported maximum nesting depth.
    def fail(*_args: object, **_kwargs: object) -> object:
        raise RecursionError

    monkeypatch.setattr(json, "loads", fail)
    observer = CodexCommandObserver(ORIGIN)
    with pytest.raises(CodexOutputError, match="malformed"):
        observer.feed(
            b'{"type":"other"}',
        )
    assert observer.report().malformed_records == 1


def test_unrecognized_private_item_identity_is_not_captured() -> None:
    observer = CodexCommandObserver(ORIGIN)
    with pytest.raises(CodexOutputError, match="malformed"):
        observer.feed(
            event(id="PRIVATE_SENTINEL", command="git diff --check", exit_code=0),
        )
    assert observer.report().observations == ()
    assert "PRIVATE_SENTINEL" not in json.dumps(asdict(observer.report()))


def test_missing_all_command_items_is_not_negative_execution_evidence() -> None:
    observer = CodexCommandObserver(ORIGIN)
    observer.feed(b'{"type":"turn.completed"}')
    report = observer.report()
    assert report.observations == ()
    assert report.terminal_observed  # feed coverage remains explicitly unclaimed


def test_missing_terminal_status_and_foreign_payload_association() -> None:
    first, second = (
        CodexCommandObserver(ORIGIN),
        CodexCommandObserver(replace(ORIGIN, task="other-task", run="other-run")),
    )
    for observer in (first, second):
        observer.feed(
            event(
                command="git diff --check",
                exit_code=0,
                task="FOREIGN_PRIVATE",
                agent="FOREIGN_PRIVATE",
            ),
        )
    a, b = first.report().observations[0], second.report().observations[0]
    assert a.outcome == "succeeded"
    assert a.origin.task == "task"
    assert b.origin.task == "other-task"
    assert a.origin != b.origin
    patterns = summarize_patterns((a, b))
    assert patterns[0].frequency == patterns[0].distinct_tasks == 2
    assert "FOREIGN_PRIVATE" not in json.dumps([asdict(x) for x in patterns])


@pytest.mark.parametrize("status", ["failed", "in_progress"])
def test_contradictory_completed_item_does_not_claim_success(status: str) -> None:
    observer = CodexCommandObserver(ORIGIN)
    observer.feed(event(status=status, exit_code=0))
    assert observer.report().observations[0].outcome == "conflict"


@pytest.mark.parametrize("fault", ["line", "records", "zero", "origin", "projection"])
def test_bounded_inputs_and_projection(fault: str) -> None:
    if fault == "zero":
        with pytest.raises(ValueError, match="bounds"):
            CodexCommandObserver(ORIGIN, maximum_records=0)
        return
    project: Any = (
        (lambda _c: "PRIVATE_SENTINEL")
        if fault == "projection"
        else project_known_command
    )
    observer = CodexCommandObserver(
        replace(ORIGIN, call="a" * 128) if fault == "origin" else ORIGIN,
        maximum_line_bytes=1 if fault == "line" else 65536,
        maximum_records=1 if fault == "records" else 4096,
        project=project,
    )
    if fault == "records":
        observer.feed(b'{"type":"turn.started"}')
    with pytest.raises(CodexOutputError):
        observer.feed(event(command="git diff --check"))
    assert observer.report().malformed_records == 1


@pytest.mark.parametrize(
    "command",
    [
        "git diff --check",
        "git diff --check HEAD",
        "git status --porcelain",
        "git status --porcelain=v1 -z",
        "git status; PRIVATE_SENTINEL",
        "bash -lc ls",
    ],
)
def test_finite_projection_does_not_parse_arbitrary_shell(command: str) -> None:
    value = project_known_command(command)
    assert value.family == (
        "git" if command.startswith("git") and ";" not in command else "unknown"
    )
