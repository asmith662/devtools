# Copyright (c) 2026
# ruff: noqa: C901, E501, EM101, PLR2004, TRY003
"""Mechanical development join for the frozen mirrored-test-path baseline."""

from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING, Any

from experiments.increment_25.development import write_artifact
from experiments.increment_26.development_judgments import USEFULNESS_SEMANTICS
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_30.mechanics import _verified_json
from experiments.increment_31.judgments import OUTPUT_NAME as JUDGMENTS_NAME
from experiments.increment_31.judgments import STATES, build_judgments
from experiments.increment_31.mechanics import (
    CANDIDATES_NAME,
    FREEZE_NAME,
    ROOT,
    build_freeze,
)
from experiments.increment_31.population import (
    BLINDED_NAME,
    JUDGMENT_FREEZE_NAME,
    build_population,
)
from experiments.retrieval_judgment_coverage import (
    judgment_identity,
    validate_frozen_judgment_coverage,
    validate_neutral_target_coverage,
    validated_outcome_mappings,
)

if TYPE_CHECKING:
    from pathlib import Path

RESULT_NAME = "mirrored_test_paths_development_results.json"
SOURCE_NAMES = (
    FREEZE_NAME,
    CANDIDATES_NAME,
    JUDGMENT_FREEZE_NAME,
    BLINDED_NAME,
    JUDGMENTS_NAME,
)
EXPECTED_IDENTITIES = {
    FREEZE_NAME: "e05fd19e2ccba9c62a08e68d73cdf833614813b86812ed2119b2c441849a1a53",
    CANDIDATES_NAME: "7c4e6d924ab5a12477746629a74470dba82281a55e22b950b2126980701113d7",
    JUDGMENT_FREEZE_NAME: "4125ed95d7750565e8ff001250e5fbcbf62f32baa5512325d03ceab297164ce6",
    BLINDED_NAME: "64fb7e675d6d7d0b28e72af7ef5adb1a7bc20bfc384cf21dc5a781c1a5eb85d8",
    JUDGMENTS_NAME: "1e603bdaa614b58474f7796e7c80ad732fa806a9bb9ae0ec95475c243aff0799",
}


def _counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(row["judgment"] for row in rows)
    return {
        "candidate_pairs": len(rows),
        **{state: counts[state] for state in STATES},
        "judged_total": counts["USEFUL"] + counts["NOT_USEFUL"],
    }


