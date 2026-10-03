# Copyright (c) 2026
# ruff: noqa: ANN001, C901, COM812, EM101, EM102, INP001, PLR0912, PLR0913, PLR0917, PLR2004, S101, T201, TRY003
"""Capture frozen Case 0005 acquisition and routing once; verify read-only later."""

from __future__ import annotations

import asyncio
import gzip
import io
import json
import pickle
import sys
import tarfile
import time
from dataclasses import asdict
from pathlib import Path

import freeze

from devtools.context.localization.lexical import acquire_localization_lexical_evidence
from devtools.context.localization.roles.models import RepositoryRoleKind
from devtools.context.localization.routing import route_localization_lexical_evidence
from devtools.context.localization.routing.models import RoutingTier

CASE = Path(__file__).resolve().parent
RELATIVE_CASE = "experiments/codex_dogfood/case_0005"
STAGE_A = "e9764cde6dc6c2f379e4b08561974cd6b59c30d3"
CAPTURE = CASE / "capture.pkl.gz"
RETRIEVAL = CASE / "retrieval.json"
ROUTING = CASE / "routing.json"
OUTPUTS = (CAPTURE, RETRIEVAL, ROUTING)


def _require_no_outputs() -> None:
    """Refuse a second capture before either production call."""
    if any(path.exists() for path in OUTPUTS):
        raise FileExistsError("Stage B output already exists; capture is single-use.")


async def _committed_stage_a(protocol: dict) -> None:
    """Compare exact committed Stage A bytes and implementation bindings."""
    tree = await freeze.git("archive", "--format=tar", STAGE_A, "--", RELATIVE_CASE)
    seen = set()
    expected = json.loads(freeze.binary(CASE / "integrity.json"))
    with tarfile.open(fileobj=io.BytesIO(tree)) as archive:
        for member in archive.getmembers():
            if not member.isfile():
                continue
            name = Path(member.name).name
            if name not in expected and name != "integrity.json":
                raise ValueError("Stage A commit has an unexpected artifact.")
            stream = archive.extractfile(member)
            assert stream is not None
            committed = stream.read()
            current = freeze.binary(CASE / name)
            if name.endswith((".json", ".py", ".md")):
                committed = committed.replace(b"\r\n", b"\n")
                current = current.replace(b"\r\n", b"\n")
            if committed != current:
                raise ValueError(f"Stage A committed artifact differs: {name}")
            seen.add(name)
    if seen != set(expected) | {"integrity.json"}:
        raise ValueError("Stage A committed artifact inventory differs.")
    implementation = await freeze.git(
        "archive", "--format=tar", STAGE_A, "--", "src/devtools"
    )
    found = set()
    with tarfile.open(fileobj=io.BytesIO(implementation)) as archive:
        for member in archive.getmembers():
            if member.name not in protocol["implementation_sha256"]:
                continue
            stream = archive.extractfile(member)
            assert stream is not None
            normalized = stream.read().replace(b"\r\n", b"\n")
            if freeze.sha(normalized) != protocol["implementation_sha256"][member.name]:
                raise ValueError("Committed production implementation differs.")
            found.add(member.name)
    if found != set(protocol["implementation_sha256"]):
        raise ValueError("Committed production implementation coverage differs.")


