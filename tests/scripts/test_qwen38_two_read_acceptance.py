# Copyright (c) 2026
# ruff: noqa: E501, INP001
"""Tests for bounded failure capture in the live two-read Qwen acceptance."""

from __future__ import annotations

import asyncio
import importlib.util
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from devtools.agents import AgentTurn, ConversationRef
from devtools.context import Message, MessageRole, MessageSource
from devtools.qwen.errors import QwenTransportError

if TYPE_CHECKING:
    from collections.abc import Iterator
    from types import ModuleType


_SCRIPT_DIRECTORY = Path("scripts/model_benchmarks").resolve()
_SCRIPT_PATH = _SCRIPT_DIRECTORY / "qwen38_two_read_acceptance.py"


@pytest.fixture
def acceptance() -> Iterator[ModuleType]:
    """Load the tracked acceptance script without making scripts a package."""
    specification = importlib.util.spec_from_file_location(
        "test_qwen38_two_read_acceptance",
        _SCRIPT_PATH,
    )
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    try:
        specification.loader.exec_module(module)
        yield module
    finally:
        sys.modules.pop(specification.name, None)


@dataclass(slots=True)
class _ScriptedAgent:
    """Return planned assistant text or a provider failure through Agent semantics."""

    responses: list[str]
    fail_on_call: int | None = None
    failure: Exception | None = None
    calls: list[Message] = field(default_factory=list)
    source: MessageSource = field(default_factory=lambda: MessageSource("qwen"))

    async def send(
        self,
        message: Message,
        *,
        conversation: ConversationRef | None = None,
    ) -> AgentTurn:
        """Retain each input and return the next exact assistant result."""
        assert conversation is None
        self.calls.append(message)
        if self.fail_on_call == len(self.calls):
            assert self.failure is not None
            raise self.failure
        return AgentTurn(
            Message.new(
                self.responses.pop(0),
                role=MessageRole.ASSISTANT,
                source=self.source,
            ),
        )


@dataclass(frozen=True, slots=True)
class _Fixture:
    """Provide static test typing for a dynamically loaded script fixture."""

    root: Path
    first_nonce: str
    second_nonce: str


def _fixture(acceptance: ModuleType, tmp_path: Path) -> _Fixture:
    created = acceptance.create_fixture(tmp_path)
    return _Fixture(created.root, created.first_nonce, created.second_nonce)


def test_first_malformed_proposal_retains_exact_assistant_and_session(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """First-turn parser failure retains the original Qwen content and zero reads."""
    fixture = _fixture(acceptance, tmp_path)
    agent = _ScriptedAgent(["{not json"])
    try:
        report = asyncio.run(
            acceptance.run_acceptance(
                task=acceptance.initial_task(),
                repository_root=fixture.root,
                agent=agent,
            ),
        )
    finally:
        shutil.rmtree(fixture.root)

    assert report.result is None
    assert report.failure_category is acceptance.QwenTwoReadFailureCategory.MODEL_CONFORMANCE
    assert report.error_type == "ReadProposalError"
    assert report.latest_assistant is not None
    assert report.latest_assistant.content == "{not json"
    assert report.tool_execution_count == 0
    assert [(message.role, message.source) for message in report.history] == [
        (MessageRole.USER, MessageSource("qwen-two-read-acceptance")),
        (MessageRole.ASSISTANT, MessageSource("qwen")),
    ]


def test_later_malformed_proposal_retains_history_and_completed_read(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """A failed second proposal retains its text, prior SYSTEM result, and one read."""
    fixture = _fixture(acceptance, tmp_path)
    agent = _ScriptedAgent(
        [
            '{"action":"read_repository_file","path":"facts/first.txt"}',
            '{"action":"unknown","path":"facts/second.txt"}',
        ],
    )
    try:
        report = asyncio.run(
            acceptance.run_acceptance(
                task=acceptance.initial_task(),
                repository_root=fixture.root,
                agent=agent,
            ),
        )
    finally:
        shutil.rmtree(fixture.root)

    assert report.result is None
    assert report.failure_category is acceptance.QwenTwoReadFailureCategory.MODEL_CONFORMANCE
    assert report.latest_assistant is not None
    assert report.latest_assistant.content.startswith('{"action":"unknown"')
    assert report.tool_execution_count == 1
    assert [message.role for message in report.history] == [
        MessageRole.USER,
        MessageRole.ASSISTANT,
        MessageRole.SYSTEM,
        MessageRole.ASSISTANT,
    ]


def test_provider_failure_does_not_invent_assistant_content(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """A provider failure before a result leaves no fabricated assistant Message."""
    fixture = _fixture(acceptance, tmp_path)
    agent = _ScriptedAgent([], fail_on_call=1, failure=QwenTransportError())
    try:
        report = asyncio.run(
            acceptance.run_acceptance(
                task=acceptance.initial_task(),
                repository_root=fixture.root,
                agent=agent,
            ),
        )
    finally:
        shutil.rmtree(fixture.root)

    assert report.result is None
    assert report.failure_category is acceptance.QwenTwoReadFailureCategory.PROVIDER
    assert report.latest_assistant is None
    assert report.tool_execution_count == 0
    assert [message.role for message in report.history] == [MessageRole.USER]


def test_temporary_fixture_is_removed_after_manual_cleanup(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """The isolated inert fixture can be removed without touching its parent."""
    fixture = _fixture(acceptance, tmp_path)
    assert (fixture.root / "facts" / "first.txt").read_text(encoding="utf-8") == fixture.first_nonce
    shutil.rmtree(fixture.root)
    assert not fixture.root.exists()
    assert tmp_path.exists()


def test_persistent_status_command_is_observational_and_repository_owned(
    acceptance: ModuleType,
) -> None:
    """The acceptance runner invokes only the tracked service status command."""
    command = acceptance._persistent_status_command()  # noqa: SLF001
    assert command.executable == acceptance.sys.executable
    assert command.arguments == (str(acceptance._SERVICE_SCRIPT), "status")  # noqa: SLF001
