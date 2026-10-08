"""Test packet integrity and blindness without making semantic judgments."""

# ruff: noqa: INP001, CPY001, D103, S101, PLR2004
from __future__ import annotations

import copy
import gzip
import itertools
import json
from typing import TYPE_CHECKING, Any, cast

import pytest

from experiments.codex_dogfood.case_0011.adjudication.reviewed import (
    build_reviewed_gold as g,
)
from experiments.codex_dogfood.case_0011.adjudication.stage_c5 import build_packet as b

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture
def packet() -> dict[str, Any]:
    return cast(
        "dict[str, Any]",
        json.loads(gzip.decompress((b.ROOT / "packet.json.gz").read_bytes())),
    )


def test_frozen_binding_and_deterministic_double_build() -> None:
    first, audit = b.artifacts()
    second, second_audit = b.artifacts()
    assert first == second
    assert audit == second_audit
    assert all(p.read_bytes() == raw for p, raw in first.items())
    b.validate_files({p.name: raw for p, raw in first.items()})
    assert g.load(b.ROOT / "projection_audit.json") == audit


def test_complete_mapping_with_cross_obligation_pairs(packet: dict[str, Any]) -> None:
    needs, units = packet["information_needs"], packet["units"]
    expected = {
        (n["identity"], u["identity"]) for n, u in itertools.product(needs, units)
    }
    actual = [(p["need"], p["unit"]) for p in packet["mapping_frame"]]
    assert len(needs) == 18
    assert len(units) == 32
    assert len(actual) == len(set(actual)) == len(expected) == 576
    assert set(actual) == expected
    assert any(
        n["obligation"] not in u["obligations"]
        for n, u in itertools.product(needs, units)
    )
    assert all(set(p) == {"need", "unit"} for p in packet["mapping_frame"])


def test_exact_need_semantics_and_neutral_unit_projection(
    packet: dict[str, Any],
) -> None:
    assert packet["information_needs"] == b.frozen_needs(packet["task"])
    gold = g.load(g.ADJ / "reviewed/reviewed_gold.json")
    audit = g.load(b.ROOT / "projection_audit.json")
    projected = {u["identity"]: u for u in packet["units"]}
    for u in gold["units"]:
        p = projected[audit["unit_projection"][u["id"]]]
        assert p["statement"] == b.neutral_statement(u["statement"])
        assert p["obligations"] == u["obligations"]
        assert set(p["alternative_membership"]) == {
            audit["alternative_projection"][a] for a in u["alternative_membership"]
        }
    assert packet["obligations"] == gold["frozen_obligations"]
    assert packet["task"] == gold["task"]


@pytest.mark.parametrize(
    "key",
    [
        "query",
        "lexical_query",
        "analyzed_terms",
        "routes",
        "resources",
        "address",
        "filename",
        "excerpt",
        "retrieval_results",
        "candidate_memberships",
        "rank",
        "score",
        "score_contributions",
        "query_cost",
        "arm",
        "outcome",
        "primary",
        "chronology",
        "model_identity",
        "confirmation",
    ],
)
def test_nested_leakage_key_rejection(packet: dict[str, Any], key: str) -> None:
    damaged = copy.deepcopy(packet)
    damaged["information_needs"][0][key] = "injected forbidden metadata"
    with pytest.raises(AssertionError):
        b.check_packet(damaged)


@pytest.mark.parametrize(
    "text",
    [
        "src/devtools/context/planning/rendering.py",
        "rendering.py",
        "stage_c_r",
        "reconciliation chronology",
        "position_1",
        "gpt-6",
    ],
)
def test_leakage_in_semantic_string_rejected(packet: dict[str, Any], text: str) -> None:
    damaged = copy.deepcopy(packet)
    damaged["units"][0]["statement"] += " " + text
    with pytest.raises(AssertionError):
        b.check_packet(damaged)


def test_no_answer_locations_or_source_identity(packet: dict[str, Any]) -> None:
    b.check_packet(packet)
    raw = g.canonical(packet).decode()
    gold = g.load(g.ADJ / "reviewed/reviewed_gold.json")
    for resource in gold["resources"]:
        assert resource["address"] not in raw
    assert ".local/codex-result.md" not in raw
    assert all("provenance" not in u for u in packet["units"])


def test_mapping_deletion_duplicate_foreign_identity_rejected(
    packet: dict[str, Any],
) -> None:
    for mode in ("delete", "duplicate", "foreign"):
        damaged = copy.deepcopy(packet)
        if mode == "delete":
            damaged["mapping_frame"].pop()
        elif mode == "duplicate":
            damaged["mapping_frame"][-1] = damaged["mapping_frame"][0]
        else:
            damaged["mapping_frame"][-1]["need"] = "foreign-need"
        with pytest.raises(AssertionError):
            b.check_packet(damaged)


def test_future_labels_are_frozen_no_judgments(packet: dict[str, Any]) -> None:
    assert packet["mapping_labels"] == b.MAPPING_LABELS
    assert packet["need_labels"] == b.NEED_LABELS
    assert packet["unit_coverage"] == b.UNIT_COVERAGE
    assert "DIRECTLY_COVERS" in packet["direct_coverage_rule"]
    assert all(set(p) == {"need", "unit"} for p in packet["mapping_frame"])


def test_overwrite_refusal(tmp_path: Path) -> None:
    path = tmp_path / "packet.json.gz"
    path.write_bytes(b"frozen")
    with pytest.raises(FileExistsError):
        g.write_new({path: b"new"})
    assert path.read_bytes() == b"frozen"


def test_workspace_whitelist_and_extra_file_rejection(tmp_path: Path) -> None:
    files, _ = b.artifacts()
    named = {p.name: raw for p, raw in files.items()}
    for name, raw in named.items():
        (tmp_path / name).write_bytes(raw)
    b.workspace_check(tmp_path, named)
    (tmp_path / "unexpected").write_bytes(b"bad")
    with pytest.raises(AssertionError):
        b.workspace_check(tmp_path, named)


def test_integrity_tamper_and_metadata_injection_rejected() -> None:
    files, _ = b.artifacts()
    named = {p.name: raw for p, raw in files.items()}
    tampered = {**named, "packet.json.gz": named["packet.json.gz"] + b"tamper"}
    with pytest.raises(AssertionError):
        b.validate_files(tampered)
    manifest = json.loads(named["manifest.json"])
    manifest["score"] = 42
    injected = {**named, "manifest.json": g.canonical(manifest)}
    with pytest.raises(AssertionError):
        b.validate_files(injected)


def test_pre_review_document_is_exact_transparency(packet: dict[str, Any]) -> None:
    assert (b.ROOT / "C5_PACKET_REVIEW.md").read_bytes() == b.review_markdown(packet)
