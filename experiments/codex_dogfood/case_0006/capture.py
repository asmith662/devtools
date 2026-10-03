# Copyright (c) 2026
# ruff: noqa: ANN001, ANN201, ANN202, C901, COM812, D103, E501, EM101, EM102, INP001, PLC0415, PLR0912, PLR0913, PLR0915, PLR0917, PLR2004, RUF100, T201, TRY003
"""Execute Case 0006 frozen treatment once and capture native outputs."""

from __future__ import annotations

import asyncio
import gzip
import hashlib
import json
import os
import pickle
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path
from unittest.mock import patch

from devtools.context.localization.association import WitnessHypothesisIdentity
from devtools.context.localization.generation import (
    GroundedMemberRecipe,
    ProjectionKind,
    WitnessGenerationPlan,
    WitnessGenerationRecipe,
    generate_witness_hypotheses,
)
from devtools.context.localization.grounding import (
    AnchorGroundingDisposition,
    build_anchor_grounding_view,
)
from devtools.context.localization.identity import (
    LocalizationObligationIdentity,
    TaskProvenance,
)
from devtools.context.localization.lexical import acquire_localization_lexical_evidence
from devtools.context.localization.roles.models import RepositoryRoleKind
from devtools.context.localization.routing import route_localization_lexical_evidence
from devtools.context.repository.resource import RepositoryResourceOccurrence

CASE = Path(__file__).resolve().parent
ROOT = CASE.parents[2]
STAGE_A = "e7aed4162672dd859a0a8a33a2b718dda8425495"
SOURCE_HEAD = "492229e0e0d4661cf5287c26d18c6488a80fe8ce"
OUTPUTS = (
    "capture.pkl.gz",
    "retrieval.json",
    "routing.json",
    "grounding.json",
    "generation.json",
    "stage_b_integrity.json",
    "stage_b.md",
)
RECOVERY_ID = "case-0006-stage-b-recovery-1"
PRIOR_FAILED_EXECUTION_COUNT = 1
RAW_CAPTURE = "stage_b_recovery_raw.pkl.gz"
RECOVERY_STARTED = "stage_b_recovery_started.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, indent=2) + "\n").encode()


def _save_raw(state: dict) -> None:
    """Durably checkpoint native results as incomplete recovery material."""
    state["recovery_metadata"] = {
        "execution_kind": "RECOVERY",
        "recovery_id": RECOVERY_ID,
        "prior_failed_execution_count": PRIOR_FAILED_EXECUTION_COUNT,
        "stage_a_commit": STAGE_A,
        "invocation_counts": dict(state.get("invocations", {})),
        "status": "INCOMPLETE_UNVALIDATED",
    }
    payload = gzip.compress(
        pickle.dumps(state, protocol=pickle.HIGHEST_PROTOCOL), mtime=0
    )
    target = CASE / RAW_CAPTURE
    with tempfile.NamedTemporaryFile(
        dir=CASE, prefix=".case0006-raw-", delete=False
    ) as stream:
        temporary = Path(stream.name)
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(target)


def _load_raw() -> dict | None:
    path = CASE / RAW_CAPTURE
    if not path.exists():
        return None
    value = pickle.loads(gzip.decompress(path.read_bytes()))  # noqa: S301
    metadata = value.get("recovery_metadata", {})
    if (metadata.get("recovery_id"), metadata.get("status")) != (
        RECOVERY_ID,
        "INCOMPLETE_UNVALIDATED",
    ):
        raise ValueError("Raw recovery capture has invalid recovery metadata.")
    return value


def _execution_decision(
    *, raw_exists: bool, started_exists: bool, outputs: tuple[str, ...]
) -> str:
    """Choose execute, resume, or refuse before any production operation."""
    if outputs:
        raise FileExistsError(f"Stage B outputs already exist: {list(outputs)}")
    if raw_exists:
        return "RESUME"
    if started_exists:
        raise FileExistsError(
            "The one authorized recovery execution was already started."
        )
    return "EXECUTE"


def _validate_member_keys(expected: set[str], actual: dict[str, object]) -> None:
    if len(actual) != len(expected) or set(actual) != expected:
        raise ValueError("Complementary member identities changed.")


def _validate_member_binding(member_attempt, member_spec: dict, grounding) -> None:
    recipe = member_attempt.recipe
    provenance = member_spec["provenance"]
    if (
        recipe.key != member_spec["identity"]
        or recipe.grounding != grounding
        or recipe.projection.name != member_spec["projection"]
        or recipe.reason != member_spec["reason"]
        or str(recipe.provenance.source_identity) != provenance["source"]
        or recipe.provenance.explanation != provenance["explanation"]
    ):
        raise ValueError("Member binding differs from exact frozen treatment fields.")


