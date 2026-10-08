"""Self-contained exact replay and fail-closed checks; no treatment imports."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import pytest

import materialize_reviewed_c5 as m


@pytest.fixture(scope="module")
def data() -> dict[str, Any]:
    return m.source_inputs()


def test_complete_replay(data: dict[str, Any]) -> None:
    m.validate_completed(m.ROOT, data)
    result = m.build(data)
    assert len(result["mappings"]) == 576
    assert result["provenance"]["agreed_pairs"] == 544
    assert result["provenance"]["disputed_pairs"] == 32
    assert result["provenance"]["shared_direct_rationales"] == 12
    assert len(result["collective_coverage"]) == 7


def test_exact_inheritance_and_decision_application(data: dict[str, Any]) -> None:
    result = m.build(data)
    primary = m.index(data["primary"]["mappings"], "need", "unit")
    independent = m.index(data["independent"]["pairs"], "need", "unit")
    decisions = {
        (r["subject"]["need"], r["subject"]["unit"]): r
        for r in data["decision"]["decisions"]
        if r["kind"] in {"PAIR_LABEL", "DIRECT_RATIONALE"}
    }
    for row in result["mappings"]:
        key = row["need"], row["unit"]
        if primary[key]["label"] == independent[key]["label"]:
            assert row["label"] == primary[key]["label"]
            assert row["label_provenance"]["origin"] == "INHERITED_AGREEMENT"
        else:
            assert row["label"] == decisions[key]["payload"]["label"]
            assert row["label_provenance"]["origin"] == "RECONCILED_DISPUTE"
        if key in decisions:
            assert all(row[k] == v for k, v in decisions[key]["payload"].items())


@pytest.mark.parametrize(
    "kind,field,value",
    [
        ("UNIT_STATUS", "status", "AMBIGUOUS_ONLY"),
        ("NEED_CLASSIFICATION", "classification", "UNNECESSARY"),
        ("ALTERNATIVE_COMPLETENESS", "strict_direct_complete", True),
    ],
)
def test_contradictory_decision_refused(
    data: dict[str, Any], kind: str, field: str, value: Any
) -> None:
    changed = copy.deepcopy(data)
    row = next(r for r in changed["decision"]["decisions"] if r["kind"] == kind)
    row["payload"][field] = value
    with pytest.raises(AssertionError, match="contradiction"):
        m.build(changed)


@pytest.mark.parametrize("mutation", ["duplicate", "missing", "unexpected"])
def test_incomplete_pair_frame_refused(data: dict[str, Any], mutation: str) -> None:
    changed = copy.deepcopy(data)
    rows = changed["primary"]["mappings"]
    if mutation == "duplicate":
        rows.append(copy.deepcopy(rows[0]))
    elif mutation == "missing":
        rows.pop()
    else:
        rows[0]["unit"] = "unexpected-unit"
    with pytest.raises(AssertionError):
        m.build(changed)


def test_agreement_cannot_be_reconciled(data: dict[str, Any]) -> None:
    changed = copy.deepcopy(data)
    changed["decision"]["decisions"].append(
        {
            "kind": "PAIR_LABEL",
            "subject": {
                "need": data["primary"]["mappings"][0]["need"],
                "unit": data["primary"]["mappings"][0]["unit"],
            },
        }
    )
    with pytest.raises(AssertionError):
        m.build(changed)


def test_collective_member_mutation_refused(data: dict[str, Any]) -> None:
    changed = copy.deepcopy(data)
    row = next(
        r
        for r in changed["decision"]["decisions"]
        if r["kind"] == "COLLECTIVE_COVERAGE"
    )
    row["payload"]["sets"][0]["needs"].pop()
    with pytest.raises(AssertionError):
        m.build(changed)


def test_exclusive_publication_and_tamper_detection(
    data: dict[str, Any], tmp_path: Path
) -> None:
    m.publish(tmp_path, data)
    m.validate_completed(tmp_path, data)
    original = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    with pytest.raises(AssertionError, match="OVERWRITE_REFUSED"):
        m.publish(tmp_path, data)
    assert original == {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    (tmp_path / m.NAMES[0]).write_bytes(b"tampered")
    with pytest.raises(AssertionError, match="replay mismatch"):
        m.validate_completed(tmp_path, data)


def test_partial_prior_publication_refused(
    data: dict[str, Any], tmp_path: Path
) -> None:
    (tmp_path / m.NAMES[-1]).write_text("prior", encoding="utf-8")
    with pytest.raises(AssertionError, match="OVERWRITE_REFUSED"):
        m.publish(tmp_path, data)
    assert len(list(tmp_path.iterdir())) == 1


@pytest.mark.parametrize("field", sorted(m.DENIED))
def test_forbidden_field_rejection(field: str) -> None:
    with pytest.raises(AssertionError, match="forbidden field"):
        m.reject_forbidden({"nested": [{field: "synthetic forbidden marker"}]})


def test_duplicate_json_refused() -> None:
    with pytest.raises(AssertionError, match="duplicate JSON field"):
        m.load(b'{"label":1,"label":2}')


def test_strict_precedence() -> None:
    assert m.unit_status(set()) == "UNCOVERED"
    assert m.unit_status({"DOES_NOT_COVER", "AMBIGUOUS"}) == "AMBIGUOUS_ONLY"
    assert m.unit_status({"AMBIGUOUS", "PARTIALLY_COVERS"}) == "PARTIAL_ONLY"
    assert m.unit_status(set(m.LABELS)) == "COVERED"
