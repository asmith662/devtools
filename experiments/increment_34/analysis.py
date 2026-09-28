# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, PLR0912, PLR2004, TRY003, C901
"""Deduplicate completed development structural surfaces without new judgments."""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import TYPE_CHECKING, Any

from experiments.increment_25.development import write_artifact
from experiments.increment_26.development_judgments import USEFULNESS_SEMANTICS
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import (
    _digest,
    read_candidate_artifact,
)
from experiments.increment_30.mechanics import _verified_json
from experiments.retrieval_judgment_coverage import (
    judgment_identity,
    validated_outcome_mappings,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

ROOT = Path(__file__).resolve().parent
RESULT_NAME = "structural_union_development_results.json"
DIRECT = ("imports", "references_calls", "containment", "mirrored_paths")
FAMILIES = (*DIRECT, "graph_1", "graph_2")
SOURCE_FILES = {
    "imports": (
        "increment_27/structural_import_candidates.json.gz",
        "increment_27/structural_import_development_results.json",
    ),
    "references_calls": (
        "increment_29/references_calls_candidates.json",
        "increment_29/references_calls_development_results.json",
    ),
    "containment": (
        "increment_30/package_containment_candidates.json",
        "increment_30/package_containment_development_results.json",
    ),
    "mirrored_paths": (
        "increment_31/mirrored_test_paths_candidates.json",
        "increment_31/mirrored_test_paths_development_results.json",
    ),
    "graph_1": (
        "increment_32/graph_round_one_candidates.json",
        "increment_32/graph_round_one_development_results.json",
    ),
    "graph_2": (
        "increment_33/graph_round_two_candidates.json",
        "increment_33/graph_round_two_development_results.json",
    ),
}
LEXICAL_PATH = "increment_27/lexical_comparison_rankings.json"
METHODS = ("canonical", "bm25_plus", "identifier", "path", "rrf")
STATES = ("USEFUL", "NOT_USEFUL", "UNJUDGED")
CaseResource = tuple[str, str, str]


def _key(case_id: str, parent: str, address: str) -> CaseResource:
    return (case_id, parent, address)


def _read_sources(
    root: Path,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any], dict[str, Any]]:
    """Read and fingerprint only completed development candidates and results."""
    sources: dict[str, dict[str, Any]] = {}
    fingerprints: dict[str, Any] = {}
    for family, (candidate_name, result_name) in SOURCE_FILES.items():
        candidate_path, result_path = (
            root.parent / candidate_name,
            root.parent / result_name,
        )
        candidate = (
            read_candidate_artifact(candidate_path)
            if family == "imports"
            else _verified_json(candidate_path)
        )
        result = _verified_json(result_path)
        payload = result["payload"]
        if (
            payload.get("heldout_executed", False)
            or payload.get("confirmation_executed", False)
            or candidate["heldout_executed"]
        ):
            raise ValueError("Structural Union source includes confirmation execution.")
        sources[family] = {"candidate": candidate, "result": result}
        fingerprints[family] = {
            "candidate": {
                "path": candidate_name,
                "content_identity": candidate["content_identity"],
                "sha256": sha256_file(candidate_path),
            },
            "result": {
                "path": result_name,
                "content_identity": result["content_identity"],
                "sha256": sha256_file(result_path),
            },
        }
    lexical_path = root.parent / LEXICAL_PATH
    lexical = _verified_json(lexical_path)
    fingerprints["lexical"] = {
        "path": LEXICAL_PATH,
        "content_identity": lexical["content_identity"],
        "sha256": sha256_file(lexical_path),
    }
    return sources, lexical, fingerprints


def _candidate_addresses(family: str, case: Mapping[str, Any]) -> set[str]:
    if family == "imports":
        return {
            str(row["address"])
            for arm in case["arms"].values()
            for row in arm["candidates"]
        }
    return {str(row["address"]) for row in case["candidates"]}


