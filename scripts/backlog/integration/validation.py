# Copyright (c) 2026
# ruff: noqa: COM812 -- concrete host-owned validation
"""The fixed integration gates, never commands supplied by a model or plan."""

from __future__ import annotations

import asyncio
import hashlib
import json
import sys
from typing import TYPE_CHECKING, Any

from devtools.core.paths import resolve_path
from devtools.core.time import Duration, Stopwatch, Timestamp
from devtools.resources.commands import Command, CommandError, CommandExecutor
from devtools.resources.filesystem import TextFile, write

if TYPE_CHECKING:
    from pathlib import Path

EXCERPT_BYTES = 16384


async def validate_tree(
    checkout: Path, evidence: Path, plan: dict[str, Any], oracle: str, *, post: bool
) -> dict[str, Any]:
    """Run actual acceptance; pre-publication additionally requires protected gate."""
    evidence.mkdir()  # noqa: ASYNC240 -- bounded local administrative boundary
    module = plan["source"].removeprefix("src/").removesuffix(".py").replace("/", ".")
    prelude = (
        "import sys\nfrom pathlib import Path\n"
        f"sys.path.insert(0, {str(checkout / 'src')!r})\n"
        f"import {module} as module\n"
        "assert Path(module.__file__).resolve() == "
        f"Path({str(checkout / plan['source'])!r})\n"
    )
    oracle_path = evidence / "oracle.py"
    write(TextFile(resolve_path(oracle_path), prelude + oracle))
    tests = tuple(
        dict.fromkeys(
            [
                *plan["tests"],
                *(f["path"] for f in plan["files"] if f["path"].startswith("tests/")),
            ]
        )
    )
    tests_path = evidence / "tests.py"
    write(
        TextFile(
            resolve_path(tests_path),
            prelude
            + "import pytest\nraise SystemExit(pytest.main("
            + repr([*tests, "--no-cov", "-q"])
            + "))\n",
        )
    )
    paths = tuple(f["path"] for f in plan["files"])
    protected_path = evidence / "protected.py"
    protected_script = checkout / "scripts/validate_development.py"
    if not post:
        write(
            TextFile(
                resolve_path(protected_path),
                prelude
                + "import runpy\n"
                + f"sys.path.insert(0, {str(checkout)!r})\n"
                + f"runpy.run_path({str(protected_script)!r},"
                + " run_name='__main__')\n",
            )
        )
    commands: list[tuple[str, tuple[str, ...]]] = [
        ("oracle", ("-I", "-B", str(oracle_path))),
        ("tests", ("-I", "-B", str(tests_path))),
    ]
    if not post:
        commands.extend(
            [
                ("ruff", ("-m", "ruff", "check", *paths)),
                ("format", ("-m", "ruff", "format", "--check", *paths)),
                ("mypy", ("-m", "mypy", "--strict", *paths)),
                ("protected", ("-I", "-B", str(protected_path))),
            ]
        )
    report: dict[str, Any] = {
        "started_at": str(Timestamp.now()),
        "profile": "post-promotion-focused" if post else "pre-publication-protected",
        "checks": [],
        "passed": False,
    }
    elapsed = Stopwatch()

    def progress() -> None:
        write(TextFile(resolve_path(evidence / "progress.json"), json.dumps(report)))

    progress()
    try:
        async with asyncio.timeout(plan["validation_seconds"]):
            for name, args in commands:
                started = Stopwatch()
                report["active_check"] = name
                progress()
                print(f"{Timestamp.now()} integration validation: {name}", flush=True)  # noqa: T201 -- operator progress
                result = await CommandExecutor().execute(
                    Command(sys.executable)
                    .args(*args)
                    .cwd(resolve_path(checkout))
                    .with_timeout(Duration.seconds(plan["validation_seconds"]))
                )
                for channel in ("stdout", "stderr"):
                    payload = getattr(result, channel)
                    write(
                        TextFile(
                            resolve_path(evidence / (name + "-" + channel + ".txt")),
                            payload.decode("latin-1"),
                            encoding="latin-1",
                        )
                    )
                check = {
                    "name": name,
                    "argv": [sys.executable, *args],
                    "exit_code": result.exit_code,
                    "elapsed_seconds": started.stop().total_seconds,
                    "stdout": result.stdout[:EXCERPT_BYTES].decode(errors="replace"),
                    "stderr": result.stderr[:EXCERPT_BYTES].decode(errors="replace"),
                    "stdout_sha256": hashlib.sha256(result.stdout).hexdigest(),
                    "stderr_sha256": hashlib.sha256(result.stderr).hexdigest(),
                    "log_directory": str(evidence),
                    "log_bytes": "exact; excerpts decoded utf-8 with replacement",
                    "excerpt_truncated": len(result.stdout) > EXCERPT_BYTES
                    or len(result.stderr) > EXCERPT_BYTES,
                    "truncated": result.stdout_truncated or result.stderr_truncated,
                }
                report["checks"].append(check)
                progress()
                if result.failed or check["truncated"]:
                    break
            else:
                report["passed"] = True
    except (TimeoutError, OSError, ValueError, CommandError) as error:
        report["error"] = str(error)
    finally:
        report.update(
            active_check=None,
            finished_at=str(Timestamp.now()),
            elapsed_seconds=elapsed.stop().total_seconds,
        )
        progress()
    return report
