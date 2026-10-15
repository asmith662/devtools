# Copyright (c) 2026
# ruff: noqa: S101, ANN401, ASYNC240, FBT001, PLR2004, COM812 -- fake external processes only
"""Exercise the actual capacity driver without a model, credentials or host writes."""

import asyncio
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from devtools.core.time import Duration
from experiments.codex_dogfood.case_0009.artifacts import json_bytes
from experiments.orchestration.engineering.host_disclosure import (
    capacity_probe as probe,
)
from experiments.orchestration.workers import capacity, schema, semantic


@pytest.mark.parametrize("valid", [True, False])
@pytest.mark.parametrize("mode", ["minimal", "capacity"])
def test_probe_is_single_attempt_and_retains_usage(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    valid: bool,
    mode: str,
) -> None:
    """A fake PASS remains in a temporary repository; failure is never retried."""
    monkeypatch.setattr(probe, "ROOT", tmp_path)
    monkeypatch.setattr(probe, "WORK_ROOT", tmp_path / "outside-model-root")
    auth = tmp_path / "synthetic-auth.json"
    auth.write_text("NOT-A-CREDENTIAL", encoding="utf-8")
    monkeypatch.setattr(probe, "AUTH_FILE", auth)
    catalog = tmp_path / "synthetic-catalog.json"
    catalog.write_bytes(json_bytes({"models": []}))
    monkeypatch.setattr(probe, "CATALOG", catalog)
    calls = []

    async def version(*_args: Any, **_kwargs: Any) -> Any:
        return SimpleNamespace(failed=False, stdout=b"codex-cli 0.162.1\n")

    async def model(
        argv: Any,
        cwd: Path,
        _environment: Any,
        _timeout: Any,
        _grace: Any,
        logs: Path,
        **kwargs: Any,
    ) -> Any:
        calls.append(argv)
        assert not any(cwd.iterdir())
        assert argv[argv.index("--model") + 1] == "gpt-6-astra"
        payload = (
            {"blocks": ["A" * 512] * 116 if valid else []}
            if mode == "capacity"
            else {"answer": "SYNTHETIC_OK" if valid else "INVALID"}
        )
        final = schema.canonical(payload)
        Path(argv[argv.index("--output-last-message") + 1]).write_bytes(final)
        events = [
            {"type": "thread.started", "thread_id": "SYNTHETIC-FAKE"},
            {"type": "turn.started"},
            {
                "type": "item.completed",
                "item": {"type": "agent_message", "text": final.decode()},
            },
            {
                "type": "turn.completed",
                "usage": {
                    "input_tokens": 123,
                    "cached_input_tokens": 0,
                    "cache_write_input_tokens": 0,
                    "output_tokens": 456,
                    "reasoning_output_tokens": 12,
                },
            },
        ]
        stdout = b"\n".join(json.dumps(event).encode() for event in events)
        logs.mkdir()
        (logs / "stdout.log").write_bytes(stdout)
        (logs / "stdin.bin").write_bytes(kwargs["stdin_bytes"])
        (logs / "exit.json").write_bytes(
            json_bytes(
                {
                    "exit_code": 0,
                    "stdout_truncated": False,
                    "stderr_truncated": False,
                }
            )
        )
        return SimpleNamespace(
            failed=False,
            exit_code=0,
            stdout=stdout,
            stderr=b"",
            stdout_truncated=False,
            stderr_truncated=False,
            duration=Duration.seconds(2),
        )

    monkeypatch.setattr(probe, "invoke", version)
    monkeypatch.setattr(semantic, "invoke", model)
    root = tmp_path / ".local/probe"
    prepared = probe.prepare(root, mode)
    assert prepared["bounds"]["probe"]["utf8_bytes"] <= 65536
    if valid:
        receipt = asyncio.run(probe.execute(root))
        if mode == "capacity":
            capacity.authenticate(receipt, probe.configuration())
        folder = "capacity-evidence" if mode == "capacity" else "minimal-evidence"
        capacity.authenticate_files(tmp_path, receipt, folder=folder)
        assert receipt["measurement"]["measurement"]["accepted"] is True
        artifact = (
            tmp_path
            / "experiments/orchestration/engineering/host_disclosure"
            / folder
            / "response.json"
        )
        artifact.write_bytes(b"tampered")
        with pytest.raises(ValueError, match="hash mismatch"):
            capacity.authenticate_files(tmp_path, receipt, folder=folder)
    else:
        with pytest.raises(ValueError, match=r"cardinality|enum"):
            asyncio.run(probe.execute(root))
        assert not (tmp_path / capacity.RECEIPT_ADDRESS).exists()
        measurement = json.loads(
            (root / "invocation/invocation-measurement.json").read_bytes()
        )
        assert measurement["measurement"]["usage"]["input_tokens"] == 123
        assert measurement["measurement"]["validated"] is False
    with pytest.raises(ValueError, match="terminal"):
        asyncio.run(probe.execute(root))
    assert len(calls) == 1
