# Copyright (c) 2026
# ruff: noqa: COM812, S101, D103, EM101, TRY003 -- bounded controlled contract tests
"""Durability, no-rerun recovery, canonical identities and blind boundaries."""

from __future__ import annotations

import ast
import copy
import json
from typing import TYPE_CHECKING

import pytest

from experiments.codex_dogfood.case_0009.artifacts import (
    binary,
    digest,
    json_bytes,
    put_text,
)
from experiments.codex_dogfood.case_0012 import freeze, packet
from experiments.codex_dogfood.case_0012.stage_b import (
    canonical,
    execute,
    reporting,
    validate_packet,
)
from experiments.codex_dogfood.case_0012.stage_b.durability import Journal
from experiments.exact_hint_routing import behavior
from experiments.exact_hint_routing.serialization import encode

pytest_plugins = ["experiments.exact_hint_routing.tests.test_behavior"]

if TYPE_CHECKING:
    from pathlib import Path

    from experiments.exact_hint_routing.models import ExactHintRoutingView
    from experiments.exact_hint_routing.routing import ExactFrame


def test_exclusive_entry_return_and_failed_boundary(tmp_path: Path) -> None:
    journal = Journal.start(tmp_path, {"execution": "fixture"})
    count = [0]

    def operation() -> dict[str, str]:
        count[0] += 1
        assert Journal.load(tmp_path).state["operations"][0]["status"] == "ENTERED"
        return {"native": "retained"}

    journal.call("one", {"frozen": True}, operation)
    restored = Journal.load(tmp_path)
    assert restored.state["values"]["one"] == {"native": "retained"}
    assert restored.state["operations"][0]["invocations"] == 1
    with pytest.raises(ValueError, match="already entered"):
        restored.call("one", {}, operation)
    with pytest.raises(FileExistsError):
        Journal.start(tmp_path, {"execution": "another"})
    assert count[0] == 1

    def failure() -> None:
        raise RuntimeError("returned no native value")

    with pytest.raises(RuntimeError):
        journal.call("failed", {}, failure)
    with pytest.raises(ValueError, match="Unrecoverable"):
        Journal.load(tmp_path).ready()


def test_claim_without_raw_blocks_second_execution(tmp_path: Path) -> None:
    (tmp_path / "execution.claim").write_text("claim")
    with pytest.raises(FileExistsError):
        Journal.start(tmp_path, {"execution": "fixture"})


