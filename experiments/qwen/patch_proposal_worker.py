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
    from devtools.models.interaction import (
        ModelInteraction,
        ModelResponse,
        ModelTermination,
        ModelUsage,
    )


_DEFAULT_MAXIMUM_ACTIONS = 5
_TARGET_PATH = "src/label.py"
_TEST_PATH = "tests/test_label.py"
_UNRELATED_PATH = "src/unrelated.py"
_MAXIMUM_GROUNDING_CORRECTIONS = 1
_ORIGINAL_SOURCE = "def normalize_label(value: str) -> str:\n    return value.strip()\n"
_UNRELATED_SOURCE = 'def unrelated_label() -> str:\n    return "unchanged"\n'
_PERMITTED_REPLACEMENTS = {
    "+    return value.strip().lower()",
    "+    return value.strip().upper()",
}
_PATCH_LINE_COUNT = 6
_SELECTION_TARGET_PATH = "src/labels.py"
_SELECTION_TEST_PATH = "tests/test_labels.py"
_SELECTION_PLAUSIBLE_PATHS = frozenset(
    {
        "docs/label-conventions.md",
        "src/display_labels.py",
        "src/label_slug.py",
        "tests/test_display_labels.py",
        "tests/test_label_slug.py",
    },
)
_SELECTION_IRRELEVANT_PATHS = frozenset(
    {"src/unrelated.py", "tests/test_unrelated.py"},
)


@dataclass(frozen=True, slots=True)
class _PatchProposalFixture:
    """Keep one fixed experiment fixture contract outside reusable framework code."""

    files: tuple[tuple[str, str], ...]
    target_path: str
    test_path: str
    plausible_unnecessary_paths: frozenset[str] = frozenset()
    clearly_irrelevant_paths: frozenset[str] = frozenset()

    @property
    def required_evidence_paths(self) -> frozenset[str]:
        """Return the two task-specific reads required before final admission."""
        return frozenset({self.target_path, self.test_path})


_BASELINE_FIXTURE = _PatchProposalFixture(
    files=(
        ("docs/decoy.md", "The label behavior is documented elsewhere.\n"),
        (_TARGET_PATH, _ORIGINAL_SOURCE),
        (_UNRELATED_PATH, _UNRELATED_SOURCE),
        (
            _TEST_PATH,
            (
                "from src.label import normalize_label\n\n\n"
                "def test_normalize_label_trims_and_ignores_case() -> None:\n"
                '    assert normalize_label("  Alpha  ") == "alpha"\n'
            ),
        ),
    ),
    target_path=_TARGET_PATH,
    test_path=_TEST_PATH,
)

_SELECTION_STRESS_FIXTURE = _PatchProposalFixture(
    files=(
        (
            "docs/label-conventions.md",
            "Display labels preserve caller capitalization; matching keys do not.\n",
        ),
        (_SELECTION_TARGET_PATH, _ORIGINAL_SOURCE),
        (
            "src/display_labels.py",
            (
                "def normalize_display_label(value: str) -> str:\n"
                "    return value.strip()\n"
            ),
        ),
        (
            "src/label_slug.py",
            (
                "def normalize_label_slug(value: str) -> str:\n"
                '    return value.strip().lower().replace(" ", "-")\n'
            ),
        ),
        (_UNRELATED_PATH, _UNRELATED_SOURCE),
        (
            _SELECTION_TEST_PATH,
            (
                "from src.labels import normalize_label\n\n\n"
                "def test_normalize_label_trims_and_ignores_case() -> None:\n"
                '    assert normalize_label("  Alpha  ") == "alpha"\n'
            ),
        ),
        (
            "tests/test_display_labels.py",
            (
                "from src.display_labels import normalize_display_label\n\n\n"
                "def test_display_label_preserves_case() -> None:\n"
                '    assert normalize_display_label("  Alpha  ") == "Alpha"\n'
            ),
        ),
        (
            "tests/test_label_slug.py",
            (
                "from src.label_slug import normalize_label_slug\n\n\n"
                "def test_label_slug_is_lowercase() -> None:\n"
                '    assert normalize_label_slug("  Alpha Beta  ") == "alpha-beta"\n'
            ),
        ),
        (
            "tests/test_unrelated.py",
            (
                "from src.unrelated import unrelated_label\n\n\n"
                "def test_unrelated_label_is_unchanged() -> None:\n"
                '    assert unrelated_label() == "unchanged"\n'
            ),
        ),
    ),
    target_path=_SELECTION_TARGET_PATH,
    test_path=_SELECTION_TEST_PATH,
    plausible_unnecessary_paths=_SELECTION_PLAUSIBLE_PATHS,
    clearly_irrelevant_paths=_SELECTION_IRRELEVANT_PATHS,
)


