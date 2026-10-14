# Copyright (c) 2026
# ruff: noqa: S101, C901, PLR0912, PT007, PT011, PT018, ANN401, D103, PLR2004 -- synthetic prospective contracts
"""Pure authored/packet/join contracts; no fresh-case treatment execution."""

from __future__ import annotations

import asyncio
import base64
import copy
import itertools
import json
import runpy
import sys
from argparse import Namespace
from pathlib import Path
from typing import Any

import pytest

from experiments.codex_dogfood.case_0009.artifacts import ROOT, json_bytes
from experiments.codex_dogfood.verification.journal import journal_type
from experiments.codex_dogfood.verification.native import NativeMemo
from experiments.orchestration.isolation import semantic_outputs, sterile
from experiments.source_grounding import contracts, reviewer, workers
from experiments.source_grounding.cases import CASES, ORIGINAL_CASES
from experiments.source_grounding.timing import summarize
from experiments.source_grounding.workers import (
    authenticate_primary,
    command,
    configuration,
    gold_packet,
    packet_files,
    write_files,
)
from experiments.structural_discrimination.stage_b.capture import Journal


def fixture() -> tuple[Any, Any, Any]:
    rows = []
    for address in ("a.py", "b.py", "c.py"):
        content = "concrete repository fact " + address
        cid = reviewer.semantic("decoded-utf8-text-sha256-v1", content)
        rows.append(
            {
                "address": address,
                "content": content,
                "content_identity": cid,
                "document_identity": reviewer.semantic(
                    "whole-resource-exact-text-v1",
                    "repository",
                    address,
                    cid,
                ),
            },
        )
    pairs = tuple(v for r in rows for v in (r["address"], r["content_identity"]))
    frame = {
        "repository_id": "repository",
        "snapshot_id": reviewer.semantic(
            "explicit-required-text-resources-sha256-v1",
            "repository",
            *pairs,
        ),
        "corpus_id": reviewer.semantic(
            "selected-observed-utf8-resource-occurrences-sha256-v1",
            "repository",
            *pairs,
        ),
        "parent_tree": "a" * 40,
    }
    obligation = {
        "id": "O1",
        "requirement": "task",
        "satisfaction": "criterion",
        "exclusions": "exclusions",
        "gap": "none",
    }
    design = {
        "case": "synthetic",
        "task_text": "synthetic public task",
        "frame": frame,
        "obligations": [obligation],
    }
    a = [
        {
            **contracts.endpoint(r),
            "a_rank": i,
            "score": float(4 - i),
            "filename_weight": 0.25,
        }
        for i, r in enumerate(rows, 1)
    ]
    fact = {
        "fact_identity": "fact",
        "derivation_identity": "derivation",
        "source_snapshot_id": frame["snapshot_id"],
        "source_address": "a.py",
        "source_range_utf8": {
            "start_line": 1,
            "start_column_utf8": 0,
            "end_line": 1,
            "end_column_utf8": 1,
        },
        "target_snapshot_id": frame["snapshot_id"],
        "target_address": "c.py",
        "target_content_identity": rows[2]["content_identity"],
        "target_declaration_identity": "declaration",
        "target_subject_identity": "subject",
        "native_route": "native",
    }
    capture = {
        "case": "synthetic",
        "frame": frame,
        "facts": [fact],
        "queries": [
            {
                "obligation": "O1",
                "A": a,
                "broad": [
                    {
                        "target": "c.py",
                        "rank": 3,
                        "predecessor": a[1],
                        "sources": [{"source": "a.py", "rank": 1, "facts": ["fact"]}],
                    },
                ],
            },
        ],
    }
    return design, rows, capture


def evidence(row: Any) -> Any:
    return {
        "source": contracts.endpoint(row),
        "start": 0,
        "end": 8,
        "quote": row["content"][:8],
    }


