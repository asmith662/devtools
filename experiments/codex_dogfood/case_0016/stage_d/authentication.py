"""Authenticate reviewed gold and captured returns without treatment execution."""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, ANN401, D103, COM812, PLR2004
import asyncio
import gzip
import json
import sys
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import ROOT, git
from experiments.codex_dogfood.case_0014.stage_d.authentication import Graph
from experiments.codex_dogfood.case_0016.adjudication.reviewed import git_identity
from experiments.codex_dogfood.case_0016.adjudication.reviewed import materialize as m
from experiments.codex_dogfood.case_0016.stage_b import authenticate as a
from experiments.codex_dogfood.case_0016.stage_b import recovery, reporting

GOLD_CHECKPOINT = "fb389ac7eec1b009e6403fc0a076a0fe0f6f3af6"
TREATMENT_CHECKPOINT = "4925f8896edc49b6162d191a6d348f78dd958a48"
START = "ef549d05acbd77edce7769d44f4377169410e80b"
SEAL = "b94bcd6dd1b7b0be12b487da70041c1f72b05fa2aa8234c589ad6b9829d734b0"
RECOVERY_CHECKPOINT = "ceeb6c4da4e2a1db332316239833cf3df6a81831"


def surface(name: str) -> Any:
    path = a.CAPTURE / name
    return json.loads(
        gzip.decompress(path.read_bytes())
        if name.endswith(".gz")
        else path.read_bytes()
    )


async def checkpoints() -> Any:
    for first, second in (
        (a.STAGE_A, RECOVERY_CHECKPOINT),
        (RECOVERY_CHECKPOINT, TREATMENT_CHECKPOINT),
        (TREATMENT_CHECKPOINT, START),
        (START, GOLD_CHECKPOINT),
        (GOLD_CHECKPOINT, "HEAD"),
    ):
        await git("merge-base", "--is-ancestor", first, second)
    stage_a = await a.authenticate()
    sys.stdout.write("Original/amended Stage A seals and replay PASS.\n")
    sys.stdout.flush()
    recovered = await recovery.authenticate_recovery()
    m.require(
        recovered["checkpoint"] == RECOVERY_CHECKPOINT, "Exact recovery checkpoint"
    )
    primary_blobs = await git_identity.verify(GOLD_CHECKPOINT)
    prefix = m.ROOT.relative_to(ROOT).as_posix()
    for name, raw in m.outputs().items():
        m.require(
            await git("show", GOLD_CHECKPOINT + ":" + prefix + "/" + name) == raw,
            "Committed reviewed gold: " + name,
        )
    m.require(
        m.sha((a.CAPTURE / "integrity.json").read_bytes()) == SEAL,
        "Exact authoritative Stage B integrity seal",
    )
    prefix = a.CAPTURE.relative_to(ROOT).as_posix()
    seal = surface("integrity.json")
    m.require(
        await git("show", TREATMENT_CHECKPOINT + ":" + prefix + "/integrity.json")
        == (a.CAPTURE / "integrity.json").read_bytes(),
        "Committed treatment seal",
    )
    important = {n: h for n, h in seal["sha256"].items() if "/" not in n}
    semaphore = asyncio.Semaphore(4)

    async def blob(name: str, expected: str) -> None:
        async with semaphore:
            raw = await git("show", TREATMENT_CHECKPOINT + ":" + prefix + "/" + name)
        m.require(
            m.sha(raw) == expected and raw == (a.CAPTURE / name).read_bytes(),
            "Committed treatment: " + name,
        )

    await asyncio.gather(*(blob(n, h) for n, h in important.items()))
    sys.stdout.write(
        "Recovery, ancestry and committed primary/gold/attempt-2 seals PASS.\n"
    )
    sys.stdout.flush()
    return {
        "starting_checkpoint": START,
        "reviewed_checkpoint": GOLD_CHECKPOINT,
        "treatment_checkpoint": TREATMENT_CHECKPOINT,
        "stage_a": stage_a,
        "recovery": recovered,
        "primary_blob_sha256": primary_blobs,
        "stage_b_integrity_sha256": SEAL,
        "stage_b_top_level_sha256": important,
        "attempt_1": "FAILED_AUDIT_ONLY; authentication only; never treatment input",
        "attempt_2": "AUTHORITATIVE",
    }


