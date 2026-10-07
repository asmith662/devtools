# Copyright (c) 2026
# ruff: noqa: C901, COM812, E501, EM101, TRY003, T201 -- one-run scientific capture
"""Execute each precommitted literal query once with production canonical BM25."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import json
import math
import time
from typing import Any

from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from experiments.codex_dogfood.acquisition.trace import layer, review
from experiments.codex_dogfood.case_0009.artifacts import (
    binary,
    digest,
    git,
    json_bytes,
    put_binary,
    put_json,
    put_text,
    read_json,
)
from experiments.codex_dogfood.case_0009.execute import _term
from experiments.codex_dogfood.case_0009.freeze import canonical_index, ensure_absent
from experiments.codex_dogfood.case_0011.freeze import (
    SEALED,
    load_inputs,
)
from experiments.codex_dogfood.case_0011.freeze import (
    verify as verify_a,
)
from experiments.codex_dogfood.case_0011.protocol import CASE, definition
from experiments.codex_dogfood.case_0011.reporting import stage_b
from experiments.retrieval_diagnostics.adapters import fields, from_rows
from experiments.retrieval_diagnostics.mechanics import Mechanics
from experiments.retrieval_diagnostics.models import Configuration

OUTPUTS = (
    "execution_started.json",
    "results.json.gz",
    "costs.json",
    "trace.json",
    "TRACE.md",
    "STAGE_B_REVIEW.md",
    "stage_b_integrity.json",
)


async def committed_stage_a() -> str:
    """Require every sealed input and concrete implementation already committed."""
    base = "experiments/codex_dogfood/case_0011/"
    commit = (
        (await git("log", "-1", "--format=%H", "--", base + "integrity.json"))
        .decode()
        .strip()
    )
    if not commit:
        raise ValueError("No committed Stage A")
    await git("merge-base", "--is-ancestor", commit, "HEAD")
    for name in (*SEALED, "integrity.json"):
        if await git("show", commit + ":" + base + name) != binary(CASE / name):
            raise ValueError("Stage A is not committed unchanged")
    m = verify_a()
    for path, expected in m["implementation_sha256"].items():
        if digest(await git("show", commit + ":" + path)) != expected:
            raise ValueError("Execution code is not committed")
    return commit


def configuration() -> Configuration:
    """One exact fixed production configuration, never parameter treatments."""
    return Configuration(
        "case-0011-U1-canonical",
        read_json(CASE / "integrity.json")["sha256"]["inputs.pkl.gz"],
        "canonical",
        1.2,
        0.75,
        0.25,
    )


def captures() -> tuple[dict[str, Any], dict[str, Any]]:
    """Run the finite fixed list once; diagnostic work is excluded from timing."""
    t, _, _ = definition()
    native = load_inputs()
    cfg = configuration()
    docs = native["documents"]
    start = time.perf_counter()
    index = canonical_index(docs)
    build_seconds = time.perf_counter() - start
    state = fields(docs, cfg)
    obligations = {o.identity.value: o.identity for o in native["task"].obligations}
    output = {}
    timings = {}
    diagnostic_times = {}
    for q in t["queries"]:
        start = time.perf_counter()
        result = retrieve_repository_text_documents_by_bm25(
            query=analyze_repository_text_lexical_query(text=q["text"]),
            index=index,
            maximum_results=len(docs.documents),
        )
        timings[q["identity"]] = time.perf_counter() - start
        start = time.perf_counter()
        if (
            result.settings.k1 != cfg.k1
            or result.settings.b != cfg.b
            or list(result.query.normalized_terms) != q["analyzed_terms"]
        ):
            raise ValueError("Production configuration or literal query differs")
        rows = [
            {
                "address": match.document_statistics.analysis.document.resource.address.value,
                "content_identity": match.document_statistics.analysis.document.resource.content_identity.value,
                "rank": ordinal,
                "score": match.score,
                "content_score": match.content_score,
                "filename_score": match.filename_score,
                "filename_weight": match.filename_weight,
                "weighted_filename_score": match.weighted_filename_score,
                "content_terms": [
                    _term(term, canonical=True) for term in match.term_contributions
                ],
                "filename_terms": [
                    _term(term, canonical=True)
                    for term in match.filename_term_contributions
                ],
            }
            for ordinal, match in enumerate(result.matches, 1)
        ]
        engine = Mechanics(
            from_rows(
                native["snapshot"],
                docs,
                q["identity"],
                q["text"],
                tuple(q["analyzed_terms"]),
                rows,
                cfg,
                state,
                complete=True,
                obligation=obligations.get(q["obligation"]),
            )
        )
        output[q["identity"]] = {
            "arm": q["arm"],
            "obligation": q["obligation"],
            "information_need": q["information_need"],
            "query_text": q["text"],
            "query_terms": q["analyzed_terms"],
            "route": q["route"],
            "execution_count": 1,
            "rows": rows,
            "query_profile": engine.query_profile(),
        }
        diagnostic_times[q["identity"]] = time.perf_counter() - start
        print("Captured " + q["identity"] + " once; effectiveness UNKNOWN", flush=True)
    return output, {
        "shared_content_index_seconds": build_seconds,
        "query_seconds": timings,
        "diagnostic_seconds": diagnostic_times,
        "timing_scope": "native query analysis and scoring, including native per-query filename index construction; excludes R1.5 projection",
        "query_count": len(timings),
        "sum_query_seconds": math.fsum(timings.values()),
    }


def enrich(
    t: dict[str, Any], result: dict[str, Any], archive_sha: str
) -> dict[str, Any]:
    """Add a result layer to the trace without rewriting Stage A."""
    trace = layer(t, "STAGE_B")
    trace["QUERY"] = [{**q, "execution_status": "EXECUTED_ONCE"} for q in t["queries"]]
    trace["RESULT"] = {
        identity: {
            "execution_count": c["execution_count"],
            "positive_count": len(c["rows"]),
            "rows": [
                {
                    k: r[k]
                    for k in (
                        "address",
                        "content_identity",
                        "rank",
                        "score",
                        "content_score",
                        "filename_score",
                        "weighted_filename_score",
                    )
                }
                for r in c["rows"]
            ],
            "complete_term_evidence": {
                "artifact": "results.json.gz",
                "archive_sha256": archive_sha,
                "locator": "queries/" + identity,
            },
            "profile": c["query_profile"],
        }
        for identity, c in result["queries"].items()
    }
    sets = {i: {r["address"] for r in c["rows"]} for i, c in result["queries"].items()}
    ids = list(sets)
    trace["overlap"] = {
        "pairs": [
            {
                "left": a,
                "right": b,
                "intersection": len(sets[a] & sets[b]),
                "left_only": len(sets[a] - sets[b]),
                "right_only": len(sets[b] - sets[a]),
            }
            for j, a in enumerate(ids)
            for b in ids[j + 1 :]
        ],
        "arms": {
            arm: {
                "query_count": len(group),
                "positive_occurrences": sum(len(s) for s in group),
                "unique_union": len(set().union(*group)),
                "duplicate_occurrences": sum(len(s) for s in group)
                - len(set().union(*group)),
            }
            for arm in "ABC"
            for group in (
                [sets[q["identity"]] for q in t["queries"] if q["arm"] == arm],
            )
        },
    }
    return trace


def run() -> dict[str, Any]:
    """Refuse retry/overwrite before retrieval and persist an exclusive marker."""
    ensure_absent(CASE, OUTPUTS)
    commit = asyncio.run(committed_stage_a())
    m = verify_a()
    put_json(
        CASE / "execution_started.json",
        {
            "stage_a_commit": commit,
            "policy": "exclusive marker; no retries; no implicit reconciliation",
        },
    )
    queries, cost = captures()
    result = {
        "schema": "case-0011-u1-results-v1",
        "frame": {
            k: m[k] for k in ("repository_id", "snapshot_id", "corpus_id", "resources")
        },
        "configuration_identity": configuration().identity,
        "queries": queries,
        "effectiveness": "UNKNOWN",
        "gold_accessed": False,
    }
    raw = json_bytes(result)
    archive = gzip.compress(raw, mtime=0)
    put_binary(CASE / "results.json.gz", archive)
    put_json(CASE / "costs.json", cost)
    t, _, _ = definition()
    trace = enrich(t, result, digest(archive))
    put_json(CASE / "trace.json", trace)
    report = stage_b(t, result, trace, cost)
    put_text(CASE / "STAGE_B_REVIEW.md", report)
    put_text(
        CASE / "TRACE.md",
        "# Case 0011 acquisition trace\n\n" + review(t) + "\n" + report,
    )
    put_json(
        CASE / "stage_b_integrity.json",
        {
            "stage_a_commit": commit,
            "archive_sha256": digest(archive),
            "canonical_payload_sha256": digest(raw),
            "sha256": {n: digest(binary(CASE / n)) for n in OUTPUTS[:-1]},
        },
    )
    return verify()


def verify() -> dict[str, Any]:
    """Replay scores, universes, trace and reports; do not rerun native queries."""
    m = verify_a()
    native = load_inputs()
    seal = read_json(CASE / "stage_b_integrity.json")
    for name, expected in seal["sha256"].items():
        if digest(binary(CASE / name)) != expected:
            raise ValueError("Stage B hash differs")
    raw = gzip.decompress(binary(CASE / "results.json.gz"))
    if digest(raw) != seal["canonical_payload_sha256"]:
        raise ValueError("Stage B payload hash differs")
    r = json.loads(raw)
    t, _, _ = definition()
    if (
        set(r["queries"]) != {q["identity"] for q in t["queries"]}
        or r["frame"]
        != {k: m[k] for k in ("repository_id", "snapshot_id", "corpus_id", "resources")}
        or r["configuration_identity"] != configuration().identity
        or r["gold_accessed"]
        or r["effectiveness"] != "UNKNOWN"
    ):
        raise ValueError("Result frame/query partition differs")
    cfg = configuration()
    state = fields(native["documents"], cfg)
    obs = {o.identity.value: o.identity for o in native["task"].obligations}
    for q in t["queries"]:
        c = r["queries"][q["identity"]]
        if (
            c["query_text"] != q["text"]
            or c["query_terms"] != q["analyzed_terms"]
            or c["execution_count"] != 1
            or any(
                c[k] != q[k] for k in ("arm", "obligation", "information_need", "route")
            )
        ):
            raise ValueError("Literal query or linkage changed")
        engine = Mechanics(
            from_rows(
                native["snapshot"],
                native["documents"],
                q["identity"],
                q["text"],
                tuple(q["analyzed_terms"]),
                c["rows"],
                cfg,
                state,
                complete=True,
                obligation=obs.get(q["obligation"]),
            )
        )
        if engine.query_profile() != c["query_profile"]:
            raise ValueError("Term profile replay differs")
    trace = enrich(t, r, seal["archive_sha256"])
    if trace != read_json(CASE / "trace.json") or trace["JUDGMENT"] or trace["FAILURE"]:
        raise ValueError("Trace replay or pre-gold boundary differs")
    cost = read_json(CASE / "costs.json")
    if (
        set(cost["query_seconds"]) != set(r["queries"])
        or cost["query_count"] != len(r["queries"])
        or cost["sum_query_seconds"] != math.fsum(cost["query_seconds"].values())
    ):
        raise ValueError("Cost capture differs")
    if stage_b(t, r, trace, cost).encode() != binary(CASE / "STAGE_B_REVIEW.md"):
        raise ValueError("Human review replay differs")
    if (
        "# Case 0011 acquisition trace\n\n"
        + review(t)
        + "\n"
        + stage_b(t, r, trace, cost)
    ).encode() != binary(CASE / "TRACE.md"):
        raise ValueError("Full trace Markdown replay differs")
    return {
        "status": "R1.5/trace replay PASSED",
        "queries": len(r["queries"]),
        "effectiveness": "UNKNOWN",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("run", "verify"))
    args = parser.parse_args()
    print(run() if args.operation == "run" else verify())
