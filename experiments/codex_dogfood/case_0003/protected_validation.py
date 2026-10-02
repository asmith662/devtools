# Copyright (c) 2026
"""Protected development validation plugin; never loads retained outcomes."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pytest

BOUNDARY = Path(__file__).with_name("validation_boundary.json")


def pytest_collection_modifyitems(config: Any, items: list[Any]) -> None:  # noqa: ANN401
    """Exclude exact retained confirmation/audit tests before execution."""
    excluded = set(json.loads(BOUNDARY.read_text(encoding="utf-8"))["excluded_tests"])
    removed = [item for item in items if item.nodeid in excluded]
    items[:] = [item for item in items if item.nodeid not in excluded]
    config.hook.pytest_deselected(items=removed)


@pytest.fixture(autouse=True)
def bounded_benchmark_cwd(request: Any, monkeypatch: pytest.MonkeyPatch) -> None:  # noqa: ANN401
    """Run only seven real-corpus benchmarks from an explicit bounded copy."""
    bounded = set(json.loads(BOUNDARY.read_text(encoding="utf-8"))["bounded_cwd_tests"])
    if request.node.nodeid in bounded:
        monkeypatch.chdir(os.environ["DEVTOOLS_CASE3_BOUNDED_ROOT"])
