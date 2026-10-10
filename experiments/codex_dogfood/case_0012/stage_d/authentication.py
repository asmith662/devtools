"""Authenticate captured bytes and historical checkpoints without native execution.

Only explicitly named Case 0012 artifacts are read. Native pickle data is never
loaded. Git access uses the existing managed command adapter. JSON/byte I/O is
the bounded experimental publication boundary, not a framework Resource API.
"""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, ANN401, D103, COM812, PLR2004
import asyncio
import gzip
import json
from itertools import pairwise
from pathlib import Path
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import binary, git
from experiments.codex_dogfood.case_0012.adjudication.reviewed import (
    materialize as gold_builder,
)

encoded, sha, require, load = (
    gold_builder.encoded,
    gold_builder.sha,
    gold_builder.require,
    gold_builder.load,
)
ROOT = Path(__file__).resolve().parent
CASE = ROOT.parent
CAPTURE = CASE / "stage_b/attempts/case-0012-stage-b-2"
GOLD = CASE / "adjudication/reviewed"
REPO = CASE.parents[2]
STAGE_A = "4ff6d3950e6c0be834f136a649c1a127f91fdba3"
STAGE_B = "a2f140d4aa2862c7cc64b80d9608ee6690a6e6bb"
BLIND = "35153e46d22ad4e151d8a71b5e10d2a38a066034"
REVIEWED = "996ea3b1f9bfc25ed770a390f37fde24077b0710"