def attestation(model: str) -> Any:
    return {
        "model": model,
        "reasoning": "High",
        "second_reviewer": False,
        "reconciliation": False,
        "host_routing_independently_verified": False,
        "blindness": ["NO_ACCESS:" + name for name in reviewer.BLINDNESS],
    }


def grounding_review(p: Any) -> Any:
    c = p["cells"][0]
    return {
        "schema": "blind-primary-review-v1",
        "case": p["case"],
        "frame": p["frame"],
        "packet_sha256": reviewer.sha(reviewer.canonical(p)),
        "attestation": attestation("GPT-6 Sol"),
        "cells": [
            {
                "obligation": "O1",
                "source": contracts.endpoint(c["source"]),
                "verdict": "GROUNDED_SOURCE",
                "spans": [evidence(c["source"])],
                "statement": "current fact",
                "reason": "material to criterion",
                "assumptions": [],
                "uncertainty": "",
                "additional_information": "",
            },
        ],
        "units": [],
        "gaps": [],
        "self_review": "same-primary audit",
    }


def test_population_cases_and_authored_obligations() -> None:
    assert list(CASES) == ["0022", "0023", "0024"]
    assert [c["position"] for c in CASES.values()] == [6, 7, 8]
    assert CASES["0022"] == ORIGINAL_CASES["0022"]
    for case in CASES.values():
        assert [o["id"] for o in case["obligations"]] == ["O1", "O2"]
        assert case["gap"].strip()
        for o in case["obligations"]:
            assert set(o) == {
                "id",
                "requirement",
                "facts",
                "satisfaction",
                "exclusions",
                "need",
                "query",
            }
            assert all(v.strip() for v in o.values())
            assert not any(c in o["query"] for c in ("/", "\\", "_"))


def test_source_candidates_and_strict_disclosure() -> None:
    design, rows, capture = fixture()
    packet = contracts.grounding_packet(design, rows, capture)
    assert [
        (c["obligation"]["id"], c["source"]["address"]) for c in packet["cells"]
    ] == [("O1", "a.py")]
    assert packet["cells"][0]["source"]["content"] == rows[0]["content"]
    reviewer.metadata(packet)
    assert "c.py" not in json.dumps(packet)
    assert "rank" not in json.dumps(packet)
    assert "query" not in json.dumps(packet)


@pytest.mark.parametrize("verdict", contracts.VERDICTS)
def test_qualified_subset_and_original_predecessor(verdict: str) -> None:
    design, rows, capture = fixture()
    review = grounding_review(contracts.grounding_packet(design, rows, capture))
    review["cells"][0]["verdict"] = verdict
    qualified = contracts.qualify(capture, review["cells"])
    q = qualified["queries"][0]
    assert q["A"] == capture["queries"][0]["A"]
    assert q["broad"] == capture["queries"][0]["broad"]
    assert bool(q["qualified"]) == (verdict == "GROUNDED_SOURCE")
    assert bool(q["uncertain_potential"]) == (verdict == "UNCERTAIN_SOURCE")
    if q["qualified"]:
        assert q["qualified"][0]["predecessor"]["a_rank"] == 2


@pytest.mark.parametrize(
    "mutation",
    (
        "target",
        "predecessor",
        "source",
        "rank",
        "source_rank",
        "self",
        "fact",
        "provenance",
        "frame",
        "missing_target",
        "duplicate_target",
        "duplicate_source",
        "duplicate_fact",
        "stale_content",
    ),
)
def test_broad_rejects_invalid_captured_join(mutation: str) -> None:
    _, rows, capture = fixture()
    q = capture["queries"][0]
    t = q["broad"][0]
    if mutation == "target":
        t["target"] = "foreign.py"
    elif mutation == "predecessor":
        t["predecessor"] = q["A"][0]
    elif mutation == "source":
        t["sources"][0]["source"] = "foreign.py"
    elif mutation == "rank":
        t["rank"] = 2
    elif mutation == "source_rank":
        t["sources"][0]["rank"] = 3
    elif mutation == "self":
        t["sources"][0]["source"] = "c.py"
    elif mutation == "fact":
        t["sources"][0]["facts"] = ["unsupported"]
    elif mutation == "provenance":
        capture["facts"][0]["target_declaration_identity"] = ""
    elif mutation == "frame":
        capture["facts"][0]["source_snapshot_id"] = "foreign"
    elif mutation == "missing_target":
        q["broad"] = []
    elif mutation == "duplicate_target":
        q["broad"].append(copy.deepcopy(t))
    elif mutation == "duplicate_source":
        t["sources"].append(copy.deepcopy(t["sources"][0]))
    elif mutation == "duplicate_fact":
        t["sources"][0]["facts"] *= 2
    elif mutation == "stale_content":
        q["A"][0]["content_identity"] = "stale"
    with pytest.raises(ValueError):
        contracts.validate_channels(capture, rows)


