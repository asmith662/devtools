# Copyright (c) 2026
# ruff: noqa: S101, D103, ANN401, ASYNC240, PT011 -- bounded invalid-JSON external-Agent fixtures
"""Strict host-disclosure transport without any live semantic model."""

from __future__ import annotations

import asyncio
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from experiments.codex_dogfood.case_0009.artifacts import json_bytes
from experiments.orchestration.workers import runtime, semantic
from experiments.source_grounding.response import object_schema


@pytest.mark.parametrize(
    "text",
    [
        "```json\n{}\n```",
        "before {}",
        "{} {}",
        '{"x":1,"x":2}',
        '{"x":{"y":1,"y":2}}',
        "[]",
        '{"x":NaN}',
    ],
)
def test_strict_payload_rejects_ambiguity(text: str) -> None:
    with pytest.raises(ValueError):
        semantic.strict_object(text)


@pytest.mark.parametrize(
    "fault",
    [
        "",
        "missing",
        "prose",
        "schema",
        "tool",
        "duplicate-turn",
        "chatter",
        "transport",
        "mutation",
    ],
)
def test_native_final_capture_is_separate_from_transport(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
) -> None:
    config = {
        "model": "synthetic-model",
        "model_id": "fake",
        "reasoning": "Medium",
        "runtime": runtime.configuration(),
    }
    packet = {
        "case": "SYNTHETIC-transport",
        "frame": {"identity": "fake"},
        "resources": [],
    }
    schema = object_schema({"answer": {"type": "string"}})

    async def fake(
        argv: Any,
        cwd: Path,
        _env: Any,
        _timeout: Any,
        _grace: Any,
        _logs: Any,
        **kwargs: Any,
    ) -> Any:
        assert not any(cwd.iterdir())
        assert argv[-1] == "-"
        assert b"do not inspect the filesystem" in kwargs["stdin_bytes"]
        assert b"SYNTHETIC-transport" in kwargs["stdin_bytes"]
        text = '{"answer":"yes"}' if fault != "schema" else '{"wrong":1}'
        if fault == "prose":
            text = "before " + text
        response = Path(argv[argv.index("--output-last-message") + 1])
        if fault != "missing":
            response.write_bytes((text + "\n").encode())
        events: list[dict[str, Any]] = [
            {"type": "thread.started", "thread_id": "fresh-synthetic"},
        ]
        if fault == "chatter":
            events.append(
                {
                    "type": "item.completed",
                    "item": {"type": "agent_message", "text": "chatter"},
                },
            )
        if fault == "tool":
            events.append(
                {"type": "item.completed", "item": {"type": "command_execution"}},
            )
        events.extend(
            [
                {
                    "type": "item.completed",
                    "item": {"type": "agent_message", "text": text},
                },
                {"type": "turn.completed", "usage": {}},
            ],
        )
        if fault == "duplicate-turn":
            events.append({"type": "turn.completed"})
        if fault == "mutation":
            (cwd / "unexpected").write_text("not science")
        return SimpleNamespace(
            failed=fault == "transport",
            exit_code=1 if fault == "transport" else 0,
            stdout_truncated=False,
            stderr_truncated=False,
            stdout=b"\n".join(
                json_bytes(event).replace(b"\n", b"") for event in events
            ),
            stderr=b"",
        )

    monkeypatch.setattr(semantic, "invoke", fake)

    async def run() -> None:
        call = semantic.primary(
            config,
            json_bytes(packet),
            b"frozen instructions",
            schema,
            "synthetic/primary",
            tmp_path / "invocation",
            {},
            10,
            0.2,
        )
        if fault:
            with pytest.raises(ValueError):
                await call
            assert not (tmp_path / "invocation/receipt.json").exists()
        else:
            result = await call
            assert result["payload"] == {"answer": "yes"}
            assert result["provenance"]["tool_calls"] == 0
            assert not result["provenance"]["scientific_filesystem_dependency"]

    asyncio.run(run())
