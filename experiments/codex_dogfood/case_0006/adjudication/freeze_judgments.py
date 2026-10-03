"""Case-specific deterministic Stage C freeze; reads no other repository files."""

import argparse
import copy
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path

from author_judgments import authored

ROOT = Path(__file__).resolve().parent
MANIFEST_SHA256 = "8bf0559814df54c246514e56fb7d92937828f9e50f9e17620a2c1acdc2934b49"
ARCHIVE_SHA256 = "a03cdd8dc39d56b4a719be43ca38f2ced8f4df6e0b304ec8187914040b3ebb2a"
CASE = "case_0006"
TASK = "codex-dogfood-case-0006-resolution-recording"
REPOSITORY = "d0e7c9e0-0c4f-4ea7-a345-3eb793ab6eb8"
SNAPSHOT = "ba654221b65584aebdd98804369864162ac3f7da1bf8862abee06ce4d2127a55"
FRAME = "49c69d2db7c6616731d9c24519a48d47a13a2ee991d46aaaf33d1f5d55b212b9"
OBLIGATIONS = (
    "hypothesis-records",
    "member-complementarity",
    "generated-integration",
    "accepted-promotion",
    "assessment-readiness",
    "provenance-frame",
    "package-integration",
    "tests",
    "documentation",
    "validation",
)
FORBIDDEN = {
    "lexical_queries",
    "lexical_query",
    "query_text",
    "query_identity",
    "role_preferences",
    "role_preference",
    "role_assignments",
    "role_assignment",
    "native_rank",
    "bm25_score",
    "score",
    "routed_position",
    "routing_tier",
    "grounding_request",
    "grounding_requests",
    "locator",
    "locator_kind",
    "locator_value",
    "grounding_disposition",
    "grounded_referent",
    "generation_recipe",
    "generation_recipe_identity",
    "projection_operator",
    "generated_hypothesis_identity",
    "generated_target",
    "generated_target_flag",
    "generation_outcome",
    "recovery_metadata",
    "capture_history",
    "recovery_history",
    "effectiveness_comparisons",
    "retrieval_results",
}


def require(condition, message):
    """Fail closed on a violated Case invariant."""
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode()


def reject_fields(value):
    """Inspect structured keys, never blacklist ordinary words in frozen text."""
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = key.lower().replace("-", "_")
            require(normalized not in FORBIDDEN, f"Forbidden structured field: {key}")
            reject_fields(item)
    elif isinstance(value, list):
        for item in value:
            reject_fields(item)


def semantic_digest(*values):
    result = hashlib.sha256()
    for value in values:
        encoded = value.encode()
        result.update(len(encoded).to_bytes(8, "big"))
        result.update(encoded)
    return result.hexdigest()


