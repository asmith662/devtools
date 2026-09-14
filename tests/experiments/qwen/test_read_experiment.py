# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, PLR2004, TRY003
"""Deterministic tests for the bounded repeated-read Qwen experiment."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import pytest

from devtools.agents.conversation import (
    Conversation,
    ConversationMessage,
    ConversationMessageRole,
    InteractionSource,
)
from devtools.core.paths import ResolvedPath
from devtools.execution import Runtime
from devtools.models.interaction import ConversationRef, ModelResponse, Prompt
from devtools.resources.filesystem import FilesystemNotFoundError, TextFile
from devtools.tools import ToolInputError
from devtools.tools.filesystem import ReadRepositoryFileTool
from experiments.qwen import read_experiment as experiment
from experiments.qwen.read_experiment import (
    QwenReadExperiment,
    ReadProposalError,
    ResultProjectionError,
)

if TYPE_CHECKING:
    from pathlib import Path


_PROVIDER_FAILURE = "provider failed"


@dataclass(slots=True)
class _ScriptedInteraction:
    """Return planned assistant text and retain each ordinary ModelInteraction input."""

    responses: list[str]
    calls: list[Prompt] = field(default_factory=list)
    source: InteractionSource = field(default_factory=lambda: InteractionSource("qwen"))

    async def send(
        self,
        prompt: Prompt,
        *,
        conversation: ConversationRef | None = None,
        maximum_output_tokens: int | None = None,
    ) -> ModelResponse:
        """Return the next planned final assistant message."""
        assert conversation is None
        del maximum_output_tokens
        self.calls.append(prompt)
        return ModelResponse(content=self.responses.pop(0), source=self.source)


@dataclass(slots=True)
class _FailingInteraction(_ScriptedInteraction):
    """Raise a provider-like failure on the selected invocation."""

    fail_on_call: int = 0

    async def send(
        self,
        prompt: Prompt,
        *,
        conversation: ConversationRef | None = None,
        maximum_output_tokens: int | None = None,
    ) -> ModelResponse:
        """Retain the attempted input before the configured provider failure."""
        if len(self.calls) + 1 == self.fail_on_call:
            self.calls.append(prompt)
            raise LookupError(_PROVIDER_FAILURE)
        return await super().send(
            prompt,
            conversation=conversation,
            maximum_output_tokens=maximum_output_tokens,
        )


def _proposal(path: str) -> str:
    return f'{{"action":"read_repository_file","path":"{path}"}}'


def _task() -> ConversationMessage:
    return ConversationMessage.new(
        "Return the requested facts using the permitted exact read proposal.",
        role=ConversationMessageRole.USER,
        source=InteractionSource("test-caller"),
    )


def _experiment(
    root: Path, interaction: _ScriptedInteraction
) -> tuple[QwenReadExperiment, Conversation]:
    session = Conversation.new()
    return (
        QwenReadExperiment(
            runtime=Runtime(),
            conversation=session,
            interaction=interaction,
            repository_root=ResolvedPath(root.resolve()),
        ),
        session,
    )


def _write(root: Path, relative_path: str, content: str) -> Path:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def test_two_valid_reads_retain_ordered_cycles_prompts_and_session(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Two same-action cycles compose through three ordinary Runtime turns."""
    root = tmp_path / "repository"
    first = _write(root, "facts/first.txt", "NONCE-A")
    second = _write(root, "facts/second.txt", "NONCE-B")
    interaction = _ScriptedInteraction(
        [_proposal("facts/first.txt"), _proposal("facts/second.txt"), "A:B"]
    )
    calls: list[ResolvedPath] = []
    original_execute = ReadRepositoryFileTool.execute

    async def execute_once(
        tool: ReadRepositoryFileTool, arguments: ResolvedPath
    ) -> object:
        calls.append(arguments)
        return await original_execute(tool, arguments)

    monkeypatch.setattr(ReadRepositoryFileTool, "execute", execute_once)
    tested, session = _experiment(root, interaction)
    result = asyncio.run(tested.run(_task()))

    assert calls == [ResolvedPath(first.resolve()), ResolvedPath(second.resolve())]
    assert [cycle.relative_path for cycle in result.cycles] == [
        "facts/first.txt",
        "facts/second.txt",
    ]
    assert result.cycles[0].proposal.content == _proposal("facts/first.txt")
    assert "NONCE-A" in result.cycles[0].result_projection
    assert '"action":"read_repository_file","path":"<repository-relative-path>"}' in (
        result.cycles[0].follow_up.content
    )
    assert "final plain-text answer" in result.cycles[0].follow_up.content
    assert "NONCE-A" in result.cycles[1].follow_up.content
    assert "NONCE-B" in result.cycles[1].follow_up.content
    assert "Do not propose another action." in result.cycles[1].follow_up.content
    assert result.final_message.content == "A:B"
    assert [message.role for message in interaction.calls] == [
        ConversationMessageRole.USER,
        ConversationMessageRole.SYSTEM,
        ConversationMessageRole.SYSTEM,
    ]
    assert [message.role for message in session.history] == [
        ConversationMessageRole.USER,
        ConversationMessageRole.ASSISTANT,
        ConversationMessageRole.SYSTEM,
        ConversationMessageRole.ASSISTANT,
        ConversationMessageRole.SYSTEM,
        ConversationMessageRole.ASSISTANT,
    ]


