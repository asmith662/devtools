# Copyright (c) 2026
"""Tests for the CLI-backed Codex agent."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest

import devtools.interactions.providers.codex
from devtools.commands import (
    Command,
    CommandExecutor,
    CommandNotFoundError,
    CommandResult,
)
from devtools.context.message import Message, MessageRole, MessageSource
from devtools.interactions import ConversationRef, Interaction
from devtools.interactions.providers.codex import (
    CodexAgent,
    CodexCommandError,
    CodexError,
    CodexOutputError,
)
from devtools.interactions.providers.codex.agent import _resolve_executable
from devtools.paths import ResolvedPath
from devtools.time import Duration

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path


_SUCCESS = (
    b'{"type":"thread.started","thread_id":"thread-42"}\n'
    b'{"type":"item.completed","item":{"type":"agent_message",'
    b'"text":"Codex reply"}}\n'
    b'{"type":"turn.completed"}\n'
)
_CODEX_AGENT_PLATFORM = "devtools.interactions.providers.codex.agent.sys.platform"
_CODEX_AGENT_WHICH = "devtools.interactions.providers.codex.agent.shutil.which"


class RecordingExecutor(CommandExecutor):
    """CommandExecutor fake retaining direct-argv invocations."""

    def __init__(self, results: Sequence[tuple[int, bytes, bool]]) -> None:
        """Initialize the queued result specifications."""
        super().__init__()
        self.commands: list[Command] = []
        self._results = list(results)

    async def execute(self, command: Command) -> CommandResult:
        """Return the next captured deterministic command result."""
        self.commands.append(command)
        exit_code, stdout, stdout_truncated = self._results.pop(0)
        return CommandResult(
            command=command,
            exit_code=exit_code,
            stdout=stdout,
            stderr=b"diagnostic output is intentionally ignored",
            duration=Duration.seconds(0),
            stdout_truncated=stdout_truncated,
        )


class MissingExecutor(CommandExecutor):
    """CommandExecutor fake preserving the command-domain missing binary error."""

    async def execute(self, _command: Command) -> CommandResult:
        """Raise the same error emitted by a missing executable at execution."""
        raise CommandNotFoundError


def _user_message(content: str = "A prompt with\nmultiple lines.") -> Message:
    """Create a normal inbound user message."""
    return Message.new(
        content,
        role=MessageRole.USER,
        source=MessageSource("caller"),
    )


def _agent(
    executor: RecordingExecutor,
    tmp_path: Path,
    *,
    executable: str = "test-codex",
) -> CodexAgent:
    """Construct the adapter with an explicit temporary working directory."""
    return CodexAgent(executor, ResolvedPath(tmp_path), executable=executable)


def test_agent_builds_fresh_read_only_jsonl_command_and_maps_turn(
    tmp_path: Path,
) -> None:
    """Fresh sends use direct argv and map Codex output to the generic turn."""
    executor = RecordingExecutor([(0, _SUCCESS, False)])
    interaction: Interaction = _agent(executor, tmp_path)
    turn = asyncio.run(interaction.send(_user_message()))

    assert interaction.source == MessageSource("codex")
    assert turn.message.content == "Codex reply"
    assert turn.message.role == MessageRole.ASSISTANT
    assert turn.message.source == interaction.source
    assert turn.conversation == ConversationRef(interaction.source, "thread-42")
    assert executor.commands[0].argv == (
        "test-codex",
        "exec",
        "--sandbox",
        "read-only",
        "--cd",
        str(tmp_path),
        "--json",
        "A prompt with\nmultiple lines.",
    )
    assert executor.commands[0].working_directory == ResolvedPath(tmp_path)


def test_agent_builds_resume_command_with_provider_thread_id(tmp_path: Path) -> None:
    """Continued turns use the installed ``exec resume`` grammar."""
    executor = RecordingExecutor([(0, _SUCCESS, False)])
    agent = _agent(executor, tmp_path)
    conversation = ConversationRef(agent.source, "thread-42")

    asyncio.run(agent.send(_user_message("Follow up"), conversation=conversation))

    assert executor.commands[0].argv == (
        "test-codex",
        "exec",
        "resume",
        "-c",
        'sandbox_mode="read-only"',
        "--json",
        "thread-42",
        "Follow up",
    )
    assert executor.commands[0].working_directory == ResolvedPath(tmp_path)


@pytest.mark.parametrize("role", [MessageRole.ASSISTANT, MessageRole.SYSTEM])
def test_agent_rejects_non_user_message_without_executing(
    tmp_path: Path,
    role: MessageRole,
) -> None:
    """Codex turns are intentionally restricted to user-role input."""
    executor = RecordingExecutor([])
    agent = _agent(executor, tmp_path)
    message = Message.new(
        "not a prompt",
        role=role,
        source=MessageSource("caller"),
    )

    with pytest.raises(ValueError, match="only user"):
        asyncio.run(agent.send(message))
    assert executor.commands == []


def test_agent_rejects_foreign_conversation_without_executing(tmp_path: Path) -> None:
    """Provider-owned continuation references cannot cross agent sources."""
    executor = RecordingExecutor([])
    agent = _agent(executor, tmp_path)

    with pytest.raises(ValueError, match="owned by the codex"):
        asyncio.run(
            agent.send(
                _user_message(),
                conversation=ConversationRef(MessageSource("qwen"), "foreign"),
            ),
        )
    assert executor.commands == []


@pytest.mark.parametrize(
    ("result", "error"),
    [
        ((5, b"provider diagnostic", False), CodexCommandError),
        ((0, _SUCCESS, True), CodexOutputError),
        ((0, b'{"type":"turn.completed"}\n', False), CodexOutputError),
    ],
)
def test_agent_rejects_unsuccessful_truncated_or_invalid_results(
    tmp_path: Path,
    result: tuple[int, bytes, bool],
    error: type[Exception],
) -> None:
    """Only an untruncated successful command can become an InteractionTurn."""
    executor = RecordingExecutor([result])
    agent = _agent(executor, tmp_path)

    with pytest.raises(error):
        asyncio.run(agent.send(_user_message()))


def test_default_windows_executable_prefers_the_direct_cmd_launcher(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The default avoids npm's PowerShell-only launcher on Windows."""
    launcher = r"C:\\npm\\codex.cmd"
    monkeypatch.setattr(_CODEX_AGENT_PLATFORM, "win32")
    monkeypatch.setattr(_CODEX_AGENT_WHICH, lambda _: launcher)

    assert _resolve_executable("codex") == launcher