def _publish_outputs(payloads: dict[str, bytes], *, validated: bool) -> None:
    """Exclusively publish finalized Stage B artifacts after validation."""
    if not validated:
        raise ValueError("Canonical Stage B outputs require successful validation.")
    existing = [name for name in OUTPUTS if (CASE / name).exists()]
    if existing:
        raise FileExistsError(f"Stage B outputs already exist: {existing}")
    if set(payloads) != set(OUTPUTS):
        raise ValueError("Final artifact set does not match canonical Stage B outputs.")
    for name, data in payloads.items():
        with (CASE / name).open("xb") as output:
            output.write(data)


def resource_data(resource: RepositoryResourceOccurrence) -> dict:
    return {
        "address": resource.address.value,
        "content_identity": resource.content_identity.value,
    }


def referent_data(referent: object) -> dict:
    result = {"type": type(referent).__name__}
    identity = getattr(referent, "identity", None)
    if identity is not None:
        result["identity"] = str(identity)
    if isinstance(referent, RepositoryResourceOccurrence):
        result["resource"] = resource_data(referent)
    else:
        resource = getattr(referent, "resource", None)
        support = getattr(referent, "support", None)
        address = getattr(resource, "address", None) or getattr(
            support, "resource_address", None
        )
        if address is not None:
            result["owner_address"] = address.value
        subject = getattr(referent, "subject", None)
        if subject is not None:
            result["subject_identity"] = str(subject.identity)
    return result


def evidence_data(evidence: object) -> dict:
    result = {"type": type(evidence).__name__}
    identity = getattr(evidence, "identity", None)
    if identity is not None:
        result["identity"] = str(identity)
    analysis = getattr(evidence, "analysis", None)
    if analysis is not None:
        result["analysis_type"] = type(analysis).__name__
        module = getattr(analysis, "module", None)
        if module is not None:
            result["module_identity"] = str(module.identity)
        resource = getattr(analysis, "resource", None)
        if resource is not None:
            result["resource"] = resource_data(resource)
    return result


def grounding_data(identity: str, grounding) -> dict:
    locator = grounding.request.locator
    if hasattr(locator, "address"):
        locator_data = {"kind": "RESOURCE_ADDRESS", "address": locator.address.value}
    elif hasattr(locator, "declared_name"):
        locator_data = {
            "kind": "PYTHON_DECLARATION",
            "module": locator.module.dotted_name,
            "name": locator.declared_name,
            "declaration_kind": locator.kind.name,
        }
    else:
        locator_data = {"kind": type(locator).__name__}
    return {
        "request_identity": identity,
        "task_identity": grounding.request.task.value,
        "anchor_identity": grounding.request.anchor.value,
        "repository_id": str(grounding.request.repository_id),
        "snapshot_id": str(grounding.request.snapshot_id),
        "locator": locator_data,
        "interpretation_provenance": {
            "source_identity": str(grounding.request.provenance.source_identity),
            "explanation": grounding.request.provenance.explanation,
        },
        "resolver": grounding.resolver.value,
        "disposition": grounding.disposition.value,
        "reason": grounding.reason,
        "candidates": [
            {
                "referent": referent_data(candidate.referent),
                "evidence": evidence_data(candidate.evidence),
            }
            for candidate in grounding.candidates
        ],
        "native_evidence": [evidence_data(item) for item in grounding.native_evidence],
        "module_universe_identity": (
            grounding.module_universe.identity if grounding.module_universe else None
        ),
    }


def lexical_result(identity: str, result, obligation: str | None) -> dict:
    return {
        "lane_identity": identity,
        "obligation_identity": obligation,
        "query_text": result.query.text,
        "query_semantics": result.query.QUERY_SEMANTICS,
        "retrieval_semantics": result.RETRIEVAL_SEMANTICS,
        "index_semantics": result.index.INDEX_SEMANTICS,
        "maximum_results": result.maximum_results,
        "settings": {"k1": result.settings.k1, "b": result.settings.b},
        "matches": [
            {
                "rank": rank,
                "resource": resource_data(
                    match.document_statistics.analysis.document.resource
                ),
                "score": match.score,
                "content_score": match.content_score,
                "filename_score": match.filename_score,
                "filename_weight": match.filename_weight,
                "weighted_filename_score": match.weighted_filename_score,
                "content_contributions": [
                    {
                        "term": term.normalized_term,
                        "tf": term.term_frequency,
                        "df": term.document_frequency,
                        "idf": term.inverse_document_frequency,
                        "contribution": term.contribution,
                    }
                    for term in match.term_contributions
                ],
                "filename_contributions": [
                    {
                        "term": term.normalized_term,
                        "tf": term.term_frequency,
                        "df": term.document_frequency,
                        "idf": term.inverse_document_frequency,
                        "contribution": term.contribution,
                    }
                    for term in match.filename_term_contributions
                ],
            }
            for rank, match in enumerate(result.matches, 1)
        ],
    }