def relative(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


async def checkpoint_bindings() -> Any:
    chain = [STAGE_A, STAGE_B, BLIND, REVIEWED]
    for ancestor, child in pairwise(chain):
        require(
            (await git("merge-base", ancestor, child)).decode().strip() == ancestor,
            "Checkpoint ancestry",
        )
    require(
        (await git("merge-base", REVIEWED, "HEAD")).decode().strip() == REVIEWED,
        "Reviewed checkpoint ancestry",
    )
    for checkpoint, path in [
        (STAGE_A, CASE / "integrity.json"),
        (STAGE_B, CAPTURE / "integrity.json"),
        (REVIEWED, GOLD / "reviewed_hashes.json"),
    ]:
        require(
            await git("show", checkpoint + ":" + relative(path)) == path.read_bytes(),
            "Checkpoint seal: " + path.name,
        )
    # README and Stage C publication status evolved after Stage A (the latter at
    # 165e971); authenticate historical frozen bytes, not current status prose.
    integrity = load(CASE / "integrity.json")
    for name, digest in integrity["sha256"].items():
        historical = await git("show", STAGE_A + ":" + relative(CASE / name))
        require(sha(historical) == digest, "Historical Stage A: " + name)
        if name not in {"README.md", ".gitattributes", "STAGE_C_PROTOCOL.md"}:
            require(
                sha((CASE / name).read_bytes()) == digest,
                "Frozen Stage A changed: " + name,
            )
    return {
        "stage_a": STAGE_A,
        "stage_b": STAGE_B,
        "blind_packet": BLIND,
        "reviewed_gold": REVIEWED,
        "ancestry": "PASS",
        "stage_a_integrity_sha256": sha((CASE / "integrity.json").read_bytes()),
        "stage_b_integrity_sha256": sha((CAPTURE / "integrity.json").read_bytes()),
        "reviewed_hashes_sha256": sha((GOLD / "reviewed_hashes.json").read_bytes()),
    }


def authenticate() -> Any:
    """Honor physical capture seals and canonical-LF implementation seals."""
    checkpoints = asyncio.run(checkpoint_bindings())
    reviewed_replay = gold_builder.verify()
    gold = load(GOLD / "reviewed_gold.json")
    integrity = load(CAPTURE / "integrity.json")
    for name, digest in integrity["sha256"].items():
        require(
            sha((CAPTURE / name).read_bytes()) == digest, "Stage B artifact: " + name
        )
    journal = integrity["journal_sha256"]
    require(
        set(journal)
        == {
            relative(p).split("case-0012-stage-b-2/", 1)[1]
            for p in (CAPTURE / "operations").glob("*.json")
        },
        "Journal roster",
    )
    for name, digest in journal.items():
        require(
            sha((CAPTURE / name).read_bytes()) == digest, "Stage B journal: " + name
        )
    for name, key in [
        ("execution.claim", "claim_sha256"),
        ("execution_started.json", "marker_sha256"),
        ("execution_completed.json", "completed_sha256"),
        ("native_context.json", "native_context_sha256"),
        ("raw_checkpoint.json", "raw_checkpoint_sha256"),
    ]:
        require(
            sha((CAPTURE / name).read_bytes()) == integrity[key],
            "Stage B execution: " + name,
        )
    marker = load(CAPTURE / "execution_started.json")
    require(marker["stage_a_commit"] == STAGE_A, "Stage B attribution")
    require(
        marker["frame"] == {k: gold["frame"][k] for k in marker["frame"]},
        "Treatment/gold frame",
    )
    for path, digest in marker["implementation_sha256"].items():
        # execute.marker hashes binary(), whose explicit text boundary maps
        # physical Windows CRLF to canonical LF. This is not a physical seal.
        require(
            sha(binary(REPO / path)) == digest,
            "Captured implementation changed: " + path,
        )
    treatment = load(CASE / "treatment.json")
    require(
        sha((CASE / "treatment.json").read_bytes()) == marker["treatment_sha256"],
        "Treatment identity",
    )
    require(
        treatment["task_identity"] == gold["task_identity"]
        and treatment["task_text"] == gold["task_text"],
        "Task join",
    )
    require(
        [
            {k: v for k, v in ob.items() if k not in {"query", "analyzed_terms"}}
            for ob in treatment["obligations"]
        ]
        == gold["obligations"],
        "Obligation join",
    )
    resources = json.loads(gzip.decompress((CASE / "resources.json.gz").read_bytes()))[
        "resources"
    ]
    require(
        len(resources)
        == len({r["address"] for r in resources})
        == len(gold["resources"])
        == 531,
        "Resource roster",
    )
    for resource, reviewed in zip(resources, gold["resources"], strict=True):
        for key in ("address", "content_identity", "byte_size", "encoding"):
            require(resource[key] == reviewed[key], "Resource join: " + key)
        require(
            resource["byte_size"] == len(resource["text"].encode("utf-8")),
            "Resource bytes",
        )
    summary, lexical = load(CAPTURE / "summary.json"), load(CAPTURE / "lexical.json")
    require(summary["execution"] == "case-0012-stage-b-2", "Authoritative execution")
    require(
        load(CAPTURE / "execution_completed.json")["execution"] == summary["execution"],
        "Completion attribution",
    )
    arms = {arm: load(CAPTURE / f"arm_{arm.lower()}.json") for arm in ("A", "B", "C")}
    behaviors = {
        arm: load(CAPTURE / f"behavior_{arm.lower()}.json") for arm in ("B", "C")
    }
    exact = json.loads(
        gzip.decompress((CAPTURE / "exact_resolutions.json.gz").read_bytes())
    )
    require(behaviors["B"] == behaviors["C"], "Frozen B/C behavioral projection")
    operations = load(CAPTURE / "operations.json")
    require(
        len(operations) == len({o["identity"] for o in operations}) == 72,
        "Operation roster",
    )
    require(
        all(o["status"] == "RETURNED" and o["invocations"] == 1 for o in operations),
        "Captured invocation contract",
    )
    require(
        {o["identity"]: o["runtime_ns"] for o in operations} == summary["runtime_ns"],
        "Captured timing identity",
    )
    for i, operation in enumerate(operations):
        require(
            operation["prior_operations"] == [o["identity"] for o in operations[:i]],
            "Operation chain",
        )
        require(
            operation["wall_call_ns"]
            == operation["runtime_ns"] + operation["durability_inside_call_ns"],
            "Operation timing decomposition",
        )
    require(
        arms["A"] == {ob: lane for ob, lane in lexical.items() if ob != "global"},
        "Arm A exact captured queries",
    )
    for ob in treatment["obligations"]:
        require(
            lexical[ob["key"]]["query_text"] == ob["query"]
            and lexical[ob["key"]]["analyzed_terms"] == ob["analyzed_terms"],
            "Frozen lexical query",
        )
    require(
        lexical["global"]["query_text"] == treatment["task_text"], "Global safety query"
    )
    return {
        "checkpoints": checkpoints,
        "reviewed_replay": reviewed_replay,
        "gold": gold,
        "resources": resources,
        "treatment": treatment,
        "summary": summary,
        "lexical": lexical,
        "arms": arms,
        "behaviors": behaviors,
        "exact": exact,
        "operations": operations,
    }
