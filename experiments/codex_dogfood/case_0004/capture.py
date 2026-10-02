# Copyright (c) 2026
# ruff: noqa: C901, COM812, PLR0912, PLR0915, PLR2004, S603, S607, T201
"""Execute the frozen Case 0004 lexical acquisition once and retain it."""

from __future__ import annotations

import gzip
import hashlib
import json
import pickle
import subprocess
import sys
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any

from devtools.context.localization.lexical import (
    LocalizationLexicalAcquisition,
    LocalizationLexicalAcquisitionRequest,
    acquire_localization_lexical_evidence,
)
from devtools.context.localization.obligation import RequirementStatus

if TYPE_CHECKING:
    from devtools.context.retrieval.lexical.bm25 import (
        RepositoryTextLexicalBm25RetrievalResult,
    )


ROOT = Path(__file__).resolve().parents[3]
CASE = Path(__file__).resolve().parent
PROTOCOL = CASE / "pre_retrieval.json"
INPUTS = CASE / "inputs.pkl.gz"
NATIVE_OUTPUT = CASE / "capture.pkl.gz"
JSON_OUTPUT = CASE / "retrieval.json"
STAGE_A = "719a3d44b45ebc664414ab0267ff23d836cc10a0"
STARTING_HEAD = "3cfda0a81ae95f578f42b8fd6b17cc8bcf751bc1"


def _sha256(content: bytes) -> str:
    """Return lowercase SHA-256 for bytes retained by this case."""
    return hashlib.sha256(content).hexdigest()


def _git_blob(commit: str, path: str) -> bytes:
    """Read one exact committed source blob for implementation verification."""
    return subprocess.check_output(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
    )


def _canonical_working_text(path: Path) -> bytes:
    """Normalize platform line endings before comparing committed text blobs."""
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").encode("utf-8")