def role_data(item) -> dict:
    return {
        "identity": item.identity,
        "role": item.role.value,
        "supports": [
            {
                "identity": support.identity,
                "kind": support.kind.value,
                "source_address": support.source_address.value,
                "native_identities": list(support.native_identities),
                "observation": list(support.observation),
            }
            for support in item.supports
        ],
    }


def routing_data(routed) -> dict:
    lanes = []
    for lane in routed.obligation_lanes:
        candidates = []
        for candidate in lane.candidates:
            match = candidate.match
            resource = match.document_statistics.analysis.document.resource
            candidates.append(
                {
                    "native_rank": candidate.native_rank,
                    "routed_position": candidate.routed_position,
                    "tier": candidate.tier.value,
                    "resource": resource_data(resource),
                    "score": match.score,
                    "role_support": [
                        role_data(item) for item in candidate.role_evidence
                    ],
                }
            )
        lanes.append(
            {
                "query_identity": lane.preference.query.value,
                "query_text": lane.native_lane.retrieval.query.text,
                "obligation_identity": lane.preference.obligation.value,
                "preferred_roles": [
                    role.value for role in lane.preference.preferred_roles
                ],
                "preferred_count": len(lane.preferred),
                "escape_count": len(lane.escape),
                "candidates": candidates,
            }
        )
    return {
        "semantics": "caller-role-or-stable-two-tier-v1",
        "global_lane_unchanged": routed.global_retrieval
        is routed.acquisition.full_task_retrieval,
        "global_lane": lexical_result(
            "global-full-task", routed.global_retrieval, None
        ),
        "lanes": lanes,
    }


def support_summary(member) -> dict:
    return {
        "target": resource_data(member.target),
        "reason": member.reason,
        "structural": [
            {
                "type": type(support).__name__,
                "grounding_request_anchor": support.grounding.request.anchor.value,
                "grounding_resolver": support.grounding.resolver.value,
                "correspondence": (
                    {
                        "identity": support.correspondence.identity,
                        "source": resource_data(support.correspondence.source),
                        "test": resource_data(support.correspondence.test),
                    }
                    if hasattr(support, "correspondence")
                    else None
                ),
            }
            for support in member.structural
        ],
        "lexical": [
            {
                "query_identity": item.query.value if item.query else None,
                "native_rank": item.native_rank,
                "score": item.match.score,
            }
            for item in member.lexical
        ],
        "role": [role_data(item) for item in member.roles],
        "routed": [
            {
                "query_identity": item.query.value,
                "native_rank": item.candidate.native_rank,
                "routed_position": item.candidate.routed_position,
                "tier": item.candidate.tier.value,
                "role_support": [
                    role_data(value) for value in item.candidate.role_evidence
                ],
            }
            for item in member.routed
        ],
    }


