"""Authenticate sealed development evidence using inert journal graphs only.

No pickle loading, frame/index preparation, retrieval, scorer, model, service,
confirmation or reserve operation is invoked. Physical import bytes and the
historical Stage A/B normalized text hash scopes remain distinct.
"""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, ANN401, D103, COM812, PLR2004
import asyncio
import gzip
import json
from collections import Counter
from itertools import pairwise
from pathlib import Path, PurePosixPath
from types import SimpleNamespace
from typing import Any

from experiments.bm25f.trace import serialize
from experiments.codex_dogfood.case_0009.artifacts import binary, git, json_bytes

# Existing inert reader for the established native graph codec; importing it
# reads no Case 0014 data and performs no semantic review or outcome comparison.
from experiments.codex_dogfood.case_0014.stage_d.authentication import Graph, unpack
from experiments.codex_dogfood.case_0015.adjudication.reviewed import git_identity
from experiments.codex_dogfood.case_0015.adjudication.reviewed import materialize as m
from experiments.codex_dogfood.case_0015.stage_b import reporting as retained
from experiments.codex_dogfood.case_0015.stage_b import validation as arithmetic

encoded, sha, require, load = m.encoded, m.sha, m.require, m.load
ROOT = Path(__file__).resolve().parent
CASE = ROOT.parent
REPO = CASE.parents[2]
CAPTURE = CASE / "stage_b/attempts/case-0015-stage-b-2"
STAGE_A = "d7e28de0e103bdf0e494a0156311fa1c14b6c9f8"
RECOVERY = "cc9aaef40dec218e63fae7de835298ef76bd241f"
STAGE_B = "a4e3f6ee2446e0b54ec1477c0fab69abfbd4c716"
BLIND = "6646f369af5e4b7908288d5c2af673148c2805c9"
REVIEWED = "c29d73cc48f1428eb93a184261ce815cf4e6b1c0"
STAGE_B_HASH = "b7b23678205360384692d4a8934e25fba3572275bcd1385d0ff32f830651e572"


