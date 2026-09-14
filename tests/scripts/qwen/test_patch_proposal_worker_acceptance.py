# Copyright (c) 2026
# ruff: noqa: INP001, SLF001
"""Deterministic reporting coverage for the B-0009 live acceptance runner."""

from __future__ import annotations

import asyncio
import importlib.util
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from devtools.agents.conversation import InteractionSource
from devtools.models.interaction import (
    ConversationRef,
    ModelResponse,
    ModelTermination,
    ModelUsage,
    Prompt,
)
from experiments.qwen.patch_proposal_worker import (
    _EXPECTED_PATCH,
    _SELECTION_STRESS_EXPECTED_PATCH,
    _SELECTION_STRESS_FIXTURE,
    create_patch_proposal_fixture,
    create_selection_stress_fixture,
    selection_stress_task,
)

if TYPE_CHECKING:
    from types import ModuleType


_SCRIPT_PATH = Path("scripts/qwen/patch_proposal_worker_acceptance.py").resolve()
_MODEL_TURN_COUNT = 6
_TOOL_ACTION_COUNT = 5
_DIRECTORY_LISTING_COUNT = 3
_FILE_READ_COUNT = 2
_UNIQUE_PATH_COUNT = 5
_CONTEXT_CAPACITY_TOKENS = 32768
_STRESS_ACTION_COUNT = 7
_STRESS_DIRECTORY_LISTING_COUNT = 3
_STRESS_FILE_READ_COUNT = 4
_STRESS_UNIQUE_PATH_COUNT = 6
_MAXIMUM_OUTPUT_TOKENS = 64


@pytest.fixture
def acceptance() -> ModuleType:
    """Load the script as a module without making scripts an installed package."""
    specification = importlib.util.spec_from_file_location(
        "test_patch_proposal_worker_acceptance",
        _SCRIPT_PATH,
    )
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


@dataclass(slots=True)
class _ScriptedInteraction:
    """Provide planned model output while exercising the actual acceptance path."""

    responses: list[str]
    calls: list[Prompt] = field(default_factory=list)
    requested_output_tokens: list[int | None] = field(default_factory=list)
    terminations: list[ModelTermination | None] | None = None
    usages: list[ModelUsage | None] | None = None
    source: InteractionSource = field(default_factory=lambda: InteractionSource("qwen"))

    async def send(
        self,
        prompt: Prompt,
        *,
        conversation: ConversationRef | None = None,
        maximum_output_tokens: int | None = None,
    ) -> ModelResponse:
        """Return one exact response without contacting a provider."""
        assert conversation is None
        self.calls.append(prompt)
        self.requested_output_tokens.append(maximum_output_tokens)
        termination = (
            self.terminations.pop(0) if self.terminations is not None else None
        )
        usage = self.usages.pop(0) if self.usages is not None else None
        return ModelResponse(
            content=self.responses.pop(0),
            source=self.source,
            termination=termination,
            usage=usage,
        )


def _proposal(action: str, path: str) -> str:
    return f'{{"action":"{action}","path":"{path}"}}'


def test_runner_parses_explicit_fixture_selection(acceptance: ModuleType) -> None:
    """The baseline remains default while the stress fixture is opt-in."""
    baseline = acceptance.parse_arguments(["--report-path", "baseline.json"])
    stress = acceptance.parse_arguments(
        ["--fixture", "selection-stress", "--report-path", "stress.json"],
    )

    assert baseline.fixture == "baseline"
    assert stress.fixture == "selection-stress"
    assert baseline.maximum_output_tokens is None
    assert stress.maximum_output_tokens is None


def test_runner_parses_explicit_experiment_output_bound(acceptance: ModuleType) -> None:
    """The live runner exposes an opt-in experiment-local output limit."""
    arguments = acceptance.parse_arguments(
        [
            "--maximum-output-tokens",
            str(_MAXIMUM_OUTPUT_TOKENS),
            "--report-path",
            "report.json",
        ],
    )

    assert arguments.maximum_output_tokens == _MAXIMUM_OUTPUT_TOKENS


def test_runner_rejects_unknown_fixture_selection(acceptance: ModuleType) -> None:
    """Only the two committed fixture choices are admitted by the CLI."""
    with pytest.raises(SystemExit):
        acceptance.parse_arguments(
            ["--fixture", "other", "--report-path", "report.json"],
        )


def test_runner_selects_committed_fixture_configuration(acceptance: ModuleType) -> None:
    """Selection composes existing fixture factories without duplicated definitions."""
    baseline = acceptance._fixture_configuration("baseline")
    stress = acceptance._fixture_configuration("selection-stress")

    assert baseline[0] is acceptance._BASELINE_FIXTURE
    assert baseline[2]().content == acceptance.coding_worker_task().content
    assert baseline[3] == _TOOL_ACTION_COUNT
    assert stress[0] is acceptance._SELECTION_STRESS_FIXTURE
    assert stress[2]().content == selection_stress_task().content
    assert stress[3] == _STRESS_ACTION_COUNT


