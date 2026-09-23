# Copyright (c) 2026
# ruff: noqa: COM812, D103, E501, EM101, EM102, PLR2004, T201, TRY003
"""Offline Increment-24 ranking comparison over retained Increment-23 surfaces.

This module neither acquires a repository nor changes production retrieval.  It
uses only retained pre-judgment capture evidence for features and joins frozen
adjudications only in its evaluator.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from enum import StrEnum
from math import log2 as _log2
from pathlib import Path
from typing import Any, cast

from experiments.purpose_relative_admission.validation_execution import (
    validate_artifact_correspondence,
    validate_artifact_envelope,
)

_SCHEMA = "devtools-b0002-purpose-relative-ranking-comparison-v1"
_DESIGN_VERSION = "increment-24-offline-purpose-relative-ranking-v1"
_CAPTURE = ".b0002-increment-23-hidden-surface-capture.json"
_MAPPING = ".b0002-increment-23-neutral-resource-mapping.json"
_FROZEN = ".b0002-increment-23-frozen-adjudication.json"
_REPORT = ".b0002-purpose-relative-independent-validation.json"


class RankingArm(StrEnum):
    """Frozen offline arms; none is production behavior."""

    CANONICAL_TOP5 = "canonical-top5"
    LEXICAL_TOP15_TRUNCATED_TO5 = "lexical-top15-truncated-to5"
    PURPOSE_AGNOSTIC_NATIVE_EVIDENCE = "purpose-agnostic-native-evidence"
    PURPOSE_RELATIVE_WITHOUT_RELATIONSHIPS = "purpose-relative-without-relationships"
    PURPOSE_RELATIVE_DETERMINISTIC = "purpose-relative-deterministic"


@dataclass(frozen=True, slots=True)
class SurfaceCandidate:
    """One resource with pre-judgment native evidence only."""

    address: str
    lexical_score: float | None
    lexical_rank: int | None
    in_top5: bool
    in_top15: bool
    incoming_support_count: int
    outgoing_support_count: int
    profile_support_count: int
    best_profile_seed_rank: int | None
    profile_encounter_count: int


@dataclass(frozen=True, slots=True)
class LabeledCandidate:
    """Evaluation-only label joined after feature construction."""

    candidate: SurfaceCandidate
    judgment: str


@dataclass(frozen=True, slots=True)
class RankingCase:
    """One fixed InformationNeed surface and purpose profile."""

    name: str
    query_text: str
    information_need: str
    profile: str
    candidates: tuple[LabeledCandidate, ...]


def ranking_design_fingerprint() -> str:
    """Fingerprint policies, split, labels policy, and source artifact contract."""
    payload = {
        "version": _DESIGN_VERSION,
        "source_artifacts": [_CAPTURE, _MAPPING, _FROZEN, _REPORT],
        "arms": [item.value for item in RankingArm],
        "consideration": "increment-23 material surface: lexical top-15 plus profile-eligible relation targets",
        "features": [
            "lexical-score", "lexical-rank", "top5", "top15",
            "incoming-distinct-support-count", "outgoing-distinct-support-count",
            "profile-distinct-support-count", "best-profile-seed-rank",
            "profile-encounter-count", "purpose-profile",
        ],
        "label_policy": "USEFUL/NOT_USEFUL are evaluator labels; UNJUDGED is retained unresolved and never a negative label",
        "split": "six grouped InformationNeeds are descriptive within-repository evaluation only; no calibration or learned training",
        "purpose_policy": "local profiles preserve lexical/native ordering; directional profiles prioritize matching directed relation support, then native lexical evidence",
        "tie_policy": "lexical rank, then address serialization only after all semantic/native keys",
        "learned": "not-estimable: six grouped needs and no non-leaking calibration/evaluation split",
    }
    return _digest(payload)


def validate_grouped_case_split(
    *, calibration: tuple[str, ...], evaluation: tuple[str, ...]
) -> None:
    """Reject same-InformationNeed leakage between calibration and evaluation."""
    if set(calibration) & set(evaluation):
        raise ValueError("A grouped InformationNeed cannot be calibration and evaluation.")


def load_ranking_cases(*, repository_root: Path) -> tuple[RankingCase, ...]:
    """Load validated retained surfaces and join labels only after features exist."""
    envelopes = {
        name: _load(repository_root / filename)
        for name, filename in {
            "capture": _CAPTURE, "mapping": _MAPPING, "frozen": _FROZEN,
            "report": _REPORT,
        }.items()
    }
    if not validate_artifact_correspondence(
        capture=envelopes["capture"], package=_load(repository_root / ".b0002-increment-23-blinded-adjudication-package.json"), mapping=envelopes["mapping"],
    ):
        raise ValueError("Increment-23 retained capture correspondence is invalid.")
    if not all(validate_artifact_envelope(item) for item in envelopes.values()):
        raise ValueError("Increment-23 retained artifact envelope is invalid.")
    capture_cases = envelopes["capture"]["payload"]["cases"]
    mappings = envelopes["mapping"]["payload"]["mappings"]
    frozen_cases = envelopes["frozen"]["payload"]["cases"]
    if not (len(capture_cases) == len(mappings) == len(frozen_cases) == 6):
        raise ValueError("Increment-23 retained case cardinality is not six.")
    values: list[RankingCase] = []
    for capture, mapping, frozen in zip(capture_cases, mappings, frozen_cases, strict=True):
        labels = {
            item["address"]: record["judgment"]
            for item, record in zip(mapping, frozen["records"], strict=True)
        }
        candidates = build_surface_candidates(capture=capture)
        values.append(
            RankingCase(
                capture["case_name"], capture["query_text"], capture["information_need"],
                capture["profile"],
                tuple(LabeledCandidate(item, labels.get(item.address, "unjudged")) for item in candidates),
            )
        )
    return tuple(values)


def build_surface_candidates(*, capture: dict[str, Any]) -> tuple[SurfaceCandidate, ...]:
    """Construct candidates from retained capture facts without labels or controls."""
    lexical = {item["address"]: item for item in capture["lexical_top_fifteen"]}
    top5 = {item["address"] for item in capture["lexical_top_five"]}
    incoming = _relationship_features(capture["incoming_surfaces"])
    outgoing = _relationship_features(capture["outgoing_surfaces"])
    eligible = _relationship_features(capture["profile_eligible_surfaces"])
    addresses = tuple(dict.fromkeys((*lexical, *incoming, *outgoing, *eligible)))
    values = []
    for address in addresses:
        lexical_item = lexical.get(address)
        profile = eligible.get(address, (0, None, 0))
        values.append(
            SurfaceCandidate(
                address,
                lexical_item["score"] if lexical_item else None,
                lexical_item["rank"] if lexical_item else None,
                address in top5,
                lexical_item is not None,
                incoming.get(address, (0, None, 0))[0],
                outgoing.get(address, (0, None, 0))[0],
                profile[0], profile[1], profile[2],
            )
        )
    return tuple(values)


def rank_case(*, case: RankingCase, arm: RankingArm) -> tuple[SurfaceCandidate, ...]:
    """Apply a predeclared deterministic ordering without using labels."""
    values = tuple(item.candidate for item in case.candidates)
    if arm is RankingArm.CANONICAL_TOP5:
        return tuple(sorted((item for item in values if item.in_top5), key=lambda item: item.lexical_rank or 10**9))
    if arm is RankingArm.LEXICAL_TOP15_TRUNCATED_TO5:
        return tuple(sorted((item for item in values if item.in_top15), key=_lexical_key)[:5])
    if arm is RankingArm.PURPOSE_AGNOSTIC_NATIVE_EVIDENCE:
        return tuple(sorted(values, key=_agnostic_key)[:5])
    if arm is RankingArm.PURPOSE_RELATIVE_WITHOUT_RELATIONSHIPS:
        return tuple(sorted(values, key=_agnostic_key)[:5])
    if arm is RankingArm.PURPOSE_RELATIVE_DETERMINISTIC:
        if case.profile == "local-definition-or-governance":
            return tuple(sorted(values, key=_agnostic_key)[:5])
        return tuple(sorted(values, key=_purpose_key)[:5])
    raise ValueError(f"Unknown ranking arm: {arm}.")


def evaluate_case(*, case: RankingCase, arm: RankingArm) -> dict[str, Any]:
    """Calculate known-label metrics and bounds without coercing UNJUDGED values."""
    ranked = rank_case(case=case, arm=arm)
    by_address = {item.candidate.address: item.judgment for item in case.candidates}
    known_useful = {address for address, label in by_address.items() if label == "useful"}
    known_not = {address for address, label in by_address.items() if label == "not-useful"}
    selected = tuple(item.address for item in ranked)
    selected_useful = tuple(address for address in selected if address in known_useful)
    selected_not = tuple(address for address in selected if address in known_not)
    selected_unjudged = tuple(address for address in selected if by_address[address] == "unjudged")
    omitted = tuple(sorted(known_useful - set(selected)))
    return {
        "case_name": case.name,
        "query_text": case.query_text,
        "profile": case.profile,
        "arm": arm.value,
        "ranking": list(selected),
        "known_useful_recovered": len(selected_useful),
        "known_useful_total": len(known_useful),
        "known_useful_omitted": list(omitted),
        "selected_not_useful_count": len(selected_not),
        "selected_unjudged_count": len(selected_unjudged),
        "hit_at_5": float(bool(selected_useful)),
        "recall_at_5": len(selected_useful) / len(known_useful) if known_useful else None,
        "mrr": next((1 / rank for rank, address in enumerate(selected, 1) if address in known_useful), 0.0),
        "ndcg_at_5": _ndcg(selected, known_useful),
        "precision_at_5_definitive": _precision(selected, known_useful, known_not),
        "pairwise_useful_not_useful_accuracy": _pairwise(ranked, known_useful, known_not),
        "judgment_limitation": bool(selected_unjudged),
        "generation_failure_known_useful": 0,
        "ranking_capacity_failure_known_useful": len(omitted),
    }


def build_report(*, repository_root: Path) -> dict[str, Any]:
    """Build the one retained Increment-24 report from existing static artifacts."""
    cases = load_ranking_cases(repository_root=repository_root)
    validate_grouped_case_split(
        calibration=(), evaluation=tuple(case.name for case in cases)
    )
    evaluations = {
        arm.value: [evaluate_case(case=case, arm=arm) for case in cases]
        for arm in RankingArm
    }
    payload = {
        "scope": "offline devtools-only ranking comparison; no production behavior change",
        "design_fingerprint": ranking_design_fingerprint(),
        "source_checkpoint": _load(repository_root / _REPORT)["payload"]["repository_checkpoint"],
        "source_artifacts": [_CAPTURE, _MAPPING, _FROZEN, _REPORT],
        "case_split": {"evaluation": [case.name for case in cases], "calibration": [], "status": "descriptive within-repository; no training or tuning"},
        "feature_definitions": [field for field in SurfaceCandidate.__dataclass_fields__ if field != "address"],
        "unjudged_policy": "Retain unresolved; exclude from definitive precision and pairwise denominators; do not train or coerce as negative.",
        "arms": evaluations,
        "aggregates": {name: _aggregate(values) for name, values in evaluations.items()},
        "learned_ranking": {"status": "not-estimable", "reason": "Six grouped InformationNeeds provide no scientifically credible non-leaking train/evaluation split; no learned model was fit."},
        "headroom": _headroom(evaluations[RankingArm.PURPOSE_RELATIVE_DETERMINISTIC.value]),
        "relationship_contribution": _contribution(evaluations, RankingArm.PURPOSE_RELATIVE_WITHOUT_RELATIONSHIPS.value, RankingArm.PURPOSE_RELATIVE_DETERMINISTIC.value),
        "purpose_contribution": _contribution(evaluations, RankingArm.PURPOSE_AGNOSTIC_NATIVE_EVIDENCE.value, RankingArm.PURPOSE_RELATIVE_DETERMINISTIC.value),
        "direct_resolution_controls": _load(repository_root / _REPORT)["payload"]["direct_resolution_controls"],
        "external_validity": "NOT_TESTED_CROSS_REPOSITORY; results are descriptive for the retained devtools surface only.",
        "failed_run_history": [],
        "disposition": "INSUFFICIENT_EVIDENCE_FOR_PRODUCTION_RANKING; local deterministic ordering is descriptive only, learned ranking not estimable, and cross-repository validity is untested.",
        "increment_25_question": "Does a distinct semantic candidate-generation family expose useful resources absent from bounded lexical retrieval?",
        "increment_26_requirement": "Freeze and evaluate at least one independent repository before architectural closure or general ranking claims.",
    }
    return {"schema": _SCHEMA, "content_identity": _digest(payload), "payload": payload}


def write_report(*, repository_root: Path, path: Path) -> dict[str, Any]:
    report = build_report(repository_root=repository_root)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return report


def _relationship_features(surfaces: list[dict[str, Any]]) -> dict[str, tuple[int, int | None, int]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for surface in surfaces:
        grouped.setdefault(surface["address"], []).append(surface)
    return {
        address: (len({item["relation_identity"] for item in items}), min(item["seed_rank"] for item in items), len(items))
        for address, items in grouped.items()
    }


def _lexical_key(item: SurfaceCandidate) -> tuple[float, int, int, str]:
    return (-(item.lexical_score or 0.0), item.lexical_rank or 10**9, -item.in_top15, item.address)


def _agnostic_key(item: SurfaceCandidate) -> tuple[int, float, int, int, str]:
    return (0 if item.in_top15 else 1, -(item.lexical_score or 0.0), item.lexical_rank or 10**9, -(item.incoming_support_count + item.outgoing_support_count), item.address)


def _purpose_key(item: SurfaceCandidate) -> tuple[int, int, int, float, int, str]:
    return (0 if item.profile_support_count else 1, -item.profile_support_count, item.best_profile_seed_rank or 10**9, -(item.lexical_score or 0.0), item.lexical_rank or 10**9, item.address)


def _ndcg(selected: tuple[str, ...], useful: set[str]) -> float | None:
    if not useful:
        return None
    dcg = sum(1 / _log2(rank + 1) for rank, address in enumerate(selected, 1) if address in useful)
    ideal = sum(1 / _log2(rank + 1) for rank in range(1, min(5, len(useful)) + 1))
    return dcg / ideal


def _precision(selected: tuple[str, ...], useful: set[str], not_useful: set[str]) -> float | None:
    definite = [address for address in selected if address in useful | not_useful]
    return len([address for address in definite if address in useful]) / len(definite) if definite else None


def _pairwise(ranked: tuple[SurfaceCandidate, ...], useful: set[str], not_useful: set[str]) -> float | None:
    positions = {item.address: index for index, item in enumerate(ranked)}
    pairs = [(good, bad) for good in useful for bad in not_useful if good in positions and bad in positions]
    return sum(positions[good] < positions[bad] for good, bad in pairs) / len(pairs) if pairs else None


def _aggregate(values: list[dict[str, Any]]) -> dict[str, Any]:
    keys = ("hit_at_5", "recall_at_5", "mrr", "ndcg_at_5", "precision_at_5_definitive", "pairwise_useful_not_useful_accuracy")
    return {
        key: sum(item[key] for item in values if item[key] is not None) / len([item for item in values if item[key] is not None]) if any(item[key] is not None for item in values) else None
        for key in keys
    } | {
        "known_useful_recovered": sum(item["known_useful_recovered"] for item in values),
        "known_useful_total": sum(item["known_useful_total"] for item in values),
        "selected_not_useful_count": sum(item["selected_not_useful_count"] for item in values),
        "selected_unjudged_count": sum(item["selected_unjudged_count"] for item in values),
        "ranking_capacity_failure_known_useful": sum(item["ranking_capacity_failure_known_useful"] for item in values),
    }


def _headroom(values: list[dict[str, Any]]) -> dict[str, int]:
    return {"generation_failure_known_useful": sum(item["generation_failure_known_useful"] for item in values), "ranking_capacity_failure_known_useful": sum(item["ranking_capacity_failure_known_useful"] for item in values)}


def _contribution(evaluations: dict[str, list[dict[str, Any]]], baseline: str, compared: str) -> dict[str, int]:
    return {"known_useful_recovery_delta": sum(item["known_useful_recovered"] for item in evaluations[compared]) - sum(item["known_useful_recovered"] for item in evaluations[baseline]), "not_useful_selection_delta": sum(item["selected_not_useful_count"] for item in evaluations[compared]) - sum(item["selected_not_useful_count"] for item in evaluations[baseline])}


def _load(path: Path) -> dict[str, Any]:
    return cast("dict[str, Any]", json.loads(path.read_text(encoding="utf-8")))


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, default=asdict, separators=(",", ":"), sort_keys=True).encode()).hexdigest()


if __name__ == "__main__":
    report = write_report(repository_root=Path.cwd(), path=Path(".b0002-purpose-relative-ranking-comparison.json"))
    print(json.dumps({"schema": report["schema"], "content_identity": report["content_identity"]}, indent=2))
