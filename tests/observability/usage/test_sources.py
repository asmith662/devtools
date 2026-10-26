# Copyright (c) 2026
# ruff: noqa: ANN401, PLR2004, PT018, PT011 -- synthetic metadata fixtures
"""Safe local usage metadata ingestion and budget/forecast failure contracts."""

import json
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any

import pytest

from devtools.agents.integrations.codex.sessions import (
    read_exec_usage,
    read_session_usage,
)
from devtools.core.time import Timestamp
from devtools.governance.usage import BudgetScope, UsageAmount, UsageBudget
from devtools.models.interaction.usage import ModelUsage
from devtools.observability.evidence.invocation import (
    Availability,
    ExecutionOrigin,
    InvocationMeasurement,
    Measured,
)
from devtools.observability.usage import UsageWindow, report
from devtools.observability.usage.forecast import forecast
from devtools.observability.usage.ingestion import (
    from_capture,
    from_session,
    measurement,
)

AT = Timestamp.from_isoformat("2026-10-15T12:00:00Z")


def measured(**changes: Any) -> InvocationMeasurement:
    """One synthetic typed existing invocation measurement."""

    def known(v: Any) -> Measured[Any]:
        return Measured(v, Availability.REPORTED, "synthetic metadata")

    unknown: Measured[Any] = Measured(None, Availability.UNKNOWN, "unavailable")
    value = InvocationMeasurement(
        backend="Codex",
        provider="OpenAI",
        execution_profile="SEMANTIC_WORKER",
        requested_model="fake",
        reported_model=unknown,
        reasoning_effort="High",
        task_id="synthetic",
        invocation_id="inv",
        backend_thread_id=known("thread"),
        backend_turn_id=known("turn"),
        disclosed_chars=known(100),
        disclosed_bytes=known(100),
        disclosure_digest="abc",
        usage=ModelUsage(
            input_tokens=1000,
            cached_input_tokens=0,
            cache_write_tokens=0,
            output_tokens=30,
            reasoning_tokens=2,
        ),
        usage_provenance="turn completed",
        raw_provider_usage_json="[]",
        model_turns=known(1),
        observed_tool_calls=known(0),
        subprocesses=unknown,
        wall_seconds=known(2.0),
        model_seconds=unknown,
        completed=True,
        validated=True,
        accepted=True,
        failure_class=None,
        execution_origin=ExecutionOrigin.EXECUTED,
        response_chars=known(10),
        response_bytes=known(10),
    )
    return replace(value, **changes)


