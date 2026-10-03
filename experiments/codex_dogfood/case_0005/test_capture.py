# Copyright (c) 2026
# ruff: noqa: ANN001, ANN002, ANN003, ANN201, ANN202, COM812, EM101, INP001, PLR2004, S101, TRY003
"""Read-only checks of the frozen Stage B capture and overwrite barrier."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

CASE = Path(__file__).resolve().parent
sys.path.insert(0, str(CASE))
SPEC = importlib.util.spec_from_file_location(
    "case0005_capture_test", CASE / "capture.py"
)
assert SPEC is not None
assert SPEC.loader is not None
capture = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(capture)


def forbidden(*_args, **_kwargs):
    """Guard production execution during every read-only test."""
    raise AssertionError("Stage B execution must not repeat.")


def test_read_only_correspondence(monkeypatch):
    """All saved native/routed data correspond without rerunning either call."""
    monkeypatch.setattr(capture, "acquire_localization_lexical_evidence", forbidden)
    monkeypatch.setattr(capture, "route_localization_lexical_evidence", forbidden)
    result = capture.verify_outputs()
    assert result["resources"] == 515
    assert result["lexical_lanes"] == 10
    assert result["routed_lanes"] == 9
    assert result["acquisition_invocations"] == 1
    assert result["routing_invocations"] == 1


def test_capture_refuses_overwrite_before_production_calls(monkeypatch):
    """A second invocation stops at the initial output-existence gate."""
    monkeypatch.setattr(capture, "acquire_localization_lexical_evidence", forbidden)
    monkeypatch.setattr(capture, "route_localization_lexical_evidence", forbidden)
    before = {
        path.name: capture.freeze.sha(capture.freeze.binary(path))
        for path in capture.OUTPUTS
    }
    with pytest.raises(FileExistsError, match="single-use"):
        capture.capture()
    after = {
        path.name: capture.freeze.sha(capture.freeze.binary(path))
        for path in capture.OUTPUTS
    }
    assert before == after


def test_corrupt_routing_serialization_rejected(monkeypatch):
    """Even parseable extra bytes fail canonical read-only correspondence."""
    original = capture.freeze.binary

    def changed(path):
        data = original(path)
        return data + b" " if path == capture.ROUTING else data

    monkeypatch.setattr(capture.freeze, "binary", changed)
    with pytest.raises(ValueError, match="Serialized Stage B output differs"):
        capture.verify_outputs()


def test_json_checkout_line_endings_do_not_change_committed_digest(monkeypatch):
    """Read-only verification binds canonical committed JSON on Windows."""
    original = capture.freeze.binary

    def checked_out(path):
        data = original(path)
        return (
            data.replace(b"\n", b"\r\n")
            if path in (capture.RETRIEVAL, capture.ROUTING)
            else data
        )

    monkeypatch.setattr(capture.freeze, "binary", checked_out)
    assert capture.verify_outputs()["lexical_lanes"] == 10


def test_global_lane_unrouted_and_validation_preference_empty():
    """Serialization retains the native global control and empty role policy."""
    retrieval = json.loads(capture.freeze.binary(capture.RETRIEVAL))
    routing = json.loads(capture.freeze.binary(capture.ROUTING))
    assert routing["global_lane_routed"] is False
    assert retrieval["lanes"][0]["query_identity"] == "global-full-task"
    assert routing["lanes"][-1]["query_identity"] == "q-validation"
    assert routing["lanes"][-1]["preferred_roles"] == []
    assert routing["lanes"][-1]["preferred_count"] == 0
    assert (
        routing["lanes"][-1]["escape_count"]
        == routing["lanes"][-1]["native_result_count"]
    )
