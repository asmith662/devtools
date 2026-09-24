# Copyright (c) 2026
"""Falsify Increment-26 blinded development judgment freeze boundaries."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, cast

import pytest

from experiments.increment_26.development_judgments import (
    DEVELOPMENT_CASE_IDS,
    EVIDENCE_IDENTITY,
    FREEZE_IDENTITY,
    INPUT_SHA256,
    NEW_PROVENANCE,
    PAIR_COUNT,
    audit_frozen_development_judgments,
    freeze_development_judgments,
    prior_judgment_matches,
)
from experiments.purpose_relative_admission.validation_execution import (
    artifact_envelope,
)

_ROOT = Path("experiments/increment_26")


def _input() -> bytes:
    return (_ROOT / "development_judgment_input.json").read_bytes()


def _frozen() -> dict[str, Any]:
    return cast(
        "dict[str, Any]",
        json.loads(
            (_ROOT / "development_frozen_judgments.json").read_text(
                encoding="utf-8",
            ),
        ),
    )


def _decisions() -> dict[str, dict[str, dict[str, str]]]:
    frozen = _frozen()
    return {
        case["case_id"]: {
            record["address"]: {
                "judgment": record["judgment"],
                "rationale": record["rationale"],
                "provenance": record["provenance"],
            }
            for record in case["records"]
        }
        for case in frozen["payload"]["cases"]
    }


def _reseal(frozen: dict[str, Any]) -> dict[str, Any]:
    return artifact_envelope(schema=str(frozen["schema"]), payload=frozen["payload"])


def test_canonical_freeze_covers_exact_neutral_population_without_origins() -> None:
    """The committed input and freeze bind exactly eight cases and 69 pairs."""
    frozen = _frozen()
    audit_frozen_development_judgments(frozen, blinded_bytes=_input())
    payload = frozen["payload"]
    assert payload["increment_26_freeze_identity"] == FREEZE_IDENTITY
    assert payload["blinded_input_sha256"] == INPUT_SHA256
    assert payload["candidate_evidence_identity"] == EVIDENCE_IDENTITY
    assert payload["pair_count"] == PAIR_COUNT
    assert tuple(case["case_id"] for case in payload["cases"]) == DEVELOPMENT_CASE_IDS
    records = [record for case in payload["cases"] for record in case["records"]]
    assert len(records) == PAIR_COUNT
    assert {record["judgment"] for record in records} == {
        "useful",
        "not-useful",
        "unjudged",
    }
    assert {record["provenance"] for record in records} == {NEW_PROVENANCE}
    assert all(
        set(record)
        == {
            "neutral_id",
            "address",
            "judgment",
            "rationale",
            "provenance",
        }
        for record in records
    )
    assert not any(
        term in json.dumps(frozen).lower()
        for term in (
            "semantic_rank",
            "lexical_rank",
            "semantic_score",
            "lexical_score",
            "winning_chunk",
        )
    )


def test_freeze_rejects_missing_duplicate_and_extra_decisions() -> None:
    """No neutral pair can be omitted, repeated, or added."""
    decisions = _decisions()
    case = DEVELOPMENT_CASE_IDS[0]
    address = next(iter(decisions[case]))
    missing = copy.deepcopy(decisions)
    missing[case].pop(address)
    with pytest.raises(ValueError, match="cover each neutral resource"):
        freeze_development_judgments(blinded_bytes=_input(), decisions=missing)
    extra = copy.deepcopy(decisions)
    extra[case]["extra.py"] = extra[case][address]
    with pytest.raises(ValueError, match="cover each neutral resource"):
        freeze_development_judgments(blinded_bytes=_input(), decisions=extra)
    duplicated = copy.deepcopy(_frozen())
    duplicated["payload"]["cases"][0]["records"][1] = copy.deepcopy(
        duplicated["payload"]["cases"][0]["records"][0],
    )
    with pytest.raises(ValueError, match="coverage or order"):
        audit_frozen_development_judgments(_reseal(duplicated), blinded_bytes=_input())


def test_three_states_and_provenance_are_enforced() -> None:
    """Uncertainty remains separate; invalid or unsupported reuse cannot pass."""
    decisions = _decisions()
    case = DEVELOPMENT_CASE_IDS[0]
    address = next(iter(decisions[case]))
    decisions[case][address]["judgment"] = "maybe"
    with pytest.raises(ValueError, match="maybe"):
        freeze_development_judgments(blinded_bytes=_input(), decisions=decisions)
    decisions = _decisions()
    decisions[case][address]["provenance"] = "REUSED_INCREMENT_25"
    with pytest.raises(ValueError, match="provenance"):
        freeze_development_judgments(blinded_bytes=_input(), decisions=decisions)


@pytest.mark.parametrize("mismatch", ["need", "snapshot", "address", "semantics"])
def test_prior_reuse_requires_all_four_identity_components(mismatch: str) -> None:
    """A prior decision can be reused only for the identical judgment unit."""
    current: dict[str, Any] = {
        "information_need": {"purpose": "p", "lexical_query": "q"},
        "parent_snapshot": "sha",
        "address": "a.py",
        "usefulness_semantics": "purpose-relative-three-state-v1",
    }
    prior = {f"prior_{key}": value for key, value in current.items()}
    assert prior_judgment_matches(**current, **prior)
    key = {
        "need": "prior_information_need",
        "snapshot": "prior_parent_snapshot",
        "address": "prior_address",
        "semantics": "prior_usefulness_semantics",
    }[mismatch]
    prior[key] = "different"
    assert not prior_judgment_matches(**current, **prior)


def test_actual_increment_25_frozen_population_has_no_reusable_pair() -> None:
    """The earlier blinded confirmation judgments have no matching need and parent."""
    prior_root = Path("experiments/increment_25")
    prior_input = json.loads(
        (prior_root / "confirmation_judgment_input.json").read_text(encoding="utf-8"),
    )
    prior_frozen = json.loads(
        (prior_root / "confirmation_frozen_judgments.json").read_text(
            encoding="utf-8",
        ),
    )
    assert {case["case_id"] for case in prior_input["cases"]} == {
        case["case_id"] for case in prior_frozen["payload"]["cases"]
    }
    current_input = json.loads(_input())

    def pair_keys(value: dict[str, Any]) -> set[tuple[str, str, str, str]]:
        return {
            (
                case["task"]["purpose"],
                case["task"]["lexical_query"],
                case["task"]["parent_snapshot_sha"],
                resource["address"],
            )
            for case in value["cases"]
            for resource in case["resources"]
        }

    assert not pair_keys(current_input) & pair_keys(prior_input)


def test_origin_leak_and_sealed_case_fail_audit() -> None:
    """Even a correctly rehashed artifact cannot introduce forbidden evidence."""
    leaked = copy.deepcopy(_frozen())
    leaked["payload"]["cases"][0]["records"][0]["semantic_rank"] = 1
    with pytest.raises(ValueError, match="leaks origin"):
        audit_frozen_development_judgments(_reseal(leaked), blinded_bytes=_input())
    sealed = copy.deepcopy(_frozen())
    sealed["payload"]["cases"][0]["case_id"] = "i25-confirmation"
    with pytest.raises(ValueError, match="sealed cases"):
        audit_frozen_development_judgments(_reseal(sealed), blinded_bytes=_input())


def test_identity_binding_and_serialization_are_deterministic() -> None:
    """The same blinded decisions reproduce the exact committed artifact bytes."""
    first = freeze_development_judgments(blinded_bytes=_input(), decisions=_decisions())
    second = freeze_development_judgments(
        blinded_bytes=_input(), decisions=_decisions(),
    )
    serialized = json.dumps(first, indent=2, sort_keys=True) + "\n"
    assert first == second == _frozen()
    assert (
        serialized.encode()
        == (_ROOT / "development_frozen_judgments.json").read_bytes()
    )
    damaged = cast("dict[str, Any]", copy.deepcopy(first))
    damaged["payload"]["candidate_evidence_identity"] = "other"
    with pytest.raises(ValueError, match="binding"):
        audit_frozen_development_judgments(_reseal(damaged), blinded_bytes=_input())
    with pytest.raises(ValueError, match="input differs"):
        freeze_development_judgments(blinded_bytes=b"{}", decisions=_decisions())