def relative(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


async def checkpoints() -> Any:
    sequence = [STAGE_A, RECOVERY, STAGE_B, BLIND, REVIEWED, "HEAD"]
    for ancestor, child in pairwise(sequence):
        require(
            (await git("merge-base", ancestor, child)).decode().strip() == ancestor,
            "Exact checkpoint ancestry",
        )
    stage_a = load(CASE / "integrity.json")
    require(
        sha(binary(CASE / "integrity.json"))
        == "86438745a88c79fa0fafd132f454fcc807de0afc93d7d01a210f740338896619",
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
        require(
            sha(binary(REPO / name)) == expected
            and sha(await git("show", STAGE_A + ":" + name)) == expected,
            "Frozen Stage A implementation: " + name,
        )
    recovery_path = CASE / "recovery/integrity.json"
    require(
        await git("show", RECOVERY + ":" + relative(recovery_path))
        == binary(recovery_path),
        "Recovery seal",
    )
    recovery = load(recovery_path)
    for name, expected in recovery["implementation"].items():
        # Later capture/packet publication metadata has legitimate successors;
        # authenticate recovery's own committed blobs without reverting them.
        require(
            sha(await git("show", RECOVERY + ":" + name)) == expected,
            "Recovery implementation blob: " + name,
        )
    failed = CASE / "stage_b/attempts/case-0015-stage-b-1"
    for name, expected in recovery["failed_audit"]["sha256"].items():
        require(
            sha(binary(failed / name)) == expected
            and sha(await git("show", RECOVERY + ":" + relative(failed / name)))
            == expected,
            "Failed audit isolation: " + name,
        )
    require(
        not (failed / "execution_completed.json").exists(),
        "Attempt 1 must remain failed audit only",
    )
    seal = load(CAPTURE / "integrity.json")
    require(
        sha(binary(CAPTURE / "integrity.json")) == STAGE_B_HASH,
        "Authoritative Stage B integrity",
    )
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
    await git_identity.verify(REVIEWED)
    for name in (
        *m.outputs(),
        "materialize.py",
        "git_identity.py",
        "test_materialize.py",
    ):
        path = m.ROOT / name
        require(
            await git("show", REVIEWED + ":" + relative(path)) == path.read_bytes(),
            "Committed reviewed publication: " + name,
        )
    for name, expected in load(m.ADJ / "primary/stage_c_hashes.json")[
        "input_sha256"
    ].items():
        path = m.PACKET / name
        require(
            sha(path.read_bytes()) == expected
            and sha(await git("show", BLIND + ":" + relative(path))) == expected,
            "Committed original blind packet: " + name,
        )
    return {
        "stage_a": STAGE_A,
        "recovery": RECOVERY,
        "stage_b": STAGE_B,
        "blind_packet": BLIND,
        "reviewed_gold": REVIEWED,
        "ancestry": "PASS",
        "stage_b_integrity_sha256": STAGE_B_HASH,
        "primary_sha256": m.HASHES,
        "reviewed_hashes_sha256": sha((m.ROOT / "reviewed_hashes.json").read_bytes()),
        "attempt_1": "FAILED_AUDIT_ONLY; ISOLATED; NOT_LOADED_AS_TREATMENT",
    }


def journal(marker: Any) -> tuple[Any, dict[str, Any]]:
    require(
        load(CAPTURE / "execution.claim") == {"execution": marker["execution"]},
        "Exactly-once claim",
    )
    context = load(CAPTURE / "native_context.json")
    require(
        context["marker_sha256"] == sha(binary(CAPTURE / "execution_started.json")),
        "Journal initial context",
    )
    unpack(context["native"])
    unpack(context["canonical"])
    chain = sha(binary(CAPTURE / "native_context.json"))
    events = sorted(
        [(load(p), p) for p in (CAPTURE / "operations").glob("*.json")],
        key=lambda pair: pair[0]["event"],
    )
    operations: list[Any] = []
    active: set[str] = set()
    graphs = {}
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
            unpack(value["native"])  # Hash authenticated, never unpickled or executed.
            graphs[op["identity"]] = Graph(json.loads(canonical))
            canonical_hashes[op["identity"]] = sha(canonical)
            operations[sequence - 1] = op
            active.remove(op["identity"])
        chain = sha(binary(path))
    schedule = [
        "frame:prepare",
        "fields:prepare",
        "index:native-prepare",
        "statistics:union-prepare",
        *[f"query:Q{i}:{arm}" for i in range(1, 7) for arm in "AB"],
        "query:reference",
    ]
    require(
        not active
        and len(operations) == 17
        and len(events) == 34
        and [o["identity"] for o in operations]
        == schedule
        == marker["operation_schedule"],
        "17 complete scheduled ENTERED/RETURNED pairs",
    )
    require(
        load(CAPTURE / "execution_completed.json")
        == {
            "execution": marker["execution"],
            "journal_chain_sha256": chain,
            "operations": schedule,
        },
        "Exactly-once completion",
    )
    return {
        "status": "PASS",
        "pairs": 17,
        "events": 34,
        "native_retries": 0,
        "failures": 0,
        "chain_sha256": chain,
        "operations": operations,
        "canonical_return_sha256": canonical_hashes,
    }, graphs


def decoded(value: Any) -> Any:
    if isinstance(value, dict):
        if set(value) == {"float_hex"}:
            return float.fromhex(value["float_hex"])
        return {k: decoded(v) for k, v in value.items()}
    if isinstance(value, list):
        return [decoded(v) for v in value]
    return value


def surface(name: str) -> Any:
    raw = gzip.decompress((CAPTURE / name).read_bytes())
    value = decoded(json.loads(raw))
    require(serialize(value) == raw, "Exact canonical float.hex surface: " + name)
    return value


def native_collection(g: Any, ref: Any, resources: Any) -> None:
    collection = g.fields(ref)
    docs = g.items(collection["documents"])
    require(len(docs) == len(resources), "Native collection cardinality")
    corpus = g.fields(collection["corpus"])
    require(
        g.plain(corpus["id"])["value"] == next(iter(resources.values()))["corpus_id"],
        "Native corpus identity",
    )
    for document_ref, expected in zip(docs, resources.values(), strict=True):
        document = g.fields(document_ref)
        resource = g.plain(document["resource"])
        require(
            g.plain(document["id"])["value"] == expected["document_identity"]
            and g.plain(document["repository_id"])["value"] == expected["repository_id"]
            and resource["address"]["value"] == expected["address"]
            and resource["content_identity"]["value"] == expected["content_identity"]
            and resource["content"] == expected["content"],
            "Native collection exact document/resource/content",
        )


def native_statistics(
    g: Any, content: Any, filename: Any, fields: Any, statistics: Any
) -> None:
    for name, ref, average_key in (
        ("CONTENT", content, "content_average_length"),
        ("FILENAME", filename, "filename_average_length"),
    ):
        index = g.fields(ref)
        stats = g.fields(index["corpus_statistics"]) if name == "CONTENT" else index
        require(
            stats["average_document_length"] == fields[average_key],
            "Native statistics average",
        )
        if name == "CONTENT":
            require(stats["document_count"] == fields["N"], "Native statistics N")
        docs = g.items(stats["document_statistics"])
        require(len(docs) == fields["N"], "Native statistics document count")
        for statistics_ref, expected in zip(docs, fields["documents"], strict=True):
            row = g.fields(statistics_ref)
            analysis = g.fields(row["analysis"])
            document = g.fields(analysis["document"])
            frequencies = g.plain(row["term_frequencies"])
            require(
                g.plain(document["id"])["value"] == expected["document_identity"]
                and row["document_length"] == expected[name]["length"]
                and g.plain(analysis["observations"]) == expected[name]["observations"]
                and {t["normalized_term"]: len(t["observations"]) for t in frequencies}
                == expected[name]["term_frequencies"],
                "Native exact full field observations/length/tf",
            )
            require(
                all(
                    t["observations"]
                    == [
                        o
                        for o in expected[name]["observations"]
                        if o["normalized_term"] == t["normalized_term"]
                    ]
                    for t in frequencies
                ),
                "Native grouped frequency observations",
            )
            if name == "FILENAME":
                require(
                    analysis["filename_stem"] == expected[name]["stem"],
                    "Native filename stem",
                )
        actual_df = {
            t["normalized_term"]: t["document_frequency"]
            for t in g.plain(stats["document_frequencies"])
        }
        require(
            actual_df
            == {t: len(v[name]) for t, v in statistics["terms"].items() if v[name]},
            "Native exact field df",
        )


def native_preparation(
    graphs: Any, resources: Any, fields: Any, statistics: Any, frame: Any
) -> None:
    for key, collection_key in (
        ("frame:prepare", "documents"),
        ("index:native-prepare", "collection"),
    ):
        g = graphs[key]
        root = g.fields(g.value["root"])
        native_collection(g, root[collection_key], resources)
        snapshot = g.fields(root["snapshot"])
        require(
            g.plain(snapshot["id"])["value"] == frame["snapshot_id"]
            and g.plain(snapshot["repository_id"])["value"] == frame["repository_id"],
            "Native snapshot identity",
        )
        if key == "index:native-prepare":
            native_statistics(g, root["content"], root["filename"], fields, statistics)
    g = graphs["fields:prepare"]
    root = g.fields(g.value["root"])
    content = g.fields(root["content"])
    native_collection(g, content["document_collection"], resources)
    for ref, expected in zip(
        g.items(content["analyses"]), fields["documents"], strict=True
    ):
        analysis = g.fields(ref)
        require(
            g.plain(analysis["observations"]) == expected["CONTENT"]["observations"],
            "Shared content preparation observations",
        )


def native_projection(g: Any, resources: Any) -> Any:
    lane = g.fields(g.value["root"])
    require(
        g.plain(lane["settings"]) == {"b": 0.75, "k1": 1.2}
        and lane["maximum_results"] == 515,
        "Native settings/full bound",
    )
    rows = []
    for rank, ref in enumerate(g.items(lane["matches"]), 1):
        match = g.fields(ref)
        document = g.fields(
            g.fields(g.fields(match["document_statistics"])["analysis"])["document"]
        )
        rid = g.plain(document["id"])["value"]
        resource = g.plain(document["resource"])
        expected = resources[rid]
        require(
            resource["content"] == expected["content"]
            and resource["address"]["value"] == expected["address"]
            and resource["content_identity"]["value"] == expected["content_identity"]
            and g.plain(document["repository_id"])["value"]
            == expected["repository_id"],
            "Native exact resource/content identity",
        )
        rows.append(
            {
                "rank": rank,
                "address": expected["address"],
                "document_identity": rid,
                "content_identity": expected["content_identity"],
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
                "content_terms": g.plain(match["term_contributions"]),
                "filename_terms": g.plain(match["filename_term_contributions"]),
            }
        )
    return {
        "query": g.plain(lane["query"]),
        "settings": g.plain(lane["settings"]),
        "maximum_results": lane["maximum_results"],
        "matches": rows,
    }


def validate_fields(fields: Any, union: Any, statistics: Any, resources: Any) -> None:
    require(fields["N"] == len(resources) == 515, "Canonical field N")
    membership: dict[str, Any] = {}
    for position, (rid, resource) in enumerate(resources.items()):
        row = fields["documents"][position]
        require(
            row["collection_position"] == position
            and all(
                row[k] == resource[k]
                for k in (
                    "repository_id",
                    "snapshot_id",
                    "corpus_id",
                    "address",
                    "document_identity",
                    "content_identity",
                )
            ),
            "Qualified field frame",
        )
        for field, text in (
            ("CONTENT", resource["content"]),
            ("FILENAME", PurePosixPath(resource["address"]).stem),
        ):
            observations = arithmetic.observations(text)
            require(
                row[field]["observations"] == observations
                and row[field]["length"] == len(observations)
                and row[field]["term_frequencies"]
                == dict(Counter(o["normalized_term"] for o in observations)),
                "Canonical field observations/length/tf",
            )
            if field == "FILENAME":
                require(row[field]["stem"] == text, "Filename stem field")
            for term in row[field]["term_frequencies"]:
                membership.setdefault(term, {"CONTENT": [], "FILENAME": []})[
                    field
                ].append(rid)
    positions = {rid: i for i, rid in enumerate(resources)}
    terms = {
        t: {
            **v,
            "union": sorted(
                set(v["CONTENT"]) | set(v["FILENAME"]), key=positions.__getitem__
            ),
            "df_union": len(set(v["CONTENT"]) | set(v["FILENAME"])),
        }
        for t, v in sorted(membership.items())
    }
    require(
        union == {"N": 515, "terms": terms}, "Exact union document-once membership/DF"
    )
    for field, key in (
        ("CONTENT", "content_average_length"),
        ("FILENAME", "filename_average_length"),
    ):
        require(
            fields[key] == sum(r[field]["length"] for r in fields["documents"]) / 515,
            "Field average includes empty fields",
        )
    expected = {
        "N": 515,
        "content_average_length": fields["content_average_length"],
        "filename_average_length": fields["filename_average_length"],
        "terms": {
            t: {
                **v,
                "content_df": len(v["CONTENT"]),
                "filename_df": len(v["FILENAME"]),
                "content_idf": arithmetic.idf(515, len(v["CONTENT"])),
                "filename_idf": arithmetic.idf(515, len(v["FILENAME"])),
                "idf_union": arithmetic.idf(515, v["df_union"]),
            }
            for t, v in terms.items()
        },
    }
    arithmetic.equal(statistics, expected, "Exact native/union statistics")


def reconstruct_native(fields: Any, union: Any, query: Any) -> Any:
    rows = []
    for row in fields["documents"]:
        channels: dict[str, Any] = {"CONTENT": [], "FILENAME": []}
        for field, key in (
            ("CONTENT", "content_average_length"),
            ("FILENAME", "filename_average_length"),
        ):
            for term in query["normalized_terms"]:
                tf = row[field]["term_frequencies"].get(term, 0)
                if not tf:
                    continue
                df = len(union["terms"][term][field])
                inverse = arithmetic.idf(515, df)
                average = fields[key]
                numerator = tf * (1.2 + 1)
                denominator = tf + 1.2 * (
                    1 - 0.75 + 0.75 * row[field]["length"] / average
                )
                channels[field].append(
                    {
                        "normalized_term": term,
                        "term_frequency": tf,
                        "document_frequency": df,
                        "inverse_document_frequency": inverse,
                        "document_length": row[field]["length"],
                        "average_document_length": average,
                        "contribution": inverse * numerator / denominator,
                    }
                )
        cs = (
            sum(t["contribution"] for t in channels["CONTENT"])
            if channels["CONTENT"]
            else 0.0
        )
        fs = sum(t["contribution"] for t in channels["FILENAME"])
        score = cs + 0.25 * fs
        if score > 0:
            rows.append(
                {
                    k: row[k]
                    for k in (
                        "collection_position",
                        "address",
                        "document_identity",
                        "content_identity",
                    )
                }
                | {
                    "score": score,
                    "content_score": cs,
                    "filename_score": fs,
                    "filename_weight": 0.25,
                    "weighted_filename_score": 0.25 * fs,
                    "content_terms": channels["CONTENT"],
                    "filename_terms": channels["FILENAME"],
                }
            )
    rows.sort(key=lambda r: (-r["score"], r["collection_position"]))
    for rank, row in enumerate(rows, 1):
        row.pop("collection_position")
        row["rank"] = rank
    return rows


def validate_arms(data: Any, graphs: Any) -> None:
    design, resources, fields, union = (
        data[k] for k in ("design", "resources", "fields", "union")
    )
    frame = data["gold"]["frame"]
    # Provenance-only adapter for the existing pure reconstruction validator;
    # no native FieldState or index is built, and validate_b calls no scorer.
    provenance: Any = SimpleNamespace(
        snapshot=SimpleNamespace(
            id=frame["snapshot_id"], repository_id=frame["repository_id"]
        ),
        collection=SimpleNamespace(corpus=SimpleNamespace(id=frame["corpus_id"])),
    )
    for i, query in enumerate(design["queries"], 1):
        q, o = f"Q{i}", f"O{i}"
        require(
            query["identity"]
            == {"task": {"value": design["task_identity"]}, "value": q}
            and query["obligation"]
            == {"task": {"value": design["task_identity"]}, "value": o},
            "Frozen query/obligation join",
        )
        a, b = data["arms"]["A"][q], data["arms"]["B"][q]
        for lane in (a, b):
            require(
                lane["case"] == design["case"]
                and lane["task_identity"] == design["task_identity"]
                and lane["query_identity"] == query["identity"]
                and lane["obligation_identity"] == query["obligation"]
                and lane["query"] == query["analysis"]
                and all(lane["frame"][k] == frame[k] for k in frame),
                "Exact lane case/task/obligation/frame",
            )
            ids = []
            for row in lane["matches"]:
                rid = row["document_identity"]
                ids.append(rid)
                require(
                    all(
                        row[k] == resources[rid][k]
                        for k in ("address", "document_identity", "content_identity")
                    ),
                    "Exact resource join",
                )
            require(len(ids) == len(set(ids)), "No duplicate candidate joins")
        require(
            {r["document_identity"] for r in a["matches"]}
            == {r["document_identity"] for r in b["matches"]},
            "Equal candidates, no additions/losses",
        )
        native = native_projection(graphs[f"query:{q}:A"], resources)
        g = graphs[f"query:{q}:A"]
        lane = g.fields(g.value["root"])
        native_statistics(
            g, lane["index"], lane["filename_index"], fields, data["statistics"]
        )
        arithmetic.equal(
            {k: a[k] for k in native}, native, "Authentic native A journal projection"
        )
        arithmetic.equal(
            a["matches"],
            reconstruct_native(fields, union, query),
            "Exact native A arithmetic/ranks/ties",
        )
        g = graphs[f"query:{q}:B"]
        captured = g.plain(g.value["root"])
        arithmetic.equal(
            {k: b[k] for k in captured}, captured, "Exact B journal projection"
        )
        arithmetic.validate_b(b, provenance, fields, union, query)
        comparison = {"A": a["matches"], "B": b}
        diagnostic, _ = retained.decomposition(comparison)
        arithmetic.equal(
            data["decomposition"][q], diagnostic, "Captured decomposition exact replay"
        )
        arithmetic.equal(
            data["contributions"][q]["candidates"],
            retained.joined(comparison, union),
            "Exact captured joined contributions",
        )
        arithmetic.equal(
            data["top_k"][q],
            retained.pairwise(a["matches"], b["matches"]),
            "Already captured top-K mechanical replay",
        )
    native_ref = native_projection(graphs["query:reference"], resources)
    g = graphs["query:reference"]
    lane = g.fields(g.value["root"])
    native_statistics(
        g, lane["index"], lane["filename_index"], fields, data["statistics"]
    )
    reference = data["reference"]
    arithmetic.equal(
        {k: reference[k] for k in native_ref},
        native_ref,
        "Unchanged captured native reference",
    )
    query = {
        "analysis": design["global_reference_lane"]["analysis"],
        "normalized_terms": list(
            dict.fromkeys(
                o["normalized_term"] for o in reference["query"]["observations"]
            )
        ),
    }
    require(reference["query"] == query["analysis"], "Frozen reference analysis")
    arithmetic.equal(
        reference["matches"],
        reconstruct_native(fields, union, query),
        "Native reference exact arithmetic",
    )


def authenticate() -> Any:
    provenance = asyncio.run(checkpoints())
    replay = m.verify()
    gold = load(m.ROOT / "reviewed_gold.json")
    design = load(CASE / "protocol.json")
    marker = load(CAPTURE / "execution_started.json")
    require(
        marker["execution"] == "case-0015-stage-b-2"
        and marker["stage_a"] == STAGE_A
        and marker["case"] == gold["primary"]["case"]
        and marker["recovery_checkpoint"] == RECOVERY
        and marker["protocol_sha256"] == sha(binary(CASE / "protocol.json")),
        "Authoritative execution/task identity",
    )
    require(
        all(marker["frame"][k] == gold["frame"][k] for k in gold["frame"]),
        "Exact repository/snapshot/corpus join",
    )
    resources = json.loads(gzip.decompress((CASE / "resources.json.gz").read_bytes()))
    by_id = {r["document_identity"]: r for r in resources}
    require(
        len(by_id) == len(resources) == 515
        and [{k: r[k] for k in gold["resource_bindings"][0]} for r in resources]
        == gold["resource_bindings"],
        "Complete exact resource/content frame join",
    )
    j, graphs = journal(marker)
    require(
        load(CAPTURE / "validation.json")["mechanical_capture"] == "PASS",
        "Stage B validation",
    )
    data = {
        "provenance": provenance,
        "gold": gold,
        "reviewed_replay": replay,
        "design": design,
        "resources": by_id,
        "journal": j,
        "arms": {a: surface("arm_" + a.lower() + ".json.gz") for a in "AB"},
        **{
            key: surface(name + ".json.gz")
            for key, name in (
                ("fields", "fields"),
                ("statistics", "native_statistics"),
                ("union", "union_statistics"),
                ("decomposition", "decomposition"),
                ("contributions", "contributions"),
                ("top_k", "top_k"),
                ("reference", "reference"),
            )
        },
        "costs": load(CAPTURE / "costs.json"),
    }
    validate_fields(data["fields"], data["union"], data["statistics"], by_id)
    native_preparation(graphs, by_id, data["fields"], data["statistics"], gold["frame"])
    g = graphs["statistics:union-prepare"]
    arithmetic.equal(data["union"], g.plain(g.value["root"]), "Union captured return")
    validate_arms(data, graphs)
    durations = {o["identity"]: o["runtime_ns"] for o in j["operations"]}
    costs = data["costs"]
    require(
        costs["shared_operations_ns"]
        == {k: durations[k] for k in marker["operation_schedule"][:4]}
        and costs["shared_charged_equally_ns"]
        == sum(costs["shared_operations_ns"].values()),
        "Shared costs, no double count",
    )
    for arm, key in (
        ("A", "arm_a_native_retrieval_ns"),
        ("B", "arm_b_bm25f_scoring_ns"),
    ):
        require(
            costs[key] == sum(durations[f"query:Q{i}:{arm}"] for i in range(1, 7))
            and costs["charged_" + arm + "_ns"]
            == costs["shared_charged_equally_ns"] + costs[key],
            "Arm charged costs",
        )
    require(
        costs["reference_ns"] == durations["query:reference"]
        and costs["query_operations_ns"]
        == {k: v for k, v in durations.items() if k.startswith("query:")}
        and all(costs[k] == v for k, v in load(CAPTURE / "capture_costs.json").items())
        and costs["derived_publication"] == load(CAPTURE / "publication_costs.json"),
        "Descriptive cost scope",
    )
    data["native_validation"] = {
        "status": "PASS",
        "native_arm_a": "AUTHENTIC",
        "field_observations": "EXACT",
        "statistics": "EXACT",
        "bm25f_reconstruction": "EXACT",
        "decomposition": "EXACT",
        "candidate_identity": "EXACT",
        "candidate_counts": {
            q: len(v["matches"]) for q, v in data["arms"]["A"].items()
        },
        "reference": "UNCHANGED",
        "scientific_reruns": 0,
        "native_operations": 0,
    }
    require(
        list(data["native_validation"]["candidate_counts"].values())
        == [290, 307, 156, 221, 425, 408],
        "Candidate counts",
    )
    return data