def test_early_final_answer_after_one_read_terminates_normally(tmp_path: Path) -> None:
    """Two is a cap, not a requirement for the experiment controller."""
    root = tmp_path / "repository"
    _write(root, "facts/first.txt", "NONCE-A")
    interaction = _ScriptedInteraction(
        [_proposal("facts/first.txt"), "final after one read"]
    )
    tested, _ = _experiment(root, interaction)

    result = asyncio.run(tested.run(_task()))

    assert len(result.cycles) == 1
    assert result.final_message.content == "final after one read"
    assert len(interaction.calls) == 2


def test_initial_plain_text_is_an_early_final_answer(tmp_path: Path) -> None:
    """The controller accepts ordinary final text without forcing a first read."""
    root = tmp_path / "repository"
    root.mkdir()
    interaction = _ScriptedInteraction(["final answer without a read"])
    tested, _ = _experiment(root, interaction)

    result = asyncio.run(tested.run(_task()))

    assert result.cycles == ()
    assert result.final_message.content == "final answer without a read"
    assert len(interaction.calls) == 1


def test_third_valid_proposal_is_rejected_without_a_third_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The local experiment cap prevents a third action execution or fourth turn."""
    root = tmp_path / "repository"
    _write(root, "facts/first.txt", "A")
    _write(root, "facts/second.txt", "B")
    _write(root, "facts/third.txt", "C")
    interaction = _ScriptedInteraction(
        [
            _proposal("facts/first.txt"),
            _proposal("facts/second.txt"),
            _proposal("facts/third.txt"),
        ],
    )
    tested, _ = _experiment(root, interaction)
    calls: list[ResolvedPath] = []
    original_execute = ReadRepositoryFileTool.execute

    async def execute_once(
        tool: ReadRepositoryFileTool, arguments: ResolvedPath
    ) -> object:
        calls.append(arguments)
        return await original_execute(tool, arguments)

    monkeypatch.setattr(ReadRepositoryFileTool, "execute", execute_once)

    with pytest.raises(ReadProposalError, match="at most two"):
        asyncio.run(tested.run(_task()))
    assert calls == [
        ResolvedPath((root / "facts/first.txt").resolve()),
        ResolvedPath((root / "facts/second.txt").resolve()),
    ]
    assert len(interaction.calls) == 3


def test_repeated_path_is_permitted_and_consumes_both_read_slots(
    tmp_path: Path,
) -> None:
    """The experiment does not turn path uniqueness into authority semantics."""
    root = tmp_path / "repository"
    _write(root, "facts/first.txt", "A")
    interaction = _ScriptedInteraction(
        [_proposal("facts/first.txt"), _proposal("facts/first.txt"), "final"]
    )
    tested, _ = _experiment(root, interaction)

    result = asyncio.run(tested.run(_task()))

    assert [cycle.relative_path for cycle in result.cycles] == [
        "facts/first.txt",
        "facts/first.txt",
    ]
    assert result.final_message.content == "final"


@pytest.mark.parametrize(
    "proposal",
    [
        '{"action":"read_repository_file"}',
        '{"action":"delete_repository","path":"facts/answer.txt"}',
        '{"action":"read_repository_file","path":"facts/answer.txt","extra":1}',
        '```json\n{"action":"read_repository_file","path":"facts/answer.txt"}\n```',
    ],
)
def test_action_like_invalid_response_is_rejected_without_reading(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    proposal: str,
) -> None:
    """Action-shaped output never degrades into a final answer or Tool execution."""
    root = tmp_path / "repository"
    root.mkdir()
    interaction = _ScriptedInteraction([proposal])
    tested, _ = _experiment(root, interaction)

    async def must_not_execute(
        _tool: ReadRepositoryFileTool, _arguments: ResolvedPath
    ) -> object:
        raise AssertionError("Invalid proposal must not reach Tool execution.")

    monkeypatch.setattr(ReadRepositoryFileTool, "execute", must_not_execute)
    with pytest.raises(ReadProposalError):
        asyncio.run(tested.run(_task()))
    assert len(interaction.calls) == 1


@pytest.mark.parametrize(
    ("content", "expected_path"),
    [
        ("42", None),
        ("The answer is 42.", None),
        ("read facts/a.txt", None),
        ("Read facts/a.txt", None),
        ("read the answer carefully: 42", None),
        ("Read this as the final answer: 42", None),
        ("read_repository_file was not needed", None),
        ("The action completed. The answer is 42.", None),
        ("I did not need read_repository_file. The answer is 42.", None),
        ('The word "action" appears in the file.', None),
        ("Here is the final answer: read_repository_file", None),
        (
            'I think the action should be {"action":"read_repository_file","path":"facts/a.txt"}',
            None,
        ),
        ('{"action":"read_repository_file","path":"facts/a.txt"}', "facts/a.txt"),
    ],
)
def test_response_classifier_accepts_plain_text_or_exact_proposal(
    content: str, expected_path: str | None
) -> None:
    """Only protocol-shaped prefixes enter exact proposal validation."""
    assert experiment._classify_response(content) == expected_path  # noqa: SLF001


@pytest.mark.parametrize(
    "content",
    [
        '```json\n{"action":"read_repository_file","path":"facts/a.txt"}\n```',
        "{not json",
        '{"foo":"bar"}',
    ],
)
def test_response_classifier_rejects_invalid_protocol_shaped_text(content: str) -> None:
    """Malformed object and fenced forms cannot silently become final answers."""
    with pytest.raises(ReadProposalError):
        experiment._classify_response(content)  # noqa: SLF001


@pytest.mark.parametrize(
    "proposal",
    [
        '{"action":"invalid","action":"read_repository_file","path":"facts/answer.txt"}',
        '{"action":"read_repository_file","action":"invalid","path":"facts/answer.txt"}',
        '{"action":"read_repository_file","path":"a","path":"b"}',
        '{"action":"read_repository_file","action":"read_repository_file","path":"facts/answer.txt"}',
    ],
)
def test_duplicate_proposal_keys_are_rejected_without_reading(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    proposal: str,
) -> None:
    """Exact proposal grammar rejects duplicate JSON fields before execution."""
    root = tmp_path / "repository"
    root.mkdir()
    interaction = _ScriptedInteraction([proposal])
    tested, _ = _experiment(root, interaction)

    async def must_not_execute(
        _tool: ReadRepositoryFileTool, _arguments: ResolvedPath
    ) -> object:
        raise AssertionError("Duplicate-key proposals must not enter Tool execution.")

    monkeypatch.setattr(ReadRepositoryFileTool, "execute", must_not_execute)
    with pytest.raises(ReadProposalError, match="duplicate"):
        asyncio.run(tested.run(_task()))
    assert len(interaction.calls) == 1


@pytest.mark.parametrize("path", ["/outside.txt", "../outside.txt"])
def test_outside_path_is_rejected_without_file_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    path: str,
) -> None:
    """Existing path materialization and Tool scope still prevent outside reads."""
    root = tmp_path / "repository"
    root.mkdir()
    interaction = _ScriptedInteraction([_proposal(path)])
    tested, _ = _experiment(root, interaction)

    async def must_not_execute(
        _tool: ReadRepositoryFileTool, _arguments: ResolvedPath
    ) -> object:
        raise AssertionError("Outside paths must not enter read execution.")

    monkeypatch.setattr(ReadRepositoryFileTool, "execute", must_not_execute)
    with pytest.raises((ReadProposalError, ToolInputError)):
        asyncio.run(tested.run(_task()))
    assert len(interaction.calls) == 1


def test_invalid_second_proposal_stops_after_first_cycle(tmp_path: Path) -> None:
    """A malformed later action-like response does not execute or continue."""
    root = tmp_path / "repository"
    _write(root, "facts/first.txt", "A")
    interaction = _ScriptedInteraction(
        [_proposal("facts/first.txt"), '{"action":"unknown","path":"facts/second.txt"}']
    )
    tested, _ = _experiment(root, interaction)

    with pytest.raises(ReadProposalError):
        asyncio.run(tested.run(_task()))
    assert len(interaction.calls) == 2


def test_second_tool_failure_preserves_first_cycle_and_stops(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A second read failure does not create another provider turn."""
    root = tmp_path / "repository"
    _write(root, "facts/first.txt", "A")
    _write(root, "facts/second.txt", "B")
    interaction = _ScriptedInteraction(
        [_proposal("facts/first.txt"), _proposal("facts/second.txt")]
    )
    tested, _ = _experiment(root, interaction)
    original_execute = ReadRepositoryFileTool.execute
    executions = 0

    async def fail_second(
        tool: ReadRepositoryFileTool, arguments: ResolvedPath
    ) -> object:
        nonlocal executions
        executions += 1
        if executions == 2:
            raise FilesystemNotFoundError(arguments)
        return await original_execute(tool, arguments)

    monkeypatch.setattr(ReadRepositoryFileTool, "execute", fail_second)
    with pytest.raises(FilesystemNotFoundError):
        asyncio.run(tested.run(_task()))
    assert executions == 2
    assert len(interaction.calls) == 2


