# Copyright (c) 2026
# ruff: noqa: E501
"""Freeze blinded Increment-25 judgments before mechanically joining origins."""

from __future__ import annotations

import hashlib
import json
from typing import TYPE_CHECKING, Final, cast

from experiments.purpose_relative_admission.validation_execution import (
    artifact_envelope,
    validate_artifact_envelope,
)
from experiments.purpose_relative_import.cases import UsefulnessJudgment

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

FROZEN_SCHEMA: Final = "devtools-increment-25-confirmation-frozen-judgments-v1"
MAPPING_SCHEMA: Final = "devtools-increment-25-confirmation-neutral-mapping-v1"
RESULT_SCHEMA: Final = "devtools-increment-25-confirmation-results-v1"
PROVENANCE: Final = (
    "independent-blinded-adjudication:parent-snapshot-task-and-resource-only"
)


def freeze_confirmation_judgments(
    *, blinded: Mapping[str, object], decisions: Mapping[str, object],
) -> tuple[dict[str, object], dict[str, object]]:
    """Require complete blinded judgments and return frozen and mapping envelopes."""
    package_identity = _digest(blinded)
    decision_cases = cast("dict[str, dict[str, dict[str, str]]]", decisions)
    blinded_cases = cast("list[dict[str, object]]", blinded["cases"])
    expected_case_ids = tuple(str(case["case_id"]) for case in blinded_cases)
    if set(decision_cases) != set(expected_case_ids):
        msg = "Judgment decisions must cover exactly the blinded confirmation cases."
        raise ValueError(msg)
    frozen_cases: list[dict[str, object]] = []
    mapping_cases: list[dict[str, object]] = []
    for case in blinded_cases:
        case_id = str(case["case_id"])
        resources = cast("list[dict[str, str]]", case["resources"])
        by_address = decision_cases[case_id]
        expected_addresses = tuple(resource["address"] for resource in resources)
        if set(by_address) != set(expected_addresses):
            msg = f"Judgments must cover exactly the blinded resources for {case_id}."
            raise ValueError(msg)
        records: list[dict[str, object]] = []
        mappings: list[dict[str, str]] = []
        for address in expected_addresses:
            decision = by_address[address]
            judgment = UsefulnessJudgment(decision["judgment"])
            rationale = decision["rationale"].strip()
            if not rationale:
                msg = f"Judgment rationale is empty for {case_id}."
                raise ValueError(msg)
            neutral_id = _neutral_id(
                package_identity=package_identity,
                case_id=case_id,
                address=address,
            )
            records.append(
                {
                    "neutral_id": neutral_id,
                    "judgment": judgment.value,
                    "rationale": rationale,
                    "candidate_origin_visible_to_adjudicator": False,
                    "provenance": PROVENANCE,
                },
            )
            mappings.append({"neutral_id": neutral_id, "address": address})
        frozen_cases.append({"case_id": case_id, "records": records})
        mapping_cases.append({"case_id": case_id, "mappings": mappings})
    frozen = artifact_envelope(
        schema=FROZEN_SCHEMA,
        payload={
            "blinded_package_identity": package_identity,
            "cases": frozen_cases,
        },
    )
    mapping = artifact_envelope(
        schema=MAPPING_SCHEMA,
        payload={
            "blinded_package_identity": package_identity,
            "cases": mapping_cases,
        },
    )
    audit_frozen_confirmation_judgments(frozen)
    return cast("dict[str, object]", frozen), cast("dict[str, object]", mapping)


