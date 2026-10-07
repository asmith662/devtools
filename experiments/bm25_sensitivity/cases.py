# Copyright (c) 2026
# ruff: noqa: C901, COM812, EM101, TRY003, PLR0912, PLR0915, PLR2004, S301 -- six explicit schemas; pinned trusted native pickle only

"""Read pinned historical native frames; never substitute today's source."""

from __future__ import annotations

import gzip
import itertools
import json
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from devtools.context.localization.identity import (
    LocalizationObligationIdentity,
    LocalizationTaskIdentity,
)
from experiments.bm25_sensitivity.protocol import BASELINE
from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    read_json,
)
from experiments.retrieval_diagnostics.models import Frame, Judgment

if TYPE_CHECKING:
    from devtools.context.repository.document import RepositoryTextDocumentCollection
    from devtools.context.repository.snapshot import RepositorySnapshot
    from devtools.context.retrieval.lexical.index import (
        RepositoryTextLexicalInvertedIndex,
    )
    from experiments.retrieval_diagnostics.models import Label

HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Case:
    """Bind exact native input to independently judged cell/alternative semantics."""

    number: int
    snapshot: RepositorySnapshot
    documents: RepositoryTextDocumentCollection
    index: RepositoryTextLexicalInvertedIndex | None
    task: str
    queries: tuple[tuple[str, str, str], ...]
    frame: Frame
    judgments: dict[str, tuple[Judgment, ...]]
    alternatives: dict[str, tuple[tuple[str, tuple[str, ...]], ...]]
    sufficient_unions: tuple[tuple[str, ...], ...]
    historical: dict[str, tuple[tuple[str, float], ...]]
    hashes: dict[str, str]


def load(number: int) -> Case:
    """Validate frozen file hashes before loading trusted committed pickle data."""
    audit = next(
        r for r in read_json(HERE / "protocol.json")["cases"] if r["case"] == number
    )
    directory = ROOT / "experiments/codex_dogfood" / f"case_{number:04d}"
    for name, sha in audit["input_sha256"].items():
        if digest(binary(directory / name)) != sha:
            raise ValueError("Historical pinned artifact differs.")
    native = pickle.loads(gzip.decompress(binary(directory / "inputs.pkl.gz")))
    if number == 9:
        request = None
        snapshot, documents = native["snapshot"], native["documents"]
        queries = tuple(
            (q.identity.value, q.obligation.value, q.text) for q in native["queries"]
        )
        task, task_identity, index = (
            read_json(directory / "treatment.json")["full_task_query"],
            native["task"].identity,
            None,
        )
        g = read_json(directory / "adjudication/judgments.json")
    else:
        request = (
            native
            if number == 4
            else native["lexical_request" if number == 7 else "request"]
        )
        snapshot = request.snapshot
        index = request.index
        documents = index.corpus_statistics.collection_analysis.document_collection
        queries = tuple(
            (q.identity.value, q.obligation.value, q.text)
            for q in request.obligation_queries
        )
        task, task_identity = request.full_task_query, request.task.identity
        g = read_json(
            directory
            / "adjudication"
            / ("blind_judgments.json" if number == 4 else "judgments.json")
        )
        if (request.settings.k1, request.settings.b) != BASELINE[:2]:
            raise ValueError("Historical BM25 settings differ.")
    frame = Frame(snapshot.repository_id, snapshot.id, documents.corpus.id)
    identity = g.get("frame", g)
    task_field = {
        4: "task_text",
        5: "task_text",
        6: "development_task",
        7: "task",
        8: "exact_task",
        9: "task",
    }[number]
    if identity["task_identity"] != task_identity.value or g[task_field] != task:
        raise ValueError("Gold/native task identity or exact text differs.")
    if (
        identity["repository_id"] != str(frame.repository)
        or identity.get("snapshot_id", identity.get("repository_snapshot_id"))
        != str(frame.snapshot)
        or identity.get("corpus_id", identity.get("eligible_frame_identity"))
        != str(frame.corpus)
    ):
        raise ValueError("Gold/native frame identity differs.")
    resource_map = {d.resource.address.value: d.resource for d in documents.documents}
    if len(resource_map) != len(documents.documents) or any(
        d.resource != snapshot.resource_at(d.resource.address)
        for d in documents.documents
    ):
        raise ValueError("Native corpus/snapshot occurrence mismatch.")
    labels: dict[tuple[str, str], str] = {}
    units: dict[tuple[str, str], set[str]] = {}
    alternatives: dict[str, tuple[tuple[str, tuple[str, ...]], ...]] = {}

    def alt(
        ob: str,
        choices: list[dict[str, Any]],
        uid_to_address: dict[str, str],
        member_key: str,
        identity_key: str = "identity",
    ) -> None:
        alternatives[ob] = tuple(
            (a[identity_key], tuple(sorted({uid_to_address[u] for u in a[member_key]})))
            for a in choices
        )

    if number == 4:
        for r in g["resource_matrix"]:
            labels.update(
                {(o, r["path"]): label for o, label in r["dispositions"].items()}
            )
        for o in g["obligations"]:
            ob = o["frozen_obligation"]["identity"]
            mapping = {u["unit_identity"]: u["path"] for u in o["information_units"]}
            for u in o["information_units"]:
                if u["category"] == "REQUIRED":
                    units.setdefault((ob, u["path"]), set()).add(u["unit_identity"])
            alt(ob, o["acceptable_witness_alternatives"], mapping, "all_of")
    elif number in (5, 8):
        rows = g[
            "resource_obligation_judgments" if number == 5 else "resource_judgments"
        ]
        for r in rows:
            ob = r["obligation_identity" if number == 5 else "obligation"]
            address = r["resource_identity" if number == 5 else "resource"]["address"]
            labels[ob, address] = r["judgment"]
            units[ob, address] = set(r["required_units"])
        mapping = {
            u["identity"]: u["resource_identity" if number == 5 else "resource"][
                "address"
            ]
            for u in g["information_units"]
        }
        for o in g["obligations"]:
            ob = o["frozen_obligation"]["identity"]
            alt(
                ob,
                o[
                    "acceptable_witness_alternatives"
                    if number == 5
                    else "acceptable_alternatives"
                ],
                mapping,
                "all_members" if number == 5 else "all_units",
            )
    elif number in (6, 7):
        mapping = (
            {
                uid: u["resource_identity"]["address"]
                for uid, u in g["information_units"].items()
            }
            if number == 6
            else {u["unit_id"]: u["address"] for u in g["information_units"]}
        )
        for o in g["judgments" if number == 6 else "obligations"]:
            ob = o["identity"]
            alt(
                ob,
                o["acceptable_witness_alternatives"],
                mapping,
                "all" if number == 6 else "members",
                "identity" if number == 6 else "alternative_id",
            )
            for address in resource_map:
                labels[ob, address] = "UNNECESSARY"
            if number == 6:
                if o["default_resource_classification"] != "UNNECESSARY":
                    raise ValueError("Unsupported gold default.")
                for r in o["helpful_resources"]:
                    labels[ob, r["resource_identity"]["address"]] = "HELPFUL_ONLY"
                for a in o["acceptable_witness_alternatives"]:
                    for u in a["all"]:
                        labels[ob, mapping[u]] = "REQUIRED"
                        units.setdefault((ob, mapping[u]), set()).add(u)
        if number == 7:
            if g["resource_classifications"]["default"] != "UNNECESSARY":
                raise ValueError("Unsupported gold default.")
            for r in g["resource_classifications"]["overrides"]:
                address = "/".join(r["resource_occurrence_identity"].split("/")[2:-1])
                labels[r["obligation"], address] = r["judgment"]
                units[r["obligation"], address] = set(r.get("unit_ids", []))
    else:
        for c in g["cells"]:
            labels[c["obligation"], c["resource"]["address"]] = c["label"]
            units[c["obligation"], c["resource"]["address"]] = set(c["required_units"])
        for o in g["obligations"]:
            alternatives[o["identity"]] = tuple(
                (
                    a["identity"],
                    tuple(sorted({w["resource"]["address"] for w in a["witnesses"]})),
                )
                for a in o["acceptable_alternatives"]
            )
    obligations = {ob for _, ob, _ in queries}
    if (
        len(obligations) != len(queries)
        or obligations != alternatives.keys()
        or len(labels) != len(obligations) * len(resource_map)
        or set(labels) != {(o, p) for o in obligations for p in resource_map}
    ):
        raise ValueError("Historical full query/gold coverage differs.")
    judgments = {
        o: tuple(
            Judgment(
                frame,
                r,
                LocalizationObligationIdentity(
                    LocalizationTaskIdentity(task_identity.value), o
                ),
                cast("Label", labels[o, p]),
                tuple(sorted(units.get((o, p), set()))),
            )
            for p, r in resource_map.items()
        )
        for o in sorted(obligations)
    }
    for ob, choices in alternatives.items():
        if not choices or any(
            not members or any(labels[ob, p] != "REQUIRED" for p in members)
            for _, members in choices
        ):
            raise ValueError("Gold alternative member is not REQUIRED in frame.")
    unions = tuple(
        sorted(
            {
                tuple(sorted({p for _, members in choice for p in members}))
                for choice in itertools.product(
                    *(alternatives[o] for o in sorted(obligations))
                )
            }
        )
    )
    historical = _historical(directory, number, queries)
    return Case(
        number,
        snapshot,
        documents,
        index,
        task,
        queries,
        frame,
        judgments,
        alternatives,
        unions,
        historical,
        audit["input_sha256"],
    )


