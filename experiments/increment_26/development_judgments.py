# Copyright (c) 2026
# ruff: noqa: C901, PLR0912, PLR0913
"""Freeze Increment-26 development judgments without candidate-origin access."""

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

SCHEMA: Final = "devtools-increment-26-development-frozen-judgments-v1"
INPUT_SHA256: Final = "7df8065b63f896e2e16d5aea29c93dd7fd46e3321ac820a656eeee795f71d69d"
EVIDENCE_IDENTITY: Final = (
    "330a9bec94a023d1033ece21f885cdaca122f70eb7d3acb02c4588e948fb4ce2"
)
FREEZE_IDENTITY: Final = (
    "a8d57b68a8043b88300c8ea5f28d12266a1d74f7aa9e9a09e323a4c6ba9f22c1"
)
DEVELOPMENT_CASE_IDS: Final = (
    "i25-66ed2049de72",
    "i25-858bfa85787e",
    "i25-6f304a8c737c",
    "i25-bb9f807bcd61",
    "i25-0f7a13667ef3",
    "i25-739c82bd3398",
    "i25-9efe3dc31e80",
    "i25-6b0e9c52fb26",
)
PAIR_COUNT: Final = 69
NEW_PROVENANCE: Final = "NEW_INCREMENT_26"
REUSED_PROVENANCE: Final = "REUSED_INCREMENT_25"
USEFULNESS_SEMANTICS: Final = "purpose-relative-three-state-v1"


def prior_judgment_matches(
    *,
    information_need: Mapping[str, object],
    parent_snapshot: str,
    address: str,
    usefulness_semantics: str,
    prior_information_need: Mapping[str, object],
    prior_parent_snapshot: str,
    prior_address: str,
    prior_usefulness_semantics: str,
) -> bool:
    """Apply the frozen four-part prior-judgment identity rule."""
    return (
        information_need == prior_information_need
        and parent_snapshot == prior_parent_snapshot
        and address == prior_address
        and usefulness_semantics == prior_usefulness_semantics
    )


def freeze_development_judgments(
    *,
    blinded_bytes: bytes,
    decisions: Mapping[str, Mapping[str, Mapping[str, str]]],
) -> dict[str, object]:
    """Freeze complete neutral decisions against the committed blinded input."""
    if hashlib.sha256(blinded_bytes).hexdigest() != INPUT_SHA256:
        msg = "Judgment input differs from the committed canonical artifact."
        raise ValueError(msg)
    blinded = json.loads(blinded_bytes)
    if not isinstance(blinded, dict) or set(blinded) != {
        "schema",
        "scope",
        "execution_identity",
        "cases",
    }:
        msg = "Blinded judgment input structure is invalid."
        raise ValueError(msg)
    if blinded["execution_identity"] != EVIDENCE_IDENTITY:
        msg = "Blinded input does not bind the canonical evidence identity."
        raise ValueError(msg)
    cases = cast("list[dict[str, object]]", blinded["cases"])
    if tuple(case["case_id"] for case in cases) != DEVELOPMENT_CASE_IDS:
        msg = "Blinded input includes missing, extra, or sealed cases."
        raise ValueError(msg)
    if set(decisions) != set(DEVELOPMENT_CASE_IDS):
        msg = "Decisions must cover exactly the frozen development cases."
        raise ValueError(msg)
    frozen_cases: list[dict[str, object]] = []
    seen_pairs: set[tuple[str, str]] = set()
    for case in cases:
        case_id = str(case["case_id"])
        resources = cast("list[dict[str, str]]", case["resources"])
        addresses = tuple(resource["address"] for resource in resources)
        if len(set(addresses)) != len(addresses) or set(decisions[case_id]) != set(
            addresses,
        ):
            msg = f"Decisions must cover each neutral resource once in {case_id}."
            raise ValueError(msg)
        records: list[dict[str, object]] = []
        for address in addresses:
            pair = (case_id, address)
            if pair in seen_pairs:
                msg = "Neutral judgment pair is duplicated."
                raise ValueError(msg)
            seen_pairs.add(pair)
            decision = decisions[case_id][address]
            if set(decision) != {"judgment", "rationale", "provenance"}:
                msg = "Decision includes unexpected or missing fields."
                raise ValueError(msg)
            judgment = UsefulnessJudgment(decision["judgment"])
            rationale = decision["rationale"].strip()
            provenance = decision["provenance"]
            if not rationale or provenance != NEW_PROVENANCE:
                msg = "Judgment lacks a rationale or valid provenance."
                raise ValueError(msg)
            records.append(
                {
                    "neutral_id": _neutral_id(case_id, address),
                    "address": address,
                    "judgment": judgment.value,
                    "rationale": rationale,
                    "provenance": provenance,
                },
            )
        frozen_cases.append({"case_id": case_id, "records": records})
    if len(seen_pairs) != PAIR_COUNT:
        msg = "Judgment pair count differs from the frozen 69-pair population."
        raise ValueError(msg)
    frozen = cast(
        "dict[str, object]",
        artifact_envelope(
            schema=SCHEMA,
            payload={
                "increment_26_freeze_identity": FREEZE_IDENTITY,
                "blinded_input_sha256": INPUT_SHA256,
                "candidate_evidence_identity": EVIDENCE_IDENTITY,
                "pair_count": PAIR_COUNT,
                "cases": frozen_cases,
            },
        ),
    )
    audit_frozen_development_judgments(frozen, blinded_bytes=blinded_bytes)
    return frozen


