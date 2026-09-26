# Copyright (c) 2026
# ruff: noqa: COM812, EM101, PLR2004, TRY003
"""Descriptive evidence diagnostics on frozen Increment-27 development pairs."""

from __future__ import annotations

from collections import Counter
from math import sqrt
from pathlib import PurePosixPath
from statistics import median
from typing import TYPE_CHECKING, Any, cast

from experiments.increment_25.development import write_artifact
from experiments.increment_26.development_judgments import USEFULNESS_SEMANTICS
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.fusion_results import (
    build_results as build_fusion_results,
)
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_27.window_results import (
    build_results as build_window_results,
)
from experiments.increment_27.window_unit import audit_saved_baseline

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

DATASET_NAME = "candidate_evidence_dataset.json"
ANALYSIS_NAME = "candidate_evidence_diagnostic.json"
METHODS = ("canonical", "bm25_plus", "identifier", "path", "rrf")
STATES = ("USEFUL", "NOT_USEFUL", "UNJUDGED")
SOURCE_NAMES = (
    "experiment_freeze.json",
    "canonical_positive_lexical_rankings.json",
    "lexical_comparison_rankings.json",
    "structural_import_candidates.json.gz",
    "structural_import_development_results.json",
    "structural_import_judgment_freeze.json",
    "comparison_frozen_judgments.json",
    "lexical_top5_development_results.json",
    "lexical_top5_frozen_judgments.json",
    "window_unit_development_results.json",
    "window_unit_frozen_judgments.json",
    "window_resource_rankings.json",
    "existing_judgment_depth_diagnostics.json",
    "lexical_import_fusion_freeze.json",
    "lexical_import_fusion_candidates.json",
    "lexical_import_fusion_development_results.json",
)
FEATURE_CLASSES = {
    "canonical_member": "A: native retrieval evidence",
    "canonical_rank": "A: native retrieval evidence",
    "canonical_score": "A: native retrieval evidence",
    "canonical_content_score": "A: native retrieval evidence",
    "canonical_filename_score": "A: native retrieval evidence",
    "bm25_plus_member": "A: native retrieval evidence",
    "bm25_plus_rank": "A: native retrieval evidence",
    "bm25_plus_score": "A: native retrieval evidence",
    "identifier_member": "A: native retrieval evidence",
    "identifier_rank": "A: native retrieval evidence",
    "identifier_score": "A: native retrieval evidence",
    "path_member": "A: native retrieval evidence",
    "path_rank": "A: native retrieval evidence",
    "path_score": "A: native retrieval evidence",
    "rrf_member": "A: saved derived retrieval evidence",
    "rrf_rank": "A: saved derived retrieval evidence",
    "rrf_score": "A: saved derived retrieval evidence",
    "lexical_method_count": "B: deterministic derivation",
    "best_lexical_rank": "B: deterministic derivation",
    "multi_lexical_method": "B: deterministic derivation",
    "structural_member": "B: deterministic derivation from native import evidence",
    "outgoing_import": "A: native candidate evidence",
    "incoming_import": "A: native candidate evidence",
    "both_import_directions": "B: deterministic derivation",
    "structural_support_count": "B: deterministic derivation",
    "distinct_relation_count": "B: deterministic derivation",
    "distinct_seed_count": "B: deterministic derivation",
    "best_seed_rank": "B: deterministic derivation from seed lexical rank",
    "path_count": "B: deterministic derivation from retained paths",
    "window_positive_rank": "A: saved retrieval evidence",
    "window_count": "C: resource characteristic in saved window corpus",
    "resource_suffix": "C: resource address characteristic",
    "resource_lexical_token_length": "C: unavailable in saved candidate records",
}
BINARY = (
    "canonical_member",
    "bm25_plus_member",
    "identifier_member",
    "path_member",
    "rrf_member",
    "multi_lexical_method",
    "structural_member",
    "outgoing_import",
    "incoming_import",
    "both_import_directions",
)
NUMERIC_DIRECTIONS = {
    "canonical_rank": "lower",
    "canonical_score": "higher",
    "canonical_content_score": "higher",
    "canonical_filename_score": "higher",
    "bm25_plus_rank": "lower",
    "bm25_plus_score": "higher",
    "identifier_rank": "lower",
    "identifier_score": "higher",
    "path_rank": "lower",
    "path_score": "higher",
    "rrf_rank": "lower",
    "rrf_score": "higher",
    "lexical_method_count": "higher",
    "best_lexical_rank": "lower",
    "structural_support_count": "higher",
    "distinct_relation_count": "higher",
    "distinct_seed_count": "higher",
    "best_seed_rank": "lower",
    "path_count": "higher",
    "window_positive_rank": "lower",
    "window_count": "higher",
}


