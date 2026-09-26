# Copyright (c) 2026
# ruff: noqa: C901, COM812, E501, EM101, PLR2004, TRY003
"""Join frozen window-unit labels to saved development candidate evidence."""

from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING, Any, cast

from experiments.increment_25.development import write_artifact
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.window_judgments import (
    BLINDED_SHA256,
    LABELS,
    validate_blinded_input,
    validate_frozen_judgments,
)
from experiments.increment_27.window_pool import candidate_surface
from experiments.increment_27.window_unit import _digest

if TYPE_CHECKING:
    from pathlib import Path

POOL_SHA256 = "bcde38a9865fe4085858b4a4494e7b0e15e9f3a83cf0f2c5a17a6740c30fb12f"
RANKINGS_SHA256 = "8b499f47de88a0b31ac30f2bf083fbe3c86ee8cfac2bde515dea66163eba0e26"
JUDGMENT_SHA256 = "34f61fd00fde71a76b290cb48797e43c62bc0a53edc6051a9589d4b6d2b58e08"
JUDGMENT_IDENTITY = "ec4bdbb83c2c9bea2b87e513ee87b5a5a8ead769d4d161364c5c599ba254c01d"
SURFACES = ("whole", "window", "overlap", "whole_only", "window_only")


def load_verified_sources(root: Path) -> dict[str, Any]:
    """Check every saved source before joining a frozen outcome to origin."""
    pairs, freeze, ranking = candidate_surface(root)
    if (
        sha256_file(root / "window_unit_pool.json") != POOL_SHA256
        or sha256_file(root / "window_resource_rankings.json") != RANKINGS_SHA256
        or sha256_file(root / "window_unit_blinded_judgment_input.json")
        != BLINDED_SHA256
    ):
        raise ValueError("Committed retrieval-unit source artifact changed.")
    pool = cast("dict[str, Any]", _read_json(root / "window_unit_pool.json"))
    if (
        pool["content_identity"]
        != _digest(
            {key: value for key, value in pool.items() if key != "content_identity"}
        )
        or pool["pairs"] != pairs
        or pool["window_freeze_identity"] != freeze["content_identity"]
        or pool["window_rankings_identity"] != ranking["content_identity"]
        or pool["window_rankings_sha256"] != RANKINGS_SHA256
        or pool["counts"] != {"pooled": 150, "reused": 138, "new": 12}
    ):
        raise ValueError("Frozen pool identity, source binding, or population changed.")
    blind = validate_blinded_input(root / "window_unit_blinded_judgment_input.json")
    if blind["pool_identity"] != pool["content_identity"]:
        raise ValueError("Neutral input does not bind to the frozen candidate pool.")
    judgment = cast(
        "dict[str, Any]", _read_json(root / "window_unit_frozen_judgments.json")
    )
    validate_frozen_judgments(blind, judgment)
    if (
        sha256_file(root / "window_unit_frozen_judgments.json") != JUDGMENT_SHA256
        or judgment["content_identity"] != JUDGMENT_IDENTITY
    ):
        raise ValueError("Frozen blind judgment checkpoint changed.")
    if len(ranking["cases"]) != 24 or set(
        cast("dict[str, Any]", freeze["payload"])["heldout_case_ids_sealed"]
    ) & {row["case_id"] for row in pairs}:
        raise ValueError("Sealed cases entered development evidence.")
    return {
        "pairs": pairs,
        "freeze": freeze,
        "ranking": ranking,
        "pool": pool,
        "blind": blind,
        "judgment": judgment,
        "judgment_sha256": sha256_file(root / "window_unit_frozen_judgments.json"),
    }


def join_frozen_labels(sources: dict[str, Any]) -> list[dict[str, Any]]:
    """Map 138 exact reused and 12 neutral new labels to 150 saved pairs."""
    pairs = sources["pairs"]
    pool = sources["pool"]
    blind = sources["blind"]
    frozen = sources["judgment"]
    by_key = {(row["case_id"], row["address"]): row for row in pairs}
    if len(by_key) != 150:
        raise ValueError("Candidate identities repeat.")
    labels: dict[tuple[str, str], tuple[str, str]] = {}
    for row in pool["reused"]:
        key = row["case_id"], row["address"]
        pair = by_key.get(key)
        if (
            pair is None
            or row["information_need"] != pair["information_need"]
            or row["parent_snapshot_sha"] != pair["parent_snapshot_sha"]
            or row["judgment"] not in LABELS
            or key in labels
        ):
            raise ValueError("Reused judgment lacks exact candidate identity.")
        labels[key] = row["judgment"], "REUSED"
    neutral_cases = {case["neutral_case_id"]: case for case in blind["cases"]}
    if len(neutral_cases) != len(blind["cases"]):
        raise ValueError("Neutral case identities repeat.")
    new_by_identity = {
        (
            row["information_need"]["purpose"],
            row["information_need"]["lexical_query"],
            row["parent_snapshot_sha"],
            row["address"],
        ): row
        for row in pool["new_pairs"]
    }
    if len(new_by_identity) != 12:
        raise ValueError("New-pair identities repeat.")
    neutral_ids = {
        (case["neutral_case_id"], resource["neutral_resource_id"], resource["address"])
        for case in blind["cases"]
        for resource in case["resources"]
    }
    if len(neutral_ids) != 12:
        raise ValueError("Neutral resource identities repeat.")
    new_keys: set[tuple[str, str]] = set()
    for row in frozen["payload"]["judgments"]:
        neutral_key = row["case_id"], row["resource_id"], row["address"]
        if neutral_key not in neutral_ids:
            raise ValueError("Frozen outcome does not match a neutral input resource.")
        case = neutral_cases[row["case_id"]]
        identity = (
            case["information_need"]["purpose"],
            case["information_need"]["lexical_query"],
            case["parent_snapshot_sha"],
            row["address"],
        )
        new_pair = new_by_identity.get(identity)
        if new_pair is None:
            raise ValueError("Neutral judgment has no exact frozen new-pair identity.")
        key = new_pair["case_id"], row["address"]
        if key in labels or key in new_keys:
            raise ValueError("Frozen new judgment duplicates another label.")
        new_keys.add(key)
        labels[key] = row["judgment"], "NEW"
    if len(labels) != 150 or len(new_keys) != 12 or set(labels) != set(by_key):
        raise ValueError("Judgment join does not cover the exact 150-pair pool.")
    return [
        {
            **pair,
            "judgment": labels[(pair["case_id"], pair["address"])][0],
            "judgment_provenance": labels[(pair["case_id"], pair["address"])][1],
        }
        for pair in pairs
    ]


