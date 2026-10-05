# Copyright (c) 2026
# ruff: noqa: D103, PLR2004, S101, COM812, TC003
"""Exercise only the Stage B durability guard without treatment operations."""

from __future__ import annotations

import gzip
import pickle
from pathlib import Path

import pytest

from experiments.codex_dogfood.case_0007 import capture


def test_stage_a_archive_is_loaded_without_rebuilding_or_running_treatment() -> None:
    manifest, inputs = capture.verify_stage_a(initial=False)

    assert manifest["frame_resource_count"] == 521
    assert len(inputs["lexical_request"].snapshot.resources) == 521
    assert len(inputs["reference_request"].sources) == 407
    assert len(inputs["grounding_requests"]) == 9
    assert len(inputs["recipe_specifications"]) == 25


def test_raw_checkpoint_round_trips_and_rejects_foreign_stage_a(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    raw = tmp_path / "stage_b_raw.pkl.gz"
    monkeypatch.setattr(capture, "RAW", raw)
    monkeypatch.setattr(capture, "RAW_RECEIPT", tmp_path / "stage_b_raw.sha256")
    state = {
        "stage_a_commit": capture.STAGE_A_COMMIT,
        "state": "PARTIAL_RAW_CAPTURE",
        "completed": ["lexical"],
    }

    capture.save_raw(state)
    loaded = capture.load_raw()

    assert loaded["completed"] == ["lexical"]
    foreign = gzip.compress(
        pickle.dumps({"stage_a_commit": "foreign"}, protocol=5), mtime=0
    )
    raw.write_bytes(foreign)
    capture.RAW_RECEIPT.write_text(f"{capture.digest(foreign)}\n", encoding="ascii")
    with pytest.raises(ValueError, match="different Stage A"):
        capture.load_raw()


def test_canonical_exclusive_write_refuses_overwrite(
    tmp_path: Path,
) -> None:
    target = tmp_path / "artifact.json"
    capture.exclusive_atomic(target, b"first", replace=False)

    with pytest.raises(FileExistsError):
        capture.exclusive_atomic(target, b"second", replace=False)

    assert target.read_bytes() == b"first"


def test_completed_operation_is_reused_without_calling_its_function() -> None:
    state = {"completed": ["generation"], "invocations": {"generation": 1}}

    capture.operation(
        state,
        "generation",
        lambda: (_ for _ in ()).throw(AssertionError("must not execute")),
    )

    assert state["invocations"] == {"generation": 1}