def generation_data(view, frozen_groundings: dict, frozen_specs: list[dict]) -> dict:
    recipe_by_id = {
        (item["obligation"], item["identity"]): item for item in frozen_specs
    }
    attempts = []
    origin_checks = []
    for attempt in view.attempts:
        spec = recipe_by_id[
            (attempt.recipe.identity.obligation.value, attempt.recipe.identity.value)
        ]
        member_attempts = []
        for member_attempt in attempt.members:
            member_spec = next(
                item
                for item in spec["members"]
                if item["identity"] == member_attempt.recipe.key
            )
            member_attempts.append(
                {
                    "member_identity": member_attempt.recipe.key,
                    "grounding_request_identity": member_spec["grounding_request"],
                    "grounding_disposition": frozen_groundings[
                        member_spec["grounding_request"]
                    ].disposition.value,
                    "grounding_reason": frozen_groundings[
                        member_spec["grounding_request"]
                    ].reason,
                    "projection": member_attempt.recipe.projection.name,
                    "caller_reason": member_attempt.recipe.reason,
                    "caller_provenance": {
                        "source_identity": str(
                            member_attempt.recipe.provenance.source_identity
                        ),
                        "explanation": member_attempt.recipe.provenance.explanation,
                    },
                    "disposition": member_attempt.disposition.value,
                    "projection_outcome_reason": (
                        "No exact native mirrored correspondence in the frozen snapshot."
                        if member_attempt.disposition.value == "no-target"
                        else None
                    ),
                    "source": referent_data(member_attempt.source)
                    if member_attempt.source
                    else None,
                    "targets": [
                        resource_data(target) for target in member_attempt.targets
                    ],
                    "result_count": member_attempt.result_count,
                    "result_limit": member_attempt.result_limit,
                    "examined_resources": member_attempt.examined_resources,
                    "truncated": member_attempt.truncated,
                    "uncovered_frontier": [
                        resource_data(item)
                        for item in member_attempt.uncovered_frontier
                    ],
                    "mirror_derivation_identity": member_attempt.mirror_analysis.derivation.identity
                    if member_attempt.mirror_analysis
                    else None,
                    "structural_support": [
                        {
                            "type": type(support).__name__,
                            "grounding_anchor": support.grounding.request.anchor.value,
                            "correspondence_identity": support.correspondence.identity
                            if hasattr(support, "correspondence")
                            else None,
                        }
                        for support in member_attempt.structural
                    ],
                }
            )
        hypotheses = []
        if attempt.hypothesis is not None:
            for member in attempt.hypothesis.members:
                origin_checks.append(
                    {
                        "hypothesis_identity": attempt.hypothesis.identity.value,
                        "target": member.target.address.value,
                        "structural_support_present": bool(member.structural),
                        "target_was_projected": any(
                            member.target in item.targets
                            and item.disposition.value == "generated"
                            for item in attempt.members
                        ),
                    }
                )
                hypotheses.append(support_summary(member))
        attempts.append(
            {
                "obligation_identity": attempt.recipe.identity.obligation.value,
                "recipe_identity": attempt.recipe.identity.value,
                "recipe_provenance": {
                    "source_identity": str(attempt.recipe.provenance.source_identity),
                    "explanation": attempt.recipe.provenance.explanation,
                },
                "disposition": attempt.disposition.value,
                "members": member_attempts,
                "hypothesis_identity": attempt.hypothesis.identity.value
                if attempt.hypothesis
                else None,
                "hypothesis_members": hypotheses,
            }
        )
    return {
        "execution_count": 1,
        "hypotheses_unresolved": True,
        "recipes": attempts,
        "origin_checks": origin_checks,
        "summary": {
            "recipes_attempted": len(view.attempts),
            "generated_hypotheses": len(view.generated),
            "member_occurrences": sum(len(item.members) for item in view.generated),
            "unique_resources": len(
                {member.target for item in view.generated for member in item.members}
            ),
            "generation_dispositions": dict(
                Counter(item.disposition.value for item in view.attempts)
            ),
            "projection_dispositions": dict(
                Counter(
                    member.disposition.value
                    for item in view.attempts
                    for member in item.members
                )
            ),
            "projection_operators": dict(
                Counter(
                    member.recipe.projection.name
                    for item in view.attempts
                    for member in item.members
                )
            ),
            "examined_resources_total": sum(
                member.examined_resources
                for item in view.attempts
                for member in item.members
            ),
            "target_origin_valid": all(
                item["structural_support_present"] and item["target_was_projected"]
                for item in origin_checks
            ),
            "lexical_supports": sum(
                len(member.lexical)
                for item in view.generated
                for member in item.members
            ),
            "role_supports": sum(
                len(member.roles) for item in view.generated for member in item.members
            ),
            "routed_supports": sum(
                len(member.routed) for item in view.generated for member in item.members
            ),
        },
    }


def build_objects(native: dict, acquisition, routed, groundings):
    requests = native["grounding_requests"]
    grounding_by_identity = {
        identity: next(
            result for result in groundings.groundings if result.request == request
        )
        for identity, request in requests.items()
    }
    recipes = []
    for spec in native["generation_recipe_specs"]:
        members = []
        for member in spec["members"]:
            request_id = member["grounding_request"]
            grounding = grounding_by_identity[request_id]
            members.append(
                GroundedMemberRecipe(
                    member["identity"],
                    grounding,
                    ProjectionKind[member["projection"]],
                    member["reason"],
                    TaskProvenance(
                        spec["provenance"]["source"],
                        explanation=member["provenance"]["explanation"],
                    ),
                )
            )
        obligation = LocalizationObligationIdentity(
            acquisition.task.identity, spec["obligation"]
        )
        recipes.append(
            WitnessGenerationRecipe(
                WitnessHypothesisIdentity(obligation, spec["identity"]),
                tuple(members),
                TaskProvenance(
                    spec["provenance"]["source"],
                    explanation=spec["provenance"]["explanation"],
                ),
            )
        )
    plan = WitnessGenerationPlan(
        acquisition.task,
        native["request"].snapshot,
        tuple(recipes),
        acquisition,
        native["role_evidence"],
        routed,
    )
    return plan, grounding_by_identity


