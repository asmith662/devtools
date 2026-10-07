# Copyright (c) 2026
# ruff: noqa: PLR2004 -- explicit prospective safety checks
"""Exercise blind packet invariants without prospective treatment or gold."""

from __future__ import annotations

import gzip
import json
from typing import Any

import pytest

from devtools.context.repository.snapshot import (
    RepositorySnapshot,
    RepositorySnapshotId,
)
from experiments.codex_dogfood.case_0009.artifacts import json_bytes
from experiments.codex_dogfood.case_0010.freeze import load_inputs, verify
from experiments.codex_dogfood.case_0010.packet import BLIND_FILES, render, validate
from experiments.codex_dogfood.case_0010.protocol import OBLIGATIONS, TASK, task_inputs
from tests.context.retrieval.lexical._helpers import _collection, _document


def native() -> dict[str, Any]:
    """Tiny frozen text frame; terms inside source are not metadata leakage."""
    docs = _collection((_document("a.py", "score rank query arm\nUnicode é\n"),))
    snapshot = RepositorySnapshot(
        RepositorySnapshotId("a" * 64),
        docs.documents[0].repository_id,
        tuple(d.resource for d in docs.documents),
    )
    task, queries = task_inputs()
    return {
        "snapshot": snapshot,
        "corpus": docs.corpus,
        "documents": docs,
        "task": task,
        "queries": queries,
    }


def test_blind_packet_double_build_and_explicit_digest_scopes() -> None:
    """Archive and canonical JSON scopes stay distinct; full content is retained."""
    a, b = render(native()), render(native())
    assert a == b
    assert set(a) == set(BLIND_FILES)
    m = json.loads(a["manifest.json"])
    assert m["task"] == TASK
    assert len(m["obligations"]) == len(OBLIGATIONS) == 10
    assert m["archive_sha256"] != m["canonical_payload_sha256"]
    resources = json.loads(gzip.decompress(a["resources.json.gz"]))
    assert (
        resources["resources"][0]["content"] == native()["documents"].documents[0].text
    )
    assert not any("query" in ob for ob in m["obligations"])


@pytest.mark.parametrize("field", ["query", "score", "arm", "parameters"])
def test_blind_packet_rejects_treatment_metadata(field: str) -> None:
    """Unknown metadata cannot leak despite authentic source words being allowed."""
    inputs = native()
    output = render(inputs)
    manifest = json.loads(output["manifest.json"])
    manifest[field] = "leak"
    output["manifest.json"] = json_bytes(manifest)
    with pytest.raises(ValueError, match="metadata"):
        validate(output, inputs)


def test_native_queries_have_no_gold_and_exact_obligation_association() -> None:
    """Task predicates and query lanes are frozen independently of any witness."""
    task, queries = task_inputs()
    assert len(queries) == 10
    assert all(not ob.witness_alternatives for ob in task.obligations)
    assert [(q.obligation, q.text) for q in queries] == [
        (ob.identity, text)
        for ob, (_, _, text) in zip(task.obligations, OBLIGATIONS, strict=True)
    ]


def test_frozen_stage_a_frame_and_packet_reconstruction() -> None:
    """Actual pinned frame has no gold and double builds deterministically."""
    manifest = verify()
    inputs = load_inputs()
    assert manifest["source_head"] == "b1f8413e30bfe870e80f01b08c2fcd81fc633aa6"
    assert manifest["resources"] == 531
    assert manifest["obligations"] == 10
    assert manifest["query_execution"] == "NONE"
    assert len(inputs["documents"].documents) == 531
    assert render(inputs) == render(inputs)
