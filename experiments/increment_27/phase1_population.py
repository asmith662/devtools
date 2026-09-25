# Copyright (c) 2026
# ruff: noqa: C901, E501, EM101, EM102, PLR0912, PLR0915, PLR2004, S607, TRY003
"""Freeze the development-only top-50 canonical lexical judgment population."""

from __future__ import annotations

import hashlib
import subprocess
from typing import TYPE_CHECKING, cast

from experiments.increment_25.development import _task_card, write_artifact
from experiments.increment_26.development_judgments import USEFULNESS_SEMANTICS
from experiments.increment_27.depth_diagnostic import (
    EXPECTED_DEVELOPMENT_SIZE,
    K_CHECKPOINTS,
    _read_json,
    canonical_json_bytes,
    load_existing_judgments,
    prior_judgment_matches,
    sha256_file,
)

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    from experiments.increment_25.task_population import TaskCard


def _digest(value: object) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


PHASE1_SCHEMA = "devtools-increment-27-phase1-pooled-judgment-freeze-v1"
POOL_SCHEMA = "devtools-increment-27-phase1-pooled-pairs-v1"
REUSE_SCHEMA = "devtools-increment-27-phase1-reused-judgments-v1"
BLINDED_SCHEMA = "devtools-increment-27-phase1-blinded-judgment-input-v1"
TOP_K = 50
ALLOWED_STATES = {"useful", "not-useful", "unjudged"}


def _neutral_id(prefix: str, identity: str) -> str:
    return f"{prefix}-{hashlib.sha256(identity.encode('utf-8')).hexdigest()[:16]}"


def _resource_contents(pairs: list[tuple[str, str]]) -> dict[tuple[str, str], str]:
    """Read exact parent blobs in one Git batch, without materializing snapshots."""
    if not pairs:
        return {}
    inputs = "".join(f"{parent}:{address}\n" for parent, address in pairs).encode()
    result = subprocess.run(
        ["git", "cat-file", "--batch"],
        input=inputs,
        capture_output=True,
        check=True,
    )
    output = result.stdout
    offset = 0
    contents: dict[tuple[str, str], str] = {}
    for pair in pairs:
        line_end = output.index(b"\n", offset)
        header = output[offset:line_end].decode("ascii").split()
        if len(header) != 3 or header[1] != "blob":
            raise ValueError(f"Parent snapshot resource is not a blob: {pair[1]}.")
        size = int(header[2])
        start = line_end + 1
        blob = output[start : start + size]
        if len(blob) != size or output[start + size : start + size + 1] != b"\n":
            raise ValueError(
                f"Could not read complete parent snapshot blob: {pair[1]}.",
            )
        contents[pair] = blob.decode("utf-8")
        offset = start + size + 1
    if offset != len(output):
        raise ValueError("Unexpected trailing data from parent snapshot blob read.")
    return contents


