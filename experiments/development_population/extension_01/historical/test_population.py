# Copyright (c) 2026
# ruff: noqa: ANN401, D103, S101, PLR2004, COM812 -- bounded protocol fixtures
"""Population determinism and holdout-leakage fixtures; no retrieval or patches."""

from __future__ import annotations

import copy
import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

import pytest

from experiments.codex_dogfood.case_0009.artifacts import json_bytes

from . import builder as b


def test_complete_inputs_and_order_invariance() -> None:
    value = b.inputs()
    assert len(value["rows"]) == 122
    assert sum(r["reason"] == "ELIGIBLE" for r in value["rows"]) == 15
    files = b.expected(value)
    reversed_value = copy.deepcopy(value)
    reversed_value["rows"].reverse()
    assert b.expected(reversed_value) == files
    freeze = json.loads(files["population_freeze.json"])
    assert len(freeze["selected_development_tasks"]) == 15
    assert freeze["next_case_id"] == "historical-development-001"
    assert (
        json.loads(files["selected_next_case.json"])
        == freeze["selected_development_tasks"][0]
    )
    assert (
        freeze["selected_development_tasks"][0]["frame"]["native_repository_snapshot"]
        == "NOT_CONSTRUCTED"
    )


@pytest.mark.parametrize(
    "field", ["parents", "child", "task_text", "body_sha256", "reason", "diff_sha256"]
)
def test_input_tamper_rejects(
    field: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    value = b.inputs()
    changed = copy.deepcopy(value)
    changed["rows"][0][field] = "altered"
    path = tmp_path / "input.json"
    path.write_bytes(json_bytes(changed))
    monkeypatch.setattr(b, "INPUT", path)
    with pytest.raises(ValueError, match="receipt differs"):
        b.inputs()


@pytest.mark.parametrize(
    "field", ["changed_paths", "diff", "child_commit", "target_symbols"]
)
def test_public_leak_rejects(field: str) -> None:
    files = b.expected(b.inputs())
    freeze = json.loads(files["population_freeze.json"])
    freeze["selected_development_tasks"][0][field] = "leak"
    files["population_freeze.json"] = json_bytes(freeze)
    files["selected_next_case.json"] = json_bytes(
        freeze["selected_development_tasks"][0]
    )
    with pytest.raises(ValueError, match="leakage"):
        b.validate_files(files)


def test_membership_and_next_case_rejects() -> None:
    files = b.expected(b.inputs())
    task = json.loads(files["selected_next_case.json"])
    task["case_id"] = "foreign"
    files["selected_next_case.json"] = json_bytes(task)
    with pytest.raises(ValueError, match="next case"):
        b.validate_files(files)


def test_task_source_hash_rejects() -> None:
    files = b.expected(b.inputs())
    freeze = json.loads(files["population_freeze.json"])
    card = freeze["selected_development_tasks"][0]
    card["task_source"]["task_sha256"] = "0" * 64
    files["population_freeze.json"] = json_bytes(freeze)
    files["selected_next_case.json"] = json_bytes(card)
    with pytest.raises(ValueError, match="hash differs"):
        b.validate_files(files)


def test_existing_publication_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "selected_next_case.json").write_bytes(b"existing")
    monkeypatch.setattr(b, "PACKAGE", tmp_path)
    original = b.inputs()
    monkeypatch.setattr(b, "inputs", lambda: original)
    monkeypatch.setattr(b, "source_hashes", dict)

    async def authenticated(_value: Any) -> None:
        return None

    monkeypatch.setattr(b, "authenticate_git", authenticated)
    with pytest.raises(FileExistsError, match="overwrite refused"):
        b.publish()
    assert (tmp_path / "selected_next_case.json").read_bytes() == b"existing"


@pytest.mark.parametrize("kind", ["seed", "order", "membership", "holdout_digest"])
def test_output_mutations_reject(kind: str) -> None:
    files = b.expected(b.inputs())
    changed = dict(files)
    if kind == "seed":
        name = "selection_provenance.json"
        value = json.loads(files[name])
        value["seed_sha256"] = "0" * 64
    elif kind == "holdout_digest":
        name = "holdout/reference_implementations.json"
        value = json.loads(files[name])
        value["reference_implementations"][0]["diff_sha256"] = "0" * 64
    else:
        name = "population_freeze.json"
        value = json.loads(files[name])
        if kind == "order":
            value["selected_development_tasks"].reverse()
        else:
            value["selected_development_tasks"].pop()
    changed[name] = json_bytes(value)
    with pytest.raises(ValueError, match="artifact differs"):
        b.compare(files, changed)


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("production_files", 0),
        ("production_files", 11),
        ("total_files", 25),
        ("lines", 2001),
        ("binary_production_test", True),
        ("parents", ["one", "two"]),
    ],
)
def test_eligible_bounds_reject(field: str, replacement: Any) -> None:
    value = copy.deepcopy(b.inputs())
    row = next(r for r in value["rows"] if r["reason"] == "ELIGIBLE")
    row[field] = replacement
    with pytest.raises(ValueError, match="Eligibility"):
        b.expected(value)


def test_audit_identity_rejects(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(b, "AUDIT_HASHES", {})
    with pytest.raises(ValueError, match="audit differs"):
        b.supporting_inputs()


def test_previous_task_identity_rejects(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(b, "PRIOR_TASK_SHA", "0" * 64)
    with pytest.raises(ValueError, match="receipt differs"):
        b.supporting_inputs()