@pytest.mark.parametrize("field", sorted(reviewer.FORBIDDEN))
def test_grounding_packet_rejects_leakage(tmp_path: Path, field: str) -> None:
    design, rows, capture = fixture()
    packet = contracts.grounding_packet(design, rows, capture)
    packet[field] = "forbidden"
    files = packet_files(packet, b"instructions", Path(reviewer.__file__).read_bytes())
    with pytest.raises(ValueError):
        sterile(tmp_path / "sterile", files) if field in {
            "query",
            "queries",
            "need",
            "rank",
            "score",
            "annotations",
            "supports",
            "local_pairs",
            "timings",
            "child_commit",
            "child_tree",
            "changed_paths",
        } else reviewer.metadata(packet)


def test_packet_preservation_gold_blindness_and_exact_frame(tmp_path: Path) -> None:
    design, rows, _ = fixture()
    files = packet_files(
        gold_packet(design, rows),
        b"instructions",
        Path(reviewer.__file__).read_bytes(),
    )
    root = tmp_path / "gold"
    sterile(root, files)
    assert reviewer.packet(root)["resources"] == rows
    assert not (root / ".git").exists() and not (root / ".local").exists()
    (root / "packet.json").write_bytes(b"{}")
    with pytest.raises(ValueError, match="mutation"):
        reviewer.packet(root)


def test_grounding_review_exact_complete_cells() -> None:
    design, rows, capture = fixture()
    packet = contracts.grounding_packet(design, rows, capture)
    review = grounding_review(packet)
    assert reviewer.validate(review, packet)["cells"] == 1
    for cells in (list[Any](), review["cells"] * 2):
        bad = {**review, "cells": cells}
        with pytest.raises(ValueError):
            reviewer.validate(bad, packet)
        with pytest.raises(ValueError):
            contracts.qualify(capture, cells)
    bad = copy.deepcopy(review)
    bad["cells"][0]["spans"][0]["source"] = contracts.endpoint(rows[2])
    with pytest.raises(ValueError):
        reviewer.validate(bad, packet)


@pytest.mark.parametrize(
    "mutation",
    (
        "case",
        "frame",
        "packet_sha256",
        "model",
        "reasoning",
        "second_reviewer",
        "reconciliation",
        "blindness",
        "span",
        "verdict",
        "uncertainty",
    ),
)
def test_reviewer_rejects_identity_and_semantic_contract_defects(mutation: str) -> None:
    design, rows, capture = fixture()
    packet = contracts.grounding_packet(design, rows, capture)
    review = grounding_review(packet)
    if mutation in {"case", "frame", "packet_sha256"}:
        review[mutation] = "foreign"
    elif mutation == "model":
        review["attestation"]["model"] = "other"
    elif mutation == "reasoning":
        review["attestation"]["reasoning"] = "Low"
    elif mutation in {"second_reviewer", "reconciliation"}:
        review["attestation"][mutation] = True
    elif mutation == "blindness":
        review["attestation"]["blindness"] = []
    elif mutation == "span":
        review["cells"][0]["spans"][0]["quote"] = "wrong"
    elif mutation == "verdict":
        review["cells"][0]["verdict"] = "HELPFUL_ONLY"
    elif mutation == "uncertainty":
        review["cells"][0]["verdict"] = "UNCERTAIN_SOURCE"
    with pytest.raises(ValueError):
        reviewer.validate(review, packet)