def _source_bindings(root: Path) -> dict[str, dict[str, str | None]]:
    bindings = {}
    for name in SOURCE_NAMES:
        path = root / name
        identity: str | None = None
        if name.endswith(".json"):
            raw_identity = _read_json(path).get("content_identity")
            identity = str(raw_identity) if raw_identity is not None else None
        bindings[name] = {
            "sha256": sha256_file(path),
            "content_identity": identity,
        }
    return bindings


def _normalize_state(value: str) -> str:
    states = {
        "useful": "USEFUL",
        "not-useful": "NOT_USEFUL",
        "not_useful": "NOT_USEFUL",
        "unjudged": "UNJUDGED",
    }
    state = states.get(value.lower())
    if state is None:
        raise ValueError("Unknown frozen usefulness state.")
    return state


def _labels(
    root: Path, cards: dict[str, dict[str, Any]]
) -> dict[tuple[str, str, str, str, str], dict[str, Any]]:
    fusion = cast(
        "dict[str, Any]",
        _read_json(root / "lexical_import_fusion_development_results.json"),
    )
    window = cast(
        "dict[str, Any]", _read_json(root / "window_unit_development_results.json")
    )
    depth = cast(
        "dict[str, Any]", _read_json(root / "existing_judgment_depth_diagnostics.json")
    )
    structural_saved = cast(
        "dict[str, Any]",
        _read_json(root / "structural_import_development_results.json"),
    )
    top5_saved = cast(
        "dict[str, Any]", _read_json(root / "lexical_top5_development_results.json")
    )
    if fusion != build_fusion_results(root) or window != build_window_results(root):
        raise ValueError("Frozen development judgment joins do not reproduce.")
    sources = (
        (
            "structural",
            structural_saved["payload"]["joined_population"],
        ),
        (
            "top5",
            top5_saved["payload"]["joined_pairs"],
        ),
        ("window", window["payload"]["pairs"]),
        (
            "prior_depth",
            [
                {"case_id": case["case_id"], **row}
                for case in depth["cases"]
                for row in case["judged_resources"]
            ],
        ),
    )
    labels: dict[tuple[str, str, str, str, str], dict[str, Any]] = {}
    for source_name, rows in sources:
        for row in rows:
            case_id, address = str(row["case_id"]), str(row["address"])
            card = cards[case_id]
            key = (
                card["information_need"]["purpose"],
                card["information_need"]["lexical_query"],
                card["parent_snapshot_sha"],
                address,
                USEFULNESS_SEMANTICS,
            )
            state = _normalize_state(str(row["judgment"]))
            if row["parent_snapshot_sha"] != card["parent_snapshot_sha"]:
                raise ValueError("Prior judgment parent differs from frozen case.")
            need = row.get("information_need", row.get("information_need_identity"))
            if need is not None and need != card["information_need"]:
                raise ValueError("Prior judgment purpose or query differs.")
            if (
                row.get(
                    "usefulness_semantics",
                    row.get("judgment_semantics", USEFULNESS_SEMANTICS),
                )
                != USEFULNESS_SEMANTICS
            ):
                raise ValueError("Prior judgment semantics differ.")
            previous = labels.get(key)
            if previous and previous["usefulness"] != state:
                raise ValueError("Exact frozen judgment sources disagree.")
            if previous:
                previous["judgment_sources"].append(source_name)
            else:
                labels[key] = {
                    "case_id": case_id,
                    "usefulness": state,
                    "judgment_sources": [source_name],
                }
    return labels


