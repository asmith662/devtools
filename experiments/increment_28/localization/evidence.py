# Copyright (c) 2026
# ruff: noqa: C901, E501, EM101, PLR2004, TRY003
"""Outcome-blind paired location control over fixed outgoing import supports."""

from __future__ import annotations

import ast
from collections import Counter
from typing import TYPE_CHECKING, Any, cast

from experiments.increment_25.development import write_artifact
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_28.import_use import (
    EVIDENCE_NAME as IMPORT_USE_EVIDENCE,
)
from experiments.increment_28.import_use import (
    FREEZE_NAME as IMPORT_USE_FREEZE,
)
from experiments.increment_28.import_use import (
    ROOT27,
    _qualified_read,
    _verified_seed_source,
)
from experiments.increment_28.import_use import (
    build_freeze as build_import_use_freeze,
)

if TYPE_CHECKING:
    from pathlib import Path

ROOT28 = ROOT27.parent / "increment_28"
FREEZE_NAME = "localization_freeze.json"
EVIDENCE_NAME = "localization_evidence.json"
STATES = (
    "IN_WINDOW_ONLY",
    "BOTH",
    "OUTSIDE_WINDOW_ONLY",
    "NO_QUALIFYING_OCCURRENCE",
    "INDETERMINATE",
)


def build_freeze(root: Path = ROOT28) -> dict[str, Any]:
    """Bind the fixed I28 evidence, source semantics, and location rules."""
    previous_freeze = cast("dict[str, Any]", _read_json(root / IMPORT_USE_FREEZE))
    previous = cast("dict[str, Any]", _read_json(root / IMPORT_USE_EVIDENCE))
    if previous_freeze != build_import_use_freeze(root.parent / "increment_27") or previous["freeze_identity"] != previous_freeze["content_identity"]:
        raise ValueError("Increment 28 pre-outcome evidence differs from its freeze.")
    cases = cast("list[dict[str, Any]]", previous["cases"])
    ids = [case["case_id"] for case in cases]
    if ids != previous_freeze["payload"]["development_case_ids"] or len(ids) != 24 or len(set(ids)) != 24 or set(ids) & set(previous_freeze["payload"]["heldout_case_ids_sealed"]):
        raise ValueError("Localization population differs from frozen development.")
    if previous["summary"]["fixed_union_pairs"] != 109 or previous["summary"]["outgoing"]["candidate_pairs"] != 99 or previous["summary"]["outgoing"]["support_count"] != 499:
        raise ValueError("Localization requires the exact fixed structural surface.")
    payload = {
        "development_case_ids": ids,
        "heldout_case_ids_sealed": previous_freeze["payload"]["heldout_case_ids_sealed"],
        "candidate_identity": previous_freeze["payload"]["candidate_identity"],
        "window_identity": previous_freeze["payload"]["window_identity"],
        "import_use_freeze_identity": previous_freeze["content_identity"],
        "import_use_evidence_identity": previous["content_identity"],
        "source_sha256": {
            IMPORT_USE_FREEZE: sha256_file(root / IMPORT_USE_FREEZE),
            IMPORT_USE_EVIDENCE: sha256_file(root / IMPORT_USE_EVIDENCE),
            "increment_27/window_resource_rankings.json": sha256_file(root.parent / "increment_27" / "window_resource_rankings.json"),
        },
        "population": {"development_cases": 24, "structural_union_pairs": 109, "outgoing_pairs": 99, "outgoing_supports": 499},
        "binding_semantics": "Reuse the unchanged Increment-28 _qualified_read source analysis and verify its saved in-window support state and occurrences exactly. The only new variable is location of a qualifying read relative to that same saved winning window.",
        "location": "A qualifying full-source occurrence is inside if its half-open Unicode character span lies wholly within the saved winning window, outside if disjoint, and indeterminate at a partial boundary. The full-source call does not count import declarations. The winning window identity, text, hash and bounds are verified against parent-snapshot source.",
        "support_states": {
            "IN_WINDOW_ONLY": "one or more source-grounded qualifying reads inside and none outside, with no unresolved relevant occurrence",
            "BOTH": "source-grounded qualifying reads inside and outside, regardless of additional unresolved occurrences",
            "OUTSIDE_WINDOW_ONLY": "one or more source-grounded qualifying reads outside, none inside, with no unresolved relevant occurrence",
            "NO_QUALIFYING_OCCURRENCE": "adequately covered full source has no qualifying read",
            "INDETERMINATE": "binding or location uncertainty prevents a defensible only/none classification; positive observed occurrences, if any, remain recorded",
        },
        "candidate_aggregation": "Apply the same five distinctions across all outgoing supports; a candidate BOTH has proven reads at both locations, ONLY requires no indeterminate support, and NO requires every support to have no qualifying occurrence. Preserve each support and candidate provenance. Primary judged comparison is strict inside (IN_WINDOW_ONLY or BOTH) versus strict OUTSIDE_WINDOW_ONLY.",
        "new_candidates": 0,
        "new_judgments": 0,
        "outcome_join_before_checkpoint": False,
    }
    return {"schema": "devtools-i28-localization-freeze-v1", "content_identity": _digest(payload), "payload": payload}