def _patch_prefix(fixture: _PatchProposalFixture) -> tuple[str, ...]:
    """Create the one permitted fixture-local diff header."""
    return (
        f"--- a/{fixture.target_path}",
        f"+++ b/{fixture.target_path}",
        "@@ -1,2 +1,2 @@",
        " def normalize_label(value: str) -> str:",
        "-    return value.strip()",
    )


def _expected_patch(fixture: _PatchProposalFixture) -> str:
    """Return the deterministic successful diff for one fixed fixture."""
    return "\n".join((*_patch_prefix(fixture), "+    return value.strip().lower()", ""))


_EXPECTED_PATCH = _expected_patch(_BASELINE_FIXTURE)
_SELECTION_STRESS_EXPECTED_PATCH = _expected_patch(_SELECTION_STRESS_FIXTURE)


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
    model_reasoning_contents: tuple[str | None, ...]
    model_terminations: tuple[ModelTermination | None, ...]
    model_usages: tuple[ModelUsage | None, ...]


@dataclass(frozen=True, slots=True)
class QwenSelectionMeasurements:
    """Retain fixture-specific read relevance facts for the stress probe only."""

    required_files_read: tuple[str, ...]
    plausible_unnecessary_files_read: tuple[str, ...]
    clearly_irrelevant_files_read: tuple[str, ...]
    required_read_coverage: float
    acquisition_precision: float | None


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


def selection_stress_task() -> ConversationMessage:
    """Create the selection-stress task without disclosing fixture locations."""
    return ConversationMessage.new(
        "Make label matching case-insensitive while preserving existing trimming "
        "behavior. Repository contents are unknown: inspect the repository before "
        "proposing a patch, and read the relevant implementation and focused test. "
        "Return exactly one unified diff and make no unrelated changes.",
        role=ConversationMessageRole.USER,
        source=InteractionSource("test-caller"),
    )


def create_patch_proposal_fixture(parent: Path) -> ResolvedPath:
    """Create the isolated repository used only by this bounded experiment."""
    return _create_fixture(parent, _BASELINE_FIXTURE)


def create_selection_stress_fixture(parent: Path) -> ResolvedPath:
    """Create the fixed repository-selection stress fixture for B-0009."""
    return _create_fixture(parent, _SELECTION_STRESS_FIXTURE)


def selection_stress_measurements(
    cycles: tuple[QwenReadOnlyCycle, ...],
) -> QwenSelectionMeasurements:
    """Classify only successful file reads against fixed stress-fixture roles."""
    read_paths = tuple(
        cycle.relative_path
        for cycle in cycles
        if isinstance(cycle, QwenReadRepositoryFileCycle)
    )
    unique_paths = tuple(dict.fromkeys(read_paths))
    required = tuple(
        path
        for path in unique_paths
        if path in _SELECTION_STRESS_FIXTURE.required_evidence_paths
    )
    plausible = tuple(
        path
        for path in unique_paths
        if path in _SELECTION_STRESS_FIXTURE.plausible_unnecessary_paths
    )
    irrelevant = tuple(
        path
        for path in unique_paths
        if path in _SELECTION_STRESS_FIXTURE.clearly_irrelevant_paths
    )
    required_events = sum(
        path in _SELECTION_STRESS_FIXTURE.required_evidence_paths for path in read_paths
    )
    return QwenSelectionMeasurements(
        required_files_read=required,
        plausible_unnecessary_files_read=plausible,
        clearly_irrelevant_files_read=irrelevant,
        required_read_coverage=len(required)
        / len(_SELECTION_STRESS_FIXTURE.required_evidence_paths),
        acquisition_precision=required_events / len(read_paths) if read_paths else None,
    )


