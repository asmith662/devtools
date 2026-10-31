# Copyright (c) 2026
# ruff: noqa: COM812 -- receipt fields
"""Pytest hooks with no eager framework imports before coverage starts."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pytest


class Observations:
    """Record actual pytest phases, including setup/teardown and collection errors."""

    def __init__(self) -> None:
        """Start with no observed tests."""
        self.phases: list[dict[str, Any]] = []
        self.collection_errors: list[str] = []

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        """Preserve failures and elapsed phase durations without inference."""
        self.phases.append(
            {
                "nodeid": report.nodeid,
                "phase": report.when,
                "outcome": report.outcome,
                "seconds": report.duration,
                "failure": str(report.longrepr) if report.failed else None,
            }
        )

    def pytest_collectreport(self, report: pytest.CollectReport) -> None:
        """Retain collection failures separately from test assertions."""
        if report.failed:
            self.collection_errors.append(str(report.longrepr))


def failure_kind(code: int, observations: Observations) -> str:
    """Classify native pytest exits without calling every failure an assertion."""
    if observations.collection_errors:
        return "collection"
    return {
        0: "passed",
        1: "test-or-coverage-failure",
        2: "interrupted",
        3: "internal-error",
        4: "configuration",
        5: "no-tests",
    }.get(code, "unknown")