def _validate_request(
    protocol: dict[str, Any], request: LocalizationLexicalAcquisitionRequest
) -> None:
    """Check frozen inputs and production implementation before acquisition."""
    if protocol["status"] != "FROZEN BEFORE RETRIEVAL":
        msg = "Case 0004 protocol is not in its frozen pre-retrieval state."
        raise ValueError(msg)
    if protocol["starting_head"] != STARTING_HEAD:
        msg = "Case 0004 protocol identifies a different starting commit."
        raise ValueError(msg)
    if request.task.identity.value != protocol["task_identity"]:
        msg = "Retained request task identity differs from the protocol."
        raise ValueError(msg)
    if (
        request.full_task_query != protocol["task_full_prompt"]
        or request.full_task_query != protocol["global_lane"]["query_text"]
        or _sha256(request.full_task_query.encode("utf-8")) != protocol["task_sha256"]
    ):
        msg = "Retained complete task query differs from the frozen protocol."
        raise ValueError(msg)
    if request.purpose != protocol["purpose"]:
        msg = "Retained purpose differs from the frozen protocol."
        raise ValueError(msg)
    if str(request.snapshot.repository_id) != protocol["repository_id"]:
        msg = "Retained repository identity differs from the frozen protocol."
        raise ValueError(msg)
    if str(request.snapshot.id) != protocol["snapshot_id"]:
        msg = "Retained snapshot identity differs from the frozen protocol."
        raise ValueError(msg)

    corpus = (
        request.index.corpus_statistics.collection_analysis.document_collection.corpus
    )
    if str(corpus.id) != protocol["eligible_corpus_id"]:
        msg = "Retained corpus identity differs from the frozen protocol."
        raise ValueError(msg)
    if (
        len(request.snapshot.resources) != protocol["frame_resource_count"]
        or len(corpus.resources) != protocol["frame_resource_count"]
        or corpus.resources != request.snapshot.resources
        or request.maximum_results != protocol["bm25"]["maximum_results"]
    ):
        msg = "Retained frame, corpus, or acquisition bound differs from protocol."
        raise ValueError(msg)
    retained_identities = [
        {"address": str(item.address), "content_identity": str(item.content_identity)}
        for item in request.snapshot.resources
    ]
    if retained_identities != protocol["snapshot_resources"]:
        msg = "Retained resource identities differ from the frozen protocol."
        raise ValueError(msg)
    if (
        request.settings.k1 != protocol["bm25"]["k1"]
        or request.settings.b != protocol["bm25"]["b"]
    ):
        msg = "Retained BM25 settings differ from the frozen protocol."
        raise ValueError(msg)

    if len(request.task.anchors) != len(protocol["anchors"]):
        msg = "Retained anchor frame differs from the frozen protocol."
        raise ValueError(msg)
    for anchor, frozen in zip(request.task.anchors, protocol["anchors"], strict=True):
        if (
            anchor.identity.value != frozen["identity"]
            or anchor.text != frozen["text"]
            or str(anchor.provenance.source_identity)
            != frozen["provenance"]["source_identity"]
        ):
            msg = "Retained anchor differs from the frozen protocol."
            raise ValueError(msg)

    obligations = request.task.obligations
    frozen_obligations = protocol["obligations"]
    if len(obligations) != len(frozen_obligations):
        msg = "Retained obligation frame differs from the frozen protocol."
        raise ValueError(msg)
    for obligation, frozen in zip(obligations, frozen_obligations, strict=True):
        if (
            obligation.identity.value != frozen["identity"]
            or obligation.predicate != frozen["predicate"]
            or [anchor.value for anchor in obligation.anchors] != frozen["anchors"]
            or obligation.provenance.source_identity
            != frozen["provenance"]["source_identity"]
            or obligation.provenance.explanation != frozen["provenance"]["explanation"]
            or obligation.requirement is not RequirementStatus.MANDATORY
            or obligation.applicability_condition != frozen["applicability_condition"]
            or obligation.satisfaction.name != frozen["satisfaction"]["name"]
            or obligation.satisfaction.statement != frozen["satisfaction"]["statement"]
            or obligation.witness_alternatives != ()
        ):
            msg = "Retained obligation differs from the frozen protocol."
            raise ValueError(msg)

    if len(request.obligation_queries) != len(protocol["obligation_lanes"]):
        msg = "Retained query lanes differ from the frozen protocol."
        raise ValueError(msg)
    for query, frozen in zip(
        request.obligation_queries, protocol["obligation_lanes"], strict=True
    ):
        if (
            query.identity.value != frozen["identity"]
            or query.obligation.value != frozen["obligation"]
            or query.text != frozen["query_text"]
        ):
            msg = "Retained obligation query differs from the frozen protocol."
            raise ValueError(msg)

    for path, expected_digest in protocol["implementation_sha256"].items():
        current = (ROOT / path).read_text(encoding="utf-8").encode("utf-8")
        if (
            _sha256(current) != expected_digest
            or _sha256(_git_blob(protocol["starting_head"], path)) != expected_digest
        ):
            msg = f"Production implementation differs from frozen source: {path}."
            raise ValueError(msg)