def build_dataset(root: Path) -> dict[str, Any]:
    """Join persisted retrieval evidence to exact frozen judgments only."""
    baseline, heldout = audit_saved_baseline(root)
    comparison = cast(
        "dict[str, Any]", _read_json(root / "lexical_comparison_rankings.json")
    )
    structural = cast(
        "dict[str, Any]",
        _read_json(root / "structural_import_development_results.json"),
    )
    windows = cast("dict[str, Any]", _read_json(root / "window_resource_rankings.json"))
    fusion_candidates = cast(
        "dict[str, Any]", _read_json(root / "lexical_import_fusion_candidates.json")
    )
    cards = {
        str(case["case_id"]): {
            "information_need": case["information_need"],
            "parent_snapshot_sha": case["parent_snapshot_sha"],
        }
        for case in fusion_candidates["payload"]["cases"]
    }
    development = [case["case_id"] for case in baseline]
    if (
        len(development) != 24
        or len(heldout) != 14
        or set(development) & set(heldout)
        or list(cards) != development
        or [case["case_id"] for case in comparison["cases"]] != development
        or [case["case_id"] for case in windows["cases"]] != development
        or [case["case_id"] for case in fusion_candidates["payload"]["cases"]]
        != development
        or fusion_candidates["payload"]["heldout_case_ids_sealed"] != heldout
    ):
        raise ValueError("Development evidence partition differs.")
    labels = _labels(root, cards)
    structural_map = {
        (row["case_id"], row["address"]): row
        for row in structural["payload"]["joined_population"]
        if row["outgoing_structural"] or row["incoming_structural"]
    }
    indexed = {}
    for case, window in zip(comparison["cases"], windows["cases"], strict=True):
        case_id = str(case["case_id"])
        indexed[case_id] = {
            "methods": {
                method: {item["address"]: item for item in case["rankings"][method]}
                for method in METHODS
            },
            "window": {
                item["address"]: item for item in window["positive_resource_ordering"]
            },
            "window_counts": window["resource_window_counts"],
        }
        if (
            case["parent_snapshot_sha"] != cards[case_id]["parent_snapshot_sha"]
            or window["parent_snapshot_sha"] != cards[case_id]["parent_snapshot_sha"]
        ):
            raise ValueError("Retrieval evidence parent differs from frozen case.")
    rows = []
    excluded_without_evidence = []
    for key, label in sorted(
        labels.items(), key=lambda item: (item[1]["case_id"], item[0][3])
    ):
        case_id, address = label["case_id"], key[3]
        item = indexed[case_id]
        native = {method: item["methods"][method].get(address) for method in METHODS}
        support = structural_map.get((case_id, address))
        paths = (
            support["structural_supports"]["outgoing"]
            + support["structural_supports"]["incoming"]
            if support
            else []
        )
        method_count = sum(value is not None for value in native.values())
        ranks = [value["rank"] for value in native.values() if value is not None]
        win = item["window"].get(address)
        features = {
            "canonical_member": native["canonical"] is not None,
            "canonical_rank": native["canonical"]["rank"]
            if native["canonical"]
            else None,
            "canonical_score": native["canonical"]["score"]
            if native["canonical"]
            else None,
            "canonical_content_score": native["canonical"]["component_scores"][
                "content"
            ]
            if native["canonical"]
            else None,
            "canonical_filename_score": native["canonical"]["component_scores"][
                "weighted_filename_stem"
            ]
            if native["canonical"]
            else None,
            "bm25_plus_member": native["bm25_plus"] is not None,
            "bm25_plus_rank": native["bm25_plus"]["rank"]
            if native["bm25_plus"]
            else None,
            "bm25_plus_score": native["bm25_plus"]["score"]
            if native["bm25_plus"]
            else None,
            "identifier_member": native["identifier"] is not None,
            "identifier_rank": native["identifier"]["rank"]
            if native["identifier"]
            else None,
            "identifier_score": native["identifier"]["score"]
            if native["identifier"]
            else None,
            "path_member": native["path"] is not None,
            "path_rank": native["path"]["rank"] if native["path"] else None,
            "path_score": native["path"]["score"] if native["path"] else None,
            "rrf_member": native["rrf"] is not None,
            "rrf_rank": native["rrf"]["rank"] if native["rrf"] else None,
            "rrf_score": native["rrf"]["score"] if native["rrf"] else None,
            "lexical_method_count": method_count,
            "best_lexical_rank": min(ranks) if ranks else None,
            "multi_lexical_method": method_count >= 2,
            "structural_member": support is not None,
            "outgoing_import": bool(support and support["outgoing_structural"]),
            "incoming_import": bool(support and support["incoming_structural"]),
            "both_import_directions": bool(
                support
                and support["outgoing_structural"]
                and support["incoming_structural"]
            ),
            "structural_support_count": len(paths) if support else None,
            "distinct_relation_count": len(
                {path["relation_identity"] for path in paths}
            )
            if support
            else None,
            "distinct_seed_count": len({path["seed_address"] for path in paths})
            if support
            else None,
            "best_seed_rank": min(path["seed_rank"] for path in paths)
            if paths
            else None,
            "path_count": len(paths) if support else None,
            "window_positive_rank": win["rank"] if win else None,
            "window_count": item["window_counts"].get(address),
            "resource_suffix": PurePosixPath(address).suffix.lower(),
            "resource_lexical_token_length": None,
        }
        if not any((method_count, support is not None, win is not None)):
            excluded_without_evidence.append({"case_id": case_id, "address": address})
            continue
        rows.append(
            {
                "case_id": case_id,
                "information_need": cards[case_id]["information_need"],
                "parent_snapshot_sha": cards[case_id]["parent_snapshot_sha"],
                "address": address,
                "usefulness_semantics": USEFULNESS_SEMANTICS,
                "usefulness": label["usefulness"],
                "judgment_sources": label["judgment_sources"],
                "features": features,
                "evidence_provenance": {
                    "lexical_methods": [
                        method for method in METHODS if native[method] is not None
                    ],
                    "structural_relation_identities": sorted(
                        {path["relation_identity"] for path in paths}
                    ),
                    "structural_seed_addresses": sorted(
                        {path["seed_address"] for path in paths}
                    ),
                    "structural_directions": [
                        direction
                        for direction in ("outgoing", "incoming")
                        if support and support[f"{direction}_structural"]
                    ],
                },
            }
        )
    if len(
        {
            (
                row["information_need"]["purpose"],
                row["information_need"]["lexical_query"],
                row["parent_snapshot_sha"],
                row["address"],
                row["usefulness_semantics"],
            )
            for row in rows
        }
    ) != len(rows):
        raise ValueError("Candidate evidence table contains duplicate exact pairs.")
    fusion_freeze = cast(
        "dict[str, Any]", _read_json(root / "lexical_import_fusion_freeze.json")
    )
    payload = {
        "development_case_ids": development,
        "heldout_case_ids_sealed": heldout,
        "suspended_increment_26_case_ids_not_executed": fusion_freeze["payload"][
            "suspended_increment_26_case_ids_not_executed"
        ],
        "source_artifacts": _source_bindings(root),
        "feature_provenance_classes": FEATURE_CLASSES,
        "missing_representation": (
            "null means unavailable or no positive evidence; Boolean membership "
            "separately records absence"
        ),
        "rows": rows,
        "excluded_exact_judgments_without_candidate_evidence": (
            excluded_without_evidence
        ),
        "confirmation_executed": False,
        "new_judgments_created": False,
    }
    return {
        "schema": "devtools-i27-candidate-evidence-dataset-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }


def write_dataset(root: Path) -> dict[str, Any]:
    """Persist the exact evidence inventory and frozen-label join."""
    artifact = build_dataset(root)
    path = root / DATASET_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing candidate evidence dataset differs.")
    write_artifact(path=path, payload=artifact)
    return artifact


def _states(rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(row["usefulness"] for row in rows)
    judged = counts["USEFUL"] + counts["NOT_USEFUL"]
    return {
        "total": len(rows),
        "USEFUL": counts["USEFUL"],
        "NOT_USEFUL": counts["NOT_USEFUL"],
        "UNJUDGED": counts["UNJUDGED"],
        "judged_total": judged,
        "useful_rate_among_judged": round(counts["USEFUL"] / judged, 6)
        if judged
        else None,
    }


def _phi(
    true_rows: list[dict[str, Any]], false_rows: list[dict[str, Any]]
) -> float | None:
    a = sum(row["usefulness"] == "USEFUL" for row in true_rows)
    b = sum(row["usefulness"] == "NOT_USEFUL" for row in true_rows)
    c = sum(row["usefulness"] == "USEFUL" for row in false_rows)
    d = sum(row["usefulness"] == "NOT_USEFUL" for row in false_rows)
    denominator = sqrt((a + b) * (c + d) * (a + c) * (b + d))
    return round((a * d - b * c) / denominator, 6) if denominator else None


def _distribution(rows: list[dict[str, Any]], field: str) -> dict[str, Any]:
    out = {}
    for state in ("USEFUL", "NOT_USEFUL"):
        values = [
            row["features"][field]
            for row in rows
            if row["usefulness"] == state and row["features"][field] is not None
        ]
        out[state] = {
            "count": len(values),
            "minimum": min(values) if values else None,
            "median": median(values) if values else None,
            "maximum": max(values) if values else None,
        }
    return out


def _within_case_auc(
    rows: list[dict[str, Any]], field: str, direction: str
) -> dict[str, Any]:
    by_case: dict[str, dict[str, list[float]]] = {}
    for row in rows:
        value = row["features"][field]
        if row["usefulness"] in ("USEFUL", "NOT_USEFUL") and value is not None:
            bucket = by_case.setdefault(
                row["case_id"], {"USEFUL": [], "NOT_USEFUL": []}
            )
            bucket[row["usefulness"]].append(float(value))
    wins = 0.0
    pairs = 0
    cases = 0
    for bucket in by_case.values():
        if bucket["USEFUL"] and bucket["NOT_USEFUL"]:
            cases += 1
        for useful in bucket["USEFUL"]:
            for not_useful in bucket["NOT_USEFUL"]:
                score = useful - not_useful
                if direction == "lower":
                    score = -score
                wins += 1.0 if score > 0 else 0.5 if score == 0 else 0.0
                pairs += 1
    return {
        "within_case_auc": round(wins / pairs, 6) if pairs else None,
        "useful_not_useful_pairs": pairs,
        "cases_with_comparable_pairs": cases,
        "direction": direction,
    }


def _rank(values: list[float]) -> list[float]:
    ordering = sorted(range(len(values)), key=values.__getitem__)
    ranks = [0.0] * len(values)
    start = 0
    while start < len(values):
        end = start + 1
        while end < len(values) and values[ordering[end]] == values[ordering[start]]:
            end += 1
        average = (start + 1 + end) / 2
        for index in ordering[start:end]:
            ranks[index] = average
        start = end
    return ranks


def _spearman(rows: list[dict[str, Any]], first: str, second: str) -> dict[str, Any]:
    pairs = [
        (float(row["features"][first]), float(row["features"][second]))
        for row in rows
        if row["features"][first] is not None and row["features"][second] is not None
    ]
    if len(pairs) < 3:
        return {"n": len(pairs), "spearman": None}
    x, y = (_rank([pair[index] for pair in pairs]) for index in (0, 1))
    mx, my = sum(x) / len(x), sum(y) / len(y)
    numerator = sum((a - mx) * (b - my) for a, b in zip(x, y, strict=True))
    denominator = sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))
    return {
        "n": len(pairs),
        "spearman": round(numerator / denominator, 6) if denominator else None,
    }


