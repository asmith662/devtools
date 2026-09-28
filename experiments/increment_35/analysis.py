# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, PLR0912, PLR2004, TRY003, C901
"""Join frozen lexical, structural, and eight-case semantic development evidence."""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from statistics import median
from typing import TYPE_CHECKING, Any

from experiments.increment_25.development import write_artifact
from experiments.increment_26.configuration import _digest as _legacy_dense_digest
from experiments.increment_26.development_judgments import USEFULNESS_SEMANTICS
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_30.mechanics import _verified_json
from experiments.retrieval_judgment_coverage import (
    judgment_identity,
    validated_outcome_mappings,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

ROOT = Path(__file__).resolve().parent
RESULT_NAME = "heterogeneous_union_development_results.json"
METHODS = ("canonical", "bm25_plus", "identifier", "path", "rrf")
STATES = ("USEFUL", "NOT_USEFUL", "UNJUDGED")
SOURCES = {
    "lexical_rankings": "increment_27/lexical_comparison_rankings.json",
    "canonical_basis": "increment_27/canonical_positive_lexical_rankings.json",
    "lexical_top5_results": "increment_27/lexical_top5_development_results.json",
    "lexical_comparison_judgments": "increment_27/comparison_frozen_judgments.json",
    "structural_union": "increment_34/structural_union_development_results.json",
    "dense_freeze": "increment_26/experiment_freeze.json",
    "dense_candidates": "increment_26/development_candidate_evidence.json",
    "dense_judgments": "increment_26/development_frozen_judgments.json",
    "dense_results": "increment_26/development_results.json",
}
Key = tuple[str, str, str]


def _key(case_id: str, parent: str, address: str) -> Key:
    return (case_id, parent, address)


def _sources(root: Path) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    """Read only frozen development artifacts and record exact file identities."""
    data: dict[str, dict[str, Any]] = {}
    fingerprints: dict[str, Any] = {}
    for name, relative in SOURCES.items():
        path = root.parent / relative
        artifact = (
            _read_json(path)
            if name in {"canonical_basis", "dense_candidates"}
            or name.startswith("dense_")
            else _verified_json(path)
        )
        if (
            name.startswith("dense_")
            and "payload" in artifact
            and artifact["content_identity"]
            != _legacy_dense_digest(artifact["payload"])
        ):
            raise ValueError("Legacy Increment-26 content identity differs.")
        data[name] = artifact
        fingerprints[name] = {
            "path": relative,
            "identity": artifact.get(
                "content_identity",
                artifact.get("execution_identity", artifact.get("freeze_identity")),
            ),
            "sha256": sha256_file(path),
        }
    dense = data["dense_candidates"]
    dense_result = data["dense_results"]["payload"]
    dense_judgments = data["dense_judgments"]["payload"]
    if (
        dense_result["candidate_evidence_sha256"]
        != fingerprints["dense_candidates"]["sha256"]
        or dense_result["candidate_evidence_identity"] != dense["execution_identity"]
        or dense_result["frozen_judgment_sha256"]
        != fingerprints["dense_judgments"]["sha256"]
        or dense_judgments["candidate_evidence_identity"] != dense["execution_identity"]
    ):
        raise ValueError("Increment-26 dense artifact bindings differ.")
    if (
        data["structural_union"]["payload"]["confirmation_executed"]
        or data["structural_union"]["payload"]["new_judgments_created"]
    ):
        raise ValueError("Structural source crossed an outcome boundary.")
    return data, fingerprints


def _case_basis(data: Mapping[str, Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    basis_rows = data["canonical_basis"]["cases"]
    ranking_rows = data["lexical_rankings"]["cases"]
    if len(basis_rows) != 24 or [row["case_id"] for row in basis_rows] != [
        row["case_id"] for row in ranking_rows
    ]:
        raise ValueError("Canonical and five-method development populations differ.")
    if [row["case_id"] for row in basis_rows] != data["structural_union"]["payload"][
        "development_case_ids"
    ]:
        raise ValueError("Structural and lexical development populations differ.")
    result: dict[str, dict[str, Any]] = {}
    for basis, ranking in zip(basis_rows, ranking_rows, strict=True):
        if (
            basis["parent_snapshot_sha"] != ranking["parent_snapshot_sha"]
            or basis["information_need"]["lexical_query"] != ranking["query_text"]
            or [row["address"] for row in basis["positive_lexical_ordering"]]
            != [row["address"] for row in ranking["rankings"]["canonical"]]
        ):
            raise ValueError("Canonical ranking identity differs from frozen basis.")
        result[basis["case_id"]] = {
            "case_id": basis["case_id"],
            "parent_snapshot_sha": basis["parent_snapshot_sha"],
            "information_need": basis["information_need"],
            "usefulness_semantics": USEFULNESS_SEMANTICS,
        }
    return result


def _candidate_surfaces(
    data: Mapping[str, Mapping[str, Any]], basis: Mapping[str, Mapping[str, Any]]
) -> tuple[dict[Key, dict[str, Any]], dict[str, set[Key]], dict[str, dict[str, Any]]]:
    """Project frozen modalities without generating a single new candidate."""
    candidates: dict[Key, dict[str, Any]] = {}
    surfaces: dict[str, set[Key]] = {
        name: set() for name in (*METHODS, "lexical", "structural", "dense")
    }
    for case in data["lexical_rankings"]["cases"]:
        case_id = case["case_id"]
        parent = basis[case_id]["parent_snapshot_sha"]
        for method in METHODS:
            for ranked in case["rankings"][method]:
                key = _key(case_id, parent, ranked["address"])
                row = candidates.setdefault(
                    key,
                    {
                        "case_id": case_id,
                        "parent_snapshot_sha": parent,
                        "address": ranked["address"],
                        "lexical_ranks": {},
                        "structural_families": [],
                        "dense": None,
                    },
                )
                if method in row["lexical_ranks"]:
                    raise ValueError("Frozen lexical method repeats one candidate.")
                row["lexical_ranks"][method] = ranked["rank"]
                surfaces[method].add(key)
                surfaces["lexical"].add(key)
    structural = data["structural_union"]["payload"]
    if (
        len(structural["candidates"])
        != structural["complete_structural_surface"]["candidate_pairs"]
    ):
        raise ValueError("Structural Union candidate artifact is incomplete.")
    for item in structural["candidates"]:
        case_id, parent, address = (
            item["case_id"],
            item["parent_snapshot_sha"],
            item["address"],
        )
        if (
            case_id not in basis
            or parent != basis[case_id]["parent_snapshot_sha"]
            or item["information_need"] != basis[case_id]["information_need"]
        ):
            raise ValueError("Structural candidate identity differs from lexical case.")
        key = _key(case_id, parent, address)
        row = candidates.setdefault(
            key,
            {
                "case_id": case_id,
                "parent_snapshot_sha": parent,
                "address": address,
                "lexical_ranks": {},
                "structural_families": [],
                "dense": None,
            },
        )
        row["structural_families"] = item["families"]
        surfaces["structural"].add(key)
    dense_cases = data["dense_candidates"]["cases"]
    frozen_dense_cases = data["dense_freeze"]["payload"]["population"][
        "development_case_ids"
    ]
    if (
        len(dense_cases) != 8
        or [case["case_id"] for case in dense_cases] != frozen_dense_cases
    ):
        raise ValueError("Dense development population differs from its freeze.")
    dense_details: dict[str, dict[str, Any]] = {}
    rankings_by_case = {
        case["case_id"]: case for case in data["lexical_rankings"]["cases"]
    }
    for case in dense_cases:
        case_id = case["case_id"]
        parent = basis[case_id]["parent_snapshot_sha"]
        if (
            case["parent_snapshot_sha"] != parent
            or case["information_need"] != basis[case_id]["information_need"]
            or case["corpus"]["corpus_id"] != rankings_by_case[case_id]["corpus_id"]
            or case["corpus"]["resource_count"]
            != rankings_by_case[case_id]["corpus_resource_count"]
        ):
            raise ValueError(
                "Dense InformationNeed/snapshot differs from development basis."
            )
        dense_details[case_id] = {
            "candidate_count": len(case["semantic_candidates"]),
            "capacity": case["capacity"]["n"],
        }
        for rank, ranked in enumerate(case["semantic_candidates"], 1):
            key = _key(case_id, parent, ranked["address"])
            row = candidates.setdefault(
                key,
                {
                    "case_id": case_id,
                    "parent_snapshot_sha": parent,
                    "address": ranked["address"],
                    "lexical_ranks": {},
                    "structural_families": [],
                    "dense": None,
                },
            )
            if row["dense"] is not None:
                raise ValueError("Dense surface repeats one candidate.")
            row["dense"] = {"rank": rank, "similarity": ranked["score"]}
            surfaces["dense"].add(key)
    return candidates, surfaces, dense_details


def _outcomes(
    data: Mapping[str, Mapping[str, Any]],
    basis: Mapping[str, Mapping[str, Any]],
    candidates: Mapping[Key, Mapping[str, Any]],
    surfaces: Mapping[str, set[Key]],
) -> tuple[dict[Key, str], dict[Key, list[str]]]:
    """Unify existing development labels; reject conflicting exact identities."""
    outcomes: dict[Key, str] = {}
    sources: dict[Key, list[str]] = defaultdict(list)
    normalized_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    purpose_index = {
        (
            row["parent_snapshot_sha"],
            row["information_need"]["purpose"],
            row["information_need"]["lexical_query"],
        ): case_id
        for case_id, row in basis.items()
    }

    def accept(
        source: str, case_id: str, parent: str, address: str, judgment: str
    ) -> None:
        key = _key(case_id, parent, address)
        state = judgment.upper().replace("-", "_")
        if (
            key not in candidates
            or state not in STATES
            or parent != basis[case_id]["parent_snapshot_sha"]
        ):
            raise ValueError(
                "Development judgment escaped the frozen union or semantics."
            )
        previous = outcomes.get(key)
        if previous is not None and previous != state:
            raise ValueError("Conflicting exact development judgments.")
        outcomes[key] = state
        sources[key].append(source)
        normalized_by_source[source].append(
            {**basis[case_id], "address": address, "judgment": state}
        )

    for row in data["lexical_top5_results"]["payload"]["joined_pairs"]:
        ranked = candidates.get(
            _key(row["case_id"], row["parent_snapshot_sha"], row["address"])
        )
        if ranked is None or not any(
            rank <= 5 for rank in ranked["lexical_ranks"].values()
        ):
            raise ValueError("Lexical top-five judgment escaped five-method top five.")
        accept(
            "lexical_top5",
            row["case_id"],
            row["parent_snapshot_sha"],
            row["address"],
            row["judgment"],
        )
    for row in data["lexical_comparison_judgments"]["payload"]["records"]:
        need = row["information_need"]
        case_id = purpose_index[
            (row["parent_snapshot_sha"], need["purpose"], need["lexical_query"])
        ]
        if row["usefulness_semantics"] != USEFULNESS_SEMANTICS:
            raise ValueError("Lexical comparison usefulness semantics differ.")
        accept(
            "lexical_comparison",
            case_id,
            row["parent_snapshot_sha"],
            row["address"],
            row["judgment"],
        )
    dense_judgments = data["dense_judgments"]["payload"]["cases"]
    if {case["case_id"] for case in dense_judgments} != {
        case["case_id"] for case in data["dense_candidates"]["cases"]
    }:
        raise ValueError("Dense judgment cases differ from frozen candidates.")
    for case in dense_judgments:
        case_id = case["case_id"]
        for row in case["records"]:
            accept(
                "dense_development",
                case_id,
                basis[case_id]["parent_snapshot_sha"],
                row["address"],
                row["judgment"],
            )
    if len(
        {
            key
            for key in surfaces["dense"]
            if "dense_development" in sources.get(key, [])
        }
    ) != len(surfaces["dense"]):
        raise ValueError("Dense candidate surface lacks exact development judgments.")
    for row in data["structural_union"]["payload"]["candidates"]:
        if row["outcome_knowledge"] != "NEVER_ADJUDICATED":
            accept(
                "structural_union",
                row["case_id"],
                row["parent_snapshot_sha"],
                row["address"],
                row["outcome_knowledge"],
            )
    for rows in normalized_by_source.values():
        validated_outcome_mappings(rows, {})
    identities: dict[tuple[str, ...], str] = {}
    for key, state in outcomes.items():
        identity = judgment_identity({**basis[key[0]], "address": key[2]})
        old = identities.get(identity)
        if old is not None and old != state:
            raise ValueError("Conflicting purpose-relative development judgments.")
        identities[identity] = state
    return outcomes, sources


def _surface(
    keys: set[Key], outcomes: Mapping[Key, str], case_ids: list[str]
) -> dict[str, Any]:
    volumes = Counter(key[0] for key in keys)
    counts = sorted(volumes.get(case_id, 0) for case_id in case_ids)
    return {
        "candidate_pairs": len(keys),
        "distinct_addresses": len({key[2] for key in keys}),
        "cases": len(volumes),
        "median_candidates_per_case": median(counts),
        "median_candidates_per_covered_case": median(volumes.values())
        if volumes
        else 0,
        "max_candidates_per_case": max(counts),
        "known_useful": sum(outcomes.get(key) == "USEFUL" for key in keys),
        "known_not_useful": sum(outcomes.get(key) == "NOT_USEFUL" for key in keys),
        "known_unjudged": sum(outcomes.get(key) == "UNJUDGED" for key in keys),
        "never_adjudicated": sum(key not in outcomes for key in keys),
    }


def build_result(root: Path = ROOT) -> dict[str, Any]:
    """Build the candidate ceiling without ranking, selecting, or adjudicating."""
    data, fingerprints = _sources(root)
    basis = _case_basis(data)
    candidates, surfaces, dense_details = _candidate_surfaces(data, basis)
    outcomes, judgment_sources = _outcomes(data, basis, candidates, surfaces)
    lexical, structural, dense = (
        surfaces[name] for name in ("lexical", "structural", "dense")
    )
    all_keys = lexical | structural | dense
    if set(candidates) != all_keys or len(dense) != 40:
        raise ValueError("Heterogeneous candidate surface differs from frozen sources.")
    regions: dict[str, set[Key]] = {}
    for key in all_keys:
        name = "+".join(
            name
            for name, surface in (
                ("lexical", lexical),
                ("structural", structural),
                ("dense", dense),
            )
            if key in surface
        )
        regions.setdefault(name, set()).add(key)
    case_ids = list(basis)
    named_surfaces = {
        "canonical_top_five": surfaces["canonical"]
        & {
            key
            for key in surfaces["canonical"]
            if candidates[key]["lexical_ranks"]["canonical"] <= 5
        },
        "lexical": lexical,
        "structural": structural,
        "lexical_structural": lexical | structural,
        "dense": dense,
        "heterogeneous": all_keys,
    }
    surface_summaries = {
        name: _surface(keys, outcomes, case_ids)
        for name, keys in named_surfaces.items()
    }
    region_summaries = {
        name: _surface(keys, outcomes, case_ids)
        for name, keys in sorted(regions.items())
    }
    lexical_overlap = {
        left: {right: len(surfaces[left] & surfaces[right]) for right in METHODS}
        for left in METHODS
    }
    lexical_multiplicity = {
        str(n): count
        for n, count in sorted(
            Counter(
                sum(key in surfaces[method] for method in METHODS) for key in lexical
            ).items()
        )
    }
    useful = {key for key in all_keys if outcomes.get(key) == "USEFUL"}
    structural_escapes = {
        key for key in structural - lexical if outcomes.get(key) == "USEFUL"
    }
    dense_escapes = {
        key for key in dense - (lexical | structural) if outcomes.get(key) == "USEFUL"
    }
    per_case: list[dict[str, Any]] = []
    for case_id in case_ids:
        counts = {
            name: sum(key[0] == case_id and key in useful for key in keys)
            for name, keys in named_surfaces.items()
        }
        per_case.append(
            {
                "case_id": case_id,
                "canonical_top_five_known_useful": counts["canonical_top_five"],
                "lexical_known_useful": counts["lexical"],
                "structural_known_useful": counts["structural"],
                "heterogeneous_known_useful": counts["heterogeneous"],
                "oracle_known_useful_at_k5": min(5, counts["heterogeneous"]),
                "headroom_beyond_canonical_known_useful": counts["heterogeneous"]
                - counts["canonical_top_five"],
                "oracle_k5_headroom_beyond_canonical": min(5, counts["heterogeneous"])
                - counts["canonical_top_five"],
            }
        )
    headroom = dict(
        sorted(
            Counter(
                row["headroom_beyond_canonical_known_useful"] for row in per_case
            ).items()
        )
    )
    dense_outside = {
        "outside_lexical_pairs": len(dense - lexical),
        "outside_structural_pairs": len(dense - structural),
        "outside_lexical_structural_pairs": len(dense - (lexical | structural)),
        "known_useful_outside_lexical_structural": len(dense_escapes),
        "cases_with_known_useful_dense_only": len({key[0] for key in dense_escapes}),
    }
    payload = {
        "source_artifacts": fingerprints,
        "definition": "exact 24-case InformationNeed/query + parent snapshot + resource address; modalities deduplicated; dense observed for eight frozen development cases only",
        "dense_evidence_gate": {
            "classification": "A_USABLE_FROZEN_DEVELOPMENT_SURFACE",
            "model": data["dense_freeze"]["payload"]["encoder"]["repository"],
            "revision": data["dense_freeze"]["payload"]["encoder"]["revision"],
            "development_cases": len(dense_details),
            "candidate_pairs": len(dense),
            "all_dense_candidates_judged": True,
            "reproduced_in_increment_26": True,
        },
        "case_basis": [basis[case_id] for case_id in case_ids],
        "surfaces": surface_summaries,
        "modality_regions": region_summaries,
        "lexical_method_pairwise_overlap": lexical_overlap,
        "lexical_method_support_multiplicity": lexical_multiplicity,
        "known_useful_coverage": {
            "candidate_pairs": len(useful),
            "distinct_addresses": len({key[2] for key in useful}),
            "cases": len({key[0] for key in useful}),
        },
        "structural_complementarity": {
            "known_useful_outside_lexical_pairs": len(structural_escapes),
            "cases_with_escaped_useful": len({key[0] for key in structural_escapes}),
            "cases_gaining_any_known_useful_coverage": len(
                {
                    key[0]
                    for key in structural_escapes
                    if not any(other[0] == key[0] for other in useful & lexical)
                }
            ),
            "distinct_escaped_addresses": len({key[2] for key in structural_escapes}),
            "support_family_membership": dict(
                sorted(
                    Counter(
                        family
                        for key in structural_escapes
                        for family in candidates[key]["structural_families"]
                    ).items()
                )
            ),
        },
        "dense_complementarity": dense_outside,
        "known_useful_oracle_at_k5": {
            "description": "non-executable lower-bound ceiling over known useful labels, with unknown candidates left unknown",
            "total_retained_known_useful": sum(
                row["oracle_known_useful_at_k5"] for row in per_case
            ),
            "lexical_only_total_retained_known_useful": sum(
                min(5, row["lexical_known_useful"]) for row in per_case
            ),
            "structural_only_total_retained_known_useful": sum(
                min(5, row["structural_known_useful"]) for row in per_case
            ),
            "canonical_top_five_known_useful": surface_summaries["canonical_top_five"][
                "known_useful"
            ],
            "cases_with_at_least_one_known_useful": sum(
                int(row["heterogeneous_known_useful"]) > 0 for row in per_case
            ),
        },
        "headroom_case_distribution": {
            str(amount): count for amount, count in headroom.items()
        },
        "oracle_k5_headroom_case_distribution": {
            str(amount): count
            for amount, count in sorted(
                Counter(
                    row["oracle_k5_headroom_beyond_canonical"] for row in per_case
                ).items()
            )
        },
        "per_case": per_case,
        "dense_case_details": dense_details,
        "candidates": [
            {
                **candidates[key],
                "modalities": [
                    name
                    for name, surface in (
                        ("lexical", lexical),
                        ("structural", structural),
                        ("dense", dense),
                    )
                    if key in surface
                ],
                "outcome_knowledge": outcomes.get(key, "NEVER_ADJUDICATED"),
                "judgment_sources": judgment_sources.get(key, []),
            }
            for key in sorted(all_keys)
        ],
        "new_judgments_created": False,
        "confirmation_executed": False,
        "fusion_executed": False,
    }
    return {
        "schema": "devtools-i35-heterogeneous-union-development-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }


def write_result(root: Path = ROOT) -> dict[str, Any]:
    """Persist a deterministic result, rejecting changed prior output."""
    artifact = build_result(root)
    path = root / RESULT_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing Heterogeneous Union result differs.")
    write_artifact(path=path, payload=artifact)
    return artifact


if __name__ == "__main__":
    write_result()