def test_recovery_finalizes_without_rerun(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    journal = Journal.start(tmp_path, {"execution": "fixture"})
    journal.call("one", {}, lambda: ("native", 1))
    journal.complete()
    monkeypatch.setattr(execute, "CAPTURE", tmp_path)
    monkeypatch.setattr(
        reporting,
        "artifacts",
        lambda state: {"view.json": json_bytes(state["values"]["one"])},
    )
    monkeypatch.setattr(execute, "verify", lambda: {"verified": True})

    def forbidden(**_kwargs: object) -> None:
        raise AssertionError("Production rerun forbidden")

    monkeypatch.setattr(
        execute, "retrieve_repository_text_documents_by_bm25", forbidden
    )
    writer = put_text

    def fail_once(*_args: object, **_kwargs: object) -> None:
        raise OSError("Final publication interrupted")

    monkeypatch.setattr(execute, "put_text", fail_once)
    with pytest.raises(OSError, match="interrupted"):
        execute.finalize()
    assert Journal.load(tmp_path).state["values"]["one"] == ("native", 1)
    monkeypatch.setattr(execute, "put_text", writer)
    assert execute.finalize() == {"verified": True}
    assert len(Journal.load(tmp_path).state["operations"]) == 1
    put_text(tmp_path / "other.json", "extra")
    (tmp_path / "view.json").write_text("tampered")
    with pytest.raises(ValueError, match="overwrite refused"):
        execute.finalize()


def test_raw_tamper_rejected(tmp_path: Path) -> None:
    Journal.start(tmp_path, {"execution": "fixture"})
    journal = Journal.load(tmp_path)
    assert journal.state["values"] == {}
    # The summary is derived; tamper rejection belongs to immutable native state.
    original = Journal.start(tmp_path / "other", {"execution": "fixture"})
    original.call("one", {}, lambda: "native")
    target = tmp_path / "other/operations/000001.returned.json"
    value = json.loads(binary(target))
    value["native"]["sha256"] = "wrong"
    target.write_bytes(json_bytes(value))
    with pytest.raises(ValueError, match="digest differs"):
        Journal.load(tmp_path / "other")


def test_streamed_frozen_identity_and_projection(
    equivalent: tuple[ExactFrame, ExactHintRoutingView, ExactHintRoutingView],
) -> None:
    frame, b, c = equivalent
    for value in (
        frame,
        b.exact_resolutions,
        b.original_lexical_acquisition.index,
        b.provenance,
    ):
        assert "".join(canonical.chunks(value)).encode() == encode(value)
        assert canonical.native_hash(value)["canonical_sha256"] == digest(encode(value))
    expected = behavior.presentation(frame, b)
    with canonical.projection_adapter():
        assert behavior.presentation(frame, b) == expected
        behavior.require_equivalent(expected, behavior.presentation(frame, c))


def test_native_view_journal_roundtrip(
    equivalent: tuple[ExactFrame, ExactHintRoutingView, ExactHintRoutingView],
    tmp_path: Path,
) -> None:
    frame, b, c = equivalent
    root = tmp_path / "journal"
    journal = Journal.start(root, {"execution": "controlled-native-view"})
    journal.context({"frame": frame, "lexical": b.original_lexical_acquisition})
    journal.call("b", {}, lambda: b)
    journal.call("c", {}, lambda: c)
    journal.complete()
    loaded = Journal.load(root)
    left, right = loaded.state["values"]["b"], loaded.state["values"]["c"]
    assert left.original_lexical_acquisition is loaded.state["values"]["lexical"]
    assert left != right
    with canonical.projection_adapter():
        behavior.require_equivalent(
            behavior.presentation(frame, left), behavior.presentation(frame, right)
        )


def fixture_payload() -> dict[str, object]:
    return {
        "case": "case-0012",
        "task_identity": "fixture",
        "task_text": "task",
        "frame": dict.fromkeys(validate_packet.FRAME, "fixture"),
        "obligations": [
            {
                "identity": str(n),
                "key": str(n),
                "statement": "fixture",
                "criterion": "fixture",
                "applicability": "mandatory",
                "task_basis": [{"start": 0, "end": 4, "text": "task"}],
            }
            for n in range(9)
        ],
        "resources": [
            {
                "address": str(n),
                "content_identity": str(n),
                "text": "fixture",
                "encoding": "utf-8",
                "byte_size": 7,
                "document_identity": str(n),
            }
            for n in range(531)
        ],
    }


def test_blind_whitelist_determinism_leakage_and_overwrite(tmp_path: Path) -> None:
    value = fixture_payload()
    output = packet.render(value)
    assert output == packet.render(copy.deepcopy(value))
    root = tmp_path / "sterile"
    packet.publish(root, output)
    assert validate_packet.validate(root)["status"] == "VERIFIED; NO ADJUDICATION"
    with pytest.raises(FileExistsError):
        packet.publish(root, output)
    (root / "extra.txt").write_text("leak")
    with pytest.raises(ValueError, match="whitelist"):
        validate_packet.validate(root)
    # Structural tripwire never censors retained repository/task text.
    leaking = copy.deepcopy(value)
    leaking["score"] = 1
    with pytest.raises(ValueError, match="whitelist"):
        validate_packet.validate_payload(leaking)


def test_native_index_rehydration_on_controlled_frame() -> None:
    frame, metadata = freeze.prepare_frame(
        {"src/pkg/a.py": b"def fixture(): pass\n", "docs/a.md": b"fixture\n"}
    )
    index = execute.index_for(frame, metadata)
    assert (
        str(index.corpus_statistics.collection_analysis.document_collection.corpus.id)
        == metadata["corpus_id"]
    )


def test_blind_validator_has_no_treatment_imports() -> None:
    tree = ast.parse(binary(packet.VALIDATOR).decode())
    allowed = {"__future__", "gzip", "hashlib", "json", "stat", "pathlib", "typing"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert all(alias.name.split(".")[0] in allowed for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node.module is not None
            assert node.module.split(".")[0] in allowed


def test_published_capture_if_present(monkeypatch: pytest.MonkeyPatch) -> None:
    if not (execute.CAPTURE / "integrity.json").exists():
        return

    def forbidden(**_kwargs: object) -> None:
        raise AssertionError("Native treatment re-entry forbidden")

    monkeypatch.setattr(
        execute, "retrieve_repository_text_documents_by_bm25", forbidden
    )
    summary = execute.verify()
    assert summary["behavioral_resolution_equality"] is True
    assert summary["behavioral_presentation_equality"] is True
    assert summary["gold"] == "ABSENT"
