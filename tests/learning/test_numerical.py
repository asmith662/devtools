# Copyright (c) 2026
"""Qualify genuine native fits through suspended-start one-process custody."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor


def test_native_states_and_scientific_publication(tmp_path: Path) -> None:
    """The OS worker executes real fits; the host consumes inspected results."""
    site = Path(sys.prefix) / "Lib/site-packages"
    worker = Path(__file__).with_name("numerical_worker.py").resolve()
    code = "import site,sys,runpy;site.addsitedir(sys.argv[1]);sys.argv=sys.argv[2:];runpy.run_path(sys.argv[0],run_name='__main__')"
    result = asyncio.run(
        CommandExecutor(contained=True).execute(
            Command(str(sys._base_executable))  # type: ignore[attr-defined]
            .args("-c", code, str(site), str(worker), str(tmp_path / "science"))
            .with_environment(
                {
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
    report = json.loads(result.stdout)
    assert report["regression_methods"] == 3
    assert report["binary_f1"]["f1"] == 1.0
    assert report["publication_status"] == "current"
    assert report["recording_status"] == "acknowledged"