def _check_frozen_contract(protocol: dict, native: dict) -> None:
    """Bind exact task, frame, settings, roles and Python environment."""
    request = native["request"]
    role_view = native["role_evidence"]
    preferences = native["preferences"]
    corpus = (
        request.index.corpus_statistics.collection_analysis.document_collection.corpus
    )
    if (
        protocol["case"] != "case_0005"
        or protocol["status"] != "FROZEN BEFORE RETRIEVAL AND ROUTING"
        or protocol["starting_head"] != freeze.START
        or protocol["python_version"] != sys.version
        or request.task.identity.value != protocol["task_identity"]
        or request.full_task_query != protocol["task_full_prompt"]
        or request.full_task_query != protocol["global_lane"]["query_text"]
        or request.purpose != protocol["purpose"]
        or str(request.snapshot.repository_id) != protocol["repository_id"]
        or str(request.snapshot.id) != protocol["snapshot_id"]
        or str(corpus.id) != protocol["eligible_corpus_id"]
        or len(request.snapshot.resources) != 515
        or len(request.task.anchors) != 6
        or len(request.task.obligations) != 9
        or len(request.obligation_queries) != 9
        or len(preferences) != 9
        or request.maximum_results != 515
        or request.settings.k1 != protocol["bm25"]["k1"]
        or request.settings.b != protocol["bm25"]["b"]
        or protocol["bm25"]["filename_weight"] != 0.25
        or protocol["routing"]["identity"] != "caller-role-or-stable-two-tier-v1"
        or role_view.derivation_identity != protocol["role_derivation"]["identity"]
        or role_view.repository_id != request.snapshot.repository_id
        or role_view.snapshot_id != request.snapshot.id
    ):
        raise ValueError("Frozen Stage A contract differs.")
    for query, preference, frozen in zip(
        request.obligation_queries,
        preferences,
        protocol["obligation_queries"],
        strict=True,
    ):
        if (
            query.identity.value != frozen["identity"]
            or query.obligation.value != frozen["obligation"]
            or query.text != frozen["text"]
            or preference.query != query.identity
            or preference.obligation != query.obligation
            or [item.name for item in preference.preferred_roles]
            != frozen["preferred_roles"]
            or any(
                not isinstance(item, RepositoryRoleKind)
                for item in preference.preferred_roles
            )
        ):
            raise ValueError("Frozen query/preference differs.")
    if (
        preferences[-1].preferred_roles != ()
        or request.obligation_queries[-1].identity.value != "q-validation"
    ):
        raise ValueError("Frozen validation preference differs.")


def _match(
    match, native_rank: int, repository_id: str, snapshot_id: str, filename_statistics
) -> dict:
    """Project exact native BM25 evidence without semantic judgment."""
    document = match.document_statistics.analysis.document
    resource = document.resource
    content_terms = {item.normalized_term for item in match.term_contributions}
    filename_terms = {
        item.normalized_term for item in match.filename_term_contributions
    }
    return {
        "native_rank": native_rank,
        "resource_identity": {
            "repository_id": repository_id,
            "snapshot_id": snapshot_id,
            "address": resource.address.value,
            "content_identity": resource.content_identity.value,
        },
        "resource_address": resource.address.value,
        "content_identity": resource.content_identity.value,
        "document_identity": document.id.value,
        "score": match.score,
        "content_score": match.content_score,
        "filename_score": match.filename_score,
        "filename_weight": match.filename_weight,
        "weighted_filename_score": match.weighted_filename_score,
        "content_contributions": [asdict(item) for item in match.term_contributions],
        "filename_contributions": [
            asdict(item) for item in match.filename_term_contributions
        ],
        "content_term_observations": {
            item.normalized_term: [
                asdict(observation) for observation in item.observations
            ]
            for item in match.document_statistics.term_frequencies
            if item.normalized_term in content_terms
        },
        "filename_term_observations": {
            item.normalized_term: [
                asdict(observation) for observation in item.observations
            ]
            for item in filename_statistics.term_frequencies
            if item.normalized_term in filename_terms
        }
        if filename_statistics is not None
        else {},
    }


def _lane(
    query_id: str, obligation_id: str | None, result, repo: str, snap: str
) -> dict:
    """Project a complete native result in original order."""
    corpus_id = (
        result.index.corpus_statistics.collection_analysis.document_collection.corpus.id
    )
    filename_statistics = (
        {
            item.analysis.document.id: item
            for item in result.filename_index.document_statistics
        }
        if result.filename_index
        else {}
    )
    return {
        "query_identity": query_id,
        "obligation_identity": obligation_id,
        "query_text": result.query.text,
        "query_semantics": result.query.QUERY_SEMANTICS,
        "query_observations": [asdict(item) for item in result.query.observations],
        "normalized_terms": list(result.query.normalized_terms),
        "retrieval_semantics": result.RETRIEVAL_SEMANTICS,
        "settings": {"k1": result.settings.k1, "b": result.settings.b},
        "maximum_results": result.maximum_results,
        "index_reference": {
            "corpus_identity": corpus_id.value,
            "content_index_semantics": result.index.INDEX_SEMANTICS,
            "filename_index_semantics": result.filename_index.INDEX_SEMANTICS
            if result.filename_index
            else None,
        },
        "result_count": len(result.matches),
        "matches": [
            _match(
                match,
                rank,
                repo,
                snap,
                filename_statistics.get(match.document_statistics.analysis.document.id),
            )
            for rank, match in enumerate(result.matches, 1)
        ],
    }