def freeze(root: Path = ROOT28) -> dict[str, Any]:
    """Persist location rules before any new source derivation."""
    artifact = build_freeze(root)
    path = root / FREEZE_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing localization freeze differs.")
    write_artifact(path=path, payload=artifact)
    return artifact


def _position(occurrence: dict[str, Any], window: dict[str, Any]) -> str:
    start, end = cast("list[int]", occurrence["char_span"])
    lo, hi = int(window["char_start"]), int(window["char_end"])
    if lo <= start and end <= hi:
        return "inside"
    if end <= lo or start >= hi:
        return "outside"
    return "partial-boundary"


def classify_localization(full: dict[str, Any], window: dict[str, Any]) -> dict[str, Any]:
    """Locate only already-qualified reads and preserve unknowns separately."""
    positives = full["occurrences"] if full["state"] == "SUPPORTED" else []
    uncertain = (
        full.get("uncertain_occurrences", [])
        if full["state"] == "SUPPORTED"
        else full["occurrences"]
        if full["state"] == "INDETERMINATE"
        else []
    )
    placed = [{**item, "location": _position(item, window)} for item in positives]
    inside = [item for item in placed if item["location"] == "inside"]
    outside = [item for item in placed if item["location"] == "outside"]
    partial = [item for item in placed if item["location"] == "partial-boundary"]
    unresolved = full["state"] == "INDETERMINATE" or bool(uncertain or partial)
    state = (
        "BOTH" if inside and outside else
        "INDETERMINATE" if unresolved else
        "IN_WINDOW_ONLY" if inside else
        "OUTSIDE_WINDOW_ONLY" if outside else
        "NO_QUALIFYING_OCCURRENCE"
    )
    return {
        "state": state,
        "full_source_state": full["state"],
        "full_source_reason": full["reason"],
        "local_binding": full.get("local_binding"),
        "inside_occurrences": inside,
        "outside_occurrences": outside,
        "partial_boundary_occurrences": partial,
        "uncertain_occurrences": uncertain,
        "known_inside": bool(inside),
        "known_outside": bool(outside),
        "unresolved": unresolved,
    }


def _candidate_state(supports: list[dict[str, Any]]) -> str:
    inside = any(row["known_inside"] for row in supports)
    outside = any(row["known_outside"] for row in supports)
    unresolved = any(row["unresolved"] for row in supports)
    if inside and outside:
        return "BOTH"
    if unresolved:
        return "INDETERMINATE"
    if inside:
        return "IN_WINDOW_ONLY"
    if outside:
        return "OUTSIDE_WINDOW_ONLY"
    return "NO_QUALIFYING_OCCURRENCE"


