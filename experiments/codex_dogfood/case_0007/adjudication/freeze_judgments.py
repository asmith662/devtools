# Copyright (c) 2026
# ruff: noqa: INP001, S101, PLR0912, PLR0915, PLR2004, ANN401, PT018, E501, T201
"""Validate and freeze only Case 0007 blind Stage C; import no repository code."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

if not __debug__:
    msg = "Case 0007 validation requires assertions; optimized Python is refused."
    raise RuntimeError(msg)

HERE = Path(__file__).resolve().parent
MANIFEST_SHA = "1367dd6840ed59ec03da3b02588ee896a64cbbe1af7415e61e7962e9a077ecb8"
ARCHIVE_SHA = "b3f435ded07aef88bbb9b374788d8357870d22d6c18853b28e0fa9ce8f6cf855"
REPOSITORY = "fe2c8984-a021-4342-9e31-404a6cf07707"
SNAPSHOT = "404104e498a8d33118b52d5bad41c0ff4a8792d4ae23a2790628b796b91f34fd"
CORPUS = "a2aaec768f650e9d8928fc1ed1a79eb5650472537b1d3538d740480c6a1b1f87"
OBLIGATIONS = (
    "declaration-identity",
    "binding-reexports",
    "module-membership",
    "explicit-exposure",
    "unsupported-behavior",
    "snapshot-provenance",
    "reference-integration",
    "package-api",
    "tests",
    "documentation",
    "validation",
)
ANCHORS = (
    "declarations",
    "bindings",
    "packages",
    "exposure",
    "abstention",
    "provenance",
    "references",
    "api",
    "verification",
)
FORBIDDEN = {
    "lexical_query",
    "query_text",
    "lexical_lane",
    "bm25_settings",
    "native_rank",
    "native_score",
    "rank",
    "score",
    "role_preference",
    "role_assignment",
    "routed_position",
    "routed_tier",
    "grounding_request",
    "locator",
    "grounding_disposition",
    "grounded_referent",
    "generation_family",
    "generation_recipe",
    "projection_operator",
    "branch_identity",
    "generated_target",
    "generated_hypothesis",
    "generated_resource",
    "reference_fanout",
    "result_overflow",
    "work_bound",
    "effectiveness_metric",
}


def canonical(value: Any) -> bytes:
    """Produce fixed UTF-8 JSON bytes without timestamps or platform newlines."""
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")


def sha(value: bytes) -> str:
    """Digest literal bytes."""
    return hashlib.sha256(value).hexdigest()


def semantic_digest(*values: str) -> str:
    """Reproduce the length-framed identities documented in the blind archive."""
    return sha(
        b"".join(len(v.encode()).to_bytes(8, "big") + v.encode() for v in values)
    )


def reject_forbidden(value: Any) -> None:
    """Reject experimental keys, without treating ordinary resource prose as metadata."""
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = key.lower().replace("-", "_").replace(" ", "_")
            assert normalized not in FORBIDDEN, f"Forbidden field: {key}"
            reject_forbidden(child)
    elif isinstance(value, list):
        for child in value:
            reject_forbidden(child)


def packet(directory: Path = HERE) -> tuple[dict[str, Any], list[dict[str, str]]]:
    """Verify exact frozen task/frame and all resource identities using blind bytes."""
    manifest_bytes = (directory / "blind_manifest.json").read_bytes()
    archive_bytes = (directory / "blind_resources.json.gz").read_bytes()
    assert sha(manifest_bytes) == MANIFEST_SHA, "Manifest digest mismatch"
    assert sha(archive_bytes) == ARCHIVE_SHA, "Archive digest mismatch"
    manifest = json.loads(manifest_bytes)
    resources = json.loads(gzip.decompress(archive_bytes))
    reject_forbidden(manifest)
    assert manifest["schema"] == "case-0007-blind-adjudication-v1"
    assert manifest["case_identity"] == "case_0007"
    assert manifest["task_identity"] == "case-0007-python-public-export-ri"
    assert manifest["repository_id"] == REPOSITORY
    assert manifest["snapshot_id"] == SNAPSHOT
    assert manifest["corpus_id"] == CORPUS
    assert manifest["eligible_resource_count"] == len(resources) == 521
    assert tuple(a["identity"] for a in manifest["shared_anchors"]) == ANCHORS
    assert tuple(o["identity"] for o in manifest["obligations"]) == OBLIGATIONS
    for obligation in manifest["obligations"]:
        assert obligation["requirement"] == "mandatory"
        assert obligation["applicability"] is None
        assert obligation["pre_execution_accepted_witness_alternatives"] == []
        assert set(obligation["satisfaction_criterion"]) == {"name", "statement"}
    identities = []
    addresses = []
    for resource in resources:
        assert set(resource) == {
            "resource_occurrence_identity",
            "address",
            "content_identity",
            "content",
        }
        assert all(isinstance(v, str) for v in resource.values())
        address = resource["address"]
        assert address and not address.startswith("/") and "\\" not in address
        assert not any(p in {"", ".", ".."} for p in address.split("/"))
        assert not address.startswith("experiments/codex_dogfood/case_0007/")
        assert (
            semantic_digest("decoded-utf8-text-sha256-v1", resource["content"])
            == resource["content_identity"]
        )
        expected = f"{REPOSITORY}/{SNAPSHOT}/{address}/{resource['content_identity']}"
        assert resource["resource_occurrence_identity"] == expected
        identities.append(expected)
        addresses.append(address)
    assert len(set(identities)) == len(set(addresses)) == 521
    assert addresses == sorted(addresses)
    state = [
        REPOSITORY,
        *(v for r in resources for v in (r["address"], r["content_identity"])),
    ]
    assert (
        semantic_digest("explicit-required-text-resources-sha256-v1", *state)
        == SNAPSHOT
    )
    assert (
        semantic_digest("selected-observed-utf8-resource-occurrences-sha256-v1", *state)
        == CORPUS
    )
    return manifest, resources


def keys(value: dict[str, Any], expected: str) -> None:
    """Use closed schemas to reject unknown fields, including disguised metadata."""
    assert set(value) == set(expected.split()), (
        f"Unexpected schema keys: {set(value) ^ set(expected.split())}"
    )


def statistics(judgments: dict[str, Any]) -> dict[str, Any]:
    """Compute gold-only counts and exact resource unions over complete alternatives."""
    units = {u["unit_id"]: u for u in judgments["information_units"]}
    required = {
        o["identity"]: sorted(
            {u for a in o["acceptable_witness_alternatives"] for u in a["members"]}
        )
        for o in judgments["obligations"]
    }
    choices = [
        o["acceptable_witness_alternatives"]
        for o in judgments["obligations"]
        if o["applicability"] == "APPLICABLE"
    ]
    combinations = list(itertools.product(*choices))
    unions = [
        sorted(
            {
                units[u]["resource_occurrence_identity"]
                for a in combo
                for u in a["members"]
            }
        )
        for combo in combinations
    ]
    smallest = min(unions, key=lambda union: (len(union), union))
    largest = max(unions, key=lambda union: (len(union), union))
    overrides = judgments["resource_classifications"]["overrides"]
    return {
        "required_units_by_obligation": {k: len(v) for k, v in required.items()},
        "distinct_required_units": len(
            {u for values in required.values() for u in values}
        ),
        "obligation_relative_required_units": sum(len(v) for v in required.values()),
        "unique_required_resources": len(
            {
                units[u]["resource_occurrence_identity"]
                for values in required.values()
                for u in values
            }
        ),
        "required_resource_cells": sum(c["judgment"] == "REQUIRED" for c in overrides),
        "helpful_resource_cells": sum(
            c["judgment"] == "HELPFUL_ONLY" for c in overrides
        ),
        "helpful_by_obligation": {
            o: sum(
                c["judgment"] == "HELPFUL_ONLY" and c["obligation"] == o
                for c in overrides
            )
            for o in OBLIGATIONS
        },
        "unresolved_resource_cells": sum(
            c["judgment"] == "unresolved" for c in overrides
        ),
        "inferable_at_start_units": sum(
            u["inferability"] == "INFERABLE_AT_START" for u in units.values()
        ),
        "inherent_discovery_units": sum(
            u["inferability"] == "INHERENT_DISCOVERY" for u in units.values()
        ),
        "alternative_combinations": len(combinations),
        "minimum_sufficient_unique_resource_union": smallest,
        "maximum_sufficient_unique_resource_union": largest,
        "minimum_sufficient_unique_resource_count": len(smallest),
        "maximum_sufficient_unique_resource_count": len(largest),
    }


def validate(  # noqa: C901
    judgments: dict[str, Any], directory: Path = HERE
) -> dict[str, Any]:
    """Check Case-local judgment schema, exact coverage, units, reviews and alternatives."""
    manifest, resources = packet(directory)
    reject_forbidden(judgments)
    keys(
        judgments,
        "schema case_identity task_identity task purpose repository_id snapshot_id corpus_id blind_packet_digests shared_anchors adjudication_method resource_frame obligations information_units resource_classifications task_interpretation_gaps task_gap_review packet_limitations coverage_diagnostics gold_statistics blindness_declaration",
    )
    assert judgments["schema"] == "case-0007-obligation-judgments-v1"
    for field in (
        "case_identity",
        "task_identity",
        "task",
        "purpose",
        "repository_id",
        "snapshot_id",
        "corpus_id",
        "shared_anchors",
    ):
        assert judgments[field] == manifest[field], field
    assert judgments["blind_packet_digests"] == {
        "blind_manifest.json": MANIFEST_SHA,
        "blind_resources.json.gz": ARCHIVE_SHA,
    }
    by_identity = {r["resource_occurrence_identity"]: r for r in resources}
    frame = judgments["resource_frame"]
    for entry in frame:
        keys(entry, "resource_occurrence_identity address content_identity")
    expected_frame = [{k: v for k, v in r.items() if k != "content"} for r in resources]
    assert frame == expected_frame
    assert tuple(o["identity"] for o in judgments["obligations"]) == OBLIGATIONS
    units = {}
    for unit in judgments["information_units"]:
        keys(
            unit,
            "unit_id resource_occurrence_identity address line_spans excerpt_sha256 information smaller_unit_review inferability inherent_discovery manually_reviewed blind_evidence_only",
        )
        assert unit["unit_id"] not in units
        resource = by_identity[unit["resource_occurrence_identity"]]
        assert unit["address"] == resource["address"]
        lines = resource["content"].splitlines()
        previous = 0
        selected = []
        for start, end in unit["line_spans"]:
            assert isinstance(start, int) and isinstance(end, int)
            assert previous < start <= end <= len(lines)
            selected.extend(lines[start - 1 : end])
            previous = end
        assert selected
        assert unit["excerpt_sha256"] == sha(("\n".join(selected) + "\n").encode())
        assert unit["information"] and unit["smaller_unit_review"]
        assert unit["manually_reviewed"] is True and unit["blind_evidence_only"] is True
        assert unit["inferability"] in {"INFERABLE_AT_START", "INHERENT_DISCOVERY"}
        if unit["inferability"] == "INHERENT_DISCOVERY":
            keys(
                unit["inherent_discovery"],
                "later_observation prerequisite why_static_inspection_insufficient",
            )
            assert all(unit["inherent_discovery"].values())
        else:
            assert unit["inherent_discovery"] is None
        units[unit["unit_id"]] = unit
    required_cells = {}
    all_used = set()
    for obligation, frozen in zip(
        judgments["obligations"], manifest["obligations"], strict=True
    ):
        keys(
            obligation,
            "identity desired_information anchors provenance requirement frozen_applicability satisfaction_criterion applicability applicability_rationale applicability_evidence acceptable_witness_alternatives required_unit_reviews",
        )
        for field in (
            "identity",
            "desired_information",
            "anchors",
            "provenance",
            "requirement",
            "satisfaction_criterion",
        ):
            assert obligation[field] == frozen[field]
        assert obligation["frozen_applicability"] == frozen["applicability"]
        assert obligation["applicability"] in {
            "APPLICABLE",
            "SUPPORTED_NOT_APPLICABLE",
            "UNRESOLVED_APPLICABILITY",
        }
        assert (
            obligation["applicability_rationale"]
            and obligation["applicability_evidence"]
        )
        if obligation["applicability"] == "SUPPORTED_NOT_APPLICABLE":
            assert obligation["applicability_evidence"] != ["frozen-task"]
        alternatives = obligation["acceptable_witness_alternatives"]
        if obligation["applicability"] == "APPLICABLE":
            assert alternatives
        used = set()
        signatures = []
        for alternative in alternatives:
            keys(
                alternative,
                "alternative_id members combination_rule complementarity competition resource_identity_alone_suffices",
            )
            assert alternative["combination_rule"] == "ALL"
            members = alternative["members"]
            assert members and len(set(members)) == len(members)
            assert set(members) <= set(units)
            signatures.append(frozenset(members))
            assert alternative["complementarity"] and alternative["competition"]
            assert alternative["resource_identity_alone_suffices"] is False
            used.update(members)
        assert len({a["alternative_id"] for a in alternatives}) == len(alternatives)
        assert len(set(signatures)) == len(signatures)
        assert not any(a < b for a in signatures for b in signatures)
        assert set(obligation["required_unit_reviews"]) == used
        for unit_id, review in obligation["required_unit_reviews"].items():
            keys(
                review,
                "why_required counterfactual structure_review inferability_review",
            )
            assert all(isinstance(v, str) and v for v in review.values())
            cell = (
                units[unit_id]["resource_occurrence_identity"],
                obligation["identity"],
            )
            required_cells.setdefault(cell, set()).add(unit_id)
        all_used.update(used)
    assert all_used == set(units), "Unreferenced required unit"
    classifications = judgments["resource_classifications"]
    keys(classifications, "default default_rationale required_semantics overrides")
    assert classifications["default"] == "UNNECESSARY"
    assert (
        classifications["default_rationale"] and classifications["required_semantics"]
    )
    observed = {}
    for cell in classifications["overrides"]:
        keys(
            cell, "resource_occurrence_identity obligation judgment unit_ids rationale"
        )
        pair = (cell["resource_occurrence_identity"], cell["obligation"])
        assert pair not in observed
        assert pair[0] in by_identity and pair[1] in OBLIGATIONS
        assert cell["judgment"] in {
            "REQUIRED",
            "HELPFUL_ONLY",
            "UNNECESSARY",
            "unresolved",
        }
        assert cell["rationale"]
        if cell["judgment"] == "REQUIRED":
            assert set(cell["unit_ids"]) == required_cells[pair]
        else:
            assert not cell["unit_ids"] and pair not in required_cells
        observed[pair] = cell["judgment"]
    assert {pair for pair, value in observed.items() if value == "REQUIRED"} == set(
        required_cells
    )
    expected_pairs = set(itertools.product(by_identity, OBLIGATIONS))
    expanded = {
        pair: observed.get(pair, classifications["default"]) for pair in expected_pairs
    }
    assert len(expanded) == 5731 and set(expanded) == expected_pairs
    assert judgments["coverage_diagnostics"] == {
        "expected_resources": 521,
        "observed_resources": len(frame),
        "expected_obligations": 11,
        "observed_obligations": 11,
        "expected_cells": 5731,
        "observed_cells": len(expanded),
        "duplicate_expected_identities": 0,
        "duplicate_observed_identities": 0,
        "missing_identities": 0,
        "unexpected_identities": 0,
    }
    gaps = judgments["task_interpretation_gaps"]
    assert len({gap["identity"] for gap in gaps}) == len(gaps)
    for gap in gaps:
        keys(
            gap,
            "identity classification requirement supporting_task_language why_mandatory inferability inherent_discovery",
        )
        assert gap["classification"] == "TASK_INTERPRETATION_GAP"
        assert gap["identity"] and gap["requirement"] and gap["why_mandatory"]
        assert gap["supporting_task_language"] in manifest["task"]
        assert gap["inferability"] in {"INFERABLE_AT_START", "INHERENT_DISCOVERY"}
        if gap["inferability"] == "INHERENT_DISCOVERY":
            keys(
                gap["inherent_discovery"],
                "later_observation prerequisite why_static_inspection_insufficient",
            )
            assert all(gap["inherent_discovery"].values())
        else:
            assert gap["inherent_discovery"] is None
    assert judgments["task_gap_review"]
    assert isinstance(judgments["packet_limitations"], list)
    assert all(
        isinstance(item, str) and item for item in judgments["packet_limitations"]
    )
    keys(
        judgments["adjudication_method"],
        "operations interpretation required_review inspection_record excluded_information",
    )
    assert all(judgments["adjudication_method"].values())
    for item in judgments["adjudication_method"]["inspection_record"]:
        assert item in by_identity
    assert judgments["blindness_declaration"] == {
        "blind_manifest_accessed": True,
        "blind_resources_accessed": True,
        "other_preexisting_case_artifacts_accessed": False,
        "lexical_treatment_or_results_accessed": False,
        "role_treatment_or_results_accessed": False,
        "grounding_treatment_or_results_accessed": False,
        "generation_treatment_or_results_accessed": False,
        "branching_or_reference_treatment_metadata_accessed": False,
        "current_task_relevant_checkout_source_accessed": False,
        "effectiveness_analysis_performed": False,
        "stage_d_performed": False,
        "confirmation_accessed": False,
    }
    calculated = statistics(judgments)
    assert judgments["gold_statistics"] == calculated
    return calculated


def freeze(directory: Path = HERE) -> dict[str, Any]:
    """Freeze canonical judgment bytes exactly once, refusing any existing seal."""
    judgment_path = directory / "judgments.json"
    raw = judgment_path.read_bytes()
    judgments = json.loads(raw)
    validate(judgments, directory)
    assert raw == canonical(judgments), "Judgments are not canonical bytes"
    seal = {
        "schema": "case-0007-stage-c-freeze-v1",
        "judgments_sha256": sha(raw),
        "judgments_bytes": len(raw),
        "blind_packet_digests": judgments["blind_packet_digests"],
    }
    with (directory / "judgments.freeze.json").open("xb") as output:
        output.write(canonical(seal))
    return seal


def replay(directory: Path = HERE) -> dict[str, Any]:
    """Validate frozen bytes and their seal without modifying either file."""
    raw = (directory / "judgments.json").read_bytes()
    judgments = json.loads(raw)
    result = validate(judgments, directory)
    assert raw == canonical(judgments)
    seal_bytes = (directory / "judgments.freeze.json").read_bytes()
    seal = json.loads(seal_bytes)
    assert seal_bytes == canonical(seal)
    assert seal == {
        "schema": "case-0007-stage-c-freeze-v1",
        "judgments_sha256": sha(raw),
        "judgments_bytes": len(raw),
        "blind_packet_digests": judgments["blind_packet_digests"],
    }
    return result


def main() -> None:
    """Expose only packet checks, Stage C freeze and Stage C replay."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["packet", "validate", "freeze", "replay"])
    operation = parser.parse_args().operation
    if operation == "packet":
        manifest, resources = packet()
        print(
            json.dumps(
                {
                    "resources": len(resources),
                    "obligations": len(manifest["obligations"]),
                    "digests": {"manifest": MANIFEST_SHA, "archive": ARCHIVE_SHA},
                    "identities_recomputed": True,
                }
            )
        )
    elif operation == "freeze":
        print(json.dumps(freeze(), sort_keys=True))
    elif operation == "replay":
        print(json.dumps(replay(), sort_keys=True))
    else:
        print(
            json.dumps(
                validate(json.loads((HERE / "judgments.json").read_bytes())),
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