def execute() -> dict:
    """Execute the single recovery or resume its incomplete native capture."""
    existing = [name for name in OUTPUTS if (CASE / name).exists()]
    state = _load_raw()
    started = CASE / RECOVERY_STARTED
    _execution_decision(
        raw_exists=state is not None,
        started_exists=started.exists(),
        outputs=tuple(existing),
    )
    if (ROOT / ".git").exists():
        _require_stage_a_ancestor()

    # Verify committed Stage A bytes before loading trusted pickle.
    from freeze import binary
    from freeze import sha as stage_a_sha

    integrity = json.loads(binary(CASE / "integrity.json"))
    for name, expected in integrity.items():
        content = binary(CASE / name)
        if name.endswith((".py", ".md", ".json")):
            content = content.replace(b"\r\n", b"\n")
        if stage_a_sha(content) != expected:
            raise ValueError(f"Stage A artifact digest differs: {name}")
    treatment = json.loads(binary(CASE / "treatment.json"))
    manifest = json.loads(binary(CASE / "pre_retrieval.json"))
    archive_bytes = binary(CASE / "inputs.pkl.gz")
    if sha(archive_bytes) != manifest["inputs_sha256"]:
        raise ValueError("Frozen native archive digest differs.")
    for path, expected in manifest["implementation_sha256"].items():
        content = binary(ROOT / path).replace(b"\r\n", b"\n")
        if sha(content) != expected:
            raise ValueError(f"Frozen production implementation differs: {path}")
    if manifest["starting_head"] != SOURCE_HEAD:
        raise ValueError("Manifest does not name the frozen source snapshot.")
    native = pickle.loads(gzip.decompress(archive_bytes))  # noqa: S301
    if state is not None:
        native = state["native"]
    request = native["request"]
    snapshot = request.snapshot
    if (
        len(snapshot.resources) != 531
        or str(snapshot.repository_id) != manifest["repository_id"]
        or str(snapshot.id) != manifest["snapshot_id"]
        or str(
            request.index.corpus_statistics.collection_analysis.document_collection.corpus.id
        )
        != manifest["eligible_corpus_id"]
    ):
        raise ValueError("Frozen native frame identity differs.")
    if (
        len(native["grounding_requests"]) != 9
        or len(native["generation_recipe_specs"]) != 9
    ):
        raise ValueError("Frozen request or recipe count differs.")
    if (
        request.full_task_query != treatment["task_full_prompt"]
        or request.purpose != treatment["purpose"]
        or len(request.obligation_queries) != len(treatment["obligation_queries"])
        or tuple(item.text for item in request.obligation_queries)
        != tuple(item["text"] for item in treatment["obligation_queries"])
        or tuple(item.preferred_roles for item in native["preferences"])
        != tuple(
            tuple(RepositoryRoleKind[name] for name in item["preferred_roles"])
            for item in treatment["obligation_queries"]
        )
    ):
        raise ValueError("Frozen task, queries, purpose or preferences differ.")

    state = state or {"native": native, "invocations": {}}
    if "acquisition" in state:
        acquisition = state["acquisition"]
        lexical_runtime = state["runtimes"]["lexical"]
    else:
        if not started.exists():
            with started.open("xb") as marker:
                marker.write(
                    canonical(
                        {
                            "execution_kind": "RECOVERY",
                            "recovery_id": RECOVERY_ID,
                            "prior_failed_execution_count": PRIOR_FAILED_EXECUTION_COUNT,
                            "maximum_additional_treatment_executions": 1,
                        }
                    )
                )
        lexical_started = time.perf_counter()
        acquisition = acquire_localization_lexical_evidence(request)
        lexical_runtime = time.perf_counter() - lexical_started
        state.update(acquisition=acquisition, runtimes={"lexical": lexical_runtime})
        state["invocations"]["lexical_acquisition"] = 1
        _save_raw(state)
    if len(acquisition.obligation_retrievals) != 10 or tuple(
        item.request.identity.value for item in acquisition.obligation_retrievals
    ) != tuple(
        item["identity"]
        for item in json.loads(binary(CASE / "treatment.json"))["obligation_queries"]
    ):
        raise ValueError("Acquisition lanes differ from the frozen ten-query order.")

    if "routed" in state:
        routed = state["routed"]
        routing_runtime = state["runtimes"]["routing"]
    else:
        routing_started = time.perf_counter()
        routed = route_localization_lexical_evidence(
            acquisition, native["role_evidence"], native["preferences"]
        )
        routing_runtime = time.perf_counter() - routing_started
        state["routed"] = routed
        state["runtimes"]["routing"] = routing_runtime
        state["invocations"]["role_routing"] = 1
        _save_raw(state)
    _validate_routing(acquisition, routed, native["preferences"])

    if "grounding_view" in state:
        grounding_view = state["grounding_view"]
        grounding_runtime = state["runtimes"]["grounding"]
    else:
        grounding_started = time.perf_counter()
        grounding_view = build_anchor_grounding_view(
            task=request.task,
            snapshot=snapshot,
            requests=tuple(native["grounding_requests"].values()),
            module_universe=native["module_universe"],
        )
        grounding_runtime = time.perf_counter() - grounding_started
        state["grounding_view"] = grounding_view
        state["runtimes"]["grounding"] = grounding_runtime
        state["invocations"]["grounding_requests"] = len(native["grounding_requests"])
        _save_raw(state)
    if len(grounding_view.groundings) != len(native["grounding_requests"]):
        raise ValueError("Grounding view did not account for every frozen request.")
    by_request = {
        identity: next(
            result
            for result in grounding_view.groundings
            if result.request == frozen_request
        )
        for identity, frozen_request in native["grounding_requests"].items()
    }
    _validate_groundings(native, snapshot, by_request)

    plan, grounding_by_identity = build_objects(
        native, acquisition, routed, grounding_view
    )
    if len(plan.recipes) != len(native["generation_recipe_specs"]):
        raise ValueError("Generation plan changed competing recipe cardinality.")
    generation_started = time.perf_counter()
    validation_cache_hits = 0

    def cached_grounding(*, task, snapshot, request, module_universe=None):
        nonlocal validation_cache_hits
        for result in grounding_by_identity.values():
            if result.request == request:
                if result.module_universe != module_universe:
                    raise ValueError(
                        "Generation validation changed the frozen module universe."
                    )
                if task != plan.task or snapshot != plan.snapshot:
                    raise ValueError("Generation validation changed the frozen frame.")
                validation_cache_hits += 1
                return result
        raise ValueError("Generation validation requested an unfrozen locator.")

    # Production generation replay-checks member groundings. Route those checks
    # through the exact once-resolved result cache; no locator is rerun.
    if "generation_view" in state:
        generation_view = state["generation_view"]
        generation_runtime = state["runtimes"]["generation"]
        validation_cache_hits = state["validation_cache_hits"]
    else:
        with patch(
            "devtools.context.localization.generation.generate.ground_task_anchor",
            cached_grounding,
        ):
            generation_view = generate_witness_hypotheses(plan)
        generation_runtime = time.perf_counter() - generation_started
        state["generation_view"] = generation_view
        state["generation_plan"] = plan
        state["runtimes"]["generation"] = generation_runtime
        state["invocations"]["generation"] = 1
        state["validation_cache_hits"] = validation_cache_hits
        _save_raw(state)
    if len(generation_view.attempts) != len(native["generation_recipe_specs"]):
        raise ValueError("Generation view omitted a frozen recipe.")
    _validate_generation(native, generation_view, grounding_by_identity, snapshot)

    retrieval = {
        "case": "case_0006",
        "execution_kind": "RECOVERY",
        "recovery_id": RECOVERY_ID,
        "prior_failed_execution_count": PRIOR_FAILED_EXECUTION_COUNT,
        "repository_id": str(snapshot.repository_id),
        "snapshot_id": str(snapshot.id),
        "global_lane": lexical_result(
            "global-full-task", acquisition.full_task_retrieval, None
        ),
        "obligation_lanes": [
            lexical_result(
                item.request.identity.value,
                item.retrieval,
                item.request.obligation.value,
            )
            for item in acquisition.obligation_retrievals
        ],
        "invocation_count": 1,
        "runtime_seconds": lexical_runtime,
    }
    routed_data = routing_data(routed)
    routed_data.update(
        {
            "execution_kind": "RECOVERY",
            "recovery_id": RECOVERY_ID,
            "prior_failed_execution_count": PRIOR_FAILED_EXECUTION_COUNT,
        }
    )
    routed_data["invocation_count"] = 1
    routed_data["runtime_seconds"] = routing_runtime
    grounding_json = {
        "case": "case_0006",
        "execution_kind": "RECOVERY",
        "recovery_id": RECOVERY_ID,
        "prior_failed_execution_count": PRIOR_FAILED_EXECUTION_COUNT,
        "invocation_count": len(native["grounding_requests"]),
        "runtime_seconds": grounding_runtime,
        "requests": [
            grounding_data(identity, by_request[identity])
            for identity in native["grounding_requests"]
        ],
        "disposition_counts": dict(
            Counter(item.disposition.value for item in by_request.values())
        ),
        "generator_grounding_cache_hits": validation_cache_hits,
        "generator_fresh_resolution_count": 0,
    }
    generated = generation_data(
        generation_view,
        grounding_by_identity,
        native["generation_recipe_specs"],
    )
    generated.update(
        {
            "execution_kind": "RECOVERY",
            "recovery_id": RECOVERY_ID,
            "prior_failed_execution_count": PRIOR_FAILED_EXECUTION_COUNT,
        }
    )
    generated["runtime_seconds"] = generation_runtime
    generated["plan"] = {
        "obligation_count": len(request.task.obligations),
        "recipe_count": len(plan.recipes),
        "member_count": sum(len(item.members) for item in plan.recipes),
        "recipe_structure": [
            {
                "obligation": item.identity.obligation.value,
                "recipe": item.identity.value,
                "members": [member.key for member in item.members],
            }
            for item in plan.recipes
        ],
    }
    native_capture = {
        "stage_a_commit": STAGE_A,
        "stage_a_manifest_sha256": sha(canonical(manifest)),
        "stage_a_archive_sha256": sha(archive_bytes),
        "request": request,
        "role_evidence": native["role_evidence"],
        "preferences": native["preferences"],
        "module_universe": native["module_universe"],
        "module_analyses": native["module_analyses"],
        "mirrored_paths": native["mirrored_paths"],
        "grounding_requests": native["grounding_requests"],
        "generation_recipe_specs": native["generation_recipe_specs"],
        "acquisition": acquisition,
        "routed": routed,
        "grounding_view": grounding_view,
        "generation_plan": plan,
        "generation_view": generation_view,
        "recovery_metadata": {
            "execution_kind": "RECOVERY",
            "recovery_id": RECOVERY_ID,
            "prior_failed_execution_count": PRIOR_FAILED_EXECUTION_COUNT,
        },
    }
    capture_bytes = gzip.compress(
        pickle.dumps(native_capture, protocol=pickle.HIGHEST_PROTOCOL), mtime=0
    )
    payloads = {
        "capture.pkl.gz": capture_bytes,
        "retrieval.json": canonical(retrieval),
        "routing.json": canonical(routed_data),
        "grounding.json": canonical(grounding_json),
        "generation.json": canonical(generated),
    }
    stage_b_record = _record(
        lexical_runtime,
        routing_runtime,
        grounding_runtime,
        generation_runtime,
        grounding_json,
        generated,
        {name: sha(data) for name, data in payloads.items()},
    )
    payloads["stage_b.md"] = stage_b_record.encode()
    digests = {name: sha(data) for name, data in payloads.items()}
    digests["capture.py"] = sha(
        (CASE / "capture.py").read_bytes().replace(b"\r\n", b"\n")
    )
    payloads["stage_b_integrity.json"] = canonical(
        {
            "case": "case_0006",
            "execution_kind": "RECOVERY",
            "recovery_id": RECOVERY_ID,
            "prior_failed_execution_count": PRIOR_FAILED_EXECUTION_COUNT,
            "stage_a_commit": STAGE_A,
            "stage_a_integrity_sha256": sha(binary(CASE / "integrity.json")),
            "artifacts": digests,
        }
    )
    _publish_outputs(payloads, validated=True)
    return {
        "retrieval_lanes": len(retrieval["obligation_lanes"]) + 1,
        "routed_lanes": len(routed_data["lanes"]),
        "groundings": grounding_json["disposition_counts"],
        "generation": generated["summary"],
        "artifact_sha256": digests,
    }


