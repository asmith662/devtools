# Copyright (c) 2026
# ruff: noqa: INP001, PLR2004 -- operational CLI test conventions

"""Resolve and validate output locations before asking for any authorization."""

from __future__ import annotations

import asyncio
import importlib.util
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

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
def test_report_directory_resolves_against_cwd_before_confirmation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    cli: ModuleType,
    *,
    absolute: bool,
) -> None:
    """A relative report is based on the caller's cwd, never the script root."""
    monkeypatch.chdir(tmp_path)
    expected = tmp_path / "new" / "run"
    value = str(expected) if absolute else "new/run"
    monkeypatch.setattr("sys.argv", ["worker", "--report-directory", value])

    def boundary(arguments: argparse.Namespace) -> None:
        assert arguments.report_directory == expected
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
