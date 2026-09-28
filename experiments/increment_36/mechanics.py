# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, EM102, PLR2004, TRY003, C901
"""Freeze one RRF selection without loading development usefulness outcomes."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from experiments.increment_25.development import write_artifact
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_30.mechanics import _verified_json

if TYPE_CHECKING:
    from collections.abc import Mapping

ROOT = Path(__file__).resolve().parent
FREEZE_NAME = "simple_rank_fusion_freeze.json"
RRF_CONSTANT = 60
BUDGET = 5
INPUTS = {
    "heterogeneous_union": (
        "increment_35/heterogeneous_union_development_results.json",
        "6d00ecc14e6845e3dd1289f9ab52a3b4a1681c3b2c187a37eed3ff2760e6da4f",
    ),
    "lexical_rankings": (
        "increment_27/lexical_comparison_rankings.json",
        "7d566ba0e402d180b2ddfc0840f3002ec8c8337edbed0e3d14e391b717b5f46e",
    ),
    "canonical_basis": (
        "increment_27/canonical_positive_lexical_rankings.json",
        "6072195afe50376722c06157ae04e8b33ed1346e4c75c763d83f22f30dd72657",
    ),
    "dense_candidates": (
        "increment_26/development_candidate_evidence.json",
        "3b78cd07360f277523ca195401d1bc322ad28c1d7e03c1ea569490b87afa277d",
    ),
}


def _input_hashes(root: Path) -> dict[str, dict[str, str]]:
    """Fingerprint the outcome-bearing union as bytes, never decode it here."""
    found: dict[str, dict[str, str]] = {}
    for name, (relative, expected) in INPUTS.items():
        actual = sha256_file(root.parent / relative)
        if actual != expected:
            raise ValueError(f"Frozen fusion source differs: {name}.")
        found[name] = {"path": relative, "sha256": actual}
    return found


def _ranked_case(
    *,
    lexical: Mapping[str, Any],
    basis: Mapping[str, Any],
    dense: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Fuse one frozen lexical RRF list and an optional frozen dense list."""
    case_id = lexical["case_id"]
    parent = lexical["parent_snapshot_sha"]
    if (
        basis["case_id"] != case_id
        or basis["parent_snapshot_sha"] != parent
        or basis["information_need"]["lexical_query"] != lexical["query_text"]
    ):
        raise ValueError("Lexical InformationNeed/snapshot differs from frozen basis.")
    lexical_ranks = {
        row["address"]: int(row["rank"]) for row in lexical["rankings"]["rrf"]
    }
    if len(lexical_ranks) != len(lexical["rankings"]["rrf"]):
        raise ValueError("Frozen lexical RRF repeats an address.")
    dense_ranks: dict[str, int] = {}
    if dense is not None:
        if (
            dense["case_id"] != case_id
            or dense["parent_snapshot_sha"] != parent
            or dense["information_need"] != basis["information_need"]
            or dense["corpus"]["corpus_id"] != lexical["corpus_id"]
            or dense["corpus"]["resource_count"] != lexical["corpus_resource_count"]
        ):
            raise ValueError("Dense case identity/corpus differs from lexical basis.")
        dense_ranks = {
            row["address"]: rank
            for rank, row in enumerate(dense["semantic_candidates"], 1)
        }
        if len(dense_ranks) != len(dense["semantic_candidates"]):
            raise ValueError("Frozen dense ranking repeats an address.")
    ranking: list[dict[str, Any]] = []
    for address in lexical_ranks.keys() | dense_ranks.keys():
        ranks = {}
        if address in lexical_ranks:
            ranks["lexical_rrf"] = lexical_ranks[address]
        if address in dense_ranks:
            ranks["dense"] = dense_ranks[address]
        ranking.append(
            {
                "address": address,
                "source_ranks": ranks,
                "score": sum(1 / (RRF_CONSTANT + rank) for rank in ranks.values()),
            }
        )
    # Earlier lexical RRF rank is a pre-outcome tie break; a dense-only address
    # follows tied lexical evidence. Address gives the final deterministic tie.
    ranking.sort(
        key=lambda row: (
            -row["score"],
            lexical_ranks.get(row["address"], float("inf")),
            row["address"],
        )
    )
    for rank, row in enumerate(ranking, 1):
        row["rank"] = rank
    if len(ranking) < BUDGET:
        raise ValueError("A development case lacks five ranked candidates.")
    return {
        "case_id": case_id,
        "information_need": basis["information_need"],
        "parent_snapshot_sha": parent,
        "source_coverage": ["lexical_rrf", "dense"]
        if dense is not None
        else ["lexical_rrf"],
        "ranking": ranking,
        "selected_top_five": [row["address"] for row in ranking[:BUDGET]],
    }


