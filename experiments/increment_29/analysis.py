# Copyright (c) 2026
# ruff: noqa: C901, COM812, EM101, PLR0912, PLR2004, TRY003
"""Mechanical development join for the completed reference/call breadth baseline."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any, cast

from experiments.increment_25.development import write_artifact
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_29.judgments import OUTPUT_NAME as JUDGMENTS_NAME
from experiments.increment_29.judgments import SEMANTICS, STATES
from experiments.increment_29.mechanics import CANDIDATES_NAME, FREEZE_NAME
from experiments.increment_29.population import BLINDED_NAME, POPULATION_NAME

ROOT = Path(__file__).resolve().parent
RESULT_NAME = "references_calls_development_results.json"


def _identity(row: dict[str, Any]) -> tuple[str, str, str, str, str]:
    need = row["information_need"]
    return (
        str(need["purpose"]),
        str(need["lexical_query"]),
        str(row["parent_snapshot_sha"]),
        str(row["address"]),
        str(row["usefulness_semantics"]),
    )


def _states(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(row["judgment"] for row in rows)
    return {
        "candidate_pairs": len(rows),
        **{state: counts[state] for state in STATES},
        "judged_total": counts["USEFUL"] + counts["NOT_USEFUL"],
    }


def _verified_sources(root: Path) -> dict[str, dict[str, Any]]:
    names = (
        FREEZE_NAME,
        CANDIDATES_NAME,
        POPULATION_NAME,
        BLINDED_NAME,
        JUDGMENTS_NAME,
    )
    sources: dict[str, dict[str, Any]] = {}
    for name in names:
        artifact = cast("dict[str, Any]", _read_json(root / name))
        hashed = (
            artifact["payload"]
            if "payload" in artifact
            else {
                key: value
                for key, value in artifact.items()
                if key != "content_identity"
            }
        )
        if artifact["content_identity"] != _digest(hashed):
            raise ValueError("An Increment-29 source artifact cannot self-verify.")
        sources[name] = artifact
    return sources


def build_results(root: Path = ROOT) -> dict[str, Any]:
    """Join only exact frozen development pair identities, without relabeling."""
    sources = _verified_sources(root)
    protocol = sources[FREEZE_NAME]
    mechanics = sources[CANDIDATES_NAME]
    population = sources[POPULATION_NAME]["payload"]
    blind = sources[BLINDED_NAME]
    judgments = sources[JUDGMENTS_NAME]["payload"]
    recorded_states = Counter(row["judgment"] for row in judgments["records"])
    if (
        mechanics["freeze_identity"] != protocol["content_identity"]
        or population["candidate_freeze_identity"] != protocol["content_identity"]
        or population["candidate_identity"] != mechanics["content_identity"]
        or population["candidate_sha256"] != sha256_file(root / CANDIDATES_NAME)
        or population["blinded_input_identity"] != blind["content_identity"]
        or judgments["blinded_input_content_identity"] != blind["content_identity"]
        or judgments["blinded_input_sha256"] != sha256_file(root / BLINDED_NAME)
        or judgments["target_count"] != 19
        or judgments["state_counts"]
        != {state: recorded_states[state] for state in STATES}
        or judgments["usefulness_semantics"] != SEMANTICS
        or set(judgments["three_states"]) != set(STATES)
        or mechanics["judgments_loaded"]
        or mechanics["heldout_executed"]
    ):
        raise ValueError("Frozen candidate and blinded judgment bindings differ.")
    for name, expected_sha in population["prior_judgment_source_sha256"].items():
        source = (
            root.parent / name
            if name.startswith("increment_")
            else root.parent / "increment_27" / name
        )
        if sha256_file(source) != expected_sha:
            raise ValueError("An exact reused judgment source changed after freeze.")
    if (
        sha256_file(root.parent / "increment_27" / "comparison_frozen_judgments.json")
        != population["comparison_judgments_sha256"]
    ):
        raise ValueError("The exact comparison judgment source changed after freeze.")
    allowed = protocol["payload"]["development_case_ids"]
    if (
        len(allowed) != 24
        or [case["case_id"] for case in mechanics["cases"]] != allowed
        or {case["case_id"] for case in mechanics["cases"]}
        & set(protocol["payload"]["heldout_case_ids_sealed"])
    ):
        raise ValueError("Development case boundary differs from frozen population.")

    frozen_new = {
        (str(row["neutral_case_id"]), str(row["neutral_resource_id"])): row
        for row in population["new_judgment_pairs"]
    }
    if (
        len(frozen_new) != len(population["new_judgment_pairs"])
        or len(frozen_new) != 19
    ):
        raise ValueError("New judgment population has duplicate target identities.")
    new: dict[tuple[str, str, str, str, str], dict[str, Any]] = {}
    for row in judgments["records"]:
        neutral_key = (str(row["neutral_case_id"]), str(row["neutral_resource_id"]))
        frozen = frozen_new.get(neutral_key)
        if (
            frozen is None
            or _identity(row) != _identity(frozen)
            or row["judgment"] not in STATES
            or not str(row["rationale"]).strip()
            or _identity(row) in new
        ):
            raise ValueError("A frozen neutral judgment has no exact candidate pair.")
        new[_identity(row)] = row
    if len(new) != len(frozen_new) or len(new) != 19:
        raise ValueError("Frozen neutral judgment coverage is incomplete.")
    reused = {_identity(row): row for row in population["reused_judgments"]}
    if len(reused) != len(population["reused_judgments"]) or set(reused) & set(new):
        raise ValueError("Reused and new exact judgments overlap or duplicate.")

    joined: list[dict[str, Any]] = []
    for case in mechanics["cases"]:
        for candidate in case["candidates"]:
            identity = {
                "case_id": case["case_id"],
                "information_need": case["information_need"],
                "parent_snapshot_sha": case["parent_snapshot_sha"],
                "address": candidate["address"],
                "usefulness_semantics": SEMANTICS,
            }
            pair_key = _identity(identity)
            prior, fresh = reused.get(pair_key), new.get(pair_key)
            if (prior is None) == (fresh is None):
                raise ValueError("Candidate pair has zero or multiple exact judgments.")
            judgment = prior if prior is not None else fresh
            if judgment is None:
                raise ValueError("Candidate pair lacks a frozen judgment.")
            joined.append(
                {
                    **identity,
                    "judgment": judgment["judgment"],
                    "judgment_origin": "exact-reuse"
                    if prior is not None
                    else "new-blinded",
                    "judgment_source": prior["source"]
                    if prior is not None
                    else JUDGMENTS_NAME,
                    "directions": candidate["directions"],
                    "reference": candidate["reference"],
                    "direct_call": candidate["direct_call"],
                    "canonical_positive_rank": candidate["canonical_positive_rank"],
                    "saved_positive_method_ranks": candidate[
                        "saved_positive_method_ranks"
                    ],
                    "absent_all_saved_positive_lexical": candidate[
                        "absent_all_saved_positive_lexical"
                    ],
                    "existing_import_candidate": candidate["existing_import_candidate"],
                    "support_count": candidate["support_count"],
                }
            )
    if (
        len(joined) != mechanics["summary"]["candidate_pairs"]
        or len({_identity(row) for row in joined}) != len(joined)
        or len(joined) != len(reused) + len(new)
    ):
        raise ValueError("Joined result does not cover the exact candidate union.")
    surfaces = {
        "union": joined,
        "forward": [row for row in joined if "forward" in row["directions"]],
        "reverse": [row for row in joined if "reverse" in row["directions"]],
        "call_tagged": [row for row in joined if row["direct_call"]],
        "reference_without_call": [row for row in joined if not row["direct_call"]],
        "canonical_rank_six_or_deeper": [
            row
            for row in joined
            if row["canonical_positive_rank"] is not None
            and row["canonical_positive_rank"] > 5
        ],
        "no_positive_canonical_rank": [
            row for row in joined if row["canonical_positive_rank"] is None
        ],
        "all_saved_lexical_escape": [
            row for row in joined if row["absent_all_saved_positive_lexical"]
        ],
        "import_escape": [
            row for row in joined if not row["existing_import_candidate"]
        ],
        "lexical_and_import_escape": [
            row
            for row in joined
            if row["absent_all_saved_positive_lexical"]
            and not row["existing_import_candidate"]
        ],
        "exact_reuse": [
            row for row in joined if row["judgment_origin"] == "exact-reuse"
        ],
        "new_blinded": [
            row for row in joined if row["judgment_origin"] == "new-blinded"
        ],
    }
    per_case = [
        {
            "case_id": case["case_id"],
            **_states([row for row in joined if row["case_id"] == case["case_id"]]),
        }
        for case in mechanics["cases"]
    ]
    payload = {
        "schema": "devtools-i29-references-calls-development-results-v1",
        "source_content_identities": {
            name: source["content_identity"] for name, source in sources.items()
        },
        "source_sha256": {name: sha256_file(root / name) for name in sources},
        "development_case_ids": allowed,
        "heldout_case_ids_sealed": protocol["payload"]["heldout_case_ids_sealed"],
        "confirmation_executed": False,
        "candidate_mechanics_changed": False,
        "usefulness_semantics": SEMANTICS,
        "joined_pairs": joined,
        "surface_counts": {name: _states(rows) for name, rows in surfaces.items()},
        "useful_escape_pairs": {
            name: [
                {"case_id": row["case_id"], "address": row["address"]}
                for row in surfaces[name]
                if row["judgment"] == "USEFUL"
            ]
            for name in (
                "all_saved_lexical_escape",
                "import_escape",
                "lexical_and_import_escape",
            )
        },
        "per_case": per_case,
        "cost_summary": mechanics["summary"],
    }
    return {
        "schema": payload["schema"],
        "content_identity": _digest(payload),
        "payload": payload,
    }


def write_results(root: Path = ROOT) -> dict[str, Any]:
    """Persist the deterministic development result after frozen judgments."""
    artifact = build_results(root)
    path = root / RESULT_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing Increment-29 development result differs.")
    write_artifact(path=path, payload=artifact)
    return artifact
