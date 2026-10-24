# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, PLR2004 -- fixed local coding operations
"""Task-scoped coding observations over existing managed Commands, not a shell."""

from __future__ import annotations

import ast
import asyncio
import hashlib
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING, Any

from apps.qwen.development_task import _hash, _runner_sources, _save, _timed_command
from apps.qwen.model_tool_composition import normalize_tool_descriptor
from devtools.core.paths import resolve_path
from devtools.resources.commands import CommandError
from devtools.resources.filesystem import TextFile, write
from devtools.tools import ToolDescriptor, ToolRunner

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from apps.qwen.tasks import CodingTask
    from devtools.models.interaction import ModelToolCall, ModelToolDefinition

COMMAND_TOOL_NAMES = ("git_inspect", "run_check", "check_changes", "is_current")
CHECKS = ("tests", "oracle", "ruff", "format", "typing")


def command_definitions(task: CodingTask) -> tuple[ModelToolDefinition, ...]:
    """Expose fixed argv choices; model text never becomes executable code."""
    if not task.command_tools:
        return ()
    specs: tuple[tuple[str, str, dict[str, Any]], ...] = (
        (
            "git_inspect",
            (
                "Inspect scoped current Git status/diff or five history commits; "
                "never mutates Git."
            ),
            {
                "operation": {"type": "string", "enum": ["status", "diff", "history"]},
                "path": {
                    "type": "string",
                    "enum": sorted({*task.sources, *task.tests, *task.read_paths}),
                },
            },
        ),
        (
            "run_check",
            (
                "Run a host-owned test/oracle/lint/format/type check on source. "
                "Use all for independent checks bound to current source/plan. "
                "Full logs are archived. No arbitrary argv or writes."
            ),
            {"check": {"type": "string", "enum": [*CHECKS, "all"]}},
        ),
        (
            "check_changes",
            (
                "Discover authorized candidate changes and run all fixed checks. "
                "Returns scoped source/Git/plan evidence, never publication authority."
            ),
            {},
        ),
        (
            "is_current",
            (
                "Reauthenticate a saved check_changes report without rerunning checks. "
                "Freshness is separate from correctness or review approval."
            ),
            {"report": {"type": "object"}},
        ),
    )
    return tuple(
        normalize_tool_descriptor(
            ToolDescriptor(
                name,
                description,
                json.dumps(
                    {
                        "type": "object",
                        "properties": properties,
                        "required": list(properties),
                        "additionalProperties": False,
                    }
                ),
            )
        )
        for name, description, properties in specs
    )


async def run_check(
    root: Path, folder: Path, task: CodingTask, check: str
) -> dict[str, Any]:
    """Share fixed check construction for inspection and final acceptance."""
    if check == "all":
        return await CodingCommands(root, folder, task)._check_bundle()  # noqa: SLF001 -- same module-level selector
    if check not in CHECKS:
        raise ValueError("Unsupported coding check")
    paths = (
        *task.existing_sources,
        *(p for p in task.new_paths if (root / p).exists()),
    )
    arguments = {
        "tests": ("-I", "-B", str(folder / "tests-runner.py")),
        "oracle": ("-I", "-B", str(folder / "oracle-runner.py")),
        "ruff": ("-m", "ruff", "check", *paths),
        "format": ("-m", "ruff", "format", "--diff", *paths),
        "typing": ("-m", "mypy", "--strict", *paths),
    }[check]
    return await _timed_command(root, sys.executable, *arguments)


def _input_identity(base: Path, path: str) -> str | None:
    """Hash only a regular, directly addressed input within its host scope."""
    raw = base / path
    resolved = resolve_path(path, base_directory=base).value
    if raw != resolved or not resolved.is_relative_to(base):
        raise ValueError("Input aliases or escapes the authorized scope: " + path)
    if raw.exists() and not raw.is_file():
        raise ValueError("Input is not a regular file: " + path)
    return _hash(raw) if raw.exists() else None


