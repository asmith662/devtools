# Copyright (c) 2026
# ruff: noqa: ANN001, ANN201, ARG001, C901, D103, E501, EM101, EM102, INP001, PERF401, PLR0911, PLR0912, PLR2004, PLR0913, PLR0917, T201, TRY003
"""Execute the frozen Case 0008 treatment with durable native checkpoints."""

from __future__ import annotations

import argparse
import asyncio
import dataclasses
import enum
import gzip
import hashlib
import json
import os
import pickle
import platform
import sys
import time
import traceback
import uuid
from collections import Counter
from pathlib import Path

import freeze

from devtools.context.localization.association import (
    WitnessHypothesisFamilyIdentity,
    WitnessHypothesisIdentity,
)
from devtools.context.localization.association.structural import (
    validate_structural_support,
)
from devtools.context.localization.generation import (
    BranchingGroundedMemberRecipe,
    GroundedMemberRecipe,
    ProjectionKind,
    WitnessGenerationPlan,
    WitnessGenerationRecipe,
    generate_witness_hypotheses,
)
from devtools.context.localization.grounding import (
    ground_task_anchor,
)
from devtools.context.localization.identity import TaskProvenance
from devtools.context.localization.lexical import acquire_localization_lexical_evidence
from devtools.context.localization.routing import route_localization_lexical_evidence

CASE = freeze.CASE
STAGE_A_COMMIT = "3eda8c6027f72a51109ed78f5684a6bbb59c65bd"
START_MARKER = CASE / "execution_started.json"
RAW = CASE / "stage_b_raw.pkl.gz"
RECOVERY_RAW = CASE / "stage_b_generation_recovery_raw.pkl.gz"
RECOVERY_ID = "case-0008-stage-b-generation-recovery-1"
ORIGINAL_EXECUTION_ID = "2fed596a-f43d-4d35-9e32-e8a609366a6f"
INITIAL_RECOVERY_RAW_SHA256 = (
    "6ca629c93233493d0cd701544297b0175ab4f9fdb7917bada75d0367f90963e2"
)
CANONICAL = (
    "capture.pkl.gz",
    "retrieval.json",
    "routing.json",
    "grounding.json",
    "generation.json",
    "stage_b_integrity.json",
    "stage_b.md",
)
GROUNDING_IDS = (
    "g-assessment",
    "g-candidate",
    "g-generation",
    "g-grounding",
    "g-witness-set",
    "g-supported-witness",
    "g-task",
    "g-obligation",
    "g-readiness",
    "g-evidence",
    "g-package",
)


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def durable_raw(state: dict) -> str:
    """Atomically replace the resumable native checkpoint with flushed bytes."""
    payload = gzip.compress(
        pickle.dumps(state, protocol=pickle.HIGHEST_PROTOCOL),
        mtime=0,
    )
    temporary = RAW.with_name(RAW.name + ".tmp-" + uuid.uuid4().hex)
    with temporary.open("xb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(RAW)
    return digest(payload)


def load_raw() -> dict:
    """Load only the case-owned native checkpoint after its marker is checked."""
    marker = json.loads(freeze.binary(START_MARKER))
    raw = freeze.binary(RAW)
    state = pickle.loads(gzip.decompress(raw))  # noqa: S301
    if state["execution_id"] != marker["execution_id"]:
        raise ValueError("Raw checkpoint execution identity differs from marker.")
    if state["stage"] == "IN_PROGRESS":
        raise RuntimeError(
            "An operation has ambiguous in-progress state; never rerun it.",
        )
    return state


def recover_known_preinvocation_failure(name: str, explanation: str) -> None:
    """Reopen only a call proven unentered by zero invocation/result evidence."""
    if not START_MARKER.exists() or not RAW.exists() or not explanation.strip():
        raise ValueError("Cannot establish a marked pre-invocation recovery state.")
    marker = json.loads(freeze.binary(START_MARKER))
    state = pickle.loads(gzip.decompress(freeze.binary(RAW)))  # noqa: S301
    status = state["operations"].get(name)
    if (
        state["execution_id"] != marker["execution_id"]
        or status is None
        or status["state"] != "IN_PROGRESS"
        or status["invocations"] != 0
        or name in state["results"]
    ):
        raise RuntimeError(
            "State does not prove the operation was never invoked/returned.",
        )
    status["state"] = "NOT_STARTED"
    status["pre_invocation_failure"] = explanation
    state["stage"] = state_for(state)
    durable_raw(state)


def begin_operation(state: dict, name: str) -> None:
    status = state["operations"].get(name)
    if status is None:
        raise ValueError("Unknown operation identity.")
    if status["state"] == "CAPTURED":
        return
    if status["state"] != "NOT_STARTED":
        raise RuntimeError(
            "Operation state is ambiguous; no automatic retry is allowed.",
        )
    status["state"] = "IN_PROGRESS"
    state["stage"] = "IN_PROGRESS"
    durable_raw(state)


def capture_operation(state: dict, name: str, value: object, started: float) -> None:
    """Make a production return durable before any inspection or transformation."""
    state["results"][name] = value
    state["operations"][name]["state"] = "CAPTURED"
    state["operations"][name]["seconds"] = time.perf_counter() - started
    state["operations"][name]["invocations"] += 1
    state["stage"] = state_for(state)
    durable_raw(state)


def state_for(state: dict) -> str:
    names = tuple(state["operations"])
    captured = [state["operations"][name]["state"] == "CAPTURED" for name in names]
    if all(captured):
        return "GENERATION_CAPTURED"
    if (
        names[-1] == "generation"
        and state["operations"]["generation"]["state"] == "CAPTURED"
    ):
        return "GENERATION_CAPTURED"
    if state["operations"]["generation"]["state"] == "NOT_STARTED":
        grounds = [name for name in names if name.startswith("grounding:")]
        if all(state["operations"][name]["state"] == "CAPTURED" for name in grounds):
            return "GROUNDING_COMPLETE"
        if any(state["operations"][name]["state"] == "CAPTURED" for name in grounds):
            return "PARTIAL_GROUNDING_CAPTURED"
    if state["operations"].get("routing", {}).get("state") == "CAPTURED":
        return "ROUTING_CAPTURED"
    if state["operations"].get("lexical", {}).get("state") == "CAPTURED":
        return "LEXICAL_CAPTURED"
    return "NOT_STARTED"


def make_recipes(treatment: dict, groundings: dict):
    obligations = {
        item.identity.value: item.identity for item in groundings["task"].obligations
    }
    recipes = []
    for specification in treatment["recipes"]:
        obligation = obligations[specification["obligation"]]
        identity_type = (
            WitnessHypothesisFamilyIdentity
            if specification["kind"] == "family"
            else WitnessHypothesisIdentity
        )
        identity = identity_type(obligation, specification["id"])
        members = []
        for member in specification["members"]:
            grounding = groundings[member["grounding"]]
            common = {
                "key": member["key"],
                "grounding": grounding,
                "projection": ProjectionKind[member["projection"]],
                "reason": member["reason"],
                "provenance": TaskProvenance(specification["provenance"]),
            }
            members.append(
                BranchingGroundedMemberRecipe(
                    **common,
                    max_results=member["max_results"],
                )
                if member["multiplicity"] == "branching"
                else GroundedMemberRecipe(**common),
            )
        recipes.append(
            WitnessGenerationRecipe(
                identity,
                tuple(members),
                TaskProvenance(specification["provenance"]),
            ),
        )
    return tuple(recipes)


def runtime_identity(manifest: dict) -> dict:
    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "packages": manifest["runtime"]["packages"],
        "uv_lock_sha256": manifest["runtime"]["uv_lock_sha256"],
        "pyproject_sha256": manifest["runtime"]["pyproject_sha256"],
    }


