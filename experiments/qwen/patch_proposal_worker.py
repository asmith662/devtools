# Copyright (c) 2026
"""Fixture-local deterministic coding-worker composition for B-0009."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from devtools.agents.conversation import (
    ConversationMessage,
    ConversationMessageRole,
    InteractionSource,
)
from devtools.core.paths import resolve_path
from devtools.resources.filesystem import FileFormat, TextFile, read, write
from experiments.qwen.two_action_read_only_experiment import (
    QwenReadOnlyCycle,
    QwenReadRepositoryFileCycle,
    QwenTwoActionReadOnlyExperiment,
)

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from devtools.agents.conversation import Conversation
    from devtools.core.paths import ResolvedPath
    from devtools.execution import Runtime
    from devtools.models.interaction import ModelInteraction


_DEFAULT_MAXIMUM_ACTIONS = 5
_TARGET_PATH = "src/label.py"
_TEST_PATH = "tests/test_label.py"
_UNRELATED_PATH = "src/unrelated.py"
_REQUIRED_EVIDENCE_PATHS = frozenset({_TARGET_PATH, _TEST_PATH})
_MAXIMUM_GROUNDING_CORRECTIONS = 1
_ORIGINAL_SOURCE = "def normalize_label(value: str) -> str:\n    return value.strip()\n"
_UNRELATED_SOURCE = 'def unrelated_label() -> str:\n    return "unchanged"\n'
_PATCH_PREFIX = (
    "--- a/src/label.py",
    "+++ b/src/label.py",
    "@@ -1,2 +1,2 @@",
    " def normalize_label(value: str) -> str:",
    "-    return value.strip()",
)
_PERMITTED_REPLACEMENTS = {
    "+    return value.strip().lower()",
    "+    return value.strip().upper()",
}
_PATCH_LINE_COUNT = 6
_EXPECTED_PATCH = "\n".join(
    (*_PATCH_PREFIX, "+    return value.strip().lower()", ""),
)


class PatchProposalError(ValueError):
    """Represent a rejected final patch in this fixture-specific experiment."""


class UngroundedFinalResponseError(ValueError):
    """Represent a final patch refused after the local grounding correction."""


@dataclass(frozen=True, slots=True)
class QwenGroundingCorrection:
    """Retain one deferred final response and the local inspection correction."""

    premature_response: ConversationMessage
    follow_up: ConversationMessage
    acquired_paths: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class QwenPatchProposalWorkerResult:
    """Retain the bounded facts and terminal fixture result for one worker run."""

    task: ConversationMessage
    cycles: tuple[QwenReadOnlyCycle, ...]
    grounding_corrections: tuple[QwenGroundingCorrection, ...]
    final_patch: str
    canonical_patch: str
    terminal_newline_canonicalized: bool
    behavior_validated: bool


def coding_worker_task() -> ConversationMessage:
    """Create the fixture task without disclosing repository locations."""
    return ConversationMessage.new(
        "Make label normalization case-insensitive while preserving existing trimming "
        "behavior. Repository contents are unknown: inspect the repository before "
        "proposing a patch, and read the relevant implementation and focused test. "
        'The only repository actions are {"action":"list_repository_directory",'
        '"path":"<repository-relative-path>"} and {"action":'
        '"read_repository_file","path":"<repository-relative-path>"}. '
        "Return exactly one unified diff and make no unrelated changes.",
        role=ConversationMessageRole.USER,
        source=InteractionSource("test-caller"),
    )


def create_patch_proposal_fixture(parent: Path) -> ResolvedPath:
    """Create the isolated repository used only by this bounded experiment."""
    root = parent / "repository"
    files = {
        "docs/decoy.md": "The label behavior is documented elsewhere.\n",
        _TARGET_PATH: _ORIGINAL_SOURCE,
        _UNRELATED_PATH: _UNRELATED_SOURCE,
        _TEST_PATH: (
            "from src.label import normalize_label\n\n\n"
            "def test_normalize_label_trims_and_ignores_case() -> None:\n"
            '    assert normalize_label("  Alpha  ") == "alpha"\n'
        ),
    }
    for relative_path, content in files.items():
        target = root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        write(TextFile(resolve_path(target), content))
    return resolve_path(root)


class QwenPatchProposalWorker:
    """Coordinate a disposable-fixture patch proposal without model-side mutation."""

    def __init__(  # noqa: PLR0913 - bounded reporting hook preserves explicit collaborators.
        self,
        *,
        runtime: Runtime,
        conversation: Conversation,
        interaction: ModelInteraction,
        repository_root: ResolvedPath,
        maximum_actions: int = _DEFAULT_MAXIMUM_ACTIONS,
        on_cycle_completed: Callable[[QwenReadOnlyCycle], None] | None = None,
        on_grounding_correction: (
            Callable[[QwenGroundingCorrection], None] | None
        ) = None,
    ) -> None:
        """Configure the existing read-only controller and fixture root."""
        corrections: list[QwenGroundingCorrection] = []

        def on_final_response(
            response: ConversationMessage,
            cycles: tuple[QwenReadOnlyCycle, ...],
        ) -> ConversationMessage | None:
            return self._ground_final_response(
                response,
                cycles,
                corrections,
                on_grounding_correction,
            )

        self._read_only = QwenTwoActionReadOnlyExperiment(
            runtime=runtime,
            conversation=conversation,
            interaction=interaction,
            repository_root=repository_root,
            maximum_actions=maximum_actions,
            on_cycle_completed=on_cycle_completed,
            on_final_response=on_final_response,
        )
        self._root = resolve_path(repository_root.value)
        self._corrections = corrections
        self._task: ConversationMessage | None = None

    async def run(self, task: ConversationMessage) -> QwenPatchProposalWorkerResult:
        """Acquire fixture facts, then validate and apply one final local patch."""
        self._task = task
        read_only_result = await self._read_only.run(task)
        final_patch = read_only_result.final_message.content
        canonical_patch = _apply_patch(self._root, final_patch)
        _validate_fixture_behavior(self._root)
        return QwenPatchProposalWorkerResult(
            task=read_only_result.task,
            cycles=read_only_result.cycles,
            grounding_corrections=tuple(self._corrections),
            final_patch=final_patch,
            canonical_patch=canonical_patch,
            terminal_newline_canonicalized=canonical_patch != final_patch,
            behavior_validated=True,
        )

    def _ground_final_response(
        self,
        response: ConversationMessage,
        cycles: tuple[QwenReadOnlyCycle, ...],
        corrections: list[QwenGroundingCorrection],
        on_grounding_correction: Callable[[QwenGroundingCorrection], None] | None,
    ) -> ConversationMessage | None:
        """Require fixture evidence before admitting one final patch response."""
        acquired_paths = tuple(
            cycle.relative_path
            for cycle in cycles
            if isinstance(cycle, QwenReadRepositoryFileCycle)
        )
        if _REQUIRED_EVIDENCE_PATHS.issubset(acquired_paths):
            return None
        if len(corrections) >= _MAXIMUM_GROUNDING_CORRECTIONS:
            msg = "Final patch remained ungrounded after the inspection correction."
            raise UngroundedFinalResponseError(msg)
        task = self._task
        if task is None:
            msg = "The coding-worker task was not configured before final admission."
            raise RuntimeError(msg)
        follow_up = ConversationMessage.new(
            f"Continue this task:\n{task.content}\n\n"
            "Repository contents are not known yet. Inspect the repository with the "
            "available read-only actions, read the relevant implementation and focused "
            "test, then return the final unified diff.",
            role=ConversationMessageRole.SYSTEM,
            source=InteractionSource("runtime"),
        )
        correction = QwenGroundingCorrection(response, follow_up, acquired_paths)
        corrections.append(correction)
        if on_grounding_correction is not None:
            on_grounding_correction(correction)
        return follow_up


def _apply_patch(root: ResolvedPath, patch: str) -> str:
    """Apply one admitted fixture diff through the canonical filesystem Resource."""
    canonical_patch, replacement = _parse_patch(patch)
    target = resolve_path(_TARGET_PATH, base_directory=root.value)
    current = _read_text(target)
    current_text = current.content
    if current_text != _ORIGINAL_SOURCE:
        msg = "The permitted patch cannot apply to the fixture's original source."
        raise PatchProposalError(msg)
    write(
        TextFile(
            target,
            _ORIGINAL_SOURCE.replace("    return value.strip()", replacement),
            encoding=current.encoding,
        ),
    )
    return canonical_patch


def _parse_patch(patch: str) -> tuple[str, str]:
    """Admit only the one-file, one-line diff grammar used by this fixture."""
    content = patch.removesuffix("\n")
    lines = content.split("\n")
    if tuple(lines[:5]) != _PATCH_PREFIX or len(lines) != _PATCH_LINE_COUNT:
        msg = "Final diff must modify only the permitted fixture source hunk."
        raise PatchProposalError(msg)
    replacement = lines[5]
    if replacement not in _PERMITTED_REPLACEMENTS:
        msg = "Final diff replacement is not permitted by this fixture contract."
        raise PatchProposalError(msg)
    return f"{content}\n", replacement[1:]


def _validate_fixture_behavior(root: ResolvedPath) -> None:
    """Execute the fixture's focused behavioral checks after host-side application."""
    target = resolve_path(_TARGET_PATH, base_directory=root.value)
    source = _read_text(target).content
    namespace: dict[str, object] = {}
    exec(compile(source, str(target.value), "exec"), namespace)  # noqa: S102
    normalizer = namespace.get("normalize_label")
    if not callable(normalizer) or normalizer("  Alpha  ") != "alpha":
        msg = "Applied patch does not satisfy case-insensitive trimmed normalization."
        raise PatchProposalError(msg)
    unrelated = _read_text(resolve_path(_UNRELATED_PATH, base_directory=root.value))
    if unrelated.content != _UNRELATED_SOURCE:
        msg = "Applied patch changed unrelated fixture content."
        raise PatchProposalError(msg)


def _read_text(path: ResolvedPath) -> TextFile:
    """Read one fixture file through the Resource's explicit text representation."""
    return cast("TextFile", read(path, file_format=FileFormat.TEXT))