def _jaccard(rows: list[dict[str, Any]], first: str, second: str) -> dict[str, Any]:
    both = sum(row["features"][first] and row["features"][second] for row in rows)
    either = sum(row["features"][first] or row["features"][second] for row in rows)
    return {
        "intersection": both,
        "union": either,
        "jaccard": round(both / either, 6) if either else None,
    }


def _profile(rows: list[dict[str, Any]]) -> dict[str, Any]:
    fields = (
        "lexical_method_count",
        "canonical_rank",
        "canonical_score",
        "path_rank",
        "structural_support_count",
        "distinct_seed_count",
        "best_seed_rank",
        "window_count",
    )
    return {
        "states": _states(rows),
        "canonical_positive": sum(row["features"]["canonical_member"] for row in rows),
        "structural": sum(row["features"]["structural_member"] for row in rows),
        "outgoing": sum(row["features"]["outgoing_import"] for row in rows),
        "incoming": sum(row["features"]["incoming_import"] for row in rows),
        "all_lexical_absent": sum(
            row["features"]["lexical_method_count"] == 0 for row in rows
        ),
        "numeric": {
            field: {
                "present": sum(row["features"][field] is not None for row in rows),
                "median_when_present": median(
                    row["features"][field]
                    for row in rows
                    if row["features"][field] is not None
                )
                if any(row["features"][field] is not None for row in rows)
                else None,
            }
            for field in fields
        },
    }