def _candidate_sets(
    sources: Mapping[str, Mapping[str, Any]], lexical: Mapping[str, Any]
) -> tuple[
    dict[str, set[CaseResource]],
    dict[CaseResource, dict[str, Any]],
    dict[str, set[CaseResource]],
    dict[str, set[CaseResource]],
]:
    """Validate frozen case identities and retain only per-family membership."""
    import_cases = sources["imports"]["candidate"]["cases"]
    ids = [str(case["case_id"]) for case in import_cases]
    if (
        len(ids) != 24
        or len(set(ids)) != 24
        or [case["case_id"] for case in lexical["cases"]] != ids
    ):
        raise ValueError("Structural Union development case population differs.")
    basis = {str(case["case_id"]): case for case in import_cases}
    for family in FAMILIES:
        if [case["case_id"] for case in sources[family]["candidate"]["cases"]] != ids:
            raise ValueError("Structural Union case ordering differs.")
    lexical_top_five: dict[str, set[CaseResource]] = {}
    lexical_all: dict[str, set[CaseResource]] = {}
    for case in lexical["cases"]:
        case_id = str(case["case_id"])
        original = basis[case_id]
        parent = str(original["parent_snapshot_sha"])
        if (
            case["parent_snapshot_sha"] != parent
            or case["query_text"] != original["information_need"]["lexical_query"]
        ):
            raise ValueError("Frozen lexical query/snapshot differs.")
        canonical = case["rankings"]["canonical"]
        lexical_top_five[case_id] = {
            _key(case_id, parent, str(row["address"]))
            for row in canonical
            if int(row["rank"]) <= 5
        }
        lexical_all[case_id] = {
            _key(case_id, parent, str(row["address"]))
            for method in METHODS
            for row in case["rankings"][method]
        }
        if len(lexical_top_five[case_id]) != 5 or {
            str(row["address"]) for row in original["seeds"]
        } != {key[2] for key in lexical_top_five[case_id]}:
            raise ValueError("Canonical lexical top-five seeds differ.")
    family_sets: dict[str, set[CaseResource]] = {}
    records: dict[CaseResource, dict[str, Any]] = {}
    for family in FAMILIES:
        population: set[CaseResource] = set()
        for case in sources[family]["candidate"]["cases"]:
            case_id = str(case["case_id"])
            original = basis[case_id]
            parent = str(case["parent_snapshot_sha"])
            if (
                parent != original["parent_snapshot_sha"]
                or case["information_need"] != original["information_need"]
            ):
                raise ValueError(
                    "Structural candidate InformationNeed/snapshot differs."
                )
            for address in _candidate_addresses(family, case):
                key = _key(case_id, parent, address)
                population.add(key)
                record = records.setdefault(
                    key,
                    {
                        "case_id": case_id,
                        "information_need": original["information_need"],
                        "parent_snapshot_sha": parent,
                        "address": address,
                        "usefulness_semantics": USEFULNESS_SEMANTICS,
                        "families": [],
                    },
                )
                record["families"].append(family)
        family_sets[family] = population
    return family_sets, records, lexical_top_five, lexical_all