def test_default_windows_executable_falls_back_to_command_domain_lookup(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Absent launchers preserve ordinary command-not-found behavior on send."""
    monkeypatch.setattr(_CODEX_AGENT_PLATFORM, "win32")
    monkeypatch.setattr(_CODEX_AGENT_WHICH, lambda _: None)

    assert _resolve_executable("codex") == "codex"


def test_explicit_executable_is_preserved_and_non_windows_keeps_codex(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Only the implicit Windows default receives Codex-specific resolution."""
    monkeypatch.setattr(_CODEX_AGENT_PLATFORM, "win32")
    monkeypatch.setattr(_CODEX_AGENT_WHICH, lambda _: "ignored")

    assert _resolve_executable(r"C:\\custom\\codex.exe") == r"C:\\custom\\codex.exe"

    monkeypatch.setattr(_CODEX_AGENT_PLATFORM, "linux")
    assert _resolve_executable("codex") == "codex"


def test_root_public_api_is_exact() -> None:
    """Only supported adapter and error boundaries are root-exported."""
    assert devtools.interactions.providers.codex.__all__ == [
        "CodexAgent",
        "CodexCommandError",
        "CodexError",
        "CodexOutputError",
    ]
    assert CodexError is devtools.interactions.providers.codex.CodexError


def test_agent_preserves_an_empty_prompt_as_one_argument(tmp_path: Path) -> None:
    """Direct argv transport does not discard a valid empty Message content."""
    executor = RecordingExecutor([(0, _SUCCESS, False)])
    agent = _agent(executor, tmp_path)

    asyncio.run(agent.send(_user_message("")))

    assert executor.commands[0].argv[-1] == ""


def test_default_resolution_failure_preserves_command_domain_error(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """An unavailable default launcher is reported by CommandExecutor on send."""
    monkeypatch.setattr(_CODEX_AGENT_PLATFORM, "win32")
    monkeypatch.setattr(_CODEX_AGENT_WHICH, lambda _: None)
    agent = CodexAgent(MissingExecutor(), ResolvedPath(tmp_path))

    with pytest.raises(CommandNotFoundError):
        asyncio.run(agent.send(_user_message()))