def audit_frozen_confirmation_judgments(envelope: Mapping[str, object]) -> None:
    """Reject damaged, incomplete, origin-bearing, or non-three-state freezes."""
    if envelope.get("schema") != FROZEN_SCHEMA or not validate_artifact_envelope(
        envelope,
    ):
        msg = "Frozen confirmation judgment envelope is invalid."
        raise ValueError(msg)
    payload = cast("dict[str, object]", envelope["payload"])
    if set(payload) != {"blinded_package_identity", "cases"}:
        msg = "Frozen confirmation judgment payload fields are invalid."
        raise ValueError(msg)
    seen_ids: set[str] = set()
    for case in cast("list[dict[str, object]]", payload["cases"]):
        if set(case) != {"case_id", "records"}:
            msg = "Frozen confirmation case fields are invalid."
            raise ValueError(msg)
        for record in cast("list[dict[str, object]]", case["records"]):
            allowed = {
                "neutral_id",
                "judgment",
                "rationale",
                "candidate_origin_visible_to_adjudicator",
                "provenance",
            }
            if set(record) != allowed:
                msg = "Frozen confirmation record fields are invalid."
                raise ValueError(msg)
            neutral_id = str(record["neutral_id"])
            if neutral_id in seen_ids:
                msg = "Frozen confirmation judgment repeats a neutral identity."
                raise ValueError(msg)
            seen_ids.add(neutral_id)
            UsefulnessJudgment(str(record["judgment"]))
            if record["candidate_origin_visible_to_adjudicator"] is not False:
                msg = "Candidate origin contaminated blinded confirmation judgment."
                raise ValueError(msg)
            if record["provenance"] != PROVENANCE or not str(record["rationale"]).strip():
                msg = "Frozen confirmation judgment lacks rationale provenance."
                raise ValueError(msg)


def evaluate_confirmation(
    *,
    candidates: Mapping[str, object],
    blinded: Mapping[str, object],
    frozen: Mapping[str, object],
    mapping: Mapping[str, object],
) -> dict[str, object]:
    """Join already-frozen judgments to candidate origins and summarize mechanics."""
    audit_frozen_confirmation_judgments(frozen)
    if mapping.get("schema") != MAPPING_SCHEMA or not validate_artifact_envelope(mapping):
        msg = "Confirmation neutral mapping envelope is invalid."
        raise ValueError(msg)
    package_identity = _digest(blinded)
    frozen_payload = cast("dict[str, object]", frozen["payload"])
    mapping_payload = cast("dict[str, object]", mapping["payload"])
    if {
        str(frozen_payload["blinded_package_identity"]),
        str(mapping_payload["blinded_package_identity"]),
    } != {package_identity}:
        msg = "Confirmation judgment artifacts do not bind to the blinded package."
        raise ValueError(msg)
    candidate_cases = cast("list[dict[str, object]]", candidates["cases"])
    frozen_cases = cast("list[dict[str, object]]", frozen_payload["cases"])
    mapping_cases = cast("list[dict[str, object]]", mapping_payload["cases"])
    if not (
        tuple(case["case_id"] for case in candidate_cases)
        == tuple(case["case_id"] for case in frozen_cases)
        == tuple(case["case_id"] for case in mapping_cases)
    ):
        msg = "Confirmation cases differ across candidate, judgment, and mapping artifacts."
        raise ValueError(msg)
    results = [
        _evaluate_case(candidate=candidate, frozen=case_frozen, mapping=case_mapping)
        for candidate, case_frozen, case_mapping in zip(
            candidate_cases,
            frozen_cases,
            mapping_cases,
            strict=True,
        )
    ]
    return cast(
        "dict[str, object]",
        artifact_envelope(
            schema=RESULT_SCHEMA,
            payload={
                "candidate_identity": _digest(candidates),
                "blinded_package_identity": package_identity,
                "frozen_judgment_identity": str(frozen["content_identity"]),
                "cases": results,
                "aggregate": _aggregate(results),
            },
        ),
    )


