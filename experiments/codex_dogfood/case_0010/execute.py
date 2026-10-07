# Copyright (c) 2026
# ruff: noqa: C901, COM812, E501, EM101, TRY003, T201 -- bounded prospective capture
"""Execute parameter arms once, then replay captured evidence without scoring."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import json
import math
import statistics
import time
from dataclasses import replace
from typing import Any

from devtools.context.retrieval.lexical.filename import (
    build_repository_text_filename_lexical_index,
)
from experiments.bm25_sensitivity.scoring import retrieve
from experiments.codex_dogfood.case_0009.artifacts import (
    binary,
    digest,
    git,
    json_bytes,
    put_binary,
    put_json,
    read_json,
)
from experiments.codex_dogfood.case_0009.execute import _term
from experiments.codex_dogfood.case_0009.freeze import canonical_index, ensure_absent
from experiments.codex_dogfood.case_0010.freeze import CASE, load_inputs
from experiments.codex_dogfood.case_0010.freeze import verify as verify_a
from experiments.codex_dogfood.case_0010.protocol import TASK
from experiments.retrieval_diagnostics.adapters import fields, from_rows
from experiments.retrieval_diagnostics.mechanics import Mechanics
from experiments.retrieval_diagnostics.models import Configuration

OUTPUTS = (
    "execution_started.json",
    "results.json.gz",
    "costs.json",
    "stage_b_integrity.json",
)


def configuration(arm: dict[str, Any]) -> Configuration:
    """Include exact parameters and shared frozen frame in diagnostic identity."""
    p = arm["parameters"]
    return Configuration(
        "case-0010-" + arm["arm"],
        read_json(CASE / "integrity.json")["sha256"]["inputs.pkl.gz"],
        "canonical",
        *p,
    )


async def require_stage_a_commit() -> str:
    """Stop unless prospective Stage A is already committed unchanged."""
    path = "experiments/codex_dogfood/case_0010/integrity.json"
    commit = (await git("log", "-1", "--format=%H", "--", path)).decode().strip()
    if not commit or digest(await git("show", commit + ":" + path)) != digest(
        binary(CASE / "integrity.json")
    ):
        raise ValueError("Stage A is not committed unchanged.")
    await git("merge-base", "--is-ancestor", commit, "HEAD")
    return commit


def run() -> dict[str, Any]:
    """No gold join; every frozen query executes once per arm."""
    ensure_absent(CASE, OUTPUTS)
    manifest = verify_a()
    commit = asyncio.run(require_stage_a_commit())
    native = load_inputs()
    treatment = read_json(CASE / "treatment.json")
    put_json(
        CASE / "execution_started.json",
        {
            "stage_a_commit": commit,
            "policy": "Exclusive marker: no retries/overwrites",
            "effectiveness": "UNKNOWN",
        },
    )
    docs = native["documents"]
    start = time.perf_counter()
    index = canonical_index(docs)
    filename = build_repository_text_filename_lexical_index(document_collection=docs)
    build_time = time.perf_counter() - start
    lanes = [
        ("global", None, TASK),
        *[(q.identity.value, q.obligation, q.text) for q in native["queries"]],
    ]
    source_fields = fields(docs, configuration(treatment["arms"][0]))
    output = {}
    costs: dict[str, Any] = {
        "shared_index_build_seconds": build_time,
        "index_reused_all_arms": True,
        "diagnostics_excluded_from_query_cost": True,
        "arms": {},
    }
    for arm in treatment["arms"]:
        config = configuration(arm)
        field_state = tuple(
            replace(f, weight=config.filename_weight if f.name == "filename" else 1.0)
            for f in source_fields
        )
        captured = {}
        timings = {}
        diagnostic_seconds = 0.0
        for identity, ob, text in lanes:
            start = time.perf_counter()
            result = retrieve(index, filename, text, config)
            timings[identity] = time.perf_counter() - start
            start = time.perf_counter()
            rows = [
                {
                    "address": m.document_statistics.analysis.document.resource.address.value,
                    "content_identity": m.document_statistics.analysis.document.resource.content_identity.value,
                    "rank": rank,
                    "score": m.score,
                    "content_score": m.content_score,
                    "filename_score": m.filename_score,
                    "filename_weight": config.filename_weight,
                    "weighted_filename_score": m.weighted_filename_score,
                    "content_terms": [
                        _term(t, canonical=True) for t in m.term_contributions
                    ],
                    "filename_terms": [
                        _term(t, canonical=True) for t in m.filename_term_contributions
                    ],
                }
                for rank, m in enumerate(result.matches, 1)
            ]
            capture = from_rows(
                native["snapshot"],
                docs,
                identity,
                text,
                result.query.normalized_terms,
                rows,
                config,
                field_state,
                complete=True,
                obligation=ob,
            )
            Mechanics(
                capture
            )  # validates every term/score/universe/tie against frozen statistics
            diagnostic_seconds += time.perf_counter() - start
            captured[identity] = {
                "obligation": ob.value if ob else None,
                "query_text": text,
                "query_terms": list(result.query.normalized_terms),
                "rows": rows,
            }
        values = sorted(timings.values())
        output[arm["arm"]] = {
            "configuration_identity": config.identity,
            "parameters": arm["parameters"],
            "lanes": captured,
        }
        costs["arms"][arm["arm"]] = {
            "query_seconds": timings,
            "median_query_seconds": statistics.median(values),
            "p95_query_seconds": values[math.ceil(0.95 * len(values)) - 1],
            "sum_query_seconds": sum(values),
            "diagnostic_validation_seconds": diagnostic_seconds,
        }
        print(
            f"Captured arm {arm['arm']}: {len(lanes)} exact one-time queries; effectiveness UNKNOWN",
            flush=True,
        )
    payload = {
        "schema": "case-0010-parameter-capture-v1",
        "repository_id": manifest["repository_id"],
        "snapshot_id": manifest["snapshot_id"],
        "corpus_id": manifest["corpus_id"],
        "resource_count": manifest["resources"],
        "task_sha256": manifest["task_sha256"],
        "arms": output,
        "effectiveness": "UNKNOWN",
        "gold_accessed": False,
    }
    raw = json_bytes(payload)
    put_binary(CASE / "results.json.gz", gzip.compress(raw, mtime=0))
    put_json(CASE / "costs.json", costs)
    put_json(
        CASE / "stage_b_integrity.json",
        {
            "stage_a_commit": commit,
            "archive_sha256": digest(binary(CASE / "results.json.gz")),
            "canonical_payload_sha256": digest(raw),
            "sha256": {n: digest(binary(CASE / n)) for n in OUTPUTS[:-1]},
        },
    )
    return verify()


def verify() -> dict[str, Any]:
    """Reconstruct every captured score/rank universe through R1.5, no second run."""
    native = load_inputs()
    seal = read_json(CASE / "stage_b_integrity.json")
    for name, expected in seal["sha256"].items():
        if digest(binary(CASE / name)) != expected:
            raise ValueError("Frozen capture changed.")
    raw = gzip.decompress(binary(CASE / "results.json.gz"))
    if (
        digest(raw) != seal["canonical_payload_sha256"]
        or digest(binary(CASE / "results.json.gz")) != seal["archive_sha256"]
    ):
        raise ValueError("Capture digest scope differs.")
    payload = json.loads(raw)
    manifest = verify_a()
    for key in ("repository_id", "snapshot_id", "corpus_id", "task_sha256"):
        if payload[key] != manifest[key]:
            raise ValueError("Capture frame differs.")
    treatment = read_json(CASE / "treatment.json")
    if set(payload["arms"]) != {a["arm"] for a in treatment["arms"]}:
        raise ValueError("Arm coverage differs.")
    lanes = {
        "global": (None, TASK),
        **{q.identity.value: (q.obligation, q.text) for q in native["queries"]},
    }
    common = fields(native["documents"], configuration(treatment["arms"][0]))
    for arm in treatment["arms"]:
        captured = payload["arms"][arm["arm"]]
        config = configuration(arm)
        if (
            config.identity != captured["configuration_identity"]
            or arm["parameters"] != captured["parameters"]
            or set(captured["lanes"]) != set(lanes)
        ):
            raise ValueError("Configuration/query coverage differs.")
        field_state = tuple(
            replace(f, weight=config.filename_weight if f.name == "filename" else 1.0)
            for f in common
        )
        for identity, (ob, text) in lanes.items():
            lane = captured["lanes"][identity]
            if lane["query_text"] != text or lane["obligation"] != (
                ob.value if ob else None
            ):
                raise ValueError("Query identity differs.")
            Mechanics(
                from_rows(
                    native["snapshot"],
                    native["documents"],
                    identity,
                    text,
                    tuple(lane["query_terms"]),
                    lane["rows"],
                    config,
                    field_state,
                    complete=True,
                    obligation=ob,
                )
            )
    if (
        payload["resource_count"] != manifest["resources"]
        or payload["effectiveness"] != "UNKNOWN"
        or payload["gold_accessed"]
    ):
        raise ValueError("Frame or stopping boundary differs.")
    return {
        "status": "R1.5 exact score/universe replay PASSED",
        "arms": len(payload["arms"]),
        "lanes_per_arm": len(lanes),
        "effectiveness": "UNKNOWN",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("run", "verify"))
    args = parser.parse_args()
    print(run() if args.operation == "run" else verify())