def _validate_routing(acquisition, routed, preferences) -> None:
    if routed.global_retrieval is not acquisition.full_task_retrieval:
        raise ValueError("Global lexical lane changed during routing.")
    if len(routed.obligation_lanes) != len(acquisition.obligation_retrievals):
        raise ValueError("Routing lane count changed.")
    for native_lane, lane, preference in zip(
        acquisition.obligation_retrievals,
        routed.obligation_lanes,
        preferences,
        strict=True,
    ):
        if lane.preference != preference:
            raise ValueError("Routed preference differs from frozen preference.")
        original = native_lane.retrieval.matches
        candidates = lane.candidates
        if len(candidates) != len(original) or {
            id(item.match) for item in candidates
        } != {id(item) for item in original}:
            raise ValueError("Routing dropped or duplicated a native candidate.")
        for tier in (lane.preferred, lane.escape):
            if tuple(item.native_rank for item in tier) != tuple(
                sorted(item.native_rank for item in tier)
            ):
                raise ValueError("Routing changed native within-tier order.")
        if (
            not preference.preferred_roles
            and tuple(item.match for item in candidates) != original
        ):
            raise ValueError("Empty preference did not preserve exact native order.")
        if tuple(item.routed_position for item in candidates) != tuple(
            range(1, len(candidates) + 1)
        ):
            raise ValueError(
                "Routed positions are not contiguous presentation positions."
            )


