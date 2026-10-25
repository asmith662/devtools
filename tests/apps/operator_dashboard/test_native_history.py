# Copyright (c) 2026
"""The existing read-only projection consumes the worker's native captures."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from apps.operator_dashboard.details import turn_detail

if TYPE_CHECKING:
    from pathlib import Path


def test_native_history_and_tool_results_are_archived_not_invented(
    tmp_path: Path,
) -> None:
    """Keep exact role/call/result payloads behind the existing raw-data switch."""
    turn = tmp_path / "turn-01"
    turn.mkdir()
    feedback = '{"validation":{"tests":{"exit_code":1}},"status":"TESTS_FAILED"}'
    request = {
        "prompt": {
            "role": "messages",
            "content": "",
            "messages": [
                {"role": "assistant", "content": "recorded intent", "tool_calls": []},
                {"role": "tool", "content": feedback, "tool_call_id": "exact-id"},
            ],
        },
    }
    result = [
        {"call": {"provider_call_id": "exact-id"}, "result": {"status": "RETURNED"}},
    ]
    for name, value in (("request.json", request), ("tools.json", result)):
        (turn / name).write_text(json.dumps(value), encoding="utf-8")
    before = {p.name: p.read_bytes() for p in turn.iterdir()}
    detail = turn_detail(tmp_path, {"number": 1}, raw=True)
    assert "recorded intent" in detail["request_text"]["text"]
    assert "exact-id" in detail["tool_results"]["text"]
    assert detail["feedback"]["text"] == feedback
    hidden = turn_detail(tmp_path, {"number": 1}, raw=False)
    assert hidden["request_text"]["availability"] == "NOT_DISCLOSED"
    assert hidden["tool_results"]["availability"] == "NOT_DISCLOSED"
    assert before == {p.name: p.read_bytes() for p in turn.iterdir()}


@pytest.mark.parametrize(
    ("proposal", "call", "expected"),
    [
        (None, None, "NOT_ESTABLISHED"),
        ("id", None, "NOT_ESTABLISHED"),
        (None, "id", "NOT_ESTABLISHED"),
        ("", "", "NOT_ESTABLISHED"),
        (" ", " ", "NOT_ESTABLISHED"),
        (1, 1, "NOT_ESTABLISHED"),
        ("id", "other", "NOT_ESTABLISHED"),
        ("id", "id", "MATCH"),
    ],
)
def test_missing_or_noncomparable_call_ids_never_match(
    tmp_path: Path,
    proposal: object,
    call: object,
    expected: str,
) -> None:
    """Actual archived data-to-detail joins require two present opaque strings."""
    turn = tmp_path / "turn-01"
    turn.mkdir()
    response = {
        "tool_calls": [
            {"name": "read_file", "provider_call_id": call, "arguments_json": "{}"},
        ],
    }
    (turn / "response.json").write_text(json.dumps(response), encoding="utf-8")
    before = (turn / "response.json").read_bytes()
    detail = turn_detail(tmp_path, {"number": 1, "proposal_id": proposal}, raw=False)
    assert detail["proposal_correlation"] == expected
    assert (turn / "response.json").read_bytes() == before