def _bundle_state(
    root: Path, folder: Path, task: CodingTask
) -> tuple[dict[str, str | None], dict[str, Any], list[str]]:
    """Observe current source separately from the fixed host validation inputs."""
    errors: list[str] = []

    def observe(base: Path, path: str) -> str | None:
        try:
            return _input_identity(base, path)
        except (OSError, ValueError) as error:
            errors.append(str(error))
            return None

    sources = {p: observe(root, p) for p in task.sources}
    inputs = {p: observe(root, p) for p in (*task.tests, *task.read_paths)}
    expected = dict(task.baseline_hashes)
    for path, identity in inputs.items():
        if identity != expected.get(path):
            errors.append("Frozen validation input differs: " + path)
    errors.extend(
        "Required source/test/read input unavailable: " + path
        for path in (*task.existing_sources, *task.tests, *task.read_paths)
        if sources.get(path, inputs.get(path)) is None
    )
    runners = {
        p: observe(folder, p)
        for p in ("tests-runner.py", "oracle-runner.py", "pytest.ini")
    }
    configuration_paths = {
        "pyproject.toml",
        "pytest.ini",
        "setup.cfg",
        "mypy.ini",
        ".mypy.ini",
        "ruff.toml",
        ".ruff.toml",
    }
    for path in (*task.sources, *task.tests):
        directory = (root / path).parent
        while directory.is_relative_to(root):
            relative = directory.relative_to(root)
            if ".." in relative.parts:
                break
            names = (
                ("conftest.py",)
                if path in task.tests
                else ("pyproject.toml", "ruff.toml", ".ruff.toml")
            )
            configuration_paths.update((relative / name).as_posix() for name in names)
            if directory == root:
                break
            directory = directory.parent
    configuration = {p: observe(root, p) for p in sorted(configuration_paths)}
    expected_runners = {
        p: hashlib.sha256(text.encode()).hexdigest()
        for p, text in _runner_sources(root, folder, task).items()
    }
    plan = {
        "task_definition_sha256": task.definition_sha256,
        "repository_root": str(root),
        "runner_directory": str(folder),
        "python": sys.executable,
        "python_version": sys.version,
        "implementation": {
            name: _hash(resolve_path(__file__).value.parent / name)
            for name in (
                "commands.py",
                "change_checks.py",
                "development_task.py",
                "tasks.py",
            )
        },
        "inputs": inputs,
        "runners": runners,
        "expected_runners": expected_runners,
        "configuration": configuration,
    }
    return sources, plan, errors


def _plan_identity(plan: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(plan, sort_keys=True).encode()).hexdigest()


