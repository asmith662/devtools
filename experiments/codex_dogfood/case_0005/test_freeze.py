# Copyright (c) 2026
# ruff: noqa: ANN001, ANN002, ANN003, ANN201, ANN202, COM812, EM101, INP001, PLR2004, S101, TRY003
"""Validate the protocol without executing acquisition or routing."""

from __future__ import annotations

import asyncio
import importlib.util
import json
from pathlib import Path

import pytest

from devtools.context.localization import lexical
from devtools.context.localization.routing import derive

CASE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("case0005_freeze", CASE / "freeze.py")
assert SPEC is not None
assert SPEC.loader is not None
freeze = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(freeze)


def forbidden(*_args, **_kwargs):
    """Fail if a static protocol check crosses the execution boundary."""
    raise AssertionError("Retrieval/routing must not execute during Stage A.")


def test_native_freeze_without_execution(monkeypatch):
    """Validate complete native binding while execution APIs are disabled."""
    monkeypatch.setattr(lexical, "acquire_localization_lexical_evidence", forbidden)
    monkeypatch.setattr(
        lexical, "retrieve_repository_text_documents_by_bm25", forbidden
    )
    monkeypatch.setattr(derive, "route_localization_lexical_evidence", forbidden)
    result = freeze.validate()
    assert result["resources"] > 0
    assert result["obligations"] == result["queries"] == result["preferences"] == 9
    assert result["retrieval_executed"] is result["routing_executed"] is False


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("src/devtools/context/localization/kernel.py", True),
        ("tests/context/test_kernel.py", True),
        ("docs/development/validation.md", True),
        ("scripts/validate_development.py", True),
        ("pyproject.toml", True),
        ("docs/implementation_ledger.md", False),
        ("tests/experiments/test_capture.py", False),
        ("experiments/codex_dogfood/case_0004/analysis.json", False),
        ("src/devtools/__pycache__/cache.py", False),
        ("scripts/other.py", False),
        (".local/outcome.md", False),
    ],
)
def test_frame_selection(path, expected):
    """Only declared areas/types/exceptions enter the committed frame."""
    assert freeze.eligible(path) is expected


def test_empty_preference_and_no_gold():
    """Caller contracts retain empty validation routing and unknown witnesses."""
    treatment = json.loads(freeze.binary(CASE / "treatment.json"))
    task, queries, preferences = freeze.task_inputs(treatment)
    assert all(not obligation.witness_alternatives for obligation in task.obligations)
    assert preferences[-1].preferred_roles == ()
    assert preferences[-1].query == queries[-1].identity
    assert queries[-1].obligation == task.obligations[-1].identity


def test_artifact_tamper_rejected(monkeypatch):
    """A modified frozen treatment cannot pass the digest gate."""
    original = freeze.binary

    def changed(path):
        data = original(path)
        return data + b" " if path.name == "treatment.json" else data

    monkeypatch.setattr(freeze, "binary", changed)
    with pytest.raises(ValueError, match="Frozen artifact changed"):
        freeze.validate()


def test_refuse_second_freeze():
    """The retained checkpoint cannot be silently regenerated."""
    with pytest.raises(FileExistsError, match="never overwrite"):
        asyncio.run(freeze.freeze())
