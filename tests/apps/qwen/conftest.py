# Copyright (c) 2026
# ruff: noqa: SLF001, COM812 -- bounded historical input fixtures
"""Only frozen task inputs, with dependencies read from maintained source.

No repository, Git checkout or source-tree copy is created. Namespace shims let
subprocesses import the two captured implementation files independently of the
already repaired maintained modules.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from apps.qwen import coding_loop as worker
from apps.qwen.tasks import MARKDOWN, SOURCE_SEGMENTS
from scripts.backlog.integration.git import blob

if TYPE_CHECKING:
    from collections.abc import Callable

    from apps.qwen.tasks import CodingTask

ROOT = Path(__file__).resolve().parents[3]


@pytest.fixture
def captured_inputs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> Callable[[CodingTask], Path]:
    """Materialize just the frozen source/test inputs, never a Devtools tree."""
    original = worker._authenticate_inputs

    async def authenticate(_root: Path, workspace: Path, task: CodingTask) -> None:
        await original(ROOT, workspace, task)

    monkeypatch.setattr(worker, "_authenticate_inputs", authenticate)
    folder = tmp_path / "captured-inputs"
    for task in (MARKDOWN, SOURCE_SEGMENTS):
        for relative, _digest in task.baseline_hashes:
            path = folder / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            text = asyncio.run(blob(ROOT, task.baseline_revision, relative))
            path.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode())
            if relative == task.source:
                for parent in path.parents:
                    if parent == folder / "src":
                        break
                    maintained = ROOT / parent.relative_to(folder)
                    (parent / "__init__.py").write_text(
                        f"__path__ = [{str(parent)!r}, {str(maintained)!r}]\n"
                        + (
                            f"exec(compile(open({str(maintained / '__init__.py')!r}, "
                            "encoding='utf-8').read(), "
                            f"{str(maintained / '__init__.py')!r}, 'exec'))\n"
                            if (maintained / "__init__.py").exists()
                            else ""
                        ),
                        encoding="utf-8",
                    )
    return lambda _task: folder
