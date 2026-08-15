# Copyright (c) 2026
"""Tests for Codex JSONL parsing."""

from __future__ import annotations

import pytest

from devtools.codex.errors import CodexOutputError
from devtools.codex.parsing import parse_codex_turn_output


def test_parser_extracts_current_successful_jsonl_contract() -> None:
    """A completed thread yields its resumable id and final agent message."""
    output = parse_codex_turn_output(
        b'{"type":"thread.started","thread_id":"thread-42"}\n'
        b'{"type":"turn.started"}\n'
        b'{"type":"item.completed","item":{"type":"agent_message",'
        b'"text":"first"}}\n'
        b'{"type":"item.completed","item":{"type":"agent_message",'
        b'"text":" final response "}}\n'
        b'{"type":"turn.completed"}\n',
    )

    assert output.thread_id == "thread-42"
    assert output.final_message == " final response "


def test_parser_allows_recoverable_error_events_before_completion() -> None:
    """Current Codex reconnect errors are not terminal without turn.failed."""
    output = parse_codex_turn_output(
        b'{"type":"thread.started","thread_id":"thread-42"}\n'
        b'{"type":"error","message":"Reconnecting... 1/5"}\n'
        b'{"type":"item.completed","item":{"type":"agent_message",'
        b'"text":"recovered"}}\n'
        b'{"type":"turn.completed"}\n',
    )

    assert output.final_message == "recovered"


@pytest.mark.parametrize(
    ("stdout", "match"),
    [
        (b"not-json\n", "not valid JSON"),
        (b"[]\n", "not an object"),
        (b'{"type": 42}\n', "no string type"),
        (b'{"type":"thread.started"}\n', "no string 'thread_id'"),
        (b'{"type":"thread.started","thread_id":" "}\n', "blank"),
        (
            b'{"type":"thread.started","thread_id":" thread "}\n',
            "whitespace around",
        ),
        (
            b'{"type":"item.completed","item":[]}',
            "no object item",
        ),
        (
            (
                b'{"type":"thread.started","thread_id":"thread"}\n'
                b'{"type":"item.completed","item":{"type":"agent_message"}}\n'
            ),
            "no string 'text'",
        ),
        (
            (
                b'{"type":"thread.started","thread_id":"thread"}\n'
                b'{"type":"turn.failed"}\n'
            ),
            "failed turn",
        ),
        (
            (
                b'{"type":"item.completed","item":{"type":"notice"}}\n'
                b'{"type":"turn.completed"}\n'
            ),
            "did not include a thread.started",
        ),
        (
            (
                b'{"type":"thread.started","thread_id":"thread"}\n'
                b'{"type":"turn.completed"}\n'
            ),
            "did not include a completed agent message",
        ),
        (
            (
                b'\n{"type":"thread.started","thread_id":"thread"}\n'
                b'{"type":"item.completed","item":{"type":"agent_message",'
                b'"text":"answer"}}\n'
            ),
            "did not include turn.completed",
        ),
    ],
)
def test_parser_rejects_incomplete_or_invalid_protocol(
    stdout: bytes,
    match: str,
) -> None:
    """Only a complete successful Codex JSONL turn is accepted."""
    with pytest.raises(CodexOutputError, match=match):
        parse_codex_turn_output(stdout)


def test_parser_rejects_non_utf8_stdout() -> None:
    """Structured output must be UTF-8 JSONL."""
    with pytest.raises(CodexOutputError, match="UTF-8"):
        parse_codex_turn_output(b"\xff")
