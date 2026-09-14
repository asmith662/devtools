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
from devtools.models.interaction import ConversationRef, ModelResponse, Prompt
from experiments.qwen.patch_proposal_worker import (
    _EXPECTED_PATCH,
    create_patch_proposal_fixture,
)

if TYPE_CHECKING:
    from types import ModuleType


_SCRIPT_PATH = Path("scripts/qwen/patch_proposal_worker_acceptance.py").resolve()


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
    source: InteractionSource = field(default_factory=lambda: InteractionSource("qwen"))

    async def send(
        self,
        prompt: Prompt,
        *,
        conversation: ConversationRef | None = None,
    ) -> ModelResponse:
        """Return one exact response without contacting a provider."""
        assert conversation is None
        self.calls.append(prompt)
        return ModelResponse(content=self.responses.pop(0), source=self.source)


def _proposal(action: str, path: str) -> str:
    return f'{{"action":"{action}","path":"{path}"}}'


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
