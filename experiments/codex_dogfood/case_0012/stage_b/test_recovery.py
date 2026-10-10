# Copyright (c) 2026
# ruff: noqa: COM812, D103, S101, EM101, TRY003, ANN401, PLR2004 -- bounded recovery fixtures
"""Native returns survive Windows summary replacement failure without rerun."""

from __future__ import annotations

import copy
import ctypes
import json
import sys
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

import pytest

from experiments.codex_dogfood.case_0009.artifacts import binary, json_bytes
from experiments.codex_dogfood.case_0012.stage_b import audit, durability, graph
from experiments.codex_dogfood.case_0012.stage_b.durability import Journal


def test_append_only_chain_and_alias_roundtrip(tmp_path: Path) -> None:
    j = Journal.start(tmp_path, {"execution": "fixture"})
    shared = {"native": [1, "x"]}
    j.context({"frame": shared})
    j.call("parent", {}, lambda: (j.call("child", {}, lambda: shared), shared))
    loaded = Journal.load(tmp_path)
    loaded.ready()
    assert loaded.state["state"] != "NATIVE_CAPTURE_COMPLETE"
    j.complete()
    assert Journal.load(tmp_path).state["state"] == "NATIVE_CAPTURE_COMPLETE"
    assert loaded.events == 4
    assert loaded.state["values"]["child"] is loaded.state["values"]["frame"]
    assert loaded.state["values"]["parent"][0] is loaded.state["values"]["child"]
    assert graph.describe(shared) == graph.describe(copy.deepcopy(shared))
    with pytest.raises(FileExistsError):
        durability.exclusive(tmp_path / "operations/000001.entered.json", {})
    with pytest.raises(ValueError, match="cannot invoke"):
        loaded.call("new", {}, lambda: None)


def test_summary_failure_is_recoverable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    j = Journal.start(tmp_path, {"execution": "fixture"})
    j.context({})
    count = []
    original = durability.atomic

    def fail(*_args: Any) -> None:
        raise PermissionError("Windows replacement failure fixture")

    monkeypatch.setattr(durability, "atomic", fail)

    def native() -> dict[str, int]:
        count.append(1)
        return {"native": 42}

    assert j.call("one", {}, native) == {"native": 42}
    restored = Journal.load(tmp_path)
    restored.ready()
    assert restored.state["values"]["one"] == {"native": 42}
    assert len(count) == 1
    monkeypatch.setattr(durability, "atomic", original)
    restored.save()
    assert json.loads(binary(tmp_path / "raw_checkpoint.json"))["journal_events"] == 2
    assert Journal.load(tmp_path).state == restored.state


@pytest.mark.skipif(
    sys.platform != "win32", reason="Native Windows handle-sharing boundary"
)
def test_windows_locked_summary_keeps_return(tmp_path: Path) -> None:
    j = Journal.start(tmp_path, {"execution": "windows-fixture"})
    j.context({})
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    create = kernel.CreateFileW
    create.argtypes = [
        ctypes.c_wchar_p,
        ctypes.c_uint32,
        ctypes.c_uint32,
        ctypes.c_void_p,
        ctypes.c_uint32,
        ctypes.c_uint32,
        ctypes.c_void_p,
    ]
    create.restype = ctypes.c_void_p
    kernel.CloseHandle.argtypes = [ctypes.c_void_p]
    handle = create(
        str(tmp_path / "raw_checkpoint.json"), 0x80000000, 1, None, 3, 0, None
    )
    assert handle not in (None, ctypes.c_void_p(-1).value)
    count = []

    def native() -> str:
        count.append(1)
        return "native-return"

    try:
        assert j.call("one", {}, native) == "native-return"
        assert (tmp_path / "summary_failure_000001.json").exists()
        restored = Journal.load(tmp_path)
        restored.ready()
        assert restored.state["values"]["one"] == "native-return"
        assert len(count) == 1
    finally:
        kernel.CloseHandle(handle)
    restored.save()
    assert Journal.load(tmp_path).state["values"]["one"] == "native-return"


def test_entered_no_return_never_inferred(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    j = Journal.start(tmp_path, {"execution": "fixture"})
    j.context({})
    original = j.event

    def event(sequence: int, status: str, payload: dict[str, Any]) -> None:
        if status == "RETURNED":
            raise OSError("immutable return publication lost")
        original(sequence, status, payload)

    monkeypatch.setattr(j, "event", event)
    with pytest.raises(OSError, match="publication lost"):
        j.call("one", {}, lambda: 12)
    with pytest.raises(ValueError, match="Unrecoverable"):
        Journal.load(tmp_path).ready()
    assert "one" not in Journal.load(tmp_path).state["values"]


def test_chain_tamper_and_distinct_attempts(tmp_path: Path) -> None:
    for n in (1, 2):
        j = Journal.start(tmp_path / str(n), {"execution": f"fixture-{n}"})
        j.call("same-operation", {}, lambda: "same-native-value")
    first, second = (Journal.load(tmp_path / str(n)) for n in (1, 2))
    assert first.state["marker"] != second.state["marker"]
    assert sum(len(j.state["operations"]) for j in (first, second)) == 2
    p = tmp_path / "2/operations/000001.returned.json"
    value = json.loads(binary(p))
    value["prior_chain_sha256"] = "tamper"
    p.write_bytes(json_bytes(value))
    with pytest.raises(ValueError, match="chain"):
        Journal.load(tmp_path / "2")


def test_failed_attempt_is_audit_only() -> None:
    old = audit.authenticate()
    assert old["operations"][-1]["status"] == "ENTERED"
    assert "lexical:materialization" not in old["values"]
    assert len({o["identity"] for o in old["operations"]}) == 6
    with pytest.raises(ValueError, match="complete independent"):
        audit.overlap(old)


def test_actual_retained_native_types_roundtrip_without_production_calls(
    tmp_path: Path,
) -> None:
    old = audit.authenticate()["values"]
    j = Journal.start(tmp_path, {"execution": "serialization-fixture"})
    j.context({"frame": old["frame"]})
    for key in (
        "index-build",
        "lexical:global",
        "lexical:source",
        "lexical:choices",
        "lexical:integrity",
    ):
        # Returning an already-retained object tests serialization only; no RI call.
        def retained(key: str = key) -> object:
            return old[key]

        j.call("fixture:" + key, {}, retained)
    loaded = Journal.load(tmp_path)
    loaded.ready()
    for key in (
        "lexical:global",
        "lexical:source",
        "lexical:choices",
        "lexical:integrity",
    ):
        assert audit.lexical_identity(old[key]) == audit.lexical_identity(
            loaded.state["values"]["fixture:" + key]
        )
        assert (
            loaded.state["values"]["fixture:" + key].index
            is loaded.state["values"]["fixture:index-build"]
        )