def initialize() -> tuple[dict, dict, dict]:
    if START_MARKER.exists():
        raise FileExistsError(
            "Stage B marker exists; inspect recovery state, do not start a new execution.",
        )
    if RAW.exists() or any((CASE / name).exists() for name in CANONICAL):
        raise FileExistsError(
            "Stage B output exists without a fresh start; inspect before proceeding.",
        )
    manifest = json.loads(freeze.binary(CASE / "pre_execution.json"))
    treatment = json.loads(freeze.binary(CASE / "treatment.json"))
    native = pickle.loads(gzip.decompress(freeze.binary(CASE / "inputs.pkl.gz")))  # noqa: S301
    if tuple(key for key, _ in native["grounding_requests"]) != GROUNDING_IDS:
        raise ValueError("Frozen grounding request identities differ.")
    execution_id = str(uuid.uuid4())
    marker = {
        "schema": "case-0008-execution-start-v1",
        "case": CASE.name,
        "stage_a_commit": STAGE_A_COMMIT,
        "treatment_sha256": manifest["treatment_sha256"],
        "stage_a_archive_sha256": manifest["inputs_sha256"],
        "stage_a_integrity_sha256": digest(freeze.binary(CASE / "integrity.json")),
        "repository_id": manifest["repository_id"],
        "snapshot_id": manifest["snapshot_id"],
        "execution_id": execution_id,
        "runtime": runtime_identity(manifest),
    }
    freeze.put_text(START_MARKER, freeze.json_bytes(marker).decode())
    operations = {
        name: {"state": "NOT_STARTED", "invocations": 0}
        for name in (
            "lexical",
            "routing",
            *(f"grounding:{key}" for key in GROUNDING_IDS),
            "generation",
        )
    }
    state = {
        "schema": "case-0008-stage-b-raw-v1",
        "case": CASE.name,
        "execution_id": execution_id,
        "stage": "NOT_STARTED",
        "operations": operations,
        "results": {},
        "bindings": None,
        "binding_failures": [],
    }
    durable_raw(state)
    return state, native, treatment


def run_operation(state: dict, name: str, operation) -> None:
    if state["operations"][name]["state"] == "CAPTURED":
        return
    begin_operation(state, name)
    started = time.perf_counter()
    result = operation()
    capture_operation(state, name, result, started)


def execute() -> dict:
    if START_MARKER.exists():
        raise FileExistsError(
            "Execution marker already exists; run resume or inspect recovery.",
        )
    freeze.validate()
    if asyncio.run(freeze.git("rev-parse", "HEAD")).decode().strip() != STAGE_A_COMMIT:
        raise ValueError("Stage A commit differs; treatment must not start.")
    if asyncio.run(freeze.git("branch", "--show-current")).decode().strip() != "main":
        raise ValueError("Stage B requires the frozen main branch.")
    if asyncio.run(freeze.git("status", "--porcelain", "--untracked-files=no")):
        raise ValueError("Tracked worktree/index changed after Stage A.")
    state, native, treatment = initialize()
    return advance(state, native, treatment)


def advance(state: dict, native: dict, treatment: dict) -> dict:
    if state["operations"]["generation"]["state"] == "IN_PROGRESS":
        raise RuntimeError(
            "Generation is ambiguous; use the separately authorized recovery.",
        )
    if state["operations"]["lexical"]["state"] == "NOT_STARTED":
        run_operation(
            state,
            "lexical",
            lambda: acquire_localization_lexical_evidence(native["request"]),
        )
    if state["operations"]["routing"]["state"] == "NOT_STARTED":
        run_operation(
            state,
            "routing",
            lambda: route_localization_lexical_evidence(
                state["results"]["lexical"],
                native["role_evidence"],
                native["preferences"],
            ),
        )
    groundings = {"task": native["request"].task}
    for key, request in native["grounding_requests"]:
        name = f"grounding:{key}"
        if state["operations"][name]["state"] == "NOT_STARTED":
            run_operation(
                state,
                name,
                lambda request=request: ground_task_anchor(
                    task=native["request"].task,
                    snapshot=native["request"].snapshot,
                    request=request,
                    module_universe=native["module_universe"],
                ),
            )
        groundings[key] = state["results"][name]
    if state["operations"]["generation"]["state"] == "NOT_STARTED":
        recipes = make_recipes(treatment, groundings)
        plan = WitnessGenerationPlan(
            task=native["request"].task,
            snapshot=native["request"].snapshot,
            recipes=recipes,
            acquisition=state["results"]["lexical"],
            role_evidence=state["results"]["routing"].role_evidence,
            routing=state["results"]["routing"],
            python_references=native["python_references"],
            python_import_dependencies=native["python_import_dependencies"],
        )
        state["bindings"] = plan
        validate_plan_aliases(plan, state["results"]["routing"])
        state["stage"] = "GROUNDING_COMPLETE"
        durable_raw(state)
        run_operation(state, "generation", lambda: generate_witness_hypotheses(plan))
    state["stage"] = "GENERATION_CAPTURED"
    durable_raw(state)
    validate_generation(state, native, treatment)
    finalize(state, native, treatment)
    return summarize(state)


def validate_plan_aliases(plan, routing_view) -> None:
    """Check only production's deliberate shared-instance associations."""
    if (
        plan.routing is not routing_view
        or plan.acquisition is not routing_view.acquisition
        or plan.role_evidence is not routing_view.role_evidence
        or routing_view.global_retrieval is not plan.acquisition.full_task_retrieval
    ):
        raise ValueError("Recovery plan does not preserve routing input aliases.")


def make_recovery_plan(state: dict, native: dict, treatment: dict):
    """Bind the frozen recipes to captured values without executing treatment."""
    if state["execution_id"] != ORIGINAL_EXECUTION_ID:
        raise ValueError("Recovery source execution identity differs.")
    if state["operations"]["generation"]["state"] != "IN_PROGRESS":
        raise ValueError("Attempt 1 does not retain the failed generation state.")
    if set(state["results"]) != {
        "lexical",
        "routing",
        *(f"grounding:{key}" for key in GROUNDING_IDS),
    }:
        raise ValueError("Captured upstream results are incomplete or unexpected.")
    groundings = {"task": native["request"].task}
    groundings.update(
        {key: state["results"][f"grounding:{key}"] for key in GROUNDING_IDS},
    )
    recipes = make_recipes(treatment, groundings)
    canonical_recipes = WitnessGenerationPlan(
        task=native["request"].task,
        snapshot=native["request"].snapshot,
        recipes=recipes,
    ).recipes
    if state["bindings"] is None or canonical_recipes != state["bindings"].recipes:
        raise ValueError("Recovery recipe bindings differ from frozen Attempt 1.")
    routing_view = state["results"]["routing"]
    plan = WitnessGenerationPlan(
        task=native["request"].task,
        snapshot=native["request"].snapshot,
        recipes=canonical_recipes,
        acquisition=routing_view.acquisition,
        role_evidence=routing_view.role_evidence,
        routing=routing_view,
        python_references=native["python_references"],
        python_import_dependencies=native["python_import_dependencies"],
    )
    validate_plan_aliases(plan, routing_view)
    return plan