def build_analysis(root: Path) -> dict[str, Any]:
    """Compute predeclared descriptive comparisons without fitting a model."""
    dataset = cast("dict[str, Any]", _read_json(root / DATASET_NAME))
    if dataset != build_dataset(root):
        raise ValueError("Frozen candidate evidence dataset does not reproduce.")
    rows = cast("list[dict[str, Any]]", dataset["payload"]["rows"])
    judged = [row for row in rows if row["usefulness"] != "UNJUDGED"]
    coverage = {}
    for field in FEATURE_CLASSES:
        present = [row for row in rows if row["features"][field] is not None]
        absent = [row for row in rows if row["features"][field] is None]
        coverage[field] = {
            "present": _states(present),
            "absent": _states(absent),
            "judged_present": len(
                [row for row in present if row["usefulness"] != "UNJUDGED"]
            ),
            "judged_absent": len(
                [row for row in absent if row["usefulness"] != "UNJUDGED"]
            ),
        }
    binary = {}
    for field in BINARY:
        true_rows = [row for row in judged if row["features"][field] is True]
        false_rows = [row for row in judged if row["features"][field] is False]
        binary[field] = {
            "true": _states(true_rows),
            "false": _states(false_rows),
            "phi": _phi(true_rows, false_rows),
        }
    numeric = {
        field: {
            "by_state": _distribution(judged, field),
            "ordering": _within_case_auc(judged, field, direction),
        }
        for field, direction in NUMERIC_DIRECTIONS.items()
    }
    redundancy = {
        "canonical_vs_bm25_plus_membership": _jaccard(
            rows, "canonical_member", "bm25_plus_member"
        ),
        "canonical_vs_rrf_membership": _jaccard(rows, "canonical_member", "rrf_member"),
        "canonical_vs_bm25_plus_rank": _spearman(
            rows, "canonical_rank", "bm25_plus_rank"
        ),
        "canonical_vs_rrf_rank": _spearman(rows, "canonical_rank", "rrf_rank"),
        "support_vs_distinct_seeds": _spearman(
            rows, "structural_support_count", "distinct_seed_count"
        ),
        "support_vs_distinct_relations": _spearman(
            rows, "structural_support_count", "distinct_relation_count"
        ),
        "method_count_by_canonical_membership": {
            str(present): _profile(
                [row for row in rows if row["features"]["canonical_member"] is present]
            )["numeric"]["lexical_method_count"]
            for present in (True, False)
        },
    }
    intersections: dict[str, Callable[[dict[str, Any]], bool]] = {
        "lexical_only": lambda f: (
            f["lexical_method_count"] > 0 and not f["structural_member"]
        ),
        "structural_only": lambda f: (
            f["lexical_method_count"] == 0 and f["structural_member"]
        ),
        "both_lexical_and_structural": lambda f: (
            f["lexical_method_count"] > 0 and f["structural_member"]
        ),
        "outgoing_only_structural": lambda f: (
            f["outgoing_import"] and not f["incoming_import"]
        ),
        "incoming_only_structural": lambda f: (
            f["incoming_import"] and not f["outgoing_import"]
        ),
        "both_import_directions": lambda f: f["both_import_directions"],
        "single_lexical_method": lambda f: f["lexical_method_count"] == 1,
        "multiple_lexical_methods": lambda f: f["lexical_method_count"] >= 2,
    }
    intersection_counts = {
        name: _states([row for row in rows if predicate(row["features"])])
        for name, predicate in intersections.items()
    }
    escapes = [
        row
        for row in rows
        if row["features"]["structural_member"]
        and row["features"]["lexical_method_count"] == 0
    ]
    escape_analysis = {
        "states": _states(escapes),
        "direction_states": {
            name: _states([row for row in escapes if predicate(row["features"])])
            for name, predicate in (
                ("outgoing_only", intersections["outgoing_only_structural"]),
                ("incoming_only", intersections["incoming_only_structural"]),
                ("both", intersections["both_import_directions"]),
            )
        },
        "numeric_by_state": {
            field: _distribution(escapes, field)
            for field in (
                "structural_support_count",
                "distinct_relation_count",
                "distinct_seed_count",
                "best_seed_rank",
                "path_count",
                "window_count",
            )
        },
        "suffix_by_state": {
            state: dict(
                sorted(
                    Counter(
                        row["features"]["resource_suffix"]
                        for row in escapes
                        if row["usefulness"] == state
                    ).items()
                )
            )
            for state in STATES
        },
        "useful_case_count": len(
            {row["case_id"] for row in escapes if row["usefulness"] == "USEFUL"}
        ),
        "useful_identities": [
            {
                "case_id": row["case_id"],
                "address": row["address"],
                "parent_snapshot_sha": row["parent_snapshot_sha"],
            }
            for row in escapes
            if row["usefulness"] == "USEFUL"
        ],
    }
    fusion = cast(
        "dict[str, Any]",
        _read_json(root / "lexical_import_fusion_development_results.json"),
    )
    candidates = cast(
        "dict[str, Any]", _read_json(root / "lexical_import_fusion_candidates.json")
    )
    by_pair = {(row["case_id"], row["address"]): row for row in rows}
    upper_union = {
        (case["case_id"], address)
        for case in candidates["payload"]["cases"]
        for address in set(case["surfaces"]["canonical_top5"])
        | {item["address"] for item in case["ranked_structural_evidence"]}
    }
    canonical = {
        (row["case_id"], row["address"])
        for row in fusion["payload"]["joined_surfaces"]["canonical_top5"]
    }
    selected_fusion = {
        (row["case_id"], row["address"])
        for row in fusion["payload"]["joined_surfaces"]["lexical4_import1"]
    }
    if (
        not upper_union <= set(by_pair)
        or not canonical | selected_fusion <= upper_union
    ):
        raise ValueError("Oracle-gap candidate identity differs from frozen union.")
    omitted_useful = [
        by_pair[key]
        for key in sorted(upper_union - canonical - selected_fusion)
        if by_pair[key]["usefulness"] == "USEFUL"
    ]
    selected_not_useful = [
        by_pair[key]
        for key in sorted(canonical | selected_fusion)
        if by_pair[key]["usefulness"] == "NOT_USEFUL"
    ]
    selected_unjudged = [
        by_pair[key]
        for key in sorted(canonical | selected_fusion)
        if by_pair[key]["usefulness"] == "UNJUDGED"
    ]
    selected_useful = [
        by_pair[key]
        for key in sorted(canonical | selected_fusion)
        if by_pair[key]["usefulness"] == "USEFUL"
    ]
    oracle_gap = {
        "candidate_union_count": len(upper_union),
        "omitted_by_both_useful": _profile(omitted_useful),
        "selected_by_either_not_useful": _profile(selected_not_useful),
        "selected_by_either_unjudged": _profile(selected_unjudged),
        "selected_by_either_useful": _profile(selected_useful),
        "omitted_useful_identities": [
            {"case_id": row["case_id"], "address": row["address"]}
            for row in omitted_useful
        ],
        "oracle_maximum_useful_at_k5": fusion["payload"]["oracle_upper_bound"][
            "maximum_useful_at_k5"
        ],
        "oracle_cases_coverable_at_least_one": fusion["payload"]["oracle_upper_bound"][
            "cases_coverable_at_least_one"
        ],
    }
    payload = {
        "dataset_identity": dataset["content_identity"],
        "dataset_sha256": sha256_file(root / DATASET_NAME),
        "population": _states(rows),
        "binary_population": _states(judged),
        "excluded_without_candidate_evidence": dataset["payload"][
            "excluded_exact_judgments_without_candidate_evidence"
        ],
        "feature_coverage": coverage,
        "univariate_binary": binary,
        "univariate_numeric": numeric,
        "redundancy": redundancy,
        "predeclared_intersections": intersection_counts,
        "lexical_universe_escapes": escape_analysis,
        "oracle_gap": oracle_gap,
        "statistical_model": (
            "not fitted: only 24 development cases, heterogeneous feature "
            "missingness, correlated lexical methods, and judgment-pool "
            "selection bias; descriptive diagnostics answer this gate"
        ),
        "confirmation_executed": False,
        "new_judgments_created": False,
    }
    return {
        "schema": "devtools-i27-candidate-evidence-diagnostic-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }


def write_analysis(root: Path) -> dict[str, Any]:
    """Persist the deterministic descriptive diagnostic."""
    artifact = build_analysis(root)
    path = root / ANALYSIS_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing candidate evidence analysis differs.")
    write_artifact(path=path, payload=artifact)
    return artifact
