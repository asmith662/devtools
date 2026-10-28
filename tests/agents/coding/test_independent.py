# Copyright (c) 2026
# ruff: noqa: D103, PLR2004, C901, PLR0915, PLR0912 -- independently specified literal outcomes
"""Complete independent engineering tasks use the same framework process as Qwen."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest

from tests.agents.coding.fixtures import (
    CHECK,
    GOOD,
    SCENARIOS,
    SOURCE,
    UNKNOWN,
    scenario,
)

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize("name", SCENARIOS)
def test_complete_framework_coding_workflow(tmp_path: Path, name: str) -> None:
    value = asyncio.run(scenario(tmp_path, name))
    successful = name in {"success", "repair", "completion-check", "two-edits"}
    assert value["accepted"] is successful
    assert value["usage"] == [None] * value["model_calls"]
    assert value["model_calls"] == value["request_count"]
    assert "src" in value["framework"]
    if successful:
        assert value["disposition"] == "validated"
        assert value["completed"] is True
        assert value["candidate_validated"] is True
        expected = (
            GOOD.replace("# \u03c0", "# changed") if name == "two-edits" else GOOD
        )
        assert value["archive"] == {"module.py": expected}
        assert value["source"] == SOURCE
        assert value["restored"] is True
        assert value["checks"][-1][0]["exit"] == 0
        assert value["checks"][-1][0]["stdout"] == "checked:7\n"
        assert value["checks"][-1][0]["argv"][-1] == CHECK
        assert value["model_calls"] == (
            3 if name in {"repair", "completion-check"} else 2
        )
        assert len(value["apply_entries"]) == (2 if name == "repair" else 1)
        if name == "repair":
            assert value["checks"][0][0]["exit"] == 1
            assert value["checks"][0][0]["passed"] is False
            assert value["feedback_ids"] == ["read-1", "edit-2", "repair-3"]
        return
    if name in {"stale", "unknown-installed", "unknown-after-check"}:
        assert value["source"] == UNKNOWN
        assert value["archive"] == {"module.py": UNKNOWN}
        assert value["reconciliation"] is True
        assert value["restored"] is False
    else:
        assert value["source"] == (GOOD if name == "restore-failed" else SOURCE)
    if name in {
        "completion-failed",
        "feedback-failed",
        "completion-raised",
        "completion-cancelled",
        "completion-overrun",
        "unknown-after-check",
        "restore-failed",
    }:
        assert value["candidate_validated"] is True
        assert value["completed"] is False
        assert value["checks"][-1][0]["exit"] == 0
    if name in {"lost-file-ack", "lost-git-ack", "primary-and-completion"}:
        assert value["original_effect_error"] is True
        assert value["apply_entries"] == ["apply"]
        assert value["archive"] == {"module.py": GOOD}
        assert value["model_calls"] == 2
        assert value["effects"][-1]["ack"] is False
        assert value["checks"] == []
    elif name not in {
        "failed-check",
        "proposal-limit",
        "unknown-installed",
        "unknown-after-check",
        "restore-failed",
        "completion-failed",
        "feedback-failed",
        "completion-raised",
        "completion-cancelled",
        "completion-overrun",
        "cancel-check",
        "lost-check-ack",
    }:
        assert value["apply_entries"] == []
    if name == "primary-and-completion":
        assert value["error"] == "OSError"
        assert value["completion_error"] == "ValueError"
    if name == "cancel-provider":
        assert value["disposition"] == "cancelled"
        assert value["failure_phase"] == "model"
        assert value["actions"] == value["proposals"] == 0
    if name in {"completion-raised", "completion-cancelled", "completion-overrun"}:
        assert value["candidate_validated"] is True
        assert value["completed"] is False
        assert value["checks"][0][0]["exit"] == 0
        assert value["model_calls"] == (3 if name == "completion-overrun" else 2)
    if name in {"cancel-check", "lost-check-ack"}:
        assert value["failure_phase"] == "validation"
        assert value["checks"][0][0]["exit"] == 0
        assert value["candidate_validated"] is False
        assert value["apply_entries"] == ["apply"]
        assert value["model_calls"] == 2
    if name in {"cancel-check", "completion-cancelled"}:
        assert value["disposition"] == "cancelled"
    if name in {
        "partial-context",
        "missing-context",
        "required-context",
        "invalid-edit",
        "unadmitted-edit",
        "overlap",
        "duplicate-arguments",
    }:
        assert value["disposition"] == "proposal_limit"
        assert value["error"] is None
    if name == "failed-check":
        assert value["checks"][0][0]["exit"] == 7
        assert value["disposition"] == "proposal_limit"
    if name == "partial-batch":
        assert value["feedback_ids"] == ["read-1"]
        assert value["effects"][0]["ack"] is True
        assert value["effects"][1]["ack"] is False
    if name in {
        "missing-id",
        "duplicate-ids",
        "foreign-model",
        "output-limit",
        "batch-overflow",
        "action-limit",
    }:
        assert value["admitted"] == []