def load_packet():
    """Verify exact pinned bytes before accepting frozen task/resource metadata."""
    manifest_bytes = (ROOT / "blind_manifest.json").read_bytes()
    archive_bytes = (ROOT / "blind_resources.json.gz").read_bytes()
    require(digest(manifest_bytes) == MANIFEST_SHA256, "Manifest digest mismatch")
    require(digest(archive_bytes) == ARCHIVE_SHA256, "Archive digest mismatch")
    manifest = json.loads(manifest_bytes)
    archive = json.loads(gzip.decompress(archive_bytes))
    reject_fields(manifest)
    reject_fields(archive)
    require(
        set(archive)
        == {
            "schema",
            "case_identity",
            "repository_id",
            "repository_snapshot_id",
            "eligible_frame_identity",
            "resources",
        },
        "Unexpected archive metadata",
    )
    require(manifest["schema"] == "case-0006-blind-adjudication-v1", "Manifest schema")
    require(archive["schema"] == "case-0006-blind-resources-v1", "Archive schema")
    for key, expected in (
        ("case_identity", CASE),
        ("repository_id", REPOSITORY),
        ("repository_snapshot_id", SNAPSHOT),
        ("eligible_frame_identity", FRAME),
    ):
        require(manifest[key] == archive[key] == expected, f"Packet identity: {key}")
    require(manifest["task_identity"] == TASK, "Task identity")
    require(
        manifest["development_task"] and manifest["purpose"], "Task/purpose missing"
    )
    require(manifest["resource_archive"] == "blind_resources.json.gz", "Archive name")
    require(
        manifest["resource_archive_sha256"] == ARCHIVE_SHA256, "Declared archive digest"
    )
    anchors = manifest["shared_anchors"]
    require(
        [a["identity"] for a in anchors]
        == [
            "hypothesis",
            "candidate-view",
            "generation-view",
            "grounding-view",
            "witness-set",
            "supported-witness",
            "assessment",
            "readiness",
            "provenance",
            "quality",
        ],
        "Anchor frame",
    )
    require(
        tuple(o["identity"] for o in manifest["obligations"]) == OBLIGATIONS,
        "Obligation frame",
    )
    for obligation in manifest["obligations"]:
        require(obligation["requirement"] == "mandatory", "Frozen priority changed")
        require(
            obligation["satisfaction_criterion"]["name"]
            and obligation["satisfaction_criterion"]["statement"],
            "Missing criterion",
        )
        require(
            set(obligation["anchor_references"]) <= {a["identity"] for a in anchors},
            "Foreign anchor",
        )
        condition = obligation["applicability_condition"]
        require(
            condition
            == (
                "Existing package/API conventions govern exposure of the new capability."
                if obligation["identity"] == "package-integration"
                else None
            ),
            "Applicability wording changed",
        )
        require(
            not obligation["pre_execution_witness_alternatives"],
            "Unexpected supplied alternatives",
        )
    resources = archive["resources"]
    require(
        manifest["eligible_resource_count"] == len(resources) == 531, "Resource count"
    )
    for resource in resources:
        require(
            set(resource) == {"identity", "address", "content_identity", "content"},
            "Resource metadata",
        )
        require(
            resource["identity"]
            == {
                "address": resource["address"],
                "content_identity": resource["content_identity"],
            },
            "Resource identity mismatch",
        )
        require(
            semantic_digest("decoded-utf8-text-sha256-v1", resource["content"])
            == resource["content_identity"],
            "Resource semantic content digest",
        )
    values = [
        v
        for r in sorted(resources, key=lambda r: r["address"])
        for v in (r["address"], r["content_identity"])
    ]
    require(
        semantic_digest(
            "explicit-required-text-resources-sha256-v1", REPOSITORY, *values
        )
        == SNAPSHOT,
        "Snapshot semantic digest",
    )
    return manifest, resources


def identity(value):
    require(set(value) == {"address", "content_identity"}, "Identity shape")
    return value["address"], value["content_identity"]


def coverage(expected, observed):
    """Exact multiset accounting independent of task semantics."""
    ec, oc = Counter(expected), Counter(observed)
    return {
        "expected_identities": len(expected),
        "observed_identities": len(observed),
        "duplicate_expected": sorted(str(k) for k, count in ec.items() if count > 1),
        "duplicate_observed": sorted(str(k) for k, count in oc.items() if count > 1),
        "missing": sorted(str(k) for k in ec.keys() - oc.keys()),
        "unexpected": sorted(str(k) for k in oc.keys() - ec.keys()),
    }


def expanded_cells(document):
    """Materialize the safe default representation for exact 531 x 10 accounting."""
    units = document["information_units"]
    cells = []
    for obligation in document["judgments"]:
        required = {
            identity(units[u["unit_identity"]]["resource_identity"])
            for u in obligation["required_units"]
        }
        helpful = {
            identity(r["resource_identity"]) for r in obligation["helpful_resources"]
        }
        for resource in document["eligible_resource_identities"]:
            key = identity(resource)
            classification = (
                "REQUIRED"
                if key in required
                else "HELPFUL_ONLY"
                if key in helpful
                else "UNNECESSARY"
            )
            cells.append((key, obligation["identity"], classification))
    return cells


