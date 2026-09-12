# Copyright (c) 2026
# ruff: noqa: E402, E501, INP001, T201
"""Run and diagnose one bounded live two-read Qwen acceptance."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
import sys
import tempfile
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING
from uuid import uuid4

_REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(_REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPOSITORY_ROOT))

from devtools.commands import Command, CommandExecutor
from devtools.context import Message, MessageRole, MessageSource, Session
from devtools.interactions.providers import (
    LlamaCppInteraction,
    LlamaCppInteractionError,
)
from devtools.paths import ResolvedPath
from devtools.runtime import Runtime
from devtools.tools.filesystem import ReadRepositoryFileTool
from experiments.qwen.read_experiment import (
    QwenReadExperiment,
    QwenReadExperimentResult,
    ReadProposalError,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.interactions import Interaction


_DEFAULT_ENDPOINT = "http://127.0.0.1:8080"
_DEFAULT_MODEL = "qwen38-local"
_CALLER_SOURCE = MessageSource("qwen-two-read-acceptance")
_SERVICE_SCRIPT = Path(__file__).with_name("llama_cpp_service.py")
_REPORT_SCHEMA = "qwen-two-read-acceptance/1"
_REQUIRED_READS = 2


class QwenTwoReadFailureCategory(StrEnum):
    """Classify only failures from this bounded Qwen acceptance script."""

    MODEL_CONFORMANCE = "MODEL CONFORMANCE"
    PROVIDER = "PROVIDER"
    FRAMEWORK_BOUNDARY = "FRAMEWORK BOUNDARY"


class QwenTwoReadAcceptanceVerdict(StrEnum):
    """Describe this script's terminal acceptance result."""

    PASS = "PASS"  # noqa: S105 - fixed public acceptance verdict token.


@dataclass(frozen=True, slots=True)
class QwenTwoReadAcceptanceReport:
    """Retain bounded live-acceptance facts without defining framework tracing."""

    task: Message
    history: tuple[Message, ...]
    tool_execution_count: int
    tool_execution_paths: tuple[str, ...]
    result: QwenReadExperimentResult | None
    failure_category: QwenTwoReadFailureCategory | None
    error_type: str | None
    error_message: str | None
    latest_assistant: Message | None


@dataclass(frozen=True, slots=True)
class QwenTwoReadFixture:
    """Describe the inert temporary files used by this one acceptance."""

    root: Path
    first_nonce: str
    second_nonce: str


@dataclass(frozen=True, slots=True)
class QwenTwoReadAcceptanceOutcome:
    """Retain script-local facts needed to emit one completed acceptance artifact."""

    report: QwenTwoReadAcceptanceReport
    first_nonce: str
    second_nonce: str
    persistent_service_status: str | None
    persistent_service_error_type: str | None
    persistent_service_error_message: str | None
    fixture_cleanup_succeeded: bool


def parse_arguments(arguments: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse the fixed persistent-endpoint inputs for this acceptance."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--endpoint", default=_DEFAULT_ENDPOINT)
    parser.add_argument("--model", default=_DEFAULT_MODEL)
    parser.add_argument(
        "--report-path",
        type=Path,
        help=(
            "Write the completed JSON acceptance artifact to this caller-selected path. "
            "When supplied, this file is authoritative; stdout remains convenience output."
        ),
    )
    return parser.parse_args(arguments)


def initial_task() -> Message:
    """Construct the unchanged model-facing task used by the failed first run."""
    content = """Return the exact value from facts/first.txt, followed by a colon, followed by the exact value from facts/second.txt.

You do not have either file's contents. The only available action is read_repository_file. The known repository-relative paths are facts/first.txt and facts/second.txt. You may request up to two reads if necessary.

If you need a read, your entire response must be exactly one bare JSON object and nothing else in this form:
{"action":"read_repository_file","path":"<repository-relative-path>"}

Do not use Markdown or prose around a proposal. When you have enough information, provide the final answer as plain text."""
    return Message.new(content, role=MessageRole.USER, source=_CALLER_SOURCE)


def create_fixture(parent: Path) -> QwenTwoReadFixture:
    """Create one isolated two-nonce fixture below an explicit temporary parent."""
    first_nonce = f"NONCE-A-{uuid4()}"
    second_nonce = f"NONCE-B-{uuid4()}"
    root = parent / f"qwen-two-read-{uuid4()}"
    facts = root / "facts"
    facts.mkdir(parents=True)
    (facts / "first.txt").write_text(first_nonce, encoding="utf-8")
    (facts / "second.txt").write_text(second_nonce, encoding="utf-8")
    return QwenTwoReadFixture(root, first_nonce, second_nonce)