def _serialize_lane(
    *,
    identity: str,
    kind: str,
    obligation_identity: str | None,
    retrieval: RepositoryTextLexicalBm25RetrievalResult,
) -> dict[str, Any]:
    """Serialize every native match and contribution without interpretation."""
    matches: list[dict[str, Any]] = []
    for rank, match in enumerate(retrieval.matches, start=1):
        resource = match.document_statistics.analysis.document.resource
        matches.append(
            {
                "native_rank": rank,
                "resource_address": str(resource.address),
                "content_identity": str(resource.content_identity),
                "score": match.score,
                "content_score": match.content_score,
                "filename_score": match.filename_score,
                "filename_weight": match.filename_weight,
                "weighted_filename_score": match.weighted_filename_score,
                "content_contributions": [
                    {
                        "normalized_term": item.normalized_term,
                        "term_frequency": item.term_frequency,
                        "document_frequency": item.document_frequency,
                        "inverse_document_frequency": item.inverse_document_frequency,
                        "document_length": item.document_length,
                        "average_document_length": item.average_document_length,
                        "contribution": item.contribution,
                    }
                    for item in match.term_contributions
                ],
                "filename_contributions": [
                    {
                        "normalized_term": item.normalized_term,
                        "term_frequency": item.term_frequency,
                        "document_frequency": item.document_frequency,
                        "inverse_document_frequency": item.inverse_document_frequency,
                        "document_length": item.document_length,
                        "average_document_length": item.average_document_length,
                        "contribution": item.contribution,
                    }
                    for item in match.filename_term_contributions
                ],
            }
        )
    return {
        "identity": identity,
        "kind": kind,
        "obligation_identity": obligation_identity,
        "query_text": retrieval.query.text,
        "query_semantics": retrieval.query.QUERY_SEMANTICS,
        "normalized_terms": list(retrieval.query.normalized_terms),
        "query_observations": [
            {
                "encounter_ordinal": item.encounter_ordinal,
                "observed_text": item.observed_text,
                "normalized_term": item.normalized_term,
                "start": item.start,
                "end": item.end,
            }
            for item in retrieval.query.observations
        ],
        "maximum_results": retrieval.maximum_results,
        "settings": {"k1": retrieval.settings.k1, "b": retrieval.settings.b},
        "result_count": len(matches),
        "matches": matches,
    }


def _validate_serialization(
    *,
    lanes: list[dict[str, Any]],
    request: LocalizationLexicalAcquisitionRequest,
    acquisition: LocalizationLexicalAcquisition,
    protocol: dict[str, Any],
) -> None:
    """Check JSON lane order and all native match data before writing outputs."""
    if len(lanes) != 9 or lanes[0]["identity"] != "global-full-task":
        msg = "Serialized acquisition does not contain the frozen nine lanes."
        raise ValueError(msg)
    if len(acquisition.obligation_retrievals) != 8:
        msg = "Native acquisition does not contain eight obligation lanes."
        raise ValueError(msg)
    expected = [
        (
            "global-full-task",
            "global",
            None,
            protocol["global_lane"]["query_text"],
            acquisition.full_task_retrieval,
        ),
        *[
            (
                frozen["identity"],
                "obligation",
                frozen["obligation"],
                frozen["query_text"],
                evidence.retrieval,
            )
            for frozen, evidence in zip(
                protocol["obligation_lanes"],
                acquisition.obligation_retrievals,
                strict=True,
            )
        ],
    ]
    for lane, (identity, kind, obligation, query_text, native) in zip(
        lanes, expected, strict=True
    ):
        rebuilt = _serialize_lane(
            identity=identity,
            kind=kind,
            obligation_identity=obligation,
            retrieval=native,
        )
        if lane != rebuilt or lane["query_text"] != query_text:
            msg = "Serialized lane differs from its native retrieval result."
            raise ValueError(msg)
        if (
            native.maximum_results != request.maximum_results
            or native.settings != request.settings
        ):
            msg = "Native lane settings differ from the frozen request."
            raise ValueError(msg)
        if any(
            item["native_rank"] != index
            for index, item in enumerate(lane["matches"], start=1)
        ):
            msg = "Serialized native match order/ranks are inconsistent."
            raise ValueError(msg)
    if (
        str(acquisition.repository_id) != protocol["repository_id"]
        or str(acquisition.snapshot_id) != protocol["snapshot_id"]
        or acquisition.task != request.task
        or acquisition.purpose != request.purpose
    ):
        msg = "Native aggregate identity differs from the frozen request."
        raise ValueError(msg)


