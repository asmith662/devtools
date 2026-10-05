# Copyright (c) 2026
# ruff: noqa: ANN401, C409, C901, COM812, D103, E501, EM101, EM102, F401, F841, I001, PERF401, PLC0415, PLR0912, PLR0915, PLR2004, PTH105, S301, SIM102, TRY003, TRY301
"""Execute Case 0007 once with operation-level durable native checkpoints."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import pickle
import platform
import sys
import time
import uuid
from collections import Counter
from pathlib import Path
from statistics import median
from typing import Any

from devtools.context.localization.generation import (
    BranchingGroundedMemberRecipe,
    GroundedMemberRecipe,
    ProjectionKind,
    WitnessGenerationPlan,
    WitnessGenerationRecipe,
    generate_witness_hypotheses,
)
from devtools.context.localization.grounding import (
    AnchorGroundingDisposition,
    ground_task_anchor,
)
from devtools.context.localization.lexical import acquire_localization_lexical_evidence
from devtools.context.localization.routing import route_localization_lexical_evidence
from devtools.context.localization.association import (
    WitnessHypothesisFamilyIdentity,
    WitnessHypothesisIdentity,
)
from devtools.context.localization.association.references import (
    PythonReferenceResourceSupport,
    validate_reference_support,
)
from devtools.context.localization.association.structural import (
    MirroredResourceSupport,
    OwnerResourceSupport,
    owner_resource,
    validate_structural_support,
)
from devtools.context.localization.identity import LocalizationObligationIdentity
from experiments.codex_dogfood.case_0007 import freeze, treatment

CASE = Path(__file__).resolve().parent
STAGE_A_COMMIT = "e495c0af2cf57efa3a63016165b41cbba65d26a5"
RAW = CASE / "stage_b_raw.pkl.gz"
RAW_RECEIPT = CASE / "stage_b_raw.sha256"
START = CASE / "execution-start.json"
LOCK = CASE / ".stage_b.lock"
OUTPUTS = (
    "retrieval.json",
    "routing.json",
    "grounding.json",
    "generation.json",
    "capture.pkl.gz",
    "stage_b_integrity.json",
    "stage_b.md",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def artifact_digest(path: Path) -> str:
    """Hash text canonically across Git checkout newline conversion."""
    if path.suffix.lower() in {".json", ".md", ".py", ".sha256"}:
        return digest(freeze.text_bytes(path))
    return digest(path.read_bytes())


def json_write(path: Path, value: object) -> None:
    data = (
        json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    ).encode()
    if path.exists():
        if path.read_bytes() != data:
            raise FileExistsError(
                f"Refusing to overwrite different canonical output: {path.name}"
            )
        return
    exclusive_atomic(path, data, replace=False)


def exclusive_atomic(path: Path, data: bytes, *, replace: bool) -> None:
    """Durably write a same-directory temporary then atomically publish it."""
    temporary = path.with_name(path.name + f".{uuid.uuid4().hex}.tmp")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(temporary, flags, 0o600)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if not replace and path.exists():
            raise FileExistsError(path)
        os.replace(temporary, path)
        if hasattr(os, "O_DIRECTORY"):
            directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def save_raw(state: dict[str, Any]) -> str:
    if state.get("state") != "CANONICAL_STAGE_B_COMPLETE":
        state["raw_status"] = "INCOMPLETE_UNVALIDATED"
    state.pop("raw_sha256", None)
    payload = gzip.compress(pickle.dumps(state, protocol=5), mtime=0)
    exclusive_atomic(RAW, payload, replace=RAW.exists())
    checksum = digest(payload)
    exclusive_atomic(
        RAW_RECEIPT,
        f"{checksum}\n".encode(),
        replace=RAW_RECEIPT.exists(),
    )
    state["raw_sha256"] = checksum
    return checksum


def load_raw() -> dict[str, Any]:
    payload = RAW.read_bytes()
    if not RAW_RECEIPT.exists() or RAW_RECEIPT.read_text(
        encoding="ascii"
    ).strip() != digest(payload):
        raise ValueError("Raw checkpoint digest receipt is absent or invalid.")
    state = pickle.loads(gzip.decompress(payload))
    if state.get("stage_a_commit") != STAGE_A_COMMIT:
        raise ValueError("Raw checkpoint belongs to a different Stage A commit.")
    return state


def runtime() -> dict[str, str]:
    return {
        "python": sys.version,
        "implementation": sys.implementation.name,
        "platform": platform.platform(),
    }


def acquire_lock() -> Any:
    stream = LOCK.open("a+b")
    try:
        if os.name == "nt":
            import msvcrt

            stream.seek(0)
            if stream.read(1) == b"":
                stream.write(b"0")
                stream.flush()
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl

            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except (OSError, BlockingIOError):
        stream.close()
        raise RuntimeError("Another Stage B process owns the execution lock.") from None
    return stream


def verify_stage_a(*, initial: bool) -> tuple[dict[str, Any], dict[str, Any]]:
    """Check committed Stage A blobs and frozen identities without rebuilding inputs."""
    manifest = json.loads((CASE / "pre_retrieval.json").read_text(encoding="utf-8"))
    integrity = json.loads((CASE / "integrity.json").read_text(encoding="utf-8"))
    for name, expected in integrity["files"].items():
        current = (
            freeze.sha((CASE / name).read_bytes())
            if name.endswith(".gz")
            else freeze.sha(freeze.text_bytes(CASE / name))
        )
        if current != expected:
            raise ValueError(f"Stage A artifact drift: {name}")
    if (
        manifest["starting_head"] != treatment.STARTING_HEAD
        or manifest["case"] != treatment.CASE
    ):
        raise ValueError("Stage A identity mismatch.")
    if initial and await_git_head() != STAGE_A_COMMIT:
        raise ValueError(
            "Current HEAD is not the expected committed Stage A checkpoint."
        )
    committed_integrity = freeze.sha(
        (
            await_git_show(
                f"{STAGE_A_COMMIT}:experiments/codex_dogfood/case_0007/integrity.json"
            )
        ).encode()
    )
    if committed_integrity != freeze.sha((CASE / "integrity.json").read_bytes()):
        raise ValueError("Stage A integrity manifest differs from its committed blob.")
    if (
        manifest["repository_id"] != "fe2c8984-a021-4342-9e31-404a6cf07707"
        or manifest["snapshot_id"]
        != "404104e498a8d33118b52d5bad41c0ff4a8792d4ae23a2790628b796b91f34fd"
    ):
        raise ValueError("Frozen repository/snapshot mismatch.")
    archive = (CASE / "inputs.pkl.gz").read_bytes()
    if freeze.sha(archive) != manifest["inputs_archive_sha256"]:
        raise ValueError("Frozen input archive digest mismatch.")
    for name, expected in manifest["implementation_sha256"].items():
        if freeze.sha(freeze.text_bytes(Path(freeze.ROOT) / name)) != expected:
            raise ValueError(f"Frozen production implementation drift: {name}")
    inputs = pickle.loads(gzip.decompress(archive))
    if (
        len(inputs["lexical_request"].snapshot.resources) != 521
        or len(inputs["reference_request"].sources) != 407
    ):
        raise ValueError("Frozen native frame cardinality mismatch.")
    if initial:
        # The committed validator also verifies request/spec scope and operation tripwires.
        freeze.validate()
    return manifest, inputs


def await_git_head() -> str:
    import asyncio

    return asyncio.run(freeze.git("rev-parse", "HEAD")).strip()


def await_git_show(spec: str) -> str:
    """Read an exact committed Stage A blob through the bounded command owner."""
    import asyncio

    return asyncio.run(freeze.git("show", spec))


def id_value(value: Any) -> str:
    return str(getattr(value, "value", value))


def locator_json(locator: Any) -> dict[str, Any]:
    name = type(locator).__name__
    if name == "PythonDirectDeclarationLocator":
        return {
            "kind": name,
            "module": locator.module.dotted_name,
            "name": locator.declared_name,
            "declaration_kind": locator.kind.name,
        }
    if name == "PythonModuleLocator":
        return {
            "kind": name,
            "module": locator.dotted_name,
            "module_kind": locator.kind.name if locator.kind else None,
        }
    return {"kind": name, "address": str(locator.address)}


def resource_json(resource: Any) -> dict[str, Any]:
    return {
        "address": resource.address.value,
        "content_identity": resource.content_identity.value,
    }


def grounding_json(g: Any, key: str) -> dict[str, Any]:
    referents = []
    for candidate in g.candidates:
        ref = candidate.referent
        referents.append(
            {
                "type": type(ref).__name__,
                "identity": id_value(getattr(ref, "identity", "")),
                "resource": resource_json(ref.resource)
                if hasattr(ref, "resource")
                else None,
                "module": getattr(ref, "dotted_name", None),
                "name": getattr(ref, "declared_name", None),
            }
        )
    evidence = []
    for item in g.native_evidence:
        identity = getattr(item, "identity", None)
        derivation = getattr(item, "derivation", None)
        if identity is None and derivation is not None:
            identity = getattr(derivation, "identity", None)
        resource = getattr(item, "resource", None)
        evidence.append(
            {
                "type": type(item).__name__,
                "identity": str(identity) if identity is not None else None,
                "derivation_identity": (
                    str(getattr(derivation, "identity", ""))
                    if derivation is not None
                    else None
                ),
                "resource": resource_json(resource) if resource is not None else None,
            }
        )
    return {
        "request_identity": key,
        "anchor": g.request.anchor.value,
        "locator": locator_json(g.request.locator),
        "repository_id": str(g.request.repository_id),
        "snapshot_id": str(g.request.snapshot_id),
        "disposition": g.disposition.value,
        "reason": g.reason,
        "resolver": str(g.resolver),
        "provenance": {
            "source_identity": g.request.provenance.source_identity,
            "explanation": g.request.provenance.explanation,
        },
        "referents": referents,
        "native_provenance": evidence,
    }


def lane_json(identity: str, query: str, matches: tuple[Any, ...]) -> dict[str, Any]:
    rows = []
    for rank, match in enumerate(matches, 1):
        doc = match.document_statistics.analysis.document
        rows.append(
            {
                "native_rank": rank,
                "resource": resource_json(doc.resource),
                "score": match.score,
                "score_contributions": [
                    {
                        "term": x.normalized_term,
                        "contribution": x.contribution,
                    }
                    for x in match.term_contributions
                ],
                "filename_score_contributions": [
                    {
                        "term": x.normalized_term,
                        "contribution": x.contribution,
                    }
                    for x in match.filename_term_contributions
                ],
            }
        )
    return {"identity": identity, "query": query, "matches": rows}


def request_key(request: Any, requests: dict[str, Any]) -> str | None:
    return next((key for key, value in requests.items() if value == request), None)


def support_json(support: Any, requests: dict[str, Any]) -> dict[str, Any]:
    name = type(support).__name__
    grounding = getattr(support, "grounding", None)
    result: dict[str, Any] = {
        "type": name,
        "grounding_request": request_key(grounding.request, requests)
        if grounding
        else None,
    }
    if name == "PythonReferenceResourceSupport":
        result["reference_request"] = {
            "identity": support.request.identity,
            "work_limit": support.request.work_limit,
            "repository_id": str(support.request.module_universe.repository_id),
            "snapshot_id": str(support.grounding.request.snapshot_id),
        }
        result["source_analysis"] = str(support.source.analysis.derivation.identity)
        result["references"] = [
            {
                "identity": str(f.identity),
                "source_address": f.occurrence.resource_address.value,
                "source_span": {
                    "start_line": f.occurrence.source_range.start_line,
                    "start_column_utf8": f.occurrence.source_range.start_column_utf8,
                    "end_line": f.occurrence.source_range.end_line,
                    "end_column_utf8": f.occurrence.source_range.end_column_utf8,
                },
                "target_declaration": str(f.target_declaration.identity),
                "target_subject": str(f.target_subject.identity),
                "route": f.route.value,
                "import_declaration": (
                    {
                        "derivation_identity": f.import_declaration.derivation_identity,
                        "declaration_ordinal": f.import_declaration.declaration_ordinal,
                    }
                    if f.import_declaration
                    else None
                ),
                "module_resolution": f.module_resolution.identity
                if f.module_resolution
                else None,
                "direct_member_resolution": f.direct_member_resolution.identity
                if f.direct_member_resolution
                else None,
                "imported_member_resolution": f.imported_member_resolution.identity
                if f.imported_member_resolution
                else None,
                "direct_call": bool(f.direct_call),
                "resolution": "positive-exact-reference",
            }
            for f in support.references
        ]
    elif name == "MirroredResourceSupport":
        result["correspondence"] = support.correspondence.identity
        result["derivation"] = support.correspondence.derivation_identity
    return result


def target_json(p: Any, requests: dict[str, Any]) -> dict[str, Any]:
    return {
        "target": resource_json(p.target),
        "structural_support": [support_json(x, requests) for x in p.structural],
    }


def generation_json(view: Any, requests: dict[str, Any]) -> dict[str, Any]:
    attempts = []
    for a in view.attempts:
        members = []
        for m in a.members:
            members.append(
                {
                    "key": m.recipe.key,
                    "operator": m.recipe.projection.name,
                    "grounding_request": request_key(
                        m.recipe.grounding.request, requests
                    ),
                    "reason": m.recipe.reason,
                    "disposition": m.disposition.value,
                    "work_performed": m.work_performed,
                    "work_limit": m.work_limit,
                    "complete": m.complete,
                    "frontier": [resource_json(x) for x in m.uncovered_frontier],
                    "result_count": m.result_count,
                    "result_limit": m.result_limit,
                    "targets": [target_json(x, requests) for x in m.projections],
                    "failure_reason": m.failure_reason,
                }
            )
        branches = [
            {
                "identity": b.identity.value,
                "family": b.identity.family.value,
                "member": b.identity.member_key,
                "disposition": b.disposition.value,
                "target": target_json(b.projection, requests),
                "reason": b.reason,
                "hypothesis": b.hypothesis.identity.value if b.hypothesis else None,
            }
            for b in a.branches
        ]
        hypothesis = a.hypothesis
        attempts.append(
            {
                "identity": a.recipe.identity.value,
                "identity_kind": type(a.recipe.identity).__name__,
                "obligation": a.recipe.identity.obligation.value,
                "disposition": a.disposition.value,
                "provenance": {
                    "source_identity": a.recipe.provenance.source_identity,
                    "explanation": a.recipe.provenance.explanation,
                },
                "members": members,
                "branches": branches,
                "hypothesis": hypothesis.identity.value if hypothesis else None,
                "hypothesis_members": [
                    {
                        "target": resource_json(x.target),
                        "reason": x.reason,
                        "structural_support": [
                            support_json(s, requests) for s in x.structural
                        ],
                        "lexical_support_count": len(x.lexical),
                        "role_support_count": len(x.roles),
                        "routed_support_count": len(x.routed),
                    }
                    for x in hypothesis.members
                ]
                if hypothesis
                else [],
            }
        )
    return {"attempts": attempts}


def build_plan(
    inputs: dict[str, Any], treatment_state: dict[str, Any]
) -> tuple[WitnessGenerationPlan | None, list[dict[str, Any]]]:
    groundings = treatment_state["groundings"]
    requests = inputs["grounding_requests"]
    specs = inputs["recipe_specifications"]
    recipes = []
    binding = []
    for spec in specs:
        members = []
        failures = []
        for row in spec["members"]:
            g_id = row["grounding_request"]
            g = groundings.get(g_id)
            entry = {
                "recipe": spec["identity"],
                "member": row["key"],
                "grounding_request": g_id,
                "operator": row["operator"],
                "grounding_disposition": g.disposition.value if g else None,
            }
            if g is None:
                failures.append({**entry, "reason": "grounding result absent"})
                continue
            cls = (
                BranchingGroundedMemberRecipe
                if row["multiplicity"] == "branching"
                else GroundedMemberRecipe
            )
            kw = {
                "key": row["key"],
                "grounding": g,
                "projection": ProjectionKind[row["operator"]],
                "reason": row["reason"],
                "provenance": treatment.PROVENANCE,
            }
            member = cls(
                **kw,
                **(
                    {"max_results": row["max_results"]}
                    if cls is BranchingGroundedMemberRecipe
                    else {}
                ),
            )
            members.append(member)
            binding.append(entry)
        if failures:
            binding.extend(failures)
            continue
        oid = LocalizationObligationIdentity(treatment.TASK_ID, spec["obligation"])
        identity = (
            WitnessHypothesisFamilyIdentity(oid, spec["identity"])
            if spec["identity_kind"] == "family"
            else WitnessHypothesisIdentity(oid, spec["identity"])
        )
        recipes.append(
            WitnessGenerationRecipe(identity, tuple(members), treatment.PROVENANCE)
        )
    if not recipes:
        return None, binding
    plan = WitnessGenerationPlan(
        treatment.interpretation(),
        inputs["lexical_request"].snapshot,
        tuple(recipes),
        treatment_state["acquisition"],
        inputs["roles"],
        treatment_state.get("routing"),
        inputs["reference_request"],
    )
    return plan, binding


def operation(state: dict[str, Any], name: str, fn: Any) -> None:
    if name in state["completed"]:
        return
    if state.get("in_flight"):
        raise RuntimeError(
            f"Operation {state['in_flight']} may have returned without a durable result; refusing any retry."
        )
    state["in_flight"] = name
    state["invocations"][name] = state["invocations"].get(name, 0) + 1
    save_raw(state)
    started = time.perf_counter()
    value = fn()
    elapsed = time.perf_counter() - started
    # Persist returned native value before any correspondence or serialization work.
    state[name] = value
    state["runtimes_seconds"][name] = elapsed
    state["completed"].append(name)
    state["in_flight"] = None
    state["receipts"][name] = {
        "returned": True,
        "elapsed_seconds": elapsed,
        "result_type": type(value).__name__,
    }
    save_raw(state)


def make_recipes(
    state: dict[str, Any],
) -> tuple[WitnessGenerationPlan | None, list[dict[str, Any]]]:
    return build_plan(state["inputs"], state)


def execute() -> None:
    lock = acquire_lock()
    try:
        initial = not START.exists() and not RAW.exists()
        manifest, inputs = verify_stage_a(initial=initial)
        if not START.exists() and any((CASE / name).exists() for name in OUTPUTS):
            raise RuntimeError(
                "Canonical Stage B outputs exist; refusing treatment execution or overwrite."
            )
        if START.exists():
            state = load_raw() if RAW.exists() else None
            if state is None:
                raise RuntimeError(
                    "Start marker exists without valid raw state; no new treatment may start."
                )
            if state.get("in_flight"):
                raise RuntimeError(
                    f"Uncertain returned operation {state['in_flight']}; stop for reconciliation, do not rerun."
                )
            if state.get("completed") and "inputs" not in state:
                raise RuntimeError(
                    "Durable state is incomplete and cannot resume safely."
                )
            if state.get("state") == "CANONICAL_STAGE_B_COMPLETE":
                if (CASE / "stage_b_integrity.json").exists():
                    raise RuntimeError(
                        "Canonical Stage B exists and is read-only; refusing reentry."
                    )
        else:
            state = {
                "case": treatment.CASE,
                "stage_a_commit": STAGE_A_COMMIT,
                "repository_id": manifest["repository_id"],
                "snapshot_id": manifest["snapshot_id"],
                "treatment_sha256": manifest["task_sha256"],
                "execution_id": str(uuid.uuid4()),
                "runtime": runtime(),
                "state": "NOT_STARTED",
                "raw_status": "INCOMPLETE_UNVALIDATED",
                "inputs": inputs,
                "completed": [],
                "invocations": {},
                "runtimes_seconds": {},
                "receipts": {},
                "groundings": {},
                "in_flight": None,
            }
        if state["completed"] == [] and not START.exists():
            marker = {
                "case": treatment.CASE,
                "stage_a_commit": STAGE_A_COMMIT,
                "repository_id": manifest["repository_id"],
                "snapshot_id": manifest["snapshot_id"],
                "treatment_sha256": manifest["task_sha256"],
                "execution_id": state["execution_id"],
                "runtime": state["runtime"],
            }
            exclusive_atomic(
                START, (json.dumps(marker, indent=2) + "\n").encode(), replace=False
            )
            state["state"] = "PARTIAL_RAW_CAPTURE"
            save_raw(state)
        # Lexical acquisition returns once; native value is checkpointed immediately.
        operation(
            state,
            "lexical",
            lambda: acquire_localization_lexical_evidence(inputs["lexical_request"]),
        )
        state["acquisition"] = state["lexical"]
        if "acquisition" not in state:
            raise AssertionError("Lexical checkpoint missing.")
        operation(
            state,
            "routing",
            lambda: route_localization_lexical_evidence(
                state["acquisition"], inputs["roles"], inputs["role_preferences"]
            ),
        )
        # One explicit resolver call per exact frozen request; each result is persisted before proceeding.
        for key, request in inputs["grounding_requests"].items():
            operation(
                state,
                f"grounding:{key}",
                lambda request=request: ground_task_anchor(
                    task=treatment.interpretation(),
                    snapshot=inputs["lexical_request"].snapshot,
                    request=request,
                    module_universe=inputs["module_universe"],
                ),
            )
            state["groundings"][key] = state[f"grounding:{key}"]
            save_raw(state)
        plan, bindings = make_recipes(state)
        state["recipe_bindings"] = bindings
        state["plan"] = plan
        save_raw(state)
        if plan is None:
            raise RuntimeError(
                "No valid generation recipes could be bound; preserve raw state for review."
            )
        operation(state, "generation", lambda: generate_witness_hypotheses(plan))
        state["state"] = "TREATMENT_COMPLETE_RAW_CAPTURE"
        save_raw(state)
        finalize(state, manifest)
    finally:
        if os.name == "nt":
            import msvcrt

            lock.seek(0)
            msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
        lock.close()
        LOCK.unlink(missing_ok=True)


def finalize(state: dict[str, Any], manifest: dict[str, Any]) -> None:
    """Validate only after all native treatment values have durable receipts."""
    inputs = state["inputs"]
    acquisition = state["acquisition"]
    routing = state["routing"]
    view = state["generation"]
    if (
        len(acquisition.obligation_retrievals) != 11
        or len(routing.obligation_lanes) != 11
        or len(state["groundings"]) != 9
    ):
        raise ValueError("Captured lane/grounding cardinality mismatch.")
    expected_specs = inputs["recipe_specifications"]
    expected_families = {
        (
            item["obligation"],
            item["identity"],
            "WitnessHypothesisFamilyIdentity"
            if item["identity_kind"] == "family"
            else "WitnessHypothesisIdentity",
        )
        for item in expected_specs
    }
    actual_families = {
        (
            item.recipe.identity.obligation.value,
            item.recipe.identity.value,
            type(item.recipe.identity).__name__,
        )
        for item in view.attempts
    }
    if (
        len(state["recipe_bindings"]) < 25
        or len(state["plan"].recipes) != 25
        or len(view.attempts) != 25
        or actual_families != expected_families
    ):
        raise ValueError("Generation recipe correspondence failed.")
    if routing.global_retrieval != acquisition.full_task_retrieval:
        raise ValueError("Routing altered global native lane.")
    for lane in routing.obligation_lanes:
        native = lane.native_lane.retrieval.matches
        routed = tuple(x.match for x in lane.candidates)
        if len(native) != len(routed) or set(native) != set(routed):
            raise ValueError("Routing removed or duplicated a native candidate.")
        tier_order = tuple(
            candidate.match
            for tier in ("preferred-role-supported", "escape")
            for candidate in sorted(
                (item for item in lane.candidates if item.tier.value == tier),
                key=lambda item: item.native_rank,
            )
        )
        if routed != tier_order:
            raise ValueError("Routing changed native order inside a presentation tier.")
    origin_validation = validate_target_origins(state)
    # Canonical retrieval retains the full native rank and score provenance.
    lanes = [
        lane_json("global", treatment.TASK, acquisition.full_task_retrieval.matches)
    ]
    lanes.extend(
        lane_json(x.request.identity.value, x.request.text, x.retrieval.matches)
        for x in acquisition.obligation_retrievals
    )
    json_write(CASE / "retrieval.json", {"case": treatment.CASE, "lanes": lanes})
    routed = []
    for lane in routing.obligation_lanes:
        routed.append(
            {
                "query": lane.preference.query.value,
                "obligation": lane.preference.obligation.value,
                "preferred_roles": [x.name for x in lane.preference.preferred_roles],
                "candidates": [
                    {
                        "native_rank": x.native_rank,
                        "routed_position": x.routed_position,
                        "tier": x.tier.value,
                        "resource": resource_json(
                            x.match.document_statistics.analysis.document.resource
                        ),
                        "role_supports": [
                            {"role": e.role.name, "identity": str(e.identity)}
                            for e in x.role_evidence
                        ],
                    }
                    for x in lane.candidates
                ],
            }
        )
    json_write(
        CASE / "routing.json",
        {
            "case": treatment.CASE,
            "global_lane_unchanged": True,
            "candidate_retention_validated": True,
            "lanes": routed,
        },
    )
    json_write(
        CASE / "grounding.json",
        {
            "case": treatment.CASE,
            "requests": [
                grounding_json(state["groundings"][key], key)
                for key in inputs["grounding_requests"]
            ],
        },
    )
    gen = generation_json(view, inputs["grounding_requests"])
    json_write(CASE / "generation.json", {"case": treatment.CASE, **gen})
    native = {
        "inputs": inputs,
        "acquisition": acquisition,
        "routing": routing,
        "groundings": state["groundings"],
        "recipe_bindings": state["recipe_bindings"],
        "plan": state["plan"],
        "generation": view,
        "execution": {
            k: state[k]
            for k in (
                "execution_id",
                "invocations",
                "runtimes_seconds",
                "receipts",
                "runtime",
            )
        },
    }
    cap = gzip.compress(pickle.dumps(native, protocol=5), mtime=0)
    cap_path = CASE / "capture.pkl.gz"
    if cap_path.exists():
        if cap_path.read_bytes() != cap:
            raise FileExistsError("Refusing to overwrite different native capture.")
    else:
        exclusive_atomic(cap_path, cap, replace=False)
    counts = Counter(a.disposition.value for a in view.attempts)
    members = [m for a in view.attempts for m in a.members]
    refs = [
        m for m in members if m.recipe.projection is ProjectionKind.REFERENCING_RESOURCE
    ]
    ground_dispositions = Counter(
        item.disposition.value for item in state["groundings"].values()
    )
    complete_fanouts = [
        m.result_count for m in refs if m.complete and m.result_count is not None
    ]
    targets_by_operator: dict[str, set[tuple[str, str]]] = {
        x.name: set() for x in ProjectionKind
    }
    for attempt in view.attempts:
        for member in attempt.members:
            for projection in member.projections:
                targets_by_operator[member.recipe.projection.name].add(
                    (
                        projection.target.address.value,
                        projection.target.content_identity.value,
                    )
                )
    all_resources = {
        tuple((m.target.address.value, m.target.content_identity.value))
        for h in view.generated
        for m in h.members
    }
    owner_mirror = (
        targets_by_operator["OWNER_RESOURCE"] | targets_by_operator["MIRRORED_RESOURCE"]
    )
    full_union = owner_mirror | targets_by_operator["REFERENCING_RESOURCE"]
    integrity = {
        "schema": "case-0007-stage-b-integrity-v1",
        "status": "CAPTURED_NOT_ADJUDICATED",
        "stage_a_commit": STAGE_A_COMMIT,
        "stage_a_integrity_sha256": digest((CASE / "integrity.json").read_bytes()),
        "execution_id": state["execution_id"],
        "raw_capture_sha256": "set-after-final-raw-checkpoint",
        "raw_receipt_sha256": "set-after-final-raw-checkpoint",
        "native_capture_sha256": digest(cap),
        "canonical_sha256": {},
        "invocations": state["invocations"],
        "durable_receipts": state["receipts"],
        "runtimes_seconds": state["runtimes_seconds"],
        "repository_id": manifest["repository_id"],
        "snapshot_id": manifest["snapshot_id"],
        "implementation_sha256": manifest["implementation_sha256"],
        "stage_a_runtime": manifest["runtime"],
        "correspondence": {
            "lexical_lanes": 12,
            "routed_lanes": 11,
            "grounding_requests": 9,
            "recipe_specs": 25,
            "generation_attempts": len(view.attempts),
            "target_origin": "passed by production association validation and exact frozen-frame checks",
            "target_origin_detail": origin_validation,
        },
        "mechanical_counts": {
            "generation_attempts": len(view.attempts),
            "attempt_dispositions": dict(counts),
            "branch_children": sum(
                len(a.children)
                for a in view.attempts
                if isinstance(a.recipe.identity, WitnessHypothesisFamilyIdentity)
            ),
            "generated_hypotheses": len(view.generated),
            "member_occurrences": sum(len(h.members) for h in view.generated),
            "unique_generated_resources": len(all_resources),
            "operator_target_counts": {
                k: len(v) for k, v in targets_by_operator.items()
            },
            "owner_mirror_union": len(owner_mirror),
            "owner_mirror_reference_union": len(full_union),
            "reference_families": len(refs),
            "grounding_dispositions": dict(ground_dispositions),
            "reference_zero": sum(m.complete and not m.projections for m in refs),
            "reference_one": sum(m.complete and len(m.projections) == 1 for m in refs),
            "reference_several": sum(
                m.complete and len(m.projections) > 1 for m in refs
            ),
            "reference_result_overflow": sum(
                m.result_count is not None and m.result_count > m.result_limit
                for m in refs
            ),
            "reference_work_overflow": sum(not m.complete for m in refs),
            "reference_distinct_target_median": median(complete_fanouts)
            if complete_fanouts
            else None,
            "reference_distinct_target_max": max(
                (
                    m.result_count
                    for m in refs
                    if m.complete and m.result_count is not None
                ),
                default=0,
            ),
            "same_owner_collisions": sum(
                b.disposition.value == "duplicate-target"
                for a in view.attempts
                for b in a.branches
            ),
            "support_attachment_counts": {
                "global_lexical": sum(
                    support.query is None
                    for h in view.generated
                    for m in h.members
                    for support in m.lexical
                ),
                "own_obligation_lexical": sum(
                    support.query is not None
                    for h in view.generated
                    for m in h.members
                    for support in m.lexical
                ),
                "roles": sum(len(m.roles) for h in view.generated for m in h.members),
                "routed_preferred": sum(
                    support.candidate.tier.value == "preferred-role-supported"
                    for h in view.generated
                    for m in h.members
                    for support in m.routed
                ),
                "routed_escape": sum(
                    support.candidate.tier.value == "escape"
                    for h in view.generated
                    for m in h.members
                    for support in m.routed
                ),
                "structural_only_members": sum(
                    bool(m.structural) and not (m.lexical or m.roles or m.routed)
                    for h in view.generated
                    for m in h.members
                ),
            },
        },
    }
    for name in (
        "retrieval.json",
        "routing.json",
        "grounding.json",
        "generation.json",
        "capture.pkl.gz",
    ):
        integrity["canonical_sha256"][name] = artifact_digest(CASE / name)
    reference_counts = Counter(m.disposition.value for m in refs)
    report = [
        "# Case 0007 Stage B",
        "",
        "**CAPTURED — NOT ADJUDICATED**",
        "",
        "Stage A frozen treatment executed once and captured. No effectiveness analysis or adjudication was performed.",
        "",
        f"- Execution: `{state['execution_id']}`",
        f"- Lexical invocations: {state['invocations'].get('lexical', 0)}; routing: {state['invocations'].get('routing', 0)}; explicit grounding: {sum(v for k, v in state['invocations'].items() if k.startswith('grounding:'))}; generation: {state['invocations'].get('generation', 0)}",
        f"- Grounding dispositions: {dict(Counter(g.disposition.value for g in state['groundings'].values()))}",
        f"- Generation attempts: {len(view.attempts)}; generated hypotheses: {len(view.generated)}; generated branches: {integrity['mechanical_counts']['branch_children']}",
        f"- Reference family mechanical dispositions: {dict(reference_counts)}",
        f"- Reference result/work overflows: {integrity['mechanical_counts']['reference_result_overflow']}/{integrity['mechanical_counts']['reference_work_overflow']}",
        f"- Unique generated resources: {len(all_resources)}",
        "",
        "Native capture and integrity manifest retain complete provenance. These counts describe execution only.",
    ]
    report_bytes = ("\n".join(report) + "\n").encode()
    report_path = CASE / "stage_b.md"
    if report_path.exists() and report_path.read_bytes() != report_bytes:
        raise FileExistsError("Refusing to overwrite different Stage B report.")
    if not report_path.exists():
        exclusive_atomic(report_path, report_bytes, replace=False)
    integrity["canonical_sha256"]["stage_b.md"] = artifact_digest(CASE / "stage_b.md")
    state["state"] = "CANONICAL_STAGE_B_COMPLETE"
    state["raw_status"] = "CANONICAL_STAGE_B_COMPLETE"
    save_raw(state)
    integrity["raw_capture_sha256"] = digest(RAW.read_bytes())
    integrity["raw_receipt_sha256"] = artifact_digest(RAW_RECEIPT)
    integrity["execution_start_sha256"] = artifact_digest(START)
    integrity["canonical_sha256"]["stage_b_raw.sha256"] = digest(
        freeze.text_bytes(RAW_RECEIPT)
    )
    json_write(CASE / "stage_b_integrity.json", integrity)


def validate_target_origins(state: dict[str, Any]) -> dict[str, int]:
    """Replay native structural support against the supplied frozen frame."""
    view = state["generation"]
    plan = state["plan"]
    snapshot = state["inputs"]["lexical_request"].snapshot
    mirrors = state["inputs"]["mirrors"]
    checked = Counter()
    for attempt in view.attempts:
        for member in attempt.members:
            for projection in member.projections:
                for support in projection.structural:
                    validate_structural_support(
                        task=plan.task,
                        snapshot=snapshot,
                        target=projection.target,
                        support=support,
                    )
                    if isinstance(support, OwnerResourceSupport):
                        source = support.grounding.candidates[0].referent
                        if owner_resource(snapshot, source) != projection.target:
                            raise ValueError("OWNER target failed exact owner replay.")
                        checked["OWNER_RESOURCE"] += 1
                    elif isinstance(support, MirroredResourceSupport):
                        if support.correspondence not in mirrors.correspondences:
                            raise ValueError("MIRROR support is absent from frozen RI.")
                        source_owner = owner_resource(
                            snapshot,
                            support.grounding.candidates[0].referent,
                        )
                        counterpart = (
                            support.correspondence.test
                            if support.correspondence.source == source_owner
                            else support.correspondence.source
                        )
                        if counterpart != projection.target:
                            raise ValueError(
                                "MIRROR target failed exact counterpart check."
                            )
                        checked["MIRRORED_RESOURCE"] += 1
                    elif isinstance(support, PythonReferenceResourceSupport):
                        validate_reference_support(
                            support,
                            snapshot,
                            projection.target,
                        )
                        checked["REFERENCING_RESOURCE"] += 1
    return dict(checked)


def verify_read_only() -> None:
    state = load_raw()
    if state["state"] != "CANONICAL_STAGE_B_COMPLETE":
        raise RuntimeError(
            "Raw Stage B is not canonical complete; no treatment rerun permitted."
        )
    integrity = json.loads(
        (CASE / "stage_b_integrity.json").read_text(encoding="utf-8")
    )
    if integrity["raw_capture_sha256"] != digest(RAW.read_bytes()):
        raise ValueError("Canonical raw capture digest mismatch.")
    if integrity["raw_receipt_sha256"] != artifact_digest(RAW_RECEIPT):
        raise ValueError("Canonical raw receipt digest mismatch.")
    if integrity["execution_start_sha256"] != artifact_digest(START):
        raise ValueError("Execution-start marker digest mismatch.")
    for name, expected in integrity["canonical_sha256"].items():
        if artifact_digest(CASE / name) != expected:
            raise ValueError(f"Canonical artifact digest mismatch: {name}")
    raise RuntimeError("Canonical Stage B is valid and read-only; refusing reentry.")


def recount_generated_targets() -> None:
    """Correct derived operator-set counts from native generated children only."""
    state = load_raw()
    if state.get("state") != "CANONICAL_STAGE_B_COMPLETE":
        raise RuntimeError("Target recount requires complete durable native capture.")
    targets: dict[str, set[tuple[str, str]]] = {
        item.name: set() for item in ProjectionKind
    }
    support_types = {
        OwnerResourceSupport: ProjectionKind.OWNER_RESOURCE.name,
        MirroredResourceSupport: ProjectionKind.MIRRORED_RESOURCE.name,
        PythonReferenceResourceSupport: ProjectionKind.REFERENCING_RESOURCE.name,
    }
    for hypothesis in state["generation"].generated:
        for member in hypothesis.members:
            for support in member.structural:
                targets[support_types[type(support)]].add(
                    (
                        member.target.address.value,
                        member.target.content_identity.value,
                    )
                )
    integrity_path = CASE / "stage_b_integrity.json"
    integrity = json.loads(integrity_path.read_text(encoding="utf-8"))
    counts = integrity["mechanical_counts"]
    counts["operator_target_counts"] = {
        name: len(values) for name, values in targets.items()
    }
    owner_mirror = targets["OWNER_RESOURCE"] | targets["MIRRORED_RESOURCE"]
    all_structural = owner_mirror | targets["REFERENCING_RESOURCE"]
    counts["owner_mirror_union"] = len(owner_mirror)
    counts["owner_mirror_reference_union"] = len(all_structural)
    counts["reference_unique_target_resources"] = len(targets["REFERENCING_RESOURCE"])
    counts["unique_generated_resources"] = len(
        {
            (member.target.address.value, member.target.content_identity.value)
            for hypothesis in state["generation"].generated
            for member in hypothesis.members
        }
    )
    integrity["mechanical_count_basis"] = (
        "operator surfaces are projected from generated child hypotheses only; "
        "diagnostic targets rejected by result bounds are excluded"
    )
    data = (
        json.dumps(integrity, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    ).encode()
    exclusive_atomic(integrity_path, data, replace=True)


def repair_missing_raw_receipt() -> None:
    """Seal the already captured raw file if its sidecar receipt is absent."""
    payload = RAW.read_bytes()
    state = pickle.loads(gzip.decompress(payload))
    integrity = json.loads(
        (CASE / "stage_b_integrity.json").read_text(encoding="utf-8")
    )
    checksum = digest(payload)
    if (
        state.get("stage_a_commit") != STAGE_A_COMMIT
        or state.get("state") != "CANONICAL_STAGE_B_COMPLETE"
        or integrity.get("raw_capture_sha256") != checksum
    ):
        raise ValueError("Cannot seal an unrecognized or empty raw checkpoint.")
    if (
        RAW_RECEIPT.exists()
        and RAW_RECEIPT.read_text(encoding="ascii").strip() == checksum
    ):
        return
    exclusive_atomic(
        RAW_RECEIPT,
        f"{checksum}\n".encode(),
        replace=RAW_RECEIPT.exists(),
    )


def resume_check() -> None:
    """Exercise completed-operation reuse and verify canonical reentry refusal."""
    before = RAW.read_bytes()
    before_receipt = RAW_RECEIPT.read_bytes()
    state = load_raw()
    counts = dict(state["invocations"])
    operation(state, "generation", lambda: (_ for _ in ()).throw(AssertionError()))
    if state["invocations"] != counts:
        raise AssertionError("Completed treatment operation invocation count changed.")
    if RAW.read_bytes() != before:
        raise AssertionError("Read-only completed-operation resume changed raw bytes.")
    if RAW_RECEIPT.read_bytes() != before_receipt:
        raise AssertionError("Read-only resume changed the raw digest receipt.")
    try:
        verify_read_only()
    except RuntimeError as error:
        if "valid and read-only" not in str(error):
            raise
    else:
        raise AssertionError("Canonical reentry did not refuse treatment execution.")


def refresh_canonical_provenance() -> None:
    """Regenerate review JSON solely from the already captured native values."""
    state = load_raw()
    if state.get("state") != "CANONICAL_STAGE_B_COMPLETE":
        raise RuntimeError("Canonical refresh requires complete raw capture.")
    grounding = {
        "case": treatment.CASE,
        "requests": [
            grounding_json(state["groundings"][key], key)
            for key in state["inputs"]["grounding_requests"]
        ],
    }
    generation = {
        "case": treatment.CASE,
        **generation_json(state["generation"], state["inputs"]["grounding_requests"]),
    }
    for name, value in (("grounding.json", grounding), ("generation.json", generation)):
        path = CASE / name
        data = (
            json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
        ).encode()
        if path.read_bytes() != data:
            exclusive_atomic(path, data, replace=True)
    integrity_path = CASE / "stage_b_integrity.json"
    integrity = json.loads(integrity_path.read_text(encoding="utf-8"))
    integrity["canonical_sha256"]["grounding.json"] = artifact_digest(
        CASE / "grounding.json"
    )
    integrity["canonical_sha256"]["generation.json"] = artifact_digest(
        CASE / "generation.json"
    )
    integrity["canonical_sha256"]["stage_b_raw.sha256"] = artifact_digest(RAW_RECEIPT)
    integrity["raw_capture_sha256"] = digest(RAW.read_bytes())
    integrity["raw_receipt_sha256"] = artifact_digest(RAW_RECEIPT)
    integrity["execution_start_sha256"] = artifact_digest(START)
    integrity["durable_receipts"] = state["receipts"]
    inputs = state["inputs"]
    snapshot = inputs["lexical_request"].snapshot
    reference_request = inputs["reference_request"]
    corpus = inputs[
        "lexical_request"
    ].index.corpus_statistics.collection_analysis.document_collection.corpus
    integrity["corpus_id"] = str(corpus.id)
    integrity["native_frame_counts"] = {
        "resources": len(snapshot.resources),
        "module_interpretations": len(inputs["modules"].interpretations),
        "function_analyses": len(inputs["functions"]),
        "class_method_analyses": len(inputs["classes"]),
        "reference_source_analyses": len(reference_request.sources),
        "mirror_correspondences": len(inputs["mirrors"].correspondences),
    }
    integrity["reference_mechanical_details"] = reference_statistics(state)
    generated = state["generation"].generated
    counts = integrity["mechanical_counts"]
    counts["fixed_hypotheses"] = sum(
        attempt.hypothesis is not None
        and isinstance(attempt.recipe.identity, WitnessHypothesisIdentity)
        for attempt in state["generation"].attempts
    )
    cells = {
        (hypothesis.identity.obligation.value, member.target.address.value)
        for hypothesis in generated
        for member in hypothesis.members
    }
    counts["obligation_resource_occurrences"] = len(cells)
    counts["per_obligation_generated_resources"] = {
        obligation: len(
            {
                resource
                for cell_obligation, resource in cells
                if cell_obligation == obligation
            }
        )
        for obligation in sorted({obligation for obligation, _ in cells})
    }
    integrity["internal_validation_replays"] = (
        "Production generation replayed grounding freshness and structural/reference "
        "support inside its single invocation; those checks are separate from the "
        "nine explicit task-level grounding executions."
    )
    counts = integrity["mechanical_counts"]
    runtimes = state["runtimes_seconds"]
    support = counts["support_attachment_counts"]
    report = [
        "# Case 0007 Stage B",
        "",
        "**CAPTURED — NOT ADJUDICATED**",
        "",
        "Stage A frozen treatment executed once and captured. No effectiveness analysis or adjudication was performed.",
        "",
        f"- Execution: `{state['execution_id']}`",
        f"- Invocations: lexical {state['invocations']['lexical']}; routing {state['invocations']['routing']}; explicit grounding {sum(v for k, v in state['invocations'].items() if k.startswith('grounding:'))}; generation {state['invocations']['generation']}",
        f"- Runtime seconds: lexical {runtimes['lexical']:.3f}; routing {runtimes['routing']:.3f}; generation {runtimes['generation']:.3f}",
        f"- Grounding dispositions: {counts['grounding_dispositions']}",
        f"- Generation attempts: {counts['generation_attempts']} {counts['attempt_dispositions']}; hypotheses {counts['generated_hypotheses']}; branches {counts['branch_children']}; members {counts['member_occurrences']}",
        f"- Obligation/resource cells: {counts['obligation_resource_occurrences']}; per-obligation generated resources {counts['per_obligation_generated_resources']}",
        f"- Reference families: zero/one/several {counts['reference_zero']}/{counts['reference_one']}/{counts['reference_several']}; complete fanout median/max {counts['reference_distinct_target_median']}/{counts['reference_distinct_target_max']}; result/work overflows {counts['reference_result_overflow']}/{counts['reference_work_overflow']}; same-owner collisions {counts['same_owner_collisions']}",
        f"- Unique generated resources: {counts['unique_generated_resources']}; operator resources {counts['operator_target_counts']}; OWNER + MIRROR {counts['owner_mirror_union']}; OWNER + MIRROR + REFERENCE {counts['owner_mirror_reference_union']}",
        f"- Support attachments: {support}",
        "",
        "These are mechanical execution and provenance counts only; they convey no witness usefulness or task coverage.",
    ]
    report_data = ("\n".join(report) + "\n").encode()
    report_path = CASE / "stage_b.md"
    if report_path.read_bytes() != report_data:
        exclusive_atomic(report_path, report_data, replace=True)
    integrity["canonical_sha256"]["stage_b.md"] = artifact_digest(report_path)
    integrity["post_processing"] = (
        "Canonical provenance JSON regenerated from durable native capture; no treatment operation executed."
    )
    data = (
        json.dumps(integrity, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    ).encode()
    exclusive_atomic(integrity_path, data, replace=True)


def reference_statistics(state: dict[str, Any]) -> dict[str, Any]:
    """Count exact reference families and supports without judging their utility."""
    view = state["generation"]
    snapshot = state["inputs"]["lexical_request"].snapshot
    families = []
    fanouts: dict[str, int] = {}
    same_owner = 0
    support_facts = 0
    direct_calls = 0
    for attempt in view.attempts:
        reference_members = [
            member
            for member in attempt.members
            if member.recipe.projection is ProjectionKind.REFERENCING_RESOURCE
        ]
        if not reference_members:
            continue
        member = reference_members[0]
        family = {
            "identity": attempt.recipe.identity.value,
            "grounding_request": request_key(
                member.recipe.grounding.request,
                state["inputs"]["grounding_requests"],
            ),
            "disposition": member.disposition.value,
            "work_performed": member.work_performed,
            "work_limit": member.work_limit,
            "complete": member.complete,
            "result_count": member.result_count,
            "result_limit": member.result_limit,
        }
        families.append(family)
        if member.complete and member.result_count is not None:
            seed = member.recipe.grounding.candidates[0].referent
            seed_subject = getattr(seed, "subject", seed)
            seed_identity = getattr(seed_subject, "identity", None)
            if seed_identity is not None:
                fanouts[str(seed_identity)] = member.result_count
            owner = owner_resource(snapshot, seed)
            same_owner += sum(item.target == owner for item in member.projections)
        for projection in member.projections:
            for support in projection.structural:
                if isinstance(support, PythonReferenceResourceSupport):
                    support_facts += len(support.references)
                    direct_calls += sum(fact.direct_call for fact in support.references)
    family_ids = {item["identity"] for item in families}
    branches = [
        branch
        for attempt in view.attempts
        if attempt.recipe.identity.value in family_ids
        for branch in attempt.branches
    ]
    complete_seed_fanouts = tuple(fanouts.values())
    return {
        "distinct_grounded_seed_count": len(fanouts),
        "families": families,
        "distinct_resource_fanout_median": median(complete_seed_fanouts)
        if complete_seed_fanouts
        else None,
        "distinct_resource_fanout_max": max(complete_seed_fanouts, default=0),
        "same_owner_reference_targets": same_owner,
        "valid_reference_children": sum(
            branch.disposition.value == "generated" for branch in branches
        ),
        "duplicate_target_branch_failures": sum(
            branch.disposition.value == "duplicate-target" for branch in branches
        ),
        "native_reference_support_facts_on_projection_targets": support_facts,
        "direct_call_tagged_support_facts": direct_calls,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-read-only", action="store_true")
    parser.add_argument("--recount-generated-targets", action="store_true")
    parser.add_argument("--resume-check", action="store_true")
    parser.add_argument("--refresh-canonical-provenance", action="store_true")
    parser.add_argument("--repair-missing-raw-receipt", action="store_true")
    args = parser.parse_args()
    if args.verify_read_only:
        verify_read_only()
    elif args.recount_generated_targets:
        recount_generated_targets()
    elif args.resume_check:
        resume_check()
    elif args.refresh_canonical_provenance:
        refresh_canonical_provenance()
    elif args.repair_missing_raw_receipt:
        repair_missing_raw_receipt()
    else:
        execute()


if __name__ == "__main__":
    main()
