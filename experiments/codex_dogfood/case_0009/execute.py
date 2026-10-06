# Copyright (c) 2026
# ruff: noqa: ANN401, C901, COM812, E501, EM101, PLR0912, PLR2004, T201, TRY003 -- bounded case-local JSON/CLI convention
"""Execute the two frozen arms once; verify replay bytes without reranking."""

from __future__ import annotations

import argparse
import gc
import gzip
import json
import pickle
import statistics
import time
import tracemalloc
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from collections.abc import Sequence

from devtools.context.retrieval.lexical.bm25 import (
    RepositoryTextLexicalBm25Match,
    RepositoryTextLexicalBm25RetrievalResult,
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from experiments.codex_dogfood.case_0009.artifacts import (
    CASE,
    binary,
    digest,
    json_bytes,
    put_binary,
    put_json,
    read_json,
)
from experiments.codex_dogfood.case_0009.freeze import (
    canonical_index,
    ensure_absent,
    load_inputs,
    verify,
)
from experiments.codex_dogfood.case_0009.protocol import TASK
from experiments.identifier_sparse.analysis import ANALYZER_SEMANTICS
from experiments.identifier_sparse.index import IdentifierIndex, build_index
from experiments.identifier_sparse.retrieval import (
    SETTINGS,
    IdentifierMatch,
    IdentifierResult,
    retrieve,
)

OUTPUTS = (
    "execution_started.json",
    "results.json.gz",
    "costs.json",
    "stage_b_integrity.json",
)


def _term(item: Any, *, canonical: bool) -> dict[str, Any]:
    """Project native field evidence without changing its measurement semantics."""
    return {
        "term": item.normalized_term if canonical else item.term,
        "tf": item.term_frequency if canonical else item.frequency,
        "df": item.document_frequency,
        "length": item.document_length,
        "average_length": item.average_document_length
        if canonical
        else item.average_length,
        "idf": item.inverse_document_frequency if canonical else item.idf,
        "contribution": item.contribution,
    }


def capture_arm(
    native: dict[str, Any], *, identifier: bool
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Capture positive universes and costs; never consume effectiveness labels."""
    documents = native["documents"]
    gc.collect()
    tracemalloc.start()
    start = time.perf_counter()
    index = build_index(documents) if identifier else canonical_index(documents)
    build_seconds = time.perf_counter() - start
    serialized_index_bytes = len(pickle.dumps(index, protocol=pickle.HIGHEST_PROTOCOL))
    lanes = [
        ("global", None, TASK),
        *[
            (query.identity.value, query.obligation.value, query.text)
            for query in native["queries"]
        ],
    ]
    output = {}
    timings = {}
    for lane, obligation, query in lanes:
        start = time.perf_counter()
        result: IdentifierResult | RepositoryTextLexicalBm25RetrievalResult
        if isinstance(index, IdentifierIndex):
            result = retrieve(index, query, maximum_results=len(documents.documents))
        else:
            result = retrieve_repository_text_documents_by_bm25(
                query=analyze_repository_text_lexical_query(text=query),
                index=index,
                maximum_results=len(documents.documents),
                settings=SETTINGS,
            )
        timings[lane] = time.perf_counter() - start
        rows = []
        matches: Sequence[IdentifierMatch | RepositoryTextLexicalBm25Match]
        if isinstance(result, IdentifierResult):
            matches = result.matches
        else:
            matches = result.matches
        content_evidence: Sequence[object]
        filename_evidence: Sequence[object]
        for rank, candidate in enumerate(matches, start=1):
            item = cast("IdentifierMatch | RepositoryTextLexicalBm25Match", candidate)
            if isinstance(item, IdentifierMatch):
                document = item.document
                content_evidence = item.content_evidence
                filename_evidence = item.filename_evidence
            else:
                document = item.document_statistics.analysis.document
                content_evidence = item.term_contributions
                filename_evidence = item.filename_term_contributions
            rows.append(
                {
                    "address": document.resource.address.value,
                    "content_identity": document.resource.content_identity.value,
                    "rank": rank,
                    "score": item.score,
                    "content_score": item.content_score,
                    "filename_score": item.filename_score,
                    "filename_weight": 0.25,
                    "weighted_filename_score": 0.25 * item.filename_score,
                    "content_terms": [
                        _term(term, canonical=not identifier)
                        for term in content_evidence
                    ],
                    "filename_terms": [
                        _term(term, canonical=not identifier)
                        for term in filename_evidence
                    ],
                }
            )
        output[lane] = {
            "obligation": obligation,
            "query_text": query,
            "query_terms": list(
                result.query_terms
                if isinstance(result, IdentifierResult)
                else result.query.normalized_terms
            ),
            "rows": rows,
        }
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    vocabulary = (
        index.content.vocabulary_size
        if isinstance(index, IdentifierIndex)
        else len(index.term_postings)
    )
    postings = (
        index.content.posting_count
        if isinstance(index, IdentifierIndex)
        else sum(len(item.postings) for item in index.term_postings)
    )
    return output, {
        "index_build_seconds": build_seconds,
        "query_seconds": timings,
        "median_query_seconds": statistics.median(timings.values()),
        "index_plus_query_seconds": build_seconds + sum(timings.values()),
        "traced_peak_bytes": peak,
        "serialized_index_bytes": serialized_index_bytes,
        "content_vocabulary_size": vocabulary,
        "content_posting_count": postings,
        "limitations": "Single execution under tracemalloc, not a latency benchmark. Peak includes evidence projection/serialization. Native A retains richer span objects than B; footprint differences are not solely token expansion. Filename rebuilt per query in both arms. No RSS measurement.",
    }


def execute() -> dict[str, Any]:
    """Publish one exact capture; failure leaves the marker and never auto-retries."""
    ensure_absent(CASE, OUTPUTS)
    manifest = verify()
    put_json(
        CASE / "execution_started.json",
        {
            "execution": "case-0009-stage-b-1",
            "stage_a_integrity_sha256": digest(binary(CASE / "integrity.json")),
            "status": "STARTED; NO AUTOMATIC RETRY",
            "authorization": "frozen treatment execution_authorization",
        },
    )
    native = load_inputs()
    a, cost_a = capture_arm(native, identifier=False)
    b, cost_b = capture_arm(native, identifier=True)
    results = {
        "schema": "case-0009-r1-results-v1",
        "snapshot_id": manifest["snapshot_id"],
        "corpus_id": manifest["corpus_id"],
        "analyzers": {"A": "unicode-word-span-casefold-v1", "B": ANALYZER_SEMANTICS},
        "arms": {"A": a, "B": b},
        "effectiveness": "UNKNOWN; NO GOLD READ",
    }
    put_binary(CASE / "results.json.gz", gzip.compress(json_bytes(results), mtime=0))
    put_json(CASE / "costs.json", {"A": cost_a, "B": cost_b})
    put_json(
        CASE / "stage_b_integrity.json",
        {
            "schema": "case-0009-stage-b-integrity-v1",
            "stage_a_integrity_sha256": digest(binary(CASE / "integrity.json")),
            "deterministic_rankings_sha256": digest(json_bytes(results)),
            "sha256": {name: digest(binary(CASE / name)) for name in OUTPUTS[:-1]},
        },
    )
    return verify_capture()


def verify_capture() -> dict[str, Any]:
    """Replay artifact integrity/score decomposition, without treatment execution."""
    manifest = verify()
    integrity = read_json(CASE / "stage_b_integrity.json")
    if integrity["stage_a_integrity_sha256"] != digest(binary(CASE / "integrity.json")):
        raise ValueError("Stage A lineage changed.")
    if set(integrity["sha256"]) != set(OUTPUTS[:-1]):
        raise ValueError("Stage B artifact coverage differs.")
    for name, expected in integrity["sha256"].items():
        if digest(binary(CASE / name)) != expected:
            raise ValueError("Frozen Stage B bytes differ.")
    results = json.loads(gzip.decompress(binary(CASE / "results.json.gz")))
    if digest(json_bytes(results)) != integrity["deterministic_rankings_sha256"]:
        raise ValueError("Deterministic rankings differ.")
    if (
        results["snapshot_id"] != manifest["snapshot_id"]
        or results["corpus_id"] != manifest["corpus_id"]
    ):
        raise ValueError("Result frame differs.")
    native = load_inputs()
    texts = {
        "global": TASK,
        **{query.identity.value: query.text for query in native["queries"]},
    }
    resources = {
        item["address"]: item["content_identity"] for item in manifest["resources"]
    }
    for arm in ("A", "B"):
        if set(results["arms"][arm]) != set(texts):
            raise ValueError("Query lane coverage differs.")
        for key, lane in results["arms"][arm].items():
            if lane["query_text"] != texts[key]:
                raise ValueError("Arm query text changed.")
            seen = set()
            previous = float("inf")
            for rank, row in enumerate(lane["rows"], start=1):
                if (
                    row["address"] in seen
                    or resources.get(row["address"]) != row["content_identity"]
                ):
                    raise ValueError("Candidate identity differs.")
                seen.add(row["address"])
                if row["rank"] != rank or not 0 < row["score"] <= previous:
                    raise ValueError("Rank ordering differs.")
                previous = row["score"]
                if (
                    abs(
                        row["score"]
                        - row["content_score"]
                        - 0.25 * row["filename_score"]
                    )
                    > 1e-10
                ):
                    raise ValueError("Field score decomposition differs.")
    return {
        "status": "VERIFIED CAPTURE; EFFECTIVENESS UNKNOWN",
        "lanes": len(texts),
        "rankings_sha256": integrity["deterministic_rankings_sha256"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("execute", "verify"))
    args = parser.parse_args()
    print(json.dumps(execute() if args.operation == "execute" else verify_capture()))
