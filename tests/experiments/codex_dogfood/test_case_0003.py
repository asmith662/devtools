# Copyright (c) 2026
# ruff: noqa: COM812
"""Meaningful isolation and completeness guards for prospective dogfood."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

from experiments.codex_dogfood.case_0003.analyze import (
    assess_order,
    expand_judgments,
    freeze_adjudication,
    join,
    trace_observation,
)


def _frame() -> dict[str, object]:
    return {
        "snapshot_id": "snapshot",
        "resources": [["required.py", "a"], ["helpful.py", "b"], ["other.py", "c"]],
    }


def _raw() -> dict[str, object]:
    return {
        "snapshot_id": "snapshot",
        "judgments": [
            {
                "address": "required.py",
                "states": ["required_for_implementation"],
                "rationale": "Implements task",
            },
            {
                "address": "helpful.py",
                "states": ["helpful_only"],
                "rationale": "Useful explanation",
            },
        ],
        "unlisted_resources_are_unnecessary": True,
        "acceptable_alternatives": [],
        "limitations": "Synthetic",
    }


def _write(path: Path, value: object) -> None:
    path.write_text(json.dumps(value), encoding="utf-8")


def test_blind_freeze_reads_only_neutral_inputs_and_refuses_overwrite(
    tmp_path: Path,
) -> None:
    """Neutral freeze never reads poisoned retrieval or agent artifacts."""
    _write(tmp_path / "adjudication_input.json", _frame())
    _write(tmp_path / "blind_raw_judgment.json", _raw())
    _write(tmp_path / "blind_adjudicator_trace.jsonl", {"type": "turn.completed"})
    # Poison retrieval/agent evidence verifies neutral freeze never opens them.
    (tmp_path / "retrieval.json").write_text("POISON", encoding="utf-8")
    (tmp_path / "post_run.json").write_text("POISON", encoding="utf-8")
    freeze_adjudication(tmp_path)
    frozen = json.loads((tmp_path / "adjudication_frozen.json").read_text())
    assert frozen["identity_coverage"]["is_exact"]
    expected_judgments = 3
    assert len(frozen["judgments"]) == expected_judgments
    assert not frozen["provenance_joined"]
    with pytest.raises(ValueError, match="already frozen"):
        freeze_adjudication(tmp_path)


@pytest.mark.parametrize(
    "kind", ["snapshot", "duplicate", "unexpected", "missing", "conflicting"]
)
def test_blind_identity_and_obligation_guards(kind: str) -> None:
    """Reject wrong snapshots, identity errors, and mixed judgments."""
    raw = _raw()
    judgments = raw["judgments"]
    assert isinstance(judgments, list)
    if kind == "snapshot":
        raw["snapshot_id"] = "wrong"
    elif kind == "duplicate":
        judgments.append(judgments[0])
    elif kind == "unexpected":
        judgments[0]["address"] = "outside.py"
    elif kind == "missing":
        raw["unlisted_resources_are_unnecessary"] = False
    else:
        judgments[0]["states"] = ["required_for_implementation", "unnecessary"]
    with pytest.raises(ValueError, match="Blind judgment"):
        expand_judgments(_frame(), raw)


def test_incomplete_coverage_preserves_missing_required_and_prefix_scope() -> None:
    """Incomplete inventories have no complete-required-coverage depth."""
    judgments = expand_judgments(_frame(), _raw())
    incomplete = assess_order(["helpful.py", "other.py"], judgments)
    assert incomplete["last_required_rank"] is None
    assert incomplete["missing_required"] == ["required.py"]
    assert incomplete["recall"]["100"] == 0
    complete = assess_order(["helpful.py", "other.py", "required.py"], judgments)
    assert complete["last_required_rank"] == len(judgments)
    assert complete["prefix_roles"] == {
        "required": 1,
        "helpful_only": 1,
        "unnecessary": 1,
        "unresolved": 0,
    }


def test_join_requires_frozen_obligations_before_opening_retrieval(
    tmp_path: Path,
) -> None:
    """The join cannot read retrieval before freezing independent outcomes."""
    (tmp_path / "retrieval.json").write_text("POISON", encoding="utf-8")
    with pytest.raises(ValueError, match="requires frozen"):
        join(tmp_path)


def test_trace_telemetry_distinguishes_opens_searches_and_validation(
    tmp_path: Path,
) -> None:
    """Searches and validations never become inferred direct opens."""
    trace = tmp_path / "trace.jsonl"
    events = [
        {
            "type": "item.completed",
            "item": {"type": "command_execution", "command": command, "exit_code": 0},
        }
        for command in (
            "rg -n query src",
            "Get-Content -Raw required.py; Get-Content helpful.py",
            "uv run pytest tests/test_required.py",
        )
    ]
    events.append({"type": "turn.completed", "usage": {"input_tokens": 1}})
    trace.write_text("\n".join(json.dumps(item) for item in events), encoding="utf-8")
    result = trace_observation(trace, {"required.py"})
    assert result["command_count"] == len(events) - 1
    assert result["search_count"] == 1
    assert result["direct_open_resources"] == ["helpful.py", "required.py"]
    assert result["outside_frame_opens"] == ["helpful.py"]
    assert len(result["validation_commands"]) == 1
    assert result["completed"]


@pytest.mark.parametrize("encoding", ["utf-8", "utf-8-sig", "utf-16"])
def test_raw_trace_encoding_preserves_bytes_and_reports_incomplete_lines(
    tmp_path: Path,
    encoding: str,
) -> None:
    """Decode actual redirected encodings while preserving truncated telemetry."""
    trace = tmp_path / "trace.jsonl"
    content = json.dumps({"type": "turn.completed"}) + '\n{"type":'
    original = content.encode(encoding)
    trace.write_bytes(original)
    result = trace_observation(trace, set())
    assert result["completed"]
    assert result["invalid_lines"] == 1
    assert trace.read_bytes() == original


@pytest.mark.parametrize("encoding", ["utf-8", "utf-16"])
def test_blind_freeze_accepts_complete_raw_redirected_trace(
    tmp_path: Path,
    encoding: str,
) -> None:
    """Neutral freezing accepts complete UTF-8 and BOM UTF-16 agent traces."""
    _write(tmp_path / "adjudication_input.json", _frame())
    _write(tmp_path / "blind_raw_judgment.json", _raw())
    trace = tmp_path / "blind_adjudicator_trace.jsonl"
    trace.write_bytes(json.dumps({"type": "turn.completed"}).encode(encoding))
    freeze_adjudication(tmp_path)
    assert (tmp_path / "adjudication_frozen.json").exists()
