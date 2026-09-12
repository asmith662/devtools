# Copyright (c) 2026
# ruff: noqa: E501, INP001, T201
"""Run and diagnose one bounded live two-read Qwen acceptance."""

from __future__ import annotations

import argparse
import asyncio
import shutil
import sys
import tempfile
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING
from uuid import uuid4

from devtools.commands import Command, CommandExecutor
from devtools.context import Message, MessageRole, MessageSource, Session
from devtools.paths import ResolvedPath
from devtools.qwen import QwenAgent, QwenError
from devtools.qwen.experiment import (
    QwenReadExperiment,
    QwenReadExperimentResult,
    ReadProposalError,
)
from devtools.runtime import Runtime
from devtools.tools.filesystem import ReadRepositoryFileTool

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.agents import Agent


_DEFAULT_ENDPOINT = "http://127.0.0.1:8080"
_DEFAULT_MODEL = "qwen38-local"
_CALLER_SOURCE = MessageSource("qwen-two-read-acceptance")
_SERVICE_SCRIPT = Path(__file__).with_name("qwen38_llama_cpp_service.py")


class QwenTwoReadFailureCategory(StrEnum):
    """Classify only failures from this bounded Qwen acceptance script."""

    MODEL_CONFORMANCE = "MODEL CONFORMANCE"
    PROVIDER = "PROVIDER"
    FRAMEWORK_BOUNDARY = "FRAMEWORK BOUNDARY"


@dataclass(frozen=True, slots=True)
class QwenTwoReadAcceptanceReport:
    """Retain bounded live-acceptance facts without defining framework tracing."""

    task: Message
    history: tuple[Message, ...]
    tool_execution_count: int
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


def parse_arguments(arguments: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse the fixed persistent-endpoint inputs for this acceptance."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--endpoint", default=_DEFAULT_ENDPOINT)
    parser.add_argument("--model", default=_DEFAULT_MODEL)
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
    agent: Agent,
) -> QwenTwoReadAcceptanceReport:
    """Run the production experiment while retaining bounded failure diagnostics."""
    session = Session.new()
    experiment = QwenReadExperiment(
        runtime=Runtime(),
        session=session,
        agent=agent,
        repository_root=ResolvedPath(repository_root),
    )
    executions = 0
    original_execute = ReadRepositoryFileTool.execute

    async def counted_execute(
        tool: ReadRepositoryFileTool,
        arguments: ResolvedPath,
    ) -> object:
        nonlocal executions
        executions += 1
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
            result=None,
            failure_category=_failure_category(error),
            error_type=type(error).__name__,
            error_message=str(error),
            latest_assistant=_latest_assistant(history, agent.source),
        )
    finally:
        ReadRepositoryFileTool.execute = original_execute

    return QwenTwoReadAcceptanceReport(
        task=task,
        history=tuple(session.history),
        tool_execution_count=executions,
        result=result,
        failure_category=None,
        error_type=None,
        error_message=None,
        latest_assistant=_latest_assistant(tuple(session.history), agent.source),
    )


def _latest_assistant(
    history: tuple[Message, ...],
    agent_source: MessageSource,
) -> Message | None:
    """Return the latest exact assistant Message retained by the selected agent."""
    return next(
        (
            message
            for message in reversed(history)
            if message.role is MessageRole.ASSISTANT and message.source == agent_source
        ),
        None,
    )


def _failure_category(error: Exception) -> QwenTwoReadFailureCategory:
    """Retain the existing acceptance categories without swallowing failures."""
    if isinstance(error, ReadProposalError):
        return QwenTwoReadFailureCategory.MODEL_CONFORMANCE
    if isinstance(error, QwenError):
        return QwenTwoReadFailureCategory.PROVIDER
    return QwenTwoReadFailureCategory.FRAMEWORK_BOUNDARY


def _print_report(report: QwenTwoReadAcceptanceReport) -> None:
    """Print bounded safe acceptance facts, including failure-time Messages."""
    print(f"tool executions: {report.tool_execution_count}")
    print(f"completed cycles: {len(report.result.cycles) if report.result else 'unavailable'}")
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


async def run(arguments: argparse.Namespace) -> QwenTwoReadAcceptanceReport:
    """Run one temporary-fixture acceptance against an independently managed endpoint."""
    with tempfile.TemporaryDirectory(prefix="devtools-qwen-two-read-") as directory:
        fixture = create_fixture(Path(directory))
        try:
            report = await run_acceptance(
                task=initial_task(),
                repository_root=fixture.root,
                agent=QwenAgent(endpoint=arguments.endpoint, model=arguments.model),
            )
            _print_report(report)
            print("persistent service status:")
            print(await _persistent_status())
            print(f"first nonce: {fixture.first_nonce}")
            print(f"second nonce: {fixture.second_nonce}")
            return report
        finally:
            shutil.rmtree(fixture.root, ignore_errors=True)


def main(arguments: Sequence[str] | None = None) -> None:
    """Run the repeatable Qwen-specific live acceptance without service ownership."""
    asyncio.run(run(parse_arguments(arguments)))


if __name__ == "__main__":
    main()
