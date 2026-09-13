# Copyright (c) 2026
# ruff: noqa: E402, E501, INP001, T201
"""Run one bounded live Qwen directory-list then repository-read acceptance."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING
from uuid import uuid4

_REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(_REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPOSITORY_ROOT))

from devtools.agents.conversation import (
    Conversation,
    ConversationMessage,
    ConversationMessageRole,
    InteractionSource,
)
from devtools.core.paths import ResolvedPath
from devtools.execution import Runtime
from devtools.models.interaction.providers import (
    LlamaCppInteraction,
    LlamaCppInteractionError,
)
from devtools.resources.commands import Command, CommandExecutor
from devtools.tools.filesystem import (
    ListRepositoryDirectoryTool,
    ReadRepositoryFileTool,
)
from experiments.qwen.two_action_read_only_experiment import (
    QwenListDirectoryCycle,
    QwenReadOnlyCycle,
    QwenReadRepositoryFileCycle,
    QwenTwoActionReadOnlyExperiment,
    QwenTwoActionReadOnlyExperimentResult,
    ReadOnlyProposalError,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.models.interaction import ModelInteraction


_DEFAULT_ENDPOINT = "http://127.0.0.1:8080"
_DEFAULT_MODEL = "qwen38-local"
_CALLER_SOURCE = InteractionSource("qwen-two-action-read-only-acceptance")
_SERVICE_SCRIPT = Path(__file__).with_name("llama_cpp_service.py")
_REPORT_SCHEMA = "qwen-two-action-read-only-acceptance/1"
_REQUIRED_ACTIONS = 2


@dataclass(frozen=True, slots=True)
class QwenTwoActionReadOnlyFixture:
    """Describe the inert unpredictable fixture used by this one acceptance."""

    root: Path
    target_filename: str
    nonce: str


@dataclass(frozen=True, slots=True)
class QwenTwoActionReadOnlyReport:
    """Retain bounded live acceptance diagnostics without framework tracing."""

    task: ConversationMessage
    history: tuple[ConversationMessage, ...]
    execution_actions: tuple[str, ...]
    execution_paths: tuple[str, ...]
    cycles: tuple[QwenReadOnlyCycle, ...]
    result: QwenTwoActionReadOnlyExperimentResult | None
    failure_category: str | None
    error_type: str | None
    error_message: str | None
    latest_assistant: ConversationMessage | None


@dataclass(frozen=True, slots=True)
class QwenTwoActionReadOnlyOutcome:
    """Retain this script's completed artifact facts after fixture cleanup."""

    report: QwenTwoActionReadOnlyReport
    target_filename: str
    nonce: str
    persistent_service_status: str | None
    persistent_service_error_type: str | None
    persistent_service_error_message: str | None
    fixture_cleanup_succeeded: bool


def parse_arguments(arguments: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse fixed persistent-endpoint inputs and an optional durable report path."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--endpoint", default=_DEFAULT_ENDPOINT)
    parser.add_argument("--model", default=_DEFAULT_MODEL)
    parser.add_argument(
        "--report-path",
        type=Path,
        help="Write the authoritative completed JSON acceptance artifact to this path.",
    )
    return parser.parse_args(arguments)


def initial_task() -> ConversationMessage:
    """Construct the fixed model-facing task without target-file or nonce leakage."""
    content = """Find the only direct file in facts whose basename begins target-, read it, and return its exact contents.

You do not know the directory contents, target filename, or file contents. The permitted read-only actions are:

list_repository_directory: List bounded direct entries inside one repository-relative directory.
{"action":"list_repository_directory","path":"<repository-relative-path>"}

read_repository_file: Read one repository-relative supported text file.
{"action":"read_repository_file","path":"<repository-relative-path>"}

If requesting an action, your entire response must be exactly one bare JSON object and nothing else. Do not use Markdown or prose around a proposal. When you have enough information, provide the final answer as plain text."""
    return ConversationMessage.new(
        content,
        role=ConversationMessageRole.USER,
        source=_CALLER_SOURCE,
    )


def create_fixture(parent: Path) -> QwenTwoActionReadOnlyFixture:
    """Create an isolated directory whose target filename and nonce are unpredictable."""
    root = parent / f"qwen-two-action-{uuid4()}"
    facts = root / "facts"
    facts.mkdir(parents=True)
    target_filename = f"target-{uuid4()}.txt"
    nonce = f"NONCE-{uuid4()}"
    (facts / f"decoy-{uuid4()}.txt").write_text("decoy", encoding="utf-8")
    (facts / target_filename).write_text(nonce, encoding="utf-8")
    return QwenTwoActionReadOnlyFixture(root, target_filename, nonce)