def _validate_groundings(native, snapshot, results) -> None:
    expected = native["grounding_requests"]
    if set(results) != set(expected) or len(results) != 9:
        raise ValueError("Grounding request identity coverage differs.")
    for identity, result in results.items():
        if result.request != expected[identity]:
            raise ValueError("Grounding result differs from its exact frozen request.")
        if (
            result.request.repository_id != snapshot.repository_id
            or result.request.snapshot_id != snapshot.id
        ):
            raise ValueError("Grounding result has a foreign repository/snapshot.")
        for candidate in result.candidates:
            referent = candidate.referent
            if isinstance(referent, RepositoryResourceOccurrence):
                snapshot.resource_at(referent.address)
            else:
                resource = getattr(referent, "resource", None)
                support = getattr(referent, "support", None)
                address = getattr(resource, "address", None) or getattr(
                    support, "resource_address", None
                )
                if address is not None:
                    snapshot.resource_at(address)
        if (
            result.disposition is AnchorGroundingDisposition.RESOLVED
            and len(result.candidates) != 1
        ):
            raise ValueError("Resolved grounding has invalid candidate cardinality.")


def _validate_generation(native, view, groundings, snapshot) -> None:
    specs = native["generation_recipe_specs"]
    observed = {
        (item.recipe.identity.obligation.value, item.recipe.identity.value): item
        for item in view.attempts
    }
    expected = {(item["obligation"], item["identity"]) for item in specs}
    if set(observed) != expected or len(observed) != len(specs):
        raise ValueError("Generation recipe identity/coverage differs.")
    spec_by_identity = {(item["obligation"], item["identity"]): item for item in specs}
    for key, attempt in observed.items():
        spec = spec_by_identity[key]
        if len(attempt.members) != len(spec["members"]):
            raise ValueError("Complementary member shape changed.")
        member_attempts = {
            member_attempt.recipe.key: member_attempt
            for member_attempt in attempt.members
        }
        _validate_member_keys(
            {item["identity"] for item in spec["members"]}, member_attempts
        )
        for member_spec in spec["members"]:
            member_attempt = member_attempts[member_spec["identity"]]
            grounding = groundings[member_spec["grounding_request"]]
            _validate_member_binding(member_attempt, member_spec, grounding)
        if attempt.hypothesis is not None:
            for member in attempt.hypothesis.members:
                if snapshot.resource_at(member.target.address) != member.target:
                    raise ValueError("Generated target is outside frozen snapshot.")
                if not member.structural:
                    raise ValueError(
                        "Generated target has no structural origin support."
                    )
    if view.association.task != view.plan.task or view.association.snapshot != snapshot:
        raise ValueError("Generated association view differs from frozen task/frame.")


