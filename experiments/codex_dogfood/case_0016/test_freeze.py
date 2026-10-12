# Copyright (c) 2026
# ruff: noqa: D103, S101, PLR2004, COM812
"""Stage A observation replay, leakage, tamper and no-execution guards."""

import asyncio
import copy
import json
from pathlib import Path
from typing import Any

import pytest

from experiments.codex_dogfood.case_0009.artifacts import digest, git
from experiments.codex_dogfood.case_0016 import freeze, protocol
from experiments.codex_dogfood.case_0016.blind import project


def test_design_and_blind_allowlist() -> None:
    design = protocol.authored()
    assert len(design["requirement_matrix"]) == 6
    assert design["seed_policy"]["K"] == 10
    assert all(value == 0 for key, value in protocol.COUNTS.items() if key != "gold")
    assert protocol.COUNTS["gold"] == "ABSENT"
    resource: dict[str, Any] = dict.fromkeys(
        (
            "repository_id",
            "snapshot_id",
            "corpus_id",
            "address",
            "document_identity",
            "content_identity",
            "content",
        ),
        "synthetic",
    )
    resource.update(
        {
            "query": "TREATMENT_SENTINEL",
            "graph_score": 999,
            "seeds": ["TREATMENT_SENTINEL"],
        }
    )
    packet = project(design, [resource])
    assert "TREATMENT_SENTINEL" not in json.dumps(packet)
    assert set(packet) == {"case", "task_identity", "task", "obligations", "resources"}
    assert all(
        "query" not in row and "query_id" not in row for row in packet["obligations"]
    )
    assert packet["task"] == design["task_text"]
    assert packet["resources"][0]["content"] == "synthetic"


@pytest.mark.parametrize(
    "name",
    [
        "stage_b",
        "gold.json",
        "graph.json",
        "rankings.json",
        "exact_seeds.json",
        "execution.claim",
    ],
)
def test_no_execution_rejects_strays(tmp_path: Path, name: str) -> None:
    (tmp_path / name).write_text("forbidden", encoding="utf-8")
    with pytest.raises(ValueError, match="Unexpected prospective"):
        freeze.no_execution(tmp_path)


def test_overwrite_refusal_precedes_observation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "protocol.json").write_text("sealed", encoding="utf-8")

    async def forbid() -> dict[str, bytes]:
        msg = "Must refuse before reading frame"
        raise AssertionError(msg)

    monkeypatch.setattr(freeze, "expected", forbid)
    with pytest.raises(FileExistsError):
        asyncio.run(freeze.publish(tmp_path))


