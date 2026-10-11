"""Authenticate named development checkpoints and inert captured JSON graphs.

No native classes are instantiated, pickle loaded, or treatment operation called.
Case-local byte reads are the artifact boundary; Git uses managed commands.
"""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, ANN401, D103, COM812, PLR2004
import asyncio
import base64
import gzip
import json
from itertools import pairwise
from pathlib import Path
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import binary, git, json_bytes
from experiments.codex_dogfood.case_0013.adjudication.reviewed import materialize as m

encoded, sha, require, load = m.encoded, m.sha, m.require, m.load
ROOT = Path(__file__).resolve().parent
CASE = ROOT.parent
REPO = CASE.parents[2]
CAPTURE = CASE / "stage_b/attempts/case-0013-stage-b-1"
STAGE_A = "6b18b6e12bbab5a0e131e0afe2fb57b5410b4f16"
STAGE_B = "2937e49feb566443f943b91267c59b60b2c7494a"
BLIND = "483caf11f6e17994b922e3f00dcb9058e28c3e3d"
REVIEWED = "f498a790714b9420b79206ad2183ed2f93f44a42"
STAGE_B_HASH = "b2132804733e7c457deaccfe759cbdfc1c6546eb6a9164b1592d1e12f8c9f999"


def relative(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


async def checkpoints() -> Any:
    chain = [STAGE_A, STAGE_B, BLIND, REVIEWED, "HEAD"]
    for ancestor, child in pairwise(chain):
        require(
            (await git("merge-base", ancestor, child)).decode().strip() == ancestor,
            "Checkpoint ancestry",
        )
    for checkpoint, root, seal_name in [
        (STAGE_A, CASE, "integrity.json"),
        (STAGE_B, CAPTURE, "integrity.json"),
        (REVIEWED, m.ROOT, "reviewed_hashes.json"),
    ]:
        path = root / seal_name
        require(
            await git("show", checkpoint + ":" + relative(path)) == path.read_bytes(),
            "Committed seal: " + relative(path),
        )
    for name, digest in load(CASE / "integrity.json")["sha256"].items():
        require(
            sha(await git("show", STAGE_A + ":" + relative(CASE / name))) == digest,
            "Historical Stage A: " + name,
        )
        require(sha(binary(CASE / name)) == digest, "Current frozen Stage A: " + name)
    for name, digest in load(m.ADJ / "IMPORT.json")["primary_sha256"].items():
        require(
            sha(await git("show", REVIEWED + ":" + relative(m.ADJ / "primary" / name)))
            == digest,
            "Committed primary identity: " + name,
        )
    require(
        await git("show", REVIEWED + ":" + relative(m.ROOT / "reviewed_gold.json"))
        == (m.ROOT / "reviewed_gold.json").read_bytes(),
        "Committed reviewed gold",
    )
    for name, digest in load(CASE / "pre_execution.json")[
        "implementation_sha256"
    ].items():
        require(
            sha(binary(REPO / name)) == digest, "Frozen Stage A implementation: " + name
        )
    return {
        "stage_a": STAGE_A,
        "stage_b": STAGE_B,
        "blind_packet": BLIND,
        "reviewed_gold": REVIEWED,
        "ancestry": "PASS",
        "stage_a_integrity_sha256": sha(binary(CASE / "integrity.json")),
        "stage_b_integrity_sha256": STAGE_B_HASH,
        "primary_hashes_sha256": m.PRIMARY_HASHES,
        "reviewed_hashes_sha256": sha((m.ROOT / "reviewed_hashes.json").read_bytes()),
    }


def unpack(value: Any) -> bytes:
    raw = base64.b85decode(value["gzip_b85"])
    require(sha(raw) == value["sha256"], "Journal compressed archive hash")
    return gzip.decompress(raw)


def journal(marker: Any) -> Any:
    require(
        load(CAPTURE / "execution.claim") == {"execution": marker["execution"]},
        "Exactly-once claim",
    )
    context = load(CAPTURE / "native_context.json")
    require(
        context["marker_sha256"] == sha(binary(CAPTURE / "execution_started.json")),
        "Journal initial context",
    )
    # Authenticate native bytes without deserializing them.
    unpack(context["native"])
    unpack(context["canonical"])
    chain = sha(binary(CAPTURE / "native_context.json"))
    events = sorted(
        [(load(p), p) for p in (CAPTURE / "operations").glob("*.json")],
        key=lambda pair: pair[0]["event"],
    )
    operations: list[Any] = []
    active: set[str] = set()
    canonical_hashes = {}
    for ordinal, (value, path) in enumerate(events, 1):
        sequence, status = value["sequence"], value["state"]
        require(
            value["event"] == ordinal
            and value["prior_chain_sha256"] == chain
            and value["execution"] == marker["execution"]
            and value["frame"] == marker["frame"]
            and value["runtime_identity"] == marker["runtime"]
            and path.name == f"{sequence:06}.{status.lower()}.json",
            "Journal event chain/frame",
        )
        op = value["operation"]
        require(
            value["input_sha256"] == sha(json_bytes(op["inputs"])),
            "Journal input identity",
        )
        if status == "ENTERED":
            require(
                sequence == len(operations) + 1
                and op["identity"] not in {o["identity"] for o in operations}
                and op["invocations"] == 1
                and op["status"] == "ENTERED"
                and op["prior_operations"] == [o["identity"] for o in operations],
                "Unique native entry/no retries",
            )
            operations.append(op)
            active.add(op["identity"])
        else:
            require(
                status == "RETURNED"
                and op["identity"] in active
                and op["invocations"] == 1
                and op["status"] == "RETURNED",
                "Native return pair",
            )
            entered = operations[sequence - 1]
            require(
                all(
                    op[k] == entered[k]
                    for k in ("identity", "inputs", "invocations", "prior_operations")
                ),
                "Return entry binding",
            )
            require(
                value["entered_sha256"]
                == sha(binary(CAPTURE / "operations" / f"{sequence:06}.entered.json")),
                "Entered digest",
            )
            canonical = unpack(value["canonical"])
            require(
                sha(canonical) == op["serialized_return_sha256"],
                "Canonical native return",
            )
            unpack(value["native"])
            canonical_hashes[op["identity"]] = sha(canonical)
            operations[sequence - 1] = op
            active.remove(op["identity"])
        chain = sha(binary(path))
    require(
        not active and len(operations) == 73 and len(events) == 146,
        "73 complete ENTERED/RETURNED pairs",
    )
    require(
        load(CAPTURE / "execution_completed.json")
        == {
            "execution": marker["execution"],
            "journal_chain_sha256": chain,
            "operations": [o["identity"] for o in operations],
        },
        "Exactly-once completion",
    )
    require(
        operations == load(CAPTURE / "operations.json"), "Captured journal projection"
    )
    return {
        "status": "PASS",
        "pairs": len(operations),
        "native_retries": 0,
        "chain_sha256": chain,
        "operations": operations,
        "canonical_return_sha256": canonical_hashes,
    }


class Graph:
    """Read the existing canonical graph as JSON; never execute its types."""

    def __init__(self, value: Any) -> None:
        """Retain only the authenticated graph's inert nodes."""
        self.value = value
        self.nodes = value["nodes"]
        require(value["schema"] == "case-0012-native-graph-v1", "Native graph schema")

    def fields(self, ref: Any) -> Any:
        """Return the existing native field references."""
        return self.nodes[ref["ref"]]["fields"]

    def items(self, ref: Any) -> Any:
        """Return the existing ordered container references."""
        return self.nodes[ref["ref"]]["items"]

    def plain(self, ref: Any) -> Any:
        """Project a bounded native subtree to ordinary JSON values."""
        if not isinstance(ref, dict) or set(ref) != {"ref"}:
            return ref
        node = self.nodes[ref["ref"]]
        if "fields" in node:
            return {k: self.plain(v) for k, v in node["fields"].items()}
        if "items" in node:
            if node["type"] == "builtins.dict":
                return {self.plain(k): self.plain(v) for k, v in node["items"]}
            return [self.plain(v) for v in node["items"]]
        return node["value"]


def native_lexical(lexical: Any, frame: Any, resources: Any) -> Any:
    graph = Graph(
        json.loads(gzip.decompress((CAPTURE / "native_lexical.json.gz").read_bytes()))
    )
    index_refs = set()
    checked = 0
    for key, ref in graph.items(graph.value["root"]):
        lane = graph.fields(ref)
        index_refs.add(lane["index"]["ref"])
        require(
            lane["maximum_results"] == len(resources), "Complete native query depth"
        )
        require(
            graph.fields(lane["query"])["text"] == lexical[key]["query_text"],
            "Native query text",
        )
        matches = graph.items(lane["matches"])
        rows = []
        for rank, match_ref in enumerate(matches, 1):
            match = graph.fields(match_ref)
            stats = graph.fields(match["document_statistics"])
            analysis = graph.fields(stats["analysis"])
            document = graph.fields(analysis["document"])
            require(
                graph.plain(document["repository_id"])["value"]
                == frame["repository_id"],
                "Native RepositoryId",
            )
            resource = graph.plain(document["resource"])
            address = resource["address"]["value"]
            require(
                resource["content_identity"]["value"]
                == resources[address]["content_identity"]
                and resource["content"] == resources[address]["text"],
                "Native resource content identity",
            )
            row = {
                "address": address,
                "content_identity": resource["content_identity"]["value"],
                "rank": rank,
                **{
                    k: match[k]
                    for k in (
                        "score",
                        "content_score",
                        "filename_score",
                        "filename_weight",
                        "weighted_filename_score",
                    )
                },
                "content_terms": graph.plain(match["term_contributions"]),
                "filename_terms": graph.plain(match["filename_term_contributions"]),
            }
            rows.append(row)
            checked += 1
        require(
            rows == lexical[key]["rows"], "Every native match/rank/score/contribution"
        )
    require(
        len(index_refs) == 1 and len(graph.items(graph.value["root"])) == 10,
        "Shared native index and ten queries",
    )
    return {
        "status": "PASS",
        "positive_rows": checked,
        "index_count": len(index_refs),
        "query_count": 10,
    }


def native_exact(summary: Any, treatment: Any, frame: Any) -> Any:
    graph = Graph(
        json.loads(
            gzip.decompress((CAPTURE / "exact_resolutions.json.gz").read_bytes())
        )
    )
    outcomes = graph.plain(graph.value["root"])
    counts = {}
    for arm in "BC":
        captured = [h for h in summary["hint_rows"] if h["arm"] == arm]
        expected = treatment["exact_route_requests"][arm]
        require(
            len(outcomes[arm]) == len(captured) == len(expected),
            "Exact independent arm roster",
        )
        for native, hint, request in zip(
            outcomes[arm], captured, expected, strict=True
        ):
            require(
                native["request"]
                == {k: v for k, v in request.items() if k != "identity"},
                "Native frozen request identity",
            )
            require(
                native["disposition"] == hint["disposition"]
                and request["identity"] == hint["request_identity"],
                "Native hint disposition",
            )
            require(
                native["repository_id"]["value"] == frame["repository_id"]
                and native["snapshot_id"]["value"] == frame["snapshot_id"]
                and native["frame_identity"] == frame["frame_identity"],
                "Native exact frame",
            )
            targets = [
                (r["address"]["value"], r["content_identity"]["value"])
                for r in native["resources"]
            ]
            require(
                targets
                == [(r["address"], r["content_identity"]) for r in hint["targets"]],
                "Exact target/content join",
            )
            require(
                len(targets) == 1
                if native["disposition"] == "RESOLVED"
                else not targets,
                "Unique native resolved promotion",
            )
            for account in hint["native_accounts"]:
                require(
                    account["request"]["repository_id"]["value"]
                    == frame["repository_id"]
                    and account["request"]["snapshot_id"]["value"]
                    == frame["snapshot_id"],
                    "Native grounding frame",
                )
        counts[arm] = len(outcomes[arm])
    return {
        "status": "PASS",
        "native_invocations": counts,
        "cross_arm": "INDEPENDENT sealed entries and returned journal pairs",
    }


def authenticate() -> Any:
    provenance = asyncio.run(checkpoints())
    reviewed = m.verify()
    gold = load(m.ROOT / "reviewed_gold.json")
    require(
        sha(binary(CAPTURE / "integrity.json")) == STAGE_B_HASH,
        "Sealed authoritative Stage B hash",
    )
    seal = load(CAPTURE / "integrity.json")
    actual = {
        p.relative_to(CAPTURE).as_posix()
        for p in CAPTURE.rglob("*")
        if p.is_file() and p.name != "integrity.json"
    }
    require(actual == set(seal["sha256"]), "Capture seal roster")
    for name, digest in seal["sha256"].items():
        require(sha(binary(CAPTURE / name)) == digest, "Authoritative Stage B: " + name)
    marker = load(CAPTURE / "execution_started.json")
    require(
        marker["stage_a_commit"] == STAGE_A
        and marker["execution"] == "case-0013-stage-b-1"
        and marker["case"] == gold["primary"]["case"],
        "Capture case/execution checkpoint",
    )
    require(marker["frame"] == gold["frame"], "Exact treatment/reviewed frame")
    for name, digest in marker["implementation_sha256"].items():
        require(sha(binary(REPO / name)) == digest, "Captured implementation: " + name)
    treatment = load(CASE / "treatment.json")
    require(
        sha(binary(CASE / "treatment.json")) == marker["treatment_sha256"],
        "Frozen treatment seal",
    )
    primary = gold["primary"]
    require(
        primary["task_identity"] == treatment["task_identity"]
        and primary["task_text"] == treatment["task_text"],
        "Exact task join",
    )
    require(
        [
            (o["identity"], o["key"], o["statement"], o["criterion"])
            for o in primary["obligations"]
        ]
        == [
            (o["identity"], o["key"], o["statement"], o["criterion"])
            for o in treatment["obligations"]
        ],
        "Exact obligation join",
    )
    resources = json.loads(gzip.decompress((CASE / "resources.json.gz").read_bytes()))[
        "resources"
    ]
    by_address = {r["address"]: r for r in resources}
    require(
        len(by_address) == len(resources) == len(gold["resource_bindings"]),
        "No missing/duplicate/unexpected resource joins",
    )
    for binding in gold["resource_bindings"]:
        require(
            {k: binding[k] for k in gold["frame"]} == marker["frame"],
            "No stale frame join",
        )
        require(
            all(
                binding[k] == by_address[binding["address"]][k]
                for k in ("address", "content_identity", "encoding", "byte_size")
            ),
            "Qualified resource content join",
        )
        r = by_address[binding["address"]]
        # Native ContentIdentity uses domain-separated length-framed text,
        # not physical SHA-256. Its exact sealed identity is joined above;
        # the separately authenticated text supplies whole-resource bytes.
        require(len(r["text"].encode()) == r["byte_size"], "Exact retained UTF-8 bytes")
    j = journal(marker)
    lexical = load(CAPTURE / "lexical.json")
    native = native_lexical(lexical, marker["frame"], by_address)
    arms = {a: load(CAPTURE / f"arm_{a.lower()}.json") for a in "ABC"}
    require(
        arms["A"] == {k: v for k, v in lexical.items() if k != "global"},
        "Arm A native lexical identity",
    )
    summary = load(CAPTURE / "summary.json")
    exact_validation = native_exact(summary, treatment, marker["frame"])
    policy = load(CAPTURE / "route_policy.json")
    require(
        policy == {a: treatment["route_decisions"][a] for a in "BC"},
        "Frozen task-only policy identity; no policy rerun",
    )
    require(
        summary["cross_arm_exact_outcomes"] == "INDEPENDENT"
        and summary["global_safety"]
        == summary["lexical_fallback"]
        == summary["native_rank_score_contributions"]
        == "PRESERVED",
        "Independent B/C and unchanged safety capture",
    )
    for key, lane in lexical.items():
        expected_query = (
            treatment["global_safety_query"]
            if key == "global"
            else next(o for o in treatment["obligations"] if o["key"] == key)
        )
        require(
            lane["query_text"]
            == expected_query.get("query", expected_query.get("text"))
            and lane["analyzed_terms"] == expected_query["analyzed_terms"],
            "Exact frozen query binding",
        )
    costs = load(CAPTURE / "costs.json")
    runtime = {op["identity"]: op["runtime_ns"] for op in j["operations"]}
    require(runtime == summary["runtime_ns"], "Captured timing identity")
    for arm in "ABC":
        route = sum(v for k, v in runtime.items() if k.startswith("route:" + arm + ":"))
        presentation = sum(
            v for k, v in runtime.items() if k.startswith("present:" + arm + ":")
        )
        policy_ns = runtime.get("policy:" + arm, 0)
        shared = runtime["index-build"] + sum(
            v for k, v in runtime.items() if k.startswith("lexical:")
        )
        charged = (
            shared
            + (runtime["purposes:shared"] if arm != "A" else 0)
            + policy_ns
            + route
            + presentation
        )
        require(
            all(
                costs["arms"][arm][k] == v
                for k, v in {
                    "route_ns": route,
                    "presentation_ns": presentation,
                    "mechanism_ns": route + presentation,
                    "policy_ns": policy_ns,
                    "charged_ns": charged,
                }.items()
            ),
            "Nonoverlapping cost arithmetic",
        )
    return {
        "provenance": provenance,
        "reviewed_replay": reviewed,
        "gold": gold,
        "treatment": treatment,
        "resources": by_address,
        "arms": arms,
        "lexical": lexical,
        "summary": summary,
        "policy": policy,
        "costs": costs,
        "journal": {k: v for k, v in j.items() if k != "operations"},
        "native_validation": native,
        "native_exact_validation": exact_validation,
        "publication": load(CAPTURE / "publication_cost.json"),
        "durability_ns": sum(
            o["durability_inside_call_ns"]
            for o in j["operations"]
            if o["identity"] in {"arm:B", "arm:C"}
        ),
        "execution_marker": marker,
    }
