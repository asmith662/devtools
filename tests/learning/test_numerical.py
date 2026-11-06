# Copyright (c) 2026
"""Qualify genuine native fits through suspended-start one-process custody."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor

_CONTROL_REGRESSION_METHODS = 3

if TYPE_CHECKING:
    from collections.abc import Callable


def test_native_states_and_scientific_publication(
    tmp_path: Path,
    control_coverage: Callable[[Path, Path], tuple[str, Callable[[], None]]],
) -> None:
    """The OS worker executes real fits; the host consumes inspected results."""
    site = Path(sys.prefix) / "Lib/site-packages"
    worker = Path(__file__).with_name("numerical_worker.py").resolve()
    executable = Path(getattr(sys, "_base_executable", sys.executable)).resolve()
    measurement, finish = control_coverage(worker, executable)
    code = (
        "import site,sys,runpy,pathlib,json;site.addsitedir(sys.argv[1]);"
        "sys.argv=sys.argv[2:];\n"
        + measurement
        + "\nrunpy.run_path(sys.argv[0],run_name='__main__')"
    )
    result = asyncio.run(
        CommandExecutor(contained=True).execute(
            Command(str(executable))
            .args("-S", "-c", code, str(site), str(worker), str(tmp_path / "science"))
            .cwd(resolve_path(tmp_path))
            .with_environment(
                {
                    "PYTHONPATH": "",
                    "PYTHONDONTWRITEBYTECODE": "1",
                    "OMP_NUM_THREADS": "1",
                    "OPENBLAS_NUM_THREADS": "1",
                    "MKL_NUM_THREADS": "1",
                    "BLIS_NUM_THREADS": "1",
                },
            )
            .with_timeout(Duration.seconds(60)),
        ),
    )
    assert result.succeeded, result.stderr.decode()
    finish()
    report = json.loads(result.stdout)
    assert report["regression_methods"] == _CONTROL_REGRESSION_METHODS
    assert report["binary_f1"]["f1"] == 1.0
    assert report["publication_status"] == "current"
    assert report["recording_status"] == "acknowledged"