def test_deterministic_stage_a_replay_tamper_and_no_treatments(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def forbid(*_args: object, **_kwargs: object) -> None:
        msg = "Prospective treatment must remain unexecuted"
        raise AssertionError(msg)

    monkeypatch.setattr(
        "devtools.context.retrieval.graph.walk.stationary_distribution", forbid
    )
    monkeypatch.setattr(
        "devtools.context.python.references.derive_python_declaration_references",
        forbid,
    )
    monkeypatch.setattr(
        "devtools.context.retrieval.lexical.bm25.retrieve_repository_text_documents_by_bm25",
        forbid,
    )
    monkeypatch.setattr(
        "devtools.context.retrieval.fusion._fused_resource_order", forbid
    )
    monkeypatch.setattr(
        "experiments.task_conditioned_graph.view.build_reference_view", forbid
    )
    monkeypatch.setattr(
        "experiments.task_conditioned_graph.seeds.resolve_exact_seeds", forbid
    )
    monkeypatch.setattr("experiments.task_conditioned_graph.ranking.rank", forbid)
    monkeypatch.setattr("experiments.task_conditioned_graph.ranking.fuse", forbid)
    monkeypatch.setattr(
        "experiments.task_conditioned_graph.diagnostic.definitions", forbid
    )
    first = asyncio.run(freeze.expected())
    second = asyncio.run(freeze.expected())
    assert first == second
    for name, raw in first.items():
        (tmp_path / name).write_bytes(raw)
    asyncio.run(freeze.verify(tmp_path))
    (tmp_path / "protocol.json").write_bytes(first["protocol.json"] + b" ")
    with pytest.raises(ValueError, match="tamper/replay"):
        asyncio.run(freeze.verify(tmp_path))


@pytest.mark.parametrize(
    "field",
    ["seed_policy", "graph_projection", "metrics", "gold_policy", "decision_rule"],
)
def test_unauthorized_contract_changes_rejected(field: str) -> None:
    original = asyncio.run(freeze.authenticate_original())["protocol"]
    amended = json.loads(json.dumps(protocol.authored()))
    amended["frame_policy"] = original["frame_policy"]
    freeze.require_unchanged_contract(original, amended)
    bad = copy.deepcopy(amended)
    if field == "decision_rule":
        bad[field]["bounds"] = "relaxed"
    elif isinstance(bad[field], dict):
        bad[field]["unauthorized"] = True
    else:
        bad[field] = []
    with pytest.raises(ValueError, match="Unauthorized"):
        freeze.require_unchanged_contract(original, bad)


@pytest.mark.parametrize(
    ("field", "key"),
    [
        ("pagerank", "damping"),
        ("fusion", "rank_constant"),
        ("map_diagnostic", "maximum_utf8_bytes"),
    ],
)
def test_numerical_parameters_remain_frozen(field: str, key: str) -> None:
    original = asyncio.run(freeze.authenticate_original())["protocol"]
    amended = json.loads(json.dumps(protocol.authored()))
    amended["frame_policy"] = original["frame_policy"]
    amended[field][key] += 1
    with pytest.raises(ValueError, match="Unauthorized"):
        freeze.require_unchanged_contract(original, amended)


def test_amendment_refuses_non_original_or_second_overwrite(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = asyncio.run(freeze.authenticate_original())

    async def authenticate() -> dict[str, Any]:
        return original

    monkeypatch.setattr(freeze, "authenticate_original", authenticate)
    for name in original["seal"]["artifacts"]:
        (tmp_path / name).write_bytes(b"not-original")
    with pytest.raises(ValueError, match="Refusing amendment overwrite"):
        asyncio.run(freeze.amend(tmp_path))


def test_original_authentication_rejects_seal_tamper(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    actual_git = git

    async def tamper(*args: str) -> bytes:
        raw = await actual_git(*args)
        return (
            raw + b" "
            if args[0] == "show" and args[1].endswith("/integrity.json")
            else raw
        )

    monkeypatch.setattr(freeze, "git", tamper)
    with pytest.raises(ValueError, match="integrity hash mismatch"):
        asyncio.run(freeze.authenticate_original())


def test_amendment_atomic_overwrite_preserves_frame_and_refuses_repeat(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    original_bytes = {
        "protocol.json": b"original\n",
        "frame.json": b"frame\n",
        "resources.json.gz": b"synthetic-gzip-bytes",
    }
    for name, raw in original_bytes.items():
        (tmp_path / name).write_bytes(raw)
    seal_bytes = b"original-seal\n"
    (tmp_path / "integrity.json").write_bytes(seal_bytes)
    monkeypatch.setattr(protocol, "PRIOR_INTEGRITY_SHA256", digest(seal_bytes))

    async def authenticate() -> dict[str, Any]:
        return {
            "seal": {
                "artifacts": {name: digest(raw) for name, raw in original_bytes.items()}
            }
        }

    async def expected() -> dict[str, bytes]:
        return {
            **original_bytes,
            "protocol.json": b"amended\n",
            "integrity.json": b"amended-seal\n",
        }

    monkeypatch.setattr(freeze, "authenticate_original", authenticate)
    monkeypatch.setattr(freeze, "expected", expected)
    asyncio.run(freeze.amend(tmp_path))
    assert (tmp_path / "protocol.json").read_bytes() == b"amended\n"
    assert (tmp_path / "frame.json").read_bytes() == original_bytes["frame.json"]
    assert (tmp_path / "resources.json.gz").read_bytes() == original_bytes[
        "resources.json.gz"
    ]
    with pytest.raises(ValueError, match="Refusing amendment overwrite"):
        asyncio.run(freeze.amend(tmp_path))
