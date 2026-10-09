# Copyright (c) 2026
# ruff: noqa: E501, PLR0915, PLR2004, EM101, TRY003, COM812 -- finite inputs; formatter owns commas
"""Authenticate Case 0011 lineage, retained inputs and diagnostic replay."""

from __future__ import annotations

import asyncio
import gzip
import io
import itertools
import json
import math
import pickle
import sys
import tarfile
from collections import Counter
from collections.abc import Hashable, Iterable
from typing import Any

from devtools.evaluation.coverage import compare_identity_coverage
from experiments.codex_dogfood.acquisition.trace import review
from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    git,
    read_json,
)
from experiments.codex_dogfood.case_0011.adjudication.reviewed import (
    build_reviewed_gold as reviewed,
)
from experiments.codex_dogfood.case_0011.adjudication.stage_c5.reviewed import (
    materialize_reviewed_c5 as c5,
)
from experiments.codex_dogfood.case_0011.execute import configuration, enrich
from experiments.codex_dogfood.case_0011.protocol import CASE, definition
from experiments.codex_dogfood.case_0011.reporting import stage_b
from experiments.retrieval_diagnostics.adapters import fields, from_rows
from experiments.retrieval_diagnostics.mechanics import Mechanics

START = "471acb53b131ccb51d5c5799cb8933624700af33"

CHAIN = (
    ("Stage A", "9b8f0f65fc34bdad0f1a4a7c2ec0077278555ae9"),
    ("Stage B", "65e8f22587c11eb54684861ba39e3e7acc7def03"),
    ("primary gold", "1ae9b07c69d2fec89b5735db12a81bff30d91702"),
    ("reviewed gold", "918e90bc3c01aaf54621e52d8c0435396005239a"),
    ("primary C.5", "d16ca97b506627ccd5bdfa9e5fc11cc0333015f1"),
    ("C.5 reliability", "53e1681d2bbea393bdf7233a279dd176f0d780ee"),
    ("reconciliation v2 protocol", "d242ed95c85c3b74ae71e16aae9b82e0b6d68b39"),
    ("final reviewed C.5", START),
)

LABELS = ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")


def require(condition: bool, message: str) -> None:  # noqa: FBT001 -- condition assertion
    """Fail closed before publishing any derived evidence."""
    if not condition:
        raise ValueError(message)


def exact[Identity: Hashable](
    expected: Iterable[Identity],
    observed: Iterable[Identity],
) -> None:
    """Reuse canonical identity coverage to reject duplicate/missing/unexpected joins."""
    require(
        compare_identity_coverage(expected=expected, observed=observed).is_exact,
        "Identity coverage differs",
    )


def unique(rows: list[dict[str, Any]], key: str) -> dict[str, Any]:
    """Reject duplicate semantic identities before indexing."""
    result = {r[key]: r for r in rows}
    exact(result, [r[key] for r in rows])
    return result