def _retrieval_json(
    protocol: dict, acquisition, capture_sha: str, seconds: float
) -> dict:
    """Serialize global and nine distinct obligation lanes without reranking."""
    repo = str(acquisition.repository_id)
    snap = str(acquisition.snapshot_id)
    lanes = [
        _lane("global-full-task", None, acquisition.full_task_retrieval, repo, snap),
        *(
            _lane(
                item.request.identity.value,
                item.request.obligation.value,
                item.retrieval,
                repo,
                snap,
            )
            for item in acquisition.obligation_retrievals
        ),
    ]
    return {
        "schema": "codex-case-0005-native-lexical-capture-v1",
        "case": "case_0005",
        "stage_a_commit": STAGE_A,
        "stage_a_manifest_sha256": freeze.sha(
            freeze.binary(CASE / "pre_retrieval.json").replace(b"\r\n", b"\n")
        ),
        "stage_a_inputs_sha256": protocol["inputs_sha256"],
        "capture_sha256": capture_sha,
        "task_identity": acquisition.task.identity.value,
        "purpose": acquisition.purpose,
        "repository_id": repo,
        "snapshot_id": snap,
        "corpus_id": protocol["eligible_corpus_id"],
        "eligible_resource_count": protocol["frame_resource_count"],
        "bm25": protocol["bm25"],
        "acquisition_seconds": seconds,
        "lane_count": len(lanes),
        "global_lane_reference": "global-full-task",
        "lanes": lanes,
    }


def _support(item) -> dict:
    """Project one native support with its original observation identity."""
    return {
        "identity": item.identity,
        "kind": item.kind.value,
        "source_address": item.source_address.value,
        "native_identities": list(item.native_identities),
        "observation": list(item.observation),
    }


def _role(item) -> dict:
    """Retain exact role and support provenance for a preferred candidate."""
    return {
        "identity": item.identity,
        "role": item.role.name,
        "resource_address": item.resource.address.value,
        "content_identity": item.resource.content_identity.value,
        "supports": [_support(support) for support in item.supports],
    }


def _candidate(candidate) -> dict:
    """Project exact routed position, native identity and matching supports."""
    resource = candidate.match.document_statistics.analysis.document.resource
    return {
        "native_rank": candidate.native_rank,
        "routed_position": candidate.routed_position,
        "tier": candidate.tier.name,
        "resource_address": resource.address.value,
        "content_identity": resource.content_identity.value,
        "matching_preferred_roles": [
            item.role.name for item in candidate.role_evidence
        ],
        "role_evidence": [_role(item) for item in candidate.role_evidence],
    }


def _routed_json(protocol: dict, routed, retrieval_digest: str, seconds: float) -> dict:
    """Serialize independent two-tier views without assigning usefulness."""
    native_lanes = _retrieval_json(protocol, routed.acquisition, "", 0.0)["lanes"]
    result = []
    for native, lane in zip(native_lanes[1:], routed.obligation_lanes, strict=True):
        result.append(
            {
                "query_identity": lane.native_lane.request.identity.value,
                "obligation_identity": lane.native_lane.request.obligation.value,
                "native_result_reference": freeze.sha(freeze.json_bytes(native)),
                "preferred_roles": [
                    role.name for role in lane.preference.preferred_roles
                ],
                "preference_query_identity": lane.preference.query.value,
                "preference_obligation_identity": lane.preference.obligation.value,
                "preferred_count": len(lane.preferred),
                "escape_count": len(lane.escape),
                "native_result_count": len(lane.native_lane.retrieval.matches),
                "candidates": [_candidate(candidate) for candidate in lane.candidates],
            }
        )
    return {
        "schema": "codex-case-0005-two-tier-routing-capture-v1",
        "case": "case_0005",
        "stage_a_commit": STAGE_A,
        "stage_a_manifest_sha256": freeze.sha(
            freeze.binary(CASE / "pre_retrieval.json").replace(b"\r\n", b"\n")
        ),
        "stage_a_inputs_sha256": protocol["inputs_sha256"],
        "retrieval_sha256": retrieval_digest,
        "task_identity": routed.acquisition.task.identity.value,
        "repository_id": str(routed.role_evidence.repository_id),
        "snapshot_id": str(routed.role_evidence.snapshot_id),
        "corpus_id": protocol["eligible_corpus_id"],
        "routing_policy_identity": protocol["routing"]["identity"],
        "role_derivation_identity": routed.role_evidence.derivation_identity,
        "global_lane_reference": freeze.sha(freeze.json_bytes(native_lanes[0])),
        "global_lane_routed": False,
        "routing_seconds": seconds,
        "routed_lane_count": len(result),
        "lanes": result,
    }


