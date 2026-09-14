# Copyright (c) 2026
# ruff: noqa: PLR2004
"""Deterministic coverage for the fixture-local B-0009 patch-proposal worker."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, cast

import pytest

from devtools.agents.conversation import Conversation, InteractionSource
from devtools.core.paths import ResolvedPath, resolve_path
from devtools.execution import Runtime
from devtools.models.interaction import ConversationRef, ModelResponse, Prompt
from devtools.resources.filesystem import (
    FileFormat,
    FilesystemNotFoundError,
    TextFile,
    read,
    write,
)
from devtools.tools import ToolInputError
from devtools.tools.filesystem import ListRepositoryDirectoryTool
from experiments.qwen.patch_proposal_worker import (
    _EXPECTED_PATCH,
    _ORIGINAL_SOURCE,
    _TARGET_PATH,
    PatchProposalError,
    QwenPatchProposalWorker,
    UngroundedFinalResponseError,
    coding_worker_task,
    create_patch_proposal_fixture,
)
from experiments.qwen.two_action_read_only_experiment import (
    QwenListDirectoryCycle,
    ReadOnlyProposalError,
)

if TYPE_CHECKING:
    from pathlib import Path


def _proposal(action: str, path: str) -> str:
    return f'{{"action":"{action}","path":"{path}"}}'


@dataclass(slots=True)
class _ScriptedInteraction:
    """Return planned local-controller replies and retain only received prompts."""

    responses: list[str]
    calls: list[Prompt] = field(default_factory=list)
    source: InteractionSource = field(default_factory=lambda: InteractionSource("qwen"))

    async def send(
        self,
        prompt: Prompt,
        *,
        conversation: ConversationRef | None = None,
    ) -> ModelResponse:
        """Return one deterministic response without contacting a model service."""
        assert conversation is None
        self.calls.append(prompt)
        return ModelResponse(content=self.responses.pop(0), source=self.source)


def _worker(
    root: Path,
    responses: list[str],
    *,
    maximum_actions: int = 5,
) -> tuple[QwenPatchProposalWorker, _ScriptedInteraction]:
    interaction = _ScriptedInteraction(responses)
    return (
        QwenPatchProposalWorker(
            runtime=Runtime(),
            conversation=Conversation.new(),
            interaction=interaction,
            repository_root=create_patch_proposal_fixture(root),
            maximum_actions=maximum_actions,
        ),
        interaction,
    )


def _required_reads() -> list[str]:
    """Return one deterministic navigation path that acquires both required facts."""
    return [
        _proposal("list_repository_directory", "."),
        _proposal("list_repository_directory", "src"),
        _proposal("read_repository_file", "src/label.py"),
        _proposal("list_repository_directory", "tests"),
        _proposal("read_repository_file", "tests/test_label.py"),
    ]


def test_worker_discovers_source_and_test_then_applies_one_valid_patch(
    tmp_path: Path,
) -> None:
    """The scripted worker has only acquired fixture facts before returning its diff."""
    worker, interaction = _worker(
        tmp_path,
        [
            *_required_reads(),
            _EXPECTED_PATCH,
        ],
    )
    task = coding_worker_task()

    result = asyncio.run(worker.run(task))

    assert "label.py" not in task.content
    assert "test_label.py" not in task.content
    assert "src" not in task.content
    assert "tests" not in task.content
    assert [cycle.relative_path for cycle in result.cycles] == [
        ".",
        "src",
        "src/label.py",
        "tests",
        "tests/test_label.py",
    ]
    assert all(
        cycle.resolved_path.value.is_relative_to((tmp_path / "repository").resolve())
        for cycle in result.cycles
    )
    listings = [
        cycle for cycle in result.cycles if isinstance(cycle, QwenListDirectoryCycle)
    ]
    expected_listed_names = ("src", "label.py", "test_label.py")
    assert [
        next(entry.name for entry in cycle.listing.entries if entry.name == expected)
        for cycle, expected in zip(listings, expected_listed_names, strict=True)
    ] == list(expected_listed_names)
    assert result.final_patch == _EXPECTED_PATCH
    assert result.behavior_validated is True
    assert len(interaction.calls) == 6
    assert all(
        str(tmp_path.resolve()) not in prompt.content for prompt in interaction.calls
    )
    root = tmp_path / "repository"
    actual_source = _read_text(_resolved(root, _TARGET_PATH)).content
    assert actual_source == _ORIGINAL_SOURCE.replace(
        ".strip()",
        ".strip().lower()",
    )
    assert _read_text(_resolved(root, "src/unrelated.py")).content == (
        'def unrelated_label() -> str:\n    return "unchanged"\n'
    )


def test_worker_corrects_one_premature_patch_then_recovers_after_required_reads(
    tmp_path: Path,
) -> None:
    """One ungrounded final response is retained and corrected without mutation."""
    worker, interaction = _worker(
        tmp_path,
        [_EXPECTED_PATCH, *_required_reads(), _EXPECTED_PATCH],
    )

    result = asyncio.run(worker.run(coding_worker_task()))

    assert len(result.grounding_corrections) == 1
    correction = result.grounding_corrections[0]
    assert correction.premature_response.content == _EXPECTED_PATCH
    assert correction.acquired_paths == ()
    assert "label.py" not in correction.follow_up.content
    assert "test_label.py" not in correction.follow_up.content
    assert len(interaction.calls) == 7
    assert result.behavior_validated is True


def test_worker_rejects_repeated_premature_final_response_without_mutating(
    tmp_path: Path,
) -> None:
    """A second final response before either required read ends the bounded probe."""
    worker, _ = _worker(tmp_path, [_EXPECTED_PATCH, _EXPECTED_PATCH])

    with pytest.raises(UngroundedFinalResponseError, match="remained ungrounded"):
        asyncio.run(worker.run(coding_worker_task()))

    assert _read_text(_resolved(tmp_path / "repository", _TARGET_PATH)).content == (
        _ORIGINAL_SOURCE
    )


@pytest.mark.parametrize(
    "responses",
    [
        [
            _EXPECTED_PATCH,
            _proposal("list_repository_directory", "src"),
            _proposal("read_repository_file", "src/label.py"),
            _EXPECTED_PATCH,
        ],
        [
            _EXPECTED_PATCH,
            _proposal("list_repository_directory", "tests"),
            _proposal("read_repository_file", "tests/test_label.py"),
            _EXPECTED_PATCH,
        ],
    ],
)
def test_worker_rejects_final_patch_after_only_one_required_file(
    tmp_path: Path,
    responses: list[str],
) -> None:
    """Reading only an implementation or test does not admit a patch."""
    worker, _ = _worker(tmp_path, responses)

    with pytest.raises(UngroundedFinalResponseError):
        asyncio.run(worker.run(coding_worker_task()))

    assert _read_text(_resolved(tmp_path / "repository", _TARGET_PATH)).content == (
        _ORIGINAL_SOURCE
    )


def test_worker_accepts_required_file_reads_in_either_order(tmp_path: Path) -> None:
    """The grounding rule tracks evidence categories rather than a path sequence."""
    worker, _ = _worker(
        tmp_path,
        [
            _EXPECTED_PATCH,
            _proposal("list_repository_directory", "tests"),
            _proposal("read_repository_file", "tests/test_label.py"),
            _proposal("list_repository_directory", "src"),
            _proposal("read_repository_file", "src/label.py"),
            _EXPECTED_PATCH,
        ],
    )

    result = asyncio.run(worker.run(coding_worker_task()))

    assert [cycle.relative_path for cycle in result.cycles] == [
        "tests",
        "tests/test_label.py",
        "src",
        "src/label.py",
    ]
    assert result.behavior_validated is True


@pytest.mark.parametrize(
    "patch",
    [
        "not a diff",
        f"```diff\n{_EXPECTED_PATCH}```",
        f"Here is the patch:\n{_EXPECTED_PATCH}",
        _EXPECTED_PATCH.replace("src/label.py", "src/unrelated.py"),
        _EXPECTED_PATCH.replace("src/label.py", "../label.py"),
        _EXPECTED_PATCH.replace(
            "+    return value.strip().lower()\n",
            "+    return value.strip().lower()\n+ignored\n",
        ),
    ],
)
def test_worker_rejects_nonpermitted_final_diff_before_mutating_fixture(
    tmp_path: Path,
    patch: str,
) -> None:
    """Malformed, fenced, prose, multi-file, and traversal diffs never apply."""
    worker, _ = _worker(tmp_path, [*_required_reads(), patch])

    with pytest.raises((PatchProposalError, ReadOnlyProposalError)):
        asyncio.run(worker.run(coding_worker_task()))

    assert _read_text(_resolved(tmp_path / "repository", _TARGET_PATH)).content == (
        _ORIGINAL_SOURCE
    )


def test_worker_rejects_patch_that_cannot_apply_to_changed_fixture(
    tmp_path: Path,
) -> None:
    """The host rejects a diff when its original hunk no longer fits."""
    worker, _ = _worker(tmp_path, [*_required_reads(), _EXPECTED_PATCH])
    target = _resolved(tmp_path / "repository", _TARGET_PATH)
    write(
        TextFile(
            target,
            "def normalize_label(value: str) -> str:\n    return value\n",
        ),
    )

    with pytest.raises(PatchProposalError, match="cannot apply"):
        asyncio.run(worker.run(coding_worker_task()))


def test_worker_rejects_applicable_patch_that_fails_fixture_behavior(
    tmp_path: Path,
) -> None:
    """Structural patch admission remains distinct from behavioral success."""
    upper_patch = _EXPECTED_PATCH.replace(".lower()", ".upper()")
    worker, _ = _worker(tmp_path, [*_required_reads(), upper_patch])

    with pytest.raises(PatchProposalError, match="does not satisfy"):
        asyncio.run(worker.run(coding_worker_task()))

    assert _read_text(_resolved(tmp_path / "repository", _TARGET_PATH)).content == (
        _ORIGINAL_SOURCE.replace(".strip()", ".strip().upper()")
    )


def test_worker_action_bound_rejects_sixth_tool_proposal(tmp_path: Path) -> None:
    """Another local proposal is rejected before a sixth Tool execution occurs."""
    worker, interaction = _worker(
        tmp_path,
        [
            _proposal("list_repository_directory", "."),
            _proposal("list_repository_directory", "src"),
            _proposal("read_repository_file", "src/label.py"),
            _proposal("list_repository_directory", "tests"),
            _proposal("read_repository_file", "tests/test_label.py"),
            _proposal("list_repository_directory", "."),
        ],
    )

    with pytest.raises(ValueError, match="at most 5"):
        asyncio.run(worker.run(coding_worker_task()))

    assert len(interaction.calls) == 6


@pytest.mark.parametrize(
    "proposal",
    ["{not json", _proposal("list_repository_directory", "../outside")],
)
def test_worker_preserves_existing_action_admission_failures(
    tmp_path: Path,
    proposal: str,
) -> None:
    """Malformed and outside-root action requests remain rejected before a patch."""
    worker, _ = _worker(tmp_path, [proposal])

    with pytest.raises((ReadOnlyProposalError, ToolInputError)):
        asyncio.run(worker.run(coding_worker_task()))


def test_worker_preserves_intermediate_tool_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A listing failure prevents final patch evaluation without wrapper conversion."""
    worker, _ = _worker(tmp_path, [_proposal("list_repository_directory", ".")])

    async def failed_listing(
        _tool: ListRepositoryDirectoryTool,
        _path: ResolvedPath,
    ) -> object:
        msg = "fixture listing failure"
        raise FilesystemNotFoundError(msg)

    monkeypatch.setattr(ListRepositoryDirectoryTool, "execute", failed_listing)

    with pytest.raises(FilesystemNotFoundError, match="fixture listing failure"):
        asyncio.run(worker.run(coding_worker_task()))


def _resolved(root: Path, relative_path: str) -> ResolvedPath:
    """Return the test fixture path through the same canonical path operation."""
    return resolve_path(relative_path, base_directory=root)


def _read_text(path: ResolvedPath) -> TextFile:
    """Read a fixture file through the canonical filesystem Resource."""
    return cast("TextFile", read(path, file_format=FileFormat.TEXT))