async def run_acceptance(
    *,
    task: ConversationMessage,
    repository_root: Path,
    interaction: ModelInteraction,
) -> QwenTwoActionReadOnlyReport:
    """Run production experiment code while retaining bounded failure diagnostics."""
    session = Conversation.new()
    completed_cycles: list[QwenReadOnlyCycle] = []
    experiment = QwenTwoActionReadOnlyExperiment(
        runtime=Runtime(),
        conversation=session,
        interaction=interaction,
        repository_root=ResolvedPath(repository_root),
        on_cycle_completed=completed_cycles.append,
    )
    actions: list[str] = []
    paths: list[str] = []
    original_list = ListRepositoryDirectoryTool.execute
    original_read = ReadRepositoryFileTool.execute

    async def counted_list(
        tool: ListRepositoryDirectoryTool,
        path: ResolvedPath,
    ) -> object:
        actions.append("list_repository_directory")
        paths.append(str(path))
        return await original_list(tool, path)

    async def counted_read(tool: ReadRepositoryFileTool, path: ResolvedPath) -> object:
        actions.append("read_repository_file")
        paths.append(str(path))
        return await original_read(tool, path)

    ListRepositoryDirectoryTool.execute = counted_list
    ReadRepositoryFileTool.execute = counted_read
    try:
        result = await experiment.run(task)
    except asyncio.CancelledError:
        raise
    except Exception as error:  # noqa: BLE001 - live acceptance retains failure state.
        history = tuple(session.history)
        return QwenTwoActionReadOnlyReport(
            task,
            history,
            tuple(actions),
            tuple(paths),
            tuple(completed_cycles),
            None,
            _failure_category(error),
            type(error).__name__,
            str(error),
            _latest_assistant(history, interaction.source),
        )
    finally:
        ListRepositoryDirectoryTool.execute = original_list
        ReadRepositoryFileTool.execute = original_read
    return QwenTwoActionReadOnlyReport(
        task,
        tuple(session.history),
        tuple(actions),
        tuple(paths),
        result.cycles,
        result,
        None,
        None,
        None,
        _latest_assistant(tuple(session.history), interaction.source),
    )


def _latest_assistant(
    history: tuple[ConversationMessage, ...],
    interaction_source: InteractionSource,
) -> ConversationMessage | None:
    """Return the latest exact retained assistant ConversationMessage from the selected source."""
    return next(
        (
            message
            for message in reversed(history)
            if message.role is ConversationMessageRole.ASSISTANT
            and message.source == interaction_source
        ),
        None,
    )


def _failure_category(error: Exception) -> str:
    """Classify only this bounded acceptance's modeled failures."""
    if isinstance(error, ReadOnlyProposalError):
        return "MODEL CONFORMANCE"
    if isinstance(error, LlamaCppInteractionError):
        return "PROVIDER"
    return "FRAMEWORK BOUNDARY"


def _verdict(outcome: QwenTwoActionReadOnlyOutcome) -> str:
    """Evaluate only this fixture's explicit causal acceptance requirements."""
    report = outcome.report
    if report.failure_category is not None:
        return f"FAIL — {report.failure_category}"
    if report.result is None or outcome.persistent_service_error_type is not None:
        return "FAIL — FRAMEWORK BOUNDARY"
    cycles = report.result.cycles
    if (
        len(cycles) != _REQUIRED_ACTIONS
        or report.execution_actions
        != ("list_repository_directory", "read_repository_file")
        or not isinstance(cycles[0], QwenListDirectoryCycle)
        or not isinstance(cycles[1], QwenReadRepositoryFileCycle)
        or cycles[0].relative_path != "facts"
        or cycles[1].relative_path != f"facts/{outcome.target_filename}"
    ):
        return "FAIL — MODEL CONFORMANCE"
    if report.result.final_message.content != outcome.nonce:
        return "FAIL — MODEL CAPABILITY"
    return "PASS"


def _message_payload(message: ConversationMessage) -> dict[str, str]:
    """Serialize only safe retained ConversationMessage facts for this script-local artifact."""
    return {
        "role": message.role.value,
        "source": message.source.value,
        "content": message.content,
    }


def _cycle_payload(
    cycle: QwenListDirectoryCycle | QwenReadRepositoryFileCycle,
) -> dict[str, object]:
    """Serialize heterogeneous experiment-local cycles without a generic event model."""
    payload: dict[str, object] = {
        "proposal": _message_payload(cycle.proposal),
        "relative_path": cycle.relative_path,
        "resolved_path": str(cycle.resolved_path),
        "result_projection": cycle.result_projection,
        "follow_up": _message_payload(cycle.follow_up),
    }
    if isinstance(cycle, QwenListDirectoryCycle):
        payload["action"] = "list_repository_directory"
        payload["listing"] = {
            "entries": [
                {"name": entry.name, "kind": entry.kind.value}
                for entry in cycle.listing.entries
            ],
            "truncated": cycle.listing.truncated,
        }
    else:
        payload["action"] = "read_repository_file"
    return payload