def _check_results(protocol: dict, native: dict, acquisition, routed) -> None:
    """Verify frame, source identity, every candidate and exact role support."""
    request = native["request"]
    role_view = native["role_evidence"]
    preferences = native["preferences"]
    _check_frozen_contract(protocol, native)
    if (
        acquisition.task is not request.task
        or acquisition.purpose != request.purpose
        or acquisition.repository_id != request.snapshot.repository_id
        or acquisition.snapshot_id != request.snapshot.id
        or len(acquisition.obligation_retrievals) != 9
        or routed.acquisition is not acquisition
        or routed.global_retrieval is not acquisition.full_task_retrieval
        or routed.role_evidence is not role_view
        or len(routed.obligation_lanes) != 9
    ):
        raise ValueError(
            "Native acquisition or routed aggregate differs from frozen inputs."
        )
    results = (
        acquisition.full_task_retrieval,
        *(lane.retrieval for lane in acquisition.obligation_retrievals),
    )
    queries = (
        request.full_task_query,
        *(item.text for item in request.obligation_queries),
    )
    for result, query in zip(results, queries, strict=True):
        if (
            result.query.text != query
            or result.index is not request.index
            or result.settings != request.settings
            or result.maximum_results != request.maximum_results
            or len(result.matches) > request.maximum_results
        ):
            raise ValueError(
                "Native lexical result differs from its frozen query/index/settings."
            )
    role_by_identity = {item.identity: item for item in role_view.evidence}
    if (
        len(role_by_identity) != len(role_view.evidence)
        or role_view.resources != request.snapshot.resources
    ):
        raise ValueError("Role view identities or frame differ.")
    for query, lexical, lane, preference in zip(
        request.obligation_queries,
        acquisition.obligation_retrievals,
        routed.obligation_lanes,
        preferences,
        strict=True,
    ):
        if lexical.request is not query:
            raise ValueError(
                "Native query identity or order differs from frozen request."
            )
        matches = lexical.retrieval.matches
        if (
            lane.native_lane is not lexical
            or lane.preference is not preference
            or len(lane.candidates) != len(matches)
            or len(lane.preferred) + len(lane.escape) != len(matches)
        ):
            raise ValueError("Routed lane lost native identity or candidate coverage.")
        positions = [candidate.native_rank for candidate in lane.candidates]
        if sorted(positions) != list(range(1, len(matches) + 1)):
            raise ValueError("Routed lane lost or duplicated a native candidate.")
        for tier in (lane.preferred, lane.escape):
            ranks = [candidate.native_rank for candidate in tier]
            if ranks != sorted(ranks) or len(ranks) != len(set(ranks)):
                raise ValueError("Routing changed native order within a tier.")
        for position, candidate in enumerate(lane.candidates, 1):
            if (
                candidate.routed_position != position
                or candidate.match is not matches[candidate.native_rank - 1]
            ):
                raise ValueError("Routed position or native match reference differs.")
            address = (
                candidate.match.document_statistics.analysis.document.resource.address
            )
            available = tuple(
                item
                for role in preference.preferred_roles
                for item in role_view.for_resource(address)
                if item.role is role
            )
            if candidate.role_evidence != available:
                raise ValueError(
                    "Routed role-support explanation differs from frozen view."
                )
            if any(
                role_by_identity.get(item.identity) is not item
                for item in candidate.role_evidence
            ):
                raise ValueError(
                    "Routed support does not reference frozen native evidence."
                )
            expected_tier = (
                RoutingTier.PREFERRED_ROLE_SUPPORTED
                if available
                else RoutingTier.ESCAPE
            )
            if candidate.tier is not expected_tier:
                raise ValueError("Routed tier qualification differs.")
        if not preference.preferred_roles and (
            lane.preferred or positions != list(range(1, len(matches) + 1))
        ):
            raise ValueError("Empty preference changed native presentation order.")
    if routed.obligation_lanes[-1].preference.preferred_roles != ():
        raise ValueError("Validation query's empty preference changed.")


