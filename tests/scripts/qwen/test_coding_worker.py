# Copyright (c) 2026
# ruff: noqa: INP001, PLR2004, COM812 -- operational CLI test conventions

"""Resolve and validate output locations before asking for any authorization."""

from __future__ import annotations

import asyncio
import importlib.util
import json
from dataclasses import asdict, replace
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from apps.qwen.tasks import MARKDOWN

if TYPE_CHECKING:
    import argparse
    from types import ModuleType


@pytest.fixture
def cli() -> ModuleType:
    """Load the operational entrypoint without relying on collection order."""
    specification = importlib.util.spec_from_file_location(
        "coding_worker_cli_test",
        Path(__file__).resolve().parents[3] / "scripts/qwen/coding_worker.py",
    )
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


@pytest.mark.parametrize("absolute", [False, True])
@pytest.mark.parametrize("task", ["markdown-fences", "python-source-segments"])
def test_report_directory_resolves_against_cwd_before_confirmation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    cli: ModuleType,
    task: str,
    *,
    absolute: bool,
) -> None:
    """A relative report is based on the caller's cwd, never the script root."""
    monkeypatch.chdir(tmp_path)
    expected = tmp_path / "new" / "run"
    value = str(expected) if absolute else "new/run"
    monkeypatch.setattr(
        "sys.argv", ["worker", "--task", task, "--report-directory", value]
    )

    def boundary(arguments: argparse.Namespace) -> None:
        assert arguments.report_directory == expected
        assert arguments.task == task
        assert task in arguments.task_objective
        assert arguments.report_path == expected
        assert arguments.authorize_local_execution is False
        message = "confirmed path boundary; no execution"
        raise SystemExit(message)

    monkeypatch.setattr(cli, "_confirm_local_execution", boundary)
    with pytest.raises(SystemExit, match="confirmed path boundary"):
        asyncio.run(cli.main())
    assert not expected.exists()


@pytest.mark.parametrize("invalid", ["", "\x00", "existing", "file/child"])
def test_invalid_report_directory_fails_before_confirmation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    invalid: str,
    cli: ModuleType,
) -> None:
    """Empty, malformed, occupied and non-directory parent paths fail closed."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "existing").mkdir()
    (tmp_path / "file").write_text("occupied", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["worker", "--report-directory", invalid])

    def forbidden(_arguments: argparse.Namespace) -> None:
        pytest.fail("Invalid paths must be rejected before authorization")

    monkeypatch.setattr(cli, "_confirm_local_execution", forbidden)
    with pytest.raises(SystemExit) as result:
        asyncio.run(cli.main())
    assert result.value.code == 2


@pytest.mark.parametrize("ready", [False, True])
def test_shared_local_profile_factory_never_invokes_model(
    cli: ModuleType, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, *, ready: bool
) -> None:
    """Both entrypoints reuse existing readiness/profile and client construction."""

    async def status(_root: Path) -> dict[str, object]:
        return {
            "state": "READY" if ready else "STOPPED",
            "expected_fingerprint": "fixture",
            "observed_fingerprint": "fixture",
        }

    calls = []
    client = object()

    def construct(**arguments: object) -> object:
        calls.append(arguments)
        return client

    async def command(_root: Path, *_arguments: str) -> dict[str, str]:
        return {"stdout": "fixture-head"}

    monkeypatch.setattr(cli, "_qwen_status", status)
    monkeypatch.setattr(cli, "_command", command)
    monkeypatch.setattr(cli, "LlamaCppInteraction", construct)
    if not ready:
        with pytest.raises(RuntimeError, match="MODEL_SERVICE_NOT_READY"):
            asyncio.run(cli.local_interaction(tmp_path))
        assert calls == []
    else:
        interaction, provenance = asyncio.run(cli.local_interaction(tmp_path))
        assert interaction is client
        assert calls[0]["model"] == "qwen38-local"
        assert provenance["model"] == "qwen38-local"
        assert provenance["profile"]


def test_host_definition_selects_native_worker_before_real_confirmation(
    cli: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The existing task contract selects read scope and truthful invocation bounds."""
    monkeypatch.chdir(tmp_path)
    task = replace(MARKDOWN, context_mode="on-demand", maximum_calls=6)
    (tmp_path / "task.json").write_text(json.dumps(asdict(task)), encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv",
        ["worker", "--task-definition", "task.json", "--report-directory", "run"],
    )

    def confirm(arguments: argparse.Namespace) -> None:
        assert arguments.task == task.name
        assert "6 model invocations" in arguments.coding_limits
        assert "8 read-only Context actions" in arguments.coding_limits
        assert arguments.report_directory == tmp_path / "run"
        message = "real confirmation boundary reached; no call"
        raise SystemExit(message)

    monkeypatch.setattr(cli, "_confirm_local_execution", confirm)
    with pytest.raises(SystemExit, match="boundary"):
        asyncio.run(cli.main())
    (tmp_path / "task.json").write_text("{}", encoding="utf-8")
    with pytest.raises(SystemExit) as error:
        asyncio.run(cli.main())
    assert error.value.code == 2