async def provenance() -> dict[str, Any]:
    """Verify ancestry and exact selected committed artifacts through managed Git."""
    relative = CASE.relative_to(ROOT).as_posix()
    scopes = (
        [*read_json(CASE / "integrity.json")["sha256"], "integrity.json"],
        [
            *read_json(CASE / "stage_b_integrity.json")["sha256"],
            "stage_b_integrity.json",
        ],
        [
            "adjudication/judgments.json",
            "adjudication/judgments.sha256",
            "adjudication/gold_statistics.json",
        ],
        [
            "adjudication/reviewed",
            "C5_PROTOCOL.md",
            "adjudication/stage_c5/packet.json.gz",
            "adjudication/stage_c5/manifest.json",
            "adjudication/stage_c5/integrity.json",
            "adjudication/stage_c5/projection_audit.json",
        ],
        ["adjudication/stage_c5/results"],
        [
            "adjudication/stage_c5/reliability",
            "adjudication/stage_c5/results/PUBLICATION.md",
        ],
        [
            "adjudication/stage_c5/reconciliation_v2/packet",
            "adjudication/stage_c5/reconciliation_v2/build_packet.py",
        ],
        [
            "adjudication/stage_c5/reviewed",
            "adjudication/stage_c5/reconciliation_v2/results",
        ],
    )
    records = []
    for i, ((stage, commit), paths) in enumerate(zip(CHAIN, scopes, strict=True)):
        if i:
            ancestor = (
                (await git("merge-base", CHAIN[i - 1][1], commit)).decode().strip()
            )
            require(ancestor == CHAIN[i - 1][1], "Frozen-chain ancestry differs")
        archive = await git(
            "-c",
            "core.autocrlf=false",
            "archive",
            "--format=tar",
            commit,
            "--",
            *(f"{relative}/{p}" for p in paths),
        )
        hashes = {}
        with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
            for member in bundle.getmembers():
                if member.isdir():
                    continue
                require(member.isfile(), "Unexpected committed artifact kind")
                stream = bundle.extractfile(member)
                require(stream is not None, "Missing committed bytes")
                if stream is None:
                    raise ValueError("Missing committed bytes")
                raw = stream.read()
                if i == 0 and member.name == f"{relative}/C5_PROTOCOL.md":
                    require(
                        digest(raw)
                        == read_json(CASE / "integrity.json")["sha256"][
                            "C5_PROTOCOL.md"
                        ],
                        "Historical Stage A C.5 protocol differs",
                    )
                elif i == 4 and member.name.endswith("/results/PUBLICATION.md"):
                    require(
                        digest(raw)
                        == "c0268363cdfc9b160208027fde1b8f0eabddf69848d397c8f512c812bc49c6fe",
                        "Historical primary C.5 publication differs",
                    )
                else:
                    require(
                        (ROOT / member.name).read_bytes() == raw,
                        f"Committed artifact differs: {member.name}",
                    )
                hashes[member.name] = digest(raw)
        require(bool(hashes), "Empty committed artifact scope")
        records.append(
            {
                "stage": stage,
                "commit": commit,
                "subject": (await git("show", "-s", "--format=%s", commit))
                .decode()
                .strip(),
                "artifact_sha256": hashes,
            },
        )
    return {
        "starting_head": START,
        "chain": records,
        "ancestry": "PASSED",
        "immutable_artifacts": "PASSED",
        "protocol_supersession": "Only C5_PROTOCOL.md was revised at 918e90bc. Both committed versions are verified; the original Stage A current-worktree verifier consequently fails. Treatment and captured artifacts remain exact.",
    }