def references(flows: Any) -> Any:
    """Bind inert native reference fields to already-validated pair identities."""
    g = Graph(surface("reference_graph.json.gz"))
    edges = g.items(g.fields(g.value["root"])["edges"])
    artifact_hash = surface("integrity.json")["sha256"]["reference_graph.json.gz"]
    result = {}
    for edge, pair in zip(edges, flows["Q1"], strict=True):
        fields = g.fields(edge)
        m.require(
            g.plain(fields["source"])["value"] == pair["source"]
            and g.plain(fields["target"])["value"] == pair["target"],
            "Pair/native edge join",
        )
        for ref, identity in zip(
            g.items(fields["references"]), pair["reference_identities"], strict=True
        ):
            native_fields = g.fields(ref)
            value = {
                k: g.plain(v)
                for k, v in native_fields.items()
                if k
                in (
                    "occurrence",
                    "target_declaration",
                    "derivation_identity",
                    "direct_call",
                    "route",
                )
            }
            target = g.fields(native_fields["target_resource"])
            value["target_resource"] = {
                k: g.plain(v) for k, v in target.items() if k != "content"
            }
            value["retained_route_support"] = {
                k: v
                for k, v in native_fields.items()
                if k not in value and k != "target_resource"
            }
            m.require(identity not in result, "Duplicate native reference identity")
            result[identity] = {
                "identity": identity,
                "source": pair["source"],
                "target": pair["target"],
                "native": value,
                "retained_native_artifact": "reference_graph.json.gz",
                "retained_native_artifact_sha256": artifact_hash,
                "native_graph_reference": ref,
            }
    m.require(len(result) == 3954, "Complete native reference provenance")
    return result


def authenticate(*, native_replay: bool = True) -> Any:
    provenance = asyncio.run(checkpoints())
    seal = surface("integrity.json")
    actual = {
        p.relative_to(a.CAPTURE).as_posix()
        for p in a.CAPTURE.rglob("*")
        if p.is_file() and p.name != "integrity.json"
    }
    m.require(actual == set(seal["sha256"]), "Capture missing/extra files")
    for name, expected in seal["sha256"].items():
        m.require(
            m.sha((a.CAPTURE / name).read_bytes()) == expected,
            "Physical attempt-2 bytes: " + name,
        )
    if native_replay:
        sys.stdout.write(
            "Validating immutable returns and captured algebra; no treatment calls.\n"
        )
        sys.stdout.flush()
        reporting.verify(a.CAPTURE)  # Validates captured objects; no treatment calls.
        sys.stdout.write("Authoritative native captured-return replay PASS.\n")
        sys.stdout.flush()
    return read_inputs(provenance)


def read_inputs(provenance: Any) -> Any:
    """Read inert inputs for metric tests; publication always authenticates first."""
    replay = m.verify()
    gold = m.load(m.ROOT / "reviewed_gold.json")
    summary = surface("summary.json")
    m.require(
        summary["case"] == "0016"
        and summary["execution"] == a.EXECUTION
        and summary["attempt_2"] == "AUTHORITATIVE",
        "Authoritative attempt identity",
    )
    m.require(
        (
            summary["resources"],
            summary["operations"],
            summary["journal_events"],
            summary["retries"],
            summary["failures"],
            summary["python_resources_assessed"],
            summary["native_assessments"],
        )
        == (514, 464, 928, 0, 0, 415, 50725),
        "Captured counters",
    )
    m.require(
        {
            k: summary["graph"][k]
            for k in (
                "nodes",
                "directed_pairs",
                "resolved_occurrences",
                "self_pairs",
                "self_occurrences",
                "dangling_nodes",
            )
        }
        == {
            "nodes": 514,
            "directed_pairs": 561,
            "resolved_occurrences": 3954,
            "self_pairs": 168,
            "self_occurrences": 2405,
            "dangling_nodes": 305,
        },
        "Captured graph",
    )
    m.require(summary["frame"] == gold["frame"], "Exact frame identity")
    marker = surface("execution_started.json")
    m.require(
        marker["case"] == gold["primary"]["case"]
        and marker["frame"] == gold["frame"]
        and marker["stage_a"] == a.STAGE_A
        and marker["recovery_checkpoint"] == RECOVERY_CHECKPOINT,
        "Native execution frame",
    )
    resources = json.loads(gzip.decompress((m.CASE / "resources.json.gz").read_bytes()))
    frame = gold["primary"]["resource_frame"]
    m.require(
        len(resources) == len(frame) == 514
        and [
            {k: r[k] for k in frame[0] if k != "resource_index"} | {"resource_index": i}
            for i, r in enumerate(resources)
        ]
        == frame,
        "Complete native gold bindings",
    )
    data = {
        "provenance": provenance,
        "gold": gold,
        "reviewed_replay": replay,
        "design": m.load(m.CASE / "protocol.json"),
        "resources": resources,
        "summary": summary,
        "costs": surface("costs.json"),
        "publication_costs": surface("publication_costs.json"),
        "arms": {arm: surface("arm_" + arm.lower() + ".json.gz") for arm in "ABC"},
        "states": surface("ppr_states.json.gz"),
        "flows": surface("pair_flows.json.gz"),
        "seeds": surface("exact_seeds_personalization.json.gz"),
    }
    data["references"] = references(data["flows"])
    operations = surface("trace.json")["operations"]
    m.require(
        [(r["operation"], r["runtime_ns"]) for r in data["costs"]["operations"]]
        == [(r["identity"], r["runtime_ns"]) for r in operations],
        "Captured cost identity",
    )
    m.require(
        all(data["costs"][k] == v for k, v in surface("capture_costs.json").items()),
        "Capture cost scopes",
    )
    return data