def audit_frozen_development_judgments(
    frozen: Mapping[str, object],
    *,
    blinded_bytes: bytes,
) -> None:
    """Prove complete coverage, identity binding, and origin blindness."""
    if frozen.get("schema") != SCHEMA or not validate_artifact_envelope(frozen):
        msg = "Frozen development judgment envelope is invalid."
        raise ValueError(msg)
    if hashlib.sha256(blinded_bytes).hexdigest() != INPUT_SHA256:
        msg = "Canonical blinded input hash is invalid."
        raise ValueError(msg)
    blinded = json.loads(blinded_bytes)
    if blinded.get("execution_identity") != EVIDENCE_IDENTITY:
        msg = "Canonical evidence identity is invalid."
        raise ValueError(msg)
    payload = cast("dict[str, object]", frozen["payload"])
    if set(payload) != {
        "increment_26_freeze_identity",
        "blinded_input_sha256",
        "candidate_evidence_identity",
        "pair_count",
        "cases",
    } or (
        payload["increment_26_freeze_identity"] != FREEZE_IDENTITY
        or payload["blinded_input_sha256"] != INPUT_SHA256
        or payload["candidate_evidence_identity"] != EVIDENCE_IDENTITY
        or payload["pair_count"] != PAIR_COUNT
    ):
        msg = "Frozen development judgment binding is invalid."
        raise ValueError(msg)
    blinded_cases = blinded["cases"]
    frozen_cases = cast("list[dict[str, object]]", payload["cases"])
    if tuple(case["case_id"] for case in frozen_cases) != DEVELOPMENT_CASE_IDS:
        msg = "Frozen judgments include missing, extra, or sealed cases."
        raise ValueError(msg)
    if tuple(case["case_id"] for case in blinded_cases) != DEVELOPMENT_CASE_IDS:
        msg = "Blinded input includes missing, extra, or sealed cases."
        raise ValueError(msg)
    seen_pairs: set[tuple[str, str]] = set()
    for blind_case, case in zip(blinded_cases, frozen_cases, strict=True):
        if set(case) != {"case_id", "records"}:
            msg = "Frozen case fields are invalid."
            raise ValueError(msg)
        expected = [item["address"] for item in blind_case["resources"]]
        records = cast("list[dict[str, object]]", case["records"])
        if [record.get("address") for record in records] != expected:
            msg = "Frozen resource coverage or order differs from blinded input."
            raise ValueError(msg)
        for record in records:
            if set(record) != {
                "neutral_id",
                "address",
                "judgment",
                "rationale",
                "provenance",
            }:
                msg = "Frozen record leaks origin or omits required fields."
                raise ValueError(msg)
            address = str(record["address"])
            pair = (str(case["case_id"]), address)
            if pair in seen_pairs or record["neutral_id"] != _neutral_id(*pair):
                msg = "Frozen neutral pair is duplicated or misidentified."
                raise ValueError(msg)
            seen_pairs.add(pair)
            UsefulnessJudgment(str(record["judgment"]))
            if (
                not str(record["rationale"]).strip()
                or record["provenance"] != NEW_PROVENANCE
            ):
                msg = "Frozen judgment rationale or provenance is invalid."
                raise ValueError(msg)
    if len(seen_pairs) != PAIR_COUNT:
        msg = "Frozen development judgment population is incomplete."
        raise ValueError(msg)


def _neutral_id(case_id: str, address: str) -> str:
    value = json.dumps([INPUT_SHA256, case_id, address], separators=(",", ":"))
    return hashlib.sha256(value.encode()).hexdigest()
