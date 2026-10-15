# Copyright (c) 2026
# ruff: noqa: PLR2004 -- explicit provider token-count fixtures
"""Usage capture does not confuse a completed turn with accepted science."""

import json

import pytest

from devtools.agents.integrations.codex.errors import CodexOutputError
from devtools.agents.integrations.codex.parsing import parse_codex_turn_output
from devtools.agents.integrations.codex.usage import capture_codex_usage


def test_all_categories_retained_without_overlapping_total() -> None:
    """Reported cache/reasoning subcategories are not added to another total."""
    raw = {
        "input_tokens": 100,
        "cached_input_tokens": 70,
        "cache_write_input_tokens": 3,
        "output_tokens": 40,
        "reasoning_output_tokens": 20,
    }
    events = [
        {"type": "thread.started", "thread_id": "thread"},
        {"type": "turn.started", "turn_id": "turn"},
        {"type": "item.completed", "item": {"type": "agent_message", "text": "x"}},
        {"type": "turn.completed", "usage": raw},
    ]
    stream = "\n".join(json.dumps(e) for e in events).encode()
    record = capture_codex_usage(stream)[0]
    assert json.loads(record.raw_json) == raw
    assert record.thread_id == "thread"
    assert record.turn_id == "turn"
    assert record.counts.input_tokens == 100
    assert record.counts.cached_input_tokens == 70
    assert record.counts.cache_write_tokens == 3
    assert record.counts.output_tokens == 40
    assert record.counts.reasoning_tokens == 20
    assert record.counts.total_tokens is None
    assert parse_codex_turn_output(stream).usage == (record,)
    # A later process/semantic failure does not erase completed-turn usage.
    assert capture_codex_usage(stream + b'\n{"type":"turn.failed"}') == (record,)


def test_absence_is_unknown_and_turn_rejection_has_no_zero_report() -> None:
    """No reported usage never implies a free invocation."""
    assert capture_codex_usage(b'{"type":"thread.started","thread_id":"x"}') == ()
    record = capture_codex_usage(b'\n{"type":"turn.completed"}\n')[0]
    assert record.counts.input_tokens is None
    assert record.counts.output_tokens is None
    assert record.raw_json == "{}"
    assert record.thread_id is None
    assert record.turn_id is None


@pytest.mark.parametrize(
    "stream",
    [
        b"\xff",
        b"[]",
        b"not-json",
        b'{"type":"thread.started","thread_id":3}',
        b'{"type":"turn.started","turn_id":3}',
        b'{"type":"turn.completed","usage":[]}',
        b'{"type":"turn.completed","usage":{"input_tokens":true}}',
        b'{"type":"turn.completed","usage":{"input_tokens":-1}}',
        b'{"type":"turn.completed"}\n{"type":"turn.completed"}',
        (
            b'{"type":"turn.started","turn_id":"x"}\n{"type":"turn.completed"}\n'
            b'{"type":"turn.started","turn_id":"x"}\n{"type":"turn.completed"}'
        ),
    ],
)
def test_invalid_or_duplicate_usage_fails(stream: bytes) -> None:
    """Do not charge duplicate events or coerce malformed counts."""
    with pytest.raises(CodexOutputError, match="usage stream"):
        capture_codex_usage(stream)


def test_distinct_turns_remain_distinct() -> None:
    """Identical numbers are not duplicate usage when different turns report them."""
    records = capture_codex_usage(
        b'{"type":"turn.started","turn_id":"a"}\n{"type":"turn.completed"}\n'
        b'{"type":"turn.started","turn_id":"b"}\n{"type":"turn.completed"}',
    )
    assert [record.ordinal for record in records] == [1, 2]


def test_optional_usage_failure_does_not_erase_valid_response() -> None:
    """Publication policy can require accounting without poisoning transport."""
    output = parse_codex_turn_output(
        b'{"type":"thread.started","thread_id":"thread"}\n'
        b'{"type":"item.completed","item":{"type":"agent_message","text":"valid"}}\n'
        b'{"type":"turn.completed","usage":{"input_tokens":false}}',
    )
    assert output.final_message == "valid"
    assert output.usage == ()
    assert output.usage_error is not None