def _result_rows(family: str, payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    if family == "imports":
        return [
            row
            for row in payload["joined_population"]
            if row["outgoing_structural"] or row["incoming_structural"]
        ]
    if family == "graph_1":
        return [*payload["reused_pairs"], *payload["sampled_pairs"]]
    return list(payload["joined_pairs"])


def _outcomes(
    sources: Mapping[str, Mapping[str, Any]],
    family_sets: Mapping[str, set[CaseResource]],
    records: Mapping[CaseResource, Mapping[str, Any]],
) -> tuple[dict[CaseResource, str], dict[CaseResource, list[dict[str, str]]]]:
    """Check each exact development label, reject any cross-source conflict."""
    by_key: dict[CaseResource, str] = {}
    supports: dict[CaseResource, list[dict[str, str]]] = defaultdict(list)
    for family in FAMILIES:
        payload = sources[family]["result"]["payload"]
        rows = _result_rows(family, payload)
        seen: set[CaseResource] = set()
        normalized: list[dict[str, Any]] = []
        for row in rows:
            key = _key(
                str(row["case_id"]),
                str(row["parent_snapshot_sha"]),
                str(row["address"]),
            )
            if key not in family_sets[family] or key in seen:
                raise ValueError(
                    "Judgment result escaped or duplicated family candidates."
                )
            seen.add(key)
            if family == "graph_2" and row["population"] == "unsampled_unadjudicated":
                if "judgment" in row:
                    raise ValueError("Graph-2 unsampled candidate acquired a judgment.")
                continue
            if "judgment" not in row or row["judgment"] not in STATES:
                raise ValueError("Frozen family judgment is missing or invalid.")
            base = records[key]
            if (
                row.get("information_need", base["information_need"])
                != base["information_need"]
                or row.get("usefulness_semantics", USEFULNESS_SEMANTICS)
                != USEFULNESS_SEMANTICS
            ):
                raise ValueError(
                    "Judgment purpose or semantics differs from candidate."
                )
            normalized_row = {**base, "judgment": str(row["judgment"])}
            normalized.append(normalized_row)
            state = str(row["judgment"])
            previous = by_key.get(key)
            if previous is not None and previous != state:
                raise ValueError("Conflicting exact structural development judgments.")
            by_key[key] = state
            supports[key].append({"family": family, "judgment": state})
        validated_outcome_mappings(normalized, {})
        if family in DIRECT and seen != family_sets[family]:
            raise ValueError("Direct family lacks complete frozen judgment rows.")
        if family == "graph_2" and seen != family_sets[family]:
            raise ValueError("Graph-2 result omits a candidate classification.")
        if (
            family == "graph_1"
            and len(seen)
            != payload["population_counts"]["exact_reused"]
            + payload["population_counts"]["new_sampled_adjudicated"]
        ):
            raise ValueError("Graph-1 sampled coverage differs.")
    # The judgment helper omits case id from its purpose-relative identity;
    # every shared identity must still carry one consistent label.
    by_judgment_identity: dict[tuple[str, ...], str] = {}
    for key, state in by_key.items():
        identity = judgment_identity(records[key])
        previous = by_judgment_identity.get(identity)
        if previous is not None and previous != state:
            raise ValueError(
                "Conflicting exact purpose-relative judgments across cases."
            )
        by_judgment_identity[identity] = state
    return by_key, supports


def _surface(
    keys: set[CaseResource],
    outcomes: Mapping[CaseResource, str],
    top: set[CaseResource],
    positive: set[CaseResource],
) -> dict[str, Any]:
    hard = keys - positive
    return {
        "candidate_pairs": len(keys),
        "distinct_addresses": len({key[2] for key in keys}),
        "cases": len({key[0] for key in keys}),
        "max_candidates_per_case": max(
            Counter(key[0] for key in keys).values(), default=0
        ),
        "outside_canonical_top_five": len(keys - top),
        "outside_all_positive_lexical": len(hard),
        "outside_all_positive_lexical_distinct_addresses": len(
            {key[2] for key in hard}
        ),
        "cases_with_hard_lexical_escape": len({key[0] for key in hard}),
        "known_useful": sum(outcomes.get(key) == "USEFUL" for key in keys),
        "known_not_useful": sum(outcomes.get(key) == "NOT_USEFUL" for key in keys),
        "known_unjudged": sum(outcomes.get(key) == "UNJUDGED" for key in keys),
        "never_adjudicated": sum(key not in outcomes for key in keys),
    }


def build_result(root: Path = ROOT) -> dict[str, Any]:
    """Join native frozen surfaces, preserving support and judgment boundaries."""
    sources, lexical, fingerprints = _read_sources(root)
    family_sets, records, top_by_case, positive_by_case = _candidate_sets(
        sources, lexical
    )
    outcomes, judgment_supports = _outcomes(sources, family_sets, records)
    top = set().union(*top_by_case.values())
    positive = set().union(*positive_by_case.values())
    direct = set().union(*(family_sets[family] for family in DIRECT))
    graph_one = direct | family_sets["graph_1"]
    complete = graph_one | family_sets["graph_2"]
    if family_sets["graph_1"] & direct or family_sets["graph_2"] & graph_one:
        raise ValueError("Frozen graph novelty overlaps an earlier union.")
    if set(records) != complete:
        raise ValueError("Union candidate records differ from family surfaces.")
    overlap = {
        left: {right: len(family_sets[left] & family_sets[right]) for right in DIRECT}
        for left in DIRECT
    }
    support_histogram = {
        str(count): frequency
        for count, frequency in sorted(
            Counter(
                sum(key in family_sets[family] for family in DIRECT) for key in direct
            ).items()
        )
    }
    leave_one_out = {}
    for family in DIRECT:
        others = set().union(
            *(family_sets[other] for other in DIRECT if other != family)
        )
        unique = direct - others
        leave_one_out[family] = {
            "lost_pairs": len(unique),
            "lost_known_useful": sum(outcomes.get(key) == "USEFUL" for key in unique),
        }
    chronology = []
    running: set[CaseResource] = set()
    for family in FAMILIES:
        added = family_sets[family] - running
        existing_addresses = {key[2] for key in running}
        chronology.append(
            {
                "family": family,
                "new_pairs": len(added),
                "new_distinct_addresses": len(
                    {key[2] for key in added} - existing_addresses
                ),
                "known_useful_new_pairs": sum(
                    outcomes.get(key) == "USEFUL" for key in added
                ),
                "known_useful_hard_lexical_escapes_new_pairs": sum(
                    outcomes.get(key) == "USEFUL" and key not in positive
                    for key in added
                ),
                "known_unjudged_new_pairs": sum(
                    outcomes.get(key) == "UNJUDGED" for key in added
                ),
                "never_adjudicated_new_pairs": sum(
                    key not in outcomes for key in added
                ),
                "cumulative_pairs": len(running | family_sets[family]),
            }
        )
        running |= family_sets[family]
    useful = {key for key in complete if outcomes.get(key) == "USEFUL"}
    useful_by_family = {
        family: len(useful & family_sets[family]) for family in FAMILIES
    }
    graph_one_result = sources["graph_1"]["result"]["payload"]
    graph_two_result = sources["graph_2"]["result"]["payload"]
    graph_one_candidates = sources["graph_1"]["candidate"]["summary"]
    graph_two_candidates = sources["graph_2"]["candidate"]["summary"]
    if graph_one_result["population_counts"]["complete_novel_candidate_pairs"] != len(
        family_sets["graph_1"]
    ) or graph_two_result["complete_candidate_summary"]["candidate_count"] != len(
        family_sets["graph_2"]
    ):
        raise ValueError("Graph sampling result differs from frozen candidate surface.")
    candidate_rows = []
    for key in sorted(complete):
        row = records[key]
        state = outcomes.get(key)
        candidate_rows.append(
            {
                **row,
                "families": sorted(row["families"], key=FAMILIES.index),
                "support_artifact_refs": [
                    {"family": family, "case_id": key[0], "address": key[2]}
                    for family in FAMILIES
                    if family in row["families"]
                ],
                "outside_canonical_top_five": key not in top,
                "outside_all_positive_lexical": key not in positive,
                "outcome_knowledge": "NEVER_ADJUDICATED" if state is None else state,
                "judgment_sources": judgment_supports.get(key, []),
            }
        )
    payload = {
        "development_case_ids": [
            case["case_id"] for case in sources["imports"]["candidate"]["cases"]
        ],
        "source_artifacts": fingerprints,
        "family_order": list(FAMILIES),
        "candidate_identity": "case + exact InformationNeed purpose/query + parent snapshot + resource address + usefulness semantics",
        "support_link_rule": "family, case_id, and address identify the authoritative frozen candidate record in that family's fingerprinted candidate artifact; graph paths remain only there",
        "outcome_states": [*STATES, "NEVER_ADJUDICATED"],
        "direct_surface": _surface(direct, outcomes, top, positive),
        "direct_plus_graph_one": _surface(graph_one, outcomes, top, positive),
        "complete_structural_surface": _surface(complete, outcomes, top, positive),
        "direct_support_multiplicity": support_histogram,
        "direct_pairwise_overlap": overlap,
        "direct_leave_one_out": leave_one_out,
        "chronological_marginal": chronology,
        "known_useful_surface": {
            "candidate_pairs": len(useful),
            "cases": len({key[0] for key in useful}),
            "distinct_addresses": len({key[2] for key in useful}),
            "outside_canonical_top_five": len(useful - top),
            "outside_all_positive_lexical": len(useful - positive),
            "support_family_membership": useful_by_family,
        },
        "graph_sampling_boundaries": {
            "graph_1": {
                "complete_pairs": len(family_sets["graph_1"]),
                "population_counts": graph_one_result["population_counts"],
                "sampled_useful_proportion": graph_one_result[
                    "sampled_useful_proportion"
                ],
            },
            "graph_2": {
                "complete_pairs": len(family_sets["graph_2"]),
                "population_counts": graph_two_result["population_counts"],
                "sampled_outcome_counts": graph_two_result["sampled_outcome_counts"],
                "sampled_useful_interval": graph_two_result["sampled_useful_interval"],
            },
            "samples_pooled": False,
        },
        "cost_progression": {
            "direct_pairs": len(direct),
            "graph_1_new_pairs": len(family_sets["graph_1"]),
            "graph_1_retained_typed_paths": graph_one_candidates[
                "retained_typed_paths"
            ],
            "graph_1_inverse_import_path_fanout": graph_one_candidates[
                "second_edge_path_fanout_by_direction"
            ]["import:inverse"],
            "graph_2_new_pairs": len(family_sets["graph_2"]),
            "graph_2_complete_typed_paths": graph_two_candidates[
                "complete_typed_paths"
            ],
            "graph_2_novel_typed_paths": graph_two_candidates["novel_typed_paths"],
            "graph_2_import_path_fanout": {
                direction: graph_two_candidates["third_edge_path_by_direction"][
                    f"import:{direction}"
                ]
                for direction in ("forward", "inverse")
            },
        },
        "candidates": candidate_rows,
        "new_judgments_created": False,
        "confirmation_executed": False,
    }
    return {
        "schema": "devtools-i34-structural-union-development-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }


def write_result(root: Path = ROOT) -> dict[str, Any]:
    """Persist only the deterministic Structural Union analysis."""
    artifact = build_result(root)
    path = root / RESULT_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing Structural Union result differs.")
    write_artifact(path=path, payload=artifact)
    return artifact


if __name__ == "__main__":
    write_result()
