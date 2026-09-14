# Copyright (c) 2026
# ruff: noqa: PLR2004
"""Deterministic tests for the bounded heterogeneous read-only Qwen experiment."""

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
from devtools.resources.filesystem import FilesystemNotFoundError
from devtools.tools.filesystem import (
    ListRepositoryDirectoryTool,
    ReadRepositoryFileTool,
)
from experiments.qwen import two_action_read_only_experiment as experiment
from experiments.qwen.two_action_read_only_experiment import (
    QwenListDirectoryCycle,
    QwenReadOnlyCycle,
    QwenReadRepositoryFileCycle,
    QwenTwoActionReadOnlyExperiment,
    ReadOnlyProposalError,
)

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from devtools.models.interaction import ModelInteraction


@dataclass(slots=True)
class _ScriptedInteraction:
    """Return exact planned assistant content and retain each controller input."""

    responses: list[str]
    calls: list[Prompt] = field(default_factory=list)
    source: InteractionSource = field(default_factory=lambda: InteractionSource("qwen"))

    async def send(
        self,
        prompt: Prompt,
        *,
        conversation: ConversationRef | None = None,
        maximum_output_tokens: int | None = None,
        thinking_enabled: bool | None = None,
    ) -> ModelResponse:
        """Return the next planned final assistant ConversationMessage."""
        assert conversation is None
        del maximum_output_tokens, thinking_enabled
        self.calls.append(prompt)
        return ModelResponse(content=self.responses.pop(0), source=self.source)


@dataclass(slots=True)
class _FailingLaterInteraction:
    """Return one proposal, then preserve a provider-like later-turn failure."""

    source: InteractionSource = field(default_factory=lambda: InteractionSource("qwen"))
    calls: list[Prompt] = field(default_factory=list)

    async def send(
        self,
        prompt: Prompt,
        *,
        conversation: ConversationRef | None = None,
        maximum_output_tokens: int | None = None,
        thinking_enabled: bool | None = None,
    ) -> ModelResponse:
        """Produce a first proposal only, then propagate a later failure."""
        assert conversation is None
        del maximum_output_tokens, thinking_enabled
        self.calls.append(prompt)
        if len(self.calls) == 1:
            return ModelResponse(
                content=_proposal("list_repository_directory", "facts"),
                source=self.source,
            )
        msg = "provider unavailable"
        raise RuntimeError(msg)


def _proposal(action: str, path: str) -> str:
    return f'{{"action":"{action}","path":"{path}"}}'


def _task() -> ConversationMessage:
    return ConversationMessage.new(
        "Find the target using only the permitted exact read-only proposals.",
        role=ConversationMessageRole.USER,
        source=InteractionSource("test-caller"),
    )


def _root_navigation_task() -> ConversationMessage:
    """Construct a task that names neither a target nor an initial directory."""
    return ConversationMessage.new(
        "Find the repository implementation responsible for reading files and report "
        "the marker it defines.",
        role=ConversationMessageRole.USER,
        source=InteractionSource("test-caller"),
    )


def _write(root: Path, relative_path: str, content: str) -> Path:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def _root_navigation_fixture(root: Path) -> tuple[Path, str]:
    """Create one repository whose source target is reached only by direct listings."""
    _write(root, "docs/decoy.md", "documentation decoy")
    _write(root, "src/unrelated/reader.py", "MARKER = 'DECOY'")
    _write(root, "tests/decoy_test.py", "MARKER = 'TEST-DECOY'")
    marker = "ROOT-NAVIGATION-TARGET"
    target = _write(
        root,
        "src/devtools/resources/filesystem/reading.py",
        f"MARKER = {marker!r}\n",
    )
    return target, marker


def _experiment(
    root: Path,
    interaction: ModelInteraction,
    on_cycle_completed: Callable[[QwenReadOnlyCycle], None] | None = None,
    *,
    maximum_actions: int = 2,
) -> tuple[QwenTwoActionReadOnlyExperiment, Conversation]:
    session = Conversation.new()
    return (
        QwenTwoActionReadOnlyExperiment(
            runtime=Runtime(),
            conversation=session,
            interaction=interaction,
            repository_root=ResolvedPath(root.resolve()),
            maximum_actions=maximum_actions,
            on_cycle_completed=on_cycle_completed,
        ),
        session,
    )