def test_later_provider_failure_follows_completed_read_cycle(tmp_path: Path) -> None:
    """Provider failure remains distinct from the successful preceding read."""
    root = tmp_path / "repository"
    _write(root, "facts/first.txt", "A")
    interaction = _FailingInteraction([_proposal("facts/first.txt")], fail_on_call=2)
    tested, _ = _experiment(root, interaction)

    with pytest.raises(LookupError, match=_PROVIDER_FAILURE):
        asyncio.run(tested.run(_task()))
    assert len(interaction.calls) == 2


@pytest.mark.parametrize("limit", [0, -1])
def test_experiment_rejects_nonpositive_projection_limit(
    tmp_path: Path, limit: int
) -> None:
    """The bounded projection policy cannot be silently disabled."""
    with pytest.raises(ValueError, match="limit"):
        QwenReadExperiment(
            runtime=Runtime(),
            conversation=Conversation.new(),
            interaction=_ScriptedInteraction([]),
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
        path=ResolvedPath((tmp_path / "answer.txt").resolve()), content="abcdef"
    )
    projection = experiment._project_text_result(  # noqa: SLF001
        "answer.txt", text, maximum_characters=3
    )
    assert "abc" in projection
    assert "projection truncated" in projection
    with pytest.raises(ResultProjectionError, match="only text"):
        experiment._project_text_result("answer.txt", object(), maximum_characters=3)  # noqa: SLF001