def source() -> dict[str, Any]:
    """Authenticate the final semantics, then bind every native/captured identity."""
    seal_a = read_json(CASE / "integrity.json")
    for name, expected in seal_a["sha256"].items():
        if name == "C5_PROTOCOL.md":
            require(
                digest(binary(CASE / name))
                == "d47f381c96090409d3a615f4802ca4ea5279f171a8395fc6a7492aa8a6dda7b0",
                "Reviewed protocol supersession differs",
            )
        else:
            require(
                digest(binary(CASE / name)) == expected,
                "Stage A sealed input differs",
            )
    manifest_a = read_json(CASE / "pre_execution.json")
    require(manifest_a["python"] == sys.version, "Frozen runtime differs")
    for name, expected in manifest_a["implementation_sha256"].items():
        require(
            digest(binary(ROOT / name)) == expected,
            "Frozen execution code differs",
        )
    native = pickle.loads(gzip.decompress(binary(CASE / "inputs.pkl.gz")))  # noqa: S301 -- exact hash-verified repository-owned native archive
    for path, raw in reviewed.artifacts().items():
        require(path.read_bytes() == raw, "Reviewed task-gold replay differs")
    c5_inputs = c5.source_inputs()
    c5.validate_completed(c5.ROOT, c5_inputs)
    semantic = c5.build(c5_inputs)
    gold = read_json(CASE / "adjudication/reviewed/reviewed_gold.json")
    stats = read_json(CASE / "adjudication/reviewed/reviewed_statistics.json")
    treatment = read_json(CASE / "treatment.json")
    projected = definition()[0]
    require(treatment == projected, "Frozen treatment definition differs")
    treatment = projected  # Restore sealed dict order for historical Markdown repr.
    seal = read_json(CASE / "stage_b_integrity.json")
    for name, expected in seal["sha256"].items():
        require(digest(binary(CASE / name)) == expected, "Stage B hash differs")
    raw = gzip.decompress(binary(CASE / "results.json.gz"))
    require(digest(raw) == seal["canonical_payload_sha256"], "Capture payload differs")
    capture = json.loads(raw)
    require(
        set(costs := read_json(CASE / "costs.json")["query_seconds"])
        == set(capture["queries"]),
        "Captured cost query frame differs",
    )
    cost_artifact = read_json(CASE / "costs.json")
    require(
        cost_artifact["query_count"] == 28
        and cost_artifact["sum_query_seconds"] == math.fsum(costs.values()),
        "Captured cost arithmetic differs",
    )
    projection = read_json(CASE / "adjudication/stage_c5/projection_audit.json")
    packet = json.loads(
        gzip.decompress(binary(CASE / "adjudication/stage_c5/packet.json.gz")),
    )
    require(gold["frame"] == packet["frame"], "Case/task/frame identity differs")
    require(
        gold["frame"]["case_identity"] == "case-0011"
        and gold["frame"]["task_identity"] == treatment["task_identity"],
        "Task identity differs",
    )
    require(
        gold["task"]
        == packet["task"]
        == treatment["task"]
        == binary(CASE / "task.txt").decode(),
        "Task text differs",
    )
    require(
        gold["frozen_obligations"] == packet["obligations"] == treatment["obligations"],
        "Obligation definitions differ",
    )
    for k in ("repository_id", "snapshot_id", "corpus_id"):
        require(capture["frame"][k] == gold["frame"][k], "Capture frame differs")
    require(
        str(native["snapshot"].repository_id) == gold["frame"]["repository_id"]
        and str(native["snapshot"].id) == gold["frame"]["snapshot_id"]
        and str(native["corpus"].id) == gold["frame"]["corpus_id"],
        "Native frame identity differs",
    )
    require(capture["frame"]["resources"] == 531, "Captured resource count differs")
    contents = {d.resource.address.value: d.text for d in native["documents"].documents}
    identities = {
        d.resource.address.value: str(d.resource.content_identity)
        for d in native["documents"].documents
    }
    resources = unique(gold["resources"], "address")
    require(
        len(resources) == len(contents) == 531
        and {p: r["content_identity"] for p, r in resources.items()} == identities,
        "531-resource content join differs",
    )
    _, _, _, raw_resources = reviewed.verify_inputs()
    require(
        contents == {r["address"]: r["content"] for r in raw_resources},
        "Frozen resource texts differ",
    )
    cells = {(r["obligation"], r["address"]): r for r in gold["cells"]}
    obligations = unique(treatment["obligations"], "identity")
    require(
        len(cells) == len(gold["cells"]) == 4779
        and set(cells) == set(itertools.product(obligations, contents)),
        "Gold cell partition differs",
    )
    require(
        Counter(r["label"] for r in cells.values())
        == {"REQUIRED": 23, "HELPFUL_ONLY": 84, "UNNECESSARY": 4672},
        "Reviewed labels differ",
    )
    unit_projection = projection["unit_projection"]
    units = {unit_projection[u["id"]]: u for u in gold["units"]}
    coverage = unique(semantic["unit_coverage"], "unit")
    require(
        len(units) == len(coverage) == 32 and units.keys() == coverage.keys(),
        "Required unit partition differs",
    )
    for uid, u in units.items():
        statement = u["statement"]
        for original, replacement in projection["location_substitutions"].items():
            statement = statement.replace(original, replacement)
        require(statement == coverage[uid]["statement"], "Exact unit statement differs")
    needs = unique(treatment["information_needs"], "identity")
    require(
        len(needs) == 18
        and [(n["identity"], n["statement"]) for n in packet["information_needs"]]
        == [(n["identity"], n["statement"]) for n in treatment["information_needs"]],
        "Frozen needs differ",
    )
    mappings = {(m["need"], m["unit"]): m for m in semantic["mappings"]}
    require(
        len(mappings) == len(semantic["mappings"]) == 576
        and set(mappings) == set(itertools.product(needs, units)),
        "Need/unit mapping partition differs",
    )
    queries = unique(treatment["queries"], "identity")
    require(
        set(capture["queries"]) == set(queries)
        and Counter(q["arm"] for q in queries.values()) == {"A": 1, "B": 9, "C": 18},
        "Treatment query partition differs",
    )
    require(
        treatment["parameters"] == [1.2, 0.75, 0.25]
        and treatment["analyzer"] == "canonical"
        and treatment["fusion"] in (False, "NONE"),
        "Frozen route differs",
    )
    require(
        capture["configuration_identity"] == configuration().identity,
        "Canonical captured configuration differs",
    )
    validate_queries(queries, capture, contents, identities)
    require(
        {q["obligation"] for q in queries.values() if q["arm"] == "B"}
        == set(obligations),
        "B obligations differ",
    )
    require(
        {q["information_need"] for q in queries.values() if q["arm"] == "C"}
        == set(needs),
        "C need queries differ",
    )
    require(
        next(q["text"] for q in queries.values() if q["arm"] == "A")
        == treatment["task"],
        "A is not exact whole task",
    )
    require(
        stats["combination_count"] == 6
        and sum(len(o["alternatives"]) for o in gold["obligations"]) == 12,
        "Alternative frame differs",
    )
    global_labels = {
        p: next(
            k
            for k in LABELS
            if any(
                c["label"] == k for (ob, address), c in cells.items() if address == p
            )
        )
        for p in contents
    }
    return {
        "gold": gold,
        "gold_statistics": stats,
        "semantic": semantic,
        "treatment": treatment,
        "capture": capture,
        "contents": contents,
        "cells": cells,
        "units": units,
        "coverage": coverage,
        "needs": needs,
        "queries": queries,
        "projection": projection,
        "global_labels": global_labels,
        "native": native,
        "costs": cost_artifact,
    }