def build_phase1_artifacts(*, experiment_root: Path) -> dict[str, dict[str, object]]:
    """Build deterministic pool, reuse map, blinded input, and linked freeze."""
    i27_root = experiment_root / "increment_27"
    source_freeze = _read_json(i27_root / "experiment_freeze.json")
    if source_freeze.get("content_identity") != _digest(source_freeze["payload"]):
        raise ValueError("Increment-27 Phase-0 freeze identity is invalid.")
    phase0_identity = str(source_freeze["content_identity"])
    payload = cast("dict[str, object]", source_freeze["payload"])
    population = cast("dict[str, object]", payload["source_population"])
    frozen_cases = cast("list[dict[str, object]]", population["development_cases"])
    frozen_by_id = {str(item["case_id"]): item for item in frozen_cases}
    heldout = set(
        cast(
            "list[str]",
            cast("dict[str, object]", population["increment_25_source_partition"])[
                "increment_27_heldout_confirmation_case_ids"
            ],
        ),
    )
    if len(frozen_by_id) != EXPECTED_DEVELOPMENT_SIZE or heldout & set(frozen_by_id):
        raise ValueError("Phase-0 case partition is not exactly 24 development cases.")

    ranking_path = i27_root / "canonical_positive_lexical_rankings.json"
    rankings_doc = _read_json(ranking_path)
    if rankings_doc.get("freeze_identity") != phase0_identity:
        raise ValueError("Canonical rankings do not bind to the Phase-0 freeze.")
    agreement = cast("dict[str, object]", rankings_doc["prior_rank_agreement"])
    if agreement.get("status") != "all retained ranks and available scores agree":
        raise ValueError("Saved canonical rankings fail prior-rank agreement.")
    ranked_cases = cast("list[dict[str, object]]", rankings_doc["cases"])
    if {str(item["case_id"]) for item in ranked_cases} != set(frozen_by_id):
        raise ValueError("Ranking cases differ from the frozen development population.")
    if len(ranked_cases) != EXPECTED_DEVELOPMENT_SIZE:
        raise ValueError(
            "Canonical ranking artifact does not contain exactly 24 cases.",
        )

    diagnostic_doc = _read_json(i27_root / "existing_judgment_depth_diagnostics.json")
    if diagnostic_doc.get("freeze_identity") != phase0_identity:
        raise ValueError("Depth diagnostics do not bind to the Phase-0 freeze.")
    summary_doc = _read_json(i27_root / "development_depth_summary.json")
    summary = cast("dict[str, object]", summary_doc["summary"])
    if summary_doc.get("freeze_identity") != phase0_identity or (
        summary.get("total_known_useful_pairs") != 49
        or summary.get("known_useful_reached_by_k")
        != [
            {"k": k, "known_useful_reached": reached, "total_known_useful": 49}
            for k, reached in zip(K_CHECKPOINTS, (2, 9, 16, 35, 41, 42), strict=True)
        ]
        or summary.get("known_useful_unreachable_by_positive_lexical_retrieval") != 5
        or summary.get("known_useful_beyond_50") != 2
    ):
        raise ValueError("Saved depth diagnostic disagrees with the supplied findings.")
    diagnostics = cast("list[dict[str, object]]", diagnostic_doc["cases"])
    if len(diagnostics) != EXPECTED_DEVELOPMENT_SIZE or {
        str(item["case_id"]) for item in diagnostics
    } != set(frozen_by_id):
        raise ValueError("Saved depth diagnostics differ from the 24-case population.")

    task_freeze = _read_json(
        experiment_root / "increment_25" / "task_population_freeze.json",
    )
    task_payload = cast("dict[str, object]", task_freeze["payload"])
    task_cards = cast("list[dict[str, object]]", task_payload["task_cards"])
    cards: dict[str, TaskCard] = {}
    for item in task_cards:
        card = _task_card(item)
        if card.case_id in frozen_by_id:
            cards[card.case_id] = card
    if set(cards) != set(frozen_by_id):
        raise ValueError("Could not reconcile all 24 exact frozen task identities.")
    prior_by_case = load_existing_judgments(
        experiment_root=experiment_root,
        cards=cards,
    )
    prior_index: dict[tuple[str, str], dict[str, object]] = {}
    for case_id, records in prior_by_case.items():
        for record in records:
            address = str(record["address"])
            prior_index[(case_id, address)] = record

    pair_rows: list[dict[str, object]] = []
    reused_rows: list[dict[str, object]] = []
    new_rows: list[dict[str, object]] = []
    case_counts: list[dict[str, object]] = []
    parent_pairs: list[tuple[str, str]] = []
    pairs_seen: set[tuple[str, str]] = set()
    neutral_case_ids: dict[str, str] = {}
    for ranked in ranked_cases:
        case_id = str(ranked["case_id"])
        frozen = frozen_by_id[case_id]
        if (
            ranked["parent_snapshot_sha"] != frozen["parent_snapshot_sha"]
            or ranked["information_need"] != frozen["information_need"]
        ):
            raise ValueError(f"Saved ranking identity differs for {case_id}.")
        parent = str(ranked["parent_snapshot_sha"])
        neutral_case = _neutral_id("case", f"{phase0_identity}|{case_id}")
        neutral_case_ids[case_id] = neutral_case
        ordered = cast("list[dict[str, object]]", ranked["positive_lexical_ordering"])
        count = cast("int", ranked["positive_result_count"])
        if count != len(ordered):
            raise ValueError(f"Incomplete saved positive ranking for {case_id}.")
        selected = ordered[: min(TOP_K, count)]
        if any(
            cast("int", row["rank"]) != index for index, row in enumerate(ordered, 1)
        ):
            raise ValueError(
                f"Saved positive ordering has a rank discontinuity: {case_id}.",
            )
        reused_count = 0
        new_count = 0
        for row in selected:
            address = str(row["address"])
            pair = (case_id, address)
            if pair in pairs_seen:
                raise ValueError(
                    f"Duplicate case/resource pair in saved ranking: {pair}.",
                )
            pairs_seen.add(pair)
            rank = cast("int", row["rank"])
            pair_rows.append({"case_id": case_id, "address": address, "rank": rank})
            parent_pairs.append((parent, address))
            prior = prior_index.get(pair)
            if prior is None:
                new_rows.append({"case_id": case_id, "address": address, "rank": rank})
                new_count += 1
                continue
            if not prior_judgment_matches(
                card=cards[case_id],
                prior_information_need=cast(
                    "Mapping[str, object]",
                    prior["information_need_identity"],
                ),
                prior_parent_snapshot=str(prior["parent_snapshot_sha"]),
                prior_address=address,
                resource_address=address,
                prior_usefulness_semantics=str(prior["judgment_semantics"]),
            ):
                raise ValueError(
                    f"Prior judgment identity mismatch for {case_id}/{address}.",
                )
            judgment = str(prior["judgment"])
            if judgment not in ALLOWED_STATES:
                raise ValueError(f"Unknown usefulness state for {case_id}/{address}.")
            reused_rows.append(
                {
                    "case_id": case_id,
                    "address": address,
                    "judgment": judgment,
                    "judgment_semantics": USEFULNESS_SEMANTICS,
                    "source": prior["source"],
                },
            )
            reused_count += 1
        case_counts.append(
            {
                "case_id": case_id,
                "positive_result_count": count,
                "pooled_pair_count": len(selected),
                "reused_judgment_count": reused_count,
                "new_judgment_count": new_count,
                "lexical_exhaustion_before_50": count < TOP_K,
            },
        )

    if set(neutral_case_ids.values()) & {str(item) for item in heldout}:
        raise ValueError(
            "Neutral development identity unexpectedly overlaps held-out ID.",
        )
    unique_parent_pairs = list(dict.fromkeys(parent_pairs))
    content_by_parent = _resource_contents(unique_parent_pairs)
    ranking_sha = sha256_file(ranking_path)
    prior_judgment_hashes = {
        "increment_25_confirmation_judgments": sha256_file(
            experiment_root / "increment_25" / "confirmation_frozen_judgments.json",
        ),
        "increment_25_neutral_mapping": sha256_file(
            experiment_root / "increment_25" / "confirmation_neutral_mapping.json",
        ),
        "increment_26_development_judgments": sha256_file(
            experiment_root / "increment_26" / "development_frozen_judgments.json",
        ),
    }
    pool_payload: dict[str, object] = {
        "schema": POOL_SCHEMA,
        "phase0_freeze_identity": phase0_identity,
        "canonical_rankings_sha256": ranking_sha,
        "pool_rule": "positive canonical lexical ranks 1 through min(50, positive result count), union by exact (case_id, resource address)",
        "pairs": pair_rows,
        "identity": _digest(pair_rows),
    }
    pool_identity = _digest(pool_payload)
    reuse_payload: dict[str, object] = {
        "schema": REUSE_SCHEMA,
        "phase0_freeze_identity": phase0_identity,
        "pooled_population_identity": pool_identity,
        "source_judgment_artifact_sha256": prior_judgment_hashes,
        "usefulness_semantics": USEFULNESS_SEMANTICS,
        "identity_rule": [
            "exact InformationNeed purpose",
            "exact frozen lexical query",
            "exact parent snapshot identity",
            "exact repository resource address",
            "exact usefulness semantics",
        ],
        "records": reused_rows,
        "identity": _digest(reused_rows),
    }
    reuse_identity = _digest(reuse_payload)

    blind_cases: list[dict[str, object]] = []
    for case_id, frozen in frozen_by_id.items():
        case_new = [item for item in new_rows if item["case_id"] == case_id]
        if not case_new:
            continue
        resources = []
        for item in case_new:
            address = str(item["address"])
            parent = str(frozen["parent_snapshot_sha"])
            resources.append(
                {
                    "neutral_resource_id": _neutral_id(
                        "resource",
                        f"{phase0_identity}|{case_id}|{address}",
                    ),
                    "address": address,
                    "content": content_by_parent[(parent, address)],
                },
            )
        blind_cases.append(
            {
                "neutral_case_id": neutral_case_ids[case_id],
                "information_need": frozen["information_need"],
                "parent_snapshot_sha": frozen["parent_snapshot_sha"],
                "resources": resources,
            },
        )
    blind_payload: dict[str, object] = {
        "schema": BLINDED_SCHEMA,
        "phase0_freeze_identity": phase0_identity,
        "pooled_population_identity": pool_identity,
        "reuse_mapping_identity": reuse_identity,
        "judgment_semantics": USEFULNESS_SEMANTICS,
        "cases": blind_cases,
    }
    blind_identity = _digest(blind_payload)
    freeze_payload: dict[str, object] = {
        "source": "Increment-27 Phase-0 frozen 24-case development rankings",
        "phase0_freeze_identity": phase0_identity,
        "canonical_rankings_sha256": ranking_sha,
        "source_judgment_artifact_sha256": prior_judgment_hashes,
        "canonical_rankings_prior_rank_agreement": agreement,
        "pool_rule": pool_payload["pool_rule"],
        "pooled_population_identity": pool_identity,
        "pooled_pairs": pair_rows,
        "reused_judgment_mapping_identity": reuse_identity,
        "reused_judgments": reused_rows,
        "new_judgment_population_identity": blind_identity,
        "new_judgment_pairs": new_rows,
        "case_counts": case_counts,
        "development_case_count": len(frozen_by_id),
        "heldout_case_count": len(heldout),
        "heldout_execution_or_outcomes_included": False,
        "blinding_contract": [
            "new judgment input exposes only neutral case identity, frozen purpose and lexical query, parent snapshot identity, neutral resource identity/address, and exact parent-snapshot content",
            "new judgment input omits lexical rank and score, retrieval origin, overlap, changed paths, post-change content, retrieval labels, diagnostics, and labels for other resources",
            "reused judgment pairs are excluded from new judgment requests",
        ],
        "usefulness_semantics": {
            "useful": "useful for the frozen InformationNeed purpose",
            "not_useful": "not useful for the frozen InformationNeed purpose",
            "unjudged": "no usefulness outcome; never coerced to not-useful",
        },
        "new_adjudication_performed": False,
        "recall_or_algorithm_comparison_performed": False,
    }
    phase1_freeze = {
        "schema": PHASE1_SCHEMA,
        "content_identity": _digest(freeze_payload),
        "payload": freeze_payload,
    }
    result: dict[str, dict[str, object]] = {
        "phase1_population_freeze.json": cast("dict[str, object]", phase1_freeze),
        "phase1_pooled_pairs.json": pool_payload,
        "phase1_reused_judgments.json": reuse_payload,
        "phase1_blinded_judgment_input.json": blind_payload,
    }
    return result


def write_phase1_artifacts(*, experiment_root: Path) -> dict[str, str]:
    """Write the four deterministic Phase-1 population artifacts."""
    artifacts = build_phase1_artifacts(experiment_root=experiment_root)
    output_root = experiment_root / "increment_27"
    identities: dict[str, str] = {}
    for name, artifact in artifacts.items():
        write_artifact(path=output_root / name, payload=artifact)
        identities[name] = hashlib.sha256(
            (output_root / name).read_bytes(),
        ).hexdigest()
    return identities
