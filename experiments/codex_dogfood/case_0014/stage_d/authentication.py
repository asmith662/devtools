"""Authenticate only sealed development checkpoints and inert captured JSON.

No native retrieval/scoring operation, pickle loading, or live model is used.
Physical byte reads preserve imported gold. Existing normalized artifact reads
retain the established Stage A/B text hashing contract. Git is managed.
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
from experiments.codex_dogfood.case_0014.adjudication.reviewed import materialize as m

encoded, sha, require, load = m.encoded, m.sha, m.require, m.load
ROOT = Path(__file__).resolve().parent
CASE = ROOT.parent
REPO = CASE.parents[2]
CAPTURE = CASE / "stage_b/attempts/case-0014-stage-b-1"
STAGE_A = "6d26f3c9cce5bc059226a0fe4023dc3ec75832ce"
STAGE_B = "06e816693fed9165467c3afde42298e6dcefe615"
BLIND = "15417485eba52eb07631c54dcb141ff8d3294606"
REVIEWED = "466e0a7a473d5baf7ff0fd75ec9ae3031760649a"
RESTORED = "c43d46607e55d7999ac0277cd196ca9d9e07b9b5"
STAGE_B_HASH = "089bd2fb9be9449dc66966e097d734410030069cbd2a12aefb57610f17fe3ba0"


def relative(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


async def checkpoints() -> Any:
    for ancestor, child in pairwise(
        [STAGE_A, STAGE_B, BLIND, REVIEWED, RESTORED, "HEAD"]
    ):
        require(
            (await git("merge-base", ancestor, child)).decode().strip() == ancestor,
            "Exact checkpoint ancestry",
        )
    stage_a = load(CASE / "integrity.json")
    require(
        sha(binary(CASE / "integrity.json"))
        == "ec069881253e903ecb28c86b5c4b87ee669f540f76fd036e523c8dbde5092505",
        "Stage A seal",
    )
    for name, expected in {**stage_a["artifacts"], **stage_a["authored"]}.items():
        path = CASE / name
        require(
            sha(binary(path)) == expected
            and sha(await git("show", STAGE_A + ":" + relative(path))) == expected,
            "Stage A artifact: " + name,
        )
    for name, expected in stage_a["implementation"].items():
        path = REPO / name
        require(
            sha(binary(path)) == expected
            and sha(await git("show", STAGE_A + ":" + name)) == expected,
            "Frozen Stage A implementation: " + name,
        )
    require(
        sha(binary(CAPTURE / "integrity.json")) == STAGE_B_HASH,
        "Authoritative Stage B integrity",
    )
    seal = load(CAPTURE / "integrity.json")
    require(
        {
            p.relative_to(CAPTURE).as_posix()
            for p in CAPTURE.rglob("*")
            if p.is_file() and p.name != "integrity.json"
        }
        == set(seal["sha256"]),
        "Stage B seal roster",
    )
    for name, expected in {"integrity.json": STAGE_B_HASH, **seal["sha256"]}.items():
        path = CAPTURE / name
        require(
            sha(binary(path)) == expected
            and sha(await git("show", STAGE_B + ":" + relative(path))) == expected,
            "Committed Stage B artifact: " + name,
        )
    for name, expected in seal["implementation_sha256"].items():
        require(
            sha(binary(REPO / name)) == expected, "Captured implementation: " + name
        )
    for name, expected in m.HASHES.items():
        path = m.ADJ / "primary" / name
        require(
            sha(path.read_bytes()) == expected
            and sha(await git("show", REVIEWED + ":" + relative(path))) == expected,
            "Committed primary bytes: " + name,
        )
    for name in ("reviewed_hashes.json", "reviewed_gold.json"):
        path = m.ROOT / name
        require(
            await git("show", REVIEWED + ":" + relative(path)) == path.read_bytes(),
            "Committed reviewed gold: " + name,
        )
    for name, expected in load(m.PACKET / "integrity.json")["sha256"].items():
        path = m.PACKET / name
        require(
            sha(path.read_bytes()) == expected
            and sha(await git("show", BLIND + ":" + relative(path))) == expected,
            "Committed blind packet: " + name,
        )
    return {
        "stage_a": STAGE_A,
        "stage_b": STAGE_B,
        "blind_packet": BLIND,
        "reviewed_gold": REVIEWED,
        "stage_a_readme_restoration": RESTORED,
        "ancestry": "PASS",
        "stage_b_integrity_sha256": STAGE_B_HASH,
        "primary_sha256": m.HASHES,
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
        not active and len(operations) == 27 and len(events) == 54,
        "27 complete ENTERED/RETURNED pairs",
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


def project_lane(graph: Graph, ref: Any, resources: Any) -> Any:
    lane = graph.fields(ref)
    require(
        graph.plain(lane["settings"]) == {"b": 0.75, "k1": 1.2}, "Native BM25 settings"
    )
    require(lane["maximum_results"] == 515, "Native full candidate bound")
    rows = []
    for rank, match_ref in enumerate(graph.items(lane["matches"]), 1):
        match = graph.fields(match_ref)
        stats = graph.fields(match["document_statistics"])
        document = graph.fields(graph.fields(stats["analysis"])["document"])
        rid = graph.plain(document["id"])["value"]
        resource = graph.plain(document["resource"])
        r = resources[rid]
        require(
            resource["content"] == r["content"]
            and resource["address"]["value"] == r["address"]
            and resource["content_identity"]["value"] == r["content_identity"]
            and graph.plain(document["repository_id"])["value"] == r["repository_id"],
            "Native qualified resource identity/content",
        )
        content = graph.plain(match["term_contributions"])
        filename = graph.plain(match["filename_term_contributions"])
        require(
            match["filename_weight"] == 0.25
            and match["content_score"] == sum(t["contribution"] for t in content)
            and match["filename_score"] == sum(t["contribution"] for t in filename)
            and match["score"]
            == match["content_score"] + 0.25 * match["filename_score"],
            "Native captured score/channel arithmetic",
        )
        rows.append(
            {
                "rank": rank,
                "document_id": rid,
                "native_score": match["score"],
                "native_content_evidence": content,
                "native_filename_evidence": filename,
            }
        )
    return {"query": graph.plain(lane["query"]), "rows": rows}


def captured_native(resources: Any, design: Any) -> Any:
    graph = Graph(
        json.loads(gzip.decompress((CAPTURE / "native_capture.json.gz").read_bytes()))
    )
    roots = dict(graph.items(graph.value["root"]))
    require(
        set(roots)
        == {
            "frame:prepare",
            "index-build",
            "query:reference",
            *["query:Q" + str(i) for i in range(1, 7)],
        },
        "Native capture roster",
    )
    index = roots["index-build"]
    collection = graph.fields(roots["frame:prepare"])
    docs = graph.items(collection["documents"])
    require(len(docs) == 515, "Native 515-document frame")
    for ref, r in zip(docs, resources.values(), strict=True):
        doc = graph.fields(ref)
        require(
            graph.plain(doc["id"])["value"] == r["document_identity"],
            "Canonical collection-order identity",
        )
    lanes = {}
    for key in [*["Q" + str(i) for i in range(1, 7)], "reference"]:
        ref = roots["query:" + key]
        require(graph.fields(ref)["index"] == index, "Single shared captured index")
        lanes[key] = project_lane(graph, ref, resources)
        expected = (
            design["global_reference_lane"]["analysis"]
            if key == "reference"
            else design["queries"][int(key[1:]) - 1]["native_query"]
        )
        require(lanes[key]["query"] == expected, "Unchanged native query analysis")
    reference = Graph(
        json.loads(gzip.decompress((CAPTURE / "reference.json.gz").read_bytes()))
    )
    require(
        project_lane(reference, reference.value["root"], resources)
        == lanes["reference"],
        "Exact unchanged reference lane",
    )
    return lanes


def validate_arms(arms: Any, design: Any, resources: Any, native: Any) -> None:
    """Check captured arithmetic only; never call the treatment scorer."""
    for i, policy in enumerate(design["queries"], 1):
        key = "Q" + str(i)
        require(
            policy["identity"]["value"] == key
            and policy["identity"]["task"]["value"] == design["task_identity"]
            and policy["obligation"]["value"] == "O" + str(i),
            "Exact obligation/query join",
        )
        anchors = policy["anchors"]
        for anchor in anchors:
            span = anchor["task_provenance"]["span"]
            literal = policy["task_text"][span["start"] : span["end"]]
            require(
                literal
                == policy["native_query"]["text"][
                    anchor["query_start"] : anchor["query_end"]
                ]
                and policy["task_text"][span["start"] - 1 : span["start"]] == "`"
                and policy["task_text"][span["end"] : span["end"] + 1] == "`",
                "Task-only anchor provenance",
            )
        roles = {}
        for term in policy["terms"]:
            observations = [
                o
                for o in policy["native_query"]["observations"]
                if o["normalized_term"] == term["analyzed_term"]
            ]
            literal = any(
                a["query_start"] <= o["start"] < o["end"] <= a["query_end"]
                for a in anchors
                for o in observations
            )
            expected_role = (
                "EXPLICIT_ANCHOR"
                if literal
                else "GENERIC_OPERATION"
                if term["analyzed_term"] in design["taxonomy"]["generic_lexicon"]
                else "SEMANTIC"
            )
            require(
                term["observations"] == observations and term["role"] == expected_role,
                "Task-only classification identity",
            )
            roles[term["analyzed_term"]] = expected_role
        maps = {}
        for arm in "ABC":
            lane = arms[arm][key]
            require(
                lane["query_policy"] == policy and lane["filename_weight"] == 0.25,
                "Frozen policy/filename identity",
            )
            rows = lane["matches"]
            require(
                [r["rank"] for r in rows] == list(range(1, len(rows) + 1)),
                "Complete consecutive captured ranks",
            )
            require(
                rows
                == sorted(
                    rows, key=lambda r: (-r["weighted_score"], r["collection_position"])
                ),
                "Native tie ordering",
            )
            maps[arm] = {r["document_id"]: r for r in rows}
            require(len(maps[arm]) == len(rows), "Duplicate candidate join")
            for row in rows:
                resource = resources[row["document_id"]]
                require(
                    all(
                        row[k] == resource[rk]
                        for k, rk in [
                            ("repository_id", "repository_id"),
                            ("corpus_id", "corpus_id"),
                            ("address", "address"),
                            ("content_identity", "content_identity"),
                        ]
                    )
                    and row["collection_position"]
                    == list(resources).index(row["document_id"]),
                    "Exact treatment document/frame join",
                )
                require(
                    float(row["native_score"]).hex() == row["native_score_hex"]
                    and float(row["weighted_score"]).hex() == row["weighted_score_hex"],
                    "Captured score hex",
                )
                evidence = [("content", t) for t in row["native_content_evidence"]] + [
                    ("filename", t) for t in row["native_filename_evidence"]
                ]
                require(
                    len(evidence) == len(row["contributions"]),
                    "Complete native contribution retention",
                )
                for contribution, (channel, term) in zip(
                    row["contributions"], evidence, strict=True
                ):
                    role = roles[term["normalized_term"]]
                    weight = design["weights"][arm][role]
                    require(
                        contribution["term"] == term["normalized_term"]
                        and contribution["role"] == role
                        and contribution["channel"] == channel
                        and contribution["channel_weight"]
                        == (1 if channel == "content" else 0.25)
                        and contribution["native"] == term["contribution"]
                        and contribution["multiplier"] == weight
                        and contribution["weighted"] == contribution["native"] * weight
                        and contribution["native_hex"]
                        == float(contribution["native"]).hex()
                        and contribution["weighted_hex"]
                        == float(contribution["weighted"]).hex(),
                        "Captured contribution application",
                    )
                total = sum(
                    t["weighted"]
                    for t in row["contributions"]
                    if t["channel"] == "content"
                ) + 0.25 * sum(
                    t["weighted"]
                    for t in row["contributions"]
                    if t["channel"] == "filename"
                )
                require(
                    total == row["weighted_score"],
                    "Frozen ordered captured contribution sum",
                )
        require(
            maps["A"].keys() == maps["B"].keys() == maps["C"].keys(),
            "A/B/C candidate contract",
        )
        for rid, row in maps["A"].items():
            for arm in "BC":
                other = maps[arm][rid]
                require(
                    all(
                        row[k] == other[k]
                        for k in (
                            "native_score",
                            "native_content_evidence",
                            "native_filename_evidence",
                            "collection_position",
                        )
                    ),
                    "Unchanged native statistics/evidence",
                )
        require(
            [
                {k: r[k] for k in native[key]["rows"][0]}
                for r in arms["A"][key]["matches"]
            ]
            == native[key]["rows"],
            "Arm A exactly native canonical BM25",
        )


def authenticate() -> Any:
    provenance = asyncio.run(checkpoints())
    replay = m.verify()
    gold = load(m.ROOT / "reviewed_gold.json")
    design = load(CASE / "protocol.json")
    marker = load(CAPTURE / "execution_started.json")
    require(
        marker["execution"] == "case-0014-stage-b-1"
        and marker["case"] == gold["primary"]["case"]
        and marker["stage_a"] == STAGE_A
        and marker["protocol_sha256"] == sha(binary(CASE / "protocol.json")),
        "Frozen execution/task identity",
    )
    require(
        all(marker["frame"][k] == gold["frame"][k] for k in gold["frame"]),
        "Exact snapshot/corpus/repository join",
    )
    resources = json.loads(gzip.decompress((CASE / "resources.json.gz").read_bytes()))
    by_id = {r["document_identity"]: r for r in resources}
    require(
        len(by_id) == len(resources) == 515
        and [{k: r[k] for k in gold["resource_bindings"][0]} for r in resources]
        == gold["resource_bindings"],
        "Complete qualified resource join",
    )
    j = journal(marker)
    require(
        [o["identity"] for o in j["operations"]] == marker["operation_schedule"],
        "27-pair frozen schedule",
    )
    require(
        load(CAPTURE / "validation.json")["mechanical_capture"] == "PASS",
        "Stage B completed validation",
    )
    native = captured_native(by_id, design)
    arms = {
        a: json.loads(
            gzip.decompress((CAPTURE / ("arm_" + a.lower() + ".json.gz")).read_bytes())
        )
        for a in "ABC"
    }
    require(
        (CAPTURE / "arm_a.json.gz").read_bytes()
        == (CAPTURE / "native_contributions.json.gz").read_bytes(),
        "Arm A native surface byte identity",
    )
    validate_arms(arms, design, by_id, native)
    for path in sorted((CAPTURE / "operations").glob("*.returned.json")):
        value = load(path)
        op = value["operation"]["identity"]
        if op.startswith("construct:"):
            _, arm, key = op.split(":")
            g = Graph(json.loads(unpack(value["canonical"])))
            require(
                g.plain(g.value["root"]) == arms[arm][key],
                "Captured arm journal return identity",
            )
    result = {
        "provenance": provenance,
        "gold": gold,
        "reviewed_replay": replay,
        "design": design,
        "resources": by_id,
        "arms": arms,
        "native": native,
        "journal": j,
        "stage_b_trace": load(CAPTURE / "trace.json"),
        "costs": load(CAPTURE / "costs.json"),
        "finalization": load(CAPTURE / "finalization_cost.json"),
        "input_gold_sha256": sha(encoded(gold)),
        "native_validation": {
            "status": "PASS",
            "index_builds": 1,
            "queries": 6,
            "reference_query_executions": 1,
            "candidate_counts": {q: len(a["matches"]) for q, a in arms["A"].items()},
            "positive_occurrences": sum(len(a["matches"]) for a in arms["A"].values()),
            "native_retries": 0,
            "failures": 0,
            "classification_application": "PASS",
            "reference": "UNCHANGED",
        },
    }
    result["input_hashes"] = {
        key: sha(encoded(result[key]))
        for key in (
            "gold",
            "design",
            "resources",
            "native",
            "journal",
            "stage_b_trace",
            "costs",
            "finalization",
            "provenance",
            "native_validation",
            "reviewed_replay",
        )
    }
    return result
