# Copyright (c) 2026
# ruff: noqa: COM812, E501, PLC0415 -- fresh coverage bootstrap requires deferred imports

"""Fresh-interpreter coverage boundary; framework imports occur after pytest."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.resources.commands import CommandResult
    from scripts.validation.observation import Observations


def run_protected(
    root: Path, output: Path, arguments: list[str], observations: Observations
) -> int:
    """Start coverage before any framework imports in an independent process."""
    import asyncio

    from devtools.core.paths import resolve_path
    from devtools.core.time import Duration
    from devtools.resources.commands import (
        Command,
        CommandExecutor,
        CommandOutputPolicy,
        CommandStderr,
        CommandStdout,
    )
    from scripts.validation.evidence import save

    child = output.with_suffix(output.suffix + ".pytest.json").absolute()
    command = (
        Command(sys.executable)
        .args(
            "-m",
            "scripts.validation.protected",
            str(child),
            *arguments,
            "--durations=30",
        )
        .cwd(resolve_path(root))
        .with_environment(
            {
                "COVERAGE_FILE": str(
                    output.with_suffix(output.suffix + ".coverage").absolute()
                )
            }
        )
        .with_timeout(Duration.hours(1))
    )

    async def execute() -> CommandResult:
        execution = CommandExecutor(
            output_policy=CommandOutputPolicy(
                max_stdout_bytes=32 << 20, max_stderr_bytes=4 << 20
            )
        ).start(command)
        async for event in execution.events():
            if isinstance(event, (CommandStdout, CommandStderr)):
                print(event.data.decode("utf-8", errors="replace"), end="", flush=True)  # noqa: T201
        return await execution

    result = asyncio.run(execute())
    for name, payload in (("stdout", result.stdout), ("stderr", result.stderr)):
        save(
            output.with_suffix(output.suffix + "." + name),
            payload.decode("utf-8", errors="replace"),
        )
    if result.stdout_truncated or result.stderr_truncated or not child.exists():
        message = "Protected child output incomplete; retain intent and diagnose infrastructure"
        raise RuntimeError(message)
    data = json.loads(child.read_text(encoding="utf-8"))
    observations.phases = data["phases"]
    observations.collection_errors = data["collection_errors"]
    return int(result.exit_code)


def main() -> int:
    """Bootstrap only pytest/hooks before instrumentation; serialize afterwards."""
    import pytest

    from scripts.validation.observation import Observations

    output = Path(sys.argv[1])
    observations = Observations()
    code = int(pytest.main(sys.argv[2:], plugins=[observations]))
    from scripts.validation.evidence import (
        save,
    )

    save(
        output,
        json.dumps(
            {
                "phases": observations.phases,
                "collection_errors": observations.collection_errors,
            }
        ),
    )
    return code


if __name__ == "__main__":
    raise SystemExit(main())