def test_root_origin_navigation_reaches_unknown_python_source_without_path_leakage(
    tmp_path: Path,
) -> None:
    """Direct listings navigate from root to a source file named only by its parent."""
    root = tmp_path / "repository"
    target, marker = _root_navigation_fixture(root)
    paths = (
        ".",
        "src",
        "src/devtools",
        "src/devtools/resources",
        "src/devtools/resources/filesystem",
        "src/devtools/resources/filesystem/reading.py",
    )
    interaction = _ScriptedInteraction(
        [
            *(_proposal("list_repository_directory", path) for path in paths[:-1]),
            _proposal("read_repository_file", paths[-1]),
            marker,
        ],
    )
    task = _root_navigation_task()
    tested, _ = _experiment(root, interaction, maximum_actions=len(paths))

    result = asyncio.run(tested.run(task))

    assert "reading.py" not in task.content
    assert "filesystem" not in task.content
    assert "src/" not in task.content
    assert [cycle.relative_path for cycle in result.cycles] == list(paths)
    assert all(
        cycle.resolved_path.value.is_relative_to(root.resolve())
        for cycle in result.cycles
    )
    assert [type(cycle) for cycle in result.cycles] == [
        QwenListDirectoryCycle,
        QwenListDirectoryCycle,
        QwenListDirectoryCycle,
        QwenListDirectoryCycle,
        QwenListDirectoryCycle,
        QwenReadRepositoryFileCycle,
    ]
    listings = [
        cycle
        for cycle in result.cycles
        if isinstance(cycle, QwenListDirectoryCycle)
    ]
    assert [
        next(entry.name for entry in cycle.listing.entries if entry.name == expected)
        for cycle, expected in zip(
            listings,
            ("src", "devtools", "resources", "filesystem", "reading.py"),
            strict=True,
        )
    ] == ["src", "devtools", "resources", "filesystem", "reading.py"]
    reads = [
        cycle
        for cycle in result.cycles
        if isinstance(cycle, QwenReadRepositoryFileCycle)
    ]
    assert len(reads) == 1
    assert reads[0].resolved_path == ResolvedPath(target.resolve())
    assert marker in reads[0].result_projection
    assert all(
        str(root.resolve()) not in cycle.result_projection
        and str(root.resolve()) not in cycle.follow_up.content
        for cycle in result.cycles
    )
    assert result.final_message.content == marker