def _write_exclusive(path: Path, content: bytes) -> None:
    """Retain immutable experimental binary/JSON bytes once."""
    with path.open("xb") as output:
        output.write(content)


def capture() -> None:
    """Preflight completely, then execute each production entry point once."""
    _require_no_outputs()
    if asyncio.run(freeze.git("rev-parse", "HEAD")).decode().strip() != STAGE_A:
        raise ValueError("Capture requires the exact Stage A commit.")
    protocol = json.loads(freeze.binary(CASE / "pre_retrieval.json"))
    asyncio.run(_committed_stage_a(protocol))
    freeze.validate()
    native = pickle.loads(gzip.decompress(freeze.binary(CASE / "inputs.pkl.gz")))  # noqa: S301
    _check_frozen_contract(protocol, native)
    _require_no_outputs()

    start = time.perf_counter()
    acquisition = acquire_localization_lexical_evidence(native["request"])
    acquisition_seconds = time.perf_counter() - start
    start = time.perf_counter()
    routed = route_localization_lexical_evidence(
        acquisition, native["role_evidence"], native["preferences"]
    )
    routing_seconds = time.perf_counter() - start

    _check_results(protocol, native, acquisition, routed)
    retained = {
        "case": "case_0005",
        "stage_a_commit": STAGE_A,
        "stage_a_manifest_sha256": freeze.sha(
            freeze.binary(CASE / "pre_retrieval.json").replace(b"\r\n", b"\n")
        ),
        "stage_a_inputs_sha256": protocol["inputs_sha256"],
        "request": native["request"],
        "role_evidence": native["role_evidence"],
        "preferences": native["preferences"],
        "acquisition": acquisition,
        "routed": routed,
        "acquisition_seconds": acquisition_seconds,
        "routing_seconds": routing_seconds,
        "invocation_counts": {"acquisition": 1, "routing": 1},
    }
    capture_bytes = gzip.compress(
        pickle.dumps(retained, protocol=pickle.HIGHEST_PROTOCOL), mtime=0
    )
    retrieval = _retrieval_json(
        protocol, acquisition, freeze.sha(capture_bytes), acquisition_seconds
    )
    retrieval_bytes = freeze.json_bytes(retrieval)
    routing = _routed_json(
        protocol, routed, freeze.sha(retrieval_bytes), routing_seconds
    )
    routing_bytes = freeze.json_bytes(routing)
    _verify_serializations(
        protocol,
        retained,
        retrieval,
        routing,
        capture_bytes,
        retrieval_bytes,
        routing_bytes,
    )
    _require_no_outputs()
    for path, content in zip(
        OUTPUTS, (capture_bytes, retrieval_bytes, routing_bytes), strict=True
    ):
        _write_exclusive(path, content)
    print(
        json.dumps(
            {
                "status": "STAGE B CAPTURED — NOT ADJUDICATED",
                "capture_sha256": freeze.sha(capture_bytes),
                "retrieval_sha256": freeze.sha(retrieval_bytes),
                "routing_sha256": freeze.sha(routing_bytes),
                "lanes": 10,
                "routed_lanes": 9,
                "invocations": retained["invocation_counts"],
                "acquisition_seconds": acquisition_seconds,
                "routing_seconds": routing_seconds,
            },
            ensure_ascii=True,
            sort_keys=True,
        )
    )