class CodingCommands:
    """Fixed task-local ToolRunner adapter; no generic command dispatcher."""

    name = "qwen_coding_commands"
    description = "Host-selected coding checks and read-only Git observations."

    def __init__(self, root: Path, folder: Path, task: CodingTask) -> None:
        """Bind operation scope and original host-written validation runners."""
        self.root, self.folder, self.task = root, folder, task
        self.count = 0
        _, self._bound_plan, _ = _bundle_state(root, folder, task)
        self._change_git: dict[str, Any] | None = None
        self._changes_lock = asyncio.Lock()

    def validate(self, arguments: tuple[str, dict[str, Any]]) -> None:
        """Refuse unknown operations, paths and keys before execution."""
        name, values = arguments
        descriptor = next(
            (d for d in command_definitions(self.task) if d.name == name), None
        )
        if descriptor is None or not isinstance(values, dict):
            raise ValueError("Coding operation is not task-authorized")
        props = json.loads(descriptor.input_schema_json)["properties"]
        if set(values) != set(props) or any(
            values[k] not in p["enum"]
            if "enum" in p
            else not isinstance(values[k], dict)
            for k, p in props.items()
        ):
            raise ValueError("Unsupported coding operation arguments")

    async def dispatch(self, call: ModelToolCall) -> dict[str, Any]:
        """Materialize one native request through the canonical ToolRunner."""
        return await ToolRunner().execute(
            self, (call.name, json.loads(call.arguments_json))
        )

    async def execute(self, arguments: tuple[str, dict[str, Any]]) -> dict[str, Any]:
        """Archive full check output and return a bounded, version-bound view."""
        name, values = arguments
        if name == "check_changes":
            from apps.qwen.change_checks import (  # noqa: PLC0415 -- same owner; avoid import cycle
                check_changes,
            )

            async with self._changes_lock:
                return await check_changes(self)
        if name == "is_current":
            from apps.qwen.change_checks import (  # noqa: PLC0415 -- same owner
                current_report,
            )

            return await current_report(self, values["report"])
        if name == "run_check" and values["check"] == "all":
            return await self._check_bundle()
        versions = {
            p: _hash(self.root / p) if (self.root / p).exists() else None
            for p in self.task.sources
        }
        if name == "run_check":
            result = await run_check(self.root, self.folder, self.task, values["check"])
        else:
            args = {
                "status": ("status", "--short", "--", values["path"]),
                "diff": ("diff", "HEAD", "--", values["path"]),
                "history": ("log", "-5", "--format=%H %s", "--", values["path"]),
            }[values["operation"]]
            result = await _timed_command(self.root, "git", *args)
        if versions != {
            p: _hash(self.root / p) if (self.root / p).exists() else None
            for p in self.task.sources
        }:
            raise ValueError("Read/check operation unexpectedly mutated source")
        self.count += 1
        target = self.folder / f"coding-command-{self.count:02d}.json"
        _save(
            target,
            {"call": call_data(arguments), "source_sha256": versions, "result": result},
        )
        return {
            "operation": name,
            "arguments": values,
            "source_sha256": versions,
            "status": "PASS" if not result["failed"] else "FAIL",
            "exit_code": result["exit_code"],
            "elapsed_seconds": result["elapsed_seconds"],
            "stdout": result["stdout"][:3000],
            "stderr": result["stderr"][:3000],
            "truncated": len(result["stdout"]) > 3000 or len(result["stderr"]) > 3000,
            "evidence": str(target.relative_to(self.folder)),
            "authority": "observation only; does not confer acceptance or publication",
        }

    async def _check_bundle(self) -> dict[str, Any]:  # noqa: C901, PLR0912, PLR0915 -- five fixed checks, one evidence journal
        """Compose existing selectors; never certify review or publish source."""
        self.count += 1
        target = self.folder / f"coding-command-{self.count:02d}.json"
        # Preserve existing immutable receipts even across fresh Tool instances.
        while target.exists():
            self.count += 1
            target = self.folder / f"coding-command-{self.count:02d}.json"
        evidence = target.relative_to(self.folder).as_posix()
        sources, plan, errors = _bundle_state(self.root, self.folder, self.task)
        source_unchanged = True
        plan_unchanged = plan == self._bound_plan
        checks: dict[str, Any] = {}
        for name in CHECKS:
            applicable = (
                self.task.quality_checks
                if name in {"ruff", "format"}
                else self.task.command_tools
                if name == "typing"
                else True
            )
            checks[name] = {
                "status": "NOT_RUN" if applicable else "NOT_APPLICABLE",
                "elapsed_seconds": 0.0,
                "stdout": "",
                "stderr": "",
                "truncated": False,
                "evidence": evidence,
            }
        for name, available in (
            (
                "tests",
                bool(self.task.tests) and bool(plan["runners"]["tests-runner.py"]),
            ),
            (
                "oracle",
                bool(self.task.oracle.strip())
                and bool(plan["runners"]["oracle-runner.py"]),
            ),
        ):
            if (
                not available
                or plan["runners"][name + "-runner.py"]
                != plan["expected_runners"][name + "-runner.py"]
                or (
                    name == "tests"
                    and plan["runners"]["pytest.ini"]
                    != plan["expected_runners"]["pytest.ini"]
                )
            ):
                checks[name].update(
                    status="BLOCKED",
                    stderr="Required host check plan/runner unavailable",
                )
        report: dict[str, Any] = {
            "operation": "run_check",
            "arguments": {"check": "all"},
            "task_definition_sha256": plan["task_definition_sha256"],
            "source_sha256": sources,
            "source_after_sha256": sources,
            "plan_sha256": _plan_identity(plan),
            "plan_after_sha256": _plan_identity(plan),
            "source_unchanged": source_unchanged,
            "plan_unchanged": plan_unchanged,
            "plan": plan,
            "checks": checks,
            "status": "BLOCKED",
            "diagnostics": errors,
            "evidence": evidence,
            "authority": "observation only; does not confer acceptance or publication",
        }
        started = time.perf_counter()
        cancellation: asyncio.CancelledError | None = None

        def journal() -> None:
            report["elapsed_seconds"] = time.perf_counter() - started
            try:
                _save(
                    target,
                    {
                        "call": call_data(("run_check", {"check": "all"})),
                        "result": report,
                    },
                    overwrite=target.exists(),
                )
            except OSError as error:
                if cancellation is None:
                    raise
                cancellation.add_note("Incomplete cancellation evidence: " + str(error))

        async def authenticate() -> None:
            nonlocal source_unchanged, plan_unchanged
            current, current_plan, issues = _bundle_state(
                self.root, self.folder, self.task
            )
            source_unchanged = source_unchanged and current == sources
            plan_unchanged = plan_unchanged and current_plan == plan
            errors.extend(issue for issue in issues if issue not in errors)
            if self._change_git is not None:
                from apps.qwen.change_checks import (  # noqa: PLC0415 -- same owner
                    git_state,
                )

                try:
                    if await git_state(self, current_plan) != self._change_git:
                        errors.append("Git/index state changed during validation")
                except (CommandError, OSError, ValueError) as error:
                    errors.append("Git observation unavailable: " + str(error))
            report.update(
                source_after_sha256=current,
                plan_after_sha256=_plan_identity(current_plan),
                source_unchanged=source_unchanged,
                plan_unchanged=plan_unchanged,
            )

        journal()  # A crash leaves NOT_RUN, never invented successful outcomes.
        try:
            for name in CHECKS:
                await authenticate()
                if errors or not source_unchanged or not plan_unchanged:
                    break
                row = checks[name]
                if row["status"] != "NOT_RUN":
                    continue
                row.update(
                    status="NOT_RUN",
                    stderr="Check started; completion not yet recorded",
                )
                journal()
                check_started = time.perf_counter()
                try:
                    result = await run_check(self.root, self.folder, self.task, name)
                    row.update(result, status="FAIL" if result["failed"] else "PASS")
                    if result.get("stdout_truncated") or result.get("stderr_truncated"):
                        row.update(
                            status="BLOCKED",
                            diagnostic=(
                                "Output retention limit exceeded; incomplete evidence"
                            ),
                        )
                except asyncio.CancelledError as error:
                    cancellation = error
                    row.update(
                        status="INTERRUPTED",
                        stderr="Host cancellation; check incomplete",
                    )
                    raise
                except (CommandError, OSError, ValueError) as error:
                    row.update(
                        status="BLOCKED", stderr=f"{type(error).__name__}: {error}"
                    )
                finally:
                    row["elapsed_seconds"] = time.perf_counter() - check_started
                    await authenticate()
                    journal()
            statuses = {row["status"] for row in checks.values()}
            report["status"] = (
                "BLOCKED"
                if errors
                or not source_unchanged
                or not plan_unchanged
                or statuses & {"BLOCKED", "NOT_RUN", "INTERRUPTED"}
                else "FAIL"
                if "FAIL" in statuses
                else "PASS"
            )
        finally:
            await authenticate()
            if errors or not source_unchanged or not plan_unchanged:
                report["status"] = "BLOCKED"
            journal()
        # Raw command outputs remain in the journal; only this view is bounded.
        view = {**report, "diagnostics": [e[:1000] for e in errors[:8]], "checks": {}}
        view.pop("plan")
        for name, row in checks.items():
            view["checks"][name] = {
                **row,
                "stdout": row["stdout"][:3000],
                "stderr": row["stderr"][:3000],
                "truncated": len(row["stdout"]) > 3000 or len(row["stderr"]) > 3000,
            }
        return view

    def is_current(self, report: dict[str, Any]) -> bool:
        """Preserve the original synchronous host API; native dispatch is async."""
        from apps.qwen.change_checks import current_report  # noqa: PLC0415

        # This bridge runs the same bounded managed observations, never a second
        # command executor. It also works inside an existing caller event loop.
        with ThreadPoolExecutor(max_workers=1) as bridge:
            result = bridge.submit(
                lambda: asyncio.run(current_report(self, report))
            ).result()
        return bool(result["current"])