def validate(document, manifest, resources):
    """Validate targets, alternatives, inferability, safe defaults and fixed frame."""
    reject_fields(document)
    require(
        document["schema"] == "case-0006-independent-judgments-v1", "Judgment schema"
    )
    for key in (
        "case_identity",
        "repository_id",
        "repository_snapshot_id",
        "eligible_frame_identity",
        "task_identity",
    ):
        require(document[key] == manifest[key], f"Judgment identity: {key}")
    require(
        document["frozen_obligations"] == manifest["obligations"],
        "Frozen obligations changed",
    )
    require(
        document["blind_packet_digests"]
        == {
            "blind_manifest.json": MANIFEST_SHA256,
            "blind_resources.json.gz": ARCHIVE_SHA256,
        },
        "Judgment packet digests",
    )
    expected = [identity(r["identity"]) for r in resources]
    observed = [identity(r) for r in document["eligible_resource_identities"]]
    resource_coverage = coverage(expected, observed)
    require(
        not any(
            resource_coverage[k]
            for k in (
                "duplicate_expected",
                "duplicate_observed",
                "missing",
                "unexpected",
            )
        ),
        "Resource coverage",
    )
    known = {identity(r["identity"]): r for r in resources}
    units = document["information_units"]
    for key, unit in units.items():
        require(key == unit["identity"], "Unit identity mismatch")
        target = identity(unit["resource_identity"])
        require(target in known, "Foreign unit target")
        lines = len(known[target]["content"].splitlines())
        require(unit["line_ranges"] and unit["information"], "Empty information unit")
        require(
            all(1 <= start <= end <= lines for start, end in unit["line_ranges"]),
            "Unit range",
        )
    judgments = document["judgments"]
    require(
        tuple(o["identity"] for o in judgments) == OBLIGATIONS,
        "Judgment completeness/order",
    )
    required_union = set()
    for obligation in judgments:
        require(
            obligation["applicability"]
            in {"APPLICABLE", "SUPPORTED_NOT_APPLICABLE", "UNRESOLVED_APPLICABILITY"},
            "Applicability",
        )
        require(obligation["applicability_rationale"], "Applicability evidence absent")
        require(
            obligation["default_resource_classification"] == "UNNECESSARY",
            "Unsafe default",
        )
        records = obligation["required_units"]
        ids = [r["unit_identity"] for r in records]
        require(
            len(ids) == len(set(ids)) and set(ids) <= units.keys(),
            "Required unit identities",
        )
        required_union.update(ids)
        for record in records:
            require(
                record["classification"] == "REQUIRED" and record["rationale"],
                "Required semantics",
            )
            require(
                record["inferability"] in {"INFERABLE_AT_START", "INHERENT_DISCOVERY"},
                "Inferability",
            )
            require(record["inferability_rationale"], "Inferability rationale")
            if record["inferability"] == "INHERENT_DISCOVERY":
                prerequisites = record["inherent_discovery_prerequisites"]
                require(
                    prerequisites
                    and all(
                        prerequisites.get(k)
                        for k in (
                            "later_observation",
                            "prerequisite",
                            "why_static_inspection_cannot_establish",
                        )
                    ),
                    "Discovery prerequisites",
                )
            else:
                require(
                    record["inherent_discovery_prerequisites"] is None,
                    "Spurious discovery",
                )
            require(
                record["manual_required_review"]["blind_evidence_only"] is True,
                "Blind review missing",
            )
        alternatives = obligation["acceptable_witness_alternatives"]
        if obligation["applicability"] == "APPLICABLE":
            require(alternatives, "Applicable mandatory alternative missing")
        sets = []
        for alternative in alternatives:
            members = alternative["all"]
            require(
                members
                and len(members) == len(set(members))
                and set(members) <= set(ids),
                "Alternative target structure",
            )
            sets.append(frozenset(members))
        require(len(sets) == len(set(sets)), "Duplicate equivalent alternative")
        require(set().union(*sets) == set(ids), "Required units outside alternatives")
        helpful = [
            identity(r["resource_identity"]) for r in obligation["helpful_resources"]
        ]
        require(
            len(helpful) == len(set(helpful)) and set(helpful) <= known.keys(),
            "Helpful targets",
        )
        required_resources = {identity(units[key]["resource_identity"]) for key in ids}
        require(not set(helpful) & required_resources, "Overlapping resource judgments")
        require(
            all(
                r["classification"] == "HELPFUL_ONLY" and r["rationale"]
                for r in obligation["helpful_resources"]
            ),
            "Helpful semantics",
        )
        require(not obligation["unresolved"], "This freeze expects no unresolved cells")
    require(required_union == units.keys(), "Unused unit definition")
    gaps = document["task_interpretation_gaps"]
    require(
        gaps
        == {
            "status": "no obvious mandatory task-interpretation gap found",
            "items": [],
        },
        "Gap representation",
    )
    cells = expanded_cells(document)
    expected_cells = [
        (key, obligation) for key in expected for obligation in OBLIGATIONS
    ]
    cell_coverage = coverage(expected_cells, [(r, o) for r, o, _ in cells])
    require(
        len(cells) == 5310
        and not any(
            cell_coverage[k]
            for k in (
                "duplicate_expected",
                "duplicate_observed",
                "missing",
                "unexpected",
            )
        ),
        "Cell coverage",
    )
    diagnostics = {
        "resources": resource_coverage,
        "resource_obligation_cells": cell_coverage,
    }
    require(
        document["identity_coverage"] == diagnostics, "Coverage diagnostic mismatch"
    )
    return diagnostics