def derive_evidence(*, repository_root: Path, root: Path = ROOT28) -> dict[str, Any]:
    """Locate all fixed outgoing support reads without opening outcomes."""
    frozen = cast("dict[str, Any]", _read_json(root / FREEZE_NAME))
    if frozen != build_freeze(root):
        raise ValueError("Localization rules must be frozen first.")
    previous = cast("dict[str, Any]", _read_json(root / IMPORT_USE_EVIDENCE))
    windows = cast("dict[str, Any]", _read_json(root.parent / "increment_27" / "window_resource_rankings.json"))
    window_cases = {row["case_id"]: row for row in windows["cases"]}
    result_cases: list[dict[str, Any]] = []
    for case in previous["cases"]:
        case_id = case["case_id"]
        ranked = {row["address"]: row["winning_window"] for row in window_cases[case_id]["positive_resource_ordering"]}
        sources: dict[str, tuple[str, Any]] = {}
        for candidate in case["outgoing"]:
            for support in candidate["supports"]:
                address = support["seed_address"]
                if address not in sources:
                    window = ranked.get(address)
                    if window is None or window["identity"] != support["window_identity"] or [window["char_start"], window["char_end"]] != support["window_char_span"]:
                        raise ValueError("Saved support window differs from winning window.")
                    sources[address] = _verified_seed_source(repository_root, case["parent_snapshot_sha"], address, window)
        candidates: list[dict[str, Any]] = []
        for candidate in case["outgoing"]:
            supports: list[dict[str, Any]] = []
            for prior in candidate["supports"]:
                address = prior["seed_address"]
                content, tree = sources[address]
                window = ranked[address]
                # The requested module may be relative/dotted; the direct AST
                # declaration text is recovered from the exact saved ordinal.
                direct = [node for node in tree.body if isinstance(node, ast.Import | ast.ImportFrom)]
                ordinal = prior["declaration_ordinal"]
                aliases = [(node, alias) for node in direct for alias in node.names]
                if ordinal >= len(aliases):
                    raise ValueError("Saved direct import ordinal is absent.")
                node, alias = aliases[ordinal]
                declaration = {
                    "module_text": alias.name if isinstance(node, ast.Import) else node.module,
                    "imported_name": prior["imported_name"],
                    "local_alias": prior["local_alias"],
                    "requested_module": prior["imported_module"],
                }
                path = {"declaration_ordinal": ordinal, "import_source_span": prior["import_source_span"]}
                inside = _qualified_read(content=content, tree=tree, resolution=declaration, path=path, window=window)
                if any(prior.get(key) != value for key, value in inside.items()):
                    raise ValueError("Frozen Increment 28 in-window binding evidence changed.")
                full = _qualified_read(content=content, tree=tree, resolution=declaration, path=path, window={"char_start": 0, "char_end": len(content)})
                located = classify_localization(full, window)
                supports.append({
                    "case_id": case_id,
                    "parent_snapshot_sha": case["parent_snapshot_sha"],
                    "candidate_address": candidate["address"],
                    "seed_address": address,
                    "seed_canonical_rank": prior["seed_canonical_rank"],
                    "window_identity": prior["window_identity"],
                    "window_char_span": prior["window_char_span"],
                    "declaration_derivation_identity": prior["declaration_derivation_identity"],
                    "declaration_ordinal": ordinal,
                    "import_source_span": prior["import_source_span"],
                    "resolution_identity": prior["resolution_identity"],
                    "relation_identity": prior["relation_identity"],
                    "imported_module": prior["imported_module"],
                    "imported_name": prior["imported_name"],
                    "local_alias": prior["local_alias"],
                    **located,
                })
            state_counts = Counter(row["state"] for row in supports)
            candidates.append({
                "case_id": case_id,
                "address": candidate["address"],
                "incoming": candidate["incoming"],
                "absent_all_saved_positive_lexical": candidate["absent_all_saved_positive_lexical"],
                "support_count": candidate["existing_support_count"],
                "distinct_supporting_seeds": candidate["distinct_supporting_seeds"],
                "best_seed_rank": candidate["existing_best_seed_rank"],
                "state_counts": {state: state_counts[state] for state in STATES},
                "state": _candidate_state(supports),
                "any_qualifying_read_anywhere": any(row["known_inside"] or row["known_outside"] for row in supports),
                "any_qualifying_read_inside": any(row["known_inside"] for row in supports),
                "any_qualifying_read_outside": any(row["known_outside"] for row in supports),
                "any_outside_window_only_support": any(row["state"] == "OUTSIDE_WINDOW_ONLY" for row in supports),
                "strict_outside_only": _candidate_state(supports) == "OUTSIDE_WINDOW_ONLY",
                "supports": supports,
            })
        result_cases.append({
            "case_id": case_id, "parent_snapshot_sha": case["parent_snapshot_sha"],
            "outgoing": candidates, "incoming_only_addresses": case["incoming_only_addresses"],
        })
    if len(result_cases) != 24 or sum(len(case["outgoing"]) for case in result_cases) != 99 or sum(len(case["incoming_only_addresses"]) for case in result_cases) != 10:
        raise ValueError("Localization candidate population changed.")
    rows = [row for case in result_cases for row in case["outgoing"]]
    if sum(row["support_count"] for row in rows) != 499:
        raise ValueError("Localization support population changed.")

    def summary(values: list[dict[str, Any]]) -> dict[str, Any]:
        support_states = Counter(support["state"] for row in values for support in row["supports"])
        candidate_states = Counter(row["state"] for row in values)
        return {
            "candidate_pairs": len(values),
            "support_count": sum(row["support_count"] for row in values),
            "support_states": {state: support_states[state] for state in STATES},
            "candidate_states": {state: candidate_states[state] for state in STATES},
            "candidate_any_qualifying_anywhere": sum(row["any_qualifying_read_anywhere"] for row in values),
            "candidate_any_qualifying_inside": sum(row["any_qualifying_read_inside"] for row in values),
            "candidate_strict_outside_only": candidate_states["OUTSIDE_WINDOW_ONLY"],
            "cases_by_state": {
                state: len({row["case_id"] for row in values if row["state"] == state})
                for state in STATES
            },
        }

    hard = [row for row in rows if row["absent_all_saved_positive_lexical"]]
    artifact: dict[str, Any] = {
        "schema": "devtools-i28-localization-evidence-v1",
        "freeze_identity": frozen["content_identity"],
        "import_use_evidence_identity": previous["content_identity"],
        "candidate_identity": frozen["payload"]["candidate_identity"],
        "window_identity": frozen["payload"]["window_identity"],
        "cases": result_cases,
        "summary": {
            "outgoing": summary(rows),
            "outgoing_all_lexical_escape": summary(hard),
            "fixed_union_pairs": 109,
            "incoming_only_pairs": 10,
        },
        "new_candidates": 0,
        "new_judgments": 0,
        "usefulness_outcomes_loaded": False,
        "heldout_executed": False,
    }
    artifact["content_identity"] = _digest(artifact)
    return artifact


def write_evidence(*, repository_root: Path, root: Path = ROOT28) -> dict[str, Any]:
    """Persist deterministic source locations before opening outcomes."""
    artifact = derive_evidence(repository_root=repository_root, root=root)
    path = root / EVIDENCE_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing localization evidence differs.")
    write_artifact(path=path, payload=artifact)
    return artifact
