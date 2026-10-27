# Copyright (c) 2026
# ruff: noqa: COM812 -- legacy task validation compatibility adapter
"""Host-owned legacy runner/oracle policy over reusable framework checks.

This adapter preserves CodingTask and report formats. It is not the framework
check engine, worker loop, publication authority or a scientific controller.
"""

from __future__ import annotations

import hashlib
import json
import time
from typing import TYPE_CHECKING, Any, cast

from devtools.core.paths import resolve_path
from devtools.core.time import Duration, Timestamp
from devtools.resources.commands import Command
from devtools.resources.filesystem import FileFormat, TextFile, read, write
from devtools.tools import ToolRunner
from devtools.tools.checks import FixedCheck, FixedCheckPlan, FixedCheckTool

if TYPE_CHECKING:
    from pathlib import Path

    from apps.qwen.commands import CodingCommands
    from apps.qwen.tasks import CodingTask
    from devtools.core.paths import ResolvedPath


def _read_text(path: ResolvedPath) -> TextFile:
    """Reuse the exact existing Resource text representation."""
    return cast("TextFile", read(path, file_format=FileFormat.TEXT))


def _save(path: Path, value: object, *, overwrite: bool = False) -> None:
    write(
        TextFile(
            resolve_path(path), json.dumps(value, indent=2, sort_keys=True) + "\n"
        ),
        overwrite=overwrite,
    )


def _hash(path: Path) -> str:
    value = _read_text(resolve_path(path))
    return hashlib.sha256(value.content.encode(value.encoding)).hexdigest()


async def _command(root: Path, *args: str) -> dict[str, Any]:
    checked = await ToolRunner().execute(
        FixedCheckTool(
            FixedCheckPlan(
                resolve_path(root),
                (
                    FixedCheck(
                        "host-command",
                        Command(args[0])
                        .args(*args[1:])
                        .cwd(resolve_path(root))
                        .with_timeout(Duration.minutes(2)),
                    ),
                ),
            )
        ),
        "host-command",
    )
    result = checked.command_result
    return {
        "argv": args,
        "exit_code": result.exit_code,
        "stdout": result.stdout.decode(errors="replace"),
        "stderr": result.stderr.decode(errors="replace"),
        "failed": result.failed,
        "stdout_truncated": result.stdout_truncated,
        "stderr_truncated": result.stderr_truncated,
    }


async def _timed_command(root: Path, *args: str) -> dict[str, Any]:
    """Retain stage timing for the one upfront-context experiment."""
    started_at = str(Timestamp.now())
    started = time.perf_counter()
    result = await _command(root, *args)
    result.update(started_at=started_at, elapsed_seconds=time.perf_counter() - started)
    return result


def _runner_sources(root: Path, folder: Path, task: CodingTask) -> dict[str, str]:
    """Render the existing fixed host runners; no configurable execution plan."""
    workspace = root
    module_name = task.source.removeprefix("src/").removesuffix(".py").replace("/", ".")
    prelude = (
        "import sys\nfrom pathlib import Path\n"
        f"sys.path.insert(0, {str(workspace / 'src')!r})\n"
        + (
            f"sys.path.insert(0, {str(workspace)!r})\n"
            if task.source.startswith("apps/")
            else ""
        )
        + f"import {module_name} as module\n"
        "assert Path(module.__file__).resolve() == "
        f"Path({str(workspace / task.source)!r})\n"
    )
    oracle_text = prelude + task.oracle
    test_arguments = [
        *(str(workspace / test) for test in task.tests),
        "-c",
        str(folder / "pytest.ini"),
        f"--confcutdir={workspace}",
        "--no-cov",
        "-q",
    ]
    tests_text = (
        prelude
        + "import json\nimport pytest\n"
        # Capture primary facts before pytest's traceback formatting. Some
        # tests deliberately forbid ast.parse, which formatters also use.
        + "class PrimaryFailures:\n"
        + "    @pytest.hookimpl(hookwrapper=True, tryfirst=True)\n"
        + "    def pytest_runtest_makereport(self, item, call):\n"
        + "        if call.excinfo is not None:\n"
        + "            facts = dict(nodeid=item.nodeid, phase=call.when, "
        + "exception=call.excinfo.type.__name__, "
        + "message=str(call.excinfo.value)[:1000], "
        + "message_truncated=len(str(call.excinfo.value)) > 1000)\n"
        + "            print('QWEN_TEST_FAILURE ' + json.dumps(facts), "
        + "file=sys.stderr, flush=True)\n"
        + "        yield\n"
        + f"arguments = {test_arguments!r}\n"
        + "raise SystemExit(pytest.main(arguments, plugins=[PrimaryFailures()]))\n"
    )
    return {
        "oracle-runner.py": oracle_text,
        "tests-runner.py": tests_text,
        "pytest.ini": "[pytest]\n",
    }


def prepare_task_validation(root: Path, folder: Path, task: CodingTask) -> Path:
    """Bind validation to the selected checkout; never copy a source tree."""
    workspace = root
    # Fixed pytest options and exact local imports. Repository conftest code is
    # part of the pinned host-owned validation environment, not model authority.
    for path, text in _runner_sources(root, folder, task).items():
        write(TextFile(resolve_path(folder / path), text))
    return workspace


async def validate_task(
    root: Path,
    folder: Path,
    *,
    task: CodingTask,
    commands: CodingCommands | None = None,
) -> dict[str, Any]:
    """Use the shared frozen-input/check journal, retaining full host diagnostics."""
    from apps.qwen.commands import (  # noqa: PLC0415 -- task-policy dependency cycle
        CodingCommands,
    )

    bound = commands if commands is not None else CodingCommands(root, folder, task)
    bundle = await bound._check_bundle(bounded=False)  # noqa: SLF001 -- host adapter over the same application-owned validation
    result = {
        name: {
            **row,
            "failed": row["status"] != "PASS",
            "exit_code": row.get("exit_code"),
        }
        for name, row in bundle["checks"].items()
        if row["status"] != "NOT_APPLICABLE"
    }
    return {
        **result,
        "integrity": {
            "failed": bundle["status"] == "BLOCKED",
            "source_unchanged": bundle["source_unchanged"],
            "plan_unchanged": bundle["plan_unchanged"],
            "diagnostics": bundle["diagnostics"],
            "evidence": bundle["evidence"],
        },
        "accepted": bundle["status"] == "PASS",
    }