def test_root_navigation_action_limit_blocks_seventh_tool_execution(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The configured root-navigation cap rejects another proposal before execution."""
    root = tmp_path / "repository"
    _root_navigation_fixture(root)
    paths = (
        ".",
        "src",
        "src/devtools",
        "src/devtools/resources",
        "src/devtools/resources/filesystem",
        "src/devtools/resources/filesystem/reading.py",
    )
    interaction = _ScriptedInteraction(
        [
            *(_proposal("list_repository_directory", path) for path in paths[:-1]),
            _proposal("read_repository_file", paths[-1]),
            _proposal("list_repository_directory", "."),
        ],
    )
    executed: list[str] = []
    original_list = ListRepositoryDirectoryTool.execute
    original_read = ReadRepositoryFileTool.execute

    async def counted_list(
        tool: ListRepositoryDirectoryTool,
        path: ResolvedPath,
    ) -> object:
        executed.append("list_repository_directory")
        return await original_list(tool, path)

    async def counted_read(
        tool: ReadRepositoryFileTool,
        path: ResolvedPath,
    ) -> object:
        executed.append("read_repository_file")
        return await original_read(tool, path)

    monkeypatch.setattr(ListRepositoryDirectoryTool, "execute", counted_list)
    monkeypatch.setattr(ReadRepositoryFileTool, "execute", counted_read)
    tested, _ = _experiment(root, interaction, maximum_actions=len(paths))

    with pytest.raises(ReadOnlyProposalError, match="at most 6"):
        asyncio.run(tested.run(_root_navigation_task()))

    assert executed == [
        "list_repository_directory",
        "list_repository_directory",
        "list_repository_directory",
        "list_repository_directory",
        "list_repository_directory",
        "read_repository_file",
    ]


@pytest.mark.parametrize("maximum_actions", [0, -1])
def test_experiment_rejects_nonpositive_action_bound(
    tmp_path: Path,
    maximum_actions: int,
) -> None:
    """A configured action budget cannot be silently disabled."""
    with pytest.raises(ValueError, match="Maximum read-only actions"):
        QwenTwoActionReadOnlyExperiment(
            runtime=Runtime(),
            conversation=Conversation.new(),
            interaction=_ScriptedInteraction([]),
            repository_root=ResolvedPath(tmp_path.resolve()),
            maximum_actions=maximum_actions,
        )


def test_list_then_read_retains_heterogeneous_cycles_and_stateless_prompts(
    tmp_path: Path,
) -> None:
    """A list result makes a discovered file name available for the later read turn."""
    root = tmp_path / "repository"
    _write(root, "facts/decoy.txt", "decoy")
    target = _write(root, "facts/target-random.txt", "NONCE-TARGET")
    interaction = _ScriptedInteraction(
        [
            _proposal("list_repository_directory", "facts"),
            _proposal("read_repository_file", "facts/target-random.txt"),
            "NONCE-TARGET",
        ],
    )
    completed_cycles: list[QwenReadOnlyCycle] = []
    tested, session = _experiment(root, interaction, completed_cycles.append)

    result = asyncio.run(tested.run(_task()))

    assert tuple(completed_cycles) == result.cycles
    assert isinstance(result.cycles[0], QwenListDirectoryCycle)
    assert isinstance(result.cycles[1], QwenReadRepositoryFileCycle)
    assert result.cycles[0].relative_path == "facts"
    assert result.cycles[1].resolved_path == ResolvedPath(target.resolve())
    assert "target-random.txt [file]" in result.cycles[0].result_projection
    assert str(root.resolve()) not in result.cycles[0].result_projection
    assert "NONCE-TARGET" in result.cycles[1].result_projection
    assert '"action":"list_repository_directory"' in result.cycles[0].follow_up.content
    assert '"action":"read_repository_file"' in result.cycles[0].follow_up.content
    assert "one remaining read-only action" in result.cycles[0].follow_up.content
    assert "Do not propose another action." in result.cycles[1].follow_up.content
    assert result.final_message.content == "NONCE-TARGET"
    assert [message.role for message in session.history] == [
        ConversationMessageRole.USER,
        ConversationMessageRole.ASSISTANT,
        ConversationMessageRole.SYSTEM,
        ConversationMessageRole.ASSISTANT,
        ConversationMessageRole.SYSTEM,
        ConversationMessageRole.ASSISTANT,
    ]


@pytest.mark.parametrize(
    "responses",
    [
        [
            _proposal("read_repository_file", "facts/first.txt"),
            _proposal("list_repository_directory", "facts"),
            "final",
        ],
        [
            _proposal("list_repository_directory", "facts"),
            _proposal("list_repository_directory", "facts"),
            "final",
        ],
        [
            _proposal("read_repository_file", "facts/first.txt"),
            _proposal("read_repository_file", "facts/first.txt"),
            "final",
        ],
    ],
)
def test_strategy_neutral_valid_action_orders_are_structurally_permitted(
    tmp_path: Path,
    responses: list[str],
) -> None:
    """The controller permits valid actions without encoding task strategy."""
    root = tmp_path / "repository"
    _write(root, "facts/first.txt", "first")
    interaction = _ScriptedInteraction(responses)
    tested, _ = _experiment(root, interaction)

    result = asyncio.run(tested.run(_task()))

    assert len(result.cycles) == 2
    assert result.final_message.content == "final"


def test_immediate_and_one_action_final_answers_terminate_normally(
    tmp_path: Path,
) -> None:
    """Two accepted actions are a cap rather than a requirement."""
    root = tmp_path / "repository"
    _write(root, "facts/first.txt", "first")
    immediate, _ = _experiment(root, _ScriptedInteraction(["final immediately"]))
    after_one, _ = _experiment(
        root,
        _ScriptedInteraction(
            [_proposal("read_repository_file", "facts/first.txt"), "final after one"],
        ),
    )

    immediate_result = asyncio.run(immediate.run(_task()))
    after_one_result = asyncio.run(after_one.run(_task()))

    assert immediate_result.cycles == ()
    assert after_one_result.final_message.content == "final after one"
    assert len(after_one_result.cycles) == 1


def test_third_valid_proposal_is_rejected_before_a_third_tool_execution(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The two-action cap rejects a third proposal without requesting a fourth turn."""
    root = tmp_path / "repository"
    _write(root, "facts/first.txt", "first")
    interaction = _ScriptedInteraction(
        [
            _proposal("list_repository_directory", "facts"),
            _proposal("read_repository_file", "facts/first.txt"),
            _proposal("list_repository_directory", "facts"),
        ],
    )
    tested, _ = _experiment(root, interaction)
    executed_actions: list[str] = []
    original_list = ListRepositoryDirectoryTool.execute
    original_read = ReadRepositoryFileTool.execute

    async def counted_list(
        tool: ListRepositoryDirectoryTool,
        path: ResolvedPath,
    ) -> object:
        executed_actions.append("list_repository_directory")
        return await original_list(tool, path)

    async def counted_read(
        tool: ReadRepositoryFileTool,
        path: ResolvedPath,
    ) -> object:
        executed_actions.append("read_repository_file")
        return await original_read(tool, path)

    monkeypatch.setattr(ListRepositoryDirectoryTool, "execute", counted_list)
    monkeypatch.setattr(ReadRepositoryFileTool, "execute", counted_read)

    with pytest.raises(ReadOnlyProposalError, match="at most two"):
        asyncio.run(tested.run(_task()))
    assert len(interaction.calls) == 3
    assert executed_actions == [
        "list_repository_directory",
        "read_repository_file",
    ]


@pytest.mark.parametrize(
    "content",
    [
        '{"action":"unknown","path":"facts"}',
        '{"action":"list_repository_directory","path":" facts"}',
        '{"action":"list_repository_directory","path":"facts","extra":1}',
        '{"action":"list_repository_directory","path":"facts","path":"other"}',
        '{"action":"list_repository_directory","action":"read_repository_file","path":"facts"}',
        '{"action":"list_repository_directory","path":123}',
        '{"action":"read_repository_file","path":null}',
        '{"action":"list_repository_directory","path":"facts"} and then inspect it',
        "{not json",
        '["list_repository_directory"]',
        '```json\n{"action":"list_repository_directory","path":"facts"}\n```',
    ],
)
def test_action_like_invalid_responses_are_rejected(content: str) -> None:
    """Protocol-shaped malformed output cannot silently become final text."""
    with pytest.raises(ReadOnlyProposalError):
        experiment._classify_response(content)  # noqa: SLF001


@pytest.mark.parametrize(
    "content",
    [
        "The action completed.",
        "read facts carefully",
        "list_repository_directory was unnecessary",
        'I think use {"action":"list_repository_directory","path":"facts"}',
    ],
)
def test_ordinary_and_embedded_protocol_prose_remain_final_text(content: str) -> None:
    """The classifier does not scan ordinary prose for embedded proposals."""
    assert experiment._classify_response(content) is None  # noqa: SLF001


def test_absolute_path_proposal_is_rejected() -> None:
    """Proposal admission remains host-independent about absolute path syntax."""
    with pytest.raises(ReadOnlyProposalError, match="repository-relative"):
        experiment._classify_response(  # noqa: SLF001
            _proposal("list_repository_directory", "C:\\\\facts"),
        )


@pytest.mark.parametrize(
    ("first_action", "failing_tool"),
    [
        ("list_repository_directory", ListRepositoryDirectoryTool),
        ("read_repository_file", ReadRepositoryFileTool),
    ],
)
def test_tool_failures_propagate_after_either_action_shape(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    first_action: str,
    failing_tool: type[ListRepositoryDirectoryTool | ReadRepositoryFileTool],
) -> None:
    """The experiment preserves Tool failures without inventing a shared wrapper."""
    root = tmp_path / "repository"
    _write(root, "facts/first.txt", "first")
    path = "facts" if first_action == "list_repository_directory" else "facts/first.txt"
    completed_cycles: list[QwenReadOnlyCycle] = []
    tested, _ = _experiment(
        root,
        _ScriptedInteraction([_proposal(first_action, path)]),
        completed_cycles.append,
    )

    async def failed_execute(_tool: object, _path: ResolvedPath) -> object:
        msg = "fixture tool failure"
        raise FilesystemNotFoundError(msg)

    monkeypatch.setattr(failing_tool, "execute", failed_execute)

    with pytest.raises(FilesystemNotFoundError, match="fixture tool failure"):
        asyncio.run(tested.run(_task()))

    assert completed_cycles == []


def test_later_interaction_failure_propagates_after_a_completed_listing(
    tmp_path: Path,
) -> None:
    """The local loop does not convert a later provider failure into a final answer."""
    root = tmp_path / "repository"
    _write(root, "facts/first.txt", "first")
    interaction = _FailingLaterInteraction()
    completed_cycles: list[QwenReadOnlyCycle] = []
    tested, session = _experiment(root, interaction, completed_cycles.append)

    with pytest.raises(RuntimeError, match="provider unavailable"):
        asyncio.run(tested.run(_task()))

    assert len(interaction.calls) == 2
    assert len(completed_cycles) == 1
    assert isinstance(completed_cycles[0], QwenListDirectoryCycle)
    assert [message.role for message in session.history] == [
        ConversationMessageRole.USER,
        ConversationMessageRole.ASSISTANT,
        ConversationMessageRole.SYSTEM,
    ]


def test_later_malformed_proposal_retains_only_the_completed_list_cycle(
    tmp_path: Path,
) -> None:
    """A completed list is published before strict parsing rejects the next turn."""
    root = tmp_path / "repository"
    _write(root, "facts/first.txt", "first")
    completed_cycles: list[QwenReadOnlyCycle] = []
    tested, _ = _experiment(
        root,
        _ScriptedInteraction(
            [_proposal("list_repository_directory", "facts"), "{not json"],
        ),
        completed_cycles.append,
    )

    with pytest.raises(ReadOnlyProposalError):
        asyncio.run(tested.run(_task()))

    assert len(completed_cycles) == 1
    assert isinstance(completed_cycles[0], QwenListDirectoryCycle)


def test_malformed_first_proposal_publishes_no_completed_cycles(tmp_path: Path) -> None:
    """Strict first-turn rejection occurs before any cycle has completed."""
    root = tmp_path / "repository"
    root.mkdir()
    completed_cycles: list[QwenReadOnlyCycle] = []
    tested, _ = _experiment(
        root,
        _ScriptedInteraction(["{not json"]),
        completed_cycles.append,
    )

    with pytest.raises(ReadOnlyProposalError):
        asyncio.run(tested.run(_task()))

    assert completed_cycles == []


def test_second_tool_failure_retains_only_the_first_completed_cycle(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A failed second read is not published as a completed experimental cycle."""
    root = tmp_path / "repository"
    _write(root, "facts/first.txt", "first")
    completed_cycles: list[QwenReadOnlyCycle] = []
    tested, _ = _experiment(
        root,
        _ScriptedInteraction(
            [
                _proposal("list_repository_directory", "facts"),
                _proposal("read_repository_file", "facts/first.txt"),
            ],
        ),
        completed_cycles.append,
    )

    async def failed_read(_tool: object, _path: ResolvedPath) -> object:
        msg = "fixture second-tool failure"
        raise FilesystemNotFoundError(msg)

    monkeypatch.setattr(ReadRepositoryFileTool, "execute", failed_read)

    with pytest.raises(FilesystemNotFoundError, match="fixture second-tool failure"):
        asyncio.run(tested.run(_task()))

    assert len(completed_cycles) == 1
    assert isinstance(completed_cycles[0], QwenListDirectoryCycle)