def call_data(arguments: tuple[str, dict[str, Any]]) -> dict[str, Any]:
    """Project native structured arguments for the existing evidence record."""
    return {"name": arguments[0], "arguments": arguments[1]}


async def format_sources(
    root: Path, folder: Path, task: CodingTask, admit: Callable[[str, str], None] | None
) -> dict[str, str]:
    """Opt-in deterministic formatting with AST equivalence and pre-write journal.

    Only individual source files enter ignored evidence; never a source-tree copy.
    Semantic diagnostics return to the existing coding repair loop unchanged.
    """
    changed = {}
    for number, path in enumerate(task.sources):
        source = (root / path).read_bytes().decode("utf-8")
        try:
            tree = ast.dump(ast.parse(source), include_attributes=False)
        except SyntaxError:
            continue
        scratch = folder / f"format-{number}.py"
        write(TextFile(resolve_path(scratch), source))
        result = await _timed_command(
            root,
            sys.executable,
            "-m",
            "ruff",
            "format",
            "--config",
            str(root / "pyproject.toml"),
            str(scratch),
        )
        _save(folder / f"format-{number}.json", result)
        if result["failed"]:
            continue
        text = scratch.read_bytes().decode("utf-8")
        if ast.dump(ast.parse(text), include_attributes=False) != tree:
            raise ValueError("Formatter changed source AST")
        if text != source:
            if admit is not None:
                admit(path, text)
            write(TextFile(resolve_path(root / path), text))
            changed[path] = text
    return changed
