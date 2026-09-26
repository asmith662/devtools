# Copyright (c) 2026
# ruff: noqa: C901, COM812, EM101, PLR0912, PLR0915, PLR2004, TRY003
"""Freeze one origin-blind development judgment population without labels."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from experiments.increment_25.development import _task_card, write_artifact
from experiments.increment_26.development_judgments import USEFULNESS_SEMANTICS
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.phase1_population import _neutral_id, _resource_contents
from experiments.increment_27.structural_imports.cost import (
    COST_NAME,
    build_cost,
    load_prior_states,
)
from experiments.increment_27.structural_imports.mechanics import (
    DIRECTIONS,
    MECHANICS_NAME,
    METHODS,
    RAW_CANDIDATE_SHA256,
    _digest,
    build_freeze,
    read_candidate_artifact,
)

if TYPE_CHECKING:
    from pathlib import Path

FREEZE_NAME = "structural_import_judgment_freeze.json"
BLIND_NAME = "comparison_blinded_judgment_input.json"


def build_population(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """Derive exact reuse, hidden origin evidence, and neutral parent content."""
    protocol = build_freeze(root)
    mechanics = read_candidate_artifact(root / MECHANICS_NAME)
    cost = _read_json(root / COST_NAME)
    cost_payload = cast("dict[str, Any]", cost["payload"])
    comparison = _read_json(root / "lexical_comparison_rankings.json")
    canonical = _read_json(root / "canonical_positive_lexical_rankings.json")
    source = _read_json(root.parent / "increment_25" / "task_population_freeze.json")
    allowed = cast(
        "list[str]", cast("dict[str, Any]", protocol["payload"])["development_case_ids"]
    )
    heldout = set(
        cast(
            "list[str]",
            cast("dict[str, Any]", protocol["payload"])["heldout_case_ids_sealed"],
        )
    )
    cards_all = {
        str(row["case_id"]): _task_card(row)
        for row in cast(
            "list[dict[str, Any]]",
            cast("dict[str, Any]", source["payload"])["task_cards"],
        )
    }
    cards = {case_id: cards_all[case_id] for case_id in allowed}
    cases = cast("list[dict[str, Any]]", mechanics["cases"])
    ranked = cast("list[dict[str, Any]]", comparison["cases"])
    baselines = cast("list[dict[str, Any]]", canonical["cases"])
    if (
        len(cases) != 24
        or [case["case_id"] for case in cases] != allowed
        or set(allowed) & heldout
        or mechanics["freeze_identity"] != protocol["content_identity"]
        or cost_payload["candidate_identity"] != mechanics["content_identity"]
        or cost_payload["candidate_sha256"] != RAW_CANDIDATE_SHA256
    ):
        raise ValueError("Candidate population or binding differs from its freeze.")
    prior = load_prior_states(root, cards)
    counts = build_cost(mechanics=mechanics, prior=prior, cards=cards)
    if counts != cost_payload["counts"]:
        raise ValueError("Exact reuse differs from the saved cost audit.")

    pair_evidence: list[dict[str, Any]] = []
    reused: list[dict[str, Any]] = []
    new: list[dict[str, Any]] = []
    structural_new: set[tuple[str, str]] = set()
    control_new: set[tuple[str, str]] = set()
    for case, ranks, baseline in zip(cases, ranked, baselines, strict=True):
        case_id = str(case["case_id"])
        card = cards[case_id]
        if (
            ranks["case_id"] != case_id
            or baseline["case_id"] != case_id
            or case["parent_snapshot_sha"] != card.parent_snapshot_sha
            or case["information_need"]
            != {
                "purpose": card.information_need_purpose,
                "lexical_query": card.lexical_query,
            }
        ):
            raise ValueError("Candidate and frozen InformationNeed differ.")
        rank_maps = {
            method: {
                str(row["address"]): int(row["rank"])
                for row in ranks["rankings"][method]
            }
            for method in METHODS
        }
        arms = cast("dict[str, dict[str, Any]]", case["arms"])
        structural: dict[str, dict[str, Any]] = {}
        controls: dict[str, set[str]] = {}
        for direction in DIRECTIONS:
            arm = arms[direction]
            structural[direction] = {}
            controls[direction] = set(arm["same_volume_lexical_control"]["addresses"])
            if (
                len(controls[direction])
                != arm["same_volume_lexical_control"]["actual_count"]
            ):
                raise ValueError("Lexical control contains duplicate addresses.")
            expected_control = [
                row["address"]
                for row in baseline["positive_lexical_ordering"][
                    len(case["seeds"]) : len(case["seeds"]) + arm["candidate_count"]
                ]
            ]
            if arm["same_volume_lexical_control"]["addresses"] != expected_control:
                raise ValueError("Lexical control differs from canonical widening.")
            for row in arm["candidates"]:
                address = str(row["address"])
                if address in structural[direction]:
                    raise ValueError("Duplicate structural candidate within one arm.")
                structural[direction][address] = row
        addresses = sorted(
            set().union(*(set(structural[d]) | controls[d] for d in DIRECTIONS))
        )
        for address in addresses:
            key = (case_id, address)
            identity = {
                "case_id": case_id,
                "information_need": case["information_need"],
                "parent_snapshot_sha": card.parent_snapshot_sha,
                "address": address,
                "usefulness_semantics": USEFULNESS_SEMANTICS,
            }
            method_ranks = {
                method: rank_maps[method].get(address) for method in METHODS
            }
            supports = {
                direction: structural[direction][address]["paths"]
                if address in structural[direction]
                else []
                for direction in DIRECTIONS
            }
            evidence = {
                **identity,
                "outgoing_structural": address in structural["outgoing"],
                "incoming_structural": address in structural["incoming"],
                "structural_supports": supports,
                "outgoing_lexical_control": address in controls["outgoing"],
                "incoming_lexical_control": address in controls["incoming"],
                "saved_positive_method_ranks": method_ranks,
                "canonical_positive_rank": method_ranks["canonical"],
                "absent_all_saved_positive_lexical": all(
                    value is None for value in method_ranks.values()
                ),
            }
            for direction in DIRECTIONS:
                row = structural[direction].get(address)
                if row is not None and (
                    row["saved_positive_method_ranks"] != method_ranks
                    or row["paths"] != supports[direction]
                ):
                    raise ValueError(
                        "Structural evidence differs from saved lexical reachability."
                    )
            pair_evidence.append(evidence)
            previous = prior.get(key)
            if previous is None:
                new.append(identity)
                if any(evidence[f"{direction}_structural"] for direction in DIRECTIONS):
                    structural_new.add(key)
                if any(
                    evidence[f"{direction}_lexical_control"] for direction in DIRECTIONS
                ):
                    control_new.add(key)
            else:
                reused.append(
                    {
                        **identity,
                        "judgment": previous["state"],
                        "source": previous["source"],
                    }
                )
    if (
        len(structural_new) != counts["structural_union"]["new"]
        or len(control_new) != counts["same_volume_control_union"]["new"]
        or len(new) != len(structural_new | control_new)
        or len({(row["case_id"], row["address"]) for row in new}) != len(new)
    ):
        raise ValueError("New judgment population fails exact deduplication.")

    contents = _resource_contents(
        list(dict.fromkeys((row["parent_snapshot_sha"], row["address"]) for row in new))
    )
    blind_cases: list[dict[str, Any]] = []
    for case_id in allowed:
        card = cards[case_id]
        targets = [
            {
                "neutral_resource_id": _neutral_id(
                    "resource",
                    f"{mechanics['content_identity']}|{case_id}|{row['address']}",
                ),
                "address": row["address"],
                "content": contents[(card.parent_snapshot_sha, row["address"])],
            }
            for row in new
            if row["case_id"] == case_id
        ]
        if not targets:
            continue
        targets.sort(key=lambda item: item["neutral_resource_id"])
        blind_cases.append(
            {
                "neutral_case_id": _neutral_id(
                    "case", f"{mechanics['content_identity']}|{case_id}"
                ),
                "information_need": {
                    "purpose": card.information_need_purpose,
                    "lexical_query": card.lexical_query,
                },
                "parent_snapshot_sha": card.parent_snapshot_sha,
                "resources": targets,
            }
        )
    blind_cases.sort(key=lambda item: item["neutral_case_id"])
    blind_payload = {
        "schema": "devtools-i27-neutral-comparison-blinded-input-v1",
        "cases": blind_cases,
    }
    blind = {
        "schema": blind_payload["schema"],
        "content_identity": _digest(blind_payload),
        "payload": blind_payload,
    }
    freeze_payload = {
        "development_case_ids": allowed,
        "heldout_case_ids_sealed": cast("dict[str, Any]", protocol["payload"])[
            "heldout_case_ids_sealed"
        ],
        "suspended_increment_26_confirmation_not_executed": True,
        "candidate_freeze_identity": protocol["content_identity"],
        "candidate_content_identity": mechanics["content_identity"],
        "candidate_raw_sha256": RAW_CANDIDATE_SHA256,
        "candidate_compressed_sha256": sha256_file(root / MECHANICS_NAME),
        "candidate_compression": {
            "format": "gzip",
            "compresslevel": 9,
            "mtime": 0,
            "source": "exact canonical UTF-8 JSON bytes",
        },
        "candidate_cost_identity": cost["content_identity"],
        "candidate_cost_sha256": sha256_file(root / COST_NAME),
        "lexical_control_source_sha256": {
            "canonical_positive_lexical_rankings.json": sha256_file(
                root / "canonical_positive_lexical_rankings.json"
            ),
            "lexical_comparison_rankings.json": sha256_file(
                root / "lexical_comparison_rankings.json"
            ),
        },
        "frozen_judgment_source_sha256": cost_payload["frozen_judgment_source_sha256"],
        "usefulness_semantics": USEFULNESS_SEMANTICS,
        "three_states": ["USEFUL", "NOT_USEFUL", "UNJUDGED"],
        "pair_identity_rule": [
            "InformationNeed purpose",
            "frozen query",
            "parent snapshot",
            "resource address",
            "usefulness semantics",
        ],
        "pair_evidence": pair_evidence,
        "reused_judgments": reused,
        "new_judgment_pairs": new,
        "counts": {
            "structural_total": counts["structural_union"]["total"],
            "structural_reused": counts["structural_union"]["reused"],
            "structural_new": len(structural_new),
            "control_total": counts["same_volume_control_union"]["total"],
            "control_reused": counts["same_volume_control_union"]["reused"],
            "control_new": len(control_new),
            "new_overlap": len(structural_new & control_new),
            "new_deduplicated": len(new),
        },
        "blinded_input_identity": blind["content_identity"],
        "new_usefulness_outcomes": False,
        "heldout_executed": False,
    }
    freeze = {
        "schema": "devtools-i27-structural-import-judgment-freeze-v1",
        "content_identity": _digest(freeze_payload),
        "payload": freeze_payload,
    }
    return freeze, blind


def write_population(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """Persist a complete hidden freeze and its separate neutral human input."""
    freeze, blind = build_population(root)
    for name, artifact in ((FREEZE_NAME, freeze), (BLIND_NAME, blind)):
        path = root / name
        if path.exists() and _read_json(path) != artifact:
            raise ValueError("Existing structural judgment freeze differs.")
        write_artifact(path=path, payload=artifact)
    return freeze, blind