def build_freeze(root: Path = ROOT) -> dict[str, Any]:
    """Bind RRF inputs, one parameter, full ranking, and K=5 before outcomes."""
    fingerprints = _input_hashes(root)
    lexical = _verified_json(root.parent / INPUTS["lexical_rankings"][0])
    basis = cast(
        "dict[str, Any]", _read_json(root.parent / INPUTS["canonical_basis"][0])
    )
    dense = cast(
        "dict[str, Any]", _read_json(root.parent / INPUTS["dense_candidates"][0])
    )
    lexical_cases = lexical["cases"]
    basis_cases = basis["cases"]
    dense_by_case = {case["case_id"]: case for case in dense["cases"]}
    if (
        len(lexical_cases) != 24
        or len(basis_cases) != 24
        or len(dense_by_case) != 8
        or [case["case_id"] for case in lexical_cases]
        != [case["case_id"] for case in basis_cases]
        or len({case["case_id"] for case in dense["cases"]}) != len(dense["cases"])
        or not set(dense_by_case).issubset({case["case_id"] for case in lexical_cases})
    ):
        raise ValueError("Frozen fusion development population differs.")
    cases = [
        _ranked_case(
            lexical=lexical_case,
            basis=basis_case,
            dense=dense_by_case.get(lexical_case["case_id"]),
        )
        for lexical_case, basis_case in zip(lexical_cases, basis_cases, strict=True)
    ]
    payload = {
        "source_artifacts": fingerprints,
        "source_content_identities": {
            "lexical_rankings": lexical["content_identity"],
            "dense_execution": dense["execution_identity"],
            "heterogeneous_union": "db4a83f891e1549970889276f7f2878d8f5e417020d5b67f378a5f267e1a8337",
        },
        "algorithm": "standard reciprocal rank fusion of frozen lexical RRF as one ranked modality and frozen dense as one ranked modality where available",
        "formula": "sum(1 / (60 + positive_rank)) over available source lists",
        "constant": RRF_CONSTANT,
        "budget_k": BUDGET,
        "ranked_inputs": ["lexical_rrf", "dense"],
        "excluded_inputs": {
            "bm25_plus": "overlapping lexical source, not independently weighted",
            "canonical_identifier_path": "already aggregated in frozen lexical RRF",
            "structural": "no frozen relevance ranking",
        },
        "missing_dense_behavior": "no dense contribution; one-list RRF preserves frozen lexical RRF order",
        "tie_rule": "higher score, then lower frozen lexical RRF rank where present, then resource address ascending",
        "candidate_identity": "case + exact InformationNeed/query + parent snapshot + repository resource address",
        "source_coverage_cases": {"lexical_rrf": 24, "dense": 8},
        "cases": cases,
        "usefulness_outcomes_loaded": False,
        "confirmation_executed": False,
    }
    return {
        "schema": "devtools-i36-simple-rrf-pre-outcome-freeze-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }


def write_freeze(root: Path = ROOT) -> dict[str, Any]:
    """Write the immutable pre-outcome RRF selection surface."""
    artifact = build_freeze(root)
    path = root / FREEZE_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing pre-outcome fusion freeze differs.")
    write_artifact(path=path, payload=artifact)
    return artifact


if __name__ == "__main__":
    write_freeze()
