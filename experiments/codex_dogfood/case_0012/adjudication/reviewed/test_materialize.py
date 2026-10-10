"""Validate publication mechanics against sealed, case-local evidence."""

# ruff: noqa: INP001, CPY001, D103, S101, PLR2004, COM812
from __future__ import annotations

import copy
import gzip
import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

import pytest

from experiments.codex_dogfood.case_0012.adjudication.reviewed import materialize as m


def join_fixture() -> tuple[Any, Any, set[str]]:
    packet = json.loads(gzip.decompress((m.REC / "packet/packet.json.gz").read_bytes()))
    original = json.loads(gzip.decompress(m.SOURCE_PAYLOAD.read_bytes()))
    return (
        packet["resources"],
        original["resources"],
        {a for p in packet["propositions"] for a in p["resource_addresses"]},
    )


def test_current_resource_join() -> None:
    packet, original, expected = join_fixture()
    assert len(packet) == len(expected) == 49
    assert set(packet[0]) - set(original[0]) == {"text_sha256"}
    assert len(set(packet[0]) & set(original[0])) == 6
    m.join_resources(packet, original, expected)


@pytest.mark.parametrize(
    "mutation",
    [
        "common",
        "content",
        "missing_digest",
        "malformed_digest",
        "missing",
        "unexpected",
        "duplicate",
        "extra_field",
        "missing_field",
        "duplicate_identity",
    ],
)
def test_resource_join_rejects(mutation: str) -> None:
    packet, original, expected = join_fixture()
    if mutation == "common":
        packet[0]["byte_size"] += 1
    elif mutation == "content":
        packet[0]["text"] += "altered"
    elif mutation == "missing_digest":
        del packet[0]["text_sha256"]
    elif mutation == "malformed_digest":
        packet[0]["text_sha256"] = "NOT-A-DIGEST"
    elif mutation == "missing":
        packet.pop()
    elif mutation == "unexpected":
        packet[0]["address"] = "unexpected"
    elif mutation == "duplicate":
        packet.append(copy.deepcopy(packet[0]))
    elif mutation == "extra_field":
        packet[0]["unrelated"] = True
    elif mutation == "missing_field":
        del packet[0]["encoding"]
    else:
        packet[1]["document_identity"] = packet[0]["document_identity"]
    with pytest.raises(
        ValueError, match=r"Resource|resource|text_sha256|digest|common"
    ):
        m.join_resources(packet, original, expected)


def test_missing_original_resource() -> None:
    packet, original, expected = join_fixture()
    original = [r for r in original if r["address"] != packet[0]["address"]]
    with pytest.raises(ValueError, match="Missing original"):
        m.join_resources(packet, original, expected)


def test_exact_reconstruction() -> None:
    assert m.verify()["status"] == "PASS"


@pytest.mark.parametrize(
    "target",
    [
        "cell",
        "identity",
        "span",
        "unit",
        "witness",
        "gap",
        "decision",
        "combination",
        "limitation",
    ],
)
def test_tamper_rejection(target: str) -> None:
    gold = copy.deepcopy(m.construct_gold())
    if target == "cell":
        gold["cells"][0]["label"] = "HELPFUL_ONLY"
    elif target == "identity":
        gold["cells"][0]["document_identity"] = "foreign"
    elif target == "span":
        gold["semantic_units"][0]["supports"][0]["evidence"][0]["end"] += 1
    elif target == "unit":
        gold["semantic_units"].pop()
    elif target == "witness":
        gold["witnesses_by_obligation"]["source"][0]["resources"].pop()
    elif target == "gap":
        gold["gaps"]["task_gap"] = ["invented"]
    elif target == "decision":
        gold["decision_applications"].pop(next(iter(gold["decision_applications"])))
    elif target == "combination":
        gold["task_sufficiency"]["complete_task_combinations"].pop()
    else:
        gold["limitations"][0]["statement"] = "altered"
    with pytest.raises((ValueError, KeyError)):
        m.validate(gold)


def test_overwrite_refusal(tmp_path: Path) -> None:
    existing, absent = tmp_path / "existing", tmp_path / "absent"
    existing.write_bytes(b"original")
    with pytest.raises(FileExistsError):
        m.write_new({absent: b"new", existing: b"replacement"})
    assert existing.read_bytes() == b"original"
    assert not absent.exists()


def test_support_bound_rejection() -> None:
    payload: Any = m.authenticate()[-1]
    span = {
        "origin": "TASK",
        "start": 0,
        "end": len(payload["task_text"]) + 1,
        "text": payload["task_text"],
    }
    with pytest.raises(ValueError, match="bounds"):
        m.validate_spans(span, payload)
