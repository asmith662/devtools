# Copyright (c) 2026
# ruff: noqa: C901, COM812, EM101, TRY003, T201 -- retained scientific replay
"""Post-capture replay erratum: preserve frozen query order after JSON decoding.

The original execute.py and every Stage A/B byte remain unchanged. This verifier
retains its checks and restores ordering solely for the derived overlap trace.
It cannot execute retrieval or overwrite any artifact.
"""

from __future__ import annotations

import gzip
import json
import math
from typing import Any

from experiments.codex_dogfood.acquisition.trace import review
from experiments.codex_dogfood.case_0009.artifacts import binary, digest, read_json
from experiments.codex_dogfood.case_0011.execute import configuration, enrich
from experiments.codex_dogfood.case_0011.freeze import load_inputs
from experiments.codex_dogfood.case_0011.freeze import verify as verify_a
from experiments.codex_dogfood.case_0011.protocol import CASE, definition
from experiments.codex_dogfood.case_0011.reporting import stage_b
from experiments.retrieval_diagnostics.adapters import fields, from_rows
from experiments.retrieval_diagnostics.mechanics import Mechanics


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
    # Restore the sealed execution order after canonical JSON sorted object keys.
    ordered = {
        **r,
        "queries": {q["identity"]: r["queries"][q["identity"]] for q in t["queries"]},
    }
    trace = enrich(t, ordered, seal["archive_sha256"])
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
    print(verify())