def initial_recovery_state(attempt1: dict, plan) -> dict:
    """Create isolated recovery state while retaining the original attempt."""
    if RECOVERY_RAW.exists():
        raise FileExistsError("Generation recovery state already exists.")
    return {
        "schema": "case-0008-generation-recovery-v1",
        "case": CASE.name,
        "recovery_id": RECOVERY_ID,
        "original_execution_id": attempt1["execution_id"],
        "stage_a_commit": STAGE_A_COMMIT,
        "stage": "GENERATION_RECOVERY_AUTHORIZED",
        "prior_generation_attempts": 1,
        "upstream_source": str(RAW.name),
        "upstream_sha256": digest(RAW.read_bytes()),
        "generation_invocations": 0,
        "generation_attempted_calls": 0,
        "generation_state": "NOT_STARTED",
        "plan": plan,
        "generation_result": None,
        "history": [
            {
                "attempt": 1,
                "state": "GENERATION_ATTEMPT_1_FAILED_BEFORE_PROJECTION",
                "returned": False,
            },
            {"recovery_id": RECOVERY_ID, "state": "GENERATION_RECOVERY_AUTHORIZED"},
        ],
    }


def durable_recovery(state: dict) -> str:
    payload = gzip.compress(
        pickle.dumps(state, protocol=pickle.HIGHEST_PROTOCOL),
        mtime=0,
    )
    temporary = RECOVERY_RAW.with_name(RECOVERY_RAW.name + ".tmp-" + uuid.uuid4().hex)
    with temporary.open("xb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(RECOVERY_RAW)
    return digest(payload)


def record_recovery_generation(state: dict, operation, post_validate) -> object:
    """Consume the one recovery call and durably retain any returned view."""
    validate_recovery_checkpoint(state)
    if (
        state["generation_state"] != "NOT_STARTED"
        or state["generation_invocations"]
        or state.get("generation_attempted_calls", 0)
    ):
        raise RuntimeError("The single generation recovery allowance is exhausted.")
    state["generation_attempted_calls"] = 1
    state["generation_state"] = "GENERATION_RECOVERY_IN_PROGRESS"
    state["stage"] = "GENERATION_RECOVERY_IN_PROGRESS"
    durable_recovery(state)
    started = time.perf_counter()
    try:
        result = operation()
    except BaseException as error:
        state["generation_state"] = "GENERATION_RECOVERY_FAILED"
        state["stage"] = "CAPTURE_FAILED"
        state["generation_error"] = {
            "type": type(error).__name__,
            "message": str(error),
            "traceback": traceback.format_exc(),
        }
        state["history"].append(
            {
                "state": "GENERATION_RECOVERY_FAILED",
                "type": type(error).__name__,
                "message": str(error),
            },
        )
        durable_recovery(state)
        raise
    state["generation_result"] = result
    state["generation_state"] = "GENERATION_RETURN_CAPTURED_UNVALIDATED"
    state["stage"] = "GENERATION_RETURN_CAPTURED_UNVALIDATED"
    state["generation_invocations"] = 1
    state["generation_seconds"] = time.perf_counter() - started
    state["history"].append(
        {
            "state": "GENERATION_RETURN_CAPTURED_UNVALIDATED",
            "successful_return": 1,
        },
    )
    durable_recovery(state)
    post_validate(result)
    state["generation_state"] = "GENERATION_RECOVERY_VALIDATED"
    state["stage"] = "GENERATION_RECOVERY_VALIDATED"
    durable_recovery(state)
    return result


def validate_partial_checkpoint(*, allow_canonical: bool = False) -> tuple[dict, dict]:
    """Verify immutable Attempt 1 bytes and the single-call authorization."""
    attempt_path = CASE / "stage_b_attempt_1.json"
    authorization_path = CASE / "recovery_authorization.json"
    attempt = json.loads(attempt_path.read_bytes())
    authorization = json.loads(authorization_path.read_bytes())
    raw_bytes = RAW.read_bytes()
    marker_bytes = START_MARKER.read_bytes()
    if digest(raw_bytes) != attempt["raw_sha256"]:
        raise ValueError("Attempt 1 raw checkpoint digest differs.")
    if digest(marker_bytes) != attempt["start_marker_sha256"]:
        raise ValueError("Attempt 1 execution marker digest differs.")
    if (
        attempt["status"] != "PARTIAL STAGE B — NOT CANONICAL"
        or attempt["generation_status"] != "GENERATION NOT CAPTURED"
        or attempt["adjudication_status"] != "NOT ADJUDICATED"
        or attempt["generation_attempt"]["combined_api_attempted"] != 1
        or attempt["generation_attempt"]["returned_successfully"]
        or attempt["generation_attempt"]["structural_projection_reached"]
    ):
        raise ValueError("Attempt 1 audit record differs from observed failure.")
    if (
        digest(freeze.binary(CASE / "inputs.pkl.gz"))
        != authorization["stage_a_archive_sha256"]
    ):
        raise ValueError("Frozen Stage A archive digest differs.")
    marker = json.loads(marker_bytes)
    raw = pickle.loads(gzip.decompress(raw_bytes))  # noqa: S301
    if (
        marker["execution_id"] != ORIGINAL_EXECUTION_ID
        or raw["execution_id"] != ORIGINAL_EXECUTION_ID
        or marker["stage_a_commit"] != STAGE_A_COMMIT
        or authorization["original_execution_id"] != ORIGINAL_EXECUTION_ID
        or authorization["recovery_id"] != RECOVERY_ID
        or raw["operations"]["generation"]["state"] != "IN_PROGRESS"
        or raw["operations"]["generation"]["invocations"] != 0
    ):
        raise ValueError("Attempt 1 identity/state differs from recovery protocol.")
    expected_operations = {
        "lexical": 1,
        "routing": 1,
        **{f"grounding:{key}": 1 for key in GROUNDING_IDS},
    }
    if any(
        raw["operations"].get(name, {}).get("state") != "CAPTURED"
        or raw["operations"][name]["invocations"] != count
        for name, count in expected_operations.items()
    ):
        raise ValueError("Captured upstream treatment counts differ.")
    allowance = authorization["allowance"]
    if allowance != {
        "additional_lexical_executions": 0,
        "additional_routing_executions": 0,
        "additional_grounding_executions": 0,
        "additional_combined_generation_api_executions": 1,
        "other_treatment_operations": 0,
    }:
        raise ValueError("Recovery authorization exceeds the frozen allowance.")
    if not allow_canonical and any((CASE / name).exists() for name in CANONICAL):
        raise ValueError("Canonical Stage B output exists for a partial attempt.")
    return raw, authorization


def validate_recovery_checkpoint(state: dict) -> None:
    """Reject recovery state that changes its upstream or spends allowance."""
    _, authorization = validate_partial_checkpoint(allow_canonical=True)
    if (
        state["recovery_id"] != RECOVERY_ID
        or state["original_execution_id"] != ORIGINAL_EXECUTION_ID
        or state["upstream_sha256"] != authorization["raw_sha256"]
        or state["generation_invocations"] not in (0, 1)
        or state.get("generation_attempted_calls", 0) not in (0, 1)
        or state["prior_generation_attempts"] != 1
    ):
        raise ValueError("Generation recovery checkpoint differs from authorization.")
    validate_plan_aliases(state["plan"], state["plan"].routing)


def recovered_execution_state(original: dict, plan, view, recovery_state: dict) -> dict:
    """Join captured upstream values with the durably returned generation view."""
    result = dict(original)
    result["stage"] = "GENERATION_RECOVERY_CAPTURED"
    result["execution_kind"] = "GENERATION_RECOVERY"
    result["recovery_id"] = RECOVERY_ID
    result["operations"] = {
        name: dict(value) for name, value in original["operations"].items()
    }
    result["operations"]["generation"] = {
        "state": "CAPTURED",
        "invocations": 1,
        "seconds": recovery_state["generation_seconds"],
        "prior_failed_attempts": 1,
    }
    result["results"] = dict(original["results"])
    result["results"]["lexical"] = plan.acquisition
    result["results"]["routing"] = plan.routing
    result["results"]["generation"] = view
    result["bindings"] = plan
    if not all(
        (
            plan.routing is result["results"]["routing"],
            plan.acquisition is plan.routing.acquisition,
            plan.role_evidence is plan.routing.role_evidence,
            plan.routing.global_retrieval is plan.acquisition.full_task_retrieval,
            view.plan is plan,
            view.association.routing is plan.routing,
            view.association.acquisition is plan.acquisition,
            view.association.role_evidence is plan.role_evidence,
        ),
    ):
        raise ValueError("Recovered execution state lost required object aliases.")
    return result


def validate_recovered_generation(state: dict, native: dict, treatment: dict) -> None:
    """Replay exact target/support origins after the native result is durable."""
    plan = state["bindings"]
    view = state["results"]["generation"]
    validate_plan_aliases(plan, state["results"]["routing"])
    validate_generation(state, native, treatment)
    if (
        len(plan.recipes) != 29
        or sum(
            isinstance(item.recipe.identity, WitnessHypothesisFamilyIdentity)
            for item in view.attempts
        )
        != 14
        or sum(
            not isinstance(item.recipe.identity, WitnessHypothesisFamilyIdentity)
            for item in view.attempts
        )
        != 15
    ):
        raise ValueError("Recovered recipe/family count differs from frozen specs.")
    for attempt in view.attempts:
        for member_attempt in attempt.members:
            for projected in member_attempt.projections:
                if (
                    native["request"].snapshot.resource_at(
                        projected.target.address,
                    )
                    != projected.target
                ):
                    raise ValueError("Recovered target is outside frozen snapshot.")
                for support in projected.structural:
                    validate_structural_support(
                        task=plan.task,
                        snapshot=plan.snapshot,
                        target=projected.target,
                        support=support,
                    )
    acquisition = plan.acquisition
    routing = plan.routing
    if (
        len(acquisition.obligation_retrievals) != 13
        or len(routing.obligation_lanes) != 13
        or routing.global_retrieval is not acquisition.full_task_retrieval
    ):
        raise ValueError("Captured lexical/routing lane correspondence differs.")
    for lane in routing.obligation_lanes:
        native_lane = next(
            (
                item
                for item in acquisition.obligation_retrievals
                if item.request.identity == lane.preference.query
                and item.request.obligation == lane.preference.obligation
            ),
            None,
        )
        if native_lane is None or len(lane.candidates) != len(
            native_lane.retrieval.matches,
        ):
            raise ValueError("Routed lane lost a native lexical candidate.")
        expected_ranks = set(range(1, len(native_lane.retrieval.matches) + 1))
        observed_ranks = {item.native_rank for item in lane.candidates}
        if observed_ranks != expected_ranks:
            raise ValueError("Routed lane lost native candidate ranks.")
        if any(
            not (1 <= item.native_rank <= len(native_lane.retrieval.matches))
            or native_lane.retrieval.matches[item.native_rank - 1] is not item.match
            for item in lane.candidates
        ):
            raise ValueError("Routed candidate is not its exact native match object.")
        tier_order: dict[str, list[int]] = {}
        for candidate in lane.candidates:
            tier_order.setdefault(candidate.tier.name, []).append(
                candidate.native_rank,
            )
        if any(ranks != sorted(ranks) for ranks in tier_order.values()):
            raise ValueError("Routed within-tier native ordering changed.")


def execute_generation_recovery() -> dict:
    """Run the only authorized combined generation API call, at most once."""
    freeze.validate(allow_stage_b=True)
    original, _ = validate_partial_checkpoint()
    recovery = pickle.loads(gzip.decompress(freeze.binary(RECOVERY_RAW)))  # noqa: S301
    validate_recovery_checkpoint(recovery)
    if (
        recovery["generation_state"] == "NOT_STARTED"
        and digest(freeze.binary(RECOVERY_RAW)) != INITIAL_RECOVERY_RAW_SHA256
    ):
        raise ValueError("Unstarted recovery raw digest differs from authorization.")
    if recovery["stage"] == "CANONICAL_COMPLETE":
        verify_recovery_canonical(recovery)
        return {"stage": recovery["stage"], "generation_calls": 1}
    if recovery["generation_state"] != "NOT_STARTED":
        if recovery["generation_state"] == "GENERATION_RETURN_CAPTURED_UNVALIDATED":
            return finalize_captured_recovery(original, recovery)
        raise RuntimeError(
            "The generation recovery allowance is consumed or ambiguous; do not rerun.",
        )
    native = pickle.loads(gzip.decompress(freeze.binary(CASE / "inputs.pkl.gz")))  # noqa: S301
    treatment = json.loads(freeze.binary(CASE / "treatment.json"))
    plan = make_recovery_plan(original, native, treatment)
    retained_plan = recovery["plan"]
    if (
        plan.recipes != retained_plan.recipes
        or plan.task.identity != retained_plan.task.identity
        or plan.snapshot.repository_id != retained_plan.snapshot.repository_id
        or plan.snapshot.id != retained_plan.snapshot.id
        or len(plan.python_references.sources)
        != len(retained_plan.python_references.sources)
        or len(plan.python_import_dependencies.sources)
        != len(retained_plan.python_import_dependencies.sources)
    ):
        raise ValueError(
            "Reconstructed recovery plan differs from its preflight state.",
        )
    validate_plan_aliases(plan, original["results"]["routing"])
    recovery["plan"] = plan
    durable_recovery(recovery)
    merged: dict = {}

    def validate_return(view) -> None:
        merged_state = recovered_execution_state(original, plan, view, recovery)
        validate_recovered_generation(merged_state, native, treatment)
        merged["state"] = merged_state

    result = record_recovery_generation(
        recovery,
        lambda: generate_witness_hypotheses(plan),
        validate_return,
    )
    if (
        merged.get("state") is None
        or merged["state"]["results"]["generation"] is not result
    ):
        raise ValueError(
            "Recovered generation return was not joined to captured state.",
        )
    finalize(merged["state"], native, treatment, recovery_state=recovery)
    verify_recovery_canonical(recovery)
    return {
        "stage": recovery["stage"],
        "execution_id": ORIGINAL_EXECUTION_ID,
        "recovery_id": RECOVERY_ID,
        "generation_calls": recovery["generation_attempted_calls"],
        "generation_seconds": recovery["generation_seconds"],
        "canonical_digests": recovery["canonical_digests"],
    }


def finalize_captured_recovery(original: dict, recovery: dict) -> dict:
    """Resume validation/finalization from a durable generation return."""
    native = pickle.loads(gzip.decompress(freeze.binary(CASE / "inputs.pkl.gz")))  # noqa: S301
    treatment = json.loads(freeze.binary(CASE / "treatment.json"))
    state = recovered_execution_state(
        original,
        recovery["plan"],
        recovery["generation_result"],
        recovery,
    )
    validate_recovered_generation(state, native, treatment)
    recovery["stage"] = "GENERATION_RECOVERY_VALIDATED"
    durable_recovery(recovery)
    finalize(state, native, treatment, recovery_state=recovery)
    verify_recovery_canonical(recovery)
    return {"stage": recovery["stage"], "generation_calls": 1}


def verify_recovery_canonical(recovery: dict) -> bool:
    """Read-only canonical reentry check; never invokes a treatment operation."""
    validate_partial_checkpoint(allow_canonical=True)
    if (
        recovery["stage"] != "CANONICAL_COMPLETE"
        or recovery["generation_state"] != "GENERATION_RECOVERY_VALIDATED"
        or recovery["generation_attempted_calls"] != 1
        or recovery["generation_invocations"] != 1
    ):
        raise ValueError("Canonical recovery invocation history is incomplete.")
    validate_plan_aliases(recovery["plan"], recovery["plan"].routing)
    for name, expected in recovery["canonical_digests"].items():
        if digest(freeze.binary(CASE / name)) != expected:
            raise ValueError(f"Canonical recovery artifact digest differs: {name}")
    return True


def load_recovery_state() -> dict:
    return pickle.loads(gzip.decompress(freeze.binary(RECOVERY_RAW)))  # noqa: S301


def resume_recovery() -> dict:
    """Finalize only a captured generation return; never enter generation."""
    recovery = load_recovery_state()
    validate_recovery_checkpoint(recovery)
    if recovery["stage"] == "CANONICAL_COMPLETE":
        verify_recovery_canonical(recovery)
        return {"stage": recovery["stage"], "generation_calls": 1}
    if recovery["generation_state"] != "GENERATION_RETURN_CAPTURED_UNVALIDATED":
        raise RuntimeError("No durable generation return is available to resume.")
    original, _ = validate_partial_checkpoint()
    return finalize_captured_recovery(original, recovery)


def validate_generation(state: dict, native: dict, treatment: dict) -> None:
    view = state["results"]["generation"]
    if (
        len(view.attempts) != len(treatment["recipes"])
        or state["bindings"] != view.plan
    ):
        raise ValueError("Generation attempt/spec correspondence differs.")
    expected = {(item["obligation"], item["id"]): item for item in treatment["recipes"]}
    observed = {
        (item.recipe.identity.obligation.value, item.recipe.identity.value): item
        for item in view.attempts
    }
    if set(observed) != set(expected):
        raise ValueError("Generation recipe identities differ from frozen specs.")
    for key, attempt in observed.items():
        spec = expected[key]
        if len(attempt.members) != len(spec["members"]):
            raise ValueError("Generation member count differs from frozen recipe.")
        actual_by_key = {member.recipe.key: member for member in attempt.members}
        for frozen in spec["members"]:
            actual = actual_by_key[frozen["key"]]
            if (
                actual.recipe.key,
                actual.recipe.projection.name,
                actual.recipe.grounding.request.locator,
            ) != (
                frozen["key"],
                frozen["projection"],
                dict(native["grounding_requests"])[frozen["grounding"]].locator,
            ):
                raise ValueError(
                    "Generation member binding differs from frozen treatment.",
                )
            for projected in actual.projections:
                if (
                    native["request"].snapshot.resource_at(projected.target.address)
                    != projected.target
                ):
                    raise ValueError("Generated target is outside exact Stage A frame.")
    if view.association.hypotheses != view.generated:
        raise ValueError("Generation hypotheses differ from validated association.")


def plain(value):
    """Convert selected native reporting values without expanding shared frames."""
    if isinstance(value, enum.Enum):
        return value.name
    if dataclasses.is_dataclass(value):
        return {
            field.name: plain(getattr(value, field.name))
            for field in dataclasses.fields(value)
        }
    if isinstance(value, dict):
        return {str(key): plain(item) for key, item in value.items()}
    if isinstance(value, (tuple, list, set, frozenset)):
        return [plain(item) for item in value]
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if hasattr(value, "value") and isinstance(value.value, (str, int)):
        return value.value
    return str(value)


def occurrence(resource) -> dict:
    return {
        "address": resource.address.value,
        "content_identity": resource.content_identity.value,
    }


def retrieval_lane(query_id, query_text, retrieval):
    rows = []
    for rank, match in enumerate(retrieval.matches, 1):
        document = match.document_statistics.analysis.document.resource
        rows.append(
            {
                "native_rank": rank,
                "resource": occurrence(document),
                "score": match.score,
                "content_score": match.content_score,
                "filename_score": match.filename_score,
                "filename_weight": match.filename_weight,
                "weighted_filename_score": match.weighted_filename_score,
                "term_contributions": plain(match.term_contributions),
                "filename_term_contributions": plain(match.filename_term_contributions),
            },
        )
    return {"query_identity": query_id, "query_text": query_text, "matches": rows}


def grounding_report(request_id, grounding):
    def referent(item) -> dict:
        value = item.referent
        row = {
            "type": type(value).__name__,
            "identity": getattr(value, "identity", None),
        }
        resource = getattr(value, "resource", None)
        if resource is None and hasattr(value, "support"):
            address = getattr(value.support, "resource_address", None)
            if address is not None:
                row["resource_address"] = address.value
        elif resource is not None:
            row["resource"] = occurrence(resource)
        subject = getattr(value, "subject", None)
        if subject is not None:
            row["subject_identity"] = getattr(subject, "identity", str(subject))
        return row

    return {
        "request_identity": request_id,
        "anchor": grounding.request.anchor.value,
        "locator": plain(grounding.request.locator),
        "disposition": grounding.disposition.name,
        "reason": grounding.reason,
        "resolver": grounding.resolver.name,
        "candidates": [
            {"referent": referent(item), "evidence_type": type(item.evidence).__name__}
            for item in grounding.candidates
        ],
        "native_evidence": [
            {"type": type(item).__name__, "identity": getattr(item, "identity", None)}
            for item in grounding.native_evidence
        ],
    }


def generation_report(view):
    attempts = []
    for item in view.attempts:
        recipe = item.recipe
        members = []
        for attempt in item.members:
            members.append(
                {
                    "key": attempt.recipe.key,
                    "projection": attempt.recipe.projection.name,
                    "grounding_anchor": attempt.recipe.grounding.request.anchor.value,
                    "grounding_locator": plain(
                        attempt.recipe.grounding.request.locator,
                    ),
                    "disposition": attempt.disposition.name,
                    "source_type": type(attempt.source).__name__
                    if attempt.source is not None
                    else None,
                    "source_identity": getattr(attempt.source, "identity", None),
                    "complete": attempt.complete,
                    "work_performed": attempt.work_performed,
                    "work_limit": attempt.work_limit,
                    "result_limit": attempt.result_limit,
                    "result_count": attempt.result_count,
                    "failure_reason": attempt.failure_reason,
                    "uncovered_frontier": [
                        occurrence(resource) for resource in attempt.uncovered_frontier
                    ],
                    "targets": [
                        {
                            "resource": occurrence(target.target),
                            "support": [
                                support_report(support) for support in target.structural
                            ],
                        }
                        for target in attempt.projections
                    ],
                },
            )
        attempts.append(
            {
                "obligation": recipe.identity.obligation.value,
                "recipe_identity": recipe.identity.value,
                "recipe_kind": "family"
                if isinstance(recipe.identity, WitnessHypothesisFamilyIdentity)
                else "fixed",
                "disposition": item.disposition.name,
                "members": members,
                "branches": [
                    {
                        "identity": branch.identity.value,
                        "target": occurrence(branch.projection.target),
                        "disposition": branch.disposition.name,
                        "hypothesis_identity": branch.hypothesis.identity.value
                        if branch.hypothesis
                        else None,
                        "reason": branch.reason,
                    }
                    for branch in item.branches
                ],
            },
        )
    return {
        "attempts": attempts,
        "generated_hypotheses": [hypothesis_report(item) for item in view.generated],
    }


def support_report(support):
    result = {
        "operator_support_type": type(support).__name__,
        "grounding_anchor": support.grounding.request.anchor.value,
    }
    if hasattr(support, "correspondence"):
        result["correspondence_identity"] = support.correspondence.identity
        result["source"] = occurrence(support.correspondence.source)
        result["test"] = occurrence(support.correspondence.test)
    if hasattr(support, "references"):
        result["reference_fact_identities"] = [
            item.identity for item in support.references
        ]
        result["referencing_source"] = occurrence(
            support.source.analysis.derivation.dependency.resource,
        )
    if hasattr(support, "relations"):
        result["resolved_import_relation_identities"] = [
            item.identity for item in support.relations
        ]
        result["dependency_targets"] = [
            occurrence(item.target.resource) for item in support.relations
        ]
        result["source_module"] = support.source.module.identity
        result["source_analysis"] = support.source.analysis.derivation_identity
    if type(support).__name__ == "OwnerResourceSupport":
        result["referent_type"] = type(
            support.grounding.candidates[0].referent,
        ).__name__
    return result


def hypothesis_report(hypothesis):
    return {
        "identity": hypothesis.identity.value,
        "identity_type": type(hypothesis.identity).__name__,
        "obligation": hypothesis.identity.obligation.value,
        "members": [
            {
                "target": occurrence(member.target),
                "reason": member.reason,
                "lexical_supports": [
                    {
                        "query": item.query.value if item.query else None,
                        "native_rank": item.native_rank,
                    }
                    for item in member.lexical
                ],
                "role_supports": [item.role.name for item in member.roles],
                "routed_supports": [
                    {
                        "query": item.query.value,
                        "native_rank": item.candidate.native_rank,
                        "position": item.candidate.routed_position,
                        "tier": item.candidate.tier.name,
                    }
                    for item in member.routed
                ],
                "structural_supports": [
                    support_report(item) for item in member.structural
                ],
            }
            for member in hypothesis.members
        ],
    }


def finalize(state, native, treatment, recovery_state=None):
    recovery_metadata = (
        {
            "execution_kind": "GENERATION_RECOVERY",
            "original_execution_id": ORIGINAL_EXECUTION_ID,
            "recovery_id": RECOVERY_ID,
            "prior_generation_attempts": 1,
            "lexical_source": RAW.name,
            "routing_source": RAW.name,
            "grounding_source": RAW.name,
            "recovery_generation_invocations": 1,
            "recovery_generation_seconds": recovery_state["generation_seconds"],
        }
        if recovery_state is not None
        else None
    )
    acquisition = state["results"]["lexical"]
    routing = state["results"]["routing"]
    groundings = [state["results"][f"grounding:{key}"] for key in GROUNDING_IDS]
    generation = state["results"]["generation"]
    retrieval = {
        "global": retrieval_lane(
            None,
            acquisition.full_task_retrieval.query.text,
            acquisition.full_task_retrieval,
        ),
        "obligations": [
            retrieval_lane(
                lane.request.identity.value,
                lane.request.text,
                lane.retrieval,
            )
            for lane in acquisition.obligation_retrievals
        ],
    }
    if recovery_metadata is not None:
        retrieval["recovery_provenance"] = recovery_metadata
    routed = {
        "global_unchanged": retrieval_lane(
            None,
            routing.global_retrieval.query.text,
            routing.global_retrieval,
        ),
        "lanes": [
            {
                "query": lane.preference.query.value,
                "obligation": lane.preference.obligation.value,
                "preferred_roles": [
                    item.name for item in lane.preference.preferred_roles
                ],
                "candidates": [
                    {
                        "native_rank": item.native_rank,
                        "routed_position": item.routed_position,
                        "tier": item.tier.name,
                        "resource": occurrence(
                            item.match.document_statistics.analysis.document.resource,
                        ),
                        "score": item.match.score,
                        "role_evidence": [
                            {"role": evidence.role.name, "identity": evidence.identity}
                            for evidence in item.role_evidence
                        ],
                    }
                    for item in lane.candidates
                ],
            }
            for lane in routing.obligation_lanes
        ],
    }
    if recovery_metadata is not None:
        routed["recovery_provenance"] = recovery_metadata
    grounding_json = {
        "groundings": [
            grounding_report(key, item)
            for key, item in zip(GROUNDING_IDS, groundings, strict=True)
        ],
        "explicit_grounding_invocations": len(groundings),
        "disposition_counts": dict(
            Counter(item.disposition.name for item in groundings),
        ),
        "resolver_replay_invocations": "not exposed as a separate production counter; generation freshness validation may replay grounding",
    }
    if recovery_metadata is not None:
        grounding_json["recovery_provenance"] = recovery_metadata
    generation_json = generation_report(generation)
    if recovery_metadata is not None:
        generation_json["recovery_provenance"] = recovery_metadata
    raw_bytes = freeze.binary(RECOVERY_RAW if recovery_state is not None else RAW)
    capture_payload = gzip.compress(
        pickle.dumps(
            {
                "state": state,
                "native": native,
                "recovery_provenance": recovery_metadata,
            },
            protocol=pickle.HIGHEST_PROTOCOL,
        ),
        mtime=0,
    )
    put_binary_once(CASE / "capture.pkl.gz", capture_payload)
    for name, value in (
        ("retrieval.json", retrieval),
        ("routing.json", routed),
        ("grounding.json", grounding_json),
        ("generation.json", generation_json),
    ):
        put_text_once(CASE / name, freeze.json_bytes(value).decode())
    counts = mechanical_counts(generation)
    invocation_counts = {
        name: {"invocations": row["invocations"], "seconds": row.get("seconds", 0.0)}
        for name, row in state["operations"].items()
    }
    integrity = {
        "schema": "case-0008-stage-b-integrity-v1",
        "case": CASE.name,
        "stage_a_commit": STAGE_A_COMMIT,
        "execution_id": state["execution_id"],
        "stage_a_digests": json.loads(freeze.binary(CASE / "integrity.json"))["sha256"],
        "recovery_provenance": recovery_metadata,
        "artifacts": {
            name: digest(freeze.binary(CASE / name))
            for name in (
                "capture.pkl.gz",
                "retrieval.json",
                "routing.json",
                "grounding.json",
                "generation.json",
            )
        },
        "raw_checkpoint_before_canonicalization_sha256": digest(raw_bytes),
        "invocations": invocation_counts,
        "counts": counts,
        "correspondence": {
            "recipes": "29/29",
            "targets_in_snapshot": True,
            "generation_plan_equal_capture": True,
        },
    }
    put_text_once(
        CASE / "stage_b_integrity.json",
        freeze.json_bytes(integrity).decode(),
    )
    integrity["artifacts"]["stage_b_integrity.json"] = digest(
        freeze.binary(CASE / "stage_b_integrity.json"),
    )
    put_text_once(
        CASE / "stage_b.md",
        human_report(
            state,
            native,
            counts,
            invocation_counts,
            integrity["artifacts"],
            recovery_metadata,
        ),
    )
    state["stage"] = "CANONICAL_COMPLETE"
    state["canonical_digests"] = {
        name: digest(freeze.binary(CASE / name)) for name in CANONICAL
    }
    if recovery_state is not None:
        recovery_state["stage"] = "CANONICAL_COMPLETE"
        recovery_state["canonical_digests"] = state["canonical_digests"]
        recovery_state["history"].append({"state": "CANONICAL_COMPLETE"})
        durable_recovery(recovery_state)
    else:
        state["canonical_digests"][RAW.name] = digest(freeze.binary(RAW))
        durable_raw(state)


def put_binary(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())


def put_binary_once(path: Path, content: bytes) -> None:
    """Permit deterministic post-processing replay, refusing different bytes."""
    if path.exists():
        if freeze.binary(path) != content:
            raise ValueError(f"Existing canonical output differs: {path.name}")
        return
    put_binary(path, content)


def put_text_once(path: Path, content: str) -> None:
    encoded = content.replace("\r\n", "\n").encode()
    if path.exists():
        if freeze.binary(path) != encoded:
            raise ValueError(f"Existing canonical output differs: {path.name}")
        return
    freeze.put_text(path, content)


def mechanical_counts(view):
    cells = set()
    resources = set()
    operator_resources = {operator.name: set() for operator in ProjectionKind}
    operator_cells = {operator.name: set() for operator in ProjectionKind}
    support = Counter()
    fixed = sum(
        not isinstance(item.recipe.identity, WitnessHypothesisFamilyIdentity)
        for item in view.attempts
    )
    family_attempts = [
        item
        for item in view.attempts
        if isinstance(item.recipe.identity, WitnessHypothesisFamilyIdentity)
    ]
    family_counts = {}
    for item in view.attempts:
        for hypothesis in item.children:
            for member in hypothesis.members:
                resource = member.target.address.value
                resources.add(resource)
                cells.add((hypothesis.identity.obligation.value, resource))
                for structural in member.structural:
                    operator = {
                        "OwnerResourceSupport": "OWNER_RESOURCE",
                        "MirroredResourceSupport": "MIRRORED_RESOURCE",
                        "PythonReferenceResourceSupport": "REFERENCING_RESOURCE",
                        "PythonImportDependencyResourceSupport": "DIRECT_IMPORT_DEPENDENCY_RESOURCE",
                    }[type(structural).__name__]
                    operator_resources[operator].add(resource)
                    operator_cells[operator].add(
                        (hypothesis.identity.obligation.value, resource),
                    )
                support["members_with_global_lexical"] += bool(
                    any(item.query is None for item in member.lexical),
                )
                support["members_with_own_lexical"] += bool(
                    any(item.query is not None for item in member.lexical),
                )
                support["members_with_role"] += bool(member.roles)
                support["members_with_routed_preferred"] += bool(
                    any(
                        item.candidate.tier.name == "PREFERRED_ROLE_SUPPORTED"
                        for item in member.routed
                    ),
                )
                support["members_with_routed_escape"] += bool(
                    any(item.candidate.tier.name == "ESCAPE" for item in member.routed),
                )
                support["members_structural_only"] += not (
                    member.lexical or member.roles or member.routed
                )
    for item in family_attempts:
        operator = next(
            member.recipe.projection.name
            for member in item.members
            if isinstance(member.recipe, BranchingGroundedMemberRecipe)
        )
        family_counts.setdefault(operator, []).append(item)
    surfaces = {}
    owner = operator_resources["OWNER_RESOURCE"]
    mirror = operator_resources["MIRRORED_RESOURCE"]
    reference = operator_resources["REFERENCING_RESOURCE"]
    imports = operator_resources["DIRECT_IMPORT_DEPENDENCY_RESOURCE"]
    for name, group in (
        ("OWNER_MIRROR", owner | mirror),
        ("OWNER_MIRROR_REFERENCE", owner | mirror | reference),
        ("OWNER_MIRROR_IMPORT", owner | mirror | imports),
        ("ALL", owner | mirror | reference | imports),
    ):
        surfaces[name] = len(group)
    fixed_outcomes = Counter(
        item.disposition.name
        for item in view.attempts
        if not isinstance(item.recipe.identity, WitnessHypothesisFamilyIdentity)
    )
    return {
        "fixed_hypotheses": fixed,
        "fixed_outcomes": dict(fixed_outcomes),
        "branching_families": len(family_attempts),
        "branching_children": sum(len(item.branches) for item in family_attempts),
        "total_hypotheses": len(view.generated),
        "member_occurrences": sum(len(h.members) for h in view.generated),
        "unique_generated_resources": len(resources),
        "obligation_resource_cells": len(cells),
        "operator_unique_resources": {
            key: len(value) for key, value in operator_resources.items()
        },
        "operator_obligation_resource_cells": {
            key: len(value) for key, value in operator_cells.items()
        },
        "structural_unions": surfaces,
        "support_member_counts": dict(support),
        "family_outcomes": {
            key: summarize_families(value) for key, value in family_counts.items()
        },
    }


def summarize_families(items):
    result = Counter()
    fanout = []
    children = 0
    targets = set()
    fixed_collisions = 0
    duplicate_failures = 0
    for item in items:
        branch = next(
            member
            for member in item.members
            if isinstance(member.recipe, BranchingGroundedMemberRecipe)
        )
        result[item.disposition.name] += 1
        if branch.complete:
            fanout.append(branch.result_count or 0)
        children += sum(
            branch_result.hypothesis is not None for branch_result in item.branches
        )
        targets.update(target.target.address.value for target in branch.projections)
        owner_targets = {
            target.target.address.value
            for member in item.members
            if not isinstance(member.recipe, BranchingGroundedMemberRecipe)
            and member.recipe.projection is ProjectionKind.OWNER_RESOURCE
            for target in member.projections
        }
        fixed_collisions += sum(
            target.target.address.value in owner_targets
            for target in branch.projections
        )
        duplicate_failures += sum(
            branch_result.disposition.name == "DUPLICATE_TARGET"
            for branch_result in item.branches
        )
    ordered = sorted(fanout)
    median = (
        None
        if not ordered
        else ordered[len(ordered) // 2]
        if len(ordered) % 2
        else (ordered[len(ordered) // 2 - 1] + ordered[len(ordered) // 2]) / 2
    )
    return {
        "families": len(items),
        "dispositions": dict(result),
        "zero_target": sum(value == 0 for value in fanout),
        "one_target": sum(value == 1 for value in fanout),
        "several_targets": sum(value > 1 for value in fanout),
        "median_complete_fanout": median,
        "maximum_complete_fanout": max(fanout, default=0),
        "children": children,
        "unique_targets": len(targets),
        "fixed_owner_target_collisions": fixed_collisions,
        "duplicate_branch_failures": duplicate_failures,
        "work_overflow": result["WORK_BOUND_EXCEEDED"],
        "result_overflow": result["RESULT_BOUND_EXCEEDED"],
    }


def human_report(state, native, counts, invocations, digests, recovery_metadata=None):
    title = (
        "# Case 0008 Stage B — generation-only recovery"
        if recovery_metadata is not None
        else "# Case 0008 Stage B"
    )
    status = (
        "**CAPTURED VIA GENERATION-ONLY RECOVERY — NOT ADJUDICATED**"
        if recovery_metadata is not None
        else "**CAPTURED - NOT ADJUDICATED**"
    )
    lines = [
        title,
        "",
        status,
        "",
        f"Execution identity: `{state['execution_id']}`.",
        f"Repository / snapshot / corpus: `{native['request'].snapshot.repository_id}` / `{native['request'].snapshot.id}` / `{native['corpus'].id}`.",
        "",
        "## Invocation accounting",
        "",
    ]
    if recovery_metadata is not None:
        lines += [
            "Attempt 1 failed during candidate-association alias validation before any projection. The frozen recovery used the original durable lexical, routing, and grounding capture; none was rerun. One combined generation API call returned and was durably captured before correspondence validation and canonicalization.",
            f"Recovery identity: `{recovery_metadata['recovery_id']}`; prior failed attempts: 1; successful recovery call: 1 ({recovery_metadata['recovery_generation_seconds']:.6f}s).",
            "",
        ]
    lines.extend(
        f"- {key}: {value['invocations']} invocation(s), {value['seconds']:.6f}s"
        for key, value in invocations.items()
    )
    lines += [
        "",
        "## Mechanical generation counts",
        "",
        "```json",
        json.dumps(counts, indent=2, sort_keys=True),
        "```",
        "",
        "## Artifact digests",
        "",
    ]
    lines.extend(f"- {name}: `{value}`" for name, value in digests.items())
    lines += [
        "",
        "Treatment identities/specs were captured and mechanically joined. These are execution counts only; no candidate was labeled REQUIRED, helpful, unnecessary, complete, sufficient or effective.",
        "",
    ]
    return "\n".join(lines)


def summarize(state):
    return {
        "stage": state["stage"],
        "execution_id": state["execution_id"],
        "invocations": {
            key: value["invocations"] for key, value in state["operations"].items()
        },
        "digests": state.get("canonical_digests", {}),
    }


def resume() -> dict:
    freeze.validate(allow_stage_b=True)
    state = load_raw()
    native = pickle.loads(gzip.decompress(freeze.binary(CASE / "inputs.pkl.gz")))  # noqa: S301
    treatment = json.loads(freeze.binary(CASE / "treatment.json"))
    if state["stage"] == "CANONICAL_COMPLETE":
        verify_canonical(state)
        return summarize(state)
    if state["operations"]["generation"]["state"] == "CAPTURED":
        validate_generation(state, native, treatment)
        finalize(state, native, treatment)
        return summarize(state)
    return advance(state, native, treatment)


def verify_canonical(state):
    if state["stage"] != "CANONICAL_COMPLETE":
        raise ValueError("Canonical completion state missing.")
    for name, expected in state["canonical_digests"].items():
        if digest(freeze.binary(CASE / name)) != expected:
            raise ValueError(f"Canonical reentry digest differs: {name}")
    integrity = json.loads(freeze.binary(CASE / "stage_b_integrity.json"))
    for name in (
        "capture.pkl.gz",
        "retrieval.json",
        "routing.json",
        "grounding.json",
        "generation.json",
    ):
        if digest(freeze.binary(CASE / name)) != integrity["artifacts"][name]:
            raise ValueError(f"Integrity artifact digest differs: {name}")
    if (
        digest(freeze.binary(CASE / "stage_b_integrity.json"))
        != state["canonical_digests"]["stage_b_integrity.json"]
    ):
        raise ValueError("Stage B integrity digest differs.")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=(
            "execute",
            "resume",
            "verify",
            "recover-preinvocation",
            "recover-generation",
            "resume-recovery",
            "verify-recovery",
        ),
    )
    parser.add_argument("--operation")
    parser.add_argument("--explanation")
    args = parser.parse_args()
    if args.command == "recover-preinvocation":
        if args.operation != "lexical" or not args.explanation:
            parser.error(
                "Only the verified pre-call lexical name-resolution failure is recoverable here",
            )
        recover_known_preinvocation_failure(args.operation, args.explanation)
        print(json.dumps({"recovered": args.operation, "production_invocation": 0}))
        return
    if args.command == "recover-generation":
        print(json.dumps(execute_generation_recovery(), indent=2, sort_keys=True))
        return
    if args.command == "resume-recovery":
        print(json.dumps(resume_recovery(), indent=2, sort_keys=True))
        return
    if args.command == "verify-recovery":
        recovery = load_recovery_state()
        print(
            json.dumps(
                {"verified": verify_recovery_canonical(recovery)},
                indent=2,
                sort_keys=True,
            ),
        )
        return
    result = (
        execute()
        if args.command == "execute"
        else resume()
        if args.command == "resume"
        else verify_canonical(load_raw())
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
