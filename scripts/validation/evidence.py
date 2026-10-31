# Copyright (c) 2026
# ruff: noqa: COM812, E501 -- operator messages and structured receipts
"""Invocation-local pytest observations and qualified repository inputs."""

from __future__ import annotations

import asyncio
import hashlib
import importlib.metadata
import os
import platform
import sys
from typing import TYPE_CHECKING, Any

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy
from devtools.resources.filesystem import TextFile, write

if TYPE_CHECKING:
    from pathlib import Path

    import pytest


def save(path: Path, payload: str) -> None:
    """Atomically retain a local receipt without replacing existing evidence."""
    path.parent.mkdir(parents=True, exist_ok=True)
    write(TextFile(resolve_path(path.absolute()), payload), overwrite=False)


def git(root: Path, *args: str) -> str:
    """Use managed Commands for bounded read-only Git queries."""
    result = asyncio.run(
        CommandExecutor(
            output_policy=CommandOutputPolicy(max_stdout_bytes=16 << 20)
        ).execute(
            Command("git")
            .args(*args)
            .cwd(resolve_path(root))
            .with_timeout(Duration.seconds(60))
        )
    )
    if not result.succeeded or result.stdout_truncated or result.stderr_truncated:
        message = f"Git input authentication failed: {args!r}"
        raise ValueError(message)
    return result.stdout.decode("utf-8").strip()


def inputs(root: Path) -> dict[str, Any]:
    """Qualify declared inputs; never claim ignored/external environment closure."""
    paths = set(git(root, "ls-files", "-z").split("\0"))
    paths.update(
        git(
            root,
            "ls-files",
            "--others",
            "--exclude-standard",
            "-z",
            "src",
            "tests",
            "scripts",
            "apps",
        ).split("\0")
    )
    hashes = {
        p: hashlib.sha256((root / p).read_bytes()).hexdigest()
        for p in sorted(paths)
        if p
        and (
            p.startswith(("src/", "tests/", "scripts/", "apps/"))
            or p
            in {
                "pyproject.toml",
                "uv.lock",
                ".python-version",
                ".gitattributes",
                ".gitignore",
                "AGENTS.md",
            }
        )
        and (root / p).is_file()
    }
    return {
        "head": git(root, "rev-parse", "HEAD"),
        "git_blobs": git(root, "ls-files", "-s"),
        "sha256": hashes,
        "python": sys.version,
        "executable": sys.executable,
        "platform": platform.platform(),
        "packages": sorted(
            f"{d.metadata['Name']}=={d.version}"
            for d in importlib.metadata.distributions()
        ),
        "environment_sha256": hashlib.sha256(
            repr(sorted(os.environ.items())).encode()
        ).hexdigest(),
        "qualification": "Declared tracked and executable untracked files; inherited environment fingerprint only. Ignored files, services and transitive external inputs are not attested. Fresh-only acceptance.",
    }


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
