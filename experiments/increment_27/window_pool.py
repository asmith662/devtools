# Copyright (c) 2026
# ruff: noqa: C901, COM812, EM101, PERF401, PLR0912, PLR0915, PLR2004, TRY003
"""Freeze exact reuse and new neutral labels for the lexical-window ablation."""

from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from pathlib import Path

from experiments.increment_25.development import _task_card, write_artifact
from experiments.increment_26.development_judgments import USEFULNESS_SEMANTICS
from experiments.increment_27.depth_diagnostic import (
    _read_json,
    load_existing_judgments,
    prior_judgment_matches,
    sha256_file,
)
from experiments.increment_27.phase1_population import _resource_contents
from experiments.increment_27.top5_results import join_judgments, load_verified_sources
from experiments.increment_27.window_unit import (
    _digest,
    audit_saved_baseline,
    build_window_freeze,
)

STATES = {"USEFUL", "NOT_USEFUL", "UNJUDGED"}


def _neutral_id(prefix: str, value: str) -> str:
    return f"{prefix}-{hashlib.sha256(value.encode('utf-8')).hexdigest()[:16]}"


def candidate_surface(
    root: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    """Build the 24-case equal-capacity union without loading usefulness labels."""
    freeze = build_window_freeze(root)
    if _read_json(root / "window_unit_freeze.json") != freeze:
        raise ValueError("Window configuration changed after freezing.")
    window = _read_json(root / "window_resource_rankings.json")
    if window.get("freeze_identity") != freeze["content_identity"] or window.get(
        "content_identity"
    ) != _digest(
        {key: value for key, value in window.items() if key != "content_identity"}
    ):
        raise ValueError("Window rankings fail frozen identity checks.")
    baseline, heldout = audit_saved_baseline(root)
    ranked_cases = cast("list[dict[str, Any]]", window["cases"])
    if (
        len(ranked_cases) != 24
        or [row["case_id"] for row in ranked_cases]
        != [row["case_id"] for row in baseline]
        or any(row["case_id"] in heldout for row in ranked_cases)
    ):
        raise ValueError(
            "Window rankings include missing, duplicated, or held-out cases."
        )
    pairs: list[dict[str, Any]] = []
    for original, candidate in zip(baseline, ranked_cases, strict=True):
        if (
            original["parent_snapshot_sha"] != candidate["parent_snapshot_sha"]
            or original["information_need"]["lexical_query"] != candidate["query_text"]
            or original["corpus_resource_count"] != candidate["corpus_resource_count"]
        ):
            raise ValueError("Window case identity differs from the baseline.")
        if {row["address"] for row in original["positive_lexical_ordering"]} != {
            row["address"] for row in candidate["positive_resource_ordering"]
        }:
            raise ValueError(
                "Window representation changed positive resource reachability."
            )
        whole = original["positive_lexical_ordering"][:5]
        windows = candidate["positive_resource_ordering"][:5]
        if (
            len({row["address"] for row in windows}) != len(windows)
            or len(windows) > 5
            or any(row["rank"] != i for i, row in enumerate(windows, 1))
        ):
            raise ValueError(
                "Window resource ordering or top-five capacity is invalid."
            )
        whole_ranks = {row["address"]: row["rank"] for row in whole}
        window_ranks = {row["address"]: row["rank"] for row in windows}
        full_whole = {
            row["address"]: row["rank"] for row in original["positive_lexical_ordering"]
        }
        for address in sorted(whole_ranks.keys() | window_ranks.keys()):
            pairs.append(
                {
                    "case_id": original["case_id"],
                    "information_need": original["information_need"],
                    "parent_snapshot_sha": original["parent_snapshot_sha"],
                    "address": address,
                    "whole_top5_rank": whole_ranks.get(address),
                    "window_top5_rank": window_ranks.get(address),
                    "whole_positive_rank": full_whole.get(address),
                }
            )
    if len({(row["case_id"], row["address"]) for row in pairs}) != len(pairs):
        raise ValueError("Pooled candidate identities repeat.")
    return pairs, freeze, window


def freeze_window_pool(root: Path) -> dict[str, Any]:
    """Freeze reusable labels and only genuinely new neutral judgment targets."""
    pairs, freeze, window = candidate_surface(root)
    population = _read_json(
        root.parent / "increment_25" / "task_population_freeze.json"
    )
    population_payload = cast("dict[str, Any]", population["payload"])
    cards = {
        str(row["case_id"]): _task_card(row) for row in population_payload["task_cards"]
    }
    top5_sources = load_verified_sources(root)
    top5_labels = {
        (row["case_id"], row["address"]): row for row in join_judgments(top5_sources)
    }
    earlier = load_existing_judgments(
        experiment_root=root.parent,
        cards={
            case_id: cards[case_id]
            for case_id in cast(
                "list[str]",
                cast("dict[str, Any]", freeze["payload"])["development_case_ids"],
            )
        },
    )
    prior = {
        (case_id, row["address"]): row
        for case_id, rows in earlier.items()
        for row in rows
    }
    reused: list[dict[str, Any]] = []
    new: list[dict[str, Any]] = []
    for pair in pairs:
        case_id, address = pair["case_id"], pair["address"]
        card = cards[case_id]
        if (
            pair["information_need"]
            != {
                "purpose": card.information_need_purpose,
                "lexical_query": card.lexical_query,
            }
            or pair["parent_snapshot_sha"] != card.parent_snapshot_sha
        ):
            raise ValueError("Candidate pair does not match the frozen task card.")
        key = (case_id, address)
        existing = top5_labels.get(key)
        earlier_label = prior.get(key)
        if earlier_label is not None and not prior_judgment_matches(
            card=card,
            prior_information_need=cast(
                "dict[str, object]", earlier_label["information_need_identity"]
            ),
            prior_parent_snapshot=str(earlier_label["parent_snapshot_sha"]),
            prior_address=str(earlier_label["address"]),
            resource_address=address,
            prior_usefulness_semantics=str(earlier_label["judgment_semantics"]),
        ):
            raise ValueError("Prior judgment identity differs.")
        if existing is not None:
            label = str(existing["judgment"])
            if earlier_label is not None and label != str(
                earlier_label["judgment"]
            ).upper().replace("-", "_"):
                raise ValueError("Earlier and top-five judgments conflict.")
            source = "increment_27_top5"
        elif earlier_label is not None:
            label = str(earlier_label["judgment"]).upper().replace("-", "_")
            source = str(earlier_label["source"])
        else:
            new.append(
                {
                    key: pair[key]
                    for key in (
                        "case_id",
                        "information_need",
                        "parent_snapshot_sha",
                        "address",
                    )
                }
            )
            continue
        if label not in STATES:
            raise ValueError("Prior judgment state is invalid.")
        reused.append(
            {
                **{
                    key: pair[key]
                    for key in (
                        "case_id",
                        "information_need",
                        "parent_snapshot_sha",
                        "address",
                    )
                },
                "judgment": label,
                "judgment_semantics": USEFULNESS_SEMANTICS,
                "source": source,
            }
        )
    if len(reused) + len(new) != len(pairs):
        raise ValueError("Judgment reuse and new targets do not partition the pool.")
    pool = {
        "schema": "devtools-i27-window-unit-pool-v1",
        "window_freeze_identity": freeze["content_identity"],
        "window_rankings_identity": window["content_identity"],
        "window_rankings_sha256": sha256_file(root / "window_resource_rankings.json"),
        "baseline_rankings_sha256": cast("dict[str, Any]", freeze["payload"])[
            "canonical_baseline_sha256"
        ],
        "judgment_semantics": USEFULNESS_SEMANTICS,
        "pairs": pairs,
        "reused": reused,
        "new_pairs": new,
        "counts": {"pooled": len(pairs), "reused": len(reused), "new": len(new)},
        "heldout_executed": False,
        "comparison_performed": False,
    }
    pool["content_identity"] = _digest(pool)
    contents = _resource_contents(
        [(row["parent_snapshot_sha"], row["address"]) for row in new]
    )
    blind_cases: list[dict[str, Any]] = []
    for case_id in cast(
        "list[str]", cast("dict[str, Any]", freeze["payload"])["development_case_ids"]
    ):
        case_rows = [row for row in new if row["case_id"] == case_id]
        if not case_rows:
            continue
        card = cards[case_id]
        neutral_case_id = _neutral_id("case", f"{freeze['content_identity']}|{case_id}")
        resources = [
            {
                "neutral_resource_id": _neutral_id(
                    "resource",
                    f"{freeze['content_identity']}|{case_id}|{row['address']}",
                ),
                "address": row["address"],
                "content": contents[(card.parent_snapshot_sha, row["address"])],
            }
            for row in case_rows
        ]
        resources.sort(key=lambda item: item["neutral_resource_id"])
        blind_cases.append(
            {
                "neutral_case_id": neutral_case_id,
                "information_need": {
                    "purpose": card.information_need_purpose,
                    "lexical_query": card.lexical_query,
                },
                "parent_snapshot_sha": card.parent_snapshot_sha,
                "resources": resources,
            }
        )
    blind_cases.sort(key=lambda item: item["neutral_case_id"])
    blind = {
        "schema": "devtools-i27-window-unit-blinded-input-v1",
        "window_freeze_identity": freeze["content_identity"],
        "pool_identity": pool["content_identity"],
        "judgment_semantics": USEFULNESS_SEMANTICS,
        "cases": blind_cases,
    }
    blind["content_identity"] = _digest(blind)
    if sum(len(case["resources"]) for case in blind_cases) != len(new) or any(
        set(resource) != {"neutral_resource_id", "address", "content"}
        for case in blind_cases
        for resource in case["resources"]
    ):
        raise ValueError("Blinded new-pair population is incomplete or leaks evidence.")
    pool_path = root / "window_unit_pool.json"
    blind_path = root / "window_unit_blinded_judgment_input.json"
    if pool_path.exists() and _read_json(pool_path) != pool:
        raise ValueError("Existing window pool differs from exact source identities.")
    if blind_path.exists() and _read_json(blind_path) != blind:
        raise ValueError(
            "Existing blinded population differs from exact source identities."
        )
    write_artifact(path=pool_path, payload=pool)
    write_artifact(path=blind_path, payload=blind)
    return {"pool": pool, "blind": blind}