def _report_payload(outcome: QwenTwoActionReadOnlyOutcome) -> dict[str, object]:
    """Construct one complete machine-readable acceptance artifact."""
    report = outcome.report
    return {
        "schema": _REPORT_SCHEMA,
        "verdict": _verdict(outcome),
        "fixture": {
            "target_filename": outcome.target_filename,
            "nonce": outcome.nonce,
            "cleanup": "completed" if outcome.fixture_cleanup_succeeded else "failed",
        },
        "task": _message_payload(report.task),
        "history": [_message_payload(message) for message in report.history],
        "latest_assistant": _message_payload(report.latest_assistant)
        if report.latest_assistant
        else None,
        "tool_executions": {
            "actions": list(report.execution_actions),
            "resolved_paths": list(report.execution_paths),
        },
        "cycles": [_cycle_payload(cycle) for cycle in report.cycles],
        "final_answer": report.result.final_message.content if report.result else None,
        "failure": {
            "category": report.failure_category,
            "error_type": report.error_type,
            "error_message": report.error_message,
        },
        "persistent_service": {
            "status": outcome.persistent_service_status,
            "error_type": outcome.persistent_service_error_type,
            "error_message": outcome.persistent_service_error_message,
        },
    }


def _write_report(path: Path, payload: dict[str, object]) -> None:
    """Atomically replace one caller-selected completed local acceptance artifact."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(f".{path.name}.{uuid4()}.tmp")
    try:
        with temporary_path.open("w", encoding="utf-8", newline="\n") as output:
            json.dump(payload, output, indent=2, sort_keys=True)
            output.write("\n")
            output.flush()
            os.fsync(output.fileno())
        temporary_path.replace(path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


async def _persistent_status() -> str:
    """Observe the independently managed persistent Qwen service after acceptance."""
    result = await CommandExecutor().execute(
        Command(sys.executable, (str(_SERVICE_SCRIPT), "status")),
    )
    output = (result.stdout or result.stderr).decode(errors="replace").strip()
    return output or "persistent service status produced no output"


async def run(arguments: argparse.Namespace) -> QwenTwoActionReadOnlyOutcome:
    """Run one temporary-fixture acceptance without owning persistent lifecycle."""
    with tempfile.TemporaryDirectory(prefix="devtools-qwen-two-action-") as directory:
        fixture = create_fixture(Path(directory))
        status: str | None = None
        status_error: Exception | None = None
        cleanup_succeeded = False
        try:
            report = await run_acceptance(
                task=initial_task(),
                repository_root=fixture.root,
                interaction=LlamaCppInteraction(
                    endpoint=arguments.endpoint,
                    model=arguments.model,
                    source=InteractionSource("qwen"),
                ),
            )
            try:
                status = await _persistent_status()
            except Exception as error:  # noqa: BLE001 - report post-run status failure.
                status_error = error
        finally:
            try:
                shutil.rmtree(fixture.root)
            except FileNotFoundError:
                pass
            else:
                cleanup_succeeded = True
        return QwenTwoActionReadOnlyOutcome(
            report,
            fixture.target_filename,
            fixture.nonce,
            status,
            type(status_error).__name__ if status_error else None,
            str(status_error) if status_error else None,
            cleanup_succeeded,
        )


def _print_outcome(outcome: QwenTwoActionReadOnlyOutcome) -> None:
    """Emit bounded human-readable convenience output alongside durable reporting."""
    print(f"acceptance verdict: {_verdict(outcome)}")
    print(f"tool actions: {', '.join(outcome.report.execution_actions) or 'none'}")
    print(f"tool paths: {', '.join(outcome.report.execution_paths) or 'none'}")
    print(
        f"final answer: {outcome.report.result.final_message.content if outcome.report.result else 'unavailable'}",
    )
    print(f"target filename: {outcome.target_filename}")
    print(f"nonce: {outcome.nonce}")
    print(
        f"persistent service status: {outcome.persistent_service_status or outcome.persistent_service_error_message}",
    )


def main(arguments: Sequence[str] | None = None) -> None:
    """Run this repeatable Qwen-specific acceptance without service ownership."""
    parsed = parse_arguments(arguments)
    try:
        outcome = asyncio.run(run(parsed))
    except Exception as error:
        if parsed.report_path is not None:
            payload = {
                "schema": _REPORT_SCHEMA,
                "verdict": "FAIL — RUNNER",
                "runner_failure": {
                    "error_type": type(error).__name__,
                    "error_message": str(error),
                },
            }
            try:
                _write_report(parsed.report_path, payload)
            except Exception as write_error:  # noqa: BLE001 - stderr remains available.
                print(
                    f"could not write durable acceptance report: {write_error}",
                    file=sys.stderr,
                )
        raise SystemExit(1) from error
    try:
        if parsed.report_path is not None:
            _write_report(parsed.report_path, _report_payload(outcome))
    except Exception as error:
        print(f"could not write durable acceptance report: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    _print_outcome(outcome)
    raise SystemExit(0 if _verdict(outcome) == "PASS" else 1)


if __name__ == "__main__":
    main()
