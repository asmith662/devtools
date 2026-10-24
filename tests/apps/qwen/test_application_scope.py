# Copyright (c) 2026
"""Explicit application paths use the existing bounded task admission."""

from __future__ import annotations

import asyncio
import sys
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from apps.qwen.coding_loop import _prepare_workspace
from apps.qwen.development_task import _timed_command
from apps.qwen.tasks import MARKDOWN

if TYPE_CHECKING:
    from pathlib import Path


def test_maintained_application_python_uses_explicit_existing_scope() -> None:
    """An application target still requires matching paths, identities and Context."""
    path = "apps/qwen/commands.py"
    task = replace(
        MARKDOWN,
        source=path,
        baseline_hashes=tuple(
            (path if p == MARKDOWN.source else p, h)
            for p, h in MARKDOWN.baseline_hashes
        ),
        context=tuple(
            (path if p == MARKDOWN.source else p, q, m, e)
            for p, q, m, e in MARKDOWN.context
        ),
        new_paths=("apps/qwen/new.py",),
    )
    assert task.sources == (path, "apps/qwen/new.py")
    with pytest.raises(ValueError, match="must agree"):
        replace(task, source="apps/other.py")


@pytest.mark.parametrize(
    "path",
    [
        "scripts/unsafe.py",
        "experiments/unsafe.py",
        "apps/../escape.py",
        "apps/file.txt",
    ],
)
def test_application_admission_does_not_admit_unbounded_or_nonpython_slots(
    path: str,
) -> None:
    """Canonical addresses and supported implementation roots remain mandatory."""
    with pytest.raises(ValueError):  # noqa: PT011 -- several independent admission checks
        replace(MARKDOWN, new_paths=(path,))


def test_application_oracle_imports_exact_local_source_in_isolated_python(
    tmp_path: Path,
) -> None:
    """Application validation adds the canonical root, without another checkout."""
    app = tmp_path / "apps"
    app.mkdir()
    (app / "__init__.py").write_text("", encoding="utf-8")
    (app / "sample.py").write_text("VALUE = 7\n", encoding="utf-8")
    folder = tmp_path / "evidence"
    folder.mkdir()
    source = "apps/sample.py"
    task = replace(
        MARKDOWN,
        source=source,
        oracle="assert module.VALUE == 7\n",
        baseline_hashes=tuple(
            (source if p == MARKDOWN.source else p, h)
            for p, h in MARKDOWN.baseline_hashes
        ),
        context=tuple(
            (source if p == MARKDOWN.source else p, q, m, e)
            for p, q, m, e in MARKDOWN.context
        ),
    )
    _prepare_workspace(tmp_path, folder, task)
    result = asyncio.run(
        _timed_command(
            tmp_path,
            sys.executable,
            "-I",
            "-B",
            str(folder / "oracle-runner.py"),
        ),
    )
    assert not result["failed"], result