def _record(
    lexical, routing, grounding, generation, grounding_json, generated, digests
) -> str:
    counts = grounding_json["disposition_counts"]
    summary = generated["summary"]
    lines = [
        "# Case 0006 Stage B",
        "",
        f"Execution kind: `RECOVERY`; recovery ID: `{RECOVERY_ID}`; prior failed executions: `{PRIOR_FAILED_EXECUTION_COUNT}`.",
        "**CAPTURED — NOT ADJUDICATED. No effectiveness analysis was performed.**",
        "",
        f"Stage A commit: `{STAGE_A}`.",
        "Execution entry point: `capture.py --execute`; all treatment inputs were loaded from the digest-verified committed native archive.",
        "",
        "## Invocation counts and runtimes",
        "",
        f"- Lexical acquisition: 1 call, {lexical:.6f}s.",
        f"- Role routing: 1 call, {routing:.6f}s.",
        f"- Explicit frozen grounding requests: {grounding_json['invocation_count']} calls, {grounding:.6f}s; dispositions `{counts}`.",
        f"- Witness generation: 1 plan execution, {generation:.6f}s; production validation checked {grounding_json['generator_grounding_cache_hits']} recipe-member references using exact cached grounding results, with zero additional resolver executions.",
        "",
        "## Mechanical outcomes",
        "",
        f"- Generated hypotheses: {summary['generated_hypotheses']}; member occurrences: {summary['member_occurrences']}; unique targets: {summary['unique_resources']}.",
        f"- Generation dispositions: `{summary['generation_dispositions']}`; projection dispositions: `{summary['projection_dispositions']}`.",
        f"- Projection operators: `{summary['projection_operators']}`; summed examined-resource count: {summary['examined_resources_total']}.",
        f"- Generated target origin check (resolved grounding plus frozen structural projection): `{summary['target_origin_valid']}`.",
        f"- Attached supports: lexical {summary['lexical_supports']}, role {summary['role_supports']}, routed {summary['routed_supports']}.",
        "- Global lane identity and routed candidate retention/order checks passed. No generated rank or position was recorded.",
        "",
        "## Output files and SHA-256",
        "",
    ]
    lines.extend(f"- `{name}`: `{digest}`" for name, digest in digests.items())
    lines.extend(
        [
            "- `stage_b.md` contains the execution record; its digest is retained in `stage_b_integrity.json`.",
            "",
            "All canonical Stage B outputs refuse overwrite. Incomplete native checkpoints are marked unvalidated and are resumed without repeating completed operations. This record contains execution/integrity facts only; no resources have been judged and no candidate surface has been evaluated for effectiveness.",
            "",
        ]
    )
    return "\n".join(lines)


def _head() -> str:
    from freeze import git

    return asyncio.run(git("rev-parse", "HEAD")).decode().strip()


def _require_stage_a_ancestor() -> None:
    from freeze import git

    asyncio.run(git("merge-base", "--is-ancestor", STAGE_A, "HEAD"))


if __name__ == "__main__":
    if sys.argv[1:] != ["--execute"]:
        raise SystemExit("Use --execute exactly once; Stage B outputs are immutable.")
    print(json.dumps(execute(), sort_keys=True))