def _surface(row: dict[str, Any], name: str) -> bool:
    whole = row["whole_top5_rank"] is not None
    window = row["window_top5_rank"] is not None
    return {
        "whole": whole,
        "window": window,
        "overlap": whole and window,
        "whole_only": whole and not window,
        "window_only": window and not whole,
    }[name]


def _counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    labels = Counter(row["judgment"] for row in rows)
    return {
        "total": len(rows),
        "USEFUL": labels["USEFUL"],
        "NOT_USEFUL": labels["NOT_USEFUL"],
        "UNJUDGED": labels["UNJUDGED"],
    }


def build_results(root: Path) -> dict[str, Any]:
    """Compute descriptive development-only arm accounting from frozen sources."""
    sources = load_verified_sources(root)
    rows = join_frozen_labels(sources)
    surfaces = {
        name: _counts([row for row in rows if _surface(row, name)]) for name in SURFACES
    }
    if (
        surfaces["whole"]["total"] != 120
        or surfaces["window"]["total"] != 120
        or surfaces["overlap"]["total"] != 90
        or surfaces["whole_only"]["total"] != 30
        or surfaces["window_only"]["total"] != 30
    ):
        raise ValueError("Frozen top-five candidate surface changed.")
    case_ids = cast("dict[str, Any]", sources["freeze"]["payload"])[
        "development_case_ids"
    ]
    per_case: list[dict[str, Any]] = []
    for case_id in case_ids:
        case_rows = [row for row in rows if row["case_id"] == case_id]
        counts = {
            name: _counts([row for row in case_rows if _surface(row, name)])
            for name in SURFACES
        }
        whole_useful = counts["whole"]["USEFUL"]
        window_useful = counts["window"]["USEFUL"]
        per_case.append(
            {
                "case_id": case_id,
                "surfaces": counts,
                "useful_difference_window_minus_whole": window_useful - whole_useful,
                "case_useful_coverage": {
                    "whole": whole_useful > 0,
                    "window": window_useful > 0,
                },
            }
        )
    if len(per_case) != 24 or _counts(rows)["total"] != 150:
        raise ValueError("Development result population changed.")
    window_only = [row for row in rows if _surface(row, "window_only")]
    no_positive_whole_rank = [
        row for row in window_only if row["whole_positive_rank"] is None
    ]
    useful_window_only = [row for row in window_only if row["judgment"] == "USEFUL"]
    payload = {
        "window_freeze_identity": sources["freeze"]["content_identity"],
        "window_rankings_identity": sources["ranking"]["content_identity"],
        "window_rankings_sha256": RANKINGS_SHA256,
        "pool_identity": sources["pool"]["content_identity"],
        "pool_sha256": POOL_SHA256,
        "blinded_input_identity": sources["blind"]["content_identity"],
        "blinded_input_sha256": BLINDED_SHA256,
        "frozen_judgment_identity": sources["judgment"]["content_identity"],
        "frozen_judgment_sha256": sources["judgment_sha256"],
        "development_case_count": 24,
        "heldout_executed": False,
        "pairs": rows,
        "union": _counts(rows),
        "surfaces": surfaces,
        "per_case": per_case,
        "reachability": {
            "window_only_no_positive_whole_rank": len(no_positive_whole_rank),
            "useful_window_only_no_positive_whole_rank": sum(
                row["judgment"] == "USEFUL" for row in no_positive_whole_rank
            ),
            "useful_window_only_whole_positive_ranks": [
                row["whole_positive_rank"] for row in useful_window_only
            ],
            "all_window_only_whole_positive_ranks": [
                row["whole_positive_rank"] for row in window_only
            ],
        },
        "interpretation_boundary": "24 historical development cases; purpose-relative three-state labels; equal top-five resource capacity; no sealed confirmation, production promotion, or statistical generalization",
    }
    return {
        "schema": "devtools-i27-window-unit-development-results-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }


def write_results(root: Path) -> dict[str, Any]:
    """Persist an immutable deterministic post-freeze result artifact."""
    result = build_results(root)
    path = root / "window_unit_development_results.json"
    if path.exists() and _read_json(path) != result:
        raise ValueError("Existing retrieval-unit result differs from frozen evidence.")
    write_artifact(path=path, payload=result)
    return result
