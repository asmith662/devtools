# Copyright (c) 2026
"""Observed native identity and explicitly simulated environment refusals; no fits."""

from __future__ import annotations

import importlib.metadata
import platform
import sys
from typing import TYPE_CHECKING

import pytest
from threadpoolctl import (  # type: ignore[import-untyped]
    threadpool_info,
    threadpool_limits,
)

from devtools.learning.integrations.sklearn import runtime
from devtools.resources.filesystem import TextFile
from devtools.resources.filesystem import read as read_file

if TYPE_CHECKING:
    from devtools.core.paths import ResolvedPath
    from devtools.resources.filesystem import File, FileFormat


@pytest.mark.parametrize("profile", ["python-314", "dependency-version"])
def test_unqualified_runtime_refuses_before_numerical_execution(
    monkeypatch: pytest.MonkeyPatch, profile: str,
) -> None:
    """Refuse untested Python or package portability before fitting."""
    if profile == "python-314":
        monkeypatch.setattr(platform, "python_version", lambda: "3.14.3")
    else:
        original = importlib.metadata.version

        def different(name: str) -> str:
            return "unqualified" if name == "numpy" else original(name)

        monkeypatch.setattr(importlib.metadata, "version", different)
    with pytest.raises(ValueError, match="qualified Windows CPython"):
        runtime.observe_runtime()


@pytest.mark.parametrize("pools", [[], [{"num_threads": 2}]])
def test_reported_native_thread_violation_refuses(
    monkeypatch: pytest.MonkeyPatch, pools: list[dict[str, int]],
) -> None:
    """Inject invalid thread metadata without creating another native worker."""
    control = importlib.import_module("threadpoolctl")
    monkeypatch.setattr(control, "threadpool_info", lambda: pools)
    with pytest.raises(ValueError, match="one native thread"):
        runtime.observe_runtime()


@pytest.mark.parametrize("boundary", ["library", "interpreter"])
def test_nonbinary_identity_read_cannot_qualify_native_bytes(
    monkeypatch: pytest.MonkeyPatch, boundary: str,
) -> None:
    """Require actual binary bytes at each native identity boundary."""
    original = read_file

    def wrong_kind(
        path: ResolvedPath, *, file_format: FileFormat, max_bytes: int,
    ) -> File:
        is_interpreter = str(path.value) == sys.executable
        if is_interpreter == (boundary == "interpreter"):
            return TextFile(path, "simulated wrong file kind")
        return original(path, file_format=file_format, max_bytes=max_bytes)

    monkeypatch.setattr(runtime, "read", wrong_kind)
    with (
        threadpool_limits(limits=1),
        pytest.raises(TypeError, match="binary bytes required"),
    ):
        runtime.observe_runtime()


def test_actual_loaded_runtime_records_coherent_binary_identities() -> None:
    """Observe actual installed native libraries with one thread, without fitting."""
    with threadpool_limits(limits=1):
        observed = runtime.observe_runtime()
        pools = threadpool_info()
    assert observed["python"] == "3.12.13"
    assert observed["versions"] == runtime.VERSIONS
    assert observed["executable"] == sys.executable
    assert pools
    assert all(p["num_threads"] == 1 for p in pools)
    assert isinstance(observed["executable_sha256"], str)