@pytest.mark.parametrize(
    ("target", "predecessor"),
    list(itertools.product(contracts.LABELS, repeat=2)),
)
def test_pair_order_and_strong_boundaries(target: str, predecessor: str) -> None:
    outcome, strong = contracts.pair(target, predecessor)
    expected = {
        ("REQUIRED", "HELPFUL_ONLY"): "BENEFICIAL",
        ("REQUIRED", "UNNECESSARY"): "BENEFICIAL",
        ("HELPFUL_ONLY", "UNNECESSARY"): "BENEFICIAL",
        ("HELPFUL_ONLY", "REQUIRED"): "HARMFUL",
        ("UNNECESSARY", "REQUIRED"): "HARMFUL",
        ("UNNECESSARY", "HELPFUL_ONLY"): "HARMFUL",
    }
    assert outcome == expected.get((target, predecessor), "NEUTRAL")
    assert bool(strong) == ({target, predecessor} == {"REQUIRED", "UNNECESSARY"})


@pytest.mark.parametrize(
    ("sb", "sh", "expected"),
    (
        (0, 0, "QUALIFIED_NO_MATERIAL_STRUCTURAL_DISCRIMINATION_SIGNAL"),
        (1, 0, "QUALIFIED_STRUCTURAL_DISCRIMINATION_SIGNAL"),
        (0, 1, "QUALIFIED_STRUCTURAL_DISCRIMINATION_CONTRADICTED"),
        (1, 1, "QUALIFIED_MIXED_STRUCTURAL_DISCRIMINATION_SIGNAL"),
    ),
)
def test_case_category_boundaries(sb: int, sh: int, expected: str) -> None:
    assert contracts.category(sb, sh) == expected


def gold_review(packet: Any, rows: Any) -> Any:
    return {
        "schema": "blind-primary-review-v1",
        "case": "synthetic",
        "frame": packet["frame"],
        "packet_sha256": reviewer.sha(reviewer.canonical(packet)),
        "attestation": attestation("GPT-6 Astra"),
        "cells": [
            {
                "obligation": "O1",
                "source": contracts.endpoint(r),
                "label": "REQUIRED"
                if i == 0
                else "HELPFUL_ONLY"
                if i == 1
                else "UNNECESSARY",
                "spans": [evidence(r)] if i < 2 else [],
                "reason": "independent content judgment",
            }
            for i, r in enumerate(rows)
        ],
        "units": [
            {
                "id": "U1",
                "obligation": "O1",
                "statement": "necessary fact",
                "basis": "REPOSITORY_SUPPORTED",
                "necessity": "criterion requires it",
                "alternatives": [[evidence(rows[0])]],
            },
        ],
        "gaps": {
            "TASK_INTERPRETATION_GAP": "PRESENT",
            "TASK_GAP": "PRESENT",
            "REPOSITORY_INFORMATION_GAP": "NONE",
            "unconditional_sufficiency": False,
            "qualification": "conditional repository integration only",
        },
        "self_review": "audited cells, units, alternatives and exclusions",
    }


def test_gold_units_witnesses_gaps_and_controller_output_compatibility() -> None:
    design, rows, _ = fixture()
    packet = gold_packet(design, rows)
    review = gold_review(packet, rows)
    result = reviewer.validate(review, packet)
    assert result["obligation_witnesses"] == {"O1": [["a.py"]]}
    assert result["conditional_repository_indispensable"] == ["a.py"]
    assert result["unconditional_task_unions"] == []
    assert result["unconditional_task_indispensable"] is None
    semantic_outputs({"stage_c_review.json": json_bytes(review)})
    review["cells"][1]["label"] = "REQUIRED"
    with pytest.raises(ValueError):
        reviewer.validate(review, packet)