def _historical(
    directory: Path, number: int, queries: tuple[tuple[str, str, str], ...]
) -> dict[str, tuple[tuple[str, float], ...]]:
    """Project native positive rank/score rows for baseline equivalence only."""
    r = (
        json.loads(gzip.decompress(binary(directory / "results.json.gz")))
        if number == 9
        else read_json(directory / "retrieval.json")
    )
    if number == 9:
        lanes = [("global", r["arms"]["A"]["global"]["rows"])] + [
            (ob, r["arms"]["A"][identity]["rows"]) for identity, ob, _ in queries
        ]
    elif number in (4, 5):
        lanes = [
            ("global" if i == 0 else lane["obligation_identity"], lane["matches"])
            for i, lane in enumerate(r["lanes"])
        ]
    elif number == 6:
        lanes = [("global", r["global_lane"]["matches"])] + [
            (lane["obligation_identity"], lane["matches"])
            for lane in r["obligation_lanes"]
        ]
    elif number == 7:
        lanes = [
            (
                "global"
                if lane["identity"] == "global"
                else next(
                    o for identity, o, _ in queries if identity == lane["identity"]
                ),
                lane["matches"],
            )
            for lane in r["lanes"]
        ]
    else:
        lanes = [("global", r["global"]["matches"])] + [
            (
                next(
                    ob
                    for identity, ob, _ in queries
                    if identity == lane["query_identity"]
                ),
                lane["matches"],
            )
            for lane in r["obligations"]
        ]
    output = {}
    for ob, rows in lanes:
        output[ob] = tuple(
            (
                m.get(
                    "address",
                    m.get(
                        "resource_address",
                        m.get("resource", m.get("resource_identity", {})).get(
                            "address"
                        ),
                    ),
                ),
                m["score"],
            )
            for m in rows
        )
    return output