def capture() -> None:
    """Validate Stage A, acquire once, and refuse all result overwrites."""
    if NATIVE_OUTPUT.exists() or JSON_OUTPUT.exists():
        msg = "Case 0004 Stage B output already exists; refusing to overwrite."
        raise FileExistsError(msg)
    protocol_blob = _git_blob(
        STAGE_A, "experiments/codex_dogfood/case_0004/pre_retrieval.json"
    )
    protocol_bytes = _canonical_working_text(PROTOCOL)
    if protocol_bytes != protocol_blob:
        msg = "Frozen Stage A protocol differs from its committed text content."
        raise ValueError(msg)
    protocol = json.loads(protocol_bytes)
    input_bytes = INPUTS.read_bytes()
    for relative, current in (
        (
            "experiments/codex_dogfood/case_0004/README.md",
            _canonical_working_text(CASE / "README.md"),
        ),
        ("experiments/codex_dogfood/case_0004/pre_retrieval.json", protocol_bytes),
        ("experiments/codex_dogfood/case_0004/inputs.pkl.gz", input_bytes),
    ):
        if _git_blob(STAGE_A, relative) != current:
            msg = (
                f"Frozen Stage A artifact differs from its committed blob: {relative}."
            )
            raise ValueError(msg)
    if _sha256(input_bytes) != protocol["inputs_archive_sha256"]:
        msg = "Retained native input archive digest differs from Stage A."
        raise ValueError(msg)
    # The archive is trusted only after its committed SHA-256 has been checked.
    request = pickle.loads(gzip.decompress(input_bytes))  # noqa: S301
    if not isinstance(request, LocalizationLexicalAcquisitionRequest):
        msg = "Retained Case 0004 archive is not the frozen acquisition request."
        raise TypeError(msg)
    _validate_request(protocol, request)
    if (
        subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
        != STAGE_A
    ):
        msg = "Capture must run from the exact Stage A checkpoint."
        raise ValueError(msg)

    start = time.perf_counter()
    acquisition = acquire_localization_lexical_evidence(request)
    runtime_seconds = time.perf_counter() - start

    lanes = [
        _serialize_lane(
            identity="global-full-task",
            kind="global",
            obligation_identity=None,
            retrieval=acquisition.full_task_retrieval,
        ),
        *[
            _serialize_lane(
                identity=evidence.request.identity.value,
                kind="obligation",
                obligation_identity=evidence.request.obligation.value,
                retrieval=evidence.retrieval,
            )
            for evidence in acquisition.obligation_retrievals
        ],
    ]
    _validate_serialization(
        lanes=lanes,
        request=request,
        acquisition=acquisition,
        protocol=protocol,
    )

    native_bytes = gzip.compress(
        pickle.dumps((request, acquisition), protocol=5), mtime=0
    )
    native_digest = _sha256(native_bytes)
    payload = {
        "schema": "codex-obligation-lexical-capture-v1",
        "case": "case_0004",
        "stage": "STAGE B CAPTURED — NOT ADJUDICATED",
        "stage_a_commit": STAGE_A,
        "protocol_sha256": _sha256(protocol_bytes),
        "inputs_archive_sha256": _sha256(input_bytes),
        "native_capture_sha256": native_digest,
        "implementation_commit": protocol["bm25"]["implementation_commit"],
        "implementation_sha256": protocol["implementation_sha256"],
        "python_version": sys.version,
        "uv_lock_sha256": _sha256((ROOT / "uv.lock").read_bytes()),
        "repository_id": str(acquisition.repository_id),
        "snapshot_id": str(acquisition.snapshot_id),
        "corpus_id": protocol["eligible_corpus_id"],
        "eligible_resource_count": protocol["frame_resource_count"],
        "purpose": acquisition.purpose,
        "acquisition_runtime_seconds": runtime_seconds,
        "acquisition_invocation_count": 1,
        "lane_count": len(lanes),
        "lanes": lanes,
    }
    json_bytes = (
        json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8")
    if NATIVE_OUTPUT.exists() or JSON_OUTPUT.exists():
        msg = "Case 0004 Stage B output appeared during capture; refusing overwrite."
        raise FileExistsError(msg)
    NATIVE_OUTPUT.write_bytes(native_bytes)
    JSON_OUTPUT.write_bytes(json_bytes)
    print(
        json.dumps(
            {
                "stage": "STAGE B CAPTURED — NOT ADJUDICATED",
                "lane_count": len(lanes),
                "eligible_resource_count": protocol["frame_resource_count"],
                "acquisition_runtime_seconds": runtime_seconds,
                "capture_sha256": native_digest,
                "retrieval_json_sha256": _sha256(json_bytes),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    capture()