def test_frozen_frame_bindings_without_treatment() -> None:
    expected = {
        "0020": (
            369,
            274,
            "0733092f5001ce157f7c190ff17574701fa01d58",
            "87f925a834e6893bc3ec6b50cf3cb73f34edfd16",
        ),
        "0021": (
            222,
            182,
            "512cf5559dbb346e361145ffe1a5bbacdd4ca566",
            "ff4a59a4d595ea98280dc079f9eb3b509104acd3",
        ),
        "0022": (
            372,
            277,
            "6bd9061f94646c02fb50a9e24dc73fc203c11a30",
            "bde2d0512f7bc36385d29cd2bad5f2e098950988",
        ),
    }
    for case, (count, python, parent, tree) in expected.items():
        root = ROOT / f"experiments/codex_dogfood/case_{case}"
        frame = json.loads((root / "frame.json").read_bytes())
        assert (
            frame["resource_count"],
            frame["python_resource_count"],
            frame["source_head"],
            frame["source_tree"],
        ) == (count, python, parent, tree)
        assert not (root / "stage_b").exists() and not (root / "adjudication").exists()
    assert configuration("Sol")["model_id"] == "gpt-6-sol"
    assert configuration("Astra")["model_id"] == "gpt-6-astra"


def test_replacement_frozen_parent_bindings_without_treatment() -> None:
    expected = {
        "0023": (
            "66ed2049de72aa5c2762ab506174c711639bbbf8",
            "4d49dcfea18f40762b70bbc11b60514db1c438ae",
        ),
        "0024": (
            "1e712c29aec32d4911d7ca2372c27a04511c999c",
            "b63225c8f037a8f2f8db0b7467d607a693d4d6af",
        ),
    }
    for case, (parent, tree) in expected.items():
        root = ROOT / f"experiments/codex_dogfood/case_{case}"
        if not (root / "frame.json").exists():
            # Source contracts also run before Stage A materialization.
            continue
        frame = json.loads((root / "frame.json").read_bytes())
        assert (frame["source_head"], frame["source_tree"]) == (parent, tree)
        assert not (root / "stage_b").exists() and not (root / "adjudication").exists()


@pytest.mark.parametrize("field", ["case", "frame"])
def test_grounding_rejects_cross_case_frame(field: str) -> None:
    design, rows, capture = fixture()
    capture[field] = "foreign"
    with pytest.raises(ValueError, match="case/frame"):
        contracts.grounding_packet(design, rows, capture)


def test_scientific_overwrite_refusal(tmp_path: Path) -> None:
    write_files(tmp_path, {"artifact.json": b"original"})
    with pytest.raises(ValueError, match="overwrite"):
        write_files(tmp_path, {"artifact.json": b"replacement", "other.json": b"new"})
    assert (tmp_path / "artifact.json").read_bytes() == b"original"
    assert not (tmp_path / "other.json").exists()


def test_operational_critical_paths_are_not_scientific_authority() -> None:
    events = [
        {"case": "a", "stage": "B", "status": "RUNNING", "elapsed_seconds": 2},
        {"case": "b", "stage": "B", "status": "RUNNING", "elapsed_seconds": 3},
        {
            "case": "b",
            "stage": "B",
            "status": "COMPLETE",
            "elapsed_seconds": 7,
            "duration_seconds": 4,
        },
        {
            "case": "a",
            "stage": "B",
            "status": "COMPLETE",
            "elapsed_seconds": 8,
            "duration_seconds": 6,
        },
        {
            "case": "cohort",
            "stage": "run",
            "status": "COMPLETE; REVIEW",
            "elapsed_seconds": 11,
        },
    ]
    result = summarize(events)
    assert result["branch_critical_path_seconds"] == {"B": 6, "C": None}
    assert result["controller_elapsed_seconds"] == 11
    assert result["controller_complete"] is True
    assert result["authority"] == "OPERATIONAL_ONLY_NOT_SCIENTIFIC_AUTHORITY"