def replay_diagnostics(s: dict[str, Any]) -> dict[str, Any]:
    """Reconstruct diagnostics from captured rows; native retrieval is never called."""
    native, t, r = s["native"], s["treatment"], s["capture"]
    cfg = configuration()
    state = fields(native["documents"], cfg)
    obs = {o.identity.value: o.identity for o in native["task"].obligations}
    explanations: dict[str, Any] = {}
    for q in t["queries"]:
        c = r["queries"][q["identity"]]
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
            ),
        )
        require(
            engine.query_profile() == c["query_profile"],
            "R1.5 captured term profile replay differs",
        )
        targets = set(s["gold_statistics"]["required_resource_union"]) | {
            row["address"] for row in c["rows"][:5]
        }
        explanations[q["identity"]] = {}
        for address in sorted(targets):
            explanation = engine.explain(engine.resources[address])
            if explanation["captured_score"] is not None:
                require(
                    explanation["score_reconstructed"], "R1.5 explanation score differs"
                )
            explanations[q["identity"]][address] = explanation
    s["r15_explanations"] = explanations
    ordered = {
        **r,
        "queries": {q["identity"]: r["queries"][q["identity"]] for q in t["queries"]},
    }
    trace = enrich(
        t,
        ordered,
        read_json(CASE / "stage_b_integrity.json")["archive_sha256"],
    )
    require(
        trace == read_json(CASE / "trace.json"),
        "Sealed Stage B trace replay differs",
    )
    b = stage_b(t, r, trace, read_json(CASE / "costs.json"))
    require(
        b.encode() == binary(CASE / "STAGE_B_REVIEW.md"),
        "Stage B review replay differs",
    )
    require(
        ("# Case 0011 acquisition trace\n\n" + review(t) + "\n" + b).encode()
        == binary(CASE / "TRACE.md"),
        "Sealed Stage B Markdown trace differs",
    )
    return {
        "status": "PASSED",
        "queries": 28,
        "native_queries_executed": 0,
        "representative_explanations": sum(len(rows) for rows in explanations.values()),
        "score_reconstruction": "PASSED",
        "scope": "R1.5 profiles, sealed B machine/human trace; Stage A C5_PROTOCOL supersession separately authenticated.",
    }


def load() -> dict[str, Any]:
    """Use one authenticated input loader and replay every captured R1.5 lane."""
    require(
        sys.flags.optimize == 0,
        "Scientific validators require Python assertions enabled",
    )
    sys.dont_write_bytecode = True
    proof = asyncio.run(provenance())
    data = source()
    data["provenance"] = proof
    data["diagnostic_replay"] = replay_diagnostics(data)
    return data


def validate_queries(
    queries: dict[str, Any],
    capture: dict[str, Any],
    contents: dict[str, str],
    identities: dict[str, str],
) -> None:
    """Validate every exact query, result identity, score sum and stable tie."""
    order = {p: i for i, p in enumerate(contents)}
    for qid, q in queries.items():
        c = capture["queries"][qid]
        require(
            c["query_text"] == q["text"]
            and c["query_terms"] == q["analyzed_terms"]
            and c["execution_count"] == 1,
            "Captured query text/terms/count differs",
        )
        require(
            all(
                c[k] == q[k] for k in ("arm", "obligation", "information_need", "route")
            ),
            "Query ownership/route differs",
        )
        rows = unique(c["rows"], "address")
        require(set(rows) <= set(contents), "Unexpected captured resource")
        require(
            c["rows"]
            == sorted(c["rows"], key=lambda r: (-r["score"], order[r["address"]])),
            "Captured tie order differs",
        )
        for rank, r in enumerate(c["rows"], 1):
            require(
                r["rank"] == rank
                and r["score"] > 0
                and r["content_identity"] == identities[r["address"]],
                "Result identity/rank differs",
            )
            require(
                math.isclose(
                    r["score"],
                    r["content_score"] + 0.25 * r["filename_score"],
                    abs_tol=1e-10,
                ),
                "Field score differs",
            )
            for field in ("content", "filename"):
                require(
                    math.isclose(
                        r[f"{field}_score"],
                        math.fsum(t["contribution"] for t in r[f"{field}_terms"]),
                        abs_tol=1e-10,
                    ),
                    "Term contributions differ",
                )