def build():
    """Combine manual judgments with exact frozen identities and audit mechanics."""
    manifest, resources = load_packet()
    units, judgments = authored()
    document = {
        "schema": "case-0006-independent-judgments-v1",
        **{
            key: manifest[key]
            for key in (
                "case_identity",
                "task_identity",
                "repository_id",
                "repository_snapshot_id",
                "eligible_frame_identity",
                "development_task",
                "purpose",
            )
        },
        "blind_packet_digests": {
            "blind_manifest.json": MANIFEST_SHA256,
            "blind_resources.json.gz": ARCHIVE_SHA256,
        },
        "method": {
            "version": "manual-static-blind-v1",
            "description": "Exact frozen text inspection, static contract tracing and manual necessity/alternative review. No task-relative retriever or production imports.",
            "resource_aggregation": "A resource cell is REQUIRED iff it contains a REQUIRED selected unit in any acceptable alternative. This is a conditional alternative witness, not a claim that every such file must be read. Other spans are not thereby required. Explicit helpful resources override the default; every remaining exact resource identity is UNNECESSARY per obligation.",
            "unit_identity": "Case-local semantic key mapped to frozen address/content identity and inclusive frozen line ranges.",
            "digest_convention": "payload_sha256 hashes canonical JSON without payload_sha256; judgments.sha256 hashes complete judgments.json bytes.",
        },
        "shared_anchors": manifest["shared_anchors"],
        "frozen_obligations": manifest["obligations"],
        "eligible_resource_identities": [r["identity"] for r in resources],
        "information_units": units,
        "judgments": judgments,
        "task_interpretation_gaps": {
            "status": "no obvious mandatory task-interpretation gap found",
            "items": [],
        },
        "limitations": [
            "docs/implementation_ledger.md is absent from the complete 531-resource frame. Its historical update contents cannot be adjudicated; do not infer a non-applicable ledger requirement or escape the packet. Architecture/package/roadmap authority is positively established within the frame.",
            "Classification concerns information needed for the frozen task, not a prescribed implementation design. Alternative test/facade witnesses establish conventions; actual new capability behavior must be tested from its own contract.",
            "No future execution pass/fail result is a repository witness. No inherent-discovery need was established by static frozen evidence.",
        ],
        "inspection_evidence": sorted(
            {u["resource_identity"]["address"] for u in units.values()}
            | {
                r["resource_identity"]["address"]
                for o in judgments
                for r in o["helpful_resources"]
            }
            | {
                "src/devtools/context/repository/observation.py",
                "docs/backlog/overview.md",
            }
        ),
        "blindness_attestation": {
            "only_authorized_preexisting_inputs_accessed": True,
            "other_case_artifacts_accessed": False,
            "current_target_implementation_accessed": False,
            "confirmation_accessed": False,
            "stage_d_performed": False,
            "lexical_treatment_accessed": False,
            "role_treatment_accessed": False,
            "grounding_treatment_or_results_accessed": False,
            "generation_treatment_or_results_accessed": False,
            "recovery_history_accessed": False,
            "effectiveness_analysis_performed": False,
        },
    }
    expected = [identity(r["identity"]) for r in resources]
    cells = expanded_cells(document)
    document["identity_coverage"] = {
        "resources": coverage(
            expected, [identity(r) for r in document["eligible_resource_identities"]]
        ),
        "resource_obligation_cells": coverage(
            [(r, o) for r in expected for o in OBLIGATIONS],
            [(r, o) for r, o, _ in cells],
        ),
    }
    validate(document, manifest, resources)
    document["payload_sha256"] = digest(canonical(document))
    return document


def write_once(document, output):
    """Refuse overwrite before writing either frozen artifact or digest sidecar."""
    sidecar = output.with_suffix(".sha256")
    require(
        not output.exists() and not sidecar.exists(),
        "Refusing overwrite of frozen judgment",
    )
    data = canonical(document)
    with output.open("xb") as stream:
        stream.write(data)
    with sidecar.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(digest(data) + "  " + output.name + "\n")


def verify_frozen():
    """Rebuild in memory; require deterministic byte identity and both digests."""
    output = ROOT / "judgments.json"
    data = output.read_bytes()
    require(data == canonical(build()), "Deterministic replay mismatch")
    document = json.loads(data)
    payload = copy.deepcopy(document)
    supplied = payload.pop("payload_sha256")
    require(digest(canonical(payload)) == supplied, "Payload digest mismatch")
    require(
        (ROOT / "judgments.sha256").read_text(encoding="utf-8")
        == digest(data) + "  judgments.json\n",
        "Artifact digest mismatch",
    )
    return digest(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", action="store_true")
    args = parser.parse_args()
    if args.freeze:
        write_once(build(), ROOT / "judgments.json")
    print(verify_frozen())
