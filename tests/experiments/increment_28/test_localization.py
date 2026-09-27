# Copyright (c) 2026
# ruff: noqa: E501, FBT001, PLR2004
"""Outcome-blind location control and fixed-population validation."""

from __future__ import annotations

import hashlib
import json

import pytest

from experiments.increment_27.depth_diagnostic import canonical_json_bytes
from experiments.increment_28.import_use import ROOT27
from experiments.increment_28.localization.evidence import (
    EVIDENCE_NAME,
    FREEZE_NAME,
    ROOT28,
    _candidate_state,
    build_freeze,
    classify_localization,
    derive_evidence,
)

WINDOW = {"char_start": 10, "char_end": 20}


def _occurrence(start: int, end: int) -> dict[str, object]:
    return {"char_span": [start, end], "span_utf8": [1, start, 1, end], "text": "x"}


@pytest.mark.parametrize(
    ("inside", "outside", "uncertain", "expected"),
    [
        (True, False, False, "IN_WINDOW_ONLY"),
        (True, True, False, "BOTH"),
        (False, True, False, "OUTSIDE_WINDOW_ONLY"),
        (True, False, True, "INDETERMINATE"),
        (False, True, True, "INDETERMINATE"),
        (True, True, True, "BOTH"),
    ],
)
def test_qualified_read_location(
    inside: bool, outside: bool, uncertain: bool, expected: str,
) -> None:
    """Location changes only where a previously qualified read occurs."""
    occurrences = ([_occurrence(10, 12)] if inside else []) + ([_occurrence(0, 2)] if outside else [])
    full = {
        "state": "SUPPORTED", "reason": None, "local_binding": "name",
        "occurrences": occurrences,
        "uncertain_occurrences": [_occurrence(3, 4)] if uncertain else [],
    }
    observed = classify_localization(full, WINDOW)
    assert observed["state"] == expected
    assert observed["known_inside"] == inside
    assert observed["known_outside"] == outside


def test_unknown_and_partial_boundary_never_become_negative() -> None:
    """Unresolved binding and split window spans cannot prove absence."""
    unknown = classify_localization(
        {"state": "INDETERMINATE", "reason": "shadowed", "occurrences": []}, WINDOW,
    )
    partial = classify_localization(
        {"state": "SUPPORTED", "reason": None, "occurrences": [_occurrence(8, 12)], "uncertain_occurrences": []}, WINDOW,
    )
    none = classify_localization(
        {"state": "NO_QUALIFYING_OCCURRENCE", "reason": None, "occurrences": []}, WINDOW,
    )
    assert unknown["state"] == partial["state"] == "INDETERMINATE"
    assert partial["partial_boundary_occurrences"]
    assert none["state"] == "NO_QUALIFYING_OCCURRENCE"


def test_candidate_aggregation_preserves_uncertainty() -> None:
    """An outside-only candidate requires adequate coverage of every support."""
    outside = {"known_inside": False, "known_outside": True, "unresolved": False}
    unknown = {"known_inside": False, "known_outside": False, "unresolved": True}
    inside = {"known_inside": True, "known_outside": False, "unresolved": False}
    assert _candidate_state([outside]) == "OUTSIDE_WINDOW_ONLY"
    assert _candidate_state([outside, unknown]) == "INDETERMINATE"
    assert _candidate_state([inside, outside, unknown]) == "BOTH"


def test_real_artifact_reproduces_fixed_supports_without_outcomes() -> None:
    """Re-derivation and identity checks bind every case and support to I28."""
    frozen = json.loads((ROOT28 / FREEZE_NAME).read_text(encoding="utf-8"))
    path = ROOT28 / EVIDENCE_NAME
    evidence = json.loads(path.read_text(encoding="utf-8"))
    original = json.loads((ROOT28 / "import_use_evidence.json").read_text(encoding="utf-8"))
    assert frozen == build_freeze()
    assert evidence == derive_evidence(repository_root=ROOT27.parents[1])
    assert evidence["freeze_identity"] == frozen["content_identity"]
    assert evidence["import_use_evidence_identity"] == original["content_identity"]
    assert evidence["content_identity"] == hashlib.sha256(canonical_json_bytes({key: value for key, value in evidence.items() if key != "content_identity"})).hexdigest()
    assert path.read_bytes() == (json.dumps(evidence, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    assert [case["case_id"] for case in evidence["cases"]] == frozen["payload"]["development_case_ids"]
    assert len(evidence["cases"]) == 24
    assert not set(frozen["payload"]["heldout_case_ids_sealed"]) & {case["case_id"] for case in evidence["cases"]}
    assert evidence["new_candidates"] == evidence["new_judgments"] == 0
    assert evidence["usefulness_outcomes_loaded"] is False
    assert evidence["heldout_executed"] is False
    for prior_case, case in zip(original["cases"], evidence["cases"], strict=True):
        assert prior_case["case_id"] == case["case_id"]
        assert prior_case["incoming_only_addresses"] == case["incoming_only_addresses"]
        prior_pairs = {row["address"]: row for row in prior_case["outgoing"]}
        assert set(prior_pairs) == {row["address"] for row in case["outgoing"]}
        for row in case["outgoing"]:
            before = prior_pairs[row["address"]]
            assert row["support_count"] == before["existing_support_count"]
            assert [support["relation_identity"] for support in row["supports"]] == [support["relation_identity"] for support in before["supports"]]
            assert [support["seed_address"] for support in row["supports"]] == [support["seed_address"] for support in before["supports"]]
            assert sum(row["state_counts"].values()) == row["support_count"]
    assert evidence["summary"]["fixed_union_pairs"] == 109
    assert evidence["summary"]["outgoing"]["candidate_pairs"] == 99
    assert evidence["summary"]["outgoing"]["support_count"] == 499


def test_preoutcome_artifact_has_no_usefulness_states() -> None:
    """Candidate evidence is frozen independently of usefulness outcomes."""
    source = (ROOT28 / EVIDENCE_NAME).read_text(encoding="utf-8")
    for forbidden in ('"USEFUL"', '"NOT_USEFUL"', '"UNJUDGED"', '"judgment"'):
        assert forbidden not in source
