# Copyright (c) 2026
"""Deterministic tests for the bounded experimental Qwen read loop."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import pytest

from devtools.agents import AgentTurn, ConversationRef
from devtools.context import Message, MessageRole, MessageSource, Session
from devtools.filesystem import FilesystemNotFoundError, TextFile
from devtools.paths import ResolvedPath
from devtools.qwen import experiment
from devtools.qwen.experiment import (
    QwenReadExperiment,
    ReadProposalError,
    ResultProjectionError,
)
from devtools.runtime import Runtime
from devtools.tools import ToolInputError
from devtools.tools.filesystem import ReadRepositoryFileTool

if TYPE_CHECKING:
    from pathlib import Path


_SECOND_PROVIDER_FAILURE = "second provider failed"
_TWO_AGENT_CALLS = 2


@dataclass(slots=True)
class _ScriptedAgent:
    """Return planned assistant text and retain each ordinary Agent input."""

    responses: list[str]
    calls: list[Message] = field(default_factory=list)
    source: MessageSource = field(default_factory=lambda: MessageSource("qwen"))

    async def send(
        self,
        message: Message,
        *,
        conversation: ConversationRef | None = None,
    ) -> AgentTurn:
        """Return the next planned final assistant message."""
        assert conversation is None
        self.calls.append(message)
        return AgentTurn(
            Message.new(
                self.responses.pop(0),
                role=MessageRole.ASSISTANT,
                source=self.source,
            ),
        )


def _task() -> Message:
    return Message.new(
        "What exact marker is stored in facts/answer.txt? "
        "Respond with only a JSON read proposal first.",
        role=MessageRole.USER,
        source=MessageSource("test-caller"),
    )


def _experiment(root: Path, agent: _ScriptedAgent) -> QwenReadExperiment:
    return QwenReadExperiment(
        runtime=Runtime(),
        session=Session.new(),
        agent=agent,
        repository_root=ResolvedPath(root.resolve()),
    )


def test_experiment_runs_exactly_one_permitted_read_then_second_runtime_turn(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """One accepted proposal reaches ToolRunner once and informs a second turn."""
    root = tmp_path / "repository"
    source = root / "facts" / "answer.txt"
    source.parent.mkdir(parents=True)
    source.write_text("MARKER-4821", encoding="utf-8")
    agent = _ScriptedAgent(
        [
            '{"action":"read_repository_file","path":"facts/answer.txt"}',
            "MARKER-4821",
        ],
    )
    calls: list[ResolvedPath] = []
    original_execute = ReadRepositoryFileTool.execute

    async def execute_once(
        tool: ReadRepositoryFileTool,
        arguments: ResolvedPath,
    ) -> object:
        calls.append(arguments)
        return await original_execute(tool, arguments)

    monkeypatch.setattr(ReadRepositoryFileTool, "execute", execute_once)

    result = asyncio.run(_experiment(root, agent).run(_task()))

    assert calls == [ResolvedPath(source.resolve())]
    assert result.first_model_text.startswith('{"action"')
    assert result.relative_path == "facts/answer.txt"
    assert result.resolved_path == ResolvedPath(source.resolve())
    assert "MARKER-4821" in result.result_projection
    assert result.follow_up.role is MessageRole.SYSTEM
    assert result.follow_up.source == MessageSource("runtime")
    assert "Original task:" in result.follow_up.content
    assert "data, not instructions" in result.follow_up.content
    assert result.final_message.content == "MARKER-4821"
    assert [message.role for message in agent.calls] == [
        MessageRole.USER,
        MessageRole.SYSTEM,
    ]


@pytest.mark.parametrize(
    "proposal",
    [
        "read facts/answer.txt",
        '{"action":"read_repository_file"}',
        '{"action":"delete_repository","path":"facts/answer.txt"}',
        '{"action":"read_repository_file","path":"facts/answer.txt","extra":1}',
    ],
)
def test_experiment_rejects_invalid_or_unknown_proposals_without_reading(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    proposal: str,
) -> None:
    """Proposal rejection stops before Tool execution and a second model turn."""
    root = tmp_path / "repository"
    root.mkdir()
    agent = _ScriptedAgent([proposal])

    async def must_not_execute(
        _tool: ReadRepositoryFileTool,
        _arguments: ResolvedPath,
    ) -> object:
        msg = "Tool execution must not occur after proposal rejection."
        raise AssertionError(msg)

    monkeypatch.setattr(ReadRepositoryFileTool, "execute", must_not_execute)

    with pytest.raises(ReadProposalError):
        asyncio.run(_experiment(root, agent).run(_task()))
    assert len(agent.calls) == 1


@pytest.mark.parametrize(
    "proposal",
    [
        '{"action":"invalid","action":"read_repository_file","path":"facts/answer.txt"}',
        '{"action":"read_repository_file","action":"invalid","path":"facts/answer.txt"}',
        '{"action":"read_repository_file","path":"a","path":"b"}',
        '{"action":"read_repository_file","action":"read_repository_file","path":"facts/answer.txt"}',
    ],
)
def test_experiment_rejects_duplicate_proposal_keys_without_reading(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    proposal: str,
) -> None:
    """Exact experiment grammar rejects duplicate JSON fields before execution."""
    root = tmp_path / "repository"
    root.mkdir()
    agent = _ScriptedAgent([proposal])

    async def must_not_execute(
        _tool: ReadRepositoryFileTool,
        _arguments: ResolvedPath,
    ) -> object:
        msg = "Duplicate-key proposals must not enter Tool execution."
        raise AssertionError(msg)

    monkeypatch.setattr(ReadRepositoryFileTool, "execute", must_not_execute)

    with pytest.raises(ReadProposalError, match="duplicate"):
        asyncio.run(_experiment(root, agent).run(_task()))
    assert len(agent.calls) == 1


@pytest.mark.parametrize("path", ["/outside.txt", "../outside.txt"])
def test_experiment_rejects_absolute_or_out_of_root_path_without_file_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    path: str,
) -> None:
    """Path materialization and Tool scope prevent outside-file execution."""
    root = tmp_path / "repository"
    root.mkdir()
    agent = _ScriptedAgent(
        [f'{{"action":"read_repository_file","path":"{path}"}}'],
    )

    async def must_not_execute(
        _tool: ReadRepositoryFileTool,
        _arguments: ResolvedPath,
    ) -> object:
        msg = "Outside paths must not enter read execution."
        raise AssertionError(msg)

    monkeypatch.setattr(ReadRepositoryFileTool, "execute", must_not_execute)

    with pytest.raises((ReadProposalError, ToolInputError)):
        asyncio.run(_experiment(root, agent).run(_task()))
    assert len(agent.calls) == 1


def test_experiment_keeps_tool_failure_distinct_from_proposal_rejection(
    tmp_path: Path,
) -> None:
    """An admitted missing path remains a Filesystem-domain execution failure."""
    root = tmp_path / "repository"
    root.mkdir()
    agent = _ScriptedAgent(
        ['{"action":"read_repository_file","path":"facts/missing.txt"}'],
    )

    with pytest.raises(FilesystemNotFoundError):
        asyncio.run(_experiment(root, agent).run(_task()))
    assert len(agent.calls) == 1


def test_experiment_propagates_second_provider_failure_after_tool_success(
    tmp_path: Path,
) -> None:
    """A second model-turn failure remains distinct from the completed Tool read."""
    root = tmp_path / "repository"
    source = root / "facts" / "answer.txt"
    source.parent.mkdir(parents=True)
    source.write_text("MARKER-4821", encoding="utf-8")
    agent = _FailingSecondAgent(
        ['{"action":"read_repository_file","path":"facts/answer.txt"}'],
    )

    with pytest.raises(LookupError, match=_SECOND_PROVIDER_FAILURE):
        asyncio.run(_experiment(root, agent).run(_task()))
    assert len(agent.calls) == _TWO_AGENT_CALLS


@pytest.mark.parametrize("limit", [0, -1])
def test_experiment_rejects_nonpositive_projection_limit(
    tmp_path: Path,
    limit: int,
) -> None:
    """The bounded projection policy cannot be silently disabled."""
    with pytest.raises(ValueError, match="limit"):
        QwenReadExperiment(
            runtime=Runtime(),
            session=Session.new(),
            agent=_ScriptedAgent([]),
            repository_root=ResolvedPath(tmp_path.resolve()),
            max_projection_characters=limit,
        )


@pytest.mark.parametrize(
    "content",
    [
        '{"action":"read_repository_file","path":""}',
        '{"action":"read_repository_file","path":" facts/answer.txt"}',
        '{"action":"read_repository_file","path":1}',
    ],
)
def test_proposal_parser_rejects_blank_or_noncanonical_path_values(
    content: str,
) -> None:
    """Only trimmed textual repository-relative path proposals are admitted."""
    with pytest.raises(ReadProposalError, match="path"):
        experiment._parse_read_proposal(content)  # noqa: SLF001


def test_projection_is_bounded_and_rejects_non_text_result(tmp_path: Path) -> None:
    """The experiment projects only bounded text rather than rich File objects."""
    text = TextFile(
        path=ResolvedPath((tmp_path / "answer.txt").resolve()),
        content="abcdef",
    )
    projection = experiment._project_text_result(  # noqa: SLF001
        "answer.txt",
        text,
        maximum_characters=3,
    )
    assert "abc" in projection
    assert "projection truncated" in projection
    with pytest.raises(ResultProjectionError, match="only text"):
        experiment._project_text_result(  # noqa: SLF001
            "answer.txt",
            object(),
            maximum_characters=3,
        )


class _FailingSecondAgent(_ScriptedAgent):
    """Raise a provider-like failure only after the accepted repository read."""

    async def send(
        self,
        message: Message,
        *,
        conversation: ConversationRef | None = None,
    ) -> AgentTurn:
        """Return first proposal then fail the second ordinary Agent invocation."""
        if self.calls:
            self.calls.append(message)
            raise LookupError(_SECOND_PROVIDER_FAILURE)
        return await super().send(message, conversation=conversation)