def _create_fixture(parent: Path, fixture: _PatchProposalFixture) -> ResolvedPath:
    """Materialize one fixed experiment repository through the filesystem Resource."""
    root = parent / "repository"
    for relative_path, content in fixture.files:
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
        maximum_output_tokens: int | None = None,
        fixture: _PatchProposalFixture = _BASELINE_FIXTURE,
        on_cycle_completed: Callable[[QwenReadOnlyCycle], None] | None = None,
        on_model_response: Callable[[ModelResponse], None] | None = None,
        on_grounding_correction: (
            Callable[[QwenGroundingCorrection], None] | None
        ) = None,
    ) -> None:
        """Configure the existing read-only controller and fixture root."""
        corrections: list[QwenGroundingCorrection] = []
        model_reasoning_contents: list[str | None] = []
        model_terminations: list[ModelTermination | None] = []
        model_usages: list[ModelUsage | None] = []

        def record_model_response(response: ModelResponse) -> None:
            model_reasoning_contents.append(response.reasoning_content)
            model_terminations.append(response.termination)
            model_usages.append(response.usage)
            if on_model_response is not None:
                on_model_response(response)

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
            maximum_output_tokens=maximum_output_tokens,
            on_cycle_completed=on_cycle_completed,
            on_model_response=record_model_response,
            on_final_response=on_final_response,
        )
        self._root = resolve_path(repository_root.value)
        self._fixture = fixture
        self._corrections = corrections
        self._model_reasoning_contents = model_reasoning_contents
        self._model_terminations = model_terminations
        self._model_usages = model_usages
        self._task: ConversationMessage | None = None

    async def run(self, task: ConversationMessage) -> QwenPatchProposalWorkerResult:
        """Acquire fixture facts, then validate and apply one final local patch."""
        self._task = task
        read_only_result = await self._read_only.run(task)
        final_patch = read_only_result.final_message.content
        canonical_patch = _apply_patch(self._root, final_patch, self._fixture)
        _validate_fixture_behavior(self._root, self._fixture)
        return QwenPatchProposalWorkerResult(
            task=read_only_result.task,
            cycles=read_only_result.cycles,
            grounding_corrections=tuple(self._corrections),
            final_patch=final_patch,
            canonical_patch=canonical_patch,
            terminal_newline_canonicalized=canonical_patch != final_patch,
            behavior_validated=True,
            model_reasoning_contents=tuple(self._model_reasoning_contents),
            model_terminations=tuple(self._model_terminations),
            model_usages=tuple(self._model_usages),
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
        if self._fixture.required_evidence_paths.issubset(acquired_paths):
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


def _apply_patch(
    root: ResolvedPath,
    patch: str,
    fixture: _PatchProposalFixture,
) -> str:
    """Apply one admitted fixture diff through the canonical filesystem Resource."""
    canonical_patch, replacement = _parse_patch(patch, fixture)
    target = resolve_path(fixture.target_path, base_directory=root.value)
    current = _read_text(target)
    current_text = current.content
    original_source = dict(fixture.files)[fixture.target_path]
    if current_text != original_source:
        msg = "The permitted patch cannot apply to the fixture's original source."
        raise PatchProposalError(msg)
    write(
        TextFile(
            target,
            original_source.replace("    return value.strip()", replacement),
            encoding=current.encoding,
        ),
    )
    return canonical_patch


def _parse_patch(patch: str, fixture: _PatchProposalFixture) -> tuple[str, str]:
    """Admit only the one-file, one-line diff grammar used by this fixture."""
    content = patch.removesuffix("\n")
    lines = content.split("\n")
    if tuple(lines[:5]) != _patch_prefix(fixture) or len(lines) != _PATCH_LINE_COUNT:
        msg = "Final diff must modify only the permitted fixture source hunk."
        raise PatchProposalError(msg)
    replacement = lines[5]
    if replacement not in _PERMITTED_REPLACEMENTS:
        msg = "Final diff replacement is not permitted by this fixture contract."
        raise PatchProposalError(msg)
    return f"{content}\n", replacement[1:]


def _validate_fixture_behavior(
    root: ResolvedPath,
    fixture: _PatchProposalFixture,
) -> None:
    """Execute the fixture's focused behavioral checks after host-side application."""
    target = resolve_path(fixture.target_path, base_directory=root.value)
    source = _read_text(target).content
    namespace: dict[str, object] = {}
    exec(compile(source, str(target.value), "exec"), namespace)  # noqa: S102
    normalizer = namespace.get("normalize_label")
    if not callable(normalizer) or normalizer("  Alpha  ") != "alpha":
        msg = "Applied patch does not satisfy case-insensitive trimmed normalization."
        raise PatchProposalError(msg)
    for relative_path, expected_content in fixture.files:
        if relative_path == fixture.target_path:
            continue
        content = _read_text(
            resolve_path(relative_path, base_directory=root.value),
        ).content
        if content != expected_content:
            msg = "Applied patch changed non-target fixture content."
            raise PatchProposalError(msg)


def _read_text(path: ResolvedPath) -> TextFile:
    """Read one fixture file through the Resource's explicit text representation."""
    return cast("TextFile", read(path, file_format=FileFormat.TEXT))
