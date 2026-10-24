# Copyright (c) 2026
# ruff: noqa: PLR2004, COM812 -- bounded pilot fixtures
"""Read-only projection of real record contracts, without providers or authority."""

from __future__ import annotations

import hashlib
import json
from typing import TYPE_CHECKING

from apps.operator_dashboard.project import project
from scripts.backlog.intake import Intake, _digest

if TYPE_CHECKING:
    from pathlib import Path


def _put(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def test_real_contract_projection_and_unchanged_sources(tmp_path: Path) -> None:
    """Keep review, legacy backlog, worker acceptance and unknown usage separate."""
    backlog = tmp_path / "docs/backlog"
    backlog.mkdir(parents=True)
    (backlog / "overview.md").write_text("# Backlog\n", encoding="utf-8")
    intake = Intake(tmp_path, coordinator=tmp_path)  # isolated synthetic host
    identity = intake.capture(
        {
            "kind": "investigation",
            "title": "Example pending issue",
            "summary": "Example",
            "benefit": "Example",
            "uncertainty": "Unreviewed",
            "discovery": {"kind": "human", "reference": "fixture"},
            "parent": None,
            "resources": ["src/example.py"],
            "evidence": ["fixture"],
            "dependencies": [],
        }
    )
    item = backlog / "items/B-0010-example.md"
    item.parent.mkdir()
    item.write_text("# B-0010 Example\n- status: BACKLOG\n", encoding="utf-8")
    result_path = tmp_path / ".local/qwen-coding-worker/run-01/result.json"
    _put(
        result_path,
        {
            "schema": "qwen-coding-loop-v2",
            "accepted": True,
            "disposition": "ACCEPTED",
            "model_calls_attempted": 2,
            "repair_cycles": 1,
            "usage_totals": {"input_tokens": 100, "output_tokens": 20},
            "turns": [
                {"validation": {"oracle": {"exit_code": 0}, "tests": {"exit_code": 0}}}
            ],
            "private_prompt": "DO NOT DISCLOSE",
            "credentials": "SECRET",
        },
    )
    before = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    result = project(tmp_path)
    assert result["proposals"][0]["id"] == identity
    assert result["proposals"][0]["state"] == "PENDING_REVIEW"
    assert result["backlog"][0]["status"] == "BACKLOG"
    assert result["work"] == []
    worker = result["workers"][0]
    assert worker["model_calls"] == 2
    assert worker["usage"]["cached_input_tokens"] is None
    assert worker["usage"]["reasoning_tokens"] is None
    assert worker["validation"] == {"tests": 0, "oracle": 0}
    assert (
        worker["reference"]["sha256"] == hashlib.sha256(before[result_path]).hexdigest()
    )
    assert "DO NOT DISCLOSE" not in json.dumps(result)
    assert "SECRET" not in json.dumps(result)
    assert before == {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}


def test_missing_partial_and_corrupt_records(tmp_path: Path) -> None:
    """Incomplete evidence is visible; missing consumption never becomes zero."""
    backlog = tmp_path / "docs/backlog"
    backlog.mkdir(parents=True)
    (backlog / "overview.md").write_text("# Backlog", encoding="utf-8")
    _put(backlog / "proposals/bad/proposal.json", {})
    _put(tmp_path / ".local/backlog/work/B-0011/assignment.json", {})
    _put(
        tmp_path / ".local/qwen-coding-worker/bad/result.json",
        {"schema": "unsupported"},
    )
    _put(
        tmp_path / ".local/qwen-coding-worker/partial/result.json",
        {"schema": "qwen-coding-loop-v2"},
    )
    result = project(tmp_path)
    assert len(result["errors"]) == 3
    assert result["workers"][0]["disposition"] == "UNKNOWN"
    assert result["workers"][0]["model_calls"] is None
    assert result["workers"][0]["usage"]["input_tokens"] is None


def test_canonical_work_status_and_receipt_authentication(tmp_path: Path) -> None:
    """Project review/escalation/uncertainty without turning grants into authority."""
    backlog = tmp_path / "docs/backlog"
    backlog.mkdir(parents=True)
    (backlog / "overview.md").write_text("# Backlog", encoding="utf-8")
    folders = tmp_path / ".local/backlog/work"
    for index, disposition in enumerate(
        ["REVIEW_CANDIDATE", "ESCALATION_REQUIRED", None],
        1,
    ):
        folder = folders / f"B-{index:04d}"
        value = {"schema": "backlog-qwen-assignment-v1"}
        _put(folder / "assignment.json", {**value, "sha256": _digest(value)})
        if disposition:
            value = {"schema": "backlog-qwen-result-v1", "disposition": disposition}
            _put(folder / "result.json", {**value, "sha256": _digest(value)})
        else:
            _put(folder / "dispatch.json", {})
        _put(folder / "authorization.json", {"note": "not current authority"})
    result = project(tmp_path)
    assert [v["disposition"] for v in result["work"]] == [
        "REVIEW_CANDIDATE",
        "ESCALATION_REQUIRED",
        "RECONCILIATION_REQUIRED",
    ]
    assert all(v["grant_record_present"] for v in result["work"])
    _put(
        folders / "B-0001/result.json",
        {"schema": "backlog-qwen-result-v1", "sha256": "bad"},
    )
    result = project(tmp_path)
    assert len(result["work"]) == 2
    assert "mismatch" in result["errors"][0]["error"]
