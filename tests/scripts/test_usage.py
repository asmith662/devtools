# Copyright (c) 2026
# ruff: noqa: ANN401, PT018 -- synthetic importer provenance fixtures
"""Native-looking deterministic fixtures must never count as consumed usage."""

import importlib.util
import json
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

from devtools.core.time import Timestamp
from devtools.models.interaction.usage import ModelUsage
from devtools.observability.usage import UsageObservation
from devtools.observability.usage.storage import load, save


def test_unverified_stdout_excluded_and_provisional_snapshot_preserved(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trusted receipt/session identity is required in addition to JSON shape."""
    spec = importlib.util.spec_from_file_location(
        "usage_cli_test",
        Path("scripts/usage.py"),
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "LEDGER", tmp_path / ".local/usage/ledger.json")
    monkeypatch.setattr(module, "WORKERS", tmp_path / "workers")
    at = Timestamp.from_isoformat("2026-10-15T12:00:00Z")

    def row(thread: str, **changes: Any) -> UsageObservation:
        return UsageObservation(
            timestamp=at,
            backend="Codex",
            provider="OpenAI",
            model="fake",
            reasoning_effort="High",
            execution_profile="SEMANTIC_WORKER",
            invocation_id=None,
            thread_id=thread,
            turn_id=None,
            response_id=None,
            usage=ModelUsage(input_tokens=10),
            source="LOCAL_CODEX_EXEC_METADATA",
            source_digest=thread,
            **changes,
        )

    save(module.LEDGER, (row("unverified"),))
    capture = {
        "measurement": {"backend_thread_id": {"value": "known"}},
        "original_capture_sha256": "capture-digest",
    }

    def metadata(path: Path) -> Any:
        if path.name == "smoke-receipt.json":
            return {
                "reasoning": "Medium",
                "paths": {
                    "direct": {
                        "logs": str(tmp_path / "absent"),
                        "semantic_receipt": {
                            "thread_id": "known",
                            "invocation": "known",
                            "usage": {
                                "input_tokens": 10,
                                "cached_input_tokens": 0,
                                "cache_write_input_tokens": 0,
                                "output_tokens": 2,
                                "reasoning_output_tokens": 0,
                            },
                        },
                    },
                },
            }
        if path.name == "seal.json":
            return {"original_usage": capture}
        return {"measurement": capture, "timestamp": str(at)}

    monkeypatch.setattr(module, "read_json", metadata)

    def projected(_value: Any, **kwargs: Any) -> UsageObservation:
        return replace(
            row("known"),
            source=kwargs["source"],
            attribution=kwargs["attribution"],
            timestamp=kwargs["timestamp"],
        )

    monkeypatch.setattr(module, "from_capture", projected)
    for thread in ("known", "unverified"):
        folder = tmp_path / ".local" / thread
        folder.mkdir(parents=True)
        (folder / "stdout.log").write_text(
            "\n".join(
                json.dumps(v)
                for v in [
                    {"type": "thread.started", "thread_id": thread},
                    {
                        "type": "turn.completed",
                        "usage": {"input_tokens": 10, "output_tokens": 2},
                    },
                ]
            ),
            encoding="utf-8",
        )
    result = module.backfill(at, codex_home=tmp_path / "no-user-sessions")
    assert result["unverified_native_records_not_counted"] == 1
    assert result["prior_provisional_rows_archived_and_excluded"] == 1
    assert not any(r.thread_id == "unverified" for r in load(module.LEDGER))
    archive = module.LEDGER.parent / "ledger-before-authenticated-import-01.json"
    assert load(archive)[0].thread_id == "unverified"
