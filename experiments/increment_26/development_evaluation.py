# Copyright (c) 2026
# ruff: noqa: C901, PLR0912, PLR0915
"""Join frozen development judgments to retained candidate origins only."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Final, cast

from experiments.increment_26.development_judgments import (
    DEVELOPMENT_CASE_IDS,
    EVIDENCE_IDENTITY,
    FREEZE_IDENTITY,
    INPUT_SHA256,
    PAIR_COUNT,
    _neutral_id,
    audit_frozen_development_judgments,
)
from experiments.purpose_relative_admission.validation_execution import (
    artifact_envelope,
)
from experiments.purpose_relative_import.cases import UsefulnessJudgment

SCHEMA: Final = "devtools-increment-26-development-results-v1"
CANDIDATE_SCHEMA: Final = "devtools-increment-26-development-candidates-v1"
CANDIDATE_SHA256: Final = (
    "3b78cd07360f277523ca195401d1bc322ad28c1d7e03c1ea569490b87afa277d"
)
JUDGMENT_SHA256: Final = (
    "1bf9ace759a876998a7de4581bd94bcc9f1347da8bfc5632dc43ae7789df8baa"
)
JUDGMENT_IDENTITY: Final = (
    "36c4ab749c8829750eb5fc47bef0125ac45d2e481626b277cb2510061c510fc8"
)
SURFACES: Final = (
    "semantic",
    "lexical",
    "overlap",
    "semantic_only",
    "lexical_only",
)
LABELS: Final = tuple(judgment.value for judgment in UsefulnessJudgment)
_ROOT = Path("experiments/increment_26")


def evaluate_development(
    *,
    candidate_bytes: bytes,
    judgment_bytes: bytes,
    blinded_input_bytes: bytes,
) -> dict[str, Any]:
    """Evaluate the exact canonical development artifacts without new judgment."""
    if hashlib.sha256(candidate_bytes).hexdigest() != CANDIDATE_SHA256:
        msg = "Candidate evidence differs from the canonical development artifact."
        raise ValueError(msg)
    if hashlib.sha256(judgment_bytes).hexdigest() != JUDGMENT_SHA256:
        msg = "Frozen judgments differ from the committed artifact."
        raise ValueError(msg)
    if hashlib.sha256(blinded_input_bytes).hexdigest() != INPUT_SHA256:
        msg = "Blinded input differs from the canonical artifact."
        raise ValueError(msg)
    candidates = cast("dict[str, Any]", json.loads(candidate_bytes))
    judgments = cast("dict[str, Any]", json.loads(judgment_bytes))
    blinded = cast("dict[str, Any]", json.loads(blinded_input_bytes))
    audit_frozen_development_judgments(judgments, blinded_bytes=blinded_input_bytes)
    if judgments["content_identity"] != JUDGMENT_IDENTITY:
        msg = "Frozen judgment identity is invalid."
        raise ValueError(msg)
    if (
        candidates.get("schema") != CANDIDATE_SCHEMA
        or candidates.get("execution_identity") != EVIDENCE_IDENTITY
        or candidates.get("execution", {}).get("freeze_identity") != FREEZE_IDENTITY
        or candidates.get("execution", {}).get("mode") != "development-only"
        or candidates.get("execution", {}).get("case_count")
        != len(DEVELOPMENT_CASE_IDS)
    ):
        msg = "Candidate evidence does not bind the frozen development execution."
        raise ValueError(msg)
    candidate_cases = candidates["cases"]
    judgment_cases = judgments["payload"]["cases"]
    blinded_cases = blinded["cases"]
    if any(
        tuple(case["case_id"] for case in cases) != DEVELOPMENT_CASE_IDS
        for cases in (candidate_cases, judgment_cases, blinded_cases)
    ):
        msg = "Development artifacts include missing, extra, or sealed cases."
        raise ValueError(msg)
    results = [
        evaluate_case(candidate, judgment, blind)
        for candidate, judgment, blind in zip(
            candidate_cases,
            judgment_cases,
            blinded_cases,
            strict=True,
        )
    ]
    aggregate = _aggregate(results)
    return artifact_envelope(
        schema=SCHEMA,
        payload={
            "increment_26_freeze_identity": FREEZE_IDENTITY,
            "candidate_evidence_sha256": CANDIDATE_SHA256,
            "candidate_evidence_identity": EVIDENCE_IDENTITY,
            "frozen_judgment_sha256": JUDGMENT_SHA256,
            "frozen_judgment_identity": JUDGMENT_IDENTITY,
            "blinded_input_sha256": INPUT_SHA256,
            "cases": results,
            "aggregate": aggregate,
        },
    )


def evaluate_case(
    candidate: dict[str, Any],
    judgment: dict[str, Any],
    blind: dict[str, Any],
) -> dict[str, Any]:
    """Account for one already-frozen neutral case and its two retained arms."""
    case_id = candidate["case_id"]
    if case_id != judgment["case_id"] or case_id != blind["case_id"]:
        msg = "Candidate and frozen judgment case identities differ."
        raise ValueError(msg)
    need = candidate["information_need"]
    task = blind["task"]
    if (
        need != {"purpose": task["purpose"], "lexical_query": task["lexical_query"]}
        or candidate["parent_snapshot_sha"] != task["parent_snapshot_sha"]
    ):
        msg = "Candidate InformationNeed or parent snapshot differs from the blind."
        raise ValueError(msg)
    semantic = candidate["semantic_candidates"]
    lexical = candidate["lexical_candidates"]
    semantic_addresses = [item["address"] for item in semantic]
    lexical_addresses = [item["address"] for item in lexical]
    n = candidate["capacity"]["n"]
    if (
        len(semantic_addresses) != n
        or len(lexical_addresses) != n
        or len(set(semantic_addresses)) != n
        or len(set(lexical_addresses)) != n
    ):
        msg = "Candidate arms violate matched distinct-resource capacity."
        raise ValueError(msg)
    if any(
        item["score"] <= 0 or item["rank"] != index
        for index, item in enumerate(lexical, 1)
    ):
        msg = "Lexical arm has a nonpositive score or invalid native rank."
        raise ValueError(msg)
    lexical_set = set(lexical_addresses)
    semantic_set = set(semantic_addresses)
    surfaces = {
        "semantic": semantic_addresses,
        "lexical": lexical_addresses,
        "overlap": [
            address for address in semantic_addresses if address in lexical_set
        ],
        "semantic_only": [
            address for address in semantic_addresses if address not in lexical_set
        ],
        "lexical_only": [
            address for address in lexical_addresses if address not in semantic_set
        ],
    }
    retained_overlap = candidate["overlap"]
    if any(
        retained_overlap[field] != surfaces[result_field]
        for field, result_field in (
            ("intersection", "overlap"),
            ("semantic_only", "semantic_only"),
            ("lexical_only", "lexical_only"),
        )
    ):
        msg = "Retained overlap differs from candidate arm ordering."
        raise ValueError(msg)
    records = judgment["records"]
    by_neutral_id = {record["neutral_id"]: record for record in records}
    union = semantic_set | lexical_set
    if len(by_neutral_id) != len(records) or {
        _neutral_id(case_id, address) for address in union
    } != set(by_neutral_id):
        msg = "Frozen neutral pairs differ from candidate union."
        raise ValueError(msg)

    def label(address: str) -> str:
        return str(by_neutral_id[_neutral_id(case_id, address)]["judgment"])

    counts = {
        surface: {
            state: sum(label(address) == state for address in addresses)
            for state in LABELS
        }
        for surface, addresses in surfaces.items()
    }
    useful = {
        surface: [
            address
            for address in addresses
            if label(address) == UsefulnessJudgment.USEFUL.value
        ]
        for surface, addresses in surfaces.items()
    }
    no_positive_rank: list[str] = []
    useful_no_positive_rank: list[str] = []
    useful_semantic_only_ranked: list[dict[str, Any]] = []
    lexical_ranks = {item["address"]: item["rank"] for item in lexical}
    for item in semantic:
        address = item["address"]
        rank = item["positive_lexical_rank"]
        if item["has_positive_lexical_rank"] != (rank is not None):
            msg = "Semantic candidate lexical reachability fields disagree."
            raise ValueError(msg)
        if address in lexical_set:
            if rank != lexical_ranks[address]:
                msg = "Overlapping candidate has inconsistent lexical rank."
                raise ValueError(msg)
        elif rank is not None and rank <= n:
            msg = "Semantic-only candidate has a rank inside matched lexical capacity."
            raise ValueError(msg)
        if rank is None:
            no_positive_rank.append(address)
            if label(address) == UsefulnessJudgment.USEFUL.value:
                useful_no_positive_rank.append(address)
        elif (
            address not in lexical_set
            and label(address) == UsefulnessJudgment.USEFUL.value
        ):
            useful_semantic_only_ranked.append(
                {"address": address, "lexical_rank": rank},
            )
    return {
        "case_id": case_id,
        "information_need": need,
        "parent_snapshot_sha": candidate["parent_snapshot_sha"],
        "capacity": n,
        "candidate_counts": {
            surface: len(addresses) for surface, addresses in surfaces.items()
        },
        "judgment_counts": counts,
        "useful_resources": useful,
        "lexical_reachability": {
            "semantic_without_positive_lexical_rank": no_positive_rank,
            "useful_semantic_without_positive_lexical_rank": useful_no_positive_rank,
            "useful_semantic_only_ranked_outside_capacity": useful_semantic_only_ranked,
        },
    }


def _aggregate(results: list[dict[str, Any]]) -> dict[str, Any]:
    candidate_counts = {
        surface: sum(case["candidate_counts"][surface] for case in results)
        for surface in SURFACES
    }
    judgment_counts = {
        surface: {
            state: sum(case["judgment_counts"][surface][state] for case in results)
            for state in LABELS
        }
        for surface in SURFACES
    }
    reachability: dict[str, Any] = {
        "semantic_without_positive_lexical_rank": [],
        "useful_semantic_without_positive_lexical_rank": [],
        "useful_semantic_only_ranked_outside_capacity": [],
    }
    for case in results:
        for field, values in case["lexical_reachability"].items():
            for value in values:
                item = {"case_id": case["case_id"]}
                if isinstance(value, str):
                    item["address"] = value
                else:
                    item.update(value)
                reachability[field].append(item)
    ranked = reachability["useful_semantic_only_ranked_outside_capacity"]
    distribution: dict[str, int] = {}
    for item in ranked:
        rank = str(item["lexical_rank"])
        distribution[rank] = distribution.get(rank, 0) + 1
    reachability["useful_semantic_only_positive_lexical_rank_distribution"] = (
        distribution
    )
    return {
        "case_count": len(results),
        "neutral_pair_count": PAIR_COUNT,
        "candidate_counts": candidate_counts,
        "judgment_counts": judgment_counts,
        "lexical_reachability": reachability,
    }


def main() -> None:
    """Persist the one canonical deterministic post-freeze development join."""
    result = evaluate_development(
        candidate_bytes=(_ROOT / "development_candidate_evidence.json").read_bytes(),
        judgment_bytes=(_ROOT / "development_frozen_judgments.json").read_bytes(),
        blinded_input_bytes=(_ROOT / "development_judgment_input.json").read_bytes(),
    )
    (_ROOT / "development_results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