def build_results(root: Path = ROOT) -> dict[str, Any]:
    """Join only exact frozen pairs after neutral judgments self-verify."""
    sources = {name: _verified_json(root / name) for name in SOURCE_NAMES}
    if {
        name: source["content_identity"] for name, source in sources.items()
    } != EXPECTED_IDENTITIES:
        raise ValueError("A frozen Increment-31 artifact identity changed.")
    protocol, mechanics = sources[FREEZE_NAME], sources[CANDIDATES_NAME]
    population, blind = sources[JUDGMENT_FREEZE_NAME]["payload"], sources[BLINDED_NAME]
    judgments = sources[JUDGMENTS_NAME]["payload"]
    if (
        protocol != build_freeze(root)
        or mechanics["freeze_identity"] != protocol["content_identity"]
        or mechanics["judgments_loaded"]
        or mechanics["heldout_executed"]
        or population["candidate_freeze_identity"] != protocol["content_identity"]
        or population["candidate_identity"] != mechanics["content_identity"]
        or population["candidate_sha256"] != sha256_file(root / CANDIDATES_NAME)
        or population["blinded_input_identity"] != blind["content_identity"]
        or (sources[JUDGMENT_FREEZE_NAME], blind) != build_population(root)
        or sources[JUDGMENTS_NAME] != build_judgments(root)
        or judgments["blinded_input_content_identity"] != blind["content_identity"]
        or judgments["blinded_input_sha256"] != sha256_file(root / BLINDED_NAME)
        or judgments["usefulness_semantics"] != USEFULNESS_SEMANTICS
        or population["usefulness_semantics"] != USEFULNESS_SEMANTICS
        or set(judgments["three_states"]) != set(STATES)
        or set(population["three_states"]) != set(STATES)
    ):
        raise ValueError("Frozen candidate and judgment bindings differ.")
    for name, expected_sha in population["prior_judgment_source_sha256"].items():
        if sha256_file(root.parent / name) != expected_sha:
            raise ValueError("An exact prior judgment source changed after freeze.")
    allowed = protocol["payload"]["development_case_ids"]
    if (
        len(allowed) != 24
        or [case["case_id"] for case in mechanics["cases"]] != allowed
        or set(allowed) & set(protocol["payload"]["heldout_case_ids_sealed"])
    ):
        raise ValueError("Joined cases differ from frozen development population.")
    frozen_new = validate_neutral_target_coverage(population["new_judgment_pairs"])
    blind_targets = {
        (str(case["neutral_case_id"]), str(resource["neutral_resource_id"]))
        for case in blind["payload"]["cases"]
        for resource in case["resources"]
    }
    if (
        len(frozen_new) != 12
        or set(frozen_new) != blind_targets
        or judgments["target_count"] != 12
    ):
        raise ValueError("Neutral targets differ from exact frozen population.")
    new_by_identity = validate_frozen_judgment_coverage(
        population["new_judgment_pairs"],
        judgments["records"],
        STATES,
        blind_targets,
    )
    reused, new_by_identity = validated_outcome_mappings(
        population["reused_judgments"],
        new_by_identity,
    )
    if len(new_by_identity) != 12 or len(reused) != 22:
        raise ValueError("New/reused judgment populations overlap or are incomplete.")
    joined: list[dict[str, Any]] = []
    for case in mechanics["cases"]:
        for candidate in case["candidates"]:
            identity = {
                "case_id": case["case_id"],
                "information_need": case["information_need"],
                "parent_snapshot_sha": case["parent_snapshot_sha"],
                "address": candidate["address"],
                "usefulness_semantics": USEFULNESS_SEMANTICS,
            }
            key = judgment_identity(identity)
            previous, fresh = reused.get(key), new_by_identity.get(key)
            if (previous is None) == (fresh is None):
                raise ValueError("Candidate has zero or multiple exact judgments.")
            record = previous if previous is not None else fresh
            if record is None:
                raise ValueError("Candidate lacks a frozen judgment.")
            joined.append(
                {
                    **identity,
                    "judgment": record["judgment"],
                    "judgment_origin": "exact-reuse"
                    if previous is not None
                    else "new-blinded",
                    "judgment_source": previous["source"]
                    if previous is not None
                    else JUDGMENTS_NAME,
                    "directions": candidate["directions"],
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
                    "existing_containment_candidate": candidate[
                        "existing_containment_candidate"
                    ],
                    "absent_existing_evidence_union": candidate[
                        "absent_existing_evidence_union"
                    ],
                    "support_count": candidate["support_count"],
                },
            )
    if (
        len(joined) != 34
        or len({judgment_identity(row) for row in joined}) != 34
        or any(
            candidate["canonical_top_five"]
            for case in mechanics["cases"]
            for candidate in case["candidates"]
        )
    ):
        raise ValueError(
            "Joined result differs from complete 34-pair candidate surface.",
        )
    surfaces = {
        "union": joined,
        "source_to_test": [
            row for row in joined if "source_to_test" in row["directions"]
        ],
        "test_to_source": [
            row for row in joined if "test_to_source" in row["directions"]
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
        "containment_escape": [
            row for row in joined if not row["existing_containment_candidate"]
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
    payload = {
        "schema": "devtools-i31-mirrored-test-path-development-results-v1",
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
        "surface_counts": {name: _counts(rows) for name, rows in surfaces.items()},
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
                "containment_escape",
                "complete_existing_evidence_escape",
            )
        },
        "per_case": [
            {
                "case_id": case["case_id"],
                **_counts([row for row in joined if row["case_id"] == case["case_id"]]),
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
    """Persist the exact completed development join."""
    result = build_results(root)
    path = root / RESULT_NAME
    if path.exists() and _read_json(path) != result:
        raise ValueError("Existing Increment-31 development result differs.")
    write_artifact(path=path, payload=result)
    return result


if __name__ == "__main__":
    write_results()