@pytest.mark.parametrize("gold", [False, True])
def test_blind_branch_serializer_transport(tmp_path: Path, *, gold: bool) -> None:
    """Synthetic authored decisions only; no semantic worker or scientific run."""
    design, rows, capture = fixture()
    payload = (
        gold_packet(design, rows)
        if gold
        else contracts.grounding_packet(design, rows, capture)
    )
    files = packet_files(
        payload,
        b"synthetic instructions",
        Path(reviewer.__file__).read_bytes(),
    )
    root = tmp_path / "primary"
    sterile(root, files)
    builder = files["stage_c_builder.py"]
    forbidden = (
        (b"GROUNDED_SOURCE", b"GPT-6 Sol", b"source-grounding")
        if gold
        else (b"REQUIRED", b"HELPFUL_ONLY", b"GPT-6 Astra", b"conditional_repository")
    )
    assert not any(word in builder for word in forbidden)
    standalone = runpy.run_path(str(root / "stage_c_builder.py"))
    assert standalone["packet"](root) == payload
    review = gold_review(payload, rows) if gold else grounding_review(payload)
    (root / "stage_c_review.json").write_bytes(json_bytes(review))
    asyncio.run(
        command(
            [
                sys.executable,
                "-B",
                str(root / "stage_c_builder.py"),
                "build",
                "--root",
                str(root),
            ],
            root,
            tmp_path / "build",
        ),
    )
    receipt = asyncio.run(
        authenticate_primary(
            root,
            "synthetic",
            design["frame"],
            tmp_path / "verify",
        ),
    )
    assert receipt["status"] == "PASS"
    assert receipt["model"] == ("GPT-6 Astra" if gold else "GPT-6 Sol")
    assert receipt["complete_cells"] == (3 if gold else 1)
    assert reviewer.products(root) == standalone["products"](root)
    assert (root / "stage_c_builder.py").read_bytes() == builder


def test_primary_bytes_roundtrip_through_existing_native_journal(
    tmp_path: Path,
) -> None:
    """Check the new payload at the canonical codec boundary using synthetic data."""
    original = b"synthetic primary bytes\x00\xff\r\n"
    payload = {
        "files_b64": {"synthetic.bin": base64.b64encode(original).decode("ascii")},
    }
    journal = Journal.start(
        tmp_path / "journal",
        {
            "case": "synthetic",
            "execution": "synthetic-byte-transport",
            "frame": {},
            "runtime": "synthetic",
        },
    )
    assert journal.call("synthetic-return", {}, lambda: payload) == payload
    journal.complete()
    loaded = journal_type(NativeMemo()).load(tmp_path / "journal")
    result = loaded.state["values"]["synthetic-return"]
    assert (
        base64.b64decode(result["files_b64"]["synthetic.bin"], validate=True)
        == original
    )


def test_packet_adapter_publishes_only_blind_branch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    design, rows, _ = fixture()
    monkeypatch.setattr(workers, "prepared", lambda *_: (design, rows))
    (tmp_path / "reviewer_codec.py").write_bytes(Path(reviewer.__file__).read_bytes())
    (tmp_path / "INSTRUCTIONS_GOLD.md").write_bytes(b"synthetic gold instructions")
    args = Namespace(
        workspace=tmp_path,
        case="synthetic",
        frame=json.dumps(design["frame"]),
        stage="packet",
    )
    assert workers.run_stage(args) == {"status": "PASS"}
    candidate = json.loads((tmp_path / "candidate.json").read_bytes())
    assert set(candidate["files"]) == {
        "packet.json",
        "INSTRUCTIONS.md",
        "stage_c_builder.py",
        "packet_integrity.json",
    }
    assert b"GROUNDED_SOURCE" not in (tmp_path / "stage_c_builder.py").read_bytes()
    args.stage = "packet_validate"
    assert workers.run_stage(args) == {"status": "PASS"}
    args.stage = "packet"
    with pytest.raises(ValueError, match="overwrite"):
        workers.run_stage(args)