def _verify_serializations(
    protocol: dict,
    retained: dict,
    retrieval: dict,
    routing: dict,
    capture_bytes: bytes,
    retrieval_bytes: bytes,
    routing_bytes: bytes,
) -> None:
    """Reproject captured objects; never re-execute production transformations."""
    native = {key: retained[key] for key in ("request", "role_evidence", "preferences")}
    acquisition, routed = retained["acquisition"], retained["routed"]
    _check_results(protocol, native, acquisition, routed)
    expected_retrieval = _retrieval_json(
        protocol,
        acquisition,
        freeze.sha(capture_bytes),
        retained["acquisition_seconds"],
    )
    expected_routing = _routed_json(
        protocol, routed, freeze.sha(retrieval_bytes), retained["routing_seconds"]
    )
    if (
        retrieval != expected_retrieval
        or routing != expected_routing
        or retrieval_bytes != freeze.json_bytes(expected_retrieval)
        or routing_bytes != freeze.json_bytes(expected_routing)
        or len(retrieval["lanes"]) != 10
        or len(routing["lanes"]) != 9
        or retained["invocation_counts"] != {"acquisition": 1, "routing": 1}
        or retrieval["repository_id"] != routing["repository_id"]
        or retrieval["snapshot_id"] != routing["snapshot_id"]
        or retrieval["corpus_id"] != routing["corpus_id"]
        or retrieval["task_identity"] != routing["task_identity"]
        or routing["global_lane_reference"]
        != freeze.sha(freeze.json_bytes(retrieval["lanes"][0]))
    ):
        raise ValueError(
            "Serialized Stage B output differs from native captured objects."
        )
    for lane, expected in zip(retrieval["lanes"][1:], routing["lanes"], strict=True):
        if expected["native_result_reference"] != freeze.sha(freeze.json_bytes(lane)):
            raise ValueError("Routed lane native result reference differs.")
        for candidate in expected["candidates"]:
            source = lane["matches"][candidate["native_rank"] - 1]
            if (candidate["resource_address"], candidate["content_identity"]) != (
                source["resource_address"],
                source["content_identity"],
            ):
                raise ValueError("Routed candidate differs from its native match.")


def verify_outputs() -> dict:
    """Read-only audit of committed-ready outputs without acquisition/routing."""
    if not all(path.exists() for path in OUTPUTS):
        raise FileNotFoundError("Stage B output inventory is incomplete.")
    protocol = json.loads(freeze.binary(CASE / "pre_retrieval.json"))
    asyncio.run(_committed_stage_a(protocol))
    capture_bytes = freeze.binary(CAPTURE)
    # Git may check text outputs out with CRLF on Windows. Their canonical
    # committed JSON bytes and cross-artifact SHA-256 values remain LF.
    retrieval_bytes = freeze.binary(RETRIEVAL).replace(b"\r\n", b"\n")
    routing_bytes = freeze.binary(ROUTING).replace(b"\r\n", b"\n")
    retained = pickle.loads(gzip.decompress(capture_bytes))  # noqa: S301
    retrieval = json.loads(retrieval_bytes)
    routing = json.loads(routing_bytes)
    if retrieval["capture_sha256"] != freeze.sha(capture_bytes) or routing[
        "retrieval_sha256"
    ] != freeze.sha(retrieval_bytes):
        raise ValueError("Stage B output digests do not join.")
    _verify_serializations(
        protocol,
        retained,
        retrieval,
        routing,
        capture_bytes,
        retrieval_bytes,
        routing_bytes,
    )
    return {
        "status": "STAGE B CAPTURED — NOT ADJUDICATED",
        "stage_a_commit": STAGE_A,
        "resources": protocol["frame_resource_count"],
        "lexical_lanes": len(retrieval["lanes"]),
        "routed_lanes": len(routing["lanes"]),
        "acquisition_invocations": retained["invocation_counts"]["acquisition"],
        "routing_invocations": retained["invocation_counts"]["routing"],
        "capture_sha256": freeze.sha(capture_bytes),
        "retrieval_sha256": freeze.sha(retrieval_bytes),
        "routing_sha256": freeze.sha(routing_bytes),
        "acquisition_seconds": retained["acquisition_seconds"],
        "routing_seconds": retained["routing_seconds"],
    }


if __name__ == "__main__":
    if sys.argv[1:] == ["--capture"]:
        capture()
    elif sys.argv[1:] == ["--verify"]:
        print(json.dumps(verify_outputs(), ensure_ascii=True, sort_keys=True))
    else:
        raise SystemExit("Use --capture once or --verify read-only.")
