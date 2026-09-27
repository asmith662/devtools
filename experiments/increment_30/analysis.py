# Copyright (c) 2026
# ruff: noqa: C901, COM812, EM101, PLR2004, TRY003
"""Mechanical development join for frozen package-containment judgments."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any, cast

from experiments.increment_25.development import write_artifact
from experiments.increment_26.development_judgments import USEFULNESS_SEMANTICS
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_30.judgments import OUTPUT_NAME as JUDGMENTS_NAME
from experiments.increment_30.judgments import STATES
from experiments.increment_30.mechanics import CANDIDATES_NAME, FREEZE_NAME
from experiments.increment_30.population import BLINDED_NAME, JUDGMENT_FREEZE_NAME
from experiments.retrieval_judgment_coverage import (
    judgment_identity,
    validate_frozen_judgment_coverage,
    validate_neutral_target_coverage,
    validated_outcome_mappings,
)

ROOT = Path(__file__).resolve().parent
RESULT_NAME = "package_containment_development_results.json"


def _verified_sources(root: Path) -> dict[str, dict[str, Any]]:
    names = (
        FREEZE_NAME,
        CANDIDATES_NAME,
        JUDGMENT_FREEZE_NAME,
        BLINDED_NAME,
        JUDGMENTS_NAME,
    )
    sources = {}
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
            raise ValueError("An Increment-30 source artifact cannot self-verify.")
        sources[name] = artifact
    return sources


def _states(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(row["judgment"] for row in rows)
    return {
        "candidate_pairs": len(rows),
        **{state: counts[state] for state in STATES},
        "judged_total": counts["USEFUL"] + counts["NOT_USEFUL"],
    }


def build_results(root: Path = ROOT) -> dict[str, Any]:
    """Join only exact frozen pair identities, preserving three-state outcomes."""
    sources = _verified_sources(root)
    protocol = sources[FREEZE_NAME]
    mechanics = sources[CANDIDATES_NAME]
    population = sources[JUDGMENT_FREEZE_NAME]["payload"]
    blind = sources[BLINDED_NAME]
    judgments = sources[JUDGMENTS_NAME]["payload"]
    counts = Counter(row["judgment"] for row in judgments["records"])
    if (
        mechanics["freeze_identity"] != protocol["content_identity"]
        or population["candidate_freeze_identity"] != protocol["content_identity"]
        or population["candidate_identity"] != mechanics["content_identity"]
        or population["candidate_sha256"] != sha256_file(root / CANDIDATES_NAME)
        or population["blinded_input_identity"] != blind["content_identity"]
        or judgments["blinded_input_content_identity"] != blind["content_identity"]
        or judgments["blinded_input_sha256"] != sha256_file(root / BLINDED_NAME)
        or judgments["target_count"] != 20
        or judgments["state_counts"] != {state: counts[state] for state in STATES}
        or judgments["usefulness_semantics"] != USEFULNESS_SEMANTICS
        or set(judgments["three_states"]) != set(STATES)
        or population["usefulness_semantics"] != USEFULNESS_SEMANTICS
        or set(population["three_states"]) != set(STATES)
        or mechanics["judgments_loaded"]
        or mechanics["heldout_executed"]
    ):
        raise ValueError("Frozen containment candidate/judgment bindings differ.")
    for name, expected_sha in population["prior_judgment_source_sha256"].items():
        if sha256_file(root.parent / name) != expected_sha:
            raise ValueError("An exact prior judgment source changed after freeze.")
    allowed = protocol["payload"]["development_case_ids"]
    if (
        len(allowed) != 24
        or [case["case_id"] for case in mechanics["cases"]] != allowed
        or set(allowed) & set(protocol["payload"]["heldout_case_ids_sealed"])
    ):
        raise ValueError("Joined cases differ from frozen development.")
    frozen_new = validate_neutral_target_coverage(population["new_judgment_pairs"])
    blind_targets = {
        (str(case["neutral_case_id"]), str(resource["neutral_resource_id"]))
        for case in blind["payload"]["cases"]
        for resource in case["resources"]
    }
    if len(frozen_new) != 20 or set(frozen_new) != blind_targets:
        raise ValueError("New judgment freeze differs from exact blind targets.")
    newly_judged = validate_frozen_judgment_coverage(
        population["new_judgment_pairs"], judgments["records"], STATES, blind_targets
    )
    reused, newly_judged = validated_outcome_mappings(
        population["reused_judgments"], newly_judged
    )
    if len(reused) != 29 or len(newly_judged) != len(frozen_new):
        raise ValueError("Reused and new exact judgment populations differ.")
    joined = []
    for case in mechanics["cases"]:
        for candidate in case["candidates"]:
            identity = {
                "case_id": case["case_id"],
                "information_need": case["information_need"],
                "parent_snapshot_sha": case["parent_snapshot_sha"],
                "address": candidate["address"],
                "usefulness_semantics": USEFULNESS_SEMANTICS,
            }
            pair_key = judgment_identity(identity)
            prior, fresh = reused.get(pair_key), newly_judged.get(pair_key)
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
                    "canonical_positive_rank": candidate["canonical_positive_rank"],
                    "saved_positive_method_ranks": candidate[
                        "saved_positive_method_ranks"
                    ],
                    "absent_all_saved_positive_lexical": candidate[
                        "absent_all_saved_positive_lexical"
                    ],
                    "existing_import_candidate": candidate["existing_import_candidate"],
                    "existing_references_calls_candidate": candidate[
                        "existing_references_calls_candidate"
                    ],
                    "absent_existing_evidence_union": candidate[
                        "absent_existing_evidence_union"
                    ],
                    "support_count": candidate["support_count"],
                }
            )
    if (
        len(joined) != mechanics["summary"]["candidate_pairs"]
        or len({judgment_identity(row) for row in joined}) != len(joined)
        or len(joined) != len(reused) + len(newly_judged)
    ):
        raise ValueError("Joined result does not cover exact frozen candidate pairs.")
    surfaces = {
        "union": joined,
        "child_to_package": [
            row for row in joined if "child_to_package" in row["directions"]
        ],
        "package_to_child": [
            row for row in joined if "package_to_child" in row["directions"]
        ],
        "canonical_top_five_escape": joined,
        "all_saved_lexical_escape": [
            row for row in joined if row["absent_all_saved_positive_lexical"]
        ],
        "import_escape": [
            row for row in joined if not row["existing_import_candidate"]
        ],
        "references_calls_escape": [
            row for row in joined if not row["existing_references_calls_candidate"]
        ],
        "complete_existing_evidence_escape": [
            row for row in joined if row["absent_existing_evidence_union"]
        ],
        "exact_reuse": [
            row for row in joined if row["judgment_origin"] == "exact-reuse"
        ],
        "new_blinded": [
            row for row in joined if row["judgment_origin"] == "new-blinded"
        ],
    }
    if any(
        candidate["canonical_top_five"]
        for case in mechanics["cases"]
        for candidate in case["candidates"]
    ):
        raise ValueError("A canonical top-five seed reappeared as a candidate.")
    payload = {
        "schema": "devtools-i30-package-containment-development-results-v1",
        "source_content_identities": {
            name: source["content_identity"] for name, source in sources.items()
        },
        "source_sha256": {name: sha256_file(root / name) for name in sources},
        "development_case_ids": allowed,
        "heldout_case_ids_sealed": protocol["payload"]["heldout_case_ids_sealed"],
        "confirmation_executed": False,
        "candidate_mechanics_changed": False,
        "usefulness_semantics": USEFULNESS_SEMANTICS,
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
                "references_calls_escape",
                "complete_existing_evidence_escape",
            )
        },
        "per_case": [
            {
                "case_id": case["case_id"],
                **_states([row for row in joined if row["case_id"] == case["case_id"]]),
            }
            for case in mechanics["cases"]
        ],
        "cost_summary": mechanics["summary"],
    }
    return {
        "schema": payload["schema"],
        "content_identity": _digest(payload),
        "payload": payload,
    }


def write_results(root: Path = ROOT) -> dict[str, Any]:
    """Persist the exact development result after all neutral judgments froze."""
    artifact = build_results(root)
    path = root / RESULT_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing Increment-30 development result differs.")
    write_artifact(path=path, payload=artifact)
    return artifact
