# Copyright (c) 2026
# ruff: noqa: INP001, COM812, E501
"""Case-local blind packet validation, deterministic freeze and exact replay."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
DIGESTS = {
    "blind_manifest.json": "d1096ba811f050a74a0232caa34245bc6de7f263494155e97c3e0ebbf147b6e0",
    "blind_resources.json.gz": "cae456fa325a435de599da24a75ed3a3728d568b4bfc613b5b6851537a98c09d",
}
FRAME = {
    "repository_id": "fe2c8984-a021-4342-9e31-404a6cf07707",
    "snapshot_id": "72a021a8a4778ffdc7f37152b5d31efb6a2ea93de82edc8c940ec76be5e641aa",
    "corpus_id": "8843f263c69d0d1b07b1fa343e63c07873827f0c3a842e7a28e50d1c8b65b93b",
}
OBLIGATIONS = (
    "frontier-semantics",
    "assessment-applicability",
    "candidate-integration",
    "witness-boundary",
    "acquisition-contract",
    "grounding-provenance",
    "frame-identity",
    "readiness-integration",
    "orchestration-boundary",
    "package-api",
    "tests",
    "documentation",
    "validation",
)
ANCHORS = (
    "frontier-request",
    "assessment",
    "candidate",
    "generation",
    "grounding",
    "witness",
    "task",
    "readiness",
    "frame",
    "orchestration",
    "package",
)
RESOURCE_COUNT = 523
CELL_COUNT = 6799

LABELS = {"REQUIRED", "HELPFUL_ONLY", "UNNECESSARY", "unresolved"}
FORBIDDEN = {
    "lexical_query",
    "lexical_queries",
    "bm25_settings",
    "role_preference",
    "role_preferences",
    "role_assignment",
    "role_assignments",
    "rank",
    "score",
    "native_rank",
    "native_score",
    "routed_tier",
    "routed_position",
    "grounding_request",
    "grounding_request_identity",
    "locator",
    "grounding_locator",
    "grounding_disposition",
    "grounded_referent",
    "generation_recipe",
    "generation_recipe_identity",
    "generated_target",
    "generated_hypotheses",
    "generated_resources",
    "projection_operator",
    "operator_selections",
    "reference_fanout",
    "import_fanout",
    "import_dependency",
    "result_bound",
    "work_bound",
    "recovery_metadata",
    "recovery_history",
    "effectiveness_comparison",
    "rankings",
    "scores",
    "branch_families",
    "fixed_recipe_structure",
    "branching_recipe_structure",
}


def require(condition: bool, message: str) -> None:  # noqa: FBT001
    """Reject invalid artifacts even when Python optimization is enabled."""
    if not condition:
        raise ValueError(message)


def keys(value: dict, expected: set[str]) -> None:
    """Require an exact schema at each structured boundary."""
    require(isinstance(value, dict) and set(value) == expected, "Schema fields differ")


def reject_forbidden(value: object) -> None:
    """Check structural keys, never ordinary vocabulary in repository text."""
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = re.sub(r"[^a-z0-9]+", "_", key.lower()).strip("_")
            require(normalized not in FORBIDDEN, f"Forbidden field: {key}")
            reject_forbidden(child)
    elif isinstance(value, list):
        for child in value:
            reject_forbidden(child)


def serialize(value: dict) -> bytes:
    """Serialize as canonical sorted UTF-8 JSON with LF and one final newline."""
    return (
        json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + "\n"
    ).encode("utf-8")


def semantic_digest(semantics: str, *values: str) -> str:
    """Replay the archived length-framed native identity convention locally."""
    digest = hashlib.sha256()
    for value in (semantics, *values):
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()


def load_packet(directory: Path = HERE) -> tuple[dict, dict]:
    """Read ONLY the two authorized preexisting Case 0008 inputs."""
    payloads = {}
    for name, digest in DIGESTS.items():
        data = (directory / name).read_bytes()
        require(
            hashlib.sha256(data).hexdigest() == digest, f"Blind digest mismatch: {name}"
        )
        payloads[name] = data
    manifest = json.loads(payloads["blind_manifest.json"])
    archive = json.loads(gzip.decompress(payloads["blind_resources.json.gz"]))
    reject_forbidden(manifest)
    reject_forbidden(archive)
    keys(
        manifest,
        {
            "adjudication_instructions",
            "blind_resources",
            "case_identity",
            "corpus_id",
            "frame_identity",
            "obligations",
            "purpose",
            "repository_id",
            "resource_count",
            "schema",
            "shared_anchors",
            "snapshot_id",
            "task",
            "task_identity",
        },
    )
    keys(
        archive,
        {
            "corpus_id",
            "repository_id",
            "resource_count",
            "resources",
            "schema",
            "snapshot_id",
        },
    )
    require(manifest["schema"] == "case-0008-blind-adjudication-v1", "Manifest schema")
    require(manifest["case_identity"] == "case_0008", "Case identity")
    require(
        manifest["task_identity"] == "case-0008-unresolved-frontier-acquisition",
        "Task identity",
    )
    require(
        manifest["frame_identity"]
        == "frozen-stage-a-repository-snapshot-and-text-corpus",
        "Frame identity",
    )
    require(
        bool(manifest["task"]) and bool(manifest["purpose"]), "Missing task/purpose"
    )
    keys(manifest["blind_resources"], {"archive_name", "sha256"})
    require(
        manifest["blind_resources"]
        == {
            "archive_name": "blind_resources.json.gz",
            "sha256": DIGESTS["blind_resources.json.gz"],
        },
        "Archive declaration",
    )
    keys(manifest["adjudication_instructions"], {"instructions", "task_guidance"})
    for key, expected in FRAME.items():
        require(manifest[key] == archive[key] == expected, f"Identity mismatch: {key}")
    require(
        manifest["resource_count"]
        == archive["resource_count"]
        == len(archive["resources"])
        == RESOURCE_COUNT,
        "Resource count",
    )
    require(
        tuple(o["identity"] for o in manifest["obligations"]) == OBLIGATIONS,
        "Obligation identities/order",
    )
    require(
        tuple(a["identity"] for a in manifest["shared_anchors"]) == ANCHORS,
        "Anchor identities/order",
    )
    for anchor in manifest["shared_anchors"]:
        keys(anchor, {"identity", "task_provenance", "text"})
        require(
            bool(anchor["text"]) and bool(anchor["task_provenance"]), "Empty anchor"
        )
    for obligation in manifest["obligations"]:
        keys(
            obligation,
            {
                "applicability_wording",
                "desired_information_predicate",
                "identity",
                "mandatory_helpful_status",
                "pre_execution_accepted_witness_alternatives",
                "satisfaction_criterion",
                "shared_anchor_references",
                "task_provenance",
            },
        )
        keys(obligation["satisfaction_criterion"], {"name", "statement"})
        require(
            obligation["mandatory_helpful_status"] == "MANDATORY", "Requirement status"
        )
        require(
            not obligation["pre_execution_accepted_witness_alternatives"],
            "Preexisting gold",
        )
        require(
            set(obligation["shared_anchor_references"]) <= set(ANCHORS),
            "Anchor reference",
        )
        require(
            bool(obligation["desired_information_predicate"])
            and bool(obligation["satisfaction_criterion"]["statement"]),
            "Missing predicate/criterion",
        )
        if obligation["identity"] != "package-api":
            require(obligation["applicability_wording"] is None, "Unexpected condition")
        else:
            require(
                obligation["applicability_wording"]
                == "Applicable when the new reusable capability requires public package/API exposure or changes existing package/dependency conventions.",
                "Package condition",
            )
    seen = set()
    for resource in archive["resources"]:
        keys(
            resource, {"address", "content", "content_identity", "occurrence_identity"}
        )
        keys(resource["occurrence_identity"], {"address", "content_identity"})
        require(
            resource["occurrence_identity"]
            == {
                "address": resource["address"],
                "content_identity": resource["content_identity"],
            },
            "Occurrence mismatch",
        )
        require(
            resource["content_identity"]
            == semantic_digest("decoded-utf8-text-sha256-v1", resource["content"]),
            "Content digest mismatch",
        )
        require(resource["address"] not in seen, "Duplicate resource")
        seen.add(resource["address"])
    state_values = [
        value
        for resource in archive["resources"]
        for value in (resource["address"], resource["content_identity"])
    ]
    require(
        semantic_digest(
            "explicit-required-text-resources-sha256-v1",
            archive["repository_id"],
            *state_values,
        )
        == archive["snapshot_id"],
        "Recomputed SnapshotId mismatch",
    )
    require(
        semantic_digest(
            "selected-observed-utf8-resource-occurrences-sha256-v1",
            archive["repository_id"],
            *state_values,
        )
        == archive["corpus_id"],
        "Recomputed CorpusId mismatch",
    )
    return manifest, archive


def resource_key(resource: dict) -> tuple[str, str]:
    """Use exact addressed content identity for coverage."""
    keys(resource, {"address", "content_identity"})
    return resource["address"], resource["content_identity"]


def validate(gold: dict, manifest: dict, archive: dict) -> None:  # noqa: C901, PLR0912, PLR0915
    """Validate all Stage C schema, references, witnesses and frame cells."""
    reject_forbidden(gold)
    keys(
        gold,
        {
            "schema",
            "case_identity",
            "task_identity",
            "exact_task",
            "repository_id",
            "snapshot_id",
            "corpus_id",
            "blind_digests",
            "method",
            "obligations",
            "information_units",
            "resource_judgments",
            "task_gaps",
            "task_gap_review",
            "packet_limitations",
            "blindness_attestation",
        },
    )
    require(gold["schema"] == "case-0008-stage-c-judgments-v1", "Gold schema")
    for key in ["case_identity", "task_identity", *FRAME]:
        require(gold[key] == manifest[key], f"Gold identity: {key}")
    require(gold["exact_task"] == manifest["task"], "Exact task changed")
    require(gold["blind_digests"] == DIGESTS, "Gold digests")
    keys(
        gold["method"],
        {
            "evidence_universe",
            "inspection",
            "necessity",
            "resource_rule",
            "alternatives",
            "inferability",
        },
    )
    require(all(gold["method"].values()), "Method missing")
    attestation = gold["blindness_attestation"]
    keys(
        attestation,
        {
            "blind_manifest_accessed",
            "blind_resources_accessed",
            "other_preexisting_case_artifacts_accessed",
            "lexical_experiment_accessed",
            "role_experiment_accessed",
            "grounding_experiment_accessed",
            "generation_experiment_accessed",
            "reference_experiment_accessed",
            "import_experiment_accessed",
            "recovery_history_accessed",
            "current_task_relevant_source_accessed",
            "stage_d_performed",
            "effectiveness_analysis_performed",
            "confirmation_accessed",
        },
    )
    for key, value in attestation.items():
        require(
            value is (key in {"blind_manifest_accessed", "blind_resources_accessed"}),
            "Blindness attestation violated",
        )
    resources = {
        resource_key(r["occurrence_identity"]): r for r in archive["resources"]
    }
    units = {}
    for unit in gold["information_units"]:
        keys(unit, {"identity", "resource", "spans", "information"})
        require(
            unit["identity"] not in units and bool(unit["identity"]),
            "Duplicate/empty unit",
        )
        key = resource_key(unit["resource"])
        require(
            key in resources and bool(unit["information"]) and bool(unit["spans"]),
            "Unit target/information",
        )
        lines = resources[key]["content"].splitlines()
        previous = 0
        for span in unit["spans"]:
            keys(span, {"start_line", "end_line", "excerpt"})
            start, end = span["start_line"], span["end_line"]
            require(
                type(start) is int
                and type(end) is int
                and previous < start <= end <= len(lines),
                "Invalid span",
            )
            require(
                span["excerpt"] == "\n".join(lines[start - 1 : end]), "Excerpt mismatch"
            )
            previous = end
        units[unit["identity"]] = unit
    require(len(gold["obligations"]) == len(OBLIGATIONS), "Obligation count")
    required_by_obligation = {}
    used = set()
    for obligation, frozen in zip(
        gold["obligations"], manifest["obligations"], strict=True
    ):
        keys(
            obligation,
            {
                "frozen_obligation",
                "applicability",
                "applicability_rationale",
                "unit_judgments",
                "acceptable_alternatives",
            },
        )
        require(obligation["frozen_obligation"] == frozen, "Frozen obligation changed")
        require(
            obligation["applicability"]
            in {"APPLICABLE", "SUPPORTED_NOT_APPLICABLE", "UNRESOLVED_APPLICABILITY"},
            "Applicability value",
        )
        require(
            bool(obligation["applicability_rationale"]),
            "Applicability evidence/rationale missing",
        )
        selected = set()
        judged = set()
        for judgment in obligation["unit_judgments"]:
            keys(
                judgment,
                {
                    "unit",
                    "judgment",
                    "rationale",
                    "inferability",
                    "discovery",
                    "manual_review",
                },
            )
            require(
                judgment["unit"] in units and judgment["unit"] not in judged,
                "Unit judgment target/duplicate",
            )
            require(
                judgment["judgment"] in LABELS and bool(judgment["rationale"]),
                "Unit judgment",
            )
            judged.add(judgment["unit"])
            if judgment["judgment"] == "REQUIRED":
                selected.add(judgment["unit"])
                require(
                    judgment["inferability"]
                    in {"INFERABLE_AT_START", "INHERENT_DISCOVERY"},
                    "Inferability",
                )
                if judgment["inferability"] == "INFERABLE_AT_START":
                    require(judgment["discovery"] is None, "Spurious discovery")
                else:
                    keys(
                        judgment["discovery"],
                        {"later_observation", "prerequisite", "why_not_static"},
                    )
                    require(
                        all(judgment["discovery"].values()),
                        "Discovery prerequisites missing",
                    )
                review = judgment["manual_review"]
                keys(
                    review,
                    {
                        "obligation",
                        "information",
                        "necessity",
                        "granularity",
                        "relationship",
                        "task_start",
                        "blind_basis",
                    },
                )
                require(
                    review["obligation"] == frozen["identity"] and all(review.values()),
                    "Manual review incomplete",
                )
        alternatives = obligation["acceptable_alternatives"]
        require(
            bool(alternatives) == (obligation["applicability"] == "APPLICABLE"),
            "Applicable alternatives missing or inappropriate",
        )
        alternative_sets = set()
        alternative_ids = set()
        members = set()
        for alternative in alternatives:
            keys(alternative, {"identity", "all_units", "rationale"})
            a = alternative["all_units"]
            require(
                bool(a) and len(set(a)) == len(a) and set(a) <= selected,
                "Alternative members",
            )
            require(
                alternative["identity"] not in alternative_ids
                and bool(alternative["rationale"]),
                "Alternative identity/rationale",
            )
            group = frozenset(a)
            require(
                group not in alternative_sets
                and not any(
                    group > other or other > group for other in alternative_sets
                ),
                "Duplicate/dominated alternative",
            )
            alternative_sets.add(group)
            alternative_ids.add(alternative["identity"])
            members.update(a)
        require(members == selected, "Required unit absent from alternatives")
        required_by_obligation[frozen["identity"]] = selected
        used.update(selected)
    require(used == set(units), "Unused information unit")
    expected = {(key, obligation) for key in resources for obligation in OBLIGATIONS}
    observed = []
    for cell in gold["resource_judgments"]:
        keys(
            cell, {"resource", "obligation", "judgment", "required_units", "rationale"}
        )
        key = resource_key(cell["resource"])
        require(
            key in resources and cell["obligation"] in OBLIGATIONS,
            "Unexpected cell identity",
        )
        require(cell["judgment"] in LABELS and bool(cell["rationale"]), "Cell judgment")
        wanted = {
            u
            for u in required_by_obligation[cell["obligation"]]
            if resource_key(units[u]["resource"]) == key
        }
        require(
            set(cell["required_units"]) == wanted
            and len(set(cell["required_units"])) == len(cell["required_units"]),
            "Cell required units mismatch",
        )
        require((cell["judgment"] == "REQUIRED") == bool(wanted), "Cell label mismatch")
        observed.append((key, cell["obligation"]))
    require(
        len(expected) == len(observed) == len(set(observed)) == CELL_COUNT
        and set(observed) == expected,
        "6799-cell coverage mismatch",
    )
    require(
        bool(gold["task_gap_review"]) and bool(gold["packet_limitations"]),
        "Review/limitations missing",
    )
    gap_ids = set()
    for gap in gold["task_gaps"]:
        keys(
            gap,
            {
                "identity",
                "requirement",
                "task_evidence",
                "why_mandatory",
                "inferability",
                "discovery",
            },
        )
        require(
            gap["identity"] not in gap_ids and gap["identity"] not in OBLIGATIONS,
            "Gap identity",
        )
        gap_ids.add(gap["identity"])
        require(
            bool(gap["task_evidence"]) and gap["task_evidence"] in manifest["task"],
            "Gap task evidence",
        )
        require(
            bool(gap["requirement"]) and bool(gap["why_mandatory"]), "Gap explanation"
        )
        require(
            gap["inferability"] in {"INFERABLE_AT_START", "INHERENT_DISCOVERY"},
            "Gap inferability",
        )
        if gap["inferability"] == "INHERENT_DISCOVERY":
            keys(
                gap["discovery"],
                {"later_observation", "prerequisite", "why_not_static"},
            )
            require(all(gap["discovery"].values()), "Gap discovery missing")
        else:
            require(gap["discovery"] is None, "Gap spurious discovery")


def statistics(gold: dict) -> dict:
    """Compute only properties of the independently adjudicated gold."""
    units = {
        u["identity"]: resource_key(u["resource"]) for u in gold["information_units"]
    }
    combinations = list(
        itertools.product(*(o["acceptable_alternatives"] for o in gold["obligations"]))
    )
    sizes = [
        len({units[u] for alternative in combination for u in alternative["all_units"]})
        for combination in combinations
    ]
    required = [
        j
        for o in gold["obligations"]
        for j in o["unit_judgments"]
        if j["judgment"] == "REQUIRED"
    ]
    return {
        "applicability": {
            o["frozen_obligation"]["identity"]: o["applicability"]
            for o in gold["obligations"]
        },
        "required_units_by_obligation": {
            o["frozen_obligation"]["identity"]: len(o["unit_judgments"])
            for o in gold["obligations"]
        },
        "distinct_required_units": len(units),
        "distinct_required_inferable_at_start": len(
            {j["unit"] for j in required if j["inferability"] == "INFERABLE_AT_START"}
        ),
        "obligation_relative_required_units": len(required),
        "unique_required_resources": len(set(units.values())),
        "cell_labels": dict(Counter(c["judgment"] for c in gold["resource_judgments"])),
        "unresolved_cells": sum(
            c["judgment"] == "unresolved" for c in gold["resource_judgments"]
        ),
        "helpful_cells_by_obligation": dict(
            Counter(
                c["obligation"]
                for c in gold["resource_judgments"]
                if c["judgment"] == "HELPFUL_ONLY"
            )
        ),
        "alternatives_by_obligation": {
            o["frozen_obligation"]["identity"]: len(o["acceptable_alternatives"])
            for o in gold["obligations"]
        },
        "alternative_count": sum(
            len(o["acceptable_alternatives"]) for o in gold["obligations"]
        ),
        "alternative_combination_count": len(combinations),
        "minimum_sufficient_unique_resource_union": min(sizes),
        "maximum_sufficient_unique_resource_union": max(sizes),
        "minimum_combination_count": sizes.count(min(sizes)),
        "required_inferable_at_start": sum(
            j["inferability"] == "INFERABLE_AT_START" for j in required
        ),
        "inherent_discovery": sum(
            j["inferability"] == "INHERENT_DISCOVERY" for j in required
        ),
        "coverage": {
            "expected_resources": 523,
            "observed_resources": 523,
            "expected_cells": 6799,
            "observed_cells": len(gold["resource_judgments"]),
            "duplicate_expected": 0,
            "duplicate_observed": 0,
            "missing": 0,
            "unexpected": 0,
        },
    }


def freeze(gold: dict, destination: Path = HERE / "judgments.json") -> str:
    """Validate and create frozen bytes exclusively; refuse either existing file."""
    manifest, archive = load_packet()
    validate(gold, manifest, archive)
    data = serialize(gold)
    digest = hashlib.sha256(data).hexdigest()
    seal = destination.with_suffix(".sha256")
    if destination.exists() or seal.exists():
        message = "Refusing to overwrite frozen Stage C judgment or seal"
        raise FileExistsError(message)
    with destination.open("xb") as stream:
        stream.write(data)
    with seal.open("x", encoding="ascii", newline="\n") as stream:
        stream.write(digest + "\n")
    return digest


def replay(destination: Path = HERE / "judgments.json") -> dict:
    """Validate the frozen seal and compare regenerated bytes exactly."""
    from build_judgments import build  # noqa: PLC0415

    manifest, archive = load_packet()
    data = destination.read_bytes()
    digest = destination.with_suffix(".sha256").read_text(encoding="ascii").strip()
    require(hashlib.sha256(data).hexdigest() == digest, "Frozen seal mismatch")
    gold = json.loads(data)
    validate(gold, manifest, archive)
    require(
        data == serialize(gold) == serialize(build()), "Deterministic replay mismatch"
    )
    return statistics(gold)


def main() -> None:
    """Expose only Case-local freeze and replay, with no unblinding command."""
    from build_judgments import build  # noqa: PLC0415

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("freeze", "replay"))
    args = parser.parse_args()
    if args.action == "freeze":
        print(freeze(build()))  # noqa: T201
    else:
        print(json.dumps(replay(), sort_keys=True, indent=2))  # noqa: T201


if __name__ == "__main__":
    main()