async def run_acceptance(
    *,
    task: Message,
    repository_root: Path,
    interaction: Interaction,
) -> QwenTwoReadAcceptanceReport:
    """Run the production experiment while retaining bounded failure diagnostics."""
    session = Session.new()
    experiment = QwenReadExperiment(
        runtime=Runtime(),
        session=session,
        interaction=interaction,
        repository_root=ResolvedPath(repository_root),
    )
    executions = 0
    execution_paths: list[str] = []
    original_execute = ReadRepositoryFileTool.execute

    async def counted_execute(
        tool: ReadRepositoryFileTool,
        arguments: ResolvedPath,
    ) -> object:
        nonlocal executions
        executions += 1
        execution_paths.append(str(arguments))
        return await original_execute(tool, arguments)

    ReadRepositoryFileTool.execute = counted_execute
    try:
        result = await experiment.run(task)
    except asyncio.CancelledError:
        raise
    except Exception as error:  # noqa: BLE001 - acceptance must retain any failure state.
        history = tuple(session.history)
        return QwenTwoReadAcceptanceReport(
            task=task,
            history=history,
            tool_execution_count=executions,
            tool_execution_paths=tuple(execution_paths),
            result=None,
            failure_category=_failure_category(error),
            error_type=type(error).__name__,
            error_message=str(error),
            latest_assistant=_latest_assistant(history, interaction.source),
        )
    finally:
        ReadRepositoryFileTool.execute = original_execute

    return QwenTwoReadAcceptanceReport(
        task=task,
        history=tuple(session.history),
        tool_execution_count=executions,
        tool_execution_paths=tuple(execution_paths),
        result=result,
        failure_category=None,
        error_type=None,
        error_message=None,
        latest_assistant=_latest_assistant(tuple(session.history), interaction.source),
    )


def _latest_assistant(
    history: tuple[Message, ...],
    interaction_source: MessageSource,
) -> Message | None:
    """Return the latest exact assistant Message retained by the selected interaction."""
    return next(
        (
            message
            for message in reversed(history)
            if message.role is MessageRole.ASSISTANT
            and message.source == interaction_source
        ),
        None,
    )


def _failure_category(error: Exception) -> QwenTwoReadFailureCategory:
    """Retain the existing acceptance categories without swallowing failures."""
    if isinstance(error, ReadProposalError):
        return QwenTwoReadFailureCategory.MODEL_CONFORMANCE
    if isinstance(error, LlamaCppInteractionError):
        return QwenTwoReadFailureCategory.PROVIDER
    return QwenTwoReadFailureCategory.FRAMEWORK_BOUNDARY


def _print_report(report: QwenTwoReadAcceptanceReport) -> None:
    """Print bounded safe acceptance facts, including failure-time Messages."""
    print(f"tool executions: {report.tool_execution_count}")
    print(f"tool execution paths: {', '.join(report.tool_execution_paths) or 'none'}")
    print(
        f"completed cycles: {len(report.result.cycles) if report.result else 'unavailable'}",
    )
    if report.failure_category is not None:
        print(f"failure category: {report.failure_category}")
        print(f"error type: {report.error_type}")
        print(f"error message: {report.error_message}")
    print("session history:")
    for message in report.history:
        print(f"{message.role.value}|{message.source.value}|{message.content}")
    if report.latest_assistant is not None:
        print("latest Qwen assistant content:")
        print(report.latest_assistant.content)


async def _persistent_status() -> str:
    """Observe the independently managed persistent Qwen service after acceptance."""
    result = await CommandExecutor().execute(_persistent_status_command())
    output = (result.stdout or result.stderr).decode(errors="replace").strip()
    return output or "persistent service status produced no output"


def _persistent_status_command() -> Command:
    """Build only the repository-owned observational persistent-service command."""
    return Command(sys.executable, (str(_SERVICE_SCRIPT), "status"))


def _verdict(outcome: QwenTwoReadAcceptanceOutcome) -> str:
    """Classify this fixed acceptance without changing experiment semantics."""
    report = outcome.report
    if report.failure_category is not None:
        return f"FAIL — {report.failure_category}"
    if outcome.persistent_service_error_type is not None:
        return "FAIL — FRAMEWORK BOUNDARY"
    if report.result is None:
        return "FAIL — FRAMEWORK BOUNDARY"
    required_paths = {"facts/first.txt", "facts/second.txt"}
    observed_paths = tuple(cycle.relative_path for cycle in report.result.cycles)
    if (
        report.tool_execution_count != _REQUIRED_READS
        or len(report.result.cycles) != _REQUIRED_READS
        or set(observed_paths) != required_paths
    ):
        return "FAIL — MODEL CONFORMANCE"
    expected_answer = f"{outcome.first_nonce}:{outcome.second_nonce}"
    if report.result.final_message.content != expected_answer:
        return "FAIL — MODEL CAPABILITY"
    return QwenTwoReadAcceptanceVerdict.PASS


