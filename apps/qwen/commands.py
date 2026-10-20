# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, PLR2004 -- fixed local coding operations
"""Task-scoped coding observations over existing managed Commands, not a shell."""

from __future__ import annotations

import ast
import json
import sys
from typing import TYPE_CHECKING, Any

from apps.qwen.development_task import _hash, _save, _timed_command
from apps.qwen.model_tool_composition import normalize_tool_descriptor
from devtools.core.paths import resolve_path
from devtools.resources.filesystem import TextFile, write
from devtools.tools import ToolDescriptor, ToolRunner

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from apps.qwen.tasks import CodingTask
    from devtools.models.interaction import ModelToolCall, ModelToolDefinition

COMMAND_TOOL_NAMES = ("git_inspect", "run_check")
CHECKS = ("tests", "oracle", "ruff", "format", "typing")


def command_definitions(task: CodingTask) -> tuple[ModelToolDefinition, ...]:
    """Expose fixed argv choices; model text never becomes executable code."""
    if not task.command_tools:
        return ()
    specs = (
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
                "Full logs are archived. No arbitrary argv or writes."
            ),
            {"check": {"type": "string", "enum": list(CHECKS)}},
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


class CodingCommands:
    """Fixed task-local ToolRunner adapter; no generic command dispatcher."""

    name = "qwen_coding_commands"
    description = "Host-selected coding checks and read-only Git observations."

    def __init__(self, root: Path, folder: Path, task: CodingTask) -> None:
        """Bind operation scope and original host-written validation runners."""
        self.root, self.folder, self.task = root, folder, task
        self.count = 0

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
            values[k] not in p["enum"] for k, p in props.items()
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