def _evaluate_case(
    *, candidate: dict[str, object], frozen: dict[str, object], mapping: dict[str, object],
) -> dict[str, object]:
    records = cast("list[dict[str, object]]", frozen["records"])
    mappings = cast("list[dict[str, str]]", mapping["mappings"])
    address_by_id = {item["neutral_id"]: item["address"] for item in mappings}
    judgments = {
        address_by_id[str(record["neutral_id"])]: str(record["judgment"])
        for record in records
    }
    structural_items = cast("list[dict[str, object]]", candidate["structural_additions"])
    structural = tuple(str(item["address"]) for item in structural_items)
    matched = tuple(cast("list[str]", candidate["matched_lexical_additions"]))
    intersection = set(structural) & set(matched)
    structural_only = set(structural) - set(matched)
    lexical_only = set(matched) - set(structural)

    def selected(addresses: object, judgment: UsefulnessJudgment) -> list[str]:
        return [
            address
            for address in cast("set[str] | tuple[str, ...]", addresses)
            if judgments[address] == judgment.value
        ]

    structural_rank = {
        str(item["address"]): item["positive_lexical_rank"]
        for item in structural_items
    }
    return {
        "case_id": candidate["case_id"],
        "m": cast("dict[str, object]", candidate["capacity"])["m"],
        "structural_additions": list(structural),
        "matched_lexical_additions": list(matched),
        "overlap": sorted(intersection),
        "judgments_by_arm": {
            "structural": _counts(structural, judgments),
            "matched_lexical": _counts(matched, judgments),
        },
        "useful_structural_only": sorted(
            selected(structural_only, UsefulnessJudgment.USEFUL),
        ),
        "useful_matched_lexical_only": sorted(
            selected(lexical_only, UsefulnessJudgment.USEFUL),
        ),
        "useful_overlap": sorted(selected(intersection, UsefulnessJudgment.USEFUL)),
        "useful_structural_lexical_ranks": [
            {"address": address, "positive_lexical_rank": structural_rank[address]}
            for address in structural
            if judgments[address] == UsefulnessJudgment.USEFUL.value
        ],
        "useful_structural_without_positive_lexical_rank": [
            address
            for address in structural
            if judgments[address] == UsefulnessJudgment.USEFUL.value
            and structural_rank[address] is None
        ],
        "resolution_diagnostics": candidate["resolution_diagnostics"],
        "lexical_exhausted": cast("dict[str, object]", candidate["capacity"])[
            "lexical_exhausted"
        ],
    }


def _counts(
    addresses: tuple[str, ...], judgments: Mapping[str, str],
) -> dict[str, int]:
    return {
        judgment.value: sum(judgments[address] == judgment.value for address in addresses)
        for judgment in UsefulnessJudgment
    }


def _aggregate(results: list[dict[str, object]]) -> dict[str, object]:
    structural = sum(len(cast("list[str]", result["structural_additions"])) for result in results)
    matched = sum(len(cast("list[str]", result["matched_lexical_additions"])) for result in results)
    overlap = sum(len(cast("list[str]", result["overlap"])) for result in results)
    structural_counts = {
        judgment.value: sum(
            cast("dict[str, int]", cast("dict[str, object]", result["judgments_by_arm"])["structural"])[judgment.value]
            for result in results
        )
        for judgment in UsefulnessJudgment
    }
    lexical_counts = {
        judgment.value: sum(
            cast("dict[str, int]", cast("dict[str, object]", result["judgments_by_arm"])["matched_lexical"])[judgment.value]
            for result in results
        )
        for judgment in UsefulnessJudgment
    }
    return {
        "case_count": len(results),
        "cases_with_structural_additions": sum(
            cast("int", result["m"]) > 0 for result in results
        ),
        "distinct_structural_additions": structural,
        "matched_lexical_additions": matched,
        "overlap": overlap,
        "lexical_exhaustion_cases": [result["case_id"] for result in results if result["lexical_exhausted"]],
        "structural_judgments": structural_counts,
        "matched_lexical_judgments": lexical_counts,
        "useful_overlap": sum(len(cast("list[str]", result["useful_overlap"])) for result in results),
        "useful_structural_only": sum(len(cast("list[str]", result["useful_structural_only"])) for result in results),
        "useful_matched_lexical_only": sum(len(cast("list[str]", result["useful_matched_lexical_only"])) for result in results),
        "useful_structural_without_positive_lexical_rank": sum(len(cast("list[str]", result["useful_structural_without_positive_lexical_rank"])) for result in results),
    }


def write_json(*, path: Path, value: Mapping[str, object]) -> None:
    """Write one deterministic judgment/evaluation artifact."""
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _neutral_id(*, package_identity: str, case_id: str, address: str) -> str:
    return "resource-" + hashlib.sha256(
        f"{package_identity}|{case_id}|{address}".encode(),
    ).hexdigest()[:16]


def _digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(),
    ).hexdigest()