def _message_payload(message: Message) -> dict[str, str]:
    """Serialize only the bounded Message facts needed by this acceptance artifact."""
    return {
        "role": message.role.value,
        "source": message.source.value,
        "content": message.content,
    }


def _report_payload(outcome: QwenTwoReadAcceptanceOutcome) -> dict[str, object]:
    """Construct this script's deterministic, safe, completed report representation."""
    report = outcome.report
    result = report.result
    cycles: list[dict[str, object]] = []
    if result is not None:
        cycles = [
            {
                "proposal": _message_payload(cycle.proposal),
                "relative_path": cycle.relative_path,
                "resolved_path": str(cycle.resolved_path),
                "result_projection": cycle.result_projection,
                "follow_up": _message_payload(cycle.follow_up),
            }
            for cycle in result.cycles
        ]
    return {
        "schema": _REPORT_SCHEMA,
        "verdict": _verdict(outcome),
        "fixture": {
            "first_nonce": outcome.first_nonce,
            "second_nonce": outcome.second_nonce,
            "cleanup": "completed"
            if outcome.fixture_cleanup_succeeded
            else "failed",
        },
        "task": _message_payload(report.task),
        "history": [_message_payload(message) for message in report.history],
        "latest_assistant": (
            _message_payload(report.latest_assistant)
            if report.latest_assistant is not None
            else None
        ),
        "tool_executions": {
            "count": report.tool_execution_count,
            "resolved_paths": list(report.tool_execution_paths),
        },
        "cycles": cycles,
        "final_answer": (
            result.final_message.content if result is not None else None
        ),
        "failure": {
            "category": (
                report.failure_category.value
                if report.failure_category is not None
                else None
            ),
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


def _print_outcome(outcome: QwenTwoReadAcceptanceOutcome) -> None:
    """Keep the established human-readable stdout report as a convenience sink."""
    _print_report(outcome.report)
    print(f"acceptance verdict: {_verdict(outcome)}")
    print("persistent service status:")
    if outcome.persistent_service_status is not None:
        print(outcome.persistent_service_status)
    else:
        print(
            "persistent service status failed: "
            f"{outcome.persistent_service_error_type}: "
            f"{outcome.persistent_service_error_message}",
        )
    print(f"first nonce: {outcome.first_nonce}")
    print(f"second nonce: {outcome.second_nonce}")


async def run(arguments: argparse.Namespace) -> QwenTwoReadAcceptanceOutcome:
    """Run one temporary-fixture acceptance against an independently managed endpoint."""
    with tempfile.TemporaryDirectory(prefix="devtools-qwen-two-read-") as directory:
        fixture = create_fixture(Path(directory))
        report: QwenTwoReadAcceptanceReport | None = None
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
                    source=MessageSource("qwen"),
                ),
            )
            try:
                status = await _persistent_status()
            except Exception as error:  # noqa: BLE001 - retain post-run observation failure.
                status_error = error
        finally:
            try:
                shutil.rmtree(fixture.root)
            except FileNotFoundError:
                pass
            else:
                cleanup_succeeded = True
        if report is None:
            msg = "Acceptance completed without producing a report."
            raise RuntimeError(msg)
        return QwenTwoReadAcceptanceOutcome(
            report=report,
            first_nonce=fixture.first_nonce,
            second_nonce=fixture.second_nonce,
            persistent_service_status=status,
            persistent_service_error_type=(
                type(status_error).__name__ if status_error is not None else None
            ),
            persistent_service_error_message=(
                str(status_error) if status_error is not None else None
            ),
            fixture_cleanup_succeeded=cleanup_succeeded,
        )


def main(arguments: Sequence[str] | None = None) -> None:
    """Run the repeatable Qwen-specific live acceptance without service ownership."""
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
            except Exception as write_error:  # noqa: BLE001 - stderr is the remaining sink.
                print(
                    f"could not write durable acceptance report: {write_error}",
                    file=sys.stderr,
                )
        raise SystemExit(1) from error
    if parsed.report_path is not None:
        try:
            _write_report(parsed.report_path, _report_payload(outcome))
        except Exception as error:
            print(
                f"could not write durable acceptance report: {error}",
                file=sys.stderr,
            )
            raise SystemExit(1) from error
    _print_outcome(outcome)
    raise SystemExit(
        0 if _verdict(outcome) is QwenTwoReadAcceptanceVerdict.PASS else 1,
    )


if __name__ == "__main__":
    main()