def test_metadata_only_session(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Private event bodies are never JSON-decoded or retained by the importer."""
    records = [
        {"type": "event_msg", "payload": {"type": "heartbeat"}},
        {
            "timestamp": str(AT),
            "ordinal": 0,
            "type": "session_meta",
            "payload": {
                "model_provider": "openai",
                "cwd": "C:/work/project",
                "base_instructions": {"text": "PRIVATE_SENTINEL"},
            },
        },
        {
            "timestamp": str(AT),
            "type": "turn_context",
            "payload": {
                "model": "fake",
                "effort": "High",
                "developer_instructions": "PRIVATE_SENTINEL",
            },
        },
        {
            "timestamp": str(AT),
            "type": "response_item",
            "payload": {"content": "PRIVATE_SENTINEL"},
        },
        {
            "timestamp": str(AT),
            "type": "token_usage_record",
            "payload": {
                "thread_id": "t",
                "turn_id": "u",
                "response_id": "r",
                "usage": {
                    "input_tokens": 10,
                    "cached_input_tokens": 2,
                    "cache_write_input_tokens": 0,
                    "output_tokens": 4,
                    "reasoning_output_tokens": 1,
                },
                "turn_token_usage": {
                    "input_tokens": 10,
                    "cached_input_tokens": 2,
                    "cache_write_input_tokens": 0,
                    "output_tokens": 4,
                    "reasoning_output_tokens": 1,
                },
            },
        },
        {
            "timestamp": str(AT),
            "type": "token_usage_record",
            "payload": {"content": "PRIVATE_SENTINEL"},
        },
        {
            "timestamp": str(AT),
            "type": "event_msg",
            "payload": {
                "type": "task_complete",
                "turn_id": "u",
                "last_agent_message": "PRIVATE_SENTINEL",
            },
        },
    ]
    path = tmp_path / "rollout.jsonl"
    path.write_text(
        "\n".join(json.dumps(r) for r in records)
        + "\n{}\n"
        + json.dumps({"type": "token_usage_record", "payload": {"thread_id": "t"}}),
        encoding="utf-8",
    )
    original = json.loads

    def safe(raw: Any, **kwargs: Any) -> Any:
        assert "PRIVATE_SENTINEL" not in str(raw)
        return original(raw, **kwargs)

    monkeypatch.setattr(json, "loads", safe)
    rows = read_session_usage(path)
    assert len(rows) == 1 and rows[0].completed and rows[0].requested_model == "fake"
    assert rows[0].usage.reasoning_tokens == 1 and rows[0].project == "project"
    observations = from_session(path)
    assert len(observations) == 2
    result = report(
        observations,
        UsageWindow.rolling(Timestamp.from_isoformat("2026-10-15T13:00:00Z")),
    )
    assert result["fresh_invocations"] == 1 and result["tokens"]["input_tokens"] == 10
    assert "PRIVATE_SENTINEL" not in str(observations)


def test_unknown_session_shapes(tmp_path: Path) -> None:
    """Unknown metadata fields and absent identities are never inferred."""
    path = tmp_path / "other.jsonl"
    path.write_text(
        "\n".join(
            json.dumps(v)
            for v in [
                {"type": "session_meta", "payload": {}},
                {"type": "turn_context", "payload": {"reasoning_effort": "low"}},
                {"type": "event_msg", "payload": {"type": "task_complete"}},
                {
                    "type": "token_usage_record",
                    "payload": {
                        "thread_id": "x",
                        "turn_id": "y",
                        "response_id": "z",
                        "secret": "not allowed",
                    },
                },
                {"type": "token_usage_record", "payload": {"thread_id": "x"}},
            ]
        ),
        encoding="utf-8",
    )
    assert read_session_usage(path) == ()
    path.write_text(
        json.dumps(
            {
                "type": "token_usage_record",
                "timestamp": str(AT),
                "payload": {
                    "thread_id": "t",
                    "turn_id": "u",
                    "response_id": "r",
                    "usage": {},
                    "turn_token_usage": {},
                },
            },
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="provider"):
        read_session_usage(path)


def test_exec_metadata_reuses_parser_without_content(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Only native identity/completion metadata reaches the existing parser."""
    path = tmp_path / "stdout.log"
    path.write_text(
        "\n".join(
            json.dumps(v)
            for v in [
                {"type": "thread.started", "thread_id": "t"},
                {"type": "turn.started", "turn_id": "u"},
                {
                    "type": "item.completed",
                    "item": {"type": "agent_message", "text": "PRIVATE_SENTINEL"},
                },
                {
                    "type": "turn.completed",
                    "usage": {"input_tokens": 10, "output_tokens": 2},
                },
            ]
        ),
        encoding="utf-8",
    )
    original = json.loads

    def safe(raw: Any, **kwargs: Any) -> Any:
        assert "PRIVATE_SENTINEL" not in str(raw)
        return original(raw, **kwargs)

    monkeypatch.setattr(json, "loads", safe)
    rows = read_exec_usage(path)
    assert len(rows) == 1 and rows[0].counts.input_tokens == 10
    assert rows[0].counts.reasoning_tokens is None
    path.write_text(
        json.dumps({"type": "turn.completed", "private": "PRIVATE_SENTINEL"}),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="Unsupported"):
        read_exec_usage(path)


def test_capture_restore_and_acceptance() -> None:
    """Provider capture restored exactly; domain rejection differs from transport."""
    value: dict[str, Any] = {"measurement": asdict(measured(accepted=False))}
    older = {"measurement": dict(value["measurement"])}
    older["measurement"].pop("response_chars")
    older["measurement"].pop("response_bytes")
    assert measurement(older).response_bytes.value is None
    assert measurement(value) == measured(accepted=False)
    row = from_capture(value, timestamp=AT, source="SYNTHETIC", source_digest="x")
    assert row.accepted is None and row.reported_model is None
    value["acceptance_domain"] = "synthetic"
    assert (
        from_capture(
            value,
            timestamp=None,
            source="SYNTHETIC",
            source_digest="y",
        ).accepted
        is False
    )
    value["measurement"]["failure_class"] = "private error text"
    assert (
        from_capture(
            value,
            timestamp=AT,
            source="SYNTHETIC",
            source_digest="z",
        ).failure_class
        == "RECORDED_INVOCATION_FAILURE"
    )


def test_budget_unset_unknown_and_limits() -> None:
    """Optional constraints are explicit; passing never grants science authority."""
    absent = UsageAmount(None, None, None)
    assert (
        UsageBudget(BudgetScope.OBSERVED_WINDOW, "local", absent)
        .check(absent, absent, absent)
        .allowed
    )
    limit = UsageBudget(BudgetScope.EXPERIMENT, "synthetic", UsageAmount(4, 100, 100))
    passed = limit.check(
        UsageAmount(1, 20, 20),
        UsageAmount(1, 30, 30),
        UsageAmount(1, 40, 40),
    )
    assert passed.status == "BUDGET_CHECK_PASS"
    blocked = limit.check(
        UsageAmount(4, 20, None),
        UsageAmount(1, 30, 30),
        UsageAmount(1, 60, 40),
    )
    assert blocked.status == "BUDGET_BLOCKED" and set(blocked.reasons) == {
        "fresh_calls:EXCEEDED",
        "input_tokens:EXCEEDED",
        "output_tokens:UNKNOWN",
    }
    with pytest.raises(ValueError):
        UsageAmount(-1, 0, 0)


def test_transparent_forecasts() -> None:
    """Small empirical brackets never become tokenizer, billing or capacity claims."""
    args: dict[str, Any] = {
        "invocation": "synthetic",
        "model": "fake",
        "reasoning_effort": "High",
        "execution_profile": "SEMANTIC_WORKER",
        "disclosed_characters": 200,
        "disclosed_bytes": 200,
        "disclosure_digest": "digest",
        "response_maximum_bytes": 50,
    }
    value = forecast(**args, calibrations=(measured(),))
    assert (
        value.input_tokens.upper == 2000
        and value.observed_small_input_floor.lower == 1000
    )
    assert (
        value.output_tokens.upper == 50
        and "EXTRAPOLATED" in value.input_tokens.provenance
    )
    unknown = forecast(**args, calibrations=(measured(requested_model="other"),))
    assert unknown.input_tokens.upper is None and unknown.output_tokens.upper is None
    large = measured(disclosed_bytes=Measured(5000, Availability.REPORTED, "synthetic"))
    assert forecast(**args, calibrations=(large,)).input_tokens.lower == 0
    missing = measured(
        usage=ModelUsage(),
        disclosed_bytes=Measured(None, Availability.UNKNOWN, "unknown"),
    )
    assert (
        forecast(**args, calibrations=(missing,)).input_tokens.availability
        == Availability.UNKNOWN
    )


def _metadata_session(tmp_path: Path, extra: str = "") -> Path:
    """Literal authored metadata, not an encoder/decoder round-trip oracle."""
    path = tmp_path / "authored.jsonl"
    path.write_text(
        '{"type":"session_meta","payload":{"model_provider":"openai","cwd":"C:/work/project"}}\n'
        '{"timestamp":"2026-10-15T12:00:00Z","type":"token_usage_record","payload":'
        '{"thread_id":"thread","turn_id":"turn","response_id":"response",'
        '"usage":{"input_tokens":7},"turn_token_usage":{"input_tokens":7}'
        + extra
        + "}}\n",
        encoding="utf-8",
    )
    return path


@pytest.mark.parametrize(
    "extra",
    [
        ',"priv\\u0061te":"PRIVATE_SENTINEL"',
        ',"Private":"PRIVATE_SENTINEL"',
        ',"usage":{"input_tokens":8}',
        ',"us\\u0061ge":{}',
        ',"thread_id":"foreign"',
        ',"thread_token_usage":{"priv\\u0061te":"PRIVATE_SENTINEL"}',
        ',"thread_token_usage":[{"private":"PRIVATE_SENTINEL"}]',
    ],
)
def test_session_decoded_metadata_keys_refuse_unknown_and_duplicates(
    tmp_path: Path,
    extra: str,
) -> None:
    """Neither escaped keys nor last-key-wins ambiguity reaches ingestion."""
    path = _metadata_session(tmp_path, extra)
    assert read_session_usage(path) == ()
    assert from_session(path) == ()


@pytest.mark.parametrize(
    "usage",
    [
        '{"input_tokens":7,"priv\\u0061te":"PRIVATE_SENTINEL"}',
        '{"input_tokens":7,"Private":"PRIVATE_SENTINEL"}',
        '{"input_tokens":7,"input_tokens":8}',
        '{"input_tokens":7,"input_\\u0074okens":8}',
        '{"input_tokens":{"priv\\u0061te":"PRIVATE_SENTINEL"}}',
        '{"input_tokens":[7]}',
        '{"input_tokens":NaN}',
    ],
)
def test_exec_decoded_metadata_never_retains_disallowed_values(
    tmp_path: Path,
    usage: str,
) -> None:
    """Public raw_json output cannot retain a rejected private measurement."""
    path = tmp_path / "stdout.log"
    path.write_text(
        '{"type":"turn.completed","usage":' + usage + "}\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError) as caught:
        read_exec_usage(path)
    assert "PRIVATE_SENTINEL" not in str(caught.value)
    assert caught.value.__cause__ is None
    assert caught.value.__context__ is None


def test_allowed_escaped_metadata_keys_and_values(tmp_path: Path) -> None:
    """JSON member equivalence is exact and case-sensitive, including escapes."""
    path = _metadata_session(tmp_path)
    path.write_bytes(
        path.read_bytes()
        .replace(b'"usage"', b'"us\\u0061ge"')
        .replace(b'"thread"', b'"thr\\u0065ad"'),
    )
    (row,) = read_session_usage(path)
    assert row.thread_id == "thread" and row.usage.input_tokens == 7
    assert len(from_session(path)) == 2
    path.write_bytes(
        b'{"type":"thread.started","thread_id":"thr\\u0065ad"}\n{"type":"turn.completed","us\\u0061ge":{"input_\\u0074okens":7}}\n',
    )
    (exec_row,) = read_exec_usage(path)
    assert exec_row.thread_id == "thread" and exec_row.counts.input_tokens == 7
    assert exec_row.raw_json == '{"input_tokens":7}'


def test_private_context_cannot_supply_nested_attribution(tmp_path: Path) -> None:
    """Escaped private context stops projection before its value is inspected."""
    path = _metadata_session(tmp_path)
    data = path.read_bytes().splitlines()
    data.insert(
        1,
        b'{"type":"turn_context","payload":{"in\\u0070ut":{"model":"PRIVATE_SENTINEL"}}}',
    )
    path.write_bytes(b"\n".join(data))
    (row,) = read_session_usage(path)
    assert row.requested_model == "UNKNOWN"
    assert "PRIVATE_SENTINEL" not in str(from_session(path))


@pytest.mark.parametrize(
    "raw",
    [
        b'{"type":"turn.completed","usage":',
        b'{"type":"turn.completed","usage":{"input_tokens":"\xff"}}',
        b'{"type":"turn.completed","usage":[]}',
        b'{"type":"turn.completed","usage":null}',
        b'{"type":"turn.completed","usage":{"input_tokens":'
        + b"[" * 1100
        + b"0"
        + b"]" * 1100
        + b"}}",
        b'{"type":"turn.completed","model":"' + b"x" * 65536 + b'"}',
    ],
    ids=["truncated", "encoding", "array", "null", "depth", "size"],
)
def test_invalid_or_oversized_exec_metadata_is_controlled(
    tmp_path: Path,
    raw: bytes,
) -> None:
    """Early bounded admission and sanitized failures retain no raw document."""
    path = tmp_path / "bad.log"
    path.write_bytes(raw)
    with pytest.raises(ValueError) as caught:
        read_exec_usage(path)
    assert caught.value.__cause__ is None and caught.value.__context__ is None


def test_large_content_line_is_skipped_without_losing_following_metadata(
    tmp_path: Path,
) -> None:
    """Bounded streaming drains content; it is never parsed to locate usage."""
    path = tmp_path / "stdout.log"
    path.write_bytes(
        b'{"type":"item.completed","item":{"text":"'
        + b"x" * 70000
        + b'"}}\n{"type":"turn.completed","usage":{"input_tokens":7}}\n',
    )
    (row,) = read_exec_usage(path)
    assert row.counts.input_tokens == 7


@pytest.mark.parametrize(
    "payload",
    [
        '"model":"first","model":"second"',
        '"model" "missing-colon"',
        '"model":{}',
        '"model":"unterminated',
        "",
    ],
)
def test_context_projection_refuses_ambiguous_or_unsupported_prefix(
    tmp_path: Path,
    payload: str,
) -> None:
    """Only unambiguous direct string context can attribute a response."""
    path = _metadata_session(tmp_path)
    lines = path.read_bytes().splitlines()
    lines.insert(1, ('{"type":"turn_context","payload":{' + payload + "}}").encode())
    path.write_bytes(b"\n".join(lines))
    (row,) = read_session_usage(path)
    assert row.requested_model == "UNKNOWN"


@pytest.mark.parametrize("change", ["timestamp", "usage", "payload", "size"])
def test_session_unusable_metadata_does_not_create_an_observation(
    tmp_path: Path,
    change: str,
) -> None:
    """Invalid or oversized candidates cannot manufacture known usage."""
    path = _metadata_session(tmp_path)
    raw = path.read_bytes()
    if change == "timestamp":
        raw = raw.replace(b'"2026-10-15T12:00:00Z"', b'"invalid"')
    elif change == "usage":
        raw = raw.replace(b'"usage":{"input_tokens":7}', b'"usage":null')
    elif change == "payload":
        raw = b'{"type":"token_usage_record","payload":null}'
    else:
        raw = raw.replace(b'"response"', b'"' + b"x" * 65536 + b'"')
    path.write_bytes(raw)
    assert read_session_usage(path) == ()


@pytest.mark.parametrize(
    "raw",
    [
        b'[{"type":"turn.completed","usage":{}}]',
        b'{"type":"turn.completed","usage":{"input_tokens":true}}',
        b'{"type":"turn.completed","usage":{"input_tokens":-1}}',
    ],
)
def test_exec_unsupported_container_or_count_refuses(
    tmp_path: Path,
    raw: bytes,
) -> None:
    """Supported counts are nonnegative integers or unknown, not containers."""
    path = tmp_path / "unsupported.log"
    path.write_bytes(raw)
    with pytest.raises(ValueError, match="Unsupported"):
        read_exec_usage(path)


def test_content_prefix_errors_and_long_drain_do_not_leak_values(
    tmp_path: Path,
) -> None:
    """Malformed event identity remains unavailable; bounded drain reaches EOF."""
    path = _metadata_session(tmp_path)
    lines = path.read_bytes().splitlines()
    lines.insert(1, b'{"type":"turn_context","payload":{"model":"\xff"}}')
    lines.insert(2, b'{"type":"event_msg","payload":')
    path.write_bytes(b"\n".join(lines))
    (row,) = read_session_usage(path)
    assert row.requested_model == "UNKNOWN"
    path.write_bytes(
        b'{"type":"\xff","usage":{}}\n'
        b'{"type":"item.completed","item":"' + b"x" * 150000,
    )
    assert read_exec_usage(path) == ()


def test_compatible_partial_and_escaped_context_is_available(tmp_path: Path) -> None:
    """Escaped allowed keys are compatible; an incomplete suffix adds no data."""
    path = _metadata_session(tmp_path)
    lines = path.read_bytes().splitlines()
    lines.insert(1, b'{"type":"turn_context","payload":{"mod\\u0065l":"fake",')
    path.write_bytes(b"\n".join(lines))
    (row,) = read_session_usage(path)
    assert row.requested_model == "fake"