def test_runner_reports_grounding_correction_and_repeated_refusal(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """The durable acceptance record separates grounding from patch conformance."""
    root = create_patch_proposal_fixture(tmp_path)
    report = asyncio.run(
        acceptance.run_acceptance(
            task=acceptance._live_task(),
            repository_root=root,
            interaction=_ScriptedInteraction([_EXPECTED_PATCH, _EXPECTED_PATCH]),
        ),
    )

    outcome = acceptance.B0009LiveOutcome(
        report=report,
        persistent_service_status="READY",
        persistent_service_error_type=None,
        persistent_service_error_message=None,
        fixture_cleanup_succeeded=True,
    )
    payload = acceptance._report_payload(outcome)

    assert report.failure_category == "UNGROUNDED_FINAL_RESPONSE"
    assert report.execution_actions == ()
    assert len(report.grounding_corrections) == 1
    assert payload["grounding"]["acquired_read_paths"] == []
    assert payload["fixture"]["id"] == "baseline"
    assert payload["grounding"]["corrections"][0]["acquired_paths"] == []
    assert payload["failure"]["category"] == "UNGROUNDED_FINAL_RESPONSE"


def test_runner_distinguishes_raw_eof_patch_from_canonical_fixture_patch(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """Reporting retains raw model text while exposing accepted canonicalization."""
    root = create_patch_proposal_fixture(tmp_path)
    raw_patch = _EXPECTED_PATCH.removesuffix("\n")
    report = asyncio.run(
        acceptance.run_acceptance(
            task=acceptance._live_task(),
            repository_root=root,
            interaction=_ScriptedInteraction(
                [
                    _proposal("list_repository_directory", "."),
                    _proposal("list_repository_directory", "src"),
                    _proposal("read_repository_file", "src/label.py"),
                    _proposal("list_repository_directory", "tests"),
                    _proposal("read_repository_file", "tests/test_label.py"),
                    raw_patch,
                ],
            ),
        ),
    )
    outcome = acceptance.B0009LiveOutcome(
        report=report,
        persistent_service_status="READY",
        persistent_service_error_type=None,
        persistent_service_error_message=None,
        fixture_cleanup_succeeded=True,
    )
    payload = acceptance._report_payload(outcome)

    assert report.result is not None
    assert payload["final_model_response"] == raw_patch
    assert payload["canonical_accepted_patch"] == _EXPECTED_PATCH
    assert payload["patch_evaluation"]["terminal_newline_canonicalized"] is True


def test_runner_reports_per_turn_and_complete_cumulative_model_usage(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """Reported usage is retained per turn and summed only when complete."""
    root = create_patch_proposal_fixture(tmp_path)
    usages: list[ModelUsage | None] = [
        ModelUsage(input_tokens=10, output_tokens=2, total_tokens=12),
        ModelUsage(input_tokens=11, output_tokens=3, total_tokens=20),
        ModelUsage(input_tokens=12, output_tokens=4, total_tokens=16),
        ModelUsage(input_tokens=13, output_tokens=5, total_tokens=18),
        ModelUsage(input_tokens=14, output_tokens=6, total_tokens=20),
        ModelUsage(input_tokens=15, output_tokens=7, total_tokens=22),
    ]
    terminations: list[ModelTermination | None] = [
        ModelTermination.NORMAL_STOP,
        ModelTermination.NORMAL_STOP,
        ModelTermination.NORMAL_STOP,
        ModelTermination.NORMAL_STOP,
        ModelTermination.NORMAL_STOP,
        ModelTermination.NORMAL_STOP,
    ]
    report = asyncio.run(
        acceptance.run_acceptance(
            task=acceptance._live_task(),
            repository_root=root,
            interaction=_ScriptedInteraction(
                [
                    _proposal("list_repository_directory", "."),
                    _proposal("list_repository_directory", "src"),
                    _proposal("read_repository_file", "src/label.py"),
                    _proposal("list_repository_directory", "tests"),
                    _proposal("read_repository_file", "tests/test_label.py"),
                    _EXPECTED_PATCH,
                ],
                terminations=terminations,
                usages=usages,
            ),
        ),
    )
    outcome = acceptance.B0009LiveOutcome(
        report=report,
        persistent_service_status="READY",
        persistent_service_error_type=None,
        persistent_service_error_message=None,
        fixture_cleanup_succeeded=True,
    )

    payload = acceptance._report_payload(outcome)
    measurements = payload["measurements"]

    assert payload["schema"] == "qwen-b0009-live-acceptance/3"
    assert measurements["model_turn_count"] == _MODEL_TURN_COUNT
    assert measurements["model_usage_by_turn"][0] == {
        "input_tokens": 10,
        "output_tokens": 2,
        "total_tokens": 12,
        "input_context_utilization": 10 / 32768,
    }
    assert measurements["model_termination_by_turn"] == ["normal_stop"] * 6
    assert measurements["cumulative_reported_model_usage"] == {
        "input_tokens": 75,
        "input_tokens_reported_turns": _MODEL_TURN_COUNT,
        "output_tokens": 27,
        "output_tokens_reported_turns": _MODEL_TURN_COUNT,
        "total_tokens": 108,
        "total_tokens_reported_turns": _MODEL_TURN_COUNT,
    }
    assert measurements["tool_action_budget"] == _TOOL_ACTION_COUNT
    assert measurements["tool_action_budget_used"] == _TOOL_ACTION_COUNT
    assert measurements["directory_listing_count"] == _DIRECTORY_LISTING_COUNT
    assert measurements["file_read_count"] == _FILE_READ_COUNT
    assert measurements["unique_path_count"] == _UNIQUE_PATH_COUNT
    assert measurements["repeated_path_count"] == 0
    assert measurements["repository_projection_characters"] > 0
    assert measurements["run_duration_seconds"] == 0
    assert measurements["selection"] is None


def test_runner_retains_and_forwards_its_experiment_local_output_bound(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """The runner reports a configured cap and sends it on every model turn."""
    interaction = _ScriptedInteraction(
        [
            _proposal("list_repository_directory", "."),
            _proposal("list_repository_directory", "src"),
            _proposal("read_repository_file", "src/label.py"),
            _proposal("list_repository_directory", "tests"),
            _proposal("read_repository_file", "tests/test_label.py"),
            _EXPECTED_PATCH,
        ],
    )
    report = asyncio.run(
        acceptance.run_acceptance(
            task=acceptance._live_task(),
            repository_root=create_patch_proposal_fixture(tmp_path),
            interaction=interaction,
            maximum_output_tokens=_MAXIMUM_OUTPUT_TOKENS,
        ),
    )
    outcome = acceptance.B0009LiveOutcome(
        report=report,
        persistent_service_status="READY",
        persistent_service_error_type=None,
        persistent_service_error_message=None,
        fixture_cleanup_succeeded=True,
    )

    assert interaction.requested_output_tokens == [_MAXIMUM_OUTPUT_TOKENS] * len(
        interaction.calls,
    )
    assert (
        acceptance._report_payload(outcome)["fixture"]["maximum_output_tokens"]
        == _MAXIMUM_OUTPUT_TOKENS
    )


def test_runner_reports_selection_stress_measurements_and_context_utilization(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """The stress artifact retains local relevance facts without generic metrics."""
    root = create_selection_stress_fixture(tmp_path)
    usages: list[ModelUsage | None] = [
        ModelUsage(input_tokens=32768, output_tokens=1, total_tokens=32769),
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ]
    report = asyncio.run(
        acceptance.run_acceptance(
            task=selection_stress_task(),
            repository_root=root,
            interaction=_ScriptedInteraction(
                [
                    _proposal("list_repository_directory", "."),
                    _proposal("list_repository_directory", "src"),
                    _proposal("read_repository_file", "src/display_labels.py"),
                    _proposal("read_repository_file", "src/labels.py"),
                    _proposal("list_repository_directory", "tests"),
                    _proposal("read_repository_file", "src/labels.py"),
                    _proposal("read_repository_file", "tests/test_labels.py"),
                    _SELECTION_STRESS_EXPECTED_PATCH,
                ],
                usages=usages,
            ),
            fixture=_SELECTION_STRESS_FIXTURE,
            maximum_actions=7,
        ),
    )
    outcome = acceptance.B0009LiveOutcome(
        report=report,
        persistent_service_status="READY",
        persistent_service_error_type=None,
        persistent_service_error_message=None,
        fixture_cleanup_succeeded=True,
    )

    measurements = acceptance._report_payload(outcome)["measurements"]

    assert measurements["model_context_capacity_tokens"] == _CONTEXT_CAPACITY_TOKENS
    assert measurements["model_usage_by_turn"][0]["input_context_utilization"] == 1
    assert measurements["model_usage_by_turn"][1] is None
    assert measurements["cumulative_reported_model_usage"]["input_tokens"] is None
    assert measurements["tool_action_budget"] == _STRESS_ACTION_COUNT
    assert measurements["tool_action_budget_used"] == _STRESS_ACTION_COUNT
    assert measurements["directory_listing_count"] == _STRESS_DIRECTORY_LISTING_COUNT
    assert measurements["file_read_count"] == _STRESS_FILE_READ_COUNT
    assert measurements["unique_path_count"] == _STRESS_UNIQUE_PATH_COUNT
    assert measurements["repeated_path_count"] == 1
    assert measurements["selection"] == {
        "required_files_read": ["src/labels.py", "tests/test_labels.py"],
        "plausible_unnecessary_files_read": ["src/display_labels.py"],
        "clearly_irrelevant_files_read": [],
        "required_read_coverage": 1,
        "acquisition_precision": 3 / 4,
    }
    assert acceptance._report_payload(outcome)["fixture"]["id"] == "selection-stress"


def test_runner_leaves_incomplete_reported_usage_unknown(
    acceptance: ModuleType,
) -> None:
    """A missing turn count prevents a fabricated cumulative model total."""
    payload = acceptance._cumulative_usage_payload(
        (ModelUsage(input_tokens=8, output_tokens=4, total_tokens=12), None),
    )

    assert payload == {
        "input_tokens": None,
        "input_tokens_reported_turns": 1,
        "output_tokens": None,
        "output_tokens_reported_turns": 1,
        "total_tokens": None,
        "total_tokens_reported_turns": 1,
    }
